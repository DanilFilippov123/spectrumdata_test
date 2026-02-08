from parser.bs4_parser import Bs4Parser
from parser.interface import Parser


def make_parser() -> Parser:
    return Bs4Parser()
