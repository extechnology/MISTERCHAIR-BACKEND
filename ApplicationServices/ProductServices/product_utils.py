from bs4 import BeautifulSoup
from django.utils.html import strip_tags

def clean_html_remove_styles(html):
    soup = BeautifulSoup(html, "lxml")

    # Remove style attributes from all tags
    for tag in soup.find_all(True):
        tag.attrs.pop("style", None)

    # OPTIONAL: remove html/body tags
    if soup.body:
        return soup.body.decode_contents()

    return str(soup)