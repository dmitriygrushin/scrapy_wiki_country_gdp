import scrapy
from ..items import CountriesGdpItem
from scrapy.loader import ItemLoader

""" to create a scrapy project exec: "scrapy startproject project_name"
to run a spider exec this command in the project dir: 
    "scrapy crawl name_of_spider", so in this case: "scrapy crawl gdp" 
    
     to output data do: 
        scrapy crawl spider_name -o name.csv | it also supports over formats i.e. name.json
            -o vs -O: -o: the former will NOT overwrite existing name.csv while the latter will
        
        scrapy is smart enough to figure out you're interested in the the yield {...} fields
    """


class GdpSpider(scrapy.Spider):
    name = "gdp"
    allowed_domains = ["wikipedia.org"]
    # what scrapy will call when the spider gets executed
    start_urls = ["https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)"]

    # after start_url http req is complete, the res will be passed in the response arg, parse will be auto-called
    def parse(self, response):
        """Specify all the steps & extraction paths using css/xpath that we want to extract from the page. The main part
        of the spider is something you've done without the framework i.e. extract, parse HTML from doc obj"""

        # visually/functionally looks like selectolax lib, but it's not
        for country in response.css("table.wikitable.sortable tbody tr:not([class])"):  # not([attr]): elem without attr
            # type(country): 'scrapy.selector.unified.Selector'
            # functionally this is the same as versions below | regular way or item or item-loaders + pipelines, ...
            #   everything can be done in this method, but it's better to have separation of concerns
            # order of executions seems to be:
            #   scrapy crawl gdp -O gdp.json -> yield the item (here) -> item-loaders -> pipeline post-processing
            item = ItemLoader(item=CountriesGdpItem(), selector=country)

            # don't need ::text or get() it gets taken care of in the ItemLoader processors
            item.add_css("country_name", "td:nth-child(1) a")
            item.add_css("region", "td:nth-child(2) a")
            item.add_css("gdp", "td:nth-child(3)")
            item.add_css("year", "td:nth-child(4)")

            yield item.load_item()

            """ missing github 
            ... -> github xpath selectors(main part before the extra scrapy stuff used for maintainability/scaling) 
                    -> outputting data -> ... -> pipelined data validation -> ...
            """

            """ "item" way of doing things vs the above or the default below
            # nothing wrong with this, but it does NOT scale very well compared to "ItemLoader" way
            
            item = CountriesGdpItem()

            item["country_name"] = country.css("td:nth-child(1) a::text").get(),
            item["region"] = country.css("td:nth-child(2) a::text").get(),
            item["gdp"] = country.css("td:nth-child(3)::text").get(),
            item["year"] = country.css("td:nth-child(4)::text").get()

            yield item
            """
            """ inside of the for loop before using "items" using items is functionally the same, it provides structure
            
           # what's being achieved with scrapy's items, item-loaders, pipelines(for post-processing) 
            - can be done here the good old fashioned way, but it wouldn't scale as well
            - so after getting the item you could do the post-processing here before returning
                which is functionally the same as using pipelines and item-loaders
            
            yield {
                # ::text is a pseudo selector (scrapy specific selector)
                "country_name": country.css("td:nth-child(1) a::text").get(),
                "region": country.css("td:nth-child(2) a::text").get(),
                "gdp": country.css("td:nth-child(3)::text").get(),
                "year": country.css("td:nth-child(4)::text").get()
            }
            """

            """ WHY USE YIELD OVER RETURN? Short answer: Its turns into a generator which is a common pattern in scrapy
            when using scrapy usually use yield: results in a generator.
                returns a val but doesn't exit the func it just pauses then if the flow of
                    ctrl is returned to the func it will pick up where it left off and pick up with the next country
                    so, it looks like a normal func but behaves like a generator
                    giving us output 1 item at a time compared to all at once at the end
            """


"""
XPATH: query lang for XML & XML-like docs(HTML). It's an alt to the CSS(CSS > XPATH) approach you've used above.
    - it's worth knowing as you may encounter this on the web 
    - fundamentally navigating around the doc obj: 
        examples below: nav, desc nav, attr select, text
        /html/body/table[3]/tbody/tr/td[2]
        //table[3]//td[2]   //: very similar to descendant combinator, a quicker way to go down the hierarchy
        //table[@class='wikitable'] - has a class wikitable
        //table[3]/@class - get class from 3rd table 
        //img[1]/@src - get src from 1st img
        //table[3]/td[2]/text() - gets text from 3rd table's 2nd td
        
        XPATH equivalent to the above CSS Version
        for country in response.xpath("//table[contains(@class, 'wikitable sortable')]//tbody//tr"):
            yield {
                # ".": start locally from the path above, so relative to country
                "country_name": country.xpath(".//td[1]//a/text()").get(),
                "region": country.xpath(".//td[2]//a/text()").get(),
                "gdp": country.xpath(".//td[3]/text()").get(),
                "year": country.xpath(".//td[4]/text()").get()
            }
"""

""" SCRAPY SHELL NOTES:
    scrapy shell "URL_HERE":
    allows you to expose selectors in the terminal
    Basically, it's like a python console where you can experiment
    and you can use the response obj like so: 
        for country in response.css("table.wikitable.sortable tbody tr"):
            print(country.css("td:nth-child(1) a::text").get())
    So, its a good way to experiment and play around with scrapy.
    If it works within the scarpy shell it will work within the spider
    
    It's similar to using the Browser's console to verify that an elem exists i.e. document.querySelectorAll('table.wikitable')
    
"""
