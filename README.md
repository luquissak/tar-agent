# TAR Agent (Teoria Ator-Rede)

Este projeto implementa um agente focado em ler documentos e extrair relações entre "Actantes" segundo a Teoria Ator-Rede (TAR), utilizando simetria generalizada para entidades humanas e não-humanas.
A arquitetura extrai dados via Vertex AI e os renderiza em um grafo interativo utilizando o Pyvis.

## Estrutura de Pastas
A estrutura segue o padrão de organização em módulos Python para um agente:

```
tar-agent/
├── app/                  # Módulo principal da aplicação
│   ├── __init__.py
│   ├── main.py           # Orquestração (Vertex AI, leitura e chamadas)
│   ├── prompt.py         # Prompt epistemológico e instrução do sistema
│   ├── schemas.py        # Modelos Pydantic para o Output Estruturado (JSON)
│   └── visualize.py      # Geração do grafo interativo com Pyvis
├── documentos/           # (Criada automaticamente) Pasta onde você colocará os arquivos .txt
├── requirements.txt      # Dependências do projeto
└── README.md
```

## Como Usar

1. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Adicione os documentos:**
   Coloque seus arquivos `.txt` dentro do diretório `documentos/`.

3. **Configure as credenciais do Google Cloud:**
   O agente utiliza a biblioteca `google-cloud-aiplatform` (Vertex AI). Certifique-se de estar autenticado:
   ```bash
   gcloud auth application-default login
   ```

4. **Execute o agente:**
   Estando na raiz do projeto `tar-agent/`, execute:
   ```bash
   python -m app.main
   ```

O script vai ler os arquivos, gerar a rede com a API do Gemini e salvar o arquivo `mapa_ator_rede.html` no diretório atual. Abra o HTML em um navegador para explorar e interagir com as conexões (física de gravidade).
