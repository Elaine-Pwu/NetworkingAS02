# Name: 蒲依蓮
# ID: 110306081
# Department: MIS

import struct
import socket
from threading import Thread

TFTP_PORT = 6969

def download_thread(fileName, clientInfo):
    print("Responsible for processing client download files")

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    fileNum = 0

    try:
        f = open(fileName, 'rb')
    except FileNotFoundError:
        errorData = struct.pack('!HHHb', 5, 5, 5, fileNum)
        s.sendto(errorData, clientInfo)
        exit()

    while True:
        readFileData = f.read(512)
        fileNum = (fileNum + 1) % 65536

        sendData = struct.pack('!HH', 3, fileNum) + readFileData
        s.sendto(sendData, clientInfo)

        if len(readFileData) < 512:
            print(f"User {clientInfo}: Download {fileName} completed!")
            break

        recvData, clientInfo = s.recvfrom(1024)

        packetOpt, packetNum = struct.unpack("!HH", recvData[:4])

        if packetOpt != 4 or packetNum != fileNum:
            print("File transfer error!")
            break

    f.close()
    s.close()
    exit()

def upload_thread(fileName, clientInfo):
    print("Responsible for processing client upload files")

    fileNum = 0
    f = open(fileName, 'wb')
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sendDataFirst = struct.pack("!HH", 4, fileNum)
    s.sendto(sendDataFirst, clientInfo)

    while True:
        recvData, clientInfo = s.recvfrom(1024)
        packetOpt, packetNum = struct.unpack("!HH", recvData[:4])

        if packetOpt == 3 and packetNum == fileNum:
            f.write(recvData[4:])
            sendData = struct.pack("!HH", 4, fileNum)
            s.sendto(sendData, clientInfo)
            fileNum = (fileNum + 1) % 65536

            if len(recvData) < 516:
                print(f"User {clientInfo}: Upload {fileName} complete!")
                break

    f.close()
    s.close()
    exit()

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('127.0.0.1', 6969))

    print("TFTP Server start successfully!")
    print("Server is running...")

    while True:
        recvData, clientInfo = s.recvfrom(516)

        if struct.unpack('!b5sb', recvData[-7:]) == (0, b'octet', 0):
            opcode, fileName = struct.unpack('!H', recvData[:2])[0], recvData[2:-7].decode('ascii')

            if opcode == 1:
                t = Thread(target=download_thread, args=(fileName, clientInfo))
                t.start()
            elif opcode == 2:
                t = Thread(target=upload_thread, args=(fileName, clientInfo))
                t.start()

if __name__ == '__main__':
    main()
# ------------------------------------------------------------------------------------------------------------------------
# import socket
# import struct
# from threading import Thread

# TFTP_PORT = 6969

# def handle_download(client_addr, filename):
#     """Handle download request from client"""
#     # Open file, send data, handle ACKs
#     print("Responsible for processing client download files")

#     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     fileNum = 0
#     print("file_n "+fileNum)

#     try:
#         f = open(filename, 'rb')
#     except FileNotFoundError:
#         errorData = struct.pack('!HHHb', 5, 5, 5, fileNum)
#         s.sendto(errorData, client_addr)
#         exit()

#     while True:     
#         readFileData = f.read(512)
#         fileNum = (fileNum + 1) % 65536
#         print("file_n "+fileNum)


#         sendData = struct.pack('!HH', 3, fileNum) + readFileData
#         s.sendto(sendData, client_addr)
#         print("sendData "+sendData)
#         print("client_addr "+client_addr)

#         if len(readFileData) < 512:
#             print(f"User {client_addr}: Download {filename} completed!")
#             break

#         recvData, client_addr = s.recvfrom(1024)

#         packetOpt, packetNum = struct.unpack("!HH", recvData[:4])

#         if packetOpt != 4 or packetNum != fileNum:
#             print("File transfer error!")
#             break

# def handle_upload(client_addr, filename):   
#     """Handle upload request from client""" 
#     # Open file, receive data, handle ACKs
#     print("Responsible for processing client upload files")

#     fileNum = 0





# def validate_packet(data):
#     """Validate TFTP packet"""
#     # Check opcode, sequence number, etc
#     opcode = struct.unpack('!H', data[:2])[0]
#     if opcode == 1:
#         print("RRQ")
#     elif opcode == 2:
#         print("WRQ")
#     elif opcode == 3:
#         print("DATA")
#     elif opcode == 4:
#         print("ACK")
#     elif opcode == 5:
#         print("ERROR")
#     else:
#         print("Invalid opcode")


# def send_ack(client_addr, block_num):
#     """Send ACK packet"""
#     # Create ACK packet and send

# def send_error(client_addr, error_code):
#     """Send error packet"""
#     # Create error packet and send

# def send_data(client_addr, block_num, data):
#     """Send data packet"""
#     # Create data packet and send

#     pass    
# def serve_client(client_addr):
#     """Handle file transfer for a client"""
#     while True:
#         # Receive request 
#         # Call handle_download or handle_upload
#         # Break when transfer complete

#         # Validate packet

#         # Check opcode
#         # If read request, call handle_download
#         # If write request, call handle_upload
#         # Else, send error packet

#         # Send ACK

#         # Check if transfer complete
#         # If complete, break
#         pass

# def main():
#     server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     server.bind(('127.0.0.1', TFTP_PORT))

#     print("TFTP server running on port", TFTP_PORT)

#     while True:
#         data, client_addr = server.recvfrom(516)
        
#         # Start thread to serve client
#         t = Thread(target=serve_client, args=(client_addr,))
#         t.start()

# if __name__ == "__main__":
#     main()
# # ------------------------------------------------------------------------------------------------------------------------
# # import socket
# # import struct
# # from threading import Thread

# # TFTP_PORT = 6969

# # def handle_download(client_socket, client_addr, filename):
# #     """Handle download request from client"""
# #     # Open the file for reading
# #     try:
# #         with open(filename, 'rb') as file:
# #             data = file.read(512)
# #             block_number = 1

# #             while data:
# #                 # Construct the DATA packet
# #                 packet = struct.pack("!HH", 3, block_number) + data

# #                 # Send the DATA packet
# #                 client_socket.sendto(packet, client_addr)

# #                 # Wait for the ACK
# #                 ack_packet, _ = client_socket.recvfrom(4)

# #                 # Validate the ACK packet
# #                 if validate_packet(ack_packet, 4, block_number):
# #                     # Move to the next block
# #                     block_number += 1
# #                     data = file.read(512)
# #                 else:
# #                     print("Invalid ACK. Retrying...")
# #     except FileNotFoundError:
# #         print("File not found:", filename)
# #         # Inform the client about the error
# #         error_packet = struct.pack("!HH", 5, 1) + b"File not found\0"
# #         client_socket.sendto(error_packet, client_addr)

# # def handle_upload(client_socket, client_addr, filename):
# #     """Handle upload request from client"""
# #     # Open the file for writing
# #     with open(filename, 'wb') as file:
# #         block_number = 1

# #         while True:
# #             # Wait for the DATA packet
# #             data_packet, _ = client_socket.recvfrom(516)

# #             # Validate the DATA packet
# #             if validate_packet(data_packet, 3, block_number):
# #                 # Extract the data from the DATA packet
# #                 data = data_packet[4:]

# #                 # Write the data to the file
# #                 file.write(data)

# #                 # Construct and send the ACK packet
# #                 ack_packet = struct.pack("!HH", 4, block_number)
# #                 client_socket.sendto(ack_packet, client_addr)

# #                 # Move to the next block
# #                 block_number += 1

# #                 # Check if it's the last block
# #                 if len(data) < 512:
# #                     break
# #             else:
# #                 print("Invalid DATA packet. Retrying...")

# # def validate_packet(packet, expected_opcode, expected_block_number):
# #     """Validate TFTP packet"""
# #     opcode, block_number = struct.unpack("!HH", packet[:4])
# #     return opcode == expected_opcode and block_number == expected_block_number

# # def serve_client(client_addr):
# #     """Handle file transfer for a client"""
# #     client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# #     client_socket.bind(('127.0.0.1', 0))

# #     while True:
# #         # Receive request
# #         request_packet, _ = client_socket.recvfrom(516)

# #         # Validate the request packet
# #         if validate_packet(request_packet, 1, 0):  # Assuming 1 is the opcode for read request
# #             filename = request_packet[2:-1].decode('utf-8')
# #             print(f"Received download request for {filename} from {client_addr}")

# #             # Call handle_download
# #             handle_download(client_socket, client_addr, filename)
# #             break
# #         elif validate_packet(request_packet, 2, 0):  # Assuming 2 is the opcode for write request
# #             filename = request_packet[2:-1].decode('utf-8')
# #             print(f"Received upload request for {filename} from {client_addr}")

# #             # Call handle_upload
# #             handle_upload(client_socket, client_addr, filename)
# #             break
# #         else:
# #             print("Invalid TFTP request. Ignoring...")

# # def main():
# #     server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# #     server.bind(('127.0.0.1', TFTP_PORT))
# #     # client_addr = "127.0.0.1"
# #     data = "test.txt"

# #     print("TFTP server running on port", 6969)
# #     # print(client_addr)

# #     while True:
# #         data, client_addr = server.recvfrom(1024)

# #         # Start thread to serve client

# #         t = Thread(target=serve_client, args=(client_addr,)).start()
# #         # t.start()

# # if __name__ == "__main__":
# #     main()
