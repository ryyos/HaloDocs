import os

from time import time, sleep
from datetime import datetime
from requests import Response
from pyquery import PyQuery
from APIRetrys import ApiRetry
from icecream import ic

from src.utils.parser import Parser
from src.utils.fileIO import File
from src.utils.corrector import vname
from src.utils.logs import logger

class HaloDocs:
    def __init__(self) -> None:

        self.__DOMAIN = 'www.halodoc.com'

        self.__API = 'https://magneto.api.halodoc.com/api/cms/categories?per_page=100&search_text='
        self.__ARTICLE_API = 'https://www.halodoc.com/kesehatan/bab-berdarah'
        self.__CHAR = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

        self.__request = ApiRetry(show_logs=False)
        self.__parser = Parser()
        self.__file = File()
        


    def extract_data(self, categories: str) -> dict:
        article = {
            ""
        }
        

    def main(self):

        for char in self.__CHAR:
            response: Response = self.__request.get(url=self.__API+char)
            ic(response)
            for content in response.json()["result"]:

                results = {
                    "domain": self.__DOMAIN,
                    "crawling_time_now": str(datetime.now),
                    "crawling_time_epoch": int(time()),
                    "update": content["updated_at"],
                    "created": content["created_at"],
                    "status": content["status"],
                    "author": {
                        "name": content["author"]["name"],
                        "designation": content["author"]["entity_type"],
                        "id": content["author"]["entity_id"]
                    },
                    "char": char,
                    "keyword": content["meta_keywords"],
                    "title": content["meta_title"],
                    "descriptions": content["meta_description"],
                    "slogan": content["slug"],
                    "source": content["source"],
                    "type": content["type"],
                    "attributes": {
                        "image_url": content["attributes"]["image_url"],
                        "thumbnail_url": content["attributes"]["thumbnail_url"],
                        "text": content["attributes"]["alt_text"]
                    },
                    "articles": self.extract_data(categories=content["slug"])
                }

                self.__file.write_json(path='private/results.json', content=results)

                ic('completed')                
                sleep(10)

