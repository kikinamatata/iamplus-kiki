import asyncio
from playwright.async_api import async_playwright
import json
import csv
from typing import List
import datetime
import re
import time


class AirlinesTime:
    airlines_name:str
    start_time:str
    end_time:str 
    def __init__(self,airlines_name, start_time,end_time):
       self.airlines_name = airlines_name
       self.start_time = start_time
       self.end_time = end_time

class Itinerary:
    price:str 

    city1_code:str
    city2_code:str
    
    city1_name:str
    city2_name:str
    
    travel_date:str
    travel_airlines:str
    travel_start_time:str
    travel_end_time:str
    
    return_date:str
    return_airlines:str
    return_start_time:str
    return_end_time:str
    
    def __init__(self,city1_code, city2_code,travel_date,return_date):
       self.city1_code = city1_code
       self.city2_code = city2_code
       self.travel_date = travel_date
       self.return_date = return_date
    
    
    def to_json(self):
        print(self.price)
        # Create a dictionary representing the JSON node
        json_node = {
                    "price":self.price,
                    "airport1_code":self.city1_code,
                    "airport2_code":self.city2_code,  
                    "airport1_name":self.city1_name,
                    "airport2_name":self.city2_name,
                    "travel_date":self.travel_date,  
                    "return_date":self.return_date,    
                    "travel":{
                           "airlines":self.travel_airlines,
                           "start_time":self.travel_start_time,
                           "end_time":self.travel_end_time,
                    },
                    "return":{
                           "airlines":self.return_airlines,
                           "start_time":self.return_start_time,
                           "end_time":self.return_end_time,
                    },
                }
        return json_node 
       

itinerary_list:List[Itinerary] = []

# Save movie_list to a JSON file
json_file = "sky-scanner.json"

async def my_print(element,name):
          text = await element.inner_html()
          print (name, text)

            
# Function to save  instances to a JSON file
async def save_itinerary_to_json(file_prefix = 'Best'):
    file_prefix = file_prefix.lower()
    json_file = 'kayak-'+file_prefix+'.json'
    serialized_list = []
    for item in itinerary_list:
        serialized_list.append(item.to_json())
        # break
    with open(json_file, 'w') as json_file:
        json.dump(serialized_list, json_file, indent=4)      


            
async def getTrip(trip_element) -> AirlinesTime:
    # <div class="css-13ekbfz"><div class="css-1rgw82s"><div class="css-k456he"><div class="css-3gojea"><div class="css-3gojea" style="grid-area: row1 / col1 / span 2 / span 2; background-image: url(&quot;https://r-xx.bstatic.com/data/airlines_logo/SQ.png&quot;);"></div></div></div></div><div class="css-1oe9l2q"><div class="css-1niqckn"><div class="css-io4ta2"><div class="css-1yl6p1k" style="text-align: left;"><div data-testid="flight_card_segment_departure_time_0" class="Text-module__root--variant-strong_1___SNYxf">23:40</div><div class="css-5nu86q"><div data-testid="flight_card_segment_departure_airport_0" class="Text-module__root--variant-small_1___+fbYj">LAX</div><div class="Text-module__root--variant-small_1___+fbYj css-1n4sh5k"> . </div><div data-testid="flight_card_segment_departure_date_0" class="Text-module__root--variant-small_1___+fbYj">14 Oct</div></div></div><div class="css-1wnqz2m" style="width: 50%;"><div data-testid="flight_card_segment_duration_0" aria-hidden="true" class="Text-module__root--variant-small_1___+fbYj css-ylq2vz">17h 10m</div><div class="HiddenVisually-module__root___CwnlX">17 hours 10 minutes</div><div class="css-1myv4yh" style="width: 100%; position: relative;"><hr class="Divider-module__root___PSOwi Divider-module__root--vertical-false___zS2cP css-5xx381"></div><div data-testid="flight_card_segment_stops_0" class="Text-module__root--variant-small_1___+fbYj css-ylq2vz">Direct</div></div><div class="css-1yl6p1k" style="text-align: right;"><div data-testid="flight_card_segment_destination_time_0" class="Text-module__root--variant-strong_1___SNYxf">07:50</div><div class="css-yyi517"><div data-testid="flight_card_segment_destination_airport_0" class="Text-module__root--variant-small_1___+fbYj">SIN</div><div class="Text-module__root--variant-small_1___+fbYj css-1n4sh5k"> . </div><div data-testid="flight_card_segment_destination_date_0" class="Text-module__root--variant-small_1___+fbYj">16 Oct</div></div></div></div></div></div></div>

    # Name of Airlines
    # <div class="css-1dimx8f"><div class="css-17m9lv6" style="flex-wrap: wrap;"><div class="css-17m9lv6" style="flex-wrap: wrap;"><div data-testid="flight_card_carrier_0" class="Text-module__root--variant-small_1___+fbYj">Singapore Airlines</div></div></div></div>
    img_div_element = await trip_element.query_selector("div.css-1dimx8f")
    airlines = await img_div_element.inner_text()
    print ('Airlenes :',airlines)
#    <div class="vmXl vmXl-mod-variant-large" bis_skin_checked="1">
#       <span>11:40 pm</span>
#       <span class="aOlM"> – </span>
#       <span>7:50 am<sup class="VY2U-adendum" title="Flight lands the next day">+1</sup></span></div>

    time_city_element_list = await trip_element.query_selector_all('div.vmXl.vmXl-mod-variant-large > *')
    
    time_element = time_city_element_list[0]
    start_time = await time_element.inner_text()
    print('start_time', start_time)
    # city_element = time_city_element_list[1]
    # start_city = await city_element.inner_text()
    # print('start_city',start_city)
    
    time_element = time_city_element_list[2]
    end_time = await time_element.inner_text()
    end_time = end_time.split('+')[0]
    end_time = end_time.split('-')[0]
    print('end_time', end_time)
    # city_element = time_city_element_list[1]
    # end_city = await city_element.inner_text()
    # print('end_city',end_city)
    return AirlinesTime( airlines, start_time,end_time) 


 #write a code for         

async def skyscanner_scrape_website(city1_code,city2_code,travel_date,return_date,city1_name,city2_name,sort_by='bestflight_a'):
    async with async_playwright() as p:
        # Launch a Chromium browser instance
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        c1 = city1_code
        c2 = city2_code 
        t1 = travel_date
        r1 = return_date
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
            itinerary = Itinerary(city1_code,city2_code,travel_date,return_date)
            itinerary.city1_name = city1_name
            itinerary.city2_name = city2_name
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
            continue
        
            # <div class="css-13ekbfz"><div class="css-1rgw82s"><div class="css-k456he"><div class="css-3gojea"><div class="css-3gojea" style="grid-area: row1 / col1 / span 2 / span 2; background-image: url(&quot;https://r-xx.bstatic.com/data/airlines_logo/SQ.png&quot;);"></div></div></div></div><div class="css-1oe9l2q"><div class="css-1niqckn"><div class="css-io4ta2"><div class="css-1yl6p1k" style="text-align: left;"><div data-testid="flight_card_segment_departure_time_0" class="Text-module__root--variant-strong_1___SNYxf">23:40</div><div class="css-5nu86q"><div data-testid="flight_card_segment_departure_airport_0" class="Text-module__root--variant-small_1___+fbYj">LAX</div><div class="Text-module__root--variant-small_1___+fbYj css-1n4sh5k"> . </div><div data-testid="flight_card_segment_departure_date_0" class="Text-module__root--variant-small_1___+fbYj">14 Oct</div></div></div><div class="css-1wnqz2m" style="width: 50%;"><div data-testid="flight_card_segment_duration_0" aria-hidden="true" class="Text-module__root--variant-small_1___+fbYj css-ylq2vz">17h 10m</div><div class="HiddenVisually-module__root___CwnlX">17 hours 10 minutes</div><div class="css-1myv4yh" style="width: 100%; position: relative;"><hr class="Divider-module__root___PSOwi Divider-module__root--vertical-false___zS2cP css-5xx381"></div><div data-testid="flight_card_segment_stops_0" class="Text-module__root--variant-small_1___+fbYj css-ylq2vz">Direct</div></div><div class="css-1yl6p1k" style="text-align: right;"><div data-testid="flight_card_segment_destination_time_0" class="Text-module__root--variant-strong_1___SNYxf">07:50</div><div class="css-yyi517"><div data-testid="flight_card_segment_destination_airport_0" class="Text-module__root--variant-small_1___+fbYj">SIN</div><div class="Text-module__root--variant-small_1___+fbYj css-1n4sh5k"> . </div><div data-testid="flight_card_segment_destination_date_0" class="Text-module__root--variant-small_1___+fbYj">16 Oct</div></div></div></div></div></div></div>
            trips = await trip_element.query_selector_all("div.css-13ekbfz")
            for index, trip in enumerate(trips):
                print (index , await trip.text_content())
                # print(index,trip)
                print("Flight ",index)
                travel_details = await getTrip(trips[0]) 
                itinerary.travel_airlines = travel_details.airlines_name
                itinerary.travel_start_time = travel_details.start_time
                itinerary.travel_end_time = travel_details.end_time
                #Return Details
                return_details = await getTrip(trips[1]) 
                itinerary.return_airlines = return_details.airlines_name
                itinerary.return_start_time = return_details.start_time
                itinerary.return_end_time = return_details.end_time

            itinerary_list.append(itinerary)
        
        # await save_itinerary_to_json(sort_by)
        
        await page.content()
        await browser.close()

    
# Run the asynchronous scraping function
if __name__ == "__main__":
    airports_dict ={}
    # Step 1: Load JSON data from the file
    with open('airports_dict.json', 'r') as json_file:
        airports_dict = json.load(json_file)
    city1 = 'LAX'
    city2 = 'SIN'
    travel_date = '2023-10-14'
    return_date = '2023-10-20'
    city1_name = airports_dict[city1.upper()]
    city2_name = airports_dict[city2.upper()]
    sort_by_best ='BEST'
    sort_by_cheapest ='CHEAPEST'
    sort_by_fastest ='FASTEST'
    asyncio.run(skyscanner_scrape_website(city1,city2,travel_date,return_date,city1_name,city2_name,sort_by_best))
