import re
from urllib.parse import unquote
from utils.article import check_article_link
from bs4 import BeautifulSoup

def get_all_articles_links(html_code) : 
    soup = BeautifulSoup(html_code,"lxml")
    extracted_links = soup.find_all('a', href=True)
    if len(extracted_links) != 0 :
        links = []
        for link in  extracted_links: 
            link = check_article_link(link['href'])
            if link : links.append("https://www.justfood.tv"+link)
        return links

def build_decoding_url(url,next_page_number,articles_page_number) : 
    ### decode url 
    url = unquote(url)
    ### replacing vars
    url = url.replace('next_page_number',next_page_number)
    url = url.replace('articles_page_number',articles_page_number)
    return url