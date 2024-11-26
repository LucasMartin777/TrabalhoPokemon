import json
import pandas as pd # type: ignore

def process_pokedex_data(input_file, output_file):
    """
    Processa o arquivo JSON gerado pelo Scrapy, para preparar dados para o Neo4j.
    """
    with open(input_file, 'r') as f:
        data = json.load(f)

    processed_data = []
    for pokemon in data:
        processed_data.append({
            "name": pokemon["name"],
            "types": pokemon["types"],
            "weight": float(pokemon["weight"].replace(' kg', '')),  # Remove 'kg' e converte para float
            "evolves_to": pokemon.get("evolves_to", None),  # Evolução opcional
            "weaknesses": pokemon.get("weaknesses", []),
            "attacks": pokemon.get("attacks", [])
        })

    # Salva o resultado em um novo arquivo JSON
    with open(output_file, 'w') as f:
        json.dump(processed_data, f, indent=4)

    print(f"Dados processados salvos em: {output_file}")

if __name__ == "__main__":
    input_file = "../output/pokedex.json"  # Caminho do arquivo bruto
    output_file = "../output/pokedex_clean.json"  # Caminho do arquivo processado
    process_pokedex_data(input_file, output_file)
