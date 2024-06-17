import datetime

from mysql.connector import connect, Error

from telegram import Bot

import logging

 

# Configuração do logging para depuração

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

 

# Token do seu Bot do Telegram

TOKEN = '7346286604:AAF0_pC-radfTKxTvvufc4_IKs5IhMaFMQs'

 

# Função para conectar ao banco de dados MySQL

def mysql_connection(host, user, passwd, database=None):

    try:

        conn = connect(

            host=host,

            user=user,

            passwd=passwd,

            database=database

        )

        logger.info("Conexão com o banco de dados estabelecida com sucesso.")

        return conn

    except Error as e:

        logger.error(f"Erro ao conectar ao banco de dados: {e}")

        return None

 

# Função para obter o ID de um usuário do Telegram a partir de um ID específico no banco de dados

def get_user_telegram_id(conn, specific_user_id):

    try:

        cursor = conn.cursor()

        cursor.execute("SELECT informacoes_contato FROM contato WHERE id = %s", (specific_user_id,))

        row = cursor.fetchone()

        if row:

            logger.info(f"Telegram ID encontrado para o usuário {specific_user_id}: {row[0]}")

            return row[0]

        logger.warning(f"Usuário com ID específico {specific_user_id} não encontrado no banco de dados.")

        return None

    except Error as e:

        logger.error(f"Erro ao buscar o ID do usuário: {e}")

        return None

    finally:

        cursor.close()

 

# Função para enviar mensagem inicial e desligar o bot

def enviar_mensagem_inicial_e_desligar():

    try:

        # Conectar ao banco de dados

        conn = mysql_connection('localhost', 'root', 'sarabi3011', 'TFG')

        if conn:

            # ID específico do usuário no banco de dados

            specific_user_id = 1  # Substitua pelo ID específico que você quer utilizar

           

            # Obtém o ID do usuário do Telegram a partir do ID específico no banco de dados

            user_telegram_id = get_user_telegram_id(conn, specific_user_id)
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

    # Envia mensagem inicial e desliga o bot após enviar

    enviar_mensagem_inicial_e_desligar()

 

if __name__ == '__main__':

    main()
