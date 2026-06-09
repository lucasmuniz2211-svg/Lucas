# 🎮 Aviator Crash Predictor

Uma aplicação Python para análise e previsão de crashes no jogo Aviator com banco de dados local.

## 🎯 Funcionalidades

✅ **Adicionar velas manualmente** - Registre os valores das velas e crashes  
✅ **Banco de dados local** - SQLite armazenado no seu PC  
✅ **Previsão de crashes** - Estima QUANDO e COM QUE VALOR o próximo crash ocorrerá  
✅ **Análise de padrões** - Detecta sequências pré-crash  
✅ **Estatísticas completas** - Taxa de crash, médias, ranges  
✅ **Histórico** - Rastreie todos os crashes anteriores  
✅ **Alertas** - Aviso quando um crash está próximo  

## 📋 Requisitos

- Python 3.7+
- Bibliotecas listadas em `requirements.txt`

## 🚀 Instalação

### 1. Clone o repositório
```bash
git clone https://github.com/lucasmuniz2211-svg/Lucas.git
cd Lucas
```

### 2. Instale as dependências
```bash
pip install -r requirements.txt
```

### 3. Execute a aplicação
```bash
python main.py
```

## 📊 Como Usar

### Menu Principal
```
🎮 AVIATOR CRASH PREDICTOR - Análise de Velas 🎮

[1] Adicionar nova vela
[2] Adicionar múltiplas velas (colada do histórico)
[3] Ver previsão do próximo CRASH
[4] Ver estatísticas gerais
[5] Ver histórico de crashes
[6] Ver análise de sequências
[7] Ver últimas velas registradas
[8] Limpar todos os dados
[0] Sair
```

### Exemplo de Uso

#### 1️⃣ Adicionar uma vela
```
Digite o valor da vela (ex: 1.45): 1.49
É um CRASH? (s/n): n
✅ Vela adicionada! Tipo: NORMAL ✓ | Valor: 1.49
```

#### 2️⃣ Adicionar histórico de uma vez
Cole todo o histórico do jogo:
```
Valores: 1.49 3.31 7.94 1.74 1.02 6.36 1.36 1.40 13.37 1.04
```

#### 3️⃣ Ver previsão
A aplicação mostrará:
- **Probabilidade de crash** em %
- **Próximas rodadas estimadas** até o crash
- **Hora estimada** do próximo crash
- **Valor médio** que o crash costuma ter
- **Nível de confiança** (ALTA/MÉDIA/BAIXA)

```
🔮 PREVISÃO DO PRÓXIMO CRASH

📊 Probabilidade de CRASH: 15.00%
⏰ Próximas rodadas estimadas: 8
🎯 Nível de Confiança: MÉDIA

🕐 Hora estimada do próximo CRASH:
   09/06/2026 14:35:22
   (4.2 minutos a partir de agora)

💰 Valor médio dos crashes anteriores:
   Média: 1.05x
   Mediana: 1.02x
   Range: 1.00x - 1.40x
```

## 📁 Estrutura de Arquivos

```
Lucas/
├── main.py              # Aplicação principal (menu interativo)
├── database.py          # Gerenciador do banco de dados SQLite
├── predictor.py         # Motor de previsões e análise
├── requirements.txt     # Dependências do projeto
├── README.md           # Este arquivo
└── aviator_data.db     # Banco de dados (criado automaticamente)
```

## 🔧 Módulos

### `database.py`
- `AviatorDatabase` - Classe para gerenciar o banco de dados
  - `adicionar_vela()` - Adiciona uma vela individual
  - `adicionar_multiplas_velas()` - Adiciona múltiplas velas
  - `obter_estatisticas()` - Retorna estatísticas
  - `obter_crashes()` - Lista todos os crashes
  - `limpar_dados()` - Remove todos os dados

### `predictor.py`
- `AviatorPredictor` - Motor de previsões
  - `prever_proximo_crash()` - Prevê o próximo crash
  - `calcular_intervalo_crashes()` - Analisa intervalos
  - `calcular_valor_medio_crashes()` - Média dos crashes
  - `prever_hora_proximo_crash()` - Hora estimada
  - `analisar_sequencias_pre_crash()` - Padrões pré-crash
  - `gerar_alerta_crash()` - Cria alertas

## 📊 Como Funciona a Previsão

A aplicação usa análise estatística baseada em:

1. **Histórico de crashes** - Registra todos os crashes anteriores
2. **Intervalos entre crashes** - Calcula o padrão de frequência
3. **Valores médios** - Estima o valor que o crash terá
4. **Desvio padrão** - Mede a consistência dos padrões
5. **Sequências pré-crash** - Analisa valores antes de cada crash

### Exemplo de Cálculo

Se você tem 10 crashes em 100 rodadas:
- **Taxa de crash**: 10%
- **Intervalo médio**: 10 rodadas
- **Próximo crash estimado**: rodada 10 (±2 rodadas)

## ⚠️ Importante

- **Esta é uma ferramenta de análise**, não garante resultados
- Quanto MAIS dados você adicionar, MAIS PRECISA será a previsão
- Recomenda-se registrar pelo menos 50+ rodadas para análises confiáveis
- Os padrões podem mudar; a análise se baseia em histórico

## 💾 Dados Armazenados

O banco de dados local guarda:
- ID da vela
- Valor da vela
- Tipo (NORMAL ou CRASH)
- Data e hora do registro
- Flag de crash

**Tudo é armazenado no seu PC** - nenhum dado é enviado para servidores.

## 🔄 Atualizações Futuras

- [ ] Gráficos em tempo real
- [ ] Integração com API do provedor
- [ ] OCR para captura automática da tela
- [ ] Previsões com Machine Learning
- [ ] Alertas sonoros

## 📝 Licença

Projeto pessoal para análise educacional.

## 🤝 Contribuições

Sinta-se livre para sugerir melhorias!

---

**Desenvolvido com ❤️ para análise do Aviator**
