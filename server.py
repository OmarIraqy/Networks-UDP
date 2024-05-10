from receiver import Receiver
from sender import Sender

class Server:
    def __init__(self, receiver_ip, receiving_port, sender_ip, sending_port, receiver_port, sender_port):
        self.receiver = Receiver(receiver_ip, receiving_port, sender_ip, sender_port)
        self.sender = Sender(sender_ip, sending_port, receiver_ip, receiver_port, timeout=1)

    def start(self):
        while True:
            self.receiver.handshake()

            data = self.receiver.start()
            if not data:
                break

            # Assume data contains the HTTP request
            lines = data.split('\r\n')
            request_line = lines[0].split(' ')
            method = request_line[0]
            path = request_line[1]

            # Handle GET request
            if method == 'GET':
                try:
                    with open(path, 'r') as file:
                        file_content = file.read()
                        response = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n" + file_content
                except FileNotFoundError:
                    response = "HTTP/1.1 404 Not Found\r\n"
                self.sender.send_data(response)

            # Handle POST request
            elif method == 'POST':
                try:
                    with open(path, 'w') as file:
                        file.write(lines[-1])
                    response = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nData written to file"
                except Exception as e:
                    response = "HTTP/1.1 500 Internal Server Error\r\n"
                self.sender.send_data(response)

            else:
                pass

# Usage
server = Server(receiver_ip='127.0.0.1', receiving_port=12346, sender_ip='127.0.0.1', sending_port=54322, receiver_port=54321, sender_port=12345)
server.start()
