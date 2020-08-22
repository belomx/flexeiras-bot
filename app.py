import config
import pika
import json
import sender
import echo
import distorceImg

skills = { "echo": echo,
           "distorceImg": distorceImg }

def message_received(body):
    json_body = json.loads(body)
    if "message" in json_body and config.number in json_body['message']:
        action = json_body['message'].split(" ")[1]
        if action and action.lower() in skills:
            skills[action.lower()].work(json_body)

def listen():
    while(True):
        try:
            credentials = pika.PlainCredentials(config.rabbit_user, config.rabbit_password)
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=config.rabbit_address, credentials=credentials))
            channel = connection.channel()
            queue_name = 'router.customers_messages'
            exchange = 'exchange.customers_messages'
            channel.exchange_declare(exchange=exchange, exchange_type='direct', durable=True)
            queue = channel.queue_declare(
            exclusive=False, queue=queue_name, durable=True, arguments={"x-dead-letter-exchange": "router.customers_messages-retry"})
            channel.queue_bind(exchange=exchange, queue=queue_name, routing_key='')

            def callback(ch, method, properties, body):
                try:
                    print(" [x] Received %r" % body)
                    message_received(body)
                except Exception as msg_err:
                    print("message error: {}, continuing...".format(msg_err))


            print("started")
            channel.basic_consume(queue_name, callback, auto_ack=True)
            channel.start_consuming()
            

        except Exception as err:
            print("Caught a channel error: {}, continuing...".format(err))
            continue

print ("starting")
listen()
