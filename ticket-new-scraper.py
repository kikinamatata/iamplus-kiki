import asyncio
from playwright.async_api import async_playwright
import json
import csv
from typing import List
import datetime


class Cinema:
    def __init__(self, name:str,url:str, showtimes:List[str]):
        self.name = name
        self.url = url
        self.showtimes = showtimes

class ShowDetails:
    def __init__(self, date:str, cinemas:List[Cinema]=None):
        self.date = date
        self.cinemas = cinemas

class Movie:
    showDetails :ShowDetails = None
    def __init__(self, name, genre, language, url):
        self.name = name
        self.genre = genre
        self.language = language
        self.url = url

    def to_json_array(self):
        # Create a dictionary representing the JSON node
        json_array = []
        date = self.showDetails.date
        for cinema in self.showDetails.cinemas:
            json_node = {
                    "MovieTitle": self.name,
                    "Theatre": cinema.name,
                    "MovieDate": date    
                }
            showtime_all = ""
            for showtime in cinema.showtimes:
                showtime_all += showtime+" "
            json_node["ShowTime"] = showtime_all
            json_array.append(json_node)
        return json_array    

# Function to serialize Movie and ShowDetails instances to JSON
def serialize_movie_and_showdetails(movie:Movie):
    return {
        "name": movie.name,
        "genre": movie.genre,
        "language": movie.language,
        "url": movie.url,
        "showDetails": {
            "date": movie.showDetails.date,
            "cinemas": [
                {
                    "name": cinema.name,
                    "url":cinema.url,
                    "showtimes": cinema.showtimes
                }
                for cinema in movie.showDetails.cinemas
            ]
        }
    }        

        

movie_list = []

base_url = 'https://ticketnew.com'

async def save_movie_list_cvs():
    # Save movie_list to a CSV file
    csv_file = "movies.csv"

    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        
        # Write header row
        writer.writerow(["Name", "URL", "Genre", "Language"])
        
        # Write data for each movie
        for movie in movie_list:
            writer.writerow([movie.name, movie.url, movie.genre, movie.language])

    print(f"Movie data saved to {csv_file}")
 
async def simple_serialized_movies():
    serialized_movies = []
    for movie in movie_list:
        serialized_movies.extend(movie.to_json_array())
    return serialized_movies



 # Function to save Movie instances to a JSON file
async def save_movies_to_json():
     # Save movie_list to a JSON file
    json_file = "movies.json"
    serialized_movies = []
    save_full_movies = False
    if save_full_movies :
       json_file = "movies_full.json"
    
       serialized_movies =  [serialize_movie_and_showdetails(movie) for movie in movie_list]
    else:
        serialized_movies = await simple_serialized_movies()
    
    with open(json_file, 'w') as json_file:
        json.dump(serialized_movies, json_file, indent=4)   

async def get_movie_url(div_element, base_url, index):
    href_value = ""

    # Find the first anchor (<a>) element within the current div
    anchor_element = await div_element.query_selector('a')
    print()
    if anchor_element:
        # Get the "href" attribute value
        href_value = base_url + await anchor_element.get_attribute('href')
        print(f'Movie {index + 1} URL:', href_value)
       
    else:
        print(f'Movie {index + 1} - No anchor elements found.')
    
    return href_value

async def extract_movie_info(div_element, index):
    # Initialize variables to store extracted data
    name = None
    genre = None
    language = None

    # Find all script elements with type "application/ld+json" within the current div
    script_elements = await div_element.query_selector_all('script[type="application/ld+json"]')

    # Iterate through each script element
    for script_element in script_elements:
        # Get script content
        script_content = await script_element.text_content()

        try:
            # Parse JSON data from the script content
            json_data = json.loads(script_content)

            # Extract desired information
            if 'name' in json_data:
                name = json_data['name']
            if 'genre' in json_data:
                genre = json_data['genre']
            if 'inLanguage' in json_data:
                language = json_data['inLanguage']

            # You can break out of the loop if you've found the data you need
            if name is not None and genre is not None and language is not None:
                break

        except json.JSONDecodeError:
            print('Invalid JSON content in script.')

    # Print the extracted data for this movie
    if name is not None:
        print(f'Movie {index + 1} - Name:', name, f'- Genre:', genre,f'- Language:', language )
    
    return name, genre, language

async def get_show_details(context,url, index):
    page = await context.new_page()
    await page.goto(url,timeout=0)
    #await page.wait_for_selector("div")
   # Find the div elements of Show Details
    div_cinema_elements = await page.query_selector_all('div.MovieSessionsListingDesktop_movieSessions__YBUAu')
    print(f'Movie {index +1}:',url)
    cinemas = []
    for index_cinema, div_element in enumerate(div_cinema_elements):
        # Find the first anchor (<a>) element within the current div
        anchor_element = await div_element.query_selector('a')
        
        if anchor_element:
            # Get the "href" attribute value
            href_value = base_url + await anchor_element.get_attribute('href')
            print(f'Movie {index +1} Cinema URL {index_cinema +1}:', href_value)
        else:
            print(f'Movie{index +1} Cinema URL {index_cinema +1}:', ' - No anchor elements found.')

        # Get the text content of the <a> element
        cinema_url =  base_url + await anchor_element.get_attribute('href')
        cinema_name =await anchor_element.inner_html()
        print(f'Movie {index +1} Cinema Name {index_cinema +1}:', cinema_name)
        print()

        #show times
        showtime_elements = await div_element.query_selector_all("div.greenCol.MovieSessionsListingDesktop_time__HWpes")
        print("Show Time Total :",len(showtime_elements))
        show_times = []
        for show_element in showtime_elements:
           
            show_time = await show_element.inner_text()
            show_time = show_time.split("\n")[0]
            show_times.append(show_time)
            print("Show Time :",show_time)
        cinemas.append(Cinema(cinema_name,cinema_url,showtimes=show_times))
                
    # Get today's date
    today_date = datetime.date.today()
    date_string = today_date.strftime("%m-%d-%Y")
    show_details :ShowDetails = ShowDetails(date_string,cinemas=cinemas)
    return show_details

async def set_movie_list(context,url):
    page = await context.new_page()
    await page.goto(url, timeout=0)
    #await page.wait_for_selector("div")

    # Find the div element with class name "mymovie"
    div_movie_elements = await page.query_selector_all('div.DesktopRunningMovie_movieCard__SDJqf')

    # Check if any div elements with class name "mymovie" were found
    if div_movie_elements:
        print(f'Found {len(div_movie_elements)} div elements with class name "DesktopRunningMovie_movieCard__SDJqf".')
        # You can loop through the elements and interact with them or extract data
        for index, div_element in enumerate(div_movie_elements):

            href_value =await get_movie_url(div_element=div_element,base_url=base_url,index=index)
            name, genre, language = await extract_movie_info(div_element=div_element,index=index)
            movie = Movie(
                        name=name,
                        genre=genre,
                        language=language,
                        url=href_value
                        )
            
            show_details = None
            show_details = await get_show_details(context=context,url=href_value,index=index)
            movie.showDetails = show_details
            movie_list.append(movie)
            # if index == 1:
            #    break


    else:
        print('No div elements with class name "DesktopRunningMovie_movieCard__SDJqf" were found.')

      

async def scrape_website():
    async with async_playwright() as p:
        # Launch a Chromium browser instance
        browser = await p.chromium.launch()
        # Create a new browser context
        context = await browser.new_context()
        url = 'https://ticketnew.com/movies/chennai'
        await set_movie_list(context, url)
        await save_movies_to_json()
        
        # Close the browser
        await browser.close()

# Run the asynchronous scraping function
if __name__ == "__main__":
    asyncio.run(scrape_website())
