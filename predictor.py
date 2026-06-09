from datetime import datetime, timedelta
import statistics

class AviatorPredictor:
    def __init__(self, velas_data):
        """
        Inicializa o preditor com dados de velas
        velas_data: lista de tuplas (id, valor, tipo, data_hora, is_crash)
        """
        self.velas = velas_data
        self.valores = [v[1] for v in velas_data]
        self.crashes = [i for i, v in enumerate(velas_data) if v[4] == 1]
    
    def calcular_intervalo_crashes(self):
        """Calcula o intervalo entre crashes em rodadas"""
        if len(self.crashes) < 2:
            return None
        
        intervalos = []
        for i in range(1, len(self.crashes)):
            intervalo = self.crashes[i] - self.crashes[i-1]
            intervalos.append(intervalo)
        
        try:
            desvio = statistics.stdev(intervalos) if len(intervalos) > 1 else 0
        except:
            desvio = 0
        
        return {
            'media': statistics.mean(intervalos),
            'mediana': statistics.median(intervalos),
            'min': min(intervalos),
            'max': max(intervalos),
            'desvio_padrao': desvio,
            'todos_intervalos': intervalos
        }
    
    def prever_proximo_crash(self):
        """Prevê quando será o próximo crash baseado no histórico"""
        if len(self.crashes) == 0:
            return {
                'probabilidade_crash': 0.5,
                'proximas_rodadas': 10,
                'confianca': 'BAIXA - Sem histórico de crashes'
            }
        
        intervalo_info = self.calcular_intervalo_crashes()
        
        if intervalo_info is None:
            return {
                'probabilidade_crash': 0.5,
                'proximas_rodadas': 10,
                'confianca': 'BAIXA - Apenas 1 crash registrado'
            }
        
        # Próximo crash estimado na média dos intervalos
        proximas_rodadas = int(round(intervalo_info['media']))
        
        # Calcular confiança baseada na consistência
        cv = (intervalo_info['desvio_padrao'] / intervalo_info['media']) if intervalo_info['media'] > 0 else 0
        
        if cv < 0.3:
            confianca = 'ALTA'
        elif cv < 0.7:
            confianca = 'MÉDIA'
        else:
            confianca = 'BAIXA'
        
        # Probabilidade de crash em qualquer rodada
        taxa_crash = len(self.crashes) / len(self.velas) if len(self.velas) > 0 else 0
        
        return {
            'probabilidade_crash': taxa_crash * 100,
            'proximas_rodadas': proximas_rodadas,
            'confianca': confianca,
            'intervalo_info': intervalo_info,
            'ultimos_intervalos': intervalo_info['todos_intervalos'][-10:] if intervalo_info else []
        }
    
    def calcular_valor_medio_crashes(self):
        """Calcula o valor médio dos crashes"""
        if len(self.crashes) == 0:
            return None
        
        valores_crashes = [self.valores[i] for i in self.crashes if i < len(self.valores)]
        
        if not valores_crashes:
            return None
        
        try:
            desvio = statistics.stdev(valores_crashes) if len(valores_crashes) > 1 else 0
        except:
            desvio = 0
        
        return {
            'media': statistics.mean(valores_crashes),
            'mediana': statistics.median(valores_crashes),
            'min': min(valores_crashes),
            'max': max(valores_crashes),
            'desvio_padrao': desvio
        }
    
    def calcular_valor_medio_normais(self):
        """Calcula o valor médio das velas normais (não crash)"""
        indices_normais = [i for i, v in enumerate(self.velas) if v[4] == 0]
        
        if not indices_normais:
            return None
        
        valores_normais = [self.valores[i] for i in indices_normais]
        
        try:
            desvio = statistics.stdev(valores_normais) if len(valores_normais) > 1 else 0
        except:
            desvio = 0
        
        return {
            'media': statistics.mean(valores_normais),
            'mediana': statistics.median(valores_normais),
            'min': min(valores_normais),
            'max': max(valores_normais),
            'desvio_padrao': desvio
        }
    
    def analisar_sequencias_pre_crash(self, janela=5):
        """Analisa padrões nas velas anteriores ao crash"""
        if len(self.crashes) < 2:
            return None
        
        sequencias = []
        
        for crash_idx in self.crashes:
            if crash_idx >= janela:
                sequencia = self.valores[crash_idx - janela:crash_idx]
                sequencias.append(sequencia)
        
        if not sequencias:
            return None
        
        # Calcular média das sequências
        media_sequencia = []
        for i in range(janela):
            valores_posicao = [seq[i] for seq in sequencias if len(seq) > i]
            if valores_posicao:
                media_sequencia.append(statistics.mean(valores_posicao))
            else:
                media_sequencia.append(0)
        
        return {
            'janela': janela,
            'num_sequencias': len(sequencias),
            'media_sequencia': media_sequencia,
            'tendencia': 'CRESCENTE' if media_sequencia[-1] > media_sequencia[0] else 'DECRESCENTE'
        }
    
    def gerar_alerta_crash(self):
        """Gera um alerta se há risco de crash iminente"""
        predicao = self.prever_proximo_crash()
        
        # Se temos histórico e a próxima rodada está próxima
        if predicao['proximas_rodadas'] <= 3 and predicao['confianca'] in ['ALTA', 'MÉDIA']:
            return {
                'alerta': True,
                'urgencia': 'ALTA' if predicao['proximas_rodadas'] == 1 else 'MÉDIA',
                'mensagem': f'⚠️ POSSÍVEL CRASH NAS PRÓXIMAS {predicao["proximas_rodadas"]} RODADAS',
                'confianca': predicao['confianca']
            }
        
        return {'alerta': False, 'mensagem': 'Nenhum alerta no momento'}
    
    def prever_hora_proximo_crash(self, intervalo_rodada_segundos=30):
        """
        Calcula a hora estimada do próximo crash
        intervalo_rodada_segundos: tempo médio entre rodadas (padrão 30s)
        """
        predicao = self.prever_proximo_crash()
        proximas_rodadas = predicao['proximas_rodadas']
        
        tempo_estimado = proximas_rodadas * intervalo_rodada_segundos
        data_crash = datetime.now() + timedelta(seconds=tempo_estimado)
        
        return {
            'data_hora_estimada': data_crash,
            'tempo_minutos': tempo_estimado / 60,
            'tempo_segundos': tempo_estimado,
            'formato': data_crash.strftime('%d/%m/%Y %H:%M:%S')
        }
