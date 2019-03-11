import os
import pygame
import socket
from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from PIL import Image
from threading import *

Config.set('graphics','resizable',0)
kv = Builder.load_file('kv.kv')

class VideoStream(Screen):
	img_src = StringProperty('')

	def __init__(self, **kwargs):
		super(VideoStream, self).__init__(**kwargs)
		self.x = 0
		self.y = 0
		Clock.schedule_interval(self.fetchScreen, 0.1)

	def fetchScreen(self, dt):
		server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		serverAddress = '80.221.148.147'
		port = 5555
		address = (serverAddress, port)
		server.connect(address)
		server.send(str.encode(str(self.x)+'-'+str(self.y)))
		image_data = b''
		while True:
			data = server.recv(20480)
			if not data:
				break
			else:
				image_data += data
		image = Image.frombytes('RGB', (1280,720), image_data)
		image.save(os.path.dirname(os.path.realpath(__file__))+'/imagedata/screencapture.jpg')
		self.img_src = os.path.dirname(os.path.realpath(__file__))+'/imagedata/screencapture.jpg'
		self.ids.image_source.reload()

class Application(App):
	def build(self):
		return VideoStream()

def send(self, data):
	try:
		client.send(str.encode(data))
		return client.recv(2048).decode()
	except socket.error as e:
		print(e)

if __name__ == "__main__":
	Application().run()