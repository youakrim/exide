import unittest,os

from exide.pptx_parser import parse_pptx


class pptx_parser_test(unittest.TestCase):
    def test_body_text_extraction(self):
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))+"/data/"
        pres = parse_pptx(os.path.join(__location__, "presentation-test.pptx"))
        self.assertEqual(pres.root_section.text, "")


if __name__ == '__main__':
    unittest.main()
