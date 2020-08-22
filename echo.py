import sender
import re

def work(json_body):
    content = re.sub("echo ", "", json_body['message'], flags=re.I)
    result = content.split(" ")[1]
    sender.publish_text(json_body['customer_id'], result)