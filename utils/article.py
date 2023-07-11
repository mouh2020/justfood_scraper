from bs4 import BeautifulSoup
import re

def check_article_link(link) : 
    pattern = r"/.*/(\d+)/.*"
    match = re.match(pattern, link)
    if match:
        number = match.group(1)
        return link
def get_article_body(article_html_code) : 
    soup = BeautifulSoup(article_html_code,"lxml")
    return str(soup.find('div',attrs={'class':'article-body'})).rjust(0)

def get_article_id(link : str) : 
    return link.split('/')[-2]

def clean_article(article_html_code : str) : 
    return article_html_code.replace('\r','').replace('\n','').replace('\t','')

def add_image_link_to_article(article_html_code :str ) : 
    return
