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
from threading import _start_new_thread

Config.set('graphics','resizable',0)
kv = Builder.load_file('kv.kv')

class VideoStream(Screen):
	img_src = StringProperty('')

	def __init__(self, **kwargs):
		super(VideoStream, self).__init__(**kwargs)
		self.imgX = 0
		self.imgY = 0
		Clock.schedule_interval(self.fetchScreen, 0.1)

	def fetchScreen(self, dt):
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		serverAddress = '80.221.148.147'
		port = 5555
		address = (serverAddress, port)
		self.server.connect(address)
		self.server.send(str.encode(str(self.imgX)+'-'+str(self.imgY)))
		image_data = b''
		while True:
			data = self.server.recv(20480)
			if not data:
				break
			else:
				image_data += data
		image = Image.frombytes('RGB', (1280,720), image_data)
		image.save(os.path.dirname(os.path.realpath(__file__))+'/images/screencapture.jpg')
		self.img_src = os.path.dirname(os.path.realpath(__file__))+'/images/screencapture.jpg'
		self.ids.image_source.reload()

	def on_touch_down(self, touch):
		self.movementX = touch.pos[0]
		self.movementY = touch.pos[1]

	def on_touch_move(self, touch):
		newX = self.imgX + self.movementX - touch.pos[0]
		newY = self.imgY + self.movementY - touch.pos[1]
		if 0 <= newX:
			self.imgX = newX
		if 0 <= newY:
			self.imgY = newY
		
	def on_touch_up(self, touch):
		if self.movementX == touch.pos[0] and self.movementY == touch.pos[1]:
			_start_new_thread(self.server.send, (str.encode(str(self.imgX + touch.pos[0])+'_'+str(self.imgY + touch.pos[1])),))

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