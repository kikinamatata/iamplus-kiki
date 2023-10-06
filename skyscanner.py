import asyncio
import re

from playwright.async_api import async_playwright

from scraper import AirlinesTime
from scraper import Itinerary
from scraper import Scraper


class SkyScanner(Scraper):

    async def get_trip(self, trip_element) -> AirlinesTime:

        try:
            # Code that might raise an exception
            a = 1 + 2

            # Name of Airlines
            # <img class="BpkImage_bpk-image__img__MDZkN" alt="United" src="//www.skyscanner.net/images/airlines/small/UA.png">
            img_element = await trip_element.query_selector(".BpkImage_bpk-image__img__MDZkN")
            airlines = await img_element.get_attribute("alt")
            print('Airlines :', airlines)
            # <div class="LegInfo_routePartialDepart__NzEwY" bis_skin_checked="1">
            # <span class="BpkText_bpk-text__MWZkY BpkText_bpk-text--lg__NjNhN LegInfo_routePartialTime__OTFkN">
            # <div bis_skin_checked="1">
            # <span class="BpkText_bpk-text__MWZkY BpkText_bpk-text--label-1__NjBhY">
            # 8:15 AM
            # </span></div></span>
            # <span class="BpkText_bpk-text__MWZkY BpkText_bpk-text--body-default__Y2M3Z">
            # <div tabindex="0" aria-label="Los Angeles International, LAX, United States" bis_skin_checked="1">
            # <span class="BpkText_bpk-text__MWZkY BpkText_bpk-text--body-default__Y2M3Z LegInfo_routePartialCityTooltip__NTE4Z">
            # LAX
            # </span>
            # </div>
            # </span>
            # </div>
            # from_city_element = await trip_element.query_selector('')

            time_city_element_list = await trip_element.query_selector_all('div.LegInfo_routePartialDepart__NzEwY > *')

            time_element = time_city_element_list[0]
            start_time = await time_element.inner_text()
            print('start_time', start_time)
            city_element = time_city_element_list[1]
            start_city = await city_element.inner_text()
            print('start_city', start_city)
            # <div class="LegInfo_routePartialArrive__Y2U1N" bis_skin_checked="1"><span class="BpkText_bpk-text__MWZkY BpkText_bpk-text--lg__NjNhN LegInfo_routePartialTime__OTFkN"><div bis_skin_checked="1"><span class="BpkText_bpk-text__MWZkY BpkText_bpk-text--label-1__NjBhY">6:45 PM</span><div class="TimeWithOffsetTooltip_offsetTooltipContainer__NjA0M" tabindex="0" aria-label="Arrives on Sunday, October 15, 2023" bis_skin_checked="1"><span class="BpkText_bpk-text__MWZkY BpkText_bpk-text--caption__MTIzM">+1</span></div></div></span><span class="BpkText_bpk-text__MWZkY BpkText_bpk-text--body-default__Y2M3Z"><div tabindex="0" aria-label="Singapore Changi, SIN, Singapore" bis_skin_checked="1"><span class="BpkText_bpk-text__MWZkY BpkText_bpk-text--body-default__Y2M3Z LegInfo_routePartialCityTooltip__NTE4Z">SIN</span></div></span></div>
            time_city_element_list = await trip_element.query_selector_all('div.LegInfo_routePartialArrive__Y2U1N > *')

            time_element = time_city_element_list[0]
            end_time = await time_element.inner_text()
            end_time = end_time.split('\n')[0]
            print('end_time', end_time)
            city_element = time_city_element_list[1]
            end_city = await city_element.inner_text()
            print('end_city', end_city)
        except Exception as e:
            # Code to handle the exception
            print(f"An exception of type {type(e).__name__} occurred: {e}")
            return None
        else:
            return AirlinesTime(airlines, start_time, end_time)

    async def scrape_website(self, json_folder_name, sort_by='bestflight_a'):
        async with async_playwright() as p:
            # Launch a Chromium browser instance
            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context()
            page = await context.new_page()
            c1 = self.city1_code
            c2 = self.city2_code
            t1 = self.travel_date
            r1 = self.return_date
            url = 'https://www.skyscanner.com/transport/flights/' + c1 + '/' + c2 + '/' + t1 + '/' + r1 + '/?''adultsv2=1&cabinclass=economy&childrenv2=&inboundaltsenabled=false&outboundaltsenabled=false&preferdirects=false&ref=home&rtn=1'

            print(url)

            # Navigate to the URL you want to scrape
            await page.goto(url)
            # await page.goto('https://www.kayak.com/flights/MAA-SIN/2023-10-29/2023-11-05?fs=fdDir=true;stops=~0&sort=bestflight_a')
            await page.get_by_role("button", name=re.compile(sort_by, re.IGNORECASE)).click()

            trip_element_list = await page.query_selector_all('div.FlightsTicket_container__NWJkY')
            for index, trip_element in enumerate(trip_element_list):
                skip_item = False
                itinerary = Itinerary(self.city1_code, self.city2_code, self.travel_date, self.return_date)
                itinerary.city1_name = self.city1_name
                itinerary.city2_name = self.city2_name
                # Get price
                # <div class="Price_mainPriceContainer__MDM3O" bis_skin_checked="1"><span class="BpkText_bpk-text__MWZkY BpkText_bpk-text--lg__NjNhN">$1,243</span></div>
                price = await trip_element.query_selector('div.Price_mainPriceContainer__MDM3O')
                price_text = await price.inner_text()
                print("Price :", price_text)
                itinerary.price = price_text
                # <div class="UpperTicketBody_legsContainer__ZjcyZ" bis_skin_checked="1"><div class="LegDetails_container__MTkyZ UpperTicketBody_leg__MmNkN" aria-hidden="true" bis_skin_checked="1"><div class="LogoImage_container__MDU0Z LegLogo_logoContainer__ODdkM UpperTicketBody_legLogo__ZjYwM" bis_skin_checked="1"><div class="LegLogo_legImage__MmY0Z" bis_skin_checked="1"><div class="BpkImage_bpk-image__YTkyO BpkImage_bpk-image--no-background__NGMyN" style="height: 0px; padding-bottom: 50%;" bis_skin_checked="1"><img class="BpkImage_bpk-image__img__MDZkN" alt="United" src="//www.skyscanner.net/images/airlines/small/UA.png"></div></div></div><div class="LegInfo_legInfo__ZGMzY" bis_skin_checked="1"><div class="LegInfo_routePartialDepart__NzEwY" bis_skin_checked="1"><span class="BpkText_bpk-text__MWZkY BpkText_bpk-text--lg__NjNhN LegInfo_routePartialTime__OTFkN"><div bis_skin_checked="1"><span class="BpkText_bpk-text__MWZkY BpkText_bpk-text--label-1__NjBhY">8:15 AM</span></div></span><span class="BpkText_bpk-text__MWZkY BpkText_bpk-text--body-default__Y2M3Z"><div tabindex="0" aria-label="Los Angeles International, LAX, United States" bis_skin_checked="1"><span class="BpkText_bpk-text__MWZkY BpkText_bpk-text--body-default__Y2M3Z LegInfo_routePartialCityTooltip__NTE4Z">LAX</span></div></span></div><div class="LegInfo_stopsContainer__NWIyN" bis_skin_checked="1"><span class="BpkText_bpk-text__MWZkY BpkText_bpk-text--xs__ZDJmY Duration_duration__NmUyM">19h 30m</span><div class="LegInfo_stopLine__MzUxZ" bis_skin_checked="1"><span class="LegInfo_stopDot__ZTAyN"></span><svg xmlns="http://www.w3.org/2000/svg" xml:space="preserve" viewBox="0 0 12 12" class="LegInfo_planeEnd__ZDkxM"><path fill="#898294" d="M3.922 12h.499a.52.52 0 0 0 .444-.247L7.949 6.8l3.233-.019A.8.8 0 0 0 12 6a.8.8 0 0 0-.818-.781L7.949 5.2 4.866.246A.525.525 0 0 0 4.421 0h-.499a.523.523 0 0 0-.489.71L5.149 5.2H2.296l-.664-1.33a.523.523 0 0 0-.436-.288L0 3.509 1.097 6 0 8.491l1.196-.073a.523.523 0 0 0 .436-.288l.664-1.33h2.853l-1.716 4.49a.523.523 0 0 0 .489.71"></path></svg></div><div class="LegInfo_stopsLabelContainer__MmM0Z" bis_skin_checked="1"><span class="BpkText_bpk-text__MWZkY BpkText_bpk-text--xs__ZDJmY LegInfo_stopsLabelRed__NTY2Y">1 stop</span>&nbsp;<div class="LegInfo_stopsRow__MTUwZ" bis_skin_checked="1"><span class="BpkText_bpk-text__MWZkY BpkText_bpk-text--xs__ZDJmY LegInfo_stopStation__M2E5N"><div tabindex="0" aria-label="SFO" bis_skin_checked="1"><span class="BpkText_bpk-text__MWZkY BpkText_bpk-text--xs__ZDJmY">SFO</span></div></span></div></div></div><div class="LegInfo_routePartialArrive__Y2U1N" bis_skin_checked="1"><span class="BpkText_bpk-text__MWZkY BpkText_bpk-text--lg__NjNhN LegInfo_routePartialTime__OTFkN"><div bis_skin_checked="1"><span class="BpkText_bpk-text__MWZkY BpkText_bpk-text--label-1__NjBhY">6:45 PM</span><div class="TimeWithOffsetTooltip_offsetTooltipContainer__NjA0M" tabindex="0" aria-label="Arrives on Sunday, October 15, 2023" bis_skin_checked="1"><span class="BpkText_bpk-text__MWZkY BpkText_bpk-text--caption__MTIzM">+1</span></div></div></span><span class="BpkText_bpk-text__MWZkY BpkText_bpk-text--body-default__Y2M3Z"><div tabindex="0" aria-label="Singapore Changi, SIN, Singapore" bis_skin_checked="1"><span class="BpkText_bpk-text__MWZkY BpkText_bpk-text--body-default__Y2M3Z LegInfo_routePartialCityTooltip__NTE4Z">SIN</span></div></span></div></div></div><div class="LegDetails_container__MTkyZ UpperTicketBody_leg__MmNkN" aria-hidden="true" bis_skin_checked="1"><div class="LogoImage_container__MDU0Z LegLogo_logoContainer__ODdkM UpperTicketBody_legLogo__ZjYwM" bis_skin_checked="1"><div class="LegLogo_legImage__MmY0Z" bis_skin_checked="1"><div class="BpkImage_bpk-image__YTkyO BpkImage_bpk-image--no-background__NGMyN" style="height: 0px; padding-bottom: 50%;" bis_skin_checked="1"><img class="BpkImage_bpk-image__img__MDZkN" alt="United" src="//www.skyscanner.net/images/airlines/small/UA.png"></div></div></div><div class="LegInfo_legInfo__ZGMzY" bis_skin_checked="1"><div class="LegInfo_routePartialDepart__NzEwY" bis_skin_checked="1"><span class="BpkText_bpk-text__MWZkY BpkText_bpk-text--lg__NjNhN LegInfo_routePartialTime__OTFkN"><div bis_skin_checked="1"><span class="BpkText_bpk-text__MWZkY BpkText_bpk-text--label-1__NjBhY">8:45 AM</span></div></span><span class="BpkText_bpk-text__MWZkY BpkText_bpk-text--body-default__Y2M3Z"><div tabindex="0" aria-label="Singapore Changi, SIN, Singapore" bis_skin_checked="1"><span class="BpkText_bpk-text__MWZkY BpkText_bpk-text--body-default__Y2M3Z LegInfo_routePartialCityTooltip__NTE4Z">SIN</span></div></span></div><div class="LegInfo_stopsContainer__NWIyN" bis_skin_checked="1"><span class="BpkText_bpk-text__MWZkY BpkText_bpk-text--xs__ZDJmY Duration_duration__NmUyM">18h 20m</span><div class="LegInfo_stopLine__MzUxZ" bis_skin_checked="1"><span class="LegInfo_stopDot__ZTAyN"></span><svg xmlns="http://www.w3.org/2000/svg" xml:space="preserve" viewBox="0 0 12 12" class="LegInfo_planeEnd__ZDkxM"><path fill="#898294" d="M3.922 12h.499a.52.52 0 0 0 .444-.247L7.949 6.8l3.233-.019A.8.8 0 0 0 12 6a.8.8 0 0 0-.818-.781L7.949 5.2 4.866.246A.525.525 0 0 0 4.421 0h-.499a.523.523 0 0 0-.489.71L5.149 5.2H2.296l-.664-1.33a.523.523 0 0 0-.436-.288L0 3.509 1.097 6 0 8.491l1.196-.073a.523.523 0 0 0 .436-.288l.664-1.33h2.853l-1.716 4.49a.523.523 0 0 0 .489.71"></path></svg></div><div class="LegInfo_stopsLabelContainer__MmM0Z" bis_skin_checked="1"><span class="BpkText_bpk-text__MWZkY BpkText_bpk-text--xs__ZDJmY LegInfo_stopsLabelRed__NTY2Y">1 stop</span>&nbsp;<div class="LegInfo_stopsRow__MTUwZ" bis_skin_checked="1"><span class="BpkText_bpk-text__MWZkY BpkText_bpk-text--xs__ZDJmY LegInfo_stopStation__M2E5N"><div tabindex="0" aria-label="SFO" bis_skin_checked="1"><span class="BpkText_bpk-text__MWZkY BpkText_bpk-text--xs__ZDJmY">SFO</span></div></span></div></div></div><div class="LegInfo_routePartialArrive__Y2U1N" bis_skin_checked="1"><span class="BpkText_bpk-text__MWZkY BpkText_bpk-text--lg__NjNhN LegInfo_routePartialTime__OTFkN"><div bis_skin_checked="1"><span class="BpkText_bpk-text__MWZkY BpkText_bpk-text--label-1__NjBhY">12:05 PM</span></div></span><span class="BpkText_bpk-text__MWZkY BpkText_bpk-text--body-default__Y2M3Z"><div tabindex="0" aria-label="Los Angeles International, LAX, United States" bis_skin_checked="1"><span class="BpkText_bpk-text__MWZkY BpkText_bpk-text--body-default__Y2M3Z LegInfo_routePartialCityTooltip__NTE4Z">LAX</span></div></span></div></div></div></div>
                trip_start_element = await trip_element.query_selector('div.UpperTicketBody_legsContainer__ZjcyZ')
                trips = await trip_start_element.query_selector_all(" > *")
                travel_details = await self.get_trip(trips[0])
                if travel_details == None:
                    continue
                itinerary.travel_airlines = travel_details.airlines_name
                itinerary.travel_start_time = travel_details.start_time
                itinerary.travel_end_time = travel_details.end_time
                # Return Details
                return_details = await self.get_trip(trips[1])
                if return_details == None:
                    continue
                itinerary.return_airlines = return_details.airlines_name
                itinerary.return_start_time = return_details.start_time
                itinerary.return_end_time = return_details.end_time

                self.itinerary_list.append(itinerary)

        await self.save_itinerary_to_json(json_folder_name, sort_by)

        # Close the page and browser when done
        await page.close(run_before_unload=False)
        await browser.close()


# Run the asynchronous scraping function
if __name__ == "__main__":
    city1 = 'lax'
    city2 = 'sin'
    travel_date = '231014'
    return_date = '231020'
    json_folder_name = 'skyscanner'
    expedia = SkyScanner(city1_code=city1, city2_code=city2, travel_date=travel_date, return_date=return_date)
    sort_by_best = 'Best'
    sort_by_cheapest = 'Cheapest'
    sort_by_fastest = 'Fastest'

    asyncio.run(expedia.scrape_website(json_folder_name, sort_by_fastest))
