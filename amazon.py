import asyncio
from collections import namedtuple

from playwright.async_api import async_playwright
from playwright.sync_api import ElementHandle

from scraper import Itinerary
from scraper import Scraper
from typing import List
import os
import json

class SortingOption:
    def __init__(self, code, name):
        self.code = code
        self.name = name

    def __str__(self):
        return self.name

# Create instances of SortingOption for different sorting options
cheapest_option = SortingOption('CHEAPEST', 'Sort by Cheapest')
costliest_option = SortingOption('COSTLIEST', 'Sort by Costliest')
best_option = SortingOption('BEST', 'Sort by Best')

current_option = cheapest_option

class Product:
    name : str
    price : str
    specs:List[str] = []

    def to_json(self):
        json= {
            "name":self.name,
            "price":self.price
        }
        d = []
        for item in self.specs:
            d.append(item)
        json['specs']=d      
        return json
    def get_price_value(self):
        return float(self.price.replace("$", "").replace(",", ""))
    
class Amazon:

    product_list:List[Product] = []

    # Function to save  instances to a JSON file
    async def save_products_to_json(self, folder_name: str, file_prefix='Best'):
        file_prefix = file_prefix.lower()
        # Check if the folder exists, and if not, create it
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        # Define the file path
        file_path = os.path.join(folder_name, folder_name + '-' + file_prefix + '.json')
        serialized_list = []
        for item in self.product_list:
            serialized_list.append(item.to_json())
            # break
        with open(file_path, 'w') as json_file:
            json.dump(serialized_list, json_file, indent=4)
       

    async def scrape_website(self, json_folder_name:str,search_text:str, sort_by:SortingOption =cheapest_option):
        async with async_playwright() as p:
            # Launch a Chromium browser instance
            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context()
            page = await context.new_page()
        
            url = 'https://www.amazon.com/s?k='+search_text
            print(url)

            # Navigate to the URL you want to scrape
            await page.goto(url, timeout=0)
            html_text = await page.content()
            # print(html_text)

             # page.
            await page.wait_for_selector('div')
            product_element_container = await page.query_selector_all('div.puisg-row')
            for index, item_element in enumerate(product_element_container):
                product = Product()
                #    <div class="a-section a-spacing-small a-spacing-top-small" bis_skin_checked="1"><div class="a-section a-spacing-none puis-padding-right-small s-title-instructions-style" bis_skin_checked="1"><h2 class="a-size-mini a-spacing-none a-color-base s-line-clamp-2"><a class="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal" href="/OPPO-Dual-SIM-Unlocked-Smartphone-Midnight/dp/B0B5LY4WHF/ref=sr_1_2?keywords=oppo+phone&amp;qid=1696565260&amp;sr=8-2"><span class="a-size-medium a-color-base a-text-normal">OPPO A77 Dual-SIM 64GB ROM + 4GB RAM (Only GSM | No CDMA) Factory Unlocked 5G Smartphone (Midnight Black) - International Version</span> </a> </h2></div><div class="a-section a-spacing-none a-spacing-top-micro" bis_skin_checked="1"><div class="a-row a-size-small" bis_skin_checked="1"><span aria-label="3.1 out of 5 stars"><span class="a-declarative" data-version-id="v3vtwxgppca0z12v18v51zrqona" data-render-id="ri9b34yhpvnbl2ktz886fmvhyi" data-action="a-popover" data-csa-c-type="widget" data-csa-c-func-deps="aui-da-a-popover" data-a-popover="{&quot;position&quot;:&quot;triggerBottom&quot;,&quot;popoverLabel&quot;:&quot;&quot;,&quot;url&quot;:&quot;/review/widgets/average-customer-review/popover/ref=acr_search__popover?ie=UTF8&amp;asin=B0B5LY4WHF&amp;ref=acr_search__popover&amp;contextId=search&quot;,&quot;closeButton&quot;:false,&quot;closeButtonLabel&quot;:&quot;&quot;}" data-csa-c-id="ru9jop-n7sp4u-rvca54-jdacwz"><a href="javascript:void(0)" role="button" class="a-popover-trigger a-declarative"><i class="a-icon a-icon-star-small a-star-small-3 aok-align-bottom"><span class="a-icon-alt">3.1 out of 5 stars</span></i><i class="a-icon a-icon-popover"></i></a></span> </span><span aria-label="7"><a class="a-link-normal s-underline-text s-underline-link-text s-link-style" href="/OPPO-Dual-SIM-Unlocked-Smartphone-Midnight/dp/B0B5LY4WHF/ref=sr_1_2?keywords=oppo+phone&amp;qid=1696565260&amp;sr=8-2#customerReviews"><span class="a-size-base s-underline-text">7</span> </a> </span></div></div><div class="puisg-row" bis_skin_checked="1"><div class="puisg-col puisg-col-4-of-12 puisg-col-4-of-16 puisg-col-4-of-20 puisg-col-4-of-24" bis_skin_checked="1"><div class="puisg-col-inner" bis_skin_checked="1"><div class="a-section a-spacing-none a-spacing-top-micro puis-product_name-instructions-style" bis_skin_checked="1"><div class="a-row a-size-base a-color-base" bis_skin_checked="1"><a class="a-size-base a-link-normal s-no-hover s-underline-text s-underline-link-text s-link-style a-text-normal" href="/OPPO-Dual-SIM-Unlocked-Smartphone-Midnight/dp/B0B5LY4WHF/ref=sr_1_2?keywords=oppo+phone&amp;qid=1696565260&amp;sr=8-2"><span class="a-product_name" data-a-size="xl" data-a-color="base"><span class="a-offscreen">$194.99</span><span aria-hidden="true"><span class="a-product_name-symbol">$</span><span class="a-product_name-whole">194<span class="a-product_name-decimal">.</span></span><span class="a-product_name-fraction">99</span></span></span> </a> <span class="a-letter-space"></span></div></div><div class="a-section a-spacing-none a-spacing-top-micro" bis_skin_checked="1"><div class="a-row a-size-base a-color-secondary s-align-children-center" bis_skin_checked="1"><div class="a-row" bis_skin_checked="1"><span aria-label="FREE delivery Oct 11 - 13 "><span class="a-color-base">FREE delivery </span><span class="a-color-base a-text-bold">Oct 11 - 13 </span></span></div><div class="a-row" bis_skin_checked="1"><span aria-label="Or fastest delivery Tue, Oct 10 "><span class="a-color-base">Or fastest delivery </span><span class="a-color-base a-text-bold">Tue, Oct 10 </span></span></div></div><div class="a-row a-size-base a-color-secondary" bis_skin_checked="1"><span aria-label="Only 8 left in stock - order soon."><span class="a-size-base a-color-product_name">Only 8 left in stock - order soon.</span></span></div></div><div class="a-section a-spacing-none a-spacing-top-mini" bis_skin_checked="1"><div class="a-row a-size-base a-color-secondary" bis_skin_checked="1"><span class="a-size-base a-color-secondary">More Buying Choices</span><br><span class="a-color-base">$169.99</span><span class="a-letter-space"></span><span class="a-declarative" data-version-id="v3vtwxgppca0z12v18v51zrqona" data-render-id="ri9b34yhpvnbl2ktz886fmvhyi" data-action="s-show-all-offers-display" data-csa-c-type="widget" data-csa-c-func-deps="aui-da-s-show-all-offers-display" data-s-show-all-offers-display="{&quot;assetMismatch&quot;:&quot;Abandon&quot;,&quot;url&quot;:&quot;/gp/aod/ajax/ref=sr_1_2_aod?asin=B0B5LY4WHF&amp;pc=sp&amp;keywords=oppo+phone&amp;qid=1696565260&amp;sr=8-2&amp;rrid=P7XMSS8JK4B253YB05T4&quot;,&quot;fallbackUrl&quot;:&quot;/gp/offer-listing/B0B5LY4WHF/ref=sr_1_2_olp?keywords=oppo+phone&amp;qid=1696565260&amp;sr=8-2&quot;}" data-csa-c-id="5z0vvu-3rtkqs-kd4v32-h4ksul"><a class="a-link-normal s-link-style s-underline-text s-underline-link-text" href="/gp/offer-listing/B0B5LY4WHF/ref=sr_1_2_olp?keywords=oppo+phone&amp;qid=1696565260&amp;sr=8-2">(3 used &amp; new offers)</a></span><div id="all-offers-display" class="a-section aok-hidden" bis_skin_checked="1"><div id="all-offers-display-spinner" class="a-spinner-wrapper aok-hidden" bis_skin_checked="1"><span class="a-spinner a-spinner-medium"></span></div></div><span class="a-declarative" data-version-id="v3vtwxgppca0z12v18v51zrqona" data-render-id="ri9b34yhpvnbl2ktz886fmvhyi" data-action="close-all-offers-display" data-csa-c-type="widget" data-csa-c-func-deps="aui-da-close-all-offers-display" data-csa-c-id="u1e7dc-h9ba5e-q95gyj-eglktn"><div id="aod-background" class="a-section aok-hidden aod-darken-background" bis_skin_checked="1"></div></span></div></div></div></div><div class="puisg-col puisg-col-4-of-12 puisg-col-4-of-16 puisg-col-8-of-20 puisg-col-8-of-24" bis_skin_checked="1"><div class="puisg-col-inner" bis_skin_checked="1"><div class="a-section a-spacing-none a-spacing-top-micro puis-product-grid-adjustment" bis_skin_checked="1"><div class="puisg-row s-product-specs-view" bis_skin_checked="1"><div class="puisg-col puisg-col-0-of-12 puisg-col-4-of-16 puisg-col-2-of-20 puisg-col-2-of-24 puis-padding-right-small" bis_skin_checked="1"><div class="puisg-col-inner" bis_skin_checked="1"><span class="a-color-secondary">Display Size</span><span class="list-separator"><span>:</span><span class="a-letter-space"></span></span><br class="row-separator"><span class="a-text-bold">6.56 inches</span></div></div><div class="puisg-col puisg-col-0-of-12 puisg-col-4-of-16 puisg-col-2-of-20 puisg-col-2-of-24 puis-padding-right-small" bis_skin_checked="1"><div class="puisg-col-inner" bis_skin_checked="1"><span class="a-color-secondary">Memory</span><span class="list-separator"><span>:</span><span class="a-letter-space"></span></span><br class="row-separator"><span class="a-text-bold">64 GB</span></div></div><div class="puisg-col puisg-col-0-of-12 puisg-col-4-of-16 puisg-col-2-of-20 puisg-col-2-of-24 puis-padding-right-small" bis_skin_checked="1"><div class="puisg-col-inner" bis_skin_checked="1"><span class="a-color-secondary">Color</span><span class="list-separator"><span>:</span><span class="a-letter-space"></span></span><br class="row-separator"><span class="a-text-bold">Midnight Black</span></div></div><div class="puisg-col puisg-col-0-of-12 puisg-col-4-of-16 puisg-col-2-of-20 puisg-col-2-of-24 puis-padding-right-small" bis_skin_checked="1"><div class="puisg-col-inner" bis_skin_checked="1"><span class="a-color-secondary">Brand</span><span class="list-separator"><span>:</span><span class="a-letter-space"></span></span><br class="row-separator"><span class="a-text-bold">OPPO</span></div></div></div></div></div></div></div></div>
                # <span class="a-size-medium a-color-base a-text-normal">OPPO A77 Dual-SIM 64GB ROM + 4GB RAM (Only GSM | No CDMA) Factory Unlocked 5G Smartphone (Midnight Black) - International Version</span>
                # <div class="a-section a-spacing-none puis-padding-right-small s-title-instructions-style" bis_skin_checked="1"><h2 class="a-size-mini a-spacing-none a-color-base s-line-clamp-2"><a class="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal" href="/OPPO-Dual-SIM-Unlocked-Smartphone-Midnight/dp/B0B5LY4WHF/ref=sr_1_2?keywords=oppo+phone&amp;qid=1696565260&amp;sr=8-2"><span class="a-size-medium a-color-base a-text-normal">OPPO A77 Dual-SIM 64GB ROM + 4GB RAM (Only GSM | No CDMA) Factory Unlocked 5G Smartphone (Midnight Black) - International Version</span> </a> </h2></div>
                product_name_element = await item_element.query_selector('div.a-section.a-spacing-none.puis-padding-right-small.s-title-instructions-style')
                if product_name_element == None:
                    continue
                product_name = await product_name_element.inner_text()
                if product_name.startswith('Sponsored'):
                    continue 
                print("Product Name :", product_name)
                product.name = product_name
                # <div class="a-row a-size-base a-color-base" bis_skin_checked="1"><a class="a-size-base a-link-normal s-no-hover s-underline-text s-underline-link-text s-link-style a-text-normal" href="/OPPO-Dual-SIM-Unlocked-Smartphone-Midnight/dp/B0B5LY4WHF/ref=sr_1_2?keywords=oppo+phone&amp;qid=1696565260&amp;sr=8-2"><span class="a-product_name" data-a-size="xl" data-a-color="base"><span class="a-offscreen">$194.99</span><span aria-hidden="true"><span class="a-product_name-symbol">$</span><span class="a-product_name-whole">194<span class="a-product_name-decimal">.</span></span><span class="a-product_name-fraction">99</span></span></span> </a> <span class="a-letter-space"></span></div>
                # <span class="a-price" data-a-size="xl" data-a-color="base"><span class="a-offscreen">$194.99</span><span aria-hidden="true"><span class="a-price-symbol">$</span><span class="a-price-whole">194<span class="a-price-decimal">.</span></span><span class="a-price-fraction">99</span></span></span>
                price_element = await item_element.query_selector('span.a-price > span.a-offscreen')
                if price_element == None:
                    continue
                price = await  price_element.inner_text()
                print('Price :',price)
                product.price = price
                # <div class="puisg-row s-product-specs-view" bis_skin_checked="1"><div class="puisg-col puisg-col-0-of-12 puisg-col-4-of-16 puisg-col-2-of-20 puisg-col-2-of-24 puis-padding-right-small" bis_skin_checked="1"><div class="puisg-col-inner" bis_skin_checked="1"><span class="a-color-secondary">Display Size</span><span class="list-separator"><span>:</span><span class="a-letter-space"></span></span><br class="row-separator"><span class="a-text-bold">6.56 inches</span></div></div><div class="puisg-col puisg-col-0-of-12 puisg-col-4-of-16 puisg-col-2-of-20 puisg-col-2-of-24 puis-padding-right-small" bis_skin_checked="1"><div class="puisg-col-inner" bis_skin_checked="1"><span class="a-color-secondary">Memory</span><span class="list-separator"><span>:</span><span class="a-letter-space"></span></span><br class="row-separator"><span class="a-text-bold">64 GB</span></div></div><div class="puisg-col puisg-col-0-of-12 puisg-col-4-of-16 puisg-col-2-of-20 puisg-col-2-of-24 puis-padding-right-small" bis_skin_checked="1"><div class="puisg-col-inner" bis_skin_checked="1"><span class="a-color-secondary">Color</span><span class="list-separator"><span>:</span><span class="a-letter-space"></span></span><br class="row-separator"><span class="a-text-bold">Midnight Black</span></div></div><div class="puisg-col puisg-col-0-of-12 puisg-col-4-of-16 puisg-col-2-of-20 puisg-col-2-of-24 puis-padding-right-small" bis_skin_checked="1"><div class="puisg-col-inner" bis_skin_checked="1"><span class="a-color-secondary">Brand</span><span class="list-separator"><span>:</span><span class="a-letter-space"></span></span><br class="row-separator"><span class="a-text-bold">OPPO</span></div></div></div>
                desc_elements = await item_element.query_selector_all('div.puisg-row.s-product-specs-view > *')
                print('Desc :')
                specs_list = []    
                for index, specs_element in enumerate(desc_elements):
                    specs = await  specs_element.inner_text()
                    specs = specs.replace('\n', ':')
                    specs_list.append(specs)
                product.specs = specs_list    
                self.product_list.append(product)
            
            # Sort the array based on the result of the get_value method
            self.product_list = sorted(self.product_list, key=lambda obj: obj.get_price_value())
            await self.save_products_to_json(json_folder_name, "".join(search_text.split()))
            # await browser.close()


# Run the asynchronous scraping function
if __name__ == "__main__":
    json_folder_name = 'amazon'
    expedia = Amazon()
    search_text = 'oppo phone'
    asyncio.run(expedia.scrape_website(json_folder_name,search_text, cheapest_option))
