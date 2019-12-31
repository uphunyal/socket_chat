from threading import Thread
import time
import socket
import pickle

#Save client socket and username 
client_username_dict  = {}

#Accept user connection and start a thread for communication between clients and server.
def handle_client():
    while True:
        socket_client, client_addr = server_socket.accept()
        print("New connectionL", client_addr)
        Thread(target = handle_messages, args = (socket_client,)).start()

#This handles all communication
def handle_messages(socket_client):

    #Get the username and send a welcome message to the user
    name = socket_client.recv(4028)
    new_name= pickle.loads(name)
    Username="Server"
    UsernameL=(len(Username)).to_bytes(2, byteorder='big')
    client_username_dict[socket_client] = new_name[2]
    Message= "Welcome to the Chat " + new_name[2] +"! Please enter exit if you want to exit the chat!"
    MessageL=(len(Message)).to_bytes(4, byteorder='big')
    new_tuple= (UsernameL, MessageL, Username, Message)

    #Send tuple
    socket_client.send(pickle.dumps(new_tuple))

    #Notify other users that user joined the chat.
    text= new_name[2] + " has joined the chat"
    print(text)
    status(text,"Server", socket_client )

    while True:
        get_message= socket_client.recv(4028)
        load_msg= pickle.loads(get_message)
        if load_msg[3]=="exit":
            newmessge= load_msg[2] + "has left the chat."
            print(newmessge)
            status(newmessge,"Server", socket_client )
            del client_username_dict[socket_client]
            break
        else:
            broadcast(get_message)
    socket_client.close()

#Function to let users if anyone has joined or left the chat. Sends to everyone except the original user.
def status(text, user, socket_client):
    new_tuple= ((len(user)).to_bytes(2, byteorder='big'), (len(text)).to_bytes(4, byteorder='big'), user, text)
    for c_socket in client_username_dict:
        if c_socket != socket_client:
            c_socket.send(pickle.dumps(new_tuple))

#Send message to all the clients  
def broadcast(msg):
    for c_socket in client_username_dict:
        c_socket.send(msg)

#Show the active users in the chat and broadcast it every one minute. 
def show_users():
    while True:
        name_list= list(client_username_dict.values())
        name_list= ", ".join(name_list)
        Message=  name_list + " are active in chat. \n"
        MessageL= (len(Message)).to_bytes(2, byteorder='big')
        Username="Server"
        UsernameL= (len(Username)).to_bytes(4, byteorder='big')
        newdata=(UsernameL, MessageL, Username, Message)
        for c_socket in client_username_dict:
            c_socket.send(pickle.dumps(newdata))
        time.sleep(60)

#Connection details

HOST = input("Please enter server IP: ")
PORT = int(input("Enter Port No for Server: "))
server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.bind(("localhost", 1234))
server_socket.listen(5)

print ("Waiting for users to connect")

#Start a thread for each client that connects to the server.
Thread (target = handle_client).start()

#Start a thread to broadcast active users in the server.
Thread (target = show_users).start()
