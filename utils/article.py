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
    return soup.find('div',attrs={'class':'article-body'})

def get_article_id(link : str) : 
    return link.split('/')[-2]

def clean_article(article_html_code : str) : 
    return article_html_code.replace('\r','').replace('\n','').replace('\t','')

def add_image_link_to_article(article_html_code :str ) : 
    soup = BeautifulSoup(article_html_code,"lxml")
    images = soup.findAll('img')
    for image in images :
        if "/UserFiles" in str(image) :
            del image["src"]
    return str(soup)

def remove_links_from_article(article_html_code :str) : 
    soup = BeautifulSoup(article_html_code,"lxml")
    for a in soup.findAll('a'):
        del a['href']
    return str(soup)
