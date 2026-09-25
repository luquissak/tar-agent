from pyvis.network import Network


def quebrar_label(texto, largura=22):
    """
    Quebra labels longos em várias linhas para evitar
    sobreposição no grafo.
    """
    if not texto:
        return ""

    palavras = str(texto).split()

    linhas = []
    linha = ""

    for palavra in palavras:
        candidata = f"{linha} {palavra}".strip()

        if len(candidata) <= largura:
            linha = candidata
        else:
            if linha:
                linhas.append(linha)
            linha = palavra

    if linha:
        linhas.append(linha)

    return "\n".join(linhas)


def gerar_grafo_interativo(
    mapa_dados,
    output_path="mapa_ator_rede.html"
):

    # ---------------------------------------------------------
    # CONFIGURAÇÃO DO GRAFO
    # ---------------------------------------------------------

    net = Network(
        height="100vh",
        width="100%",
        bgcolor="#222222",
        font_color="white",
        directed=True,
    )

    cores_categoria = {
        "humano": "#4CAF50",
        "tecnico": "#2196F3",
        "institucional": "#FFC107",
        "natural": "#9C27B0"
    }

    # ---------------------------------------------------------
    # ACTANTES
    # ---------------------------------------------------------

    for actante in mapa_dados["actantes"]:

        if isinstance(actante, dict):
            categoria = actante.get("categoria", "")
            id_nome = actante.get("id_nome", "")
            papel = actante.get("papel_na_rede", "")
        else:
            categoria = actante.categoria
            id_nome = actante.id_nome
            papel = actante.papel_na_rede

        categoria = categoria.strip().lower()

        cor = cores_categoria.get(
            categoria,
            "#FFFFFF"
        )

        label = quebrar_label(
            id_nome,
            largura=22
        )

        net.add_node(
            id_nome,

            # Texto visível
            label=label,

            # Tooltip ao passar o mouse
            title=(
                f"<b>{id_nome}</b><br>"
                f"<br>"
                f"<b>Categoria:</b> {categoria}<br>"
                f"<b>Papel na rede:</b> {papel}"
            ),

            # Aparência
            color=cor,
            shape="dot",
            size=24,

            # Fonte do nó
            font={
                "size": 16,
                "face": "Arial",
                "color": "white",
                "strokeWidth": 3,
                "strokeColor": "#222222",
                "align": "center"
            },

            # Espaço entre círculo e texto
            margin=12,

            # Borda
            borderWidth=2
        )

    # ---------------------------------------------------------
    # TRANSLAÇÕES
    # ---------------------------------------------------------

    for relacao in mapa_dados["translacoes"]:

        if isinstance(relacao, dict):
            origem = relacao.get("origem_id", "")
            destino = relacao.get("destino_id", "")
            acao = relacao.get("acao_mediadora", "")
        else:
            origem = relacao.origem_id
            destino = relacao.destino_id
            acao = relacao.acao_mediadora

        label_acao = quebrar_label(
            acao,
            largura=20
        )

        net.add_edge(
            origem,
            destino,

            # Texto visível na aresta
            label=label_acao,

            # Tooltip
            title=f"<b>Translação:</b><br>{acao}",

            arrows="to",

            width=1.5,

            color={
                "color": "#BBBBBB",
                "highlight": "#FFFFFF",
                "hover": "#FFFFFF"
            },

            font={
                "size": 13,
                "face": "Arial",
                "color": "#FFFFFF",

                # Contorno para não desaparecer sobre a linha
                "strokeWidth": 4,
                "strokeColor": "#222222",

                "align": "horizontal"
            },

            smooth={
                "enabled": True,
                "type": "curvedCW",
                "roundness": 0.15
            }
        )

    # ---------------------------------------------------------
    # FÍSICA DO GRAFO
    # ---------------------------------------------------------

    net.set_options("""
    {
        "nodes": {
            "borderWidth": 2,
            "shadow": false
        },

        "edges": {
            "smooth": {
                "enabled": true,
                "type": "dynamic"
            }
        },

        "physics": {
            "enabled": true,

            "solver": "barnesHut",

            "barnesHut": {
                "gravitationalConstant": -12000,
                "centralGravity": 0.10,
                "springLength": 280,
                "springConstant": 0.025,
                "damping": 0.30,
                "avoidOverlap": 1.0
            },

            "stabilization": {
                "enabled": true,
                "iterations": 1000,
                "updateInterval": 100,
                "fit": true
            }
        },

        "interaction": {
            "hover": true,
            "tooltipDelay": 100,
            "dragNodes": true,
            "dragView": true,
            "zoomView": true,
            "navigationButtons": true,
            "keyboard": true
        }
    }
    """)



    # ---------------------------------------------------------
    # SALVAR
    # ---------------------------------------------------------

    net.save_graph(output_path)

    print(
        f"Grafo gerado com sucesso em '{output_path}'"
    )