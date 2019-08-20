# TCP Multithreaded Chat on python
In this project we’ll create a simple chat program.

## Definitions:
*	Client: Represents a user.
*	Server: Server that handles clients requests.

## Connection:

### Client:

*	To start a new client (create user), Name, Job Title and Company Name should be passed as command line args to client script.
*	Client connect to server.
*	Client sends its above info to server.
*	Client receives and stores its unique ID from server.

### Server:

*	Will keep waiting for new connections as long as it is running.
*	Should handle several clients at the same time.
*	Server accepts new connection.
*	Server create a unique ID for that client equal to FD number of that connection.
*	Server set client status field “Available” as default value.
*	Server stores clients info in a dictionary like: {ID:{Name:”user_name”, Title:”job_title”, Company:”company_name”, Status:”Available”}, ID :…etc}.
*	Server then reply to the client with its unique ID.

Client will provide the following features and take user input to do:
Hint: Server & Client can define a message type to distinguish between “send message”, “change status”, “print history” and “close” messages.

### Chatting:

*   Client types { send } 
*	To send a message, the client provide receiver ID and message body to the server.
*	Server should then redirect message to the receiver ID with full sender info if receiver status is “Available”.
*	Server will also reply with “SUCCESS” to the sender.
*	Sender then prints that message sent successfully.
*	Otherwise, no message is sent to the desired receiver.
*	Server will also reply with “FAIL” to the sender.
*	Sender then prints message failed to deliver message because …
*	When a client receive a message, it should print full sender info with date and message body in a nice format.
*	Sender and receiver clients should store conversation between them locally in a special log file (Open file and append) in a clear format.
*	Note: Client should store conversation in a special log file for each other client it sent/received messages to/from.

### Change Status:

*   Client types { chs }
*	Client can send change status message to server to switch between Available and UnAvailable.

### Print History:

*   Client types { history }
*	Client enters another client ID to view its history.
*	Client read local log file (cookies) related to the given ID if exists, and print messages history in a clear format.
*	Otherwise prints “No History”.

### Close:

*	Client choose to close { quit } by closing the socket.
*	Server should handle close signal coming from client and remove related entry from dictionary.
*	Server then close its socket.

note: be careful to write { send } without the Braces.
