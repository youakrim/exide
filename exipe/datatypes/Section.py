#!/usr/bin/python
#-*- coding: utf-8 -*-


class Section:
	def __init__(self, title):
		self.subelements = []
		self.title = title

	def get_emphasized_text(self):
		pass

	def get_named_entities(self, ):
		pass

	@property
	def text(self, ):
		text = ""
		for element in self.subelements:
			text+=element.text
		return text

	def get_slides_of_type(self, ):
		pass

	def get_urls(self, ):
		pass

	def get_slides(self, ):
		pass

