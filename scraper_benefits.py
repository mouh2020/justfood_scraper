from utils.article import * 
from utils.title import *
from utils.base import *
from database import create_db_and_tables,engine,Article
from loguru import logger
from utils.process_requests import make_request
from sqlmodel import Session,select
import time
logger.add("justfood_scraper.log",format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {function} | {message}",colorize=False,enqueue=True,mode="w")

create_db_and_tables()
recipes_url ="https://www.justfood.tv/الفئة/معجنات/بيتزا/next_page_number/articles_page_number"

for i in range(1,500) : 
    try :
        time.sleep(1.5)
        url_to_scrape = build_decoding_url(url=recipes_url,
                                                    next_page_number=str(i),
                                                    articles_page_number="1")
        logger.info(f'scrap first page url : {url_to_scrape}')
        page_html_code = make_request(url=url_to_scrape)
        if page_html_code == None : 
            continue
        article_pages_number = get_article_pages_number(page_html_code)
        logger.info(f'article pages number : {str(article_pages_number)}')
        if article_pages_number == None : 
            continue
        for j in range(1,article_pages_number+1) : 
            articles_links = get_all_articles_links(html_code=page_html_code)
            if articles_links == None :  
                continue
            for article_link in articles_links : 
                article_id = int(get_article_id(link=article_link))
                database_session = Session(engine)
                fetched_article =database_session.exec(select(Article).where(Article.article_id==article_id)).first()
                if fetched_article : 
                    continue
                logger.info(f'fetch article_id  : {str(article_id)}')
                article_html_code = make_request(url=article_link)
                article_body_html = get_article_body(article_html_code=article_html_code)
                article = clean_article(str(article_body_html))
                title = get_title(article_html_code=article_html_code)
                title = clean_title(title=title)
                logger.info(f'article title  : {str(title)}')
                article_to_insert = Article(
                    article_id=article_id,
                    title=title,
                    article_text=article_body_html.text,
                    article_html=str(article)
                )
                database_session.add(article_to_insert)
                database_session.commit()
                database_session.close()
                time.sleep(1.5)
                url_to_scrape = build_decoding_url(url=recipes_url,
                                                next_page_number=str(i),
                                                articles_page_number=str(j))
                page_html_code = make_request(url=url_to_scrape)
    except Exception as e : 
        logger.error(f'error occured : {str(e)}')




        
        
        
        
        