from playwright.async_api import async_playwright
import asyncio





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
        
        await page.goto('https://www.expedia.com/Flights-Search?flight-type=on&leg1=from:LAX,to:SIN,departure:11/1/2023TANYT&leg2=from:SIN,to:LAX,departure:11/8/2023TANYT&mode=search&options=cabinclass:economy&passengers=adults:1,infantinlap:N&trip=roundtrip', timeout=0)
        # await page.goto('https://flights.booking.com/flights/LAX.AIRPORT-SIN.AIRPORT/?type=ROUNDTRIP&adults=1&cabinClass=ECONOMY&children=&from=LAX.AIRPORT&to=SIN.AIRPORT&stops=0&depart=2023-10-20&return=2023-11-05&sort=FASTEST', timeout=0)
        # await page.goto('https://www.kayak.com/flights/SIN-MAA/2023-10-28/2023-11-04?fs=fdDir=true;stops=~0&sort=bestflight_a', timeout=0)
        # await page.goto('https://www.skyscanner.com/transport/flights/sins/trz/231011/231019/?adultsv2=1&cabinclass=economy&childrenv2=&inboundaltsenabled=false&outboundaltsenabled=false&preferdirects=false&ref=home&rtn=1', timeout=0)
        # Get the HTML content of the page
        
        html_content = await page.content()
        print(html_content)

        
       

# Run the asynchronous scraping function
if __name__ == "__main__":
    asyncio.run(scrape_website())

