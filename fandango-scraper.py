import asyncio
from playwright.async_api import async_playwright
import json
import csv
from typing import List
import datetime
import re




class Cinema:
    name :str
    url : str
    showtimes:List[str] =[]

class ShowDetails:
    date :str
    cinemas:List[Cinema] = []

class Movie:
    pass

    showDetails :ShowDetails = ShowDetails()
    name : str
    genre : str
    language : str
    url : str
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

movie_list:List[Movie] = []
base_url = 'https://www.fandango.com'
movies_url = 'https://www.fandango.com/movies-in-theaters'

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


 
async def simple_serialized_movies():
    serialized_movies = []
    for movie in movie_list:
        serialized_movies.extend(movie.to_json_array())
    return serialized_movies



 # Function to save Movie instances to a JSON file
async def save_movies_to_json():
     # Save movie_list to a JSON file
    json_file = "fandango_movies.json"
    serialized_movies = []
    serialized_movies = await simple_serialized_movies()
    
    with open(json_file, 'w') as json_file:
        json.dump(serialized_movies, json_file, indent=4)   



async def set_movie_list(context,url):
    page = await context.new_page()
    await page.goto(url, timeout=0)
    # Get the HTML content of the page
    # html_content = await page.content()
    # print(html_content)
    #await page.wait_for_selector("div")
    query_string = 'ul.browse-movielist li'
    # Find the div element with class name "mymovie"
    div_movie_elements = await page.query_selector_all(query_string)

    # Iterate through the selected li elements
    for index, div_element in enumerate(div_movie_elements):
        # item_text = await div_element.inner_html()
        # print(item_text)
        movie = Movie()
        # Find the first anchor (<a>) element within the current div
        anchor_element = await div_element.query_selector('a')
        movie.url = base_url +  await anchor_element.get_attribute('href')
        print("Movie URL :", movie.url)
        #<span class="heading-style-1 browse-movielist--title poster-card--title" aria-hidden="true">Expend4bles (2023)</span>
        movie_title_element = await div_element.query_selector('.poster-card--title')

        # Get the text content of the movie title element
        movie.name = await movie_title_element.text_content()
        print("Movie Name :", movie.name)
        movie_list.append(movie)
        
    else:
        print('No div elements for movies were found.')

    
      
async def update_theatre_list(context,movie:Movie):
    print("Load URL", movie.url)
    page = await context.new_page()
    await page.goto(movie.url, timeout=0)
    # Get the HTML content of the page
    html_content = await page.content()
    # print(html_content)
    
    today_date = datetime.date.today()
    date_string = today_date.strftime("%m-%d-%Y")
    movie.showDetails.date = date_string
    theater_element_list = await page.query_selector_all(".js-movie-showtime-theater.movie-showtimes__theater.fd-panel.dark__section")
    for index,theater_element in enumerate(theater_element_list):
        cinema :Cinema = Cinema()
        theater_name_element = await theater_element.query_selector("a.movie-showtimes__detail-link")
        cinema.name = await theater_name_element.inner_text()
        print(cinema.name)
        #Shows
        show_element_list = await theater_element.query_selector_all("li.showtimes-btn-list__item")
        show_time_list = []
        for show_element in show_element_list:
            show_time =await show_element.inner_text()
            # Remove all special characters and extra whitespace
            show_time = re.sub(r'[^a-zA-Z0-9\s]', '', show_time)
            # Remove extra whitespace and trim leading/trailing whitespace
            show_time = ' '.join(show_time.split())
            print(show_time)
            show_time_list.append(show_time)
        cinema.showtimes = show_time_list
        print(cinema.showtimes)   
        movie.showDetails.cinemas.append(cinema)


async def scrape_website():
    async with async_playwright() as p:
        # Launch a Chromium browser instance
        browser = await p.chromium.launch()
        # Create a new browser context
        context = await browser.new_context()
        url = movies_url
        await set_movie_list(context, url)
        movie:Movie = Movie()
        movie.url = "https://www.fandango.com/expend4bles-2023-232154/movie-overview"
        for index,movie in enumerate(movie_list):
         print("Movie :",index)
         await update_theatre_list(context,movie)
        print("Total Movies :",len(movie_list))
        print("Total Cinemas :", len(movie_list[0].showDetails.cinemas))
        await save_movies_to_json()
        
        # Close the browser
        await browser.close()

# Run the asynchronous scraping function
if __name__ == "__main__":
    asyncio.run(scrape_website())
