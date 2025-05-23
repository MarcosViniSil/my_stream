import pika
from pika import BlockingConnection,PlainCredentials,BlockingConnection,ConnectionParameters,BasicProperties
from dotenv import load_dotenv
load_dotenv()
import os

class QueueService:

    def __init__(self):
        self.user       =   os.environ["USER_RABBITMQ"] 
        self.password   =   os.environ["PASSWORD_RABBITMQ"] 
        self.exchange   =   os.environ["EXCHANGE_RABBITMQ"] 
        self.routingKey =   os.environ["ROUTINGKEY_RABBITMQ"]


    def sendMessageQueue(self,message : dict) -> None:

        connection = self.createConnection()
        channel    = connection.channel()
        try:
            self.createQueue(channel)
            channel.basic_publish(exchange = self.exchange, routing_key = self.routingKey, body = str(message),
            properties=BasicProperties(delivery_mode=2))
            channel.close()
        except Exception as e:
            print(e)
            raise ValueError("Erro ao enviar mensagem para a fila")

    def createQueue(self,channel:BlockingConnection) -> None:
        channel.exchange_declare("test", durable=True, exchange_type="topic")
        channel.queue_declare(queue= "C",durable=True)
        channel.queue_bind(exchange="test", queue="C", routing_key="C")

    def createConnection(self) -> BlockingConnection:
        try:
            credentials = PlainCredentials(self.user,self.password)
            connection  = BlockingConnection(ConnectionParameters(host="localhost", credentials= credentials))
            return connection
        except Exception as e:
            raise ValueError("Erro ao criar conexão com a fila de mensagens")
