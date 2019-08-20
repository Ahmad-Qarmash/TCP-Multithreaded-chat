import argparse
import pickle
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import re
from time import gmtime, strftime


def receive():
    """Handles receiving of messages."""
    try:
        while True:
            msg = client_socket.recv(BUFFER_SIZE).decode("utf8")
            if not msg:
                break
            else:
                if msg == "SUCCESS":
                    print("\n message sent Successfully")
                else:
                    x = strftime("%H:%M", gmtime())
                    print("\n", x, "- ", msg)
    except Exception as e:  # Possibly client has left the chat.
        print("Connection Ended")


def send():
    """Handles sending of messages."""
    while True:
        print(" \n Type {send} to send a message , {quit} to close the connection , {chs} to change the status ,{history} to Print history")
        info_list = []
        msg_type = input(str("\n Enter your option:"))
        info_list.append(msg_type)
        if msg_type == "{quit}":
            message_type = pickle.dumps(info_list)
            client_socket.send(message_type)
            client_socket.close()
            exit()
        elif msg_type == "{history}":
            rcv = input(str("\n Enter the id to print the history with him: "))
            try:
                f = open(f"{client_id}to{rcv}.txt", "r")
                if f.mode == 'r':
                    contents = f.read()
                    print(contents)
            except:
                print("No History")
        elif msg_type == "{chs}":
            message_type = pickle.dumps(info_list)
            client_socket.send(message_type)
        elif msg_type == "{send}":
            receiver = input(str("\n Enter an id to send him a message: "))
            msg = input(str("\n my message >> "))
            info_list.append(receiver)
            info_list.append(msg)
            message_info = pickle.dumps(info_list)
            client_socket.sendall(message_info)
        else:
            print("Please Enter a valid input")


# We are trying to initialize the parser
parser = argparse.ArgumentParser()
parser.add_argument("name", help="Enter your name: ")
parser.add_argument("jop", help="Enter your Jop Title: ")
parser.add_argument("company", help="Enter your Company Name: ")
# Trying to parse the argument
try:
    args = parser.parse_args()
    name = args.name
    jop = args.jop
    company = args.company
    information = [name, jop, company]
    data = pickle.dumps(information)
except:
    print("Incorrect Information for the client")
    exit()
# <sockets section>
HOST = "localhost"
PORT = 33301
BUFFER_SIZE = 1024
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect((HOST, PORT))
print("connected to the server")
client_socket.send(data)
message = client_socket.recv(BUFFER_SIZE).decode("utf8")
if "Welcome to the server your id is" in message:
    t = strftime("%H:%M", gmtime())
    print(t, "Server Message:", message)
    client_id = re.findall('\d+', message)[0]
while 1:
    receive_thread = Thread(target=receive)
    receive_thread.start()
    send()
