import asyncio
from collections import namedtuple

from playwright.async_api import async_playwright
from playwright.sync_api import ElementHandle

from scraper import Itinerary
from scraper import Scraper

# Define a named tuple for the result
Result = namedtuple("Result", ["price", "airlines_name", "start_time", "end_time"])


class Expedia(Scraper):

    async def get_travel_iternity(self, trip_element: ElementHandle) -> Result:
        # Get price
        # <span data-stid="" class="uitk-lockup-price" aria-hidden="true">$527</span>
        price = await trip_element.query_selector('span.uitk-lockup-price')
        price_text = await price.inner_text()
        print("Price :", price_text)

        # <div class="uitk-text truncate-lines-2 uitk-type-200 uitk-text-default-theme" data-test-id="flight-operated">Delta • Delta 9045 and 7662 operated by Korean Air</div>
        # airlines_name_element  = await trip_element.query_selector('div[data-test-id="flight-operated"]')
        airlines_name_element = await trip_element.query_selector(
            'div.uitk-text.truncate-lines-2.uitk-type-200.uitk-text-default-theme')
        airlines_name = await airlines_name_element.inner_text()
        print('Travel Airlines ', airlines_name)

        # <div data-test-id="arrival-time"><span class="uitk-text uitk-type-400 uitk-type-medium uitk-text-emphasis-theme" data-test-id="departure-time">
        # 11:50am - 5:00am</span><span class="uitk-text uitk-type-100 uitk-text-negative-theme uitk-spacing uitk-spacing-margin-inlinestart-one"><sup data-test-id="arrives-next-day">+2</sup></span></div>
        # time_element  = await trip_element.query_selector('span[data-test-id="departure-time"]')
        time_element = await trip_element.query_selector(
            'span.uitk-text.uitk-type-400.uitk-type-medium.uitk-text-emphasis-theme')
        start_end_time = await time_element.inner_text()
        times = start_end_time.split(" - ")
        start_time = times[0]
        end_time = times[1]
        print('start time', start_time, 'end_time', end_time)
        return Result(price_text, airlines_name, start_time, end_time)

    # write a code for

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

            # travel_url = 'https://www.expedia.com/Flights-Search?flight-type=on&leg1=from:LAX,to:SIN,departure:11/1/2023TANYT&mode=search&options=cabinclass:economy&passengers=adults:1,infantinlap:N&trip=oneway&sortOrder=INCREASING&sortType=PRICE'

            travel_url = 'https://www.expedia.com/Flights-Search?flight-type=on&leg1=from:' + c1 + ',to:' + c2
            travel_url += ',departure:' + t1 + 'TANYT' + '&mode=search&options=cabinclass:economy&passengers=adults:1,infantinlap:N&trip=oneway'
            travel_url += '&sortOrder=INCREASING&sortType=' + sort_by
            # travel_url+= 'filters=[{"numOfStopFilterValue":{"stopInfo":{"numberOfStops":0,"stopFilterOperation":"EQUAL"}}}]'
            print(travel_url)

            # Navigate to the URL you want to scrape
            await page.goto(travel_url, timeout=0)
            html_text = await page.content()
            # print(html_text)

            # <div class="css-209ldq"><div id="flight-card-0"><div class="Box-module__root___Hr7Gv Box-module__root--background-color-elevation_one___QasI2 Box-module__root--border-color-neutral_alt___JbiyK Box-module__root--border-width-100___9-Izb Box-module__root--border-radius-200___db4tG Box-module__root--overflow-hidden___3GhcK" style="--bui_box_padding--s: 0;"><div class="css-4o3ibe"><div class="css-v2mveg" style="width: 64%;"><div class="css-13ekbfz"><div class="css-1rgw82s"><div class="css-k456he"><div class="css-3gojea"><div class="css-3gojea" style="grid-area: row1 / col1 / span 2 / span 2; background-image: url(&quot;https://r-xx.bstatic.com/data/airlines_logo/SQ.png&quot;);"></div></div></div></div><div class="css-1oe9l2q"><div class="css-1niqckn"><div class="css-io4ta2"><div class="css-1yl6p1k" style="text-align: left;"><div data-testid="flight_card_segment_departure_time_0" class="Text-module__root--variant-strong_1___SNYxf">23:40</div><div class="css-5nu86q"><div data-testid="flight_card_segment_departure_airport_0" class="Text-module__root--variant-small_1___+fbYj">LAX</div><div class="Text-module__root--variant-small_1___+fbYj css-1n4sh5k"> . </div><div data-testid="flight_card_segment_departure_date_0" class="Text-module__root--variant-small_1___+fbYj">14 Oct</div></div></div><div class="css-1wnqz2m" style="width: 50%;"><div data-testid="flight_card_segment_duration_0" aria-hidden="true" class="Text-module__root--variant-small_1___+fbYj css-ylq2vz">17h 10m</div><div class="HiddenVisually-module__root___CwnlX">17 hours 10 minutes</div><div class="css-1myv4yh" style="width: 100%; position: relative;"><hr class="Divider-module__root___PSOwi Divider-module__root--vertical-false___zS2cP css-5xx381"></div><div data-testid="flight_card_segment_stops_0" class="Text-module__root--variant-small_1___+fbYj css-ylq2vz">Direct</div></div><div class="css-1yl6p1k" style="text-align: right;"><div data-testid="flight_card_segment_destination_time_0" class="Text-module__root--variant-strong_1___SNYxf">07:50</div><div class="css-yyi517"><div data-testid="flight_card_segment_destination_airport_0" class="Text-module__root--variant-small_1___+fbYj">SIN</div><div class="Text-module__root--variant-small_1___+fbYj css-1n4sh5k"> . </div><div data-testid="flight_card_segment_destination_date_0" class="Text-module__root--variant-small_1___+fbYj">16 Oct</div></div></div></div></div></div></div><div class="css-13z7c5r"></div><div class="css-1dimx8f"><div class="css-17m9lv6" style="flex-wrap: wrap;"><div class="css-17m9lv6" style="flex-wrap: wrap;"><div data-testid="flight_card_carrier_0" class="Text-module__root--variant-small_1___+fbYj">Singapore Airlines</div></div></div></div><div class="css-13ekbfz"><div class="css-1rgw82s"><div class="css-k456he"><div class="css-3gojea"><div class="css-3gojea" style="grid-area: row1 / col1 / span 2 / span 2; background-image: url(&quot;https://r-xx.bstatic.com/data/airlines_logo/SQ.png&quot;);"></div></div></div></div><div class="css-1oe9l2q"><div class="css-1niqckn"><div class="css-io4ta2"><div class="css-1yl6p1k" style="text-align: left;"><div data-testid="flight_card_segment_departure_time_1" class="Text-module__root--variant-strong_1___SNYxf">20:45</div><div class="css-5nu86q"><div data-testid="flight_card_segment_departure_airport_1" class="Text-module__root--variant-small_1___+fbYj">SIN</div><div class="Text-module__root--variant-small_1___+fbYj css-1n4sh5k"> . </div><div data-testid="flight_card_segment_departure_date_1" class="Text-module__root--variant-small_1___+fbYj">20 Oct</div></div></div><div class="css-1wnqz2m" style="width: 50%;"><div data-testid="flight_card_segment_duration_1" aria-hidden="true" class="Text-module__root--variant-small_1___+fbYj css-ylq2vz">15h 55m</div><div class="HiddenVisually-module__root___CwnlX">15 hours 55 minutes</div><div class="css-1myv4yh" style="width: 100%; position: relative;"><hr class="Divider-module__root___PSOwi Divider-module__root--vertical-false___zS2cP css-5xx381"></div><div data-testid="flight_card_segment_stops_1" class="Text-module__root--variant-small_1___+fbYj css-ylq2vz">Direct</div></div><div class="css-1yl6p1k" style="text-align: right;"><div data-testid="flight_card_segment_destination_time_1" class="Text-module__root--variant-strong_1___SNYxf">21:40</div><div class="css-yyi517"><div data-testid="flight_card_segment_destination_airport_1" class="Text-module__root--variant-small_1___+fbYj">LAX</div><div class="Text-module__root--variant-small_1___+fbYj css-1n4sh5k"> . </div><div data-testid="flight_card_segment_destination_date_1" class="Text-module__root--variant-small_1___+fbYj">20 Oct</div></div></div></div></div></div></div><div class="css-13z7c5r"></div><div class="css-1dimx8f"><div class="css-17m9lv6" style="flex-wrap: wrap;"><div class="css-17m9lv6" style="flex-wrap: wrap;"><div data-testid="flight_card_carrier_1" class="Text-module__root--variant-small_1___+fbYj">Singapore Airlines</div></div></div></div></div><div class="css-1lhjur2"><div><div class="css-k456he" style="margin-top: 0px;"><div class="css-1iubv4" style="padding-bottom: 8px;"><span class="Icon-module__root___tiYlo Icon-module__root--size-large___6DYLv" aria-hidden="true"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="m 15 12.75 H 9 C 8.036 12.755 7.255 13.536 7.25 14.5 v 4 c 0.005 0.964 0.786 1.745 1.75 1.75 h 6 c 0.964 -0.005 1.745 -0.786 1.75 -1.75 v -4 C 16.745 13.536 15.964 12.755 15 12.75 z m -6 1.5 h 6 c 0.138 0 0.25 0.112 0.25 0.25 v 0.62 h -6.5 V 14.5 c 0 -0.138 0.112 -0.25 0.25 -0.25 z m 6 4.5 H 9 c -0.138 0 -0.25 -0.112 -0.25 -0.25 v -1.88 h 3.5 v 0.26 a 0.75 0.75 0 0 0 1.5 0 v -0.26 h 1.5 v 1.88 c 0 0.138 -0.112 0.25 -0.25 0.25 z M 15.69 4.42 a 3.73 3.73 0 0 0 -7.38 0 C 6.219 4.958 4.755 6.84 4.75 9 v 11.5 c 0 1.243 1.007 2.25 2.25 2.25 h 10 c 1.243 0 2.25 -1.007 2.25 -2.25 V 9 C 19.245 6.84 17.781 4.958 15.69 4.42 z M 12 2.75 c 0.95 0.002 1.796 0.603 2.11 1.5 H 9.89 C 10.204 3.353 11.05 2.752 12 2.75 z m 5.75 17.75 c -0.005 0.412 -0.338 0.745 -0.75 0.75 H 7 C 6.588 21.245 6.255 20.912 6.25 20.5 V 9 C 6.255 7.207 7.707 5.755 9.5 5.75 h 5 c 1.793 0.005 3.245 1.457 3.25 3.25 z"></path></svg></span><span class="Icon-module__root___tiYlo Icon-module__root--size-large___6DYLv" aria-hidden="true"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="m 15 14.75 H 9 a 0.75 0.75 0 0 1 0 -1.5 h 6 a 0.75 0.75 0 0 1 0 1.5 z M 15.75 18 C 15.745 17.588 15.412 17.255 15 17.25 H 9 a 0.75 0.75 0 0 0 0 1.5 h 6 c 0.412 -0.005 0.745 -0.338 0.75 -0.75 z m 3 -6.5 v 9 c 0 1.243 -1.007 2.25 -2.25 2.25 h -0.75 v 0.5 a 0.75 0.75 0 0 1 -1.5 0 v -0.5 h -4.5 v 0.5 a 0.75 0.75 0 0 1 -1.5 0 v -0.5 H 7.5 c -1.243 0 -2.25 -1.007 -2.25 -2.25 v -9 c 0 -1.243 1.007 -2.25 2.25 -2.25 h 1.75 v -8 C 9.25 0.56 9.81 0 10.5 0 h 3 c 0.69 0 1.25 0.56 1.25 1.25 v 8 h 1.75 c 1.243 0 2.25 1.007 2.25 2.25 z m -8 -2.25 h 2.5 V 1.5 h -2.5 z m 6.5 2.25 C 17.245 11.088 16.912 10.755 16.5 10.75 h -9 C 7.088 10.755 6.755 11.088 6.75 11.5 v 9 c 0.005 0.412 0.338 0.745 0.75 0.75 h 9 c 0.412 -0.005 0.745 -0.338 0.75 -0.75 z"></path></svg></span><span class="Icon-module__root___tiYlo Icon-module__root--size-large___6DYLv" aria-hidden="true"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="m 15 9.25 H 9 a 0.75 0.75 0 0 1 0 -1.5 h 6 a 0.75 0.75 0 0 1 0 1.5 z M 15.75 13 C 15.745 12.588 15.412 12.255 15 12.25 H 9 a 0.75 0.75 0 0 0 0 1.5 h 6 c 0.412 -0.005 0.745 -0.338 0.75 -0.75 z m 0 4.5 C 15.745 17.088 15.412 16.755 15 16.75 H 9 a 0.75 0.75 0 0 0 0 1.5 h 6 c 0.412 -0.005 0.745 -0.338 0.75 -0.75 z m 4 -12 v 15 c 0 1.243 -1.007 2.25 -2.25 2.25 h -1.75 v 0.5 a 0.75 0.75 0 0 1 -1.5 0 v -0.5 h -4.5 v 0.5 a 0.75 0.75 0 0 1 -1.5 0 v -0.5 H 6.5 c -1.243 0 -2.25 -1.007 -2.25 -2.25 v -15 C 4.25 4.257 5.257 3.25 6.5 3.25 h 1.75 v -2 C 8.25 0.56 8.81 0 9.5 0 h 5 c 0.69 0 1.25 0.56 1.25 1.25 v 2 h 1.75 c 1.243 0 2.25 1.007 2.25 2.25 z m -10 -2.25 h 4.5 V 1.5 h -4.5 z m 8.5 2.25 C 18.245 5.088 17.912 4.755 17.5 4.75 h -11 C 6.088 4.755 5.755 5.088 5.75 5.5 v 15 c 0.005 0.412 0.338 0.745 0.75 0.75 h 11 c 0.412 -0.005 0.745 -0.338 0.75 -0.75 z"></path></svg></span></div><div class="css-1niqckn" style="margin-bottom: 16px;"><div class="css-1niqckn" style="display: block; color: rgb(89, 89, 89); text-align: end;"><div class="Text-module__root--variant-small_2___2owJY"><span>Included: </span><span><span>personal item, cabin bag, checked bag</span></span></div></div></div></div></div><div class="" style="text-align: right;"><div class="css-1niqckn"><div aria-label="$2,390.61 Total price for all travellers" class="css-yyi517"><div aria-hidden="true" data-test-id="flight_card_price_main_price" class="Title-module__root___YFagE css-1qm7m38 Title-module__root--variant-headline_3___QrjqY"><div class="Text-module__root--variant-headline_3___7x4vh Text-module__root--color-neutral___dV7Ia Title-module__title___R8jbF"><div class="css-vxcmzt">$2,391</div></div></div></div><div aria-hidden="true" data-test-id="flight_card_price_total_price" class="Text-module__root--variant-small_1___+fbYj css-3estlk">Total price for all travellers</div></div><button data-testid="flight_card_bound_select_flight" aria-describedby="flight-card-0" type="button" class="Actionable-module__root___o3y3+ Button-module__root___2Z2KR Button-module__root--variant-secondary___yqUtJ Button-module__root--size-medium___+UaTJ Button-module__root--wide-false___V33Sh Button-module__root--variant-secondary-action___wCvOr css-1nt3u54"><span class="Button-module__text___YLOOX">See flight</span></button></div></div></div></div></div></div>    
            trip_element_list = await page.query_selector_all('li[data-test-id="offer-listing"]')
            for index, trip_element in enumerate(trip_element_list):
                itinerary = Itinerary(self.city1_code, self.city2_code, travel_date, return_date)
                itinerary.city1_name = self.city1_name
                itinerary.city2_name = self.city2_name

                travel_result: Result = await self.get_travel_iternity(trip_element)
                itinerary.price = travel_result.price
                itinerary.travel_airlines = travel_result.airlines_name
                itinerary.travel_start_time = travel_result.start_time
                itinerary.travel_end_time = travel_result.end_time
                self.itinerary_list.append(itinerary)

            await browser.close()

            return_url = 'https://www.expedia.com/Flights-Search?flight-type=on&leg1=from:' + c2 + ',to:' + c1
            return_url += ',departure:' + r1 + 'TANYT' + '&mode=search&options=cabinclass:economy&passengers=adults:1,infantinlap:N&trip=oneway'
            return_url += '&sortOrder=INCREASING&sortType=' + sort_by
            print(return_url)

            # Navigate to the URL you want to scrape
            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context()
            page = await context.new_page()
            await page.goto(return_url, timeout=0)
            html_text = await page.content()

            # <div class="css-209ldq"><div id="flight-card-0"><div class="Box-module__root___Hr7Gv Box-module__root--background-color-elevation_one___QasI2 Box-module__root--border-color-neutral_alt___JbiyK Box-module__root--border-width-100___9-Izb Box-module__root--border-radius-200___db4tG Box-module__root--overflow-hidden___3GhcK" style="--bui_box_padding--s: 0;"><div class="css-4o3ibe"><div class="css-v2mveg" style="width: 64%;"><div class="css-13ekbfz"><div class="css-1rgw82s"><div class="css-k456he"><div class="css-3gojea"><div class="css-3gojea" style="grid-area: row1 / col1 / span 2 / span 2; background-image: url(&quot;https://r-xx.bstatic.com/data/airlines_logo/SQ.png&quot;);"></div></div></div></div><div class="css-1oe9l2q"><div class="css-1niqckn"><div class="css-io4ta2"><div class="css-1yl6p1k" style="text-align: left;"><div data-testid="flight_card_segment_departure_time_0" class="Text-module__root--variant-strong_1___SNYxf">23:40</div><div class="css-5nu86q"><div data-testid="flight_card_segment_departure_airport_0" class="Text-module__root--variant-small_1___+fbYj">LAX</div><div class="Text-module__root--variant-small_1___+fbYj css-1n4sh5k"> . </div><div data-testid="flight_card_segment_departure_date_0" class="Text-module__root--variant-small_1___+fbYj">14 Oct</div></div></div><div class="css-1wnqz2m" style="width: 50%;"><div data-testid="flight_card_segment_duration_0" aria-hidden="true" class="Text-module__root--variant-small_1___+fbYj css-ylq2vz">17h 10m</div><div class="HiddenVisually-module__root___CwnlX">17 hours 10 minutes</div><div class="css-1myv4yh" style="width: 100%; position: relative;"><hr class="Divider-module__root___PSOwi Divider-module__root--vertical-false___zS2cP css-5xx381"></div><div data-testid="flight_card_segment_stops_0" class="Text-module__root--variant-small_1___+fbYj css-ylq2vz">Direct</div></div><div class="css-1yl6p1k" style="text-align: right;"><div data-testid="flight_card_segment_destination_time_0" class="Text-module__root--variant-strong_1___SNYxf">07:50</div><div class="css-yyi517"><div data-testid="flight_card_segment_destination_airport_0" class="Text-module__root--variant-small_1___+fbYj">SIN</div><div class="Text-module__root--variant-small_1___+fbYj css-1n4sh5k"> . </div><div data-testid="flight_card_segment_destination_date_0" class="Text-module__root--variant-small_1___+fbYj">16 Oct</div></div></div></div></div></div></div><div class="css-13z7c5r"></div><div class="css-1dimx8f"><div class="css-17m9lv6" style="flex-wrap: wrap;"><div class="css-17m9lv6" style="flex-wrap: wrap;"><div data-testid="flight_card_carrier_0" class="Text-module__root--variant-small_1___+fbYj">Singapore Airlines</div></div></div></div><div class="css-13ekbfz"><div class="css-1rgw82s"><div class="css-k456he"><div class="css-3gojea"><div class="css-3gojea" style="grid-area: row1 / col1 / span 2 / span 2; background-image: url(&quot;https://r-xx.bstatic.com/data/airlines_logo/SQ.png&quot;);"></div></div></div></div><div class="css-1oe9l2q"><div class="css-1niqckn"><div class="css-io4ta2"><div class="css-1yl6p1k" style="text-align: left;"><div data-testid="flight_card_segment_departure_time_1" class="Text-module__root--variant-strong_1___SNYxf">20:45</div><div class="css-5nu86q"><div data-testid="flight_card_segment_departure_airport_1" class="Text-module__root--variant-small_1___+fbYj">SIN</div><div class="Text-module__root--variant-small_1___+fbYj css-1n4sh5k"> . </div><div data-testid="flight_card_segment_departure_date_1" class="Text-module__root--variant-small_1___+fbYj">20 Oct</div></div></div><div class="css-1wnqz2m" style="width: 50%;"><div data-testid="flight_card_segment_duration_1" aria-hidden="true" class="Text-module__root--variant-small_1___+fbYj css-ylq2vz">15h 55m</div><div class="HiddenVisually-module__root___CwnlX">15 hours 55 minutes</div><div class="css-1myv4yh" style="width: 100%; position: relative;"><hr class="Divider-module__root___PSOwi Divider-module__root--vertical-false___zS2cP css-5xx381"></div><div data-testid="flight_card_segment_stops_1" class="Text-module__root--variant-small_1___+fbYj css-ylq2vz">Direct</div></div><div class="css-1yl6p1k" style="text-align: right;"><div data-testid="flight_card_segment_destination_time_1" class="Text-module__root--variant-strong_1___SNYxf">21:40</div><div class="css-yyi517"><div data-testid="flight_card_segment_destination_airport_1" class="Text-module__root--variant-small_1___+fbYj">LAX</div><div class="Text-module__root--variant-small_1___+fbYj css-1n4sh5k"> . </div><div data-testid="flight_card_segment_destination_date_1" class="Text-module__root--variant-small_1___+fbYj">20 Oct</div></div></div></div></div></div></div><div class="css-13z7c5r"></div><div class="css-1dimx8f"><div class="css-17m9lv6" style="flex-wrap: wrap;"><div class="css-17m9lv6" style="flex-wrap: wrap;"><div data-testid="flight_card_carrier_1" class="Text-module__root--variant-small_1___+fbYj">Singapore Airlines</div></div></div></div></div><div class="css-1lhjur2"><div><div class="css-k456he" style="margin-top: 0px;"><div class="css-1iubv4" style="padding-bottom: 8px;"><span class="Icon-module__root___tiYlo Icon-module__root--size-large___6DYLv" aria-hidden="true"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="m 15 12.75 H 9 C 8.036 12.755 7.255 13.536 7.25 14.5 v 4 c 0.005 0.964 0.786 1.745 1.75 1.75 h 6 c 0.964 -0.005 1.745 -0.786 1.75 -1.75 v -4 C 16.745 13.536 15.964 12.755 15 12.75 z m -6 1.5 h 6 c 0.138 0 0.25 0.112 0.25 0.25 v 0.62 h -6.5 V 14.5 c 0 -0.138 0.112 -0.25 0.25 -0.25 z m 6 4.5 H 9 c -0.138 0 -0.25 -0.112 -0.25 -0.25 v -1.88 h 3.5 v 0.26 a 0.75 0.75 0 0 0 1.5 0 v -0.26 h 1.5 v 1.88 c 0 0.138 -0.112 0.25 -0.25 0.25 z M 15.69 4.42 a 3.73 3.73 0 0 0 -7.38 0 C 6.219 4.958 4.755 6.84 4.75 9 v 11.5 c 0 1.243 1.007 2.25 2.25 2.25 h 10 c 1.243 0 2.25 -1.007 2.25 -2.25 V 9 C 19.245 6.84 17.781 4.958 15.69 4.42 z M 12 2.75 c 0.95 0.002 1.796 0.603 2.11 1.5 H 9.89 C 10.204 3.353 11.05 2.752 12 2.75 z m 5.75 17.75 c -0.005 0.412 -0.338 0.745 -0.75 0.75 H 7 C 6.588 21.245 6.255 20.912 6.25 20.5 V 9 C 6.255 7.207 7.707 5.755 9.5 5.75 h 5 c 1.793 0.005 3.245 1.457 3.25 3.25 z"></path></svg></span><span class="Icon-module__root___tiYlo Icon-module__root--size-large___6DYLv" aria-hidden="true"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="m 15 14.75 H 9 a 0.75 0.75 0 0 1 0 -1.5 h 6 a 0.75 0.75 0 0 1 0 1.5 z M 15.75 18 C 15.745 17.588 15.412 17.255 15 17.25 H 9 a 0.75 0.75 0 0 0 0 1.5 h 6 c 0.412 -0.005 0.745 -0.338 0.75 -0.75 z m 3 -6.5 v 9 c 0 1.243 -1.007 2.25 -2.25 2.25 h -0.75 v 0.5 a 0.75 0.75 0 0 1 -1.5 0 v -0.5 h -4.5 v 0.5 a 0.75 0.75 0 0 1 -1.5 0 v -0.5 H 7.5 c -1.243 0 -2.25 -1.007 -2.25 -2.25 v -9 c 0 -1.243 1.007 -2.25 2.25 -2.25 h 1.75 v -8 C 9.25 0.56 9.81 0 10.5 0 h 3 c 0.69 0 1.25 0.56 1.25 1.25 v 8 h 1.75 c 1.243 0 2.25 1.007 2.25 2.25 z m -8 -2.25 h 2.5 V 1.5 h -2.5 z m 6.5 2.25 C 17.245 11.088 16.912 10.755 16.5 10.75 h -9 C 7.088 10.755 6.755 11.088 6.75 11.5 v 9 c 0.005 0.412 0.338 0.745 0.75 0.75 h 9 c 0.412 -0.005 0.745 -0.338 0.75 -0.75 z"></path></svg></span><span class="Icon-module__root___tiYlo Icon-module__root--size-large___6DYLv" aria-hidden="true"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="m 15 9.25 H 9 a 0.75 0.75 0 0 1 0 -1.5 h 6 a 0.75 0.75 0 0 1 0 1.5 z M 15.75 13 C 15.745 12.588 15.412 12.255 15 12.25 H 9 a 0.75 0.75 0 0 0 0 1.5 h 6 c 0.412 -0.005 0.745 -0.338 0.75 -0.75 z m 0 4.5 C 15.745 17.088 15.412 16.755 15 16.75 H 9 a 0.75 0.75 0 0 0 0 1.5 h 6 c 0.412 -0.005 0.745 -0.338 0.75 -0.75 z m 4 -12 v 15 c 0 1.243 -1.007 2.25 -2.25 2.25 h -1.75 v 0.5 a 0.75 0.75 0 0 1 -1.5 0 v -0.5 h -4.5 v 0.5 a 0.75 0.75 0 0 1 -1.5 0 v -0.5 H 6.5 c -1.243 0 -2.25 -1.007 -2.25 -2.25 v -15 C 4.25 4.257 5.257 3.25 6.5 3.25 h 1.75 v -2 C 8.25 0.56 8.81 0 9.5 0 h 5 c 0.69 0 1.25 0.56 1.25 1.25 v 2 h 1.75 c 1.243 0 2.25 1.007 2.25 2.25 z m -10 -2.25 h 4.5 V 1.5 h -4.5 z m 8.5 2.25 C 18.245 5.088 17.912 4.755 17.5 4.75 h -11 C 6.088 4.755 5.755 5.088 5.75 5.5 v 15 c 0.005 0.412 0.338 0.745 0.75 0.75 h 11 c 0.412 -0.005 0.745 -0.338 0.75 -0.75 z"></path></svg></span></div><div class="css-1niqckn" style="margin-bottom: 16px;"><div class="css-1niqckn" style="display: block; color: rgb(89, 89, 89); text-align: end;"><div class="Text-module__root--variant-small_2___2owJY"><span>Included: </span><span><span>personal item, cabin bag, checked bag</span></span></div></div></div></div></div><div class="" style="text-align: right;"><div class="css-1niqckn"><div aria-label="$2,390.61 Total price for all travellers" class="css-yyi517"><div aria-hidden="true" data-test-id="flight_card_price_main_price" class="Title-module__root___YFagE css-1qm7m38 Title-module__root--variant-headline_3___QrjqY"><div class="Text-module__root--variant-headline_3___7x4vh Text-module__root--color-neutral___dV7Ia Title-module__title___R8jbF"><div class="css-vxcmzt">$2,391</div></div></div></div><div aria-hidden="true" data-test-id="flight_card_price_total_price" class="Text-module__root--variant-small_1___+fbYj css-3estlk">Total price for all travellers</div></div><button data-testid="flight_card_bound_select_flight" aria-describedby="flight-card-0" type="button" class="Actionable-module__root___o3y3+ Button-module__root___2Z2KR Button-module__root--variant-secondary___yqUtJ Button-module__root--size-medium___+UaTJ Button-module__root--wide-false___V33Sh Button-module__root--variant-secondary-action___wCvOr css-1nt3u54"><span class="Button-module__text___YLOOX">See flight</span></button></div></div></div></div></div></div>
            trip_element_list = await page.query_selector_all('li[data-test-id="offer-listing"]')
            for index, itinerary in enumerate(self.itinerary_list):
                try:
                    trip_element = trip_element_list[index]
                    return_result: Result = await self.get_travel_iternity(trip_element)
                    amount1 = int(itinerary.price[1:].replace(",", ""))
                    amount2 = int(return_result.price[1:].replace(",", ""))
                    itinerary.price = f"${amount1 + amount2}"
                    itinerary.return_airlines = return_result.airlines_name
                    itinerary.return_start_time = return_result.start_time
                    itinerary.return_end_time = return_result.end_time
                except IndexError as e:
                    # Handle the exception and print its details
                    print(f"An error occurred: {e}")
                    # Remove remaining items in the list to match the given data
                    self.itinerary_list = self.itinerary_list[:index]
                    # Break the for loop
                    break

            await self.save_itinerary_to_json(json_folder_name, sort_by)
            await browser.close()


# Run the asynchronous scraping function
if __name__ == "__main__":
    city1 = 'LAX'
    city2 = 'SIN'
    travel_date = '11/1/2023'
    return_date = '11/8/2023'
    json_folder_name = 'expedia'
    expedia = Expedia(city1_code=city1, city2_code=city2, travel_date=travel_date, return_date=return_date)
    sort_by_cheapest = 'CHEAPEST'
    sort_by_fastest = 'DURATION'
    asyncio.run(expedia.scrape_website(json_folder_name, sort_by_fastest))
