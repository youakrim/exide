#!/usr/bin/python
#-*- coding: utf-8 -*-
import os

from .pptx_parser import parse_pptx
from .odp_parser import parse_odp


def parse(file):
    file_extension = os.path.splitext(file)[1]
    if file_extension == ".pptx":
        return parse_pptx(file)
    elif file_extension == ".odp":
        return parse_odp(file)
    else:
        raise Exception("Unsupported file extension")
