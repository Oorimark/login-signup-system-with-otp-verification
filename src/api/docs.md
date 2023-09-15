DOC SCRAPES

Client login route: Login route
Description: The client login route takes the following processes 1. Validates the client send request (decorator) 2. Validates the credentials are sent by client (decorator) 3. Check if password for the username (email) exist (function scope) 4. Send a session token and the user id so the client can access (function scope)

CHATTING LOGIC
Client can chat with each other but not in a peer-to-peer connection type. Messages are first sent to the database and the client does to that collection to receive the message. A sender sends a message by sending his id, receiver's id and the message

```json
{
  "sender_id": "string",
  "receiver_id": "string",
  "message": "string"
}
```

After this is sent through the client-messaging-route, the data is then saved to the collection.

### Client Receiving Message

A client receive a message by first sending details such sender's id, receiver's id, and number of existing message.

```json
{
  "sender_id": "string",
  "receiver_id": "string",
  "no_of_existing_messages": "number"
}
```

The sender's id and the receiver's id are not sensitive data as either could be sent as another. The numbers of existing message helps the server to know the number of messages the client as already so it would send the messages that are not available.
