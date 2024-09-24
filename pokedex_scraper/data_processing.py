# pokedex_scraper/data_processing.py

import pandas as pd
import json

def load_data(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def clean_data(data):
    df = pd.DataFrame(data)
    # Remover entradas com dados obrigatórios ausentes
    df.dropna(subset=['numero', 'nome', 'url'], inplace=True)
    # Converter tipos numéricos
    df['numero'] = df['numero'].astype(int)
    df['tamanho_cm'] = pd.to_numeric(df['tamanho_cm'], errors='coerce')
    df['peso_kg'] = pd.to_numeric(df['peso_kg'], errors='coerce')
    # Remover ou preencher valores nulos
    df.fillna({'tamanho_cm': 0, 'peso_kg': 0}, inplace=True)
    return df

def main():
    data = load_data('output/pokedex.json')  # Ajuste o caminho conforme necessário
    df = clean_data(data)
    # Salvar o DataFrame limpo em um novo arquivo JSON ou CSV
    df.to_json('output/pokedex_clean.json', orient='records', indent=4)
    df.to_csv('output/pokedex_clean.csv', index=False)
    print("Dados processados e salvos com sucesso.")

if __name__ == "__main__":
    main()
