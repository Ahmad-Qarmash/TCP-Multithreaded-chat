"""Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import pickle
import os
from time import gmtime, strftime
import signal


clients = {}
connections = set()
HOST = ''
PORT = 33301
BUFFER_SIZE = 1024
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind((HOST, PORT))
SERVER.listen(3)

def broadcast(current_sock, msg):
    """Broadcasts a message to all the clients."""
    for sock in connections:
        if sock != current_sock:
            sock.sendall(bytes(msg, "utf8"))


def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""
    while True:
        try:
            client_id = client.fileno()
            name = clients[client_id]["Name"]

            data = client.recv(BUFFER_SIZE)
            data = pickle.loads(data)
            msg_type = data[0]

            if msg_type == "{quit}":
                broadcast(client, f"\n {name} has left the chat.")
                client.close()
                del clients[client_id]
                connections.remove(client)

                # get the current working directory 
                cwd = os.getcwd()
                # get every file that starts with the client_id (that belongs to the quited client)
                file_list = [f for f in os.listdir(cwd) if f.startswith(f"{client_id}")]
                # delete the history of that client
                for f in file_list:
                    os.remove(os.path.join(cwd, f))
                break

            elif msg_type == "{chs}":
                state = clients[client_id]["Status"]
                if state == "Available":
                    broadcast(client, f"\n {name} is Not Available now")
                    clients[client_id]["Status"] = "Unavailable"
                else:
                    broadcast(client, f"\n {name} is  Available now.")
                    clients[client_id]["Status"] = "Available"

            elif msg_type == "{send}":
                try:
                    receiver_id = int(data[1])
                except ValueError:
                    print("Non integer value")
                    client.sendall(bytes("invalid ID (Not an Integer)", "utf8"))
                else:
                    # save the sended message into variable
                    msg = data[2]
                    if receiver_id not in clients:
                        client.sendall(bytes(" ID Does Not Exist)", "utf8"))
                    else:
                        # this loop used to get the receiver object in order to send him the message sent from the client
                        for connection in connections:
                            fd = int(connection.fileno())
                            if receiver_id == fd:
                                # check the availability of the reciever
                                if clients[receiver_id]["Status"] == "Available":
                                    print("SUCCESS")
                                    # when you send the message to yourself
                                    if(receiver_id == client_id):
                                        client.sendall(bytes("\n you sent the message to yourself successfully", "utf8"))
                                    else:
                                        client.sendall(bytes("SUCCESS", "utf8"))
                                        msg = clients[client_id]["Name"] + ", " + clients[client_id]["Title"] + ", " + clients[client_id]["Company"] + ": \n" + f"   {msg}"
                                        connection.sendall(bytes(msg, "utf8"))
                                        # create a file and append messages on this file
                                        filename = f"{client_id}to{receiver_id}.txt"
                                        with open(filename, "a") as f:
                                            x = strftime("%H:%M", gmtime())
                                            f.write(f"{x} - {msg} \r\n")
                                            f.close()
                                        # this is to store both sended and recieved messages
                                        reverse = f"{receiver_id}to{client_id}.txt"
                                        # this if used to not store the self message twice 
                                        if filename != reverse:
                                            with open(reverse, "a") as f:
                                                x = strftime("%H:%M", gmtime())
                                                f.write(f"{x} - {msg} \r\n")
                                                f.close()
                                else:
                                    msg = "send failed " + clients[receiver_id]["Name"] +" is not alive right now"
                                    client.sendall(bytes(msg, "utf8"))
            else:
                print("\n Please Enter a valid input")
        except Exception as e:
            '''
            if e.errno == 10054.:
                print("window closed by force")
                
            '''


def handle_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client_sock, client_address = SERVER.accept()
    
        connections.add(client_sock)

        client_id = client_sock.fileno()
        client_sock.sendall(bytes(f"Welcome to the server your id is {client_id}", "utf8"))

        data = client_sock.recv(BUFFER_SIZE)

        # Pickling is a way to convert a python object (list, dict, etc.) into a character stream. 
        # The idea is that this character stream contains all the information necessary to reconstruct the object in another python script.
        data = pickle.loads(data)
        client_name = data[0]
        client_title = data[1]
        client_company =  data[2]
        print(client_name, "has connected at address", client_address)
        clients[client_id] = {"Name": client_name, "Title": client_title, "Company": client_company, "Status": "Available"}
        print(clients)

        Thread(target=handle_client, args=(client_sock,)).start()


def main():
    
    print("Waiting for connections...")

    ACCEPT_THREAD = Thread(target=handle_incoming_connections)
    ACCEPT_THREAD.start()  # Starts the infinite loop.
    ACCEPT_THREAD.join()
    SERVER.close()
    
   
if __name__ == "__main__":
    main()
   