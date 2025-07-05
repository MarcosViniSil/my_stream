import json
from threading import Thread
import pika
from pika import BlockingConnection,PlainCredentials,BlockingConnection,ConnectionParameters,BasicProperties
import pika.exceptions as pexc
from dotenv import load_dotenv
import time
from src.processing.processFile import ProcessFiles
from src.repository.streamRepository import StreamRepository
from src.workers.processFilesWorker import ProcessFilesWorker
load_dotenv()
import os
import logging
from datetime import date
from queue import Queue

class ConsumeQueue:

    def __init__(self,process: ProcessFiles,streamRepository:StreamRepository,processWorker:ProcessFilesWorker):
        self.user       =   os.environ["USER_RABBITMQ"] 
        self.password   =   os.environ["PASSWORD_RABBITMQ"] 
        self.exchange   =   os.environ["EXCHANGE_RABBITMQ"] 
        self.routingKey =   os.environ["ROUTINGKEY_RABBITMQ"]
        self.process = process
        self.streamRepository = streamRepository
        self.worker = processWorker

    def createConnection(self) -> BlockingConnection:
        
        retries = 5
        delay = 3  
        for attempt in range(retries):
            try:
                credentials = PlainCredentials(self.user, self.password)
                connection = BlockingConnection(ConnectionParameters(host="localhost", credentials=credentials,heartbeat=600,blocked_connection_timeout=1800))
                return connection
            except Exception as e:
                print(f"[TENTATIVA {attempt+1}/{retries}] Erro ao conectar ao RabbitMQ: {e}")
                time.sleep(delay)
        raise ValueError("Não foi possível conectar ao RabbitMQ após várias tentativas.")
    

    def consumeMessageQueue(self) -> None:
        while True:
            connection = None
            try:
                connection = self.createConnection()
                channel = connection.channel()
                channel.queue_declare(queue="C", durable=True)
                channel.basic_qos(prefetch_count=1)

                resultQueue = Queue()

                def callback(ch, method, properties, body):
                    logging.info(f"[FILA] Mensagem recebida: {body.decode()}")

                    def worker():
                        try:
                            data = json.loads(body.decode().replace("'", '"'))
                            videoId = data["videoId"]
                            bucketName = data["videoUrl"].split("/")[-2]
                            fileName = data["videoUrl"].split("/")[-1]
                            taskId = self.streamRepository.saveTask(videoId, bucketName, fileName)
                            self.worker.processTask(
                                taskId=taskId,
                                videoId=videoId,
                                bucket=bucketName,
                                fileName=fileName
                            )
                            resultQueue.put((method.delivery_tag, True))
                        except Exception as e:
                            logging.error(f"[FILA] Erro ao processar tarefa: {e}")
                            resultQueue.put((method.delivery_tag, False))

                    Thread(target=worker, daemon=True).start()

                channel.basic_consume(queue="C", on_message_callback=callback)

                logging.info("Aguardando mensagens... Pressione CTRL+C para sair.")

                while True:
                    connection.process_data_events(time_limit=1)

                    while not resultQueue.empty():
                        delivery_tag, success = resultQueue.get()
                        if success:
                            channel.basic_ack(delivery_tag=delivery_tag)
                        else:
                            channel.basic_nack(delivery_tag=delivery_tag, requeue=False)

            except (pexc.AMQPConnectionError, pexc.AMQPChannelError) as e:
                logging.error(f"Erro de conexão AMQP: {e}")
                time.sleep(5)

            except Exception as e:
                logging.error(f"Erro inesperado: {e}")
                time.sleep(5)

            finally:
                try:
                    if connection and connection.is_open:
                        connection.close()
                        logging.info("Conexão com RabbitMQ encerrada.")
                except Exception as e:
                    logging.error(f"Erro ao fechar conexão: {e}")


