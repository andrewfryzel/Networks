from socket import *
from threading import *
import sys

print 'Server Ready'
#accept input for port number
proxyPort = 80
proxyPort =  int(sys.argv[1])
serverPort = 80

#In order to print out how many clients are connected
count = 0

threads = []
	#https://www.tutorialspoint.com/python/python_multithreading.htm 
 	#https://stackoverflow.com/questions/31851514/how-does-thread-init-self-in-a-class-work
#Start Threading Process
class ThreadingStart(Thread):

  def __init__(self, addr, socket):
    Thread.__init__(self)
    self.addr = addr
    #Use this in place of connectionSocket
    self.socket = socket

  #Apparently this has to be called 'run' (?) cant be called start because of line 194 I'm guessing
  def run(self):
    flag = True
    #print 'Port: ', proxyPort
    print 'addr  1:', addr

    serverAddress = 'localhost'
    host = ''
    URL = ''
    path = ''
    urlTOken = ''
    messageToArray = []

    while flag == True:
      print 'Listening for requests'
      global count
      count = 1 + count
      print 'Connected Clients: ', count
      #self.socket, addr = clientSocket.accept()
      messageFromClient = self.socket.recv(1024)

      #array for messageFromClient
      #split and get the first line of input
      messageToArray = messageFromClient.split("\\r\\n")
      #split into the three parts
      array = messageToArray[0].split()

      #print 'Recieved Sentence:', messageFromClient
      #print 'Recieved Array:', messageToArray
      countLines = messageFromClient.count('\\r\\n')


    #ERROR CHECKING
      if(len(array) == 3):
        print 'Correct Number args'
      else:
        print 'Invalid numbers of args'
        print len(messageToArray), array, len(array)
        self.socket.send('HTTP/1.0 400 Bad Request\n')
        self.socket.close()
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
          print 'Starts with http'
        else:
          self.socket.send('HTTP/1.0 400 Bad Request\n')
          self.socket.close()
          exit()


        #if(httpToken.startswith('HTTP/')):
        if('HTTP' not in httpToken and httpToken.endswith('\\r\\n') == False ):
          print 'fail'
          self.socket.send('HTTP/1.0 400 Bad Request\n')
          self.socket.close()
          exit()

        #Header Checking : <HEADER NAME>: <HEADER VALUE>
        #ignore first line, start with second line for headers
        #check headers for
        #print 'benchmark 2'
        line = 1
        while(line < len(messageToArray) -1):
          #print 'benchmark 1'
          headers = messageToArray[line].split()
          print headers
          if(headers[0].endswith(':') == False):
            self.socket.send('HTTP/1.0 400 Bad Request\n')
            self.socket.close()
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

        #Need to break out of the while loop
        flag = False

      #https://www.w3schools.com/tags/ref_httpmethods.asp all the different http requests
      elif (messageToArray[0].startswith('POST') or messageToArray[0].startswith('PUT') or messageToArray[0].startswith('HEAD') or messageToArray[0].startswith('DELETE') or messageToArray[0].startswith('PATCH') or messageToArray[0].startswith('OPTIONS')):
        self.socket.send('HTTP/1.0 501 Not Implemented\n')
        self.socket.close()
        exit()

      else:
        self.socket.send('HTTP/1.0 400 Bad Request\n')
        self.socket.close()
        exit()

    #print 'benchmark 3'
    #print 'host', host

    #In PA1-A this was in the while loop, just moved it down here

    #Setup the return output socket
    returnSocket = socket(AF_INET,SOCK_STREAM)
    returnSocket.connect((host, 80))

    #Get the request and the extra \r\n added to the end
    request = 'GET ' + path + ' HTTP/1.0\r\n'
    request = request + '\r\n'

    #Decrement counter when process is done

    count = count - 1

    #Send the message out
    returnSocket.send(request)
    response = returnSocket.recv(1024)

    #Send the message in
    self.socket.send(response)
    print response

    self.socket.close()
    returnSocket.close()

proxyPort =  int(sys.argv[1])

clientSocket = socket(AF_INET,SOCK_STREAM)

clientSocket.bind(('',proxyPort))

#Sticking this in a while loop solved the issue of not getting new threads
#https://stackoverflow.com/questions/27609866/while-loop-not-continuing-after-starting-a-new-thread-python
while 1:
  clientSocket.listen(1)

  (connectionSocket, addr) = clientSocket.accept()
  print 'add 2', addr

  newThread = ThreadingStart(addr, connectionSocket)
  newThread.start()
  threads.append(newThread)

#End process
clientSocket.close()

#Not sure if Join is necessary but its works
#https://stackoverflow.com/questions/21486105/when-why-and-how-to-call-thread-join-in-python
#https://stackoverflow.com/questions/15085348/what-is-the-use-of-join-in-python-threading
for thr in threads:
  thr.join()
exit(0)


#Sources: *Select is better for performance and sockets*
#https://pymotw.com/2/select/
#https://stackoverflow.com/questions/36636982/i-need-advice-should-i-use-select-or-threading
#https://stackoverflow.com/questions/51104534/python-socket-receive-send-multi-threading
#https://stackoverflow.com/questions/32784206/socket-python-select-and-multiprocessing
#https://stackoverflow.com/questions/47234464/socket-programming-in-python-error-group-argument-must-be-none-for-now-and-s
#https://stackoverflow.com/questions/15958026/getting-errno-9-bad-file-descriptor-in-python-socket
#https://stackoverflow.com/questions/38292142/python-socket-error-errno-9-bad-file-descriptor
#https://dzone.com/articles/python-thread-part-1  

#Complete
