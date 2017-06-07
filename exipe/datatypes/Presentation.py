#!/usr/bin/python
# -*- coding: utf-8 -*-
import jsonpickle, json


class Presentation:
    def __init__(self, section=None):
        self.root_section = section
        self.metadata = None

    def get_slide_by_id(self, id):
        '''
        The ID of a slide corresponds to its page number. The first slide of a presentation will have 1 as its ID.
        :param id: slide number
        :return: Slide -- if no slide matches the given id, None is returned
        '''
        for slide in self.root_section.slides:
            if slide.id == id:
                return slide
        return None

    def export_to_json(self):
        """
        Serialize the presentation to a JSON string.
        :return: str. -- JSON string
        """
        return json.dumps(json.loads(jsonpickle.encode(self)), indent=4)

    @property
    def outline(self):
        if self.root_section is not None:
            return self.root_section.outline
        return ""
