import pika
from pika import BlockingConnection,PlainCredentials,BlockingConnection,ConnectionParameters,BasicProperties
from dotenv import load_dotenv
import time
from src.processing.processFile import ProcessFiles
load_dotenv()
import os

class ConsumeQueue:

    def __init__(self,process: ProcessFiles):
        self.user       =   os.environ["USER_RABBITMQ"] 
        self.password   =   os.environ["PASSWORD_RABBITMQ"] 
        self.exchange   =   os.environ["EXCHANGE_RABBITMQ"] 
        self.routingKey =   os.environ["ROUTINGKEY_RABBITMQ"]
        self.process = process

    def createConnection(self) -> BlockingConnection:
        retries = 5
        delay = 3  
        for attempt in range(retries):
            try:
                credentials = PlainCredentials(self.user, self.password)
                connection = BlockingConnection(ConnectionParameters(host="localhost", credentials=credentials,heartbeat=600))
                return connection
            except Exception as e:
                print(f"[TENTATIVA {attempt+1}/{retries}] Erro ao conectar ao RabbitMQ: {e}")
                time.sleep(delay)
        raise ValueError("Não foi possível conectar ao RabbitMQ após várias tentativas.")


    def consumeMessageQueue(self) -> None:
        connection = self.createConnection()
        channel = connection.channel()

        try:
            channel.queue_declare(queue="C", durable=True)

            def callback(ch, method, properties, body):
                print(f"Mensagem recebida: {body.decode()}")
                self.process.getMessageFromQueue(str(body.decode()))
                ch.basic_ack(delivery_tag=method.delivery_tag)

            channel.basic_consume(queue="C", on_message_callback=callback)

            print("Aguardando mensagens... Pressione CTRL+C para sair.")
            channel.start_consuming()

        except Exception as e:
            print(f"Erro ao consumir mensagens: {e}")

        finally:
            if connection.is_open:
                try:
                    connection.close()
                except Exception as e:
                    print(f"Erro ao fechar conexão: {e}")
