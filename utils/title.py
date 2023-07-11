from bs4 import BeautifulSoup

def get_title(article_html_code) :
    soup = BeautifulSoup(article_html_code,"lxml")
    return soup.title.text

def clean_title(title : str) : 
    return title.replace(' | Just Food','').strip()