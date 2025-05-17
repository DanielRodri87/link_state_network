"""
Network Performance Testing Module

This module provides functionality for testing and visualizing network performance metrics
including response times, connectivity success rates, and connection matrices between routers.
"""

import subprocess
import sys
import os
import re
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from typing import List, Tuple, Any, Optional

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from class_net.manipulation import Manipulacao
from class_net.message import Mensagem

def plotar_matriz_tempos(router_list: List[str], response_matrix: np.ndarray) -> None:
    """
    Plot a heatmap showing response times between routers.
    
    Args:
        router_list: List of router identifiers
        response_matrix: Matrix containing response times
    """
    plt.figure(figsize=(12, 10))
    matrix_display = np.copy(response_matrix)
    mask = np.isnan(response_matrix)
    colormap = sns.color_palette("YlOrRd", as_cmap=True)
    
    ax = sns.heatmap(matrix_display, 
                annot=True, 
                cmap=colormap,
                mask=mask,
                xticklabels=router_list, 
                yticklabels=router_list,
                vmin=0.0,
                fmt='.2f',
                cbar_kws={'label': 'Tempo de resposta (ms)'})
    
    plt.xlabel('Roteador de Destino')
    plt.ylabel('Roteador de Origem')
    plt.title('Tempo de Resposta entre Roteadores (ms)')
    plt.tight_layout()
    plt.savefig('matriz_tempos_resposta.png')
    plt.close()
    
    print("Matriz de tempos de resposta salva como 'matriz_tempos_resposta.png'")

def executar_teste_ping() -> Tuple[List[str], np.ndarray, np.ndarray, List[List[Any]], List[List[str]]]:
    """
    Execute ping tests between all routers and collect performance metrics.
    
    Returns:
        Tuple containing:
        - List of router names
        - Results matrix (connectivity status)
        - Response time matrix
        - List of successful tests
        - List of failed tests
    """
    failed_tests = []
    successful_tests = []
    router_list = Manipulacao.roteadores_encontrados()
    
    results_matrix = np.zeros((len(router_list), len(router_list)))
    time_matrix = np.zeros((len(router_list), len(router_list)))
    time_matrix.fill(np.nan)
    
    print("Executando testes de ping entre roteadores...")
    
    for i, r_origem in enumerate(router_list):
        print(f"Testando {r_origem}...")
        for j, r_destino in enumerate(router_list):
            try:
                ip = Manipulacao.extrair_ip_roteadores(r_destino)
                comando = f"docker exec {r_origem} ping -c 1 -W 0.1 {ip}"
                result = subprocess.run(comando, shell=True, check=True, text=True, capture_output=True)
                if result.returncode == 0:
                    output = result.stdout
                    tempo_ms = extrair_tempo_ping(output)
                    
                    print(Mensagem.formatar_sucesso(f"{r_origem} -> {r_destino} sucesso. Tempo: {tempo_ms:.2f}ms"))
                    successful_tests.append([r_origem, r_destino, tempo_ms])
                    results_matrix[i][j] = 1
                    time_matrix[i][j] = tempo_ms
            except subprocess.CalledProcessError as e:
                print(Mensagem.formatar_erro(f"{r_origem} -> {r_destino} falhou."))
                failed_tests.append([r_origem, r_destino])
                results_matrix[i][j] = 0
    
    print('\n')
    if failed_tests:
        print("Roteadores com falha:")
        for roteador, destino in failed_tests:
            print(Mensagem.formatar_erro(f"{roteador} -> {destino} falhou."))
    
    return router_list, results_matrix, time_matrix, successful_tests, failed_tests

def extrair_tempo_ping(ping_output: str) -> float:
    """
    Extract response time from ping command output.
    
    Args:
        ping_output: Raw output string from ping command
        
    Returns:
        float: Response time in milliseconds
    """
    try:
        time_match = re.search(r'time=(\d+\.?\d*) ms', ping_output)
        if time_match:
            return float(time_match.group(1))
        return 0.0
    except Exception as error:
        print(f"Erro ao extrair tempo do ping: {error}")
        return 0.0

def plotar_grafico_taxa_sucesso(router_list: List[str], results_matrix: np.ndarray) -> None:
    """
    Plot bar graph showing ping success rates for each router.
    
    Args:
        router_list: List of router identifiers
        results_matrix: Matrix containing test results
    """
    plt.figure(figsize=(12, 6))
    success_rates = np.sum(results_matrix, axis=1) / len(router_list) * 100
    
    barras = plt.bar(router_list, success_rates, color='skyblue')
    
    plt.xlabel('Roteador de Origem')
    plt.ylabel('Taxa de Sucesso (%)')
    plt.title('Taxa de Sucesso de Ping por Roteador')
    plt.xticks(rotation=45, ha='right')
    plt.ylim(0, 105)
    
    for i, barra in enumerate(barras):
        plt.text(barra.get_x() + barra.get_width()/2, barra.get_height() + 2,
                f'{success_rates[i]:.1f}%', ha='center', va='bottom')

    plt.tight_layout()
    plt.savefig('grafico_taxa_sucesso.png')
    plt.close()
    print("Gráfico de taxa de sucesso salvo como 'grafico_taxa_sucesso.png'")

def plotar_matriz_conectividade(router_list: List[str], results_matrix: np.ndarray) -> None:
    """
    Plot heatmap showing connectivity matrix between routers.
    
    Args:
        router_list: List of router identifiers
        results_matrix: Matrix containing connectivity results
    """
    plt.figure(figsize=(10, 8))
    
    sns.heatmap(results_matrix, annot=True, cmap="YlGnBu", 
                xticklabels=router_list, yticklabels=router_list, 
                cbar_kws={'label': 'Sucesso (1) / Falha (0)'})
    
    plt.xlabel('Roteador de Destino')
    plt.ylabel('Roteador de Origem')
    plt.title('Matriz de Conectividade entre Roteadores')
    plt.tight_layout()
    plt.savefig('matriz_conectividade.png')
    plt.close()
    print("Matriz de conectividade salva como 'matriz_conectividade.png'")

def main() -> None:
    """
    Execute performance tests and generate visualization reports.
    
    Performs ping tests, generates graphs, and displays statistics.
    """
    router_list, results_matrix, time_matrix, successes, failures = executar_teste_ping()
    
    plotar_grafico_taxa_sucesso(router_list, results_matrix)
    plotar_matriz_conectividade(router_list, results_matrix)
    plotar_matriz_tempos(router_list, time_matrix)
    
    total_tests = len(router_list) * len(router_list)
    success_rate = len(successes) / total_tests * 100
    
    response_times = [test[2] for test in successes if len(test) > 2]
    if response_times:
        avg_time = sum(response_times) / len(response_times)
        min_time = min(response_times)
        max_time = max(response_times)
    else:
        avg_time = min_time = max_time = 0
    
    print(f"\nEstatísticas de conectividade:")
    print(f"Total de testes: {total_tests}")
    print(f"Sucesso: {len(successes)} ({success_rate:.1f}%)")
    print(f"Falha: {len(failures)} ({100 - success_rate:.1f}%)")
    
    print(f"\nEstatísticas de tempo de resposta:")
    print(f"Tempo médio: {avg_time:.2f} ms")
    print(f"Tempo mínimo: {min_time:.2f} ms")
    print(f"Tempo máximo: {max_time:.2f} ms")
    
    print("\nTeste de ping e geração de gráficos concluídos.")

if __name__ == "__main__":
    main()