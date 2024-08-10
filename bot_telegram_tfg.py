import datetime

from mysql.connector import connect, Error

from telegram import Bot

import logging

from configparser import ConfigParser

# Configuração do logging para depuração

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

def get_data():
    try:
        
        logger.info("iniciando - get_data()")
        file = 'config.ini.txt'
        config = ConfigParser()
        config.read(file)

        logger.info(config.sections())

        return config
    
    except Error as e:
        
        logger.error(f"Erro na busca aos dados config.ini.txt :{e}")

        return None
 

# Função para conectar ao banco de dados MySQL

def mysql_connection(config):#host, user, passwd, database=None):
    logger.info("iniciando - mysql_connection")
    try:

            conn = connect(

                host=config["conn_bd"]["host"],
                
                user=config["conn_bd"]["user"],
                    
                passwd=config["conn_bd"]["passwd"],
                    
                database=config["conn_bd"]["database"]

            )
            logger.info(f"host = {conn._host}")
            logger.info(f"user = {conn._user}")
            logger.info(f"passwd = {conn._password}")
            logger.info(f"database = {conn._database}")

            logger.info("Conexão com o banco de dados estabelecida com sucesso.")

            return conn

    except Error as e:

            logger.error(f"Erro ao conectar ao banco de dados: {e}")

            return None

 

# Função para obter o ID de um usuário do Telegram a partir de um ID específico no banco de dados

def get_user_telegram_id(conn, config):
    logger.info("iniciando - get_user_telegram_id()")

    try:

        cursor = conn.cursor()

        cursor.execute("SELECT informacoes_contato FROM contato WHERE id = %s", config["user_id"]["specific_user_id"])

        row = cursor.fetchone()

        if row:

            logger.info("Telegram ID encontrado para o usuário %s: {row[0]}", config["user_id"]["specific_user_id"])

            return row[0]

        logger.warning(f"Usuário com ID específico %s não encontrado no banco de dados.", config["user_id"]["specific_user_id"])

        return None

    except Error as e:

        logger.error(f"Erro ao buscar o ID do usuário: {e}")

        return None

    finally:

        cursor.close()

 

# Função para enviar mensagem inicial e desligar o bot

def enviar_mensagem_inicial_e_desligar(conn, config):

    try:

        # Conectar ao banco de dados

        user_id = config["user_id"]["specific_user_id"]

        host = config["conn_bd"]["host"]

        passwd = config["conn_bd"]["passwd"]

        database = config["conn_bd"]["database"]

        user = config["conn_bd"]["user"]

        conn = mysql_connection(host,user,passwd,database)        
        
        if conn:

            # Obtém o ID do usuário do Telegram a partir do ID específico no banco de dados

            user_telegram_id = get_user_telegram_id(conn, config['user_id']['specific_user_id'])
            
            print(user_telegram_id)
           
            if user_telegram_id:

                bot = Bot(TOKEN)

                bot.send_message(chat_id=user_telegram_id, text='Bot iniciado. Olá! Este é o bot de avisos do Mooca Solidária.')

                logger.info("Mensagem enviada com sucesso.")

                bot.send_message(chat_id=user_telegram_id, text='Seu pedido de cesta foi concluído! Venha buscar sua cesta em 20/04.')

            else:

                logger.warning(f"Não foi possível enviar a mensagem. ID do usuário do Telegram não encontrado.")

           

            conn.close()

        else:

            logger.error("Falha ao estabelecer conexão com o banco de dados.")

    except Exception as e:

        logger.error(f"Erro ao enviar mensagem inicial: {e}")

 

def main():

    config = get_data()
    conn = mysql_connection(config)
        # Envia mensagem inicial e desliga o bot após enviar
    enviar_mensagem_inicial_e_desligar(conn, config)

 

if __name__ == '__main__':

    main()
