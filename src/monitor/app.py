from flask import Flask
from os import getenv
import zmq

app = Flask(__name__)

zmq_context = zmq.Context()

messages = []

@app.route('/', methods=['GET'])
def index():
  return '\n'.join(map(lambda m : m.decode('utf-8'), messages))

def pull_messages():
  with zmq_context.socket(zmq.PULL) as socket:
    socket.bind(f'tcp://*:{getenv('MONITOR_PORT')}')
    while True:
      message = socket.recv()
      messages.append(message)

if __name__ == '__main__':
  from threading import Thread
  message_puller = Thread(target=pull_messages)
  message_puller.daemon = True
  message_puller.start()
  app.run(host='0.0.0.0', port=getenv('SERVICE_PORT', 80))
