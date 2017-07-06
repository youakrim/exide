#!/usr/bin/python
# -*- coding: utf-8 -*-
import jsonpickle, json


class Presentation:
    """
    A |Presentation| object has the following attributes :
        - root_section (Section): Root of the elements (Slides and Sections) tree of the Presentation
        - initial_format (String): gives the file format of the original file.
        - title (String) : title of the presentation
        - author (String): name of the author of the presentation
        - category (String) : category of the presentation if filled
        - comments (String) : comments of the presentation if filled
        - keyword (list of strings) : keyword of the presentation if filled
        - language (string): language of the presentation if filled
        - created (string) : date of creation if filled
        - last_modified (string): date of the last modification
        - subject (string) : subject of the presentation if filled
    """
    def __init__(self, section=None):
        self.root_section = section
        self.initial_format = ""
        self.title = ""
        self.author = ""
        self.category = ""
        self.comments = ""
        self.keywords = ""
        self.language = ""
        self.created = ""
        self.last_modified = ""
        self.subject = ""

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

    def export_to_JSON(self):
        """
        Serialize the presentation to a JSON string.

        :return: str. -- JSON string
        """
        return json.dumps(json.loads(jsonpickle.encode(self)), indent=4)

    @property
    def outline(self):
        """
        Return a string of several lines giving the outline of the presentation

        :return:
        """
        if self.root_section is not None:
            return self.root_section.outline
        return ""
