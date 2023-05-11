import xml.sax
from typing import Optional


class WikiReader(xml.sax.ContentHandler):
    def __init__(self, ns_filter, callback):
        super().__init__()

        self.tag_stack: list[str] = []
        self.filter = ns_filter
        self.callback = callback

        self.page_title: Optional[str] = None
        self.page_text: Optional[str] = None
        self.namespace: Optional[int] = None  # Parses only when this = 0 (en.wikipedia.org/wiki/Wikipedia:Namespace)
        self.real_article_processed = 0
        self.total_article_processed = 0

    # Called when the XML Reader is starting a new tag
    def startElement(self, name, attrs):
        if name == "ns":
            self.namespace = None

        elif name == "page":
            self.page_text = None
            self.page_title = None

        elif name == "title":
            self.page_title = ""

        elif name == "text":
            self.page_text = ""

        self.tag_stack.append(name)

    # Called when the XML Reader has finished reading the content of a tag
    def endElement(self, name):
        if name == self.tag_stack[-1]:
            self.tag_stack.pop()

        if self.filter(self.namespace):  # is article
            if name == "page":
                if self.page_text is not None:
                    self.real_article_processed += 1
                    self.callback((self.page_title, self.page_text))
                self.total_article_processed += 1
        elif name == "page":
            self.total_article_processed += 1

    # Called with the content of a tag (no xml)
    def characters(self, content):
        if len(self.tag_stack) == 0:
            return

        if self.tag_stack[-1] == "text":
            self.page_text += content

        if self.tag_stack[-1] == "title":
            self.page_title += content

        if self.tag_stack[-1] == "ns":
            self.namespace = int(content)
