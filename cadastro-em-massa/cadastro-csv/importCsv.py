import requests
import time
import pandas as pd

def enviar_para_backend(endpoint, arquivo):
    headers= {
           'ngrok-skip-browser-warning': 'true'
       }
    try:
        # Enviar o CSV para o back-end usando uma requisição POST
        
        arquivo = arquivo.to_csv(index=False, sep=';', encoding='utf-8')
        
        response = requests.post(endpoint, data=arquivo)
        
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
                 Exemplo: Arquivo = teste.csv | Insira = teste
                 """)
    if not nome:
        continua = False
    else:
        arquivos.append(nome)


# url_backend = 'https://daring-bat-mostly.ngrok-free.app/usuarios/cadastro/massa/csv'  #  URL backend
url_backend = 'http://localhost:8080/usuarios/cadastro/massa/csv'  #  URL backend

for arquivo in arquivos:
    
    arquivo = pd.read_csv(f'{arquivo}.csv')

    enviar_para_backend(url_backend, arquivo)