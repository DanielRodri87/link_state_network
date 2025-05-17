
def plotar_matriz_tempos(roteadores, matriz_tempos):
    """
    Plota um mapa de calor mostrando os tempos de resposta entre roteadores
    """
    plt.figure(figsize=(12, 10))
    
    # Criar uma cópia da matriz para formatação
    matriz_display = np.copy(matriz_tempos)
    
    # Configurar o mapa de calor com máscaras para valores NaN
    mask = np.isnan(matriz_tempos)
    
    # Usar um colormap com graduação de cores para representar os tempos
    cmap = sns.color_palette("YlOrRd", as_cmap=True)
    
    # Plotar o mapa de calor
    ax = sns.heatmap(matriz_display, 
                annot=True, 
                cmap=cmap,
                mask=mask,
                xticklabels=roteadores, 
                yticklabels=roteadores,
                vmin=0.0,
                fmt='.2f',
                cbar_kws={'label': 'Tempo de resposta (ms)'})
    
    # Adicionar rótulos e título
    plt.xlabel('Roteador de Destino')
    plt.ylabel('Roteador de Origem')
    plt.title('Tempo de Resposta entre Roteadores (ms)')
    
    # Ajustar a figura para caber todos os elementos
    plt.tight_layout()
    
    # Salvar a figura
    plt.savefig('matriz_tempos_resposta.png')
    plt.close()
    
    print("Matriz de tempos de resposta salva como 'matriz_tempos_resposta.png'")
import subprocess
import sys
import os
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Adicionando o diretório pai ao path para importar os módulos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from class_net.manipulation import Manipulacao
from class_net.message import Mensagem

def executar_teste_ping():
    """
    Executa testes de ping entre todos os roteadores e retorna os resultados
    """
    falha = []
    sucesso = []
    roteadores = Manipulacao.roteadores_encontrados()
    matriz_resultados = np.zeros((len(roteadores), len(roteadores)))
    matriz_tempos = np.zeros((len(roteadores), len(roteadores)))
    matriz_tempos.fill(np.nan)  # Preencher com NaN para indicar ausência de dados
    
    print("Executando testes de ping entre roteadores...")
    
    for i, r_origem in enumerate(roteadores):
        print(f"Testando {r_origem}...")
        for j, r_destino in enumerate(roteadores):
            try:
                ip = Manipulacao.extrair_ip_roteadores(r_destino)
                comando = f"docker exec {r_origem} ping -c 1 -W 0.1 {ip}"
                result = subprocess.run(comando, shell=True, check=True, text=True, capture_output=True)
                if result.returncode == 0:
                    # Extrair o tempo de resposta do output do ping
                    output = result.stdout
                    tempo_ms = extrair_tempo_ping(output)
                    
                    print(Mensagem.formatar_sucesso(f"{r_origem} -> {r_destino} sucesso. Tempo: {tempo_ms:.2f}ms"))
                    sucesso.append([r_origem, r_destino, tempo_ms])
                    matriz_resultados[i][j] = 1  # 1 indica sucesso
                    matriz_tempos[i][j] = tempo_ms
            except subprocess.CalledProcessError as e:
                print(Mensagem.formatar_erro(f"{r_origem} -> {r_destino} falhou."))
                falha.append([r_origem, r_destino])
                matriz_resultados[i][j] = 0  # 0 indica falha
    
    print('\n')
    if falha:
        print("Roteadores com falha:")
        for roteador, destino in falha:
            print(Mensagem.formatar_erro(f"{roteador} -> {destino} falhou."))
    
    return roteadores, matriz_resultados, matriz_tempos, sucesso, falha

def extrair_tempo_ping(output):
    """
    Extrai o tempo de resposta em ms da saída do comando ping
    """
    try:
        # Procura pelo padrão "time=X ms" na saída do ping
        import re
        match = re.search(r'time=(\d+\.?\d*) ms', output)
        if match:
            return float(match.group(1))
        return 0.0
    except Exception as e:
        print(f"Erro ao extrair tempo do ping: {e}")
        return 0.0

def plotar_grafico_taxa_sucesso(roteadores, matriz_resultados):
    """
    Plota um gráfico de barras mostrando a taxa de sucesso de ping para cada roteador
    """
    plt.figure(figsize=(12, 6))
    
    # Calcular a taxa de sucesso para cada roteador (origem)
    taxa_sucesso = np.sum(matriz_resultados, axis=1) / len(roteadores) * 100
    
    # Criar barras para cada roteador
    barras = plt.bar(roteadores, taxa_sucesso, color='skyblue')
    
    # Adicionar rótulos e título
    plt.xlabel('Roteador de Origem')
    plt.ylabel('Taxa de Sucesso (%)')
    plt.title('Taxa de Sucesso de Ping por Roteador')
    plt.xticks(rotation=45, ha='right')
    plt.ylim(0, 105)  # Limite y para melhor visualização
    
    # Adicionar os valores em cima das barras
    for i, barra in enumerate(barras):
        plt.text(barra.get_x() + barra.get_width()/2, barra.get_height() + 2,
                f'{taxa_sucesso[i]:.1f}%', ha='center', va='bottom')

    plt.tight_layout()
    plt.savefig('grafico_taxa_sucesso.png')
    plt.close()
    print("Gráfico de taxa de sucesso salvo como 'grafico_taxa_sucesso.png'")

def plotar_matriz_conectividade(roteadores, matriz_resultados):
    """
    Plota um mapa de calor mostrando a matriz de conectividade entre roteadores
    """
    plt.figure(figsize=(10, 8))
    
    # Criar o mapa de calor
    sns.heatmap(matriz_resultados, annot=True, cmap="YlGnBu", 
                xticklabels=roteadores, yticklabels=roteadores, 
                cbar_kws={'label': 'Sucesso (1) / Falha (0)'})
    
    plt.xlabel('Roteador de Destino')
    plt.ylabel('Roteador de Origem')
    plt.title('Matriz de Conectividade entre Roteadores')
    plt.tight_layout()
    plt.savefig('matriz_conectividade.png')
    plt.close()
    print("Matriz de conectividade salva como 'matriz_conectividade.png'")

def main():
    # Executar o teste de ping e obter os resultados
    roteadores, matriz_resultados, matriz_tempos, sucesso, falha = executar_teste_ping()
    
    # Plotar os gráficos
    plotar_grafico_taxa_sucesso(roteadores, matriz_resultados)
    plotar_matriz_conectividade(roteadores, matriz_resultados)
    plotar_matriz_tempos(roteadores, matriz_tempos)
    
    # Mostrar estatísticas
    total_testes = len(roteadores) * len(roteadores)
    taxa_sucesso_global = len(sucesso) / total_testes * 100
    
    # Calcular estatísticas de tempo
    tempos = [item[2] for item in sucesso if len(item) > 2]
    if tempos:
        tempo_medio = sum(tempos) / len(tempos)
        tempo_min = min(tempos)
        tempo_max = max(tempos)
    else:
        tempo_medio = tempo_min = tempo_max = 0
    
    print(f"\nEstatísticas de conectividade:")
    print(f"Total de testes: {total_testes}")
    print(f"Sucesso: {len(sucesso)} ({taxa_sucesso_global:.1f}%)")
    print(f"Falha: {len(falha)} ({100 - taxa_sucesso_global:.1f}%)")
    
    print(f"\nEstatísticas de tempo de resposta:")
    print(f"Tempo médio: {tempo_medio:.2f} ms")
    print(f"Tempo mínimo: {tempo_min:.2f} ms")
    print(f"Tempo máximo: {tempo_max:.2f} ms")
    
    print("\nTeste de ping e geração de gráficos concluídos.")

if __name__ == "__main__":
    main()