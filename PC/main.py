import cv2
import socket
import win32api, win32con
from collections import deque
from grabscreen import grab_screen
from threading import *

def main():
	serverAddress = '80.221.148.147'
	port = 5555
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.bind((serverAddress, port))
	server.listen(1)
	print('Server running...')
	while True:
		connection, address = server.accept()
		request = connection.recv(2048).decode('utf-8')
		if len(request.split('-')) == 2:
			coordinates = request.split('-')
			x = round(float(coordinates[0]))
			y = round(float(coordinates[1]))
			img = grab_screen(region=(x, y, x+1279, y+719))
			for i in range(720):
				deque(img[i,0:1279], i)
			connection.sendall(img)
		else:
			clickPoint = request.split('_')
			x = round(float(clickPoint[0]))
			y = round(float(clickPoint[1]))
			win32api.SetCursorPos((x,y))
			win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
			win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
		connection.close()

if __name__ == "__main__":
	main()