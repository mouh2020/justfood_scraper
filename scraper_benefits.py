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
    time.sleep(1.5)
    try :
        for j in range(1,500) :
            url_to_scrape = build_decoding_url(url=recipes_url,
                                            next_page_number=str(i),
                                            articles_page_number=str(j))
            logger.info(f'url_to_scrape : {url_to_scrape}')
            page_html_code = make_request(url=url_to_scrape)
            if page_html_code == None : 
                continue
            articles_links = get_all_articles_links(html_code=page_html_code)
            if articles_links == None or len(articles_links) < 7: 
                break
            logger.info(f'articles_links_number : {len(articles_links)}')
            for article_link in articles_links : 
                ##### Process article.
                article_id = int(get_article_id(link=article_link))
                database_session = Session(engine)
                fetched_article =database_session.exec(select(Article).where(Article.article_id==article_id)).first()
                if fetched_article : 
                    logger.info(f'found duplicate article : {str(article_id)}')
                    continue
                logger.info(f'fetch article_id  : {str(article_id)}')
                article_html_code = make_request(url=article_link)
                #print(article_html_code)
                article_body_html = get_article_body(article_html_code=article_html_code)
                article = clean_article(str(article_body_html))
                #### Add images
                #article = add_image_link_to_article(article)
                ##### Process article title.
                title = get_title(article_html_code=article_html_code)
                title = clean_title(title=title)
                #### Check if article exists.
                #### Insert article.
                logger.info(f'article title  : {str(article_id)}')
                article_to_insert = Article(
                    article_id=article_id,
                    title=title,
                    article_text=article_body_html.text,
                    article_html=str(article)
                )
                database_session.add(article_to_insert)
                database_session.commit()
                time.sleep(1.5)
    except Exception as e : 
        logger.error(f'error occured : {str(e)}')




        
        
        
        
        