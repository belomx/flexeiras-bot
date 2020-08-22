import sender

def work(json_body):
    sender.publish_text(json_body['customer_id'], "echo " + json_body['message'])