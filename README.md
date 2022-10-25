# File Sharing System
a project for Computer Networks at BIU written in Python

## Introduction
This project is a file sharing platform.

    Watchdog module to monitor changes in the folder.
    support for multiple diffrent clients.
    support for multiple diffrent sessions within a client.
    
 ### Client-Side
 
#### Connection initialization:
The client is being initialized; a client should provide five arguments:
1. `IP` - server's IP.
2. `PORT` - server's port.
3. `PATH` - path to the synchronized folder.
4. `TIME` - desired interval for an update.
5. `ID` - client's ID

The method `initialize_connection`:
The method will check if a client has provided an ID; if so, the client will send a pull request to the server requesting the files stored on the server.
o.w a new client will be initialized, and the server will send a push request to the server resulting in an upload of the provided folder.

#### Synchronazation with the server:
`update_request` method:
update_request - method is in-charge of notifying a server an update is needed with the current client, happens each `TIME` interval, or is triggered by the watchdog module.

each update consists the following: 
1. `num_updates` the number of updates about to be transmitted.
2. for each update the relative path is provided and full data.

There are several different sanarios:
1. `NEW_FILE` - new file is transmitted from client to server.
2. `NEW_FOLDER` - new folder is transmitted from client to server.
3. `DELETE` - a delete request of a folder or a file is transmitted to the server. 



#### WatchDog Module:
    Python API and shell utilities to monitor file system events.
  The watchdog module monitors the provided folder and notifies the server about a change that occurred in the folder.
  For every change that occured in the folder, the client will notify the server of the difference with the commands defined above.
  
 ### Server-Side
 
 #### Connection initialization:
The server receives a connection from the client and passes the `client-id` provided.
If the ID provided is invalid, the server generates a new client on the cloud and transmits the generated ID back to the client for future connections.
 
 1. `Client-ID` - the ID of the client (as authorization information`
 2. `Session-ID` - the current session of the client.

  #### Synchronazation with the client:
`send_updates` method:
send_updates - If the client requests an update, send all updates according to the client's id and session id.
  The server keeps track of all updates that occur and are transmitted for each session of the current client.
  By receiving the update request, the server transmits only the update relevant to the provided session.
  
  `add_update` method:
  add_update - add the given update to all clients with the corresponding id and all possible session ids
  when receiving a new update, the server adds the update to all sessions to push on future update requests.
  
 
 ##Visual Explanation:
 
 ![image](https://user-images.githubusercontent.com/92247226/192823574-d9183725-7c75-4cf4-8e39-dbb16afb5add.png)

`RED_COLOR`: Auto-Generated ID for the client.
`GREEN_COLOR`: The synchronized folder.
`PURPULE_COLOR`: The server's folder consits of all the clients.


### Auto Push To Server On New Client:
![2022-09-28-18-37-08](https://user-images.githubusercontent.com/92247226/192826430-9b77de9d-864f-4239-8816-48671b6cadf6.gif)


### Auto Pull On Existing Client:
![2022-09-28-18-43-27(1)](https://user-images.githubusercontent.com/92247226/192826129-d96c571f-fe7e-498a-8791-dfbf7e7ad231.gif)

### WatchDog Trigger And Push To Server:
![2022-09-28-18-37-08(1)](https://user-images.githubusercontent.com/92247226/192826614-50e6da4c-cf9c-4ea2-a53e-8d996f3af215.gif)

