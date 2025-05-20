# 🖧 Projeto de Simulação de Rede de Computadores
### Daniel Rodrigues de Sousa, Redes II, 2025.1

Este projeto simula uma rede de computadores com hosts e roteadores utilizando o algoritmo de Estado de Enlace (Link State Routing). É uma ferramenta educacional criada no contexto da disciplina Redes II, com foco em aprendizado e experimentação.

## 📌 Objetivos

- 📡 Simular o funcionamento de uma rede de computadores.
- 🔁 Implementar o algoritmo de roteamento por estado de enlace.
- 🐍 Utilizar Python para lógica de rede e Docker para isolar os ambientes de rede.
- 🌐 Permitir a criação de diferentes topologias de rede.

## ⚙️ Pré-requisitos

Antes de começar, você precisa ter instalado:

- **Docker**
- **Make**
- **Python** (caso queira instalar o make via pip)

Instale o Make com o comando:

```bash
pip install make
```

Bibliotecas utilizadas:
```bash
pip install matplotlib
```

```bash
pip install networkx
```

```bash
pip install yaml
```

```bash
pip install psutil
```

## ▶️ Como Executar

Para gerar uma topologia:

```bash
cd generate_compose
```
```bash
python3 yaml_generator.py
```

```bash
python3 docker_compose_create.py
```

1. Abre um menu para que o usuário escolha a topologia desejada;
2. Esse código gera um arquivo **config_yaml** que contém a topologia selecionada
3. Gerar o docker compose com a topologia nova gerada

Para rodar a simulação:

```bash
make
```

- Obs: Caso esteja na pasta /gera_yml, volte para a raiz do projeto, por meio desse comando:
```bash
cd ..
```
- Agora sim, rode:
```bash
make
```

Esses comandos irão:

- Criar os containers Docker para hosts e roteadores.
- Gerar uma topologia aleatória.
- Iniciar a comunicação entre os nós da rede.

## 📡 Protocolo de Comunicação

A comunicação entre os hosts e roteadores é feita usando o **UDP (User Datagram Protocol)**.

### Por que UDP?
-- (Explicações mais detalhadas no relatório técnico)
- ⚡ **Alta velocidade**: ideal para aplicações em tempo real.
- 🔁 **Sem confirmação**: não há verificação de entrega dos pacotes, o que simplifica a simulação.
- ⚙️ **Leve e simples**: menos sobrecarga que o TCP.

UDP é amplamente utilizado em:

- Transmissões de áudio e vídeo em tempo real
- Jogos online
- Aplicações onde a latência é mais importante que a confiabilidade

## 🕸️ Topologias de Rede

Durante a execução, uma topologia aleatória é escolhida entre:

- 🌟 **Estrela** Representa a topologia em estrela, onde todos os dispositivos se conectam a um ponto central (hub ou switch).
- 🔗 **Anel** Refere-se à topologia em anel, onde cada dispositivo está conectado a dois outros, formando um circuito fechado.
- 🌳 **Árvore** Simboliza a topologia em árvore, que combina características da estrela e do barramento, com uma estrutura hierárquica de dispositivos.
- 📏 **Linha** Representa a topologia em barramento (linha), onde todos os dispositivos compartilham um único meio de comunicação linear.

## 🔧 Como funciona a construção

- São definidos `n` hosts e `n` roteadores.
- Cada host se conecta a um roteador.
- A conexão entre roteadores depende da topologia selecionada.

Essa abordagem permite simular diversos cenários de rede, com diferentes comportamentos e complexidades.

## 🧪 Exemplos de Aplicação

Este projeto pode ser utilizado para:

- 🧠 **Compreensão prática de algoritmos de roteamento**
- 🧑‍💻 **Simulação de comportamento de redes reais**
- 📊 **Análise de desempenho em diferentes topologias**
- 🎓 **Apoio a atividades acadêmicas e laboratoriais**

## 🎓 Observações Finais

Este projeto foi desenvolvido como parte da disciplina Redes II e tem como principal objetivo demonstrar conceitos fundamentais de redes e roteamento de maneira prática, interativa e flexível.