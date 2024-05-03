import socket

def send_message(message, receiver_ip, receiver_port):
    # Create a UDP socket
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        # Send the message
        sock.sendto(message.encode(), (receiver_ip, receiver_port))
        print(f"Sent: {message}")
        while True:
            # Receive data from the socket
            data, addr = sock.recvfrom(1024)  # Buffer size is 1024 bytes
            print(f"Received: {data.decode()} from {addr}")





# Sender settings
receiver_ip = "localhost"  # Using localhost
receiver_port = 12345
# Example message to send
message_to_send = "Hello, UDP Server!"
# Send message to the server
send_message(message_to_send, receiver_ip, receiver_port)
