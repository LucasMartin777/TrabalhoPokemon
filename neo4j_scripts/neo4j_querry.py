from neo4j import GraphDatabase

# ---------------------------Configuração da conexão com o banco de dados---------------------------
driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "senac123"))
session = driver.session()

# Consulta: Pokémons que podem atacar Pikachu devido à sua fraqueza e possuem peso maior que 10 kg
def pokemons_que_atacam_pikachu():
    query = """
        MATCH (pikachu:Pokemon {name: 'Pikachu'})-[:WEAK_TO]->(fraqueza:Type)
        MATCH (pokemon:Pokemon)-[:HAS_TYPE]->(fraqueza)
        WHERE pokemon.weight > 10
        RETURN pokemon.name AS nome, pokemon.weight AS peso
    """
    resultado = session.run(query)
    for registro in resultado:
        print(f"Pokémon: {registro['nome']} (Peso: {registro['peso']} kg)")

# ---------------------------Consulta: Tipo mais atacado por Pokémon de gelo---------------------------
def tipo_mais_atacado_por_gelo():
    query = """
        MATCH (pokemon:Pokemon)-[:WEAK_TO]->(:Type {name: 'Ice'})
        MATCH (pokemon)-[:HAS_TYPE]->(tipo:Type)
        RETURN tipo.name AS tipo, COUNT(pokemon) AS quantidade
        ORDER BY quantidade DESC
        LIMIT 1
    """
    resultado = session.run(query)
    for registro in resultado:
        print(f"Tipo mais atacado por gelo: {registro['tipo']} (Quantidade: {registro['quantidade']})")

# ---------------------------Consulta: Evoluções que aumentam pelo menos o dobro do peso---------------------------
def evolucoes_com_dobro_do_peso():
    query = """
        MATCH (antes:Pokemon)-[:EVOLVES_TO]->(depois:Pokemon)
        WHERE depois.weight >= 2 * antes.weight
        RETURN antes.name AS nome_anterior, antes.weight AS peso_anterior,
               depois.name AS nome_posterior, depois.weight AS peso_posterior
    """
    resultado = session.run(query)
    for registro in resultado:
        print(f"{registro['nome_anterior']} (Peso: {registro['peso_anterior']} kg) evolui para "
              f"{registro['nome_posterior']} (Peso: {registro['peso_posterior']} kg)")

# ---------------------------Execução das consultas---------------------------
print("Pokémons que atacam Pikachu com peso maior que 10 kg:")
pokemons_que_atacam_pikachu()

print("\nTipo mais atacado por gelo:")
tipo_mais_atacado_por_gelo()

print("\nEvoluções que dobram o peso:")
evolucoes_com_dobro_do_peso()

session.close()
