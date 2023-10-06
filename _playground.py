from playwright.async_api import async_playwright
import asyncio
from typing import List

from playwright.sync_api import ElementHandle


class Product:
    name : str
    price : str
    desc :str

async def scrape_website():
    async with async_playwright() as p:
       
        # Launch a Chromium browser instance
        browser = await p.chromium.launch(headless=False)
        # browser = await p.chromium.launch()
        context = await browser.new_context()
        page = await context.new_page()
        # Define custom headers
        
        custom_headers = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
         'Cookie':'Apache=GwXXvg-AAABitqdr9k-c9-X2PwEA; kmkid=A41u9ss9CqNyN5npuY_nfzo; kayak=VoCvjV14J$IgrLx7ImQB; csid=6603444f-0238-4e7f-bd2d-21722b5b16d2; _gcl_au=1.1.1037543940.1695995043; _fbp=fb.1.1695995043000.0.9221568841256571; tracker_device=ab360a81-7b62-4125-9b77-c9b67552ddf2; kanid=; kanlabel=; __gads=ID=3bb52c5151c73793:T=1695995045:RT=1696002451:S=ALNI_MbQnJuQzNLcvIqtcva5GExWNQQq2Q; __gpi=UID=000009d89d22f49a:T=1695995045:RT=1696002451:S=ALNI_MYlyi6V0p7lQDFHVE4pcM03UO_1sA; g_state={"i_p":1696013083839,"i_l":1}; cluster=4; p1.med.sid=R-4sqqAJO4LkmYfUAuhKutT-BJGOsqQSHVZnSwKmaFsR62TpudvlXusgclxJwGO8L; kayak.mc=ATfDu8L_VkOVJ_ggzylm7NIglSeT-EupmtjpoW-tw-vQYR7M5tUM6Y5A_UvuHYqB6T_MDFvBL7G4_-KG0Tl_iUk0DxI5dSQbsTBDOlFEKvdIEiEGUCaI2pNp0UFsMli5J-bFE5g2oqhBhK6p6LV8C5yEe71-qlvJtObpsoREieGjWK__xhwSMsrHysjpo79SawywCdt5VPh6y9hPSHQFUnaEspoNwUdutw2LJI5m5FIdrS9Fkg2IDVgJF1UcQjoHy29vGJHGt58hmQs9tsidy4ld1vxIJnOK44XCZv_TfRtIL34fXVQRY9FAMYd7-364O1n5tQGqiEWubeRv4CWZp3yjklvUdMl7FGk0UAcsOd6sDp3gaz_rbEFCjpSW6ypvVS0PbDZuty4_4unSCDXNu4Q2cqVrGt1sPxANf5Kt41eTakX50-n6JLa-2JRF6_HUTnZkwDtjq5vsGcVu2FKCjajwZPg9l62YMLL30WYAeAFVE3BP8gu7iFvBKTYceKCFemAvmZVM_ztQDpuFsUVfYzSJuGVWFXihgHz6xWpkPks5qitCAQ4i8P_TaqcMdC6l6NghjdvMzv4NADfPJBlBWEXdakudYDKqDj9oaCaOBOMhziqm3xabF_MazYnFDyzc0zjGBCwn-gcH5HoOnRK10K0Vl_PK_TkxkT8dOmHS1sJb; _uetsid=414020e05ece11ee8e3fd9142f6963c9; _uetvid=41401ba05ece11eea7943713d4f1cc71',   
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        }
        await page.set_extra_http_headers(custom_headers)
        # Navigate to the URL you want to scrape
        # await page.goto('https://www.fandango.com/')
        # &sortOrder=INCREASING&sortType=DURATION
        # &sortOrder=INCREASING&sortType=PRICE
        # await page.goto('https://www.expedia.com/Flights-Search?flight-type=on&leg1=from:LAX,to:SIN,departure:11/1/2023TANYT&leg2=from:SIN,to:LAX,departure:11/8/2023TANYT&mode=search&options=cabinclass:economy&passengers=adults:1,infantinlap:N&trip=roundtrip', timeout=0)
        # await page.goto('https://flights.booking.com/flights/LAX.AIRPORT-SIN.AIRPORT/?type=ROUNDTRIP&adults=1&cabinClass=ECONOMY&children=&from=LAX.AIRPORT&to=SIN.AIRPORT&stops=0&depart=2023-10-20&return=2023-11-05&sort=FASTEST', timeout=0)
        # await page.goto('https://www.kayak.com/flights/SIN-MAA/2023-10-28/2023-11-04?fs=fdDir=true;stops=~0&sort=bestflight_a', timeout=0)
        # await page.goto('https://www.skyscanner.com/transport/flights/sins/trz/231011/231019/?adultsv2=1&cabinclass=economy&childrenv2=&inboundaltsenabled=false&outboundaltsenabled=false&preferdirects=false&ref=home&rtn=1', timeout=0)
        await page.goto('https://www.amazon.com/s?k=oppo+phone', timeout=0)
        html_content = await page.content()
        # page.
        product_element_container = await page.query_selector_all('div.puisg-row')
        product_list = []       
        for product in enumerate(product_element_container):
        #    <div class="a-section a-spacing-small a-spacing-top-small" bis_skin_checked="1"><div class="a-section a-spacing-none puis-padding-right-small s-title-instructions-style" bis_skin_checked="1"><h2 class="a-size-mini a-spacing-none a-color-base s-line-clamp-2"><a class="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal" href="/OPPO-Dual-SIM-Unlocked-Smartphone-Midnight/dp/B0B5LY4WHF/ref=sr_1_2?keywords=oppo+phone&amp;qid=1696565260&amp;sr=8-2"><span class="a-size-medium a-color-base a-text-normal">OPPO A77 Dual-SIM 64GB ROM + 4GB RAM (Only GSM | No CDMA) Factory Unlocked 5G Smartphone (Midnight Black) - International Version</span> </a> </h2></div><div class="a-section a-spacing-none a-spacing-top-micro" bis_skin_checked="1"><div class="a-row a-size-small" bis_skin_checked="1"><span aria-label="3.1 out of 5 stars"><span class="a-declarative" data-version-id="v3vtwxgppca0z12v18v51zrqona" data-render-id="ri9b34yhpvnbl2ktz886fmvhyi" data-action="a-popover" data-csa-c-type="widget" data-csa-c-func-deps="aui-da-a-popover" data-a-popover="{&quot;position&quot;:&quot;triggerBottom&quot;,&quot;popoverLabel&quot;:&quot;&quot;,&quot;url&quot;:&quot;/review/widgets/average-customer-review/popover/ref=acr_search__popover?ie=UTF8&amp;asin=B0B5LY4WHF&amp;ref=acr_search__popover&amp;contextId=search&quot;,&quot;closeButton&quot;:false,&quot;closeButtonLabel&quot;:&quot;&quot;}" data-csa-c-id="ru9jop-n7sp4u-rvca54-jdacwz"><a href="javascript:void(0)" role="button" class="a-popover-trigger a-declarative"><i class="a-icon a-icon-star-small a-star-small-3 aok-align-bottom"><span class="a-icon-alt">3.1 out of 5 stars</span></i><i class="a-icon a-icon-popover"></i></a></span> </span><span aria-label="7"><a class="a-link-normal s-underline-text s-underline-link-text s-link-style" href="/OPPO-Dual-SIM-Unlocked-Smartphone-Midnight/dp/B0B5LY4WHF/ref=sr_1_2?keywords=oppo+phone&amp;qid=1696565260&amp;sr=8-2#customerReviews"><span class="a-size-base s-underline-text">7</span> </a> </span></div></div><div class="puisg-row" bis_skin_checked="1"><div class="puisg-col puisg-col-4-of-12 puisg-col-4-of-16 puisg-col-4-of-20 puisg-col-4-of-24" bis_skin_checked="1"><div class="puisg-col-inner" bis_skin_checked="1"><div class="a-section a-spacing-none a-spacing-top-micro puis-price-instructions-style" bis_skin_checked="1"><div class="a-row a-size-base a-color-base" bis_skin_checked="1"><a class="a-size-base a-link-normal s-no-hover s-underline-text s-underline-link-text s-link-style a-text-normal" href="/OPPO-Dual-SIM-Unlocked-Smartphone-Midnight/dp/B0B5LY4WHF/ref=sr_1_2?keywords=oppo+phone&amp;qid=1696565260&amp;sr=8-2"><span class="a-price" data-a-size="xl" data-a-color="base"><span class="a-offscreen">$194.99</span><span aria-hidden="true"><span class="a-price-symbol">$</span><span class="a-price-whole">194<span class="a-price-decimal">.</span></span><span class="a-price-fraction">99</span></span></span> </a> <span class="a-letter-space"></span></div></div><div class="a-section a-spacing-none a-spacing-top-micro" bis_skin_checked="1"><div class="a-row a-size-base a-color-secondary s-align-children-center" bis_skin_checked="1"><div class="a-row" bis_skin_checked="1"><span aria-label="FREE delivery Oct 11 - 13 "><span class="a-color-base">FREE delivery </span><span class="a-color-base a-text-bold">Oct 11 - 13 </span></span></div><div class="a-row" bis_skin_checked="1"><span aria-label="Or fastest delivery Tue, Oct 10 "><span class="a-color-base">Or fastest delivery </span><span class="a-color-base a-text-bold">Tue, Oct 10 </span></span></div></div><div class="a-row a-size-base a-color-secondary" bis_skin_checked="1"><span aria-label="Only 8 left in stock - order soon."><span class="a-size-base a-color-price">Only 8 left in stock - order soon.</span></span></div></div><div class="a-section a-spacing-none a-spacing-top-mini" bis_skin_checked="1"><div class="a-row a-size-base a-color-secondary" bis_skin_checked="1"><span class="a-size-base a-color-secondary">More Buying Choices</span><br><span class="a-color-base">$169.99</span><span class="a-letter-space"></span><span class="a-declarative" data-version-id="v3vtwxgppca0z12v18v51zrqona" data-render-id="ri9b34yhpvnbl2ktz886fmvhyi" data-action="s-show-all-offers-display" data-csa-c-type="widget" data-csa-c-func-deps="aui-da-s-show-all-offers-display" data-s-show-all-offers-display="{&quot;assetMismatch&quot;:&quot;Abandon&quot;,&quot;url&quot;:&quot;/gp/aod/ajax/ref=sr_1_2_aod?asin=B0B5LY4WHF&amp;pc=sp&amp;keywords=oppo+phone&amp;qid=1696565260&amp;sr=8-2&amp;rrid=P7XMSS8JK4B253YB05T4&quot;,&quot;fallbackUrl&quot;:&quot;/gp/offer-listing/B0B5LY4WHF/ref=sr_1_2_olp?keywords=oppo+phone&amp;qid=1696565260&amp;sr=8-2&quot;}" data-csa-c-id="5z0vvu-3rtkqs-kd4v32-h4ksul"><a class="a-link-normal s-link-style s-underline-text s-underline-link-text" href="/gp/offer-listing/B0B5LY4WHF/ref=sr_1_2_olp?keywords=oppo+phone&amp;qid=1696565260&amp;sr=8-2">(3 used &amp; new offers)</a></span><div id="all-offers-display" class="a-section aok-hidden" bis_skin_checked="1"><div id="all-offers-display-spinner" class="a-spinner-wrapper aok-hidden" bis_skin_checked="1"><span class="a-spinner a-spinner-medium"></span></div></div><span class="a-declarative" data-version-id="v3vtwxgppca0z12v18v51zrqona" data-render-id="ri9b34yhpvnbl2ktz886fmvhyi" data-action="close-all-offers-display" data-csa-c-type="widget" data-csa-c-func-deps="aui-da-close-all-offers-display" data-csa-c-id="u1e7dc-h9ba5e-q95gyj-eglktn"><div id="aod-background" class="a-section aok-hidden aod-darken-background" bis_skin_checked="1"></div></span></div></div></div></div><div class="puisg-col puisg-col-4-of-12 puisg-col-4-of-16 puisg-col-8-of-20 puisg-col-8-of-24" bis_skin_checked="1"><div class="puisg-col-inner" bis_skin_checked="1"><div class="a-section a-spacing-none a-spacing-top-micro puis-product-grid-adjustment" bis_skin_checked="1"><div class="puisg-row s-product-specs-view" bis_skin_checked="1"><div class="puisg-col puisg-col-0-of-12 puisg-col-4-of-16 puisg-col-2-of-20 puisg-col-2-of-24 puis-padding-right-small" bis_skin_checked="1"><div class="puisg-col-inner" bis_skin_checked="1"><span class="a-color-secondary">Display Size</span><span class="list-separator"><span>:</span><span class="a-letter-space"></span></span><br class="row-separator"><span class="a-text-bold">6.56 inches</span></div></div><div class="puisg-col puisg-col-0-of-12 puisg-col-4-of-16 puisg-col-2-of-20 puisg-col-2-of-24 puis-padding-right-small" bis_skin_checked="1"><div class="puisg-col-inner" bis_skin_checked="1"><span class="a-color-secondary">Memory</span><span class="list-separator"><span>:</span><span class="a-letter-space"></span></span><br class="row-separator"><span class="a-text-bold">64 GB</span></div></div><div class="puisg-col puisg-col-0-of-12 puisg-col-4-of-16 puisg-col-2-of-20 puisg-col-2-of-24 puis-padding-right-small" bis_skin_checked="1"><div class="puisg-col-inner" bis_skin_checked="1"><span class="a-color-secondary">Color</span><span class="list-separator"><span>:</span><span class="a-letter-space"></span></span><br class="row-separator"><span class="a-text-bold">Midnight Black</span></div></div><div class="puisg-col puisg-col-0-of-12 puisg-col-4-of-16 puisg-col-2-of-20 puisg-col-2-of-24 puis-padding-right-small" bis_skin_checked="1"><div class="puisg-col-inner" bis_skin_checked="1"><span class="a-color-secondary">Brand</span><span class="list-separator"><span>:</span><span class="a-letter-space"></span></span><br class="row-separator"><span class="a-text-bold">OPPO</span></div></div></div></div></div></div></div></div>
           product_name_element = await product.query_selector('div.a-section.a-spacing-small.a-spacing-top-small')
           product_name = await product_name_element.inner_text()
           print("Product Name :", product_name)
           
        #    print(product)
        # print(html_content)
        # Get the HTML content of the page
        
       
    

        
       

# Run the asynchronous scraping function
if __name__ == "__main__":
    asyncio.run(scrape_website())

