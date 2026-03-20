from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        # attrs is a list of (attribute, value)
        for attr, value in attrs:
            print(f"  Attribute -> {attr} = {value}")

        # Example: check if a specific attribute exists
        for attr, value in attrs:
            if attr == "class":
                print("  -> This tag has a class:", value)
        print("Encountered a start tag:", tag)

    def handle_endtag(self, tag):
        print("Encountered an end tag :", tag)

    def handle_data(self, data):
        print("Encountered some data  :", data)

parser = MyHTMLParser()
parser.feed('<html><head><title>Test</title></head>'
            '<body><h1>Parse me!</h1><a href="yoolo"></a></body></html>')