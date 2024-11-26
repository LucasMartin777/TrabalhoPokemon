from neo4j import GraphDatabase

class PokemonQueries:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def query_pokemons_that_can_attack_pikachu(self):
        query = """
        MATCH (p:Pokemon)-[:HAS_TYPE]->(t:Type)
        WHERE t.name IN ["Ground"] AND p.weight > 10
        RETURN p.name AS Pokemon
        """
        return self._run_query(query)

    def query_most_common_type_attacked_by_ice(self):
        query = """
        MATCH (p:Pokemon)-[:HAS_TYPE]->(t:Type)<-[:WEAK_TO]-(ice:Type {name: "Ice"})
        RETURN t.name AS Type, COUNT(p) AS Count
        ORDER BY Count DESC
        LIMIT 1
        """
        return self._run_query(query)

    def query_evolutions_with_weight_gain(self):
        query = """
        MATCH (p1:Pokemon)-[:EVOLVES_TO]->(p2:Pokemon)-[:EVOLVES_TO]->(p3:Pokemon)
        WHERE p3.weight >= 2 * p1.weight
        RETURN COUNT(p3) AS EvolutionCount
        """
        return self._run_query(query)

    def _run_query(self, query):
        with self.driver.session() as session:
            result = session.run(query)
            return [record for record in result]

if __name__ == "__main__":
    uri = "bolt://localhost:7687"
    user = "neo4j"
    password = "senha"

    queries = PokemonQueries(uri, user, password)

    # Executar consultas
    print("Pokémons que podem atacar Pikachu:")
    print(queries.query_pokemons_that_can_attack_pikachu())

    print("\nTipo mais comum atacado por gelo:")
    print(queries.query_most_common_type_attacked_by_ice())

    print("\nEvoluções que dobram de peso:")
    print(queries.query_evolutions_with_weight_gain())

    queries.close()
