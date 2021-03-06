import cv2
import socket
import win32api, win32con
from collections import deque
from grabscreen import grab_screen

def main():
	serverAddress = ''
	port = 5555
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.bind((serverAddress, port))
	server.listen(1)
	print('Server running...')
	while True:
		connection, address = server.accept()
		coordinates = connection.recv(2048).decode('utf-8').split('-')
		x = round(float(coordinates[0]))
		y = round(float(coordinates[1]))
		img = grab_screen(region=(x, y, x+1279, y+719))
		for i in range(720):
			deque(img[i,0:1279], i)
		connection.sendall(img)
		connection.close()

if __name__ == "__main__":
	main()