import getpass
import mysql.connector

senha = getpass.getpass("Senha do banco: ")

conexao = mysql.connector.connect(
    host="localhost",
    user="zabeau",
    password=senha,
    database="movies_db"
)

cursor = conexao.cursor()


def salvar_filme(filme):
  # evitar duplicate
    sql = """
        INSERT IGNORE INTO filmes ( 
            id,
            titulo,
            data_lancamento,
            pais,
            genero,
            duracao,
            diretor,
            atores,
            sinopse,
            nota_imdb,
            nota_rotten_tomatoes,
            nota_metacritic
        )
        VALUES (
            %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s
        )
    """

    valores = (
        filme["id"],
        filme["titulo"],
        filme["data_lancamento"],
        filme["pais"],
        filme["genero"],
        filme["duracao"],
        filme["diretor"],
        filme["atores"],
        filme["sinopse"],
        filme["nota_imdb"],
        filme["nota_rotten_tomatoes"],
        filme["nota_metacritic"]
    )

    cursor.execute(sql, valores)
    conexao.commit()