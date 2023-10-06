import asyncio
from scraper import Scraper
from scraper import Itinerary
from playwright.async_api import async_playwright
import json
import csv
from typing import List
import datetime
import re
import time
import os


class Booking(Scraper):       


            
    async def getTrip(self,trip_element):
        
        # <div class="css-13ekbfz"><div class="css-1rgw82s"><div class="css-k456he"><div class="css-3gojea"><div class="css-3gojea" style="grid-area: row1 / col1 / span 2 / span 2; background-image: url(&quot;https://r-xx.bstatic.com/data/airlines_logo/SQ.png&quot;);"></div></div></div></div><div class="css-1oe9l2q"><div class="css-1niqckn"><div class="css-io4ta2"><div class="css-1yl6p1k" style="text-align: left;"><div data-testid="flight_card_segment_departure_time_0" class="Text-module__root--variant-strong_1___SNYxf">23:40</div><div class="css-5nu86q"><div data-testid="flight_card_segment_departure_airport_0" class="Text-module__root--variant-small_1___+fbYj">LAX</div><div class="Text-module__root--variant-small_1___+fbYj css-1n4sh5k"> . </div><div data-testid="flight_card_segment_departure_date_0" class="Text-module__root--variant-small_1___+fbYj">14 Oct</div></div></div><div class="css-1wnqz2m" style="width: 50%;"><div data-testid="flight_card_segment_duration_0" aria-hidden="true" class="Text-module__root--variant-small_1___+fbYj css-ylq2vz">17h 10m</div><div class="HiddenVisually-module__root___CwnlX">17 hours 10 minutes</div><div class="css-1myv4yh" style="width: 100%; position: relative;"><hr class="Divider-module__root___PSOwi Divider-module__root--vertical-false___zS2cP css-5xx381"></div><div data-testid="flight_card_segment_stops_0" class="Text-module__root--variant-small_1___+fbYj css-ylq2vz">Direct</div></div><div class="css-1yl6p1k" style="text-align: right;"><div data-testid="flight_card_segment_destination_time_0" class="Text-module__root--variant-strong_1___SNYxf">07:50</div><div class="css-yyi517"><div data-testid="flight_card_segment_destination_airport_0" class="Text-module__root--variant-small_1___+fbYj">SIN</div><div class="Text-module__root--variant-small_1___+fbYj css-1n4sh5k"> . </div><div data-testid="flight_card_segment_destination_date_0" class="Text-module__root--variant-small_1___+fbYj">16 Oct</div></div></div></div></div></div></div>
                
        # <div data-testid="flight_card_segment_departure_time_0" class="Text-module__root--variant-strong_1___SNYxf">23:40</div>
        # <div data-testid="flight_card_segment_destination_time_0" class="Text-module__root--variant-strong_1___SNYxf">07:50</div>
        time_city_element_list = await trip_element.query_selector_all('div.Text-module__root--variant-strong_1___SNYxf')
        
        time_element = time_city_element_list[0]
        start_time = await time_element.inner_text()
        print('start_time', start_time)
        # city_element = time_city_element_list[1]
        # start_city = await city_element.inner_text()
        # print('start_city',start_city)
        
        time_element = time_city_element_list[1]
        end_time = await time_element.inner_text()
        end_time = end_time.split('+')[0]
        end_time = end_time.split('-')[0]
        print('end_time', end_time)
        # city_element = time_city_element_list[1]
        # end_city = await city_element.inner_text()
        # print('end_city',end_city)
        return start_time, end_time 


    #write a code for         

    async def scrape_website(self,json_folder_name:str,sort_by:str='bestflight_a'):
        async with async_playwright() as p:
            # Launch a Chromium browser instance
            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context()
            page = await context.new_page()
            c1 = self.city1_code
            c2 = self.city2_code 
            t1 = self.travel_date
            r1 = self.return_date
            url = 'https://www.skyscanner.com/transport/flights/'+ c1 +'/' + c2 +'/'+ t1+'/'+r1+'/?''adultsv2=1&cabinclass=economy&childrenv2=&inboundaltsenabled=false&outboundaltsenabled=false&preferdirects=false&ref=home&rtn=1'
            url = 'https://www.kayak.com/flights/'+ c1 +'-'+ c2 +'/'+ t1 + '/' + r1 + '?fs=fdDir=true;stops=~0&sort=' + sort_by
            
            c1 = c1 +'.AIRPORT'
            c2 = c2 + '.AIRPORT' 
            url = 'https://flights.booking.com/flights/'+ c1 +'-'+ c2 +'/'+'?type=ROUNDTRIP&adults=1&cabinClass=ECONOMY&children=&from='+ c1+'&to='+c2+'&stops=0&depart='+t1+'&return='+r1+'&sort='+ sort_by
            print(url)
        
            # Navigate to the URL you want to scrape
            await page.goto(url,timeout=0)
            # await page.goto('https://www.kayak.com/flights/MAA-SIN/2023-10-29/2023-11-05?fs=fdDir=true;stops=~0&sort=bestflight_a')
            html_text = await page.content()
            # print(html_text)
            # <div class="css-209ldq"><div id="flight-card-0"><div class="Box-module__root___Hr7Gv Box-module__root--background-color-elevation_one___QasI2 Box-module__root--border-color-neutral_alt___JbiyK Box-module__root--border-width-100___9-Izb Box-module__root--border-radius-200___db4tG Box-module__root--overflow-hidden___3GhcK" style="--bui_box_padding--s: 0;"><div class="css-4o3ibe"><div class="css-v2mveg" style="width: 64%;"><div class="css-13ekbfz"><div class="css-1rgw82s"><div class="css-k456he"><div class="css-3gojea"><div class="css-3gojea" style="grid-area: row1 / col1 / span 2 / span 2; background-image: url(&quot;https://r-xx.bstatic.com/data/airlines_logo/SQ.png&quot;);"></div></div></div></div><div class="css-1oe9l2q"><div class="css-1niqckn"><div class="css-io4ta2"><div class="css-1yl6p1k" style="text-align: left;"><div data-testid="flight_card_segment_departure_time_0" class="Text-module__root--variant-strong_1___SNYxf">23:40</div><div class="css-5nu86q"><div data-testid="flight_card_segment_departure_airport_0" class="Text-module__root--variant-small_1___+fbYj">LAX</div><div class="Text-module__root--variant-small_1___+fbYj css-1n4sh5k"> . </div><div data-testid="flight_card_segment_departure_date_0" class="Text-module__root--variant-small_1___+fbYj">14 Oct</div></div></div><div class="css-1wnqz2m" style="width: 50%;"><div data-testid="flight_card_segment_duration_0" aria-hidden="true" class="Text-module__root--variant-small_1___+fbYj css-ylq2vz">17h 10m</div><div class="HiddenVisually-module__root___CwnlX">17 hours 10 minutes</div><div class="css-1myv4yh" style="width: 100%; position: relative;"><hr class="Divider-module__root___PSOwi Divider-module__root--vertical-false___zS2cP css-5xx381"></div><div data-testid="flight_card_segment_stops_0" class="Text-module__root--variant-small_1___+fbYj css-ylq2vz">Direct</div></div><div class="css-1yl6p1k" style="text-align: right;"><div data-testid="flight_card_segment_destination_time_0" class="Text-module__root--variant-strong_1___SNYxf">07:50</div><div class="css-yyi517"><div data-testid="flight_card_segment_destination_airport_0" class="Text-module__root--variant-small_1___+fbYj">SIN</div><div class="Text-module__root--variant-small_1___+fbYj css-1n4sh5k"> . </div><div data-testid="flight_card_segment_destination_date_0" class="Text-module__root--variant-small_1___+fbYj">16 Oct</div></div></div></div></div></div></div><div class="css-13z7c5r"></div><div class="css-1dimx8f"><div class="css-17m9lv6" style="flex-wrap: wrap;"><div class="css-17m9lv6" style="flex-wrap: wrap;"><div data-testid="flight_card_carrier_0" class="Text-module__root--variant-small_1___+fbYj">Singapore Airlines</div></div></div></div><div class="css-13ekbfz"><div class="css-1rgw82s"><div class="css-k456he"><div class="css-3gojea"><div class="css-3gojea" style="grid-area: row1 / col1 / span 2 / span 2; background-image: url(&quot;https://r-xx.bstatic.com/data/airlines_logo/SQ.png&quot;);"></div></div></div></div><div class="css-1oe9l2q"><div class="css-1niqckn"><div class="css-io4ta2"><div class="css-1yl6p1k" style="text-align: left;"><div data-testid="flight_card_segment_departure_time_1" class="Text-module__root--variant-strong_1___SNYxf">20:45</div><div class="css-5nu86q"><div data-testid="flight_card_segment_departure_airport_1" class="Text-module__root--variant-small_1___+fbYj">SIN</div><div class="Text-module__root--variant-small_1___+fbYj css-1n4sh5k"> . </div><div data-testid="flight_card_segment_departure_date_1" class="Text-module__root--variant-small_1___+fbYj">20 Oct</div></div></div><div class="css-1wnqz2m" style="width: 50%;"><div data-testid="flight_card_segment_duration_1" aria-hidden="true" class="Text-module__root--variant-small_1___+fbYj css-ylq2vz">15h 55m</div><div class="HiddenVisually-module__root___CwnlX">15 hours 55 minutes</div><div class="css-1myv4yh" style="width: 100%; position: relative;"><hr class="Divider-module__root___PSOwi Divider-module__root--vertical-false___zS2cP css-5xx381"></div><div data-testid="flight_card_segment_stops_1" class="Text-module__root--variant-small_1___+fbYj css-ylq2vz">Direct</div></div><div class="css-1yl6p1k" style="text-align: right;"><div data-testid="flight_card_segment_destination_time_1" class="Text-module__root--variant-strong_1___SNYxf">21:40</div><div class="css-yyi517"><div data-testid="flight_card_segment_destination_airport_1" class="Text-module__root--variant-small_1___+fbYj">LAX</div><div class="Text-module__root--variant-small_1___+fbYj css-1n4sh5k"> . </div><div data-testid="flight_card_segment_destination_date_1" class="Text-module__root--variant-small_1___+fbYj">20 Oct</div></div></div></div></div></div></div><div class="css-13z7c5r"></div><div class="css-1dimx8f"><div class="css-17m9lv6" style="flex-wrap: wrap;"><div class="css-17m9lv6" style="flex-wrap: wrap;"><div data-testid="flight_card_carrier_1" class="Text-module__root--variant-small_1___+fbYj">Singapore Airlines</div></div></div></div></div><div class="css-1lhjur2"><div><div class="css-k456he" style="margin-top: 0px;"><div class="css-1iubv4" style="padding-bottom: 8px;"><span class="Icon-module__root___tiYlo Icon-module__root--size-large___6DYLv" aria-hidden="true"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="m 15 12.75 H 9 C 8.036 12.755 7.255 13.536 7.25 14.5 v 4 c 0.005 0.964 0.786 1.745 1.75 1.75 h 6 c 0.964 -0.005 1.745 -0.786 1.75 -1.75 v -4 C 16.745 13.536 15.964 12.755 15 12.75 z m -6 1.5 h 6 c 0.138 0 0.25 0.112 0.25 0.25 v 0.62 h -6.5 V 14.5 c 0 -0.138 0.112 -0.25 0.25 -0.25 z m 6 4.5 H 9 c -0.138 0 -0.25 -0.112 -0.25 -0.25 v -1.88 h 3.5 v 0.26 a 0.75 0.75 0 0 0 1.5 0 v -0.26 h 1.5 v 1.88 c 0 0.138 -0.112 0.25 -0.25 0.25 z M 15.69 4.42 a 3.73 3.73 0 0 0 -7.38 0 C 6.219 4.958 4.755 6.84 4.75 9 v 11.5 c 0 1.243 1.007 2.25 2.25 2.25 h 10 c 1.243 0 2.25 -1.007 2.25 -2.25 V 9 C 19.245 6.84 17.781 4.958 15.69 4.42 z M 12 2.75 c 0.95 0.002 1.796 0.603 2.11 1.5 H 9.89 C 10.204 3.353 11.05 2.752 12 2.75 z m 5.75 17.75 c -0.005 0.412 -0.338 0.745 -0.75 0.75 H 7 C 6.588 21.245 6.255 20.912 6.25 20.5 V 9 C 6.255 7.207 7.707 5.755 9.5 5.75 h 5 c 1.793 0.005 3.245 1.457 3.25 3.25 z"></path></svg></span><span class="Icon-module__root___tiYlo Icon-module__root--size-large___6DYLv" aria-hidden="true"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="m 15 14.75 H 9 a 0.75 0.75 0 0 1 0 -1.5 h 6 a 0.75 0.75 0 0 1 0 1.5 z M 15.75 18 C 15.745 17.588 15.412 17.255 15 17.25 H 9 a 0.75 0.75 0 0 0 0 1.5 h 6 c 0.412 -0.005 0.745 -0.338 0.75 -0.75 z m 3 -6.5 v 9 c 0 1.243 -1.007 2.25 -2.25 2.25 h -0.75 v 0.5 a 0.75 0.75 0 0 1 -1.5 0 v -0.5 h -4.5 v 0.5 a 0.75 0.75 0 0 1 -1.5 0 v -0.5 H 7.5 c -1.243 0 -2.25 -1.007 -2.25 -2.25 v -9 c 0 -1.243 1.007 -2.25 2.25 -2.25 h 1.75 v -8 C 9.25 0.56 9.81 0 10.5 0 h 3 c 0.69 0 1.25 0.56 1.25 1.25 v 8 h 1.75 c 1.243 0 2.25 1.007 2.25 2.25 z m -8 -2.25 h 2.5 V 1.5 h -2.5 z m 6.5 2.25 C 17.245 11.088 16.912 10.755 16.5 10.75 h -9 C 7.088 10.755 6.755 11.088 6.75 11.5 v 9 c 0.005 0.412 0.338 0.745 0.75 0.75 h 9 c 0.412 -0.005 0.745 -0.338 0.75 -0.75 z"></path></svg></span><span class="Icon-module__root___tiYlo Icon-module__root--size-large___6DYLv" aria-hidden="true"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="m 15 9.25 H 9 a 0.75 0.75 0 0 1 0 -1.5 h 6 a 0.75 0.75 0 0 1 0 1.5 z M 15.75 13 C 15.745 12.588 15.412 12.255 15 12.25 H 9 a 0.75 0.75 0 0 0 0 1.5 h 6 c 0.412 -0.005 0.745 -0.338 0.75 -0.75 z m 0 4.5 C 15.745 17.088 15.412 16.755 15 16.75 H 9 a 0.75 0.75 0 0 0 0 1.5 h 6 c 0.412 -0.005 0.745 -0.338 0.75 -0.75 z m 4 -12 v 15 c 0 1.243 -1.007 2.25 -2.25 2.25 h -1.75 v 0.5 a 0.75 0.75 0 0 1 -1.5 0 v -0.5 h -4.5 v 0.5 a 0.75 0.75 0 0 1 -1.5 0 v -0.5 H 6.5 c -1.243 0 -2.25 -1.007 -2.25 -2.25 v -15 C 4.25 4.257 5.257 3.25 6.5 3.25 h 1.75 v -2 C 8.25 0.56 8.81 0 9.5 0 h 5 c 0.69 0 1.25 0.56 1.25 1.25 v 2 h 1.75 c 1.243 0 2.25 1.007 2.25 2.25 z m -10 -2.25 h 4.5 V 1.5 h -4.5 z m 8.5 2.25 C 18.245 5.088 17.912 4.755 17.5 4.75 h -11 C 6.088 4.755 5.755 5.088 5.75 5.5 v 15 c 0.005 0.412 0.338 0.745 0.75 0.75 h 11 c 0.412 -0.005 0.745 -0.338 0.75 -0.75 z"></path></svg></span></div><div class="css-1niqckn" style="margin-bottom: 16px;"><div class="css-1niqckn" style="display: block; color: rgb(89, 89, 89); text-align: end;"><div class="Text-module__root--variant-small_2___2owJY"><span>Included: </span><span><span>personal item, cabin bag, checked bag</span></span></div></div></div></div></div><div class="" style="text-align: right;"><div class="css-1niqckn"><div aria-label="$2,390.61 Total price for all travellers" class="css-yyi517"><div aria-hidden="true" data-test-id="flight_card_price_main_price" class="Title-module__root___YFagE css-1qm7m38 Title-module__root--variant-headline_3___QrjqY"><div class="Text-module__root--variant-headline_3___7x4vh Text-module__root--color-neutral___dV7Ia Title-module__title___R8jbF"><div class="css-vxcmzt">$2,391</div></div></div></div><div aria-hidden="true" data-test-id="flight_card_price_total_price" class="Text-module__root--variant-small_1___+fbYj css-3estlk">Total price for all travellers</div></div><button data-testid="flight_card_bound_select_flight" aria-describedby="flight-card-0" type="button" class="Actionable-module__root___o3y3+ Button-module__root___2Z2KR Button-module__root--variant-secondary___yqUtJ Button-module__root--size-medium___+UaTJ Button-module__root--wide-false___V33Sh Button-module__root--variant-secondary-action___wCvOr css-1nt3u54"><span class="Button-module__text___YLOOX">See flight</span></button></div></div></div></div></div></div>    
            trip_element_list = await page.query_selector_all('div.css-209ldq')
            for index,trip_element in enumerate(trip_element_list):
                itinerary = Itinerary(self.city1_code,self.city2_code,self.travel_date,self.return_date)
                itinerary.city1_name = self.city1_name
                itinerary.city2_name = self.city2_name
                #Get price 
                # <div class="css-vxcmzt">$2,391</div>
                price = await trip_element.query_selector('div.css-vxcmzt')
                if price == None:
                    continue
                price_text = await price.inner_text()
                print("Price :",price_text)
                itinerary.price = price_text 

                # <div class="css-1dimx8f"><div class="css-17m9lv6" style="flex-wrap: wrap;"><div class="css-17m9lv6" style="flex-wrap: wrap;"><div data-testid="flight_card_carrier_0" class="Text-module__root--variant-small_1___+fbYj">Singapore Airlines</div></div></div></div>
                airlines_names  = await trip_element.query_selector_all("div.css-1dimx8f")  
                itinerary.travel_airlines = await airlines_names[0].inner_text()
                itinerary.return_airlines = await airlines_names[1].inner_text() 
                print('Travel Airlines ',itinerary.travel_airlines)
                print('Return Airlines ',itinerary.return_airlines)
                
                # <div class="css-13ekbfz"><div class="css-1rgw82s"><div class="css-k456he"><div class="css-3gojea"><div class="css-3gojea" style="grid-area: row1 / col1 / span 2 / span 2; background-image: url(&quot;https://r-xx.bstatic.com/data/airlines_logo/SQ.png&quot;);"></div></div></div></div><div class="css-1oe9l2q"><div class="css-1niqckn"><div class="css-io4ta2"><div class="css-1yl6p1k" style="text-align: left;"><div data-testid="flight_card_segment_departure_time_0" class="Text-module__root--variant-strong_1___SNYxf">23:40</div><div class="css-5nu86q"><div data-testid="flight_card_segment_departure_airport_0" class="Text-module__root--variant-small_1___+fbYj">LAX</div><div class="Text-module__root--variant-small_1___+fbYj css-1n4sh5k"> . </div><div data-testid="flight_card_segment_departure_date_0" class="Text-module__root--variant-small_1___+fbYj">14 Oct</div></div></div><div class="css-1wnqz2m" style="width: 50%;"><div data-testid="flight_card_segment_duration_0" aria-hidden="true" class="Text-module__root--variant-small_1___+fbYj css-ylq2vz">17h 10m</div><div class="HiddenVisually-module__root___CwnlX">17 hours 10 minutes</div><div class="css-1myv4yh" style="width: 100%; position: relative;"><hr class="Divider-module__root___PSOwi Divider-module__root--vertical-false___zS2cP css-5xx381"></div><div data-testid="flight_card_segment_stops_0" class="Text-module__root--variant-small_1___+fbYj css-ylq2vz">Direct</div></div><div class="css-1yl6p1k" style="text-align: right;"><div data-testid="flight_card_segment_destination_time_0" class="Text-module__root--variant-strong_1___SNYxf">07:50</div><div class="css-yyi517"><div data-testid="flight_card_segment_destination_airport_0" class="Text-module__root--variant-small_1___+fbYj">SIN</div><div class="Text-module__root--variant-small_1___+fbYj css-1n4sh5k"> . </div><div data-testid="flight_card_segment_destination_date_0" class="Text-module__root--variant-small_1___+fbYj">16 Oct</div></div></div></div></div></div></div>
                trips = await trip_element.query_selector_all("div.css-13ekbfz")
                
                itinerary.travel_start_time, itinerary.travel_end_time = await self.getTrip(trips[0]) 
                #Return Details
                itinerary.return_start_time, itinerary.return_end_time = await self.getTrip(trips[1]) 

                self.itinerary_list.append(itinerary)
            
            await self.save_itinerary_to_json(json_folder_name,sort_by)
            
            await page.content()
            await browser.close()

 

    
# Run the asynchronous scraping function
if __name__ == "__main__":
    city1 = 'LAX'
    city2 = 'SIN'
    travel_date = '2023-10-14'
    return_date = '2023-10-20'
    json_folder_name = 'booking'
    expedia = Booking(city1_code=city1, city2_code=city2, travel_date=travel_date, return_date=return_date)
    sort_by_cheapest = 'CHEAPEST'
    sort_by_fastest = 'DURATION'
    asyncio.run(expedia.scrape_website(json_folder_name, sort_by_fastest))
