import requests

from rag import buscar_contexto


URL = "http://localhost:11434/api/generate"

MODELO = "qwen2.5:3b"

TEMPERATURE = 0.1


SCHEMA = """
Banco de dados: movies_db

Tabela: filmes

Colunas:
- id VARCHAR(20)
- titulo VARCHAR(255)
- data_lancamento DATE
- pais VARCHAR(255)
- genero VARCHAR(255)
- duracao INT
- diretor VARCHAR(255)
- atores TEXT
- sinopse TEXT
- nota_imdb DECIMAL(3,1)
- votos_imdb INT
- nota_rotten_tomatoes INT
- nota_metacritic INT
"""


def gerar_sql(pergunta):

    contexto = buscar_contexto(pergunta)

    prompt = f"""
Você é um especialista em MySQL e NL2SQL.

Sua tarefa é converter a pergunta do usuário em uma consulta
SQL para o banco de dados informado.

SCHEMA:
{SCHEMA}

CONTEXTO RECUPERADO PELO RAG:
{contexto}

REGRAS:

1. Se a pergunta NÃO tiver relação com filmes ou com os
dados disponíveis na tabela filmes, responda exatamente:

NAO_RELACIONADA

2. Se a pergunta tiver relação com o banco, gere somente
uma consulta SELECT válida em MySQL.

3. Use somente a tabela filmes.

4. Use somente as colunas informadas no schema.

5. Não invente colunas.

6. Não use INSERT, UPDATE, DELETE, DROP ou ALTER.

7. Não coloque explicações.

8. Retorne somente o SQL ou NAO_RELACIONADA.

PERGUNTA:
{pergunta}
"""

    resposta = requests.post(
        URL,
        json={
            "model": MODELO,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": TEMPERATURE
            },
            "keep_alive": "10m"
        }
    )

    resposta.raise_for_status()

    sql = resposta.json()["response"].strip()

    sql = sql.replace("```sql", "")
    sql = sql.replace("```", "")

    return sql.strip()


if __name__ == "__main__":

    while True:

        pergunta = input("\nVocê: ").strip()

        if pergunta.lower() == "sair":
            break

        sql = gerar_sql(pergunta)

        if sql == "NAO_RELACIONADA":
            print("Essa pergunta não está relacionada ao banco de filmes.")
            continue

        print("\nSQL gerado:")
        print(sql)