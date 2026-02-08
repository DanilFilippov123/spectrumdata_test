from spectrumdata_test.parser.bs4_parser import Bs4Parser
from spectrumdata_test.parser.interface import Parser


def make_parser() -> Parser:
    return Bs4Parser()
