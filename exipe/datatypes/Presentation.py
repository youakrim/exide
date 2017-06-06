#!/usr/bin/python
# -*- coding: utf-8 -*-
import jsonpickle, json

class Presentation:
    def __init__(self, section):
        self.root_section = section
        self.metadata = None

    def get_slide_by_id(self, id):
        pass

    def export_to_json(self, ):
        return json.dumps(json.loads(jsonpickle.encode(self)), indent=4)
