# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import sqlite3

""" Why is a Pipeline?
Pipeline: Python class that implements a method process_item, 
    it takes the "item" that comes out of the "loading process" as input
    returns an item, (un-modded), (modded), (checks, modded), (checks, item should NOT process further)
    
    There is a catch:
        once you define/modify/introduce a new pipeline you have to make sure 
            it's configured in the settings to be running correctly
        1. uncomment it from settings
        2. as you introduce other custom pipelines you define a new class here, but for it to be integrated 
            with the spider you need to add it in the item pipeline by adding it in settings.py
            
    ITEM_PIPELINES = {
        
        # name, order in which the pipeline with run, so customPipeline will run first in this case
        # 0 - 1000 is the range for the order # i.e. the 200, 300 below
        "countries_gdp.pipelines.CountriesGdpPipeline": 300,
        # "customPipline": 200,
    }
"""


class CountriesGdpPipeline:
    def process_item(self, item, spider):
        if not isinstance(item["gdp"], float):
            # item will NOT be processed further
            raise DropItem("Missing GDP value. Item excluded. ")  # scrapy specific exception

        return item


class SaveToDatabasePipeline:
    # This will export a sqlite db that you can access it. I used DBeaver to access it
    def __init__(self):
        # if you would like to use a cloud db you'd have to make changes here in the initialization stages
        self.con = sqlite3.connect("countries_gdp.db")  # SQLite: connect-to-db if sql-db-exists else create-db
        self.cur = self.con.cursor()  # pointer to the db that allows you to run queries

    def open_spider(self, spider):
        # called when the spider is open which is when the spider starts scraping
        # make sure the table exists/created here, so you don't have to check in the methods i.e. process_item
        # SQL query to create a table
        self.cur.execute("""CREATE TABLE IF NOT EXISTS countries_gdp 
        (country_name TEXT PRIMARY KEY,
        region TEXT,
        gdp REAL,
        year INTEGER)""")

        self.con.commit()

    def process_item(self, item, spider):
        # to help prevent sql injection attacks it's better to NOT set the VALUES manually
        self.con.execute("""INSERT INTO countries_gdp (country_name, region, gdp, year) 
                            VALUES (?, ?, ?, ?)""",
                     (item["country_name"], item["region"], item["gdp"], item["year"]))
        self.con.commit()

    def close_spider(self):
        # after the scraping is done close the connection
        self.con.close()
