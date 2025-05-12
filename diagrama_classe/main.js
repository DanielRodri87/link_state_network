// Configuração inicial do mermaid
mermaid.initialize({
    startOnLoad: true,
    theme: 'default',
    securityLevel: 'loose'
});

// Definição do diagrama de classes
const diagram = `
classDiagram
    class RoteadorApp {
        -dict lsdb
        -Event event
        -List threads
        +__init__()
        +atualizar_tabela()
        +monitorar_vizinhos()
        +iniciar_threads()
        +parar()
    }

    class VizinhosManager {
        -dict vizinhos_inativos
        -dict ultimo_tempo_vida
        +atualiza_status_vizinhos()
        +verifica_roteadores_ativos(lsdb)
    }

    class LSAManager {
        -VizinhosManager vizinhos_manager
        +__init__(vizinhos_manager)
        +enviar_lsa(event)
        +receber_lsa(lsdb, event)
    }

    class AtualizadorDeRotas {
        -GerenciadorDeRotas gerenciador
        +__init__(gerenciador)
        +recalcular_rotas(vizinhos_inativos)
    }

    class GerenciadorDeRotas {
        -dict lsdb
        -dict vizinhos_inativos
        +__init__(lsdb, vizinhos_inativos)
        +calcular_menor_caminho()
        +atualizar_tabela_roteamento()
    }

    RoteadorApp *-- VizinhosManager
    RoteadorApp *-- LSAManager
    RoteadorApp *-- AtualizadorDeRotas
    RoteadorApp *-- GerenciadorDeRotas
    LSAManager --> VizinhosManager
    AtualizadorDeRotas --> GerenciadorDeRotas
`;

// Renderizar o diagrama
document.getElementById('mermaid-diagram').innerHTML = diagram;

// Função para baixar o diagrama como imagem
document.getElementById('download-btn').addEventListener('click', async () => {
    const svgElement = document.querySelector('.mermaid svg');
    const svgData = new XMLSerializer().serializeToString(svgElement);
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    const img = new Image();
    
    img.onload = () => {
        canvas.width = img.width;
        canvas.height = img.height;
        ctx.drawImage(img, 0, 0);
        
        const link = document.createElement('a');
        link.download = 'diagrama_classes.png';
        link.href = canvas.toDataURL('image/png');
        link.click();
    };

    img.src = 'data:image/svg+xml;base64,' + btoa(unescape(encodeURIComponent(svgData)));
});
