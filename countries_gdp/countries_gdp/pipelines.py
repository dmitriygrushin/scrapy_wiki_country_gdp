# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

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
