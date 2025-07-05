import json
import pika
from pika import BlockingConnection,PlainCredentials,BlockingConnection,ConnectionParameters,BasicProperties
from pika.exceptions import StreamLostError, ChannelClosedByBroker
from dotenv import load_dotenv
import time
from src.processing.processFile import ProcessFiles
from src.repository.streamRepository import StreamRepository
load_dotenv()
import os
import logging
from datetime import date

class ConsumeQueue:

    def __init__(self,process: ProcessFiles,streamRepository:StreamRepository):
        self.user       =   os.environ["USER_RABBITMQ"] 
        self.password   =   os.environ["PASSWORD_RABBITMQ"] 
        self.exchange   =   os.environ["EXCHANGE_RABBITMQ"] 
        self.routingKey =   os.environ["ROUTINGKEY_RABBITMQ"]
        self.process = process
        self.streamRepository = streamRepository

    def createConnection(self) -> BlockingConnection:
        
        retries = 5
        delay = 3  
        for attempt in range(retries):
            try:
                credentials = PlainCredentials(self.user, self.password)
                connection = BlockingConnection(ConnectionParameters(host="localhost", credentials=credentials,heartbeat=3600))
                return connection
            except Exception as e:
                print(f"[TENTATIVA {attempt+1}/{retries}] Erro ao conectar ao RabbitMQ: {e}")
                time.sleep(delay)
        raise ValueError("Não foi possível conectar ao RabbitMQ após várias tentativas.")


    def consumeMessageQueue(self) -> None:
        connection = self.createConnection()
        channel = connection.channel()
        taskId = ""
        try:
            channel.queue_declare(queue="C", durable=True)
            channel.basic_qos(prefetch_count=1)
            def callback(ch, method, properties, body):
                print(f"mensagem recebida: {body.decode()}")
                try:
                    message = body.decode().replace("'", '"')
                    data = json.loads(message)
                    
                    videoId = str(data["videoId"])
                    bucketName = str(data["videoUrl"]).split("/")[-2]
                    fileName = str(data["videoUrl"]).split("/")[-1]
                    
                    taskId = self.streamRepository.saveTask(videoId, bucketName, fileName)
                    
                    self.process.getMessageFromQueue(videoId,bucketName,fileName)
                    
                    logging.info(f"Mensagem {body.decode()} processada com sucesso")
                except Exception as e:
                    logging.error(f"Ao processar mensagem {body.decode()} o seguinte erro aconteceu: {e}")
                finally:
                    try:
                        ch.basic_ack(delivery_tag=method.delivery_tag)
                        self.streamRepository.changeStatus(taskId,'READY')
                    except (StreamLostError, ChannelClosedByBroker) as e:
                        logging.error(f"Não foi possível enviar ACK porque a conexão já foi perdida: {e}")
                        self.streamRepository.changeStatus(taskId,'READY')
                    except Exception as e:
                        logging.error(f"Erro inesperado ao enviar ACK: {e}")
                        self.streamRepository.changeStatus(taskId,'FAIL')

            channel.basic_consume(queue="C", on_message_callback=callback)

            print("Aguardando mensagens... Pressione CTRL+C para sair.")
            channel.start_consuming()

        except Exception as e:
            logging.error(f"Ocorreu um erro ao procesar mensagem da fila, erro que ocorreu: {e}")

        finally:
            if connection.is_open:
                try:
                    connection.close()
                except Exception as e:
                    logging.error(f"Ocorreu um erro ao fechar conexão, erro que ocorreu: {e}")
