import socket
from packet import Packet

class Sender:
    def __init__(self, sender_ip, sender_port, receiver_ip, receiver_port, timeout, data_size=20):
        self.sender_ip = sender_ip
        self.sender_port = sender_port
        self.receiver_ip = receiver_ip
        self.receiver_port = receiver_port
        self.timeout = timeout
        self.data_size = data_size
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(self.timeout)
        self.sock.bind((self.sender_ip, self.sender_port))

    def handshake(self):
        self.send_syn()
        self.wait_for_syn_ack()

    def send_syn(self):
        syn_packet = Packet('SYN', Packet.pick_id(), 0, 0, '')
        self.sock.sendto(syn_packet.to_bytes(), (self.receiver_ip, self.receiver_port))
        print("Sent SYN packet")

    def wait_for_syn_ack(self):
        try:
            syn_ack_bytes, _ = self.sock.recvfrom(1024)
            syn_ack_packet = Packet.from_bytes(syn_ack_bytes)
            if syn_ack_packet.get_type() == 'SYN-ACK':
                print("Received SYN-ACK, sending ACK")
                ack_packet = Packet('ACK', syn_ack_packet.id, syn_ack_packet.seq, 0, '')
                self.sock.sendto(ack_packet.to_bytes(), (self.receiver_ip, self.receiver_port))
            else:
                print("Did not receive SYN-ACK")
                exit()
        except socket.timeout:
            print("Timeout waiting for SYN-ACK")
            self.sock.close()
            exit()

    def send_data(self, data):
        self.handshake()
        seq_num = 2  # Start with the next sequence number after SYN
        while seq_num < len(data):
            # Create a new packet
            packet = Packet('DATA', Packet.pick_id(), seq_num, self.data_size, data[seq_num-2:seq_num-2 + self.data_size])

            # Serialize packet to bytes
            packet_bytes = packet.to_bytes()

            # Send packet
            self.sock.sendto(packet_bytes, (self.receiver_ip, self.receiver_port))
            print(f"Sent packet with seq_num={seq_num}")

            # Wait for acknowledgment
            try:
                ack, _ = self.sock.recvfrom(1024)
                ack_packet = Packet.from_bytes(ack)

                # Check if the acknowledgment is correct
                if ack_packet.get_type() == 'ACK' and ack_packet.id == packet.id:
                    print(f"Received ACK for seq_num={seq_num}")
                    seq_num += self.data_size  # Move to the next sequence number
            except socket.timeout:
                print(f"Timeout for seq_num={seq_num}, retransmitting...")
                # Timeout, retransmit the packet
                continue
        
        self.send_fin()
        self.wait_for_fin_ack()
        self.close()

    def send_fin(self):
        fin_packet = Packet('FIN', Packet.pick_id(), 0, 0, '')
        self.sock.sendto(fin_packet.to_bytes(), (self.receiver_ip, self.receiver_port))
        print("Sent FIN packet")

    def wait_for_fin_ack(self):
        try:
            fin_ack_bytes, _ = self.sock.recvfrom(1024)
            fin_ack_packet = Packet.from_bytes(fin_ack_bytes)
            if fin_ack_packet.get_type() == 'FIN-ACK':
                print("Received FIN-ACK, sending ACK")
                ack_packet = Packet('ACK', fin_ack_packet.id, fin_ack_packet.seq, 0, '')
                self.sock.sendto(ack_packet.to_bytes(), (self.receiver_ip, self.receiver_port))
            else:
                print("Did not receive FIN-ACK")
                exit()
        except socket.timeout:
            print("Timeout waiting for FIN-ACK")
            exit()

    def close(self):
        # Close the socket
        self.sock.close()
