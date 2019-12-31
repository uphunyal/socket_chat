import socket
from threading import Thread
import pickle

#Receive the message from the server.
def receive_message():
    while True:
        data = client_socket.recv(4028)
        new_data= pickle.loads(data)
        print(new_data[2], ": ", new_data[3])

#Connect to server

HOST = input("Please enter server IP: ")
PORT = int(input("Please enter port to connect: "))
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
print("Connection successful! \n\n")

#Get username
Username = input("Enter your username: ")
#Username length in 2 bytes
UsernameL =  (len(Username)).to_bytes(2, byteorder='big')
Message=''
#Message Length in 4 bytes
MessageL= (len(Message)).to_bytes(4, byteorder='big')

#Standard tuple of 2 bytes username length, 4 bytes message length, n bytes username, and n bytes message
data = (UsernameL, MessageL, Username,Message)
new_data = pickle.dumps(data)

#Send username data
client_socket.send(new_data)

#Start thread to receive message
Thread(target = receive_message).start()

#Keep sending message until user enters exit
while True:
    #print(name,end = '')
    Message = input()
    MessageL= (len(Message)).to_bytes(4, byteorder='big')
    data = (UsernameL, MessageL, Username,Message)
    if Message=="exit":
        data = (UsernameL, MessageL, Username,Message)
        client_socket.send(pickle.dumps(data))
        print("Disconnected from chat server! Please restart the program if you want to continue! \n\n\n\n\n\n")
        break
    else:
        client_socket.send(pickle.dumps(data))
client_socket.close()