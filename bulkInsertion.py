import pandas as pd
import json
import requests
import time
import unicodedata
import re

def excel_to_json(arquivo):
    try:
        # Ler o arquivo Excel
        df = pd.read_excel(f'{arquivo}.xlsx')

        # Preenchendo com string vazia, valores nulos na planilha
        df.fillna('', inplace=True)  

        # Converte para JSON
        json_data = df.to_json(orient='records', date_format='iso')
        
        # Normaliza a string para NFD (Caracter + Acento Separado)
        json_normalizado = unicodedata.normalize('NFD', json_data)
    
        # Usar regex para remover os caracteres que fazem parte da categoria de acentos
        json_formatado = re.sub(r'[\u0300-\u036f]', '', json_normalizado)

        # Retorna o JSON
        return json.loads(json_formatado)
    
    except FileNotFoundError:
        print(f"Arquivo {arquivo}.xlsx não encontrado.")
        return None

def enviar_para_backend(endpoint, dados_json):
    headers= {
           'ngrok-skip-browser-warning': 'true'
       }
    try:
        # Enviar o JSON para o back-end usando uma requisição POST
        response = requests.post(endpoint, json= dados_json, headers= headers)
        
        # Verificar se a requisição foi bem-sucedida
        if response.status_code == 201:
            print(f"Dados enviados com sucesso para {endpoint}")
            time.sleep(120)
        else:
            print(f"Falha ao enviar dados. Status code: {response.status_code}")
            print(f"Resposta: {response.text}")
            time.sleep(120)
    
    except requests.exceptions.RequestException as e:
        print(f"Erro ao tentar se conectar com o back-end: {e}")
        time.sleep(120)

arquivos = []
continua = True

while continua:
    nome = input("""
                 Insira o nome do arquivo sem extensão (ou tecle Enter para finalizar):
                 Exemplo: Arquivo = teste.xlsx | Insira = teste
                 """)
    if not nome:
        continua = False
    else:
        arquivos.append(nome)

url_backend = 'https://daring-bat-mostly.ngrok-free.app/usuarios/completo/cadastro'  #  URL backend

for arquivo in arquivos:
    json_result = excel_to_json(arquivo)
    
    if json_result is not None:
        # Print do resultado em JSON
        print(f"JSON gerado para o arquivo {arquivo}:")
        print(json.dumps(json_result, indent=4))
        
        # Enviar o JSON para o back-end
        enviar_para_backend(url_backend, json_result)
