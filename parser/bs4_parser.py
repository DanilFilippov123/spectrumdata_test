from urllib.parse import urlparse, urljoin

from bs4 import BeautifulSoup

from parser.interface import Parser, ParserResult


class Bs4Parser(Parser):
    def parse(self, content: str, base_url: str) -> ParserResult:
        soup = BeautifulSoup(content, "html.parser")
        title = soup.title.string

        body = soup.find("body")
        links = body.find_all("a", href=True)
        new_urls = []

        for link in links:
            href = link.get("href")
            if href is None:
                continue
            absolute_url = href if urlparse(href).scheme else urljoin(base_url, href)
            if absolute_url.startswith("http"):
                new_urls.append(absolute_url)

        return ParserResult(title=title, body=str(body), urls=new_urls)
