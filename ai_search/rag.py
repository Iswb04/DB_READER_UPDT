from sentence_transformers import SentenceTransformer
import faiss
import numpy as np


modelo_embeddings = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)


documentos = [

         """
    Banco de dados: movies_db.
    Tabela: filmes.

    Todos os dados armazenados nesta tabela são provenientes
    da API OMDb e estão em inglês.

    A pergunta do usuário pode estar em português.
    """,
    
    """
    A tabela filmes contém informações sobre filmes.
    A coluna id contém o identificador IMDb do filme.
    """,

    """
    A coluna titulo contém o nome do filme.
    """,

    """
    A coluna data_lancamento contém a data de lançamento do filme.
    Ela possui o formato DATE.
    """,
 
    """
    A coluna pais contém o país de origem do filme.
    """,

    """
    A coluna genero contém os gêneros do filme.
    """,

    """
    A coluna diretor contém o nome do diretor do filme.
    """,

    """
    A coluna nota_imdb contém a nota do filme no IMDb.
    A nota varia de 0 a 10.
    """,

    """
    A coluna votos_imdb contém a quantidade de votos recebidos no IMDb.
    """,

    """
    A coluna nota_rotten_tomatoes contém a porcentagem do Rotten Tomatoes.
    """,

    """
    A coluna nota_metacritic contém a nota do Metacritic.
    """,

    """
    Exemplo:
    Pergunta: Quais filmes têm nota IMDb maior que 8?

    SQL:
    SELECT titulo, nota_imdb
    FROM filmes
    WHERE nota_imdb > 8;
    """,

    """
    Exemplo:
    Pergunta: Quais filmes foram lançados em 2014?

    SQL:
    SELECT titulo, data_lancamento
    FROM filmes
    WHERE YEAR(data_lancamento) = 2014;
    """,

    """
    Exemplo:
    Pergunta: Quais filmes foram dirigidos por Christopher Nolan?

    SQL:
    SELECT titulo
    FROM filmes
    WHERE diretor = 'Christopher Nolan';
    """
]


embeddings = modelo_embeddings.encode(documentos)

embeddings = np.array(embeddings).astype("float32")

indice = faiss.IndexFlatL2(embeddings.shape[1])

indice.add(embeddings)


def buscar_contexto(pergunta, quantidade=3):

    embedding_pergunta = modelo_embeddings.encode(
        [pergunta]
    )

    embedding_pergunta = np.array(
        embedding_pergunta
    ).astype("float32")

    distancias, indices = indice.search(
        embedding_pergunta,
        quantidade
    )

    contexto = []

    for i in indices[0]:
        contexto.append(documentos[i])

    return "\n\n".join(contexto)