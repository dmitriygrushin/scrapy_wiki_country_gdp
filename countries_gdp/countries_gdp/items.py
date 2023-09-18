# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

"""What are items? Why do you need them? You can go without them, so why are they useful?

Useful:
    * Introducing structured data - fields you want to extract from a web page
    * When defining a scrapy item class you're declaring a schema for the data you want to extract
        - Easier to store in DB, or integrate in Django

"""

import scrapy
from itemloaders.processors import TakeFirst, MapCompose
from w3lib.html import remove_tags
""" Definitions:

Processors:
    TakeFirst: extract the 1st val from a list of vals
    MapCompose: 
            * Apply a list of funcs to a val. A way to chain funcs together in a single step.
            * Define a pipeline of processing steps that will be applied to each field in the item 
                as the val is extracted from the selector and loaded on to the item
Item vs ItemLoader:
    Item: structure
    ItemLoader: process of loading data into the item 
    
w3lib.html.remove_tags: 
    <a>some text</a> -> "some text"
    
"""

"""

"""
class CountriesGdpItem(scrapy.Item):
    # scrapy.Item - exposes a dict like API, scrapy specific specialized dict
    country_name = scrapy.Field(
        # Formalization of the transition from selector to value that's assigned to a field
        # creating instances ofMapCompose and TakeFirst
        input_processor=MapCompose(remove_tags, str.strip),  # what comes in
        output_processor=TakeFirst()  # what comes out | TakeFirst() will extract the 1st val from a list of vals
    )
    region = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip),
        output_processor=TakeFirst()
    )
    gdp = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip),
        output_processor=TakeFirst()
    )
    year = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip),
        output_processor=TakeFirst()
    )
