import smtplib
import ssl
from email.message import EmailMessage
from mysql.connector import connect, Error

def mysql_connection(host, user, passwd, database=None):
    return connect(host=host, user=user, passwd=passwd, database=database)

def send_email(*resultado):
    
    #configurar email da mooca solidária
    email_sender = 'paulocafasso@gmail.com'
    #configurar senha de app na conta google a qual pertence o email a cima
    email_password = 'wamz uxat tmlv ixpj' 
    nome = resultado[0]

    print(resultado[0])
    print(resultado[1])

    subject = 'Doação Pronta para Retirada na Mooca Solidária'
    body = f"""
        Olá {nome},

        Esperamos que você esteja bem!

        Viemos informar que a doação solicitada por você está pronta para retirada. Abaixo estão os detalhes:

        Local de Retirada: RUA PADRE RAPOSO, 397 - MOOCA - SÃO PAULO - SP
        Horário Disponível para Retirada: 9:00 - 18:00
        Contato: +55 (11) 98081-8010
        (Favor não responder a esse e-mail)
        

        Agradecemos pela oportunidade de contribuir e aguardamos sua visita/retirada.

        Atenciosamente,

        Mooca Solidária
        instagram - moocasolidaria
    """

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = resultado[1]
    em['Subject'] = subject
    em.set_content(body)

    # Adiciona SSL (camada de segurança)
    context = ssl.create_default_context()

    # Faz login e envia email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, resultado[1], em.as_string())

def main():
    try:
        connection = mysql_connection('localhost', 'root', 'root', 'tfg')
        cursor = connection.cursor()
        
        # query escrita de forma que busque no banco os nomes e email de todos 
        # os usuários com requisições em situação concluida nas ultimas 3 horas
        email_query = '''
            SELECT u.nome, u.email
            FROM usuario u
            JOIN requisicoes r ON u.id = r.usuario_id
            JOIN situacao s ON r.situacao_id = s.id
            WHERE s.situacao = 'Concluida'
            AND r.data_ultima_atualizacao >= NOW() - INTERVAL 3 HOUR;
        '''
        cursor.execute(email_query)
        resultados = cursor.fetchall()
        
        #TESTES MOCKADOS
        #resultados =[ 
        #('Aeris', 'aeris.rasmussen@sptech.school'),
        #('Bianca', 'bianca.reis@sptech.school'),
        #('Davi', 'davi.rsilva@sptech.school'),
        #('Julio', 'julio.dahi@sptech.school'),
        #('Tiago','tiago.navarro@sptech.school')
        #]
        
        
        for resultado in resultados:
            print(resultado)
            send_email(*resultado)
           
    except Error as e:
        print(f"Erro de conexão: {e}")
        
    finally:
        if connection.is_connected():
            connection.close()


if __name__ == "__main__":
    main()
