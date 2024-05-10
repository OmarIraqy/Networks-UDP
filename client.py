from sender import Sender
from receiver import Receiver

class Client:
    def __init__(self, receiver_ip, receiving_port, sender_ip, sending_port, receiver_port, sender_port):
        self.receiver = Receiver(receiver_ip, receiving_port, sender_ip, sender_port)
        self.sender = Sender(sender_ip, sending_port, receiver_ip, receiver_port, timeout=1)

    def start(self, data):
        self.sender.handshake()
        # Assume data contains the HTTP request
        self.sender.send_data(data)
        response = self.receiver.start()
        return response

# Usage
client = Client(receiver_ip='127.0.0.1', receiving_port=54321, sender_ip='127.0.0.1', sending_port=12345, receiver_port=12346, sender_port=54322)
data = "POST test.txt HTTP/1.1\r\nHost: localhost\r\n\r\nFinal Test"
response = client.start(data)
print(response)
