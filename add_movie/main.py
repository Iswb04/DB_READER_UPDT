from buscar import buscar_filme
from salvar import salvar_filme

filmes = [
    "Interstellar",
    "Inception",
    "The Dark Knight",
    "Oppenheimer",
    "Dunkirk",
    "Tenet",
    "The Prestige",
    "Memento",
    "Batman Begins",
    "Insomnia"
]

for titulo in filmes:

    filme = buscar_filme(titulo)

    if filme:
        salvar_filme(filme)
        print(f"{titulo} salvo com sucesso!")