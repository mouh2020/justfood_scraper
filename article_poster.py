import requests,time, base64 
from database import engine,Article
from sqlalchemy import Column
from sqlmodel import Session,select
from config import *
from utils.article import add_image_link_to_article,remove_links_from_article
from loguru import logger

logger.add("justfood_scraper.log",format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {function} | {message}",colorize=False,enqueue=True,mode="w")

def post_article(article : Article,type="draft") : # change from "draft" to "publish" when you finish testing.
    credentials = f'{wp_username}:{wp_password}'
    token = base64.b64encode(credentials.encode())
    headers = {"Authorization": "Basic " + token.decode('utf-8'), "Content-Type":"application/json"}
    wp_post_endpoint = wp_url+"/wp-json/wp/v2/posts"
    post = {
        'title' : article.title,
        'status' : type,
        'content': remove_links_from_article(add_image_link_to_article(article.article_html))
    }
    try :
        response =  requests.post(wp_post_endpoint,
                                json=post,
                                headers=headers)
        if response.status_code == 201 or response.status_code == 200 : 
            return True
    except Exception as e : 
        logger.error(f'error occured : {str(e)}')

database_session = Session(engine)
articles_number = len(database_session.exec(select(Article).where(Article.is_posted==False)).all())
database_session.close()
# (186٬684) 
while True : 
    database_session = Session(engine)
    article = database_session.exec(select(Article).where(Article.is_posted == False)).first()
    if article == None : 
        break
    if post_article(article=article,type="publish") : 
        articles_number-=1
        logger.info(f'left articles : {articles_number}')
        article.is_posted = True
        database_session.add(article)
        database_session.commit()
    database_session.close()
    






