import socket
from random import random
from packet import Packet

class Receiver:
    def __init__(self, receiver_ip, receiver_port, sender_ip, sender_port):
        self.receiver_ip = receiver_ip
        self.receiver_port = receiver_port
        self.sender_ip = sender_ip
        self.sender_port = sender_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.receiver_ip, self.receiver_port))
        self.flag = True

    def start(self):
        while self.flag:
            self.handshake()

            data = ''
            fin_flag = True
            while fin_flag:
                try:
                    data_bytes, _ = self.sock.recvfrom(1024)
                    data_packet = Packet.from_bytes(data_bytes)
                    if data_packet.get_type() == 'DATA':
                        print(f"Received data packet with seq_num={data_packet.seq}")
                        if data_packet.checksum == Packet.checksum(data_packet):
                            if random() >= 0.02:
                                data += data_packet.data
                                ack_packet = Packet('ACK', data_packet.id, data_packet.seq, 0, '')
                                self.sock.sendto(ack_packet.to_bytes(), (self.sender_ip, self.sender_port))
                            else:
                                print("Packet loss, discarding acknowledgment...")
                        else:
                            print("Corrupted data packet, discarding...")
                    elif data_packet.get_type() == 'FIN':
                        print("Received FIN, sending FIN-ACK")
                        fin_ack_packet = Packet('FIN-ACK', data_packet.id, data_packet.seq, 0, '')
                        self.sock.sendto(fin_ack_packet.to_bytes(), (self.sender_ip, self.sender_port))
                        fin_flag = False
                    else:
                        print("Did not receive FIN")
                except socket.timeout:
                    print("Timeout waiting for data, closing connection")
                    break


            try:
                ack_bytes, _ = self.sock.recvfrom(1024)
                ack_packet = Packet.from_bytes(ack_bytes)
                if ack_packet.get_type() == 'ACK':
                    print("Received ACK for FIN-ACK, closing connection")
                    break
                else:
                    print("Did not receive ACK for FIN-ACK")
                    break
            except socket.timeout:
                print("Timeout waiting for ACK")
                break
    
        self.sock.close()
        return data

    def handshake(self):
        flag = True
        while flag:
            syn_bytes, _ = self.sock.recvfrom(1024)
            syn_packet = Packet.from_bytes(syn_bytes)
            if syn_packet.get_type() == 'SYN':
                print("Received SYN, sending SYN-ACK")
                flag=False
                syn_ack_packet = Packet('SYN-ACK', syn_packet.id, syn_packet.seq, 0, '')
                self.sock.sendto(syn_ack_packet.to_bytes(), (self.sender_ip, self.sender_port))
            else:
                print("Did not receive SYN")
                continue

            try:
                ack_bytes, _ = self.sock.recvfrom(1024)
                ack_packet = Packet.from_bytes(ack_bytes)
                if ack_packet.get_type() == 'ACK' and ack_packet.id == syn_packet.id:
                    print("Received ACK, handshake complete")
                    break
                else:
                    print("Did not receive ACK for SYN-ACK")
                    break
            except socket.timeout:
                print("Timeout waiting for ACK")
                break