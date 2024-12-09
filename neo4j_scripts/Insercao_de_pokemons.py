from neo4j import GraphDatabase
import json


url_banco = "bolt://localhost:7687"
usuario_banco = "neo4j"
senha_banco = "senac123"

driver = GraphDatabase.driver(url_banco, auth=(usuario_banco, senha_banco))
sessao = driver.session()

# Função para criar os relacionamentos de fraquezas entre Pokémon e Tipos
def estabelecer_relacionamentos_fraquezas(pokemons):
    for pokemon in pokemons:
        id_pokemon = pokemon['pokemon_id']
        fraquezas = pokemon['weaknesses']
        
        for fraqueza in fraquezas:
            sessao.run("""
                MATCH (p:Pokemon {id: $id})
                MATCH (f:Tipo {nome: $nome})
                MERGE (p)-[:FRACO_CONTRA]->(f)
                """, id=id_pokemon, nome=fraqueza)

# Função para criar nós representando os Tipos de Pokémon
def criar_nos_tipos():
    lista_tipos = ["Normal", "Água", "Fogo", "Grama", "Elétrico", "Gelo", "Lutador", "Veneno", "Terra", 
                   "Voador", "Psíquico", "Inseto", "Pedra", "Fantasma", "Dragão", "Sombrio", "Aço", "Fada"]
    
    for tipo in lista_tipos:
        sessao.run("""
            MERGE (t:Tipo {nome: $nome})
            """, nome=tipo)

# Função para criar os relacionamentos de tipos entre Pokémon e seus Tipos
def estabelecer_relacionamentos_tipos(pokemons):
    for pokemon in pokemons:
        id_pokemon = pokemon['pokemon_id']
        tipos = pokemon['types']
        
        for tipo in tipos:
            sessao.run("""
                MATCH (p:Pokemon {id: $id})
                MATCH (t:Tipo {nome: $nome})
                MERGE (p)-[:TEM_TIPO]->(t)
                """, id=id_pokemon, nome=tipo)

# Função para criar os relacionamentos de evolução entre Pokémon
def estabelecer_relacionamentos_evolucoes(pokemons):
    for pokemon in pokemons:
        evolucoes = pokemon.get('evolutions', [])
        
        if evolucoes:
            for atual, proximo in zip(evolucoes, evolucoes[1:]):
                sessao.run("""
                    MERGE (p1:Pokemon {nome: $nome_atual})
                    MERGE (p2:Pokemon {nome: $nome_proximo})
                    MERGE (p1)-[:EVOLUI_PARA]->(p2)
                    """, nome_atual=atual, nome_proximo=proximo)

# Função para adicionar os Pokémon no banco de dados
def criar_nos_pokemon(lista_pokemons):
    for pokemon in lista_pokemons:
        nome = pokemon['pokemon_name']
        id_pokemon = pokemon['pokemon_id']
        peso = float(pokemon['weight']) if pokemon.get('weight') else None
        altura = float(pokemon['height']) if pokemon.get('height') else None

        # Inserção dos dados básicos do Pokémon no grafo
        sessao.run("""
            MERGE (p:Pokemon {id: $id, nome: $nome})
            SET p.peso = $peso, p.altura = $altura
            """, id=id_pokemon, nome=nome, peso=peso, altura=altura)

# Carregar o arquivo JSON com os dados dos Pokémon
with open('pokemons_sorted.json', 'r') as arquivo:
    dados_pokemon = json.load(arquivo)

# Execução das funções
criar_nos_pokemon(dados_pokemon)
criar_nos_tipos()
estabelecer_relacionamentos_tipos(dados_pokemon)
estabelecer_relacionamentos_fraquezas(dados_pokemon)
estabelecer_relacionamentos_evolucoes(dados_pokemon)




sessao.close()
driver.close()
