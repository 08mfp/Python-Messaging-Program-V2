"""
serverInit.py- 
"""


import threading
import time
import socket as socketlib


class Socket():
	"""
	Mutable wrapper class for sockets.
	"""

	def __init__(self, socket):
		self._socket = socket
	
	def send(self, msg):
		self._socket.send(msg.strip()+b"\n")
		
	def close(self):
		self._socket.close()
		

class Receiver():
	"""
	A class for receiving newline delimited text commands on a socket.
	"""

	def __init__(self):
		self._lock = threading.RLock()
		self._running = True

	def __call__(self, socket):
		"""Called for a connection."""
		socket.settimeout(1)
		wrappedSocket = Socket(socket)
		stored = ''
		chunk = ''
		
		self._lock.acquire()
		self.onConnect(wrappedSocket)
		self._lock.release()
		
		while self.isRunning():
			(message, sep, rest) = stored.partition('\n')
			if sep == '': 
				while self.isRunning():
					try:
						chunk = ''
						chunk = socket.recv(1024).decode() 
						stored += chunk
						break
					except socketlib.timeout:
						pass
					except:
						print('EXCEPTION')
				if chunk == '':
					break;
				continue
			else: 
				stored = rest			
			self._lock.acquire()
			success = self.onMessage(wrappedSocket, message)
			self._lock.release()
			if not success:
				break;
		self._lock.acquire()
		self.onDisconnect(wrappedSocket)		
		self._lock.release()
		socket.close()
		del socket
		self.onJoin()

	def stop(self):
		"""Stop this receiver."""
		self._lock.acquire()
		self._running = False
		self._lock.release()
		
	def isRunning(self):
		"""Is this receiver still running?"""
		self._lock.acquire()
		running = self._running
		self._lock.release()
		return running
		
	def onConnect(self, socket):
		pass

	def onMessage(self, socket, message):
		pass

	def onDisconnect(self, socket):
		pass

	def onJoin(self):
		pass

		
		
class Server(Receiver):

	def start(self, ip, port):
		serversocket = socketlib.socket(socketlib.AF_INET, socketlib.SOCK_STREAM)
		serversocket.setsockopt(socketlib.SOL_SOCKET, socketlib.SO_REUSEADDR, 1)
		serversocket.bind((ip, int(port)))
		serversocket.listen(10)
		serversocket.settimeout(1)
		self.onStart()
		threads = []
		while self.isRunning():
			try:
				(socket, address) = serversocket.accept()								
				thread = threading.Thread(target = self, args = (socket,))
				threads.append(thread)
				thread.start()
			except socketlib.timeout:
				pass
			except:		
				self.stop()
		while len(threads):
			threads.pop().join()
		self.onStop()

	def onStart(self):
		pass

	def onStop(self):
		pass



class Client(Receiver):
	
	def start(self, ip, port):

		self._socket = socketlib.socket(socketlib.AF_INET, socketlib.SOCK_STREAM)
		self._socket.settimeout(1)
		self._socket.connect((ip, int(port)))

		self.onStart()

		self._thread = threading.Thread(target = self, args = (self._socket,))
		self._thread.start()
		
	def send(self, message):
		self._lock.acquire()
		self._socket.send(message.strip()+b'\n')
		self._lock.release()
		time.sleep(0.5)

	def stop(self):
		Receiver.stop(self)
		
		if self._thread != threading.currentThread():
			self._thread.join()
		self.onStop()		

	def onStart(self):
		pass

	def onStop(self):
		pass
		
	def onJoin(self):
		self.stop()
