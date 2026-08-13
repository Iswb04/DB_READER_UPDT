import requests

from rag import buscar_contexto


URL = "http://localhost:11434/api/generate"

MODELO = "qwen2.5:7b"

TEMPERATURE = 0.2


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

3. Use somente as colunas informadas no schema.

4. Não invente colunas.

5. Não use INSERT, UPDATE, DELETE, DROP ou ALTER.

6. Não coloque explicações.

7. Retorne somente o SQL ou NAO_RELACIONADA.

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

    resposta.raise_for_status() # Verifica se a requisição HTTP deu certo.

    sql = resposta.json()["response"].strip() # pegar resposta do ollama JSON e organizar

    sql = sql.replace("```sql", "") # remover o "sql" se vier junto
    sql = sql.replace("```", "") # remover o "```" se vier junto no fechamento

    return sql.strip() # devolver o slq limpo


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