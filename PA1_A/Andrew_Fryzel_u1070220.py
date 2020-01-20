from socket import *
import sys

#accept input for port number
proxyPort = 80
proxyPort =  int(sys.argv[1])
serverPort = 80

print 'Port: ', proxyPort

serverAddress = 'localhost'
host = ''
URL = ''
path = ''
messageToArray = []
messageFromClient = ''

#set up sockets
#serverSocket = socket(AF_INET,SOCK_STREAM)
returnSocket = socket(AF_INET,SOCK_STREAM)

clientSocket = socket(AF_INET,SOCK_STREAM)
clientSocket.setsockopt(SOL_SOCKET,SO_REUSEADDR, 1)

#serverAddress = 'localhost'
#print 'Host: ', host
#print 'Port: ', proxyPort
#cant bind to lower than 1024: https://stackoverflow.com/questions/24001147/python-bind-socket-error-errno-13-permission-denied
clientSocket.bind((host,proxyPort))
print 'Bound to:', clientSocket.getsockname()
#print 'bind: ', clientSocket.getsockname()

clientSocket.listen(1)

while 1:
	print 'Listening for requests'
	connectionSocket, addr = clientSocket.accept()
	print 'Accepted connection'
	messageFromClient = connectionSocket.recv(1024)

	#array for messageFromClient
	#split and get the first line of input
	messageToArray = messageFromClient.split("\\r\\n")
	print 'Got message' 
	#split into the three parts
	array = messageToArray[0].split()

	#print 'Recieved Sentence:', messageFromClient
	#print 'Recieved Array:', messageToArray
	countLines = messageFromClient.count('\\r\\n')


#ERROR CHECKING
	if(len(array) != 3):
		#print 'Invalid numbers of args'
		#print len(messageToArray), array, len(array)
		connectionSocket.send('HTTP/1.0 400 Bad Request\n')
		connectionSocket.close()
		exit()

#https://www.tutorialspoint.com/python/string_startswith.htm
#GET check, if it starts with anything but GET return error
	if messageToArray[0].startswith('GET'):
		splitArray = messageToArray[0].split()
		#print 'SPlit Array:', splitArray[0]
		#print 'SPlit Array:', splitArray[1]
		#print 'SPlit Array:', splitArray[2]
		getToken = splitArray[0]
		urlToken = splitArray[1]
		httpToken = splitArray[2]
		#print 'getToken', getToken
		#print 'urlToke', urlToken
		#print 'httpToken', httpToken
#TODO
		#check for Absolute URI https://tools.ietf.org/html/rfc1945
		if(urlToken.startswith('http://') or urlToken.startswith('HTTP://')):
			#Have to have this here because i dont understand python / how to negate "startswith" functions
			print ''
		else:
			connectionSocket.send('HTTP/1.0 400 Bad Request\n')
			connectionSocket.close()
			exit()


		#if(httpToken.startswith('HTTP/')):
		if('HTTP' not in httpToken and httpToken.endswith('\\r\\n') == False ):
			#print 'fail'
			connectionSocket.send('HTTP/1.0 400 Bad Request\n')
			connectionSocket.close()
			exit()

		#Header Checking : <HEADER NAME>: <HEADER VALUE>
		#ignore first line, start with second line for headers
		#check headers for
		#print 'benchmark 2'
		line = 1
		while(line < len(messageToArray) -1):
			#print 'benchmark 1'
			headers = messageToArray[line].split()
			#print headers
			if(headers[0].endswith(':') == False):
				connectionSocket.send('HTTP/1.0 400 Bad Request\n')
				connectionSocket.close()
				exit()
			#i++
			i = 1+i

		#Parse the URL to remove the http and stuff
		#https://www.geeksforgeeks.org/python-string-replace/
		if('http://' in urlToken):
			host = urlToken.replace('http://', '')
		else:
			host = urlToken;


		#remove the extensions to get the base uri
		#since we remove the http:// the only / will be after the base address
		startingPoint = 0
		if('/' in host):
			#search from beginning of string to find the /
			#https://www.w3schools.com/python/ref_string_find.asp
			endindPoint = host.find('/', startingPoint)
			#get the path
			path = host[endindPoint:len(host)]
			#clip it, get just the host addr
			host = host[startingPoint:endindPoint]
			#print 'this is the host ',host
		else:
			host = host[startingPoint:len(urlToken)]
			#print 'this is the direct host ',host
	#https://www.w3schools.com/tags/ref_httpmethods.asp all the different http requests
	elif (messageToArray[0].startswith('POST') or messageToArray[0].startswith('PUT') or messageToArray[0].startswith('HEAD') or messageToArray[0].startswith('DELETE') or messageToArray[0].startswith('PATCH') or messageToArray[0].startswith('OPTIONS')):
		connectionSocket.send('HTTP/1.0 501 Not Implemented\n')
		connectionSocket.close()
		exit()

	else:
		connectionSocket.send('HTTP/1.0 400 Bad Request\n')
		connectionSocket.close()
		exit()
	#print 'benchmark 3'
	#print 'host', host
	#print 'url', urlToken

	returnSocket.connect((host, 80))
	request = 'GET ' + path + ' HTTP/1.0\r\n'

	request = request + '\r\n'
	#print 'URL' , URL
	#returnSocket.send(messageFromClient)
	returnSocket.send(request)
	response = returnSocket.recv(1024)

	print response

	connectionSocket.close()
	returnSocket.close()
	clientSocket.close()
	exit()
