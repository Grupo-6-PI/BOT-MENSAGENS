import smtplib
import ssl
from email.message import EmailMessage
from mysql.connector import connect, Error
import time

def mysql_connection(host, user, passwd, database=None):
    return connect(host=host, user=user, passwd=passwd, database=database)

def send_email(nome,receiverAdress):
    
    email_sender = 'paulocafasso@gmail.com'
    email_password = 'wamz uxat tmlv ixpj'
    nome = nome
    
    subject = 'Pedido Mooca Solidária'
    body = """
        Olá, {nome}!
        Nós da Mooca Solidária temos o prazer de dizer que está tudo pronto para você, agora é só vir buscar.
        Caso não se lembre do endereço: RUA PADRE RAPOSO, 397 - MOOCA - SÃO PAULO - SP
        (Por favor não responder esse e-mail)
    """

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = receiverAdress
    em['Subject'] = subject
    em.set_content(body)

    # Adiciona SSL (camada de segurança)
    context = ssl.create_default_context()

    # Faz login e envia email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, receiverAdress, em.as_string())

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
        result = cursor.fetchall()
        
        for resultado in result:
            send_email(*resultado)
           
    except Error as e:
        print(f"Erro de conexão: {e}")
        
    finally:
        if connection.is_connected():
            connection.close()
    
    
    
    # cron schedule - - > não use while true