import pika
from pika import BlockingConnection,PlainCredentials,BlockingConnection,ConnectionParameters,BasicProperties
from dotenv import load_dotenv
load_dotenv()
import os

class ConsumeQueue:

    def __init__(self):
        self.user       =   os.environ["USER_RABBITMQ"] 
        self.password   =   os.environ["PASSWORD_RABBITMQ"] 
        self.exchange   =   os.environ["EXCHANGE_RABBITMQ"] 
        self.routingKey =   os.environ["ROUTINGKEY_RABBITMQ"]

    def createConnection(self) -> BlockingConnection:
        try:
            credentials = PlainCredentials(self.user, self.password)
            connection = BlockingConnection(ConnectionParameters(host="localhost", credentials=credentials))
            return connection
        except Exception as e:
            raise ValueError(f"Erro ao criar conexão com a fila de mensagens: {e}")

    def consumeMessageQueue(self) -> None:
        connection = self.createConnection()
        channel = connection.channel()

        try:
    
            channel.queue_declare(queue="C", durable=True)

            def callback(ch, method, properties, body):
                print(f"Mensagem recebida: {body.decode()}")
        
                ch.basic_ack(delivery_tag=method.delivery_tag)

            channel.basic_consume(queue="C", on_message_callback=callback)

            print("Aguardando mensagens... Pressione CTRL+C para sair.")
            channel.start_consuming()

        except Exception as e:
            print(f"Erro ao consumir mensagens: {e}")
        finally:
            connection.close()