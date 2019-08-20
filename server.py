"""Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import pickle
import os
from time import gmtime, strftime
import signal


def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client_sock, client_address = SERVER.accept()
        connections.add(client_sock)
        client_id = client_sock.fileno()
        client_sock.sendall(bytes(f"Welcome to the server your id is {client_id}", "utf8"))
        data = client_sock.recv(BUFFER_SIZE)
        data = pickle.loads(data)
        print(data[0], "has connected at address", client_address)
        clients[client_id] = {"Name": data[0], "Title": data[1], "Company": data[2], "Status": "Available"}
        print(clients)
        Thread(target=handle_client, args=(client_sock,)).start()


def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""
    while True:
        try:
            client_id = client.fileno()
            name = clients[client_id]["Name"]
            data = client.recv(BUFFER_SIZE)
            data = pickle.loads(data)
            if data[0] == "{quit}":
                broadcast(client, f"\n {name} has left the chat.")
                client.close()
                del clients[client_id]
                connections.remove(client)
                cwd = os.getcwd()
                file_list = [f for f in os.listdir(cwd) if f.startswith(f"{client_id}")]
                for f in file_list:
                    os.remove(os.path.join(cwd, f))
                break
            elif data[0] == "{chs}":
                state = clients[client_id]["Status"]
                if state == "Available":
                    broadcast(client, f"\n {name} is Not Available now")
                    clients[client_id]["Status"] = "Unavailable"
                else:
                    broadcast(client, f"\n {name} is  Available now.")
                    clients[client_id]["Status"] = "Available"
            elif data[0] == "{send}":
                try:
                    receiver_id = int(data[1])
                except ValueError:
                    print("Non integer value")
                    client.sendall(bytes("invalid ID (Not an Integer)", "utf8"))
                else:
                    msg = data[2]
                    if receiver_id not in clients:
                        client.sendall(bytes(" ID Does Not Exist)", "utf8"))
                    else:
                        for i in connections:
                            fd = int(i.fileno())
                            if receiver_id == fd:
                                if clients[receiver_id]["Status"] == "Available":
                                    print("SUCCESS")
                                    if(receiver_id == client_id):
                                        client.sendall(bytes("\n you sent the message to yourself successfully", "utf8"))
                                    else:
                                        client.sendall(bytes("SUCCESS", "utf8"))
                                        msg = clients[client_id]["Name"] + ", " + clients[client_id]["Title"] + ", " + clients[client_id]["Company"] + ": \n" + f"   {msg}"
                                        i.sendall(bytes(msg, "utf8"))
                                        filename = f"{client_id}to{receiver_id}.txt"
                                        with open(filename, "a") as f:
                                            x = strftime("%H:%M", gmtime())
                                            f.write(f"{x} - {msg} \r\n")
                                            f.close()
                                        reverse = f"{receiver_id}to{client_id}.txt"
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


def broadcast(cs_sock, msg):
    """Broadcasts a message to all the clients."""
    for sock in connections:
        if sock != cs_sock:
            sock.sendall(bytes(msg, "utf8"))


clients = {}
connections = set()
HOST = ''
PORT = 33301
BUFFER_SIZE = 1024
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind((HOST, PORT))
if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connections...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()  # Starts the infinite loop.
    ACCEPT_THREAD.join()
    SERVER.close()