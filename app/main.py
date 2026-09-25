import os
import json

from google import genai
from google.genai import types

from app.schemas import MapaAtorRede
from app.prompt import instrucao_tar
from app.visualize import gerar_grafo_interativo


PROJECT_ID = "llm-studies"
LOCATION = "us-central1"
MODEL_NAME = "gemini-2.5-flash"


def processar_pasta(caminho_pasta, client):
    mapa_global = {
        "actantes": [],
        "translacoes": []
    }

    if not os.path.exists(caminho_pasta):
        print(
            f"Pasta '{caminho_pasta}' não encontrada. "
            "Criando diretório vazio..."
        )
        os.makedirs(caminho_pasta)
        return mapa_global

    arquivos = [
        f
        for f in os.listdir(caminho_pasta)
        if f.endswith(".txt")
    ]

    if not arquivos:
        print(
            f"Nenhum arquivo .txt encontrado em "
            f"'{caminho_pasta}'."
        )
        return mapa_global

    for arquivo in arquivos:

        caminho_arquivo = os.path.join(
            caminho_pasta,
            arquivo
        )

        with open(
            caminho_arquivo,
            "r",
            encoding="utf-8"
        ) as f:
            conteudo = f.read()

        print(f"Processando arquivo: {arquivo}")

        try:

            resposta = client.models.generate_content(
                model=MODEL_NAME,
                contents=[
                    instrucao_tar,
                    conteudo
                ],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=MapaAtorRede,
                ),
            )

            dados = json.loads(resposta.text)

            mapa_global["actantes"].extend(
                dados.get("actantes", [])
            )

            mapa_global["translacoes"].extend(
                dados.get("translacoes", [])
            )

        except Exception as e:

            print(
                f"Erro ao processar "
                f"'{arquivo}': {e}"
            )

    return mapa_global


def main():

    client = genai.Client(
        vertexai=True,
        project=PROJECT_ID,
        location=LOCATION,
    )

    caminho_documentos = "./documentos"

    dados_extraidos = processar_pasta(
        caminho_documentos,
        client
    )

    if dados_extraidos["actantes"]:

        gerar_grafo_interativo(
            dados_extraidos,
            output_path="mapa_ator_rede.html"
        )

    else:

        print(
            "Nenhum dado extraído "
            "para gerar o grafo."
        )


if __name__ == "__main__":
    main()