import xml.sax
from typing import Optional


class WikiReader(xml.sax.ContentHandler):
    def __init__(self, ns_filter, callback):
        super().__init__()

        self.tag_stack: list[str] = []
        self.filter = ns_filter
        self.callback = callback

        self.redirect_title = None
        self.page_title: Optional[str] = None
        self.page_text: Optional[str] = None
        self.namespace: Optional[int] = None  # Parses only when this = 0 (en.wikipedia.org/wiki/Wikipedia:Namespace)
        self.real_article_processed = 0
        self.total_article_processed = 0

        self.redirect_content = ""

    # Called when the XML Reader is starting a new tag
    def startElement(self, name, attrs):
        if name == "ns":
            self.namespace = None

        if name == "redirect":
            self.redirect_title = attrs['title']

        elif name == "page":
            self.page_text = None
            self.page_title = None
            self.redirect_title = None

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
                if self.redirect_title is None:
                    if self.page_text is not None:
                        self.real_article_processed += 1
                        self.callback((self.page_title, self.page_text, False))
                    self.total_article_processed += 1
                else:
                    # TODO: redirect queue
                    self.total_article_processed += 1
                    self.callback((self.page_title, self.redirect_title, True))
                    pass
        elif name == "page":
            self.total_article_processed += 1

    # Called with the content of a tag (no xml)
    def characters(self, content):
        if len(self.tag_stack) == 0:
            return

        elif self.tag_stack[-1] == "text":
            self.page_text += content

        elif self.tag_stack[-1] == "title":
            self.page_title += content

        elif self.tag_stack[-1] == "ns":
            self.namespace = int(content)
