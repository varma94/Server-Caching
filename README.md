Server Caching

Created a multithreaded web proxy server that supports GET method and implements caching.

Project Tasks:
•	Create a ServerSocket object to monitor the port 8080 or other ports from input;
•	If receive client request, create a new thread to process the request. Also a new socket is
•	created for the connection with client;
• The ServerSocket object continues monitoring;
• Parse the request line and headers sent by the client.
• If the new request matches a past one, the proxy server will directly return the cached data.
• Send request to “real” Web server. A HTTP response including the requested file will be
•	Received at the proxy server.
• The thread reads in the instream, get the file name and the content;
•	Forward the content to the Client.
• Close the socket, and end the thread.

Technology : Python
