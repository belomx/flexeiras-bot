import json
import os
import pika
import config

def publish_text(to, content):
    body = { "customer_id": to, "content": content, "msg_id": 1 }
    json_string = json.dumps(body)
    print(json_string)
    queue_name = 'hook.whatsapp_outbound_message_' + config.number
    exchange = 'exchange.customers_messages'
    credentials = pika.PlainCredentials(config.rabbit_user, config.rabbit_password)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=config.rabbit_address, credentials=credentials))
    channel = connection.channel()
    channel.queue_bind(exchange=exchange, queue=queue_name, routing_key='')
    channel.basic_publish(exchange=exchange,
                            routing_key='',
                            body=json_string,
                            properties=pika.BasicProperties(
                                delivery_mode=2,
                            ))
    connection.close()