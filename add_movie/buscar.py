import requests
from datetime import datetime
import getpass

API_KEY = getpass.getpass("Chave da API: ")

URL = "https://www.omdbapi.com/"


def converter_votos(votos):
    if votos == "N/A":
        return None

    votos = votos.replace(",", "")

    if votos.endswith("M"):
        return int(float(votos[:-1]) * 1_000_000)

    elif votos.endswith("K"):
        return int(float(votos[:-1]) * 1_000)

    return int(votos)


def buscar_filme(titulo):

    params = {
        "apikey": API_KEY,
        "t": titulo
    }

    response = requests.get(URL, params=params)
    response.raise_for_status()

    dados = response.json()

    if dados.get("Response") == "False":
        print("Filme não encontrado:", dados.get("Error"))
        return None

    # Converte a data: "07 Nov 2014" -> "2014-11-07"
    data_lancamento = dados["Released"]

    if data_lancamento != "N/A":
        data_lancamento = datetime.strptime(
            data_lancamento,
            "%d %b %Y"
        ).strftime("%Y-%m-%d")
    else:
        data_lancamento = None

    # Converte duração: "169 min" -> 169
    duracao = dados["Runtime"]

    if duracao != "N/A":
        duracao = int(duracao.replace(" min", ""))
    else:
        duracao = None

    # Converte nota IMDb: "8.7" -> 8.7
    nota_imdb = dados["imdbRating"]

    if nota_imdb != "N/A":
        nota_imdb = float(nota_imdb)
    else:
        nota_imdb = None

    # Converte votos IMDb: "2,2M" / "2.2M" -> 2200000
    votos_imdb = converter_votos(dados["imdbVotes"])

    filme = {
        "id": dados["imdbID"],
        "titulo": dados["Title"],
        "data_lancamento": data_lancamento,
        "pais": dados["Country"],
        "genero": dados["Genre"],
        "duracao": duracao,
        "diretor": dados["Director"],
        "atores": dados["Actors"],
        "sinopse": dados["Plot"],
        "nota_imdb": nota_imdb,
        "votos_imdb": votos_imdb,

        # Rotten Tomatoes e Metacritic não são campos diretos
        "nota_rotten_tomatoes": None,
        "nota_metacritic": None
    }

    # Pega as notas do Rotten Tomatoes e Metacritic
    for rating in dados.get("Ratings", []):

        if rating["Source"] == "Rotten Tomatoes":
            valor = rating["Value"]

            if valor != "N/A":
                filme["nota_rotten_tomatoes"] = int(
                    valor.replace("%", "")
                )

        elif rating["Source"] == "Metacritic":
            valor = rating["Value"]

            if valor != "N/A":
                filme["nota_metacritic"] = int(
                    valor.split("/")[0]
                )

    return filme


if __name__ == "__main__":

    filme = buscar_filme("Interstellar")

    if filme:
        print(filme)