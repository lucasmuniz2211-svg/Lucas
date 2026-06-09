#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from database import AviatorDatabase
from predictor import AviatorPredictor
from datetime import datetime
import os

def limpar_tela():
    """Limpa a tela do console"""
    os.system('cls' if os.name == 'nt' else 'clear')

def exibir_menu():
    """Exibe o menu principal"""
    print("\n" + "="*60)
    print("🎮 AVIATOR CRASH PREDICTOR - Análise de Velas 🎮".center(60))
    print("="*60)
    print("\n[1] Adicionar nova vela")
    print("[2] Adicionar múltiplas velas (colada do histórico)")
    print("[3] Ver previsão do próximo CRASH")
    print("[4] Ver estatísticas gerais")
    print("[5] Ver histórico de crashes")
    print("[6] Ver análise de sequências")
    print("[7] Ver últimas velas registradas")
    print("[8] Limpar todos os dados")
    print("[0] Sair")
    print("="*60)

def adicionar_vela_manual(db):
    """Adiciona uma vela manualmente"""
    try:
        valor = float(input("\n📊 Digite o valor da vela (ex: 1.45): "))
        is_crash = input("É um CRASH? (s/n): ").lower() == 's'
        
        db.adicionar_vela(valor, is_crash)
        tipo = "CRASH 💥" if is_crash else "NORMAL ✓"
        print(f"\n✅ Vela adicionada! Tipo: {tipo} | Valor: {valor}")
    except ValueError:
        print("❌ Erro: Digite um número válido!")

def adicionar_multiplas_velas(db):
    """Adiciona múltiplas velas copiadas do histórico"""
    print("\n📋 Cole os valores separados por espaço ou quebra de linha:")
    print("Exemplo: 1.49 3.31 7.94 1.74 1.02 6.36")
    print("(Digite 'fim' em uma linha vazia para terminar)")
    
    valores_str = ""
    while True:
        linha = input()
        if linha.lower() == 'fim':
            break
        valores_str += linha + " "
    
    try:
        valores = [float(v) for v in valores_str.split() if v]
        
        if not valores:
            print("❌ Nenhum valor foi fornecido!")
            return
        
        db.adicionar_multiplas_velas(valores)
        print(f"\n✅ {len(valores)} velas adicionadas com sucesso!")
        print(f"Valores: {valores}")
    except ValueError as e:
        print(f"❌ Erro ao processar valores: {e}")

def exibir_previsao(db):
    """Exibe a previsão do próximo crash"""
    velas = db.obter_ultimas_velas(200)
    
    if not velas:
        print("\n❌ Nenhuma vela registrada ainda!")
        return
    
    predictor = AviatorPredictor(velas)
    predicao = predictor.prever_proximo_crash()
    
    print("\n" + "="*60)
    print("🔮 PREVISÃO DO PRÓXIMO CRASH".center(60))
    print("="*60)
    
    print(f"\n📊 Probabilidade de CRASH: {predicao['probabilidade_crash']:.2f}%")
    print(f"⏰ Próximas rodadas estimadas: {predicao['proximas_rodadas']}")
    print(f"🎯 Nível de Confiança: {predicao['confianca']}")
    
    # Hora estimada
    hora_info = predictor.prever_hora_proximo_crash()
    print(f"\n🕐 Hora estimada do próximo CRASH:")
    print(f"   {hora_info['formato']}")
    print(f"   ({hora_info['tempo_minutos']:.1f} minutos a partir de agora)")
    
    # Valor médio dos crashes
    valor_crashes = predictor.calcular_valor_medio_crashes()
    if valor_crashes:
        print(f"\n💰 Valor médio dos crashes anteriores:")
        print(f"   Média: {valor_crashes['media']:.2f}x")
        print(f"   Mediana: {valor_crashes['mediana']:.2f}x")
        print(f"   Range: {valor_crashes['min']:.2f}x - {valor_crashes['max']:.2f}x")
    
    # Alerta
    alerta = predictor.gerar_alerta_crash()
    if alerta['alerta']:
        print(f"\n⚠️ ALERTA: {alerta['mensagem']}")
        print(f"   Urgência: {alerta['urgencia']}")
    
    # Últimos intervalos entre crashes
    if predicao['ultimos_intervalos']:
        print(f"\n📈 Últimos intervalos entre crashes (rodadas):")
        print(f"   {predicao['ultimos_intervalos']}")

def exibir_estatisticas(db):
    """Exibe estatísticas gerais"""
    stats = db.obter_estatisticas()
    
    print("\n" + "="*60)
    print("📊 ESTATÍSTICAS GERAIS".center(60))
    print("="*60)
    
    print(f"\n📈 Total de velas registradas: {stats['total_velas']}")
    print(f"💥 Total de crashes: {stats['total_crashes']}")
    print(f"📊 Taxa de crash: {stats['taxa_crash']:.2f}%")
    
    print(f"\n💰 Velas normais:")
    print(f"   Média: {stats['media_velas_normais']:.2f}x" if stats['media_velas_normais'] else "   N/A")
    print(f"   Range: {stats['min_normal']:.2f}x - {stats['max_normal']:.2f}x" if stats['min_normal'] else "   N/A")
    
    print(f"\n💥 Crashes:")
    print(f"   Média: {stats['media_crashes']:.2f}x" if stats['media_crashes'] else "   N/A")

def exibir_crashes(db):
    """Exibe o histórico de crashes"""
    crashes = db.obter_crashes()
    
    if not crashes:
        print("\n❌ Nenhum crash registrado!")
        return
    
    print("\n" + "="*60)
    print("💥 HISTÓRICO DE CRASHES".center(60))
    print("="*60)
    
    for idx, (id, valor, data_hora) in enumerate(crashes[:20], 1):
        print(f"{idx}. Valor: {valor:.2f}x | Data/Hora: {data_hora}")

def exibir_analise_sequencias(db):
    """Exibe análise de sequências pré-crash"""
    velas = db.obter_ultimas_velas(200)
    
    if not velas:
        print("\n❌ Nenhuma vela registrada!")
        return
    
    predictor = AviatorPredictor(velas)
    sequencias = predictor.analisar_sequencias_pre_crash(janela=5)
    
    print("\n" + "="*60)
    print("📊 ANÁLISE DE SEQUÊNCIAS PRÉ-CRASH".center(60))
    print("="*60)
    
    if sequencias:
        print(f"\n🔍 Padrão detectado nos {sequencias['janela']} rodadas antes do crash:")
        print(f"   Tendência: {sequencias['tendencia']}")
        print(f"   Número de sequências analisadas: {sequencias['num_sequencias']}")
        print(f"\n   Valores médios da sequência:")
        for i, valor in enumerate(sequencias['media_sequencia'], 1):
            print(f"      Rodada -{sequencias['janela']-i}: {valor:.2f}x")
    else:
        print("\n❌ Dados insuficientes para análise de sequências!")

def exibir_ultimas_velas(db):
    """Exibe as últimas velas registradas"""
    velas = db.obter_ultimas_velas(20)
    
    if not velas:
        print("\n❌ Nenhuma vela registrada!")
        return
    
    print("\n" + "="*60)
    print("📊 ÚLTIMAS VELAS REGISTRADAS".center(60))
    print("="*60)
    
    for idx, (id, valor, tipo, data_hora, is_crash) in enumerate(velas, 1):
        icon = "💥" if is_crash else "✓"
        print(f"{idx}. {icon} {valor:.2f}x | {tipo} | {data_hora}")

def main():
    """Função principal"""
    db = AviatorDatabase()
    
    while True:
        limpar_tela()
        exibir_menu()
        opcao = input("\nEscolha uma opção: ").strip()
        
        if opcao == "0":
            print("\n👋 Saindo... Obrigado por usar o Aviator Predictor!")
            break
        elif opcao == "1":
            adicionar_vela_manual(db)
            input("\n[ENTER] para continuar...")
        elif opcao == "2":
            adicionar_multiplas_velas(db)
            input("\n[ENTER] para continuar...")
        elif opcao == "3":
            exibir_previsao(db)
            input("\n[ENTER] para continuar...")
        elif opcao == "4":
            exibir_estatisticas(db)
            input("\n[ENTER] para continuar...")
        elif opcao == "5":
            exibir_crashes(db)
            input("\n[ENTER] para continuar...")
        elif opcao == "6":
            exibir_analise_sequencias(db)
            input("\n[ENTER] para continuar...")
        elif opcao == "7":
            exibir_ultimas_velas(db)
            input("\n[ENTER] para continuar...")
        elif opcao == "8":
            confirma = input("\n⚠️ Tem certeza que deseja limpar TODOS os dados? (s/n): ").lower()
            if confirma == 's':
                db.limpar_dados()
                print("✅ Dados limpos com sucesso!")
            input("\n[ENTER] para continuar...")
        else:
            print("❌ Opção inválida!")
            input("\n[ENTER] para continuar...")

if __name__ == "__main__":
    main()
