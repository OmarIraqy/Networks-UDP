import socket

def receive_message(server_address, server_port):
    # Create a UDP socket
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        # Bind the socket to the server address and port
        sock.bind((server_address, server_port))
        print(f"Listening on {server_address}:{server_port}")
        
        # Receive messages continuously
        while True:
            # Receive data from the socket
            data, addr = sock.recvfrom(1024)  # Buffer size is 1024 bytes
            print(f"Received: {data.decode()} from {addr}")
            
            # Send Message back to Sender
            message = "Received Thanks"
            sock.sendto(message.encode(), addr) 


receiver_ip = "localhost" 
receiver_port = 12345
# Receive messages on the server
receive_message(receiver_ip, receiver_port)
