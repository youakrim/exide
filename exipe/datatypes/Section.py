#!/usr/bin/python
#-*- coding: utf-8 -*-

class Section:
	def __init__(self, title):
		self.title = title
		self.subelements = []
		self.level = 0
		self.toc_slide_id = None

	def emphasized_text(self, ):
		pass

	def named_entities(self, ):
		pass

	def text(self, ):
		pass

	def urls(self, ):
		pass

	def slides(self, ):
		pass

	def outline(self, ):
		pass

	def get_slides_of_type(self, type):
		pass

	def get_slides_by_keyword(self, keyword):
		pass

	def get_slides_by_title(self, title):
		pass

