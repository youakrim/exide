import re

def namespace(element):
    """
    Return the XML namespace string of the given element.

    :param element: LXML object
    :return: String
    """
    m = re.match('\{.*\}', element.tag)
    return m.group(0) if m else ''