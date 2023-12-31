import asyncio
from playwright.async_api import async_playwright
import json
import csv
from typing import List
import datetime
import re
import os




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

class AirlinesTime:
    airlines_name:str
    start_time:str
    end_time:str 
    def __init__(self,airlines_name, start_time,end_time):
       self.airlines_name = airlines_name
       self.start_time = start_time
       self.end_time = end_time

async def getTrip(trip_element) -> AirlinesTime:
    # Name of Airlines
    # <img src="https://content.r9cdn.net/rimg/provider-logos/airlines/v/SQ.png?crop=false&amp;width=108&amp;height=92&amp;fallback=default3.png&amp;_v=0ff33e55a8f21c7c3192f0394e8dfdb2" alt="Singapore Airlines">
    img_element = await trip_element.query_selector("img")
    airlines = await img_element.get_attribute("alt")
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


          
          
      
      
# Function to save  instances to a JSON file
async def save_itinerary_to_json(file_prefix = 'Best'):
    file_prefix = file_prefix.lower()
    # Define the folder path
    folder_path = "kayak"
    # Check if the folder exists, and if not, create it
    if not os.path.exists(folder_path):
     os.makedirs(folder_path)
    # Define the file path
    file_path = os.path.join(folder_path, folder_path +'-' + file_prefix+'.json')
    serialized_list = []
    for item in itinerary_list:
        serialized_list.append(item.to_json())
        # break
    with open(file_path, 'w') as json_file:
        json.dump(serialized_list, json_file, indent=4)      

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
        url = 'https://www.kayak.com/flights/'+ c1 +'-'+ c2 +'/'+ t1 + '/' + r1 + '?fs=fdDir=true;stops=~0&sort=' + sort_by
        print(url)
      
        # Navigate to the URL you want to scrape
        await page.goto(url)
        # await page.goto('https://www.kayak.com/flights/MAA-SIN/2023-10-29/2023-11-05?fs=fdDir=true;stops=~0&sort=bestflight_a')
        html_text = await page.content()
        print(html_text)
        
        trip_element_list = await page.query_selector_all('div.nrc6')
        for index,trip_element in enumerate(trip_element_list):
            itinerary = Itinerary(city1_code,city2_code,travel_date,return_date)
            itinerary.city1_name = city1_name
            itinerary.city2_name = city2_name
            #Get price 
            # <div class="f8F1-price-text" bis_skin_checked="1">$2,403</div>
            price = await trip_element.query_selector('div.f8F1-price-text')
            price_text = await price.inner_text()
            print("Price :",price_text)
            itinerary.price = price_text
            #<div class="UpperTicketBody_legsContainer__ZjcyZ" bis_skin_checked="1"><div class="LegDetails_container__MTkyZ UpperTicketBody_leg__MmNkN" aria-hidden="true" bis_skin_checked="1"><div class="LogoImage_container__MDU0Z LegLogo_logoContainer__ODdkM UpperTicketBody_legLogo__ZjYwM" bis_skin_checked="1"><div class="LegLogo_legImage__MmY0Z" bis_skin_checked="1"><div class="BpkImage_bpk-image__YTkyO BpkImage_bpk-image--no-background__NGMyN" style="height: 0px; padding-bottom: 50%;" bis_skin_checked="1"><img class="BpkImage_bpk-image__img__MDZkN" alt="United" src="//www.skyscanner.net/images/airlines/small/UA.png"></div></div></div><div class="LegInfo_legInfo__ZGMzY" bis_skin_checked="1"><div class="LegInfo_routePartialDepart__NzEwY" bis_skin_checked="1"><span class="BpkText_bpk-text__MWZkY BpkText_bpk-text--lg__NjNhN LegInfo_routePartialTime__OTFkN"><div bis_skin_checked="1"><span class="BpkText_bpk-text__MWZkY BpkText_bpk-text--label-1__NjBhY">8:15 AM</span></div></span><span class="BpkText_bpk-text__MWZkY BpkText_bpk-text--body-default__Y2M3Z"><div tabindex="0" aria-label="Los Angeles International, LAX, United States" bis_skin_checked="1"><span class="BpkText_bpk-text__MWZkY BpkText_bpk-text--body-default__Y2M3Z LegInfo_routePartialCityTooltip__NTE4Z">LAX</span></div></span></div><div class="LegInfo_stopsContainer__NWIyN" bis_skin_checked="1"><span class="BpkText_bpk-text__MWZkY BpkText_bpk-text--xs__ZDJmY Duration_duration__NmUyM">19h 30m</span><div class="LegInfo_stopLine__MzUxZ" bis_skin_checked="1"><span class="LegInfo_stopDot__ZTAyN"></span><svg xmlns="http://www.w3.org/2000/svg" xml:space="preserve" viewBox="0 0 12 12" class="LegInfo_planeEnd__ZDkxM"><path fill="#898294" d="M3.922 12h.499a.52.52 0 0 0 .444-.247L7.949 6.8l3.233-.019A.8.8 0 0 0 12 6a.8.8 0 0 0-.818-.781L7.949 5.2 4.866.246A.525.525 0 0 0 4.421 0h-.499a.523.523 0 0 0-.489.71L5.149 5.2H2.296l-.664-1.33a.523.523 0 0 0-.436-.288L0 3.509 1.097 6 0 8.491l1.196-.073a.523.523 0 0 0 .436-.288l.664-1.33h2.853l-1.716 4.49a.523.523 0 0 0 .489.71"></path></svg></div><div class="LegInfo_stopsLabelContainer__MmM0Z" bis_skin_checked="1"><span class="BpkText_bpk-text__MWZkY BpkText_bpk-text--xs__ZDJmY LegInfo_stopsLabelRed__NTY2Y">1 stop</span>&nbsp;<div class="LegInfo_stopsRow__MTUwZ" bis_skin_checked="1"><span class="BpkText_bpk-text__MWZkY BpkText_bpk-text--xs__ZDJmY LegInfo_stopStation__M2E5N"><div tabindex="0" aria-label="SFO" bis_skin_checked="1"><span class="BpkText_bpk-text__MWZkY BpkText_bpk-text--xs__ZDJmY">SFO</span></div></span></div></div></div><div class="LegInfo_routePartialArrive__Y2U1N" bis_skin_checked="1"><span class="BpkText_bpk-text__MWZkY BpkText_bpk-text--lg__NjNhN LegInfo_routePartialTime__OTFkN"><div bis_skin_checked="1"><span class="BpkText_bpk-text__MWZkY BpkText_bpk-text--label-1__NjBhY">6:45 PM</span><div class="TimeWithOffsetTooltip_offsetTooltipContainer__NjA0M" tabindex="0" aria-label="Arrives on Sunday, October 15, 2023" bis_skin_checked="1"><span class="BpkText_bpk-text__MWZkY BpkText_bpk-text--caption__MTIzM">+1</span></div></div></span><span class="BpkText_bpk-text__MWZkY BpkText_bpk-text--body-default__Y2M3Z"><div tabindex="0" aria-label="Singapore Changi, SIN, Singapore" bis_skin_checked="1"><span class="BpkText_bpk-text__MWZkY BpkText_bpk-text--body-default__Y2M3Z LegInfo_routePartialCityTooltip__NTE4Z">SIN</span></div></span></div></div></div><div class="LegDetails_container__MTkyZ UpperTicketBody_leg__MmNkN" aria-hidden="true" bis_skin_checked="1"><div class="LogoImage_container__MDU0Z LegLogo_logoContainer__ODdkM UpperTicketBody_legLogo__ZjYwM" bis_skin_checked="1"><div class="LegLogo_legImage__MmY0Z" bis_skin_checked="1"><div class="BpkImage_bpk-image__YTkyO BpkImage_bpk-image--no-background__NGMyN" style="height: 0px; padding-bottom: 50%;" bis_skin_checked="1"><img class="BpkImage_bpk-image__img__MDZkN" alt="United" src="//www.skyscanner.net/images/airlines/small/UA.png"></div></div></div><div class="LegInfo_legInfo__ZGMzY" bis_skin_checked="1"><div class="LegInfo_routePartialDepart__NzEwY" bis_skin_checked="1"><span class="BpkText_bpk-text__MWZkY BpkText_bpk-text--lg__NjNhN LegInfo_routePartialTime__OTFkN"><div bis_skin_checked="1"><span class="BpkText_bpk-text__MWZkY BpkText_bpk-text--label-1__NjBhY">8:45 AM</span></div></span><span class="BpkText_bpk-text__MWZkY BpkText_bpk-text--body-default__Y2M3Z"><div tabindex="0" aria-label="Singapore Changi, SIN, Singapore" bis_skin_checked="1"><span class="BpkText_bpk-text__MWZkY BpkText_bpk-text--body-default__Y2M3Z LegInfo_routePartialCityTooltip__NTE4Z">SIN</span></div></span></div><div class="LegInfo_stopsContainer__NWIyN" bis_skin_checked="1"><span class="BpkText_bpk-text__MWZkY BpkText_bpk-text--xs__ZDJmY Duration_duration__NmUyM">18h 20m</span><div class="LegInfo_stopLine__MzUxZ" bis_skin_checked="1"><span class="LegInfo_stopDot__ZTAyN"></span><svg xmlns="http://www.w3.org/2000/svg" xml:space="preserve" viewBox="0 0 12 12" class="LegInfo_planeEnd__ZDkxM"><path fill="#898294" d="M3.922 12h.499a.52.52 0 0 0 .444-.247L7.949 6.8l3.233-.019A.8.8 0 0 0 12 6a.8.8 0 0 0-.818-.781L7.949 5.2 4.866.246A.525.525 0 0 0 4.421 0h-.499a.523.523 0 0 0-.489.71L5.149 5.2H2.296l-.664-1.33a.523.523 0 0 0-.436-.288L0 3.509 1.097 6 0 8.491l1.196-.073a.523.523 0 0 0 .436-.288l.664-1.33h2.853l-1.716 4.49a.523.523 0 0 0 .489.71"></path></svg></div><div class="LegInfo_stopsLabelContainer__MmM0Z" bis_skin_checked="1"><span class="BpkText_bpk-text__MWZkY BpkText_bpk-text--xs__ZDJmY LegInfo_stopsLabelRed__NTY2Y">1 stop</span>&nbsp;<div class="LegInfo_stopsRow__MTUwZ" bis_skin_checked="1"><span class="BpkText_bpk-text__MWZkY BpkText_bpk-text--xs__ZDJmY LegInfo_stopStation__M2E5N"><div tabindex="0" aria-label="SFO" bis_skin_checked="1"><span class="BpkText_bpk-text__MWZkY BpkText_bpk-text--xs__ZDJmY">SFO</span></div></span></div></div></div><div class="LegInfo_routePartialArrive__Y2U1N" bis_skin_checked="1"><span class="BpkText_bpk-text__MWZkY BpkText_bpk-text--lg__NjNhN LegInfo_routePartialTime__OTFkN"><div bis_skin_checked="1"><span class="BpkText_bpk-text__MWZkY BpkText_bpk-text--label-1__NjBhY">12:05 PM</span></div></span><span class="BpkText_bpk-text__MWZkY BpkText_bpk-text--body-default__Y2M3Z"><div tabindex="0" aria-label="Los Angeles International, LAX, United States" bis_skin_checked="1"><span class="BpkText_bpk-text__MWZkY BpkText_bpk-text--body-default__Y2M3Z LegInfo_routePartialCityTooltip__NTE4Z">LAX</span></div></span></div></div></div></div>
            # trip_start_element = await trip_element.query_selector_all('div.nrc6')
            # <div class="c3J0r" bis_skin_checked="1"><div class="c3J0r-container" bis_skin_checked="1"><div class="aVdy-select-leg" bis_skin_checked="1"><div class="aVdy-select-leg-checkbox" bis_skin_checked="1"><span class="PVIO PVIO-mod-theme-default PVIO-mod-size-base "><span class="PVIO-input-wrapper"><input tabindex="0" aria-disabled="false" aria-checked="false" class="PVIO-input" type="checkbox" aria-label="" value="false"><svg viewBox="0 0 200 200" width="1.25em" height="1.25em" xmlns="http://www.w3.org/2000/svg" class="icon" role="img" aria-hidden="true"><path d="M132.639 63.231l-48.974 53.26l-17.569-13.51l-12.191 15.855c22.199 17.07 30.128 26.802 38.284 17.932l55.172-60l-14.722-13.537z"></path></svg></span></span></div></div><div class="tdCx-mod-spaced tdCx-mod-stacked" bis_skin_checked="1"><div class="tdCx-leg-carrier" bis_skin_checked="1"><div class="c5iUd c5iUd-mod-variant-medium" bis_skin_checked="1"><div class="c5iUd-leg-carrier" bis_skin_checked="1"><img src="https://content.r9cdn.net/rimg/provider-logos/airlines/v/SQ.png?crop=false&amp;width=108&amp;height=92&amp;fallback=default3.png&amp;_v=0ff33e55a8f21c7c3192f0394e8dfdb2" alt="Singapore Airlines"></div></div></div></div><div class="VY2U" bis_skin_checked="1"><div class="vmXl vmXl-mod-variant-large" bis_skin_checked="1"><span>8:45 pm</span><span class="aOlM"> – </span><span>9:40 pm</span></div><div class="c_cgF c_cgF-mod-variant-default" dir="auto" bis_skin_checked="1">Singapore Airlines</div></div><div class="JWEO" bis_skin_checked="1"><div class="vmXl vmXl-mod-variant-default" bis_skin_checked="1"><span class="JWEO-stops-text">nonstop</span></div><div class="c_cgF c_cgF-mod-variant-default" bis_skin_checked="1"></div></div><div class="xdW8" bis_skin_checked="1"><div class="vmXl vmXl-mod-variant-default" bis_skin_checked="1">15h 55m</div><div class="c_cgF c_cgF-mod-variant-default" bis_skin_checked="1"><div class="EFvI" bis_skin_checked="1"><div class="c_cgF c_cgF-mod-variant-default" title="Singapore Changi" bis_skin_checked="1"><span class="EFvI-ap-info" dir="auto"><span>SIN</span></span></div><span class="aOlM">-</span><div class="c_cgF c_cgF-mod-variant-default" title="Los Angeles" bis_skin_checked="1"><span class="EFvI-ap-info" dir="auto"><span>LAX</span></span></div></div></div></div></div></div>
            trips = await trip_element.query_selector_all("div.c3J0r")
           
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
        
        await save_itinerary_to_json(sort_by)
        
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
    sort_by_best ='bestflight_a'
    sort_by_cheapest ='price_a'
    sort_by_fastest ='duration_a'
    asyncio.run(skyscanner_scrape_website(city1,city2,travel_date,return_date,city1_name,city2_name,sort_by_cheapest))
