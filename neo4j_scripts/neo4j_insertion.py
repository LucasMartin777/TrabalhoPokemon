from neo4j import GraphDatabase
import json

class PokemonNeo4j:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def insert_pokemon(self, pokemon_data):
        with self.driver.session() as session:
            for pokemon in pokemon_data:
                session.write_transaction(self._create_pokemon, pokemon)

    @staticmethod
    def _create_pokemon(tx, pokemon):
        # Cria nós de Pokémon
        tx.run(
            """
            MERGE (p:Pokemon {name: $name, weight: $weight})
            WITH p
            UNWIND $types AS type
            MERGE (t:Type {name: type})
            MERGE (p)-[:HAS_TYPE]->(t)
            WITH p
            UNWIND $weaknesses AS weakness
            MERGE (w:Type {name: weakness})
            MERGE (p)-[:WEAK_TO]->(w)
            WITH p
            UNWIND $attacks AS attack
            MERGE (a:Attack {name: attack})
            MERGE (p)-[:CAN_USE]->(a)
            WITH p
            OPTIONAL MATCH (e:Pokemon {name: $evolves_to})
            WHERE $evolves_to IS NOT NULL
            MERGE (p)-[:EVOLVES_TO]->(e)
            """,
            name=pokemon["name"],
            weight=pokemon["weight"],
            types=pokemon["types"],
            weaknesses=pokemon["weaknesses"],
            attacks=pokemon["attacks"],
            evolves_to=pokemon.get("evolves_to", None)
        )

if __name__ == "__main__":
    # Conexão com o Neo4j
    uri = "bolt://localhost:7687"  # Atualize com a URI do Neo4j
    user = "neo4j"
    password = "senha"  # Substitua pela senha do Neo4j
    pokemon_file = "../output/pokedex_clean.json"

    # Carregar os dados processados
    with open(pokemon_file, 'r') as f:
        pokemon_data = json.load(f)

    # Inserir dados no Neo4j
    neo4j = PokemonNeo4j(uri, user, password)
    neo4j.insert_pokemon(pokemon_data)
    neo4j.close()

    print("Dados inseridos no Neo4j com sucesso!")
