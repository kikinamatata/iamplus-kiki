import os
import json
from typing import List
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
                    # "return":{
                    #        "airlines":self.return_airlines,
                    #        "start_time":self.return_start_time,
                    #        "end_time":self.return_end_time,
                    # },
                }
        return json_node    
    
class Scraper:

    city1_code:str
    city2_code:str
    travel_date:str
    return_date:str
    city1_name:str
    city2_name:str

    itinerary_list:List[Itinerary] = []
    airports_dict ={}

    def __init__(self,city1_code, city2_code,travel_date,return_date):
       self.city1_code = city1_code
       self.city2_code = city2_code
       self.travel_date = travel_date
       self.return_date = return_date
       with open('airports_dict.json', 'r') as json_file:
             self.airports_dict = json.load(json_file)
       self.city1_name = self.airports_dict[self.city1_code.upper()]
       self.city2_name = self.airports_dict[self.city2_code.upper()]       
             

    
    
    async def my_print(element,name):
            text = await element.inner_html()
            print (name, text)

    # Function to save  instances to a JSON file
    async def save_itinerary_to_json(self,folder_name:str,  file_prefix = 'Best'):
            file_prefix = file_prefix.lower()
            # Check if the folder exists, and if not, create it
            if not os.path.exists(folder_name):
              os.makedirs(folder_name)
            # Define the file path
            file_path = os.path.join(folder_name, folder_name +'-' + file_prefix+'.json')
            serialized_list = []
            for item in self.itinerary_list:
                serialized_list.append(item.to_json())
                # break
            with open(file_path, 'w') as json_file:
                json.dump(serialized_list, json_file, indent=4)    

                   

