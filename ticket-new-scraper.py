import asyncio
from playwright.async_api import async_playwright
import json
import csv
from typing import List

class Cinema:
    def __init__(self, name:str, showtimes:List[str]):
        self.name = name
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

async def save_movie_list_json():
    # Save movie_list to a JSON file
    json_file = "movies.json"

    # Convert the movie_list to JSON format
    movie_data_json = json.dumps([movie.__dict__ for movie in movie_list], indent=4)

    # Write the JSON data to a file
    with open(json_file, 'w') as file:
        file.write(movie_data_json)

    print(f"Movie data saved to {json_file}")   

async def get_movie_url(div_element, base_url, index):
    href_value = ""

    # Find the first anchor (<a>) element within the current div
    anchor_element = await div_element.query_selector('a')

    if anchor_element:
        # Get the "href" attribute value
        href_value = base_url + await anchor_element.get_attribute('href')
        print(f'Movie {index + 1} - Href Value:', href_value)
        print()
    else:
        print(f'Movie {index + 1} - No anchor elements found.')
        print()
    
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
        print(f'Movie {index + 1} - Name:', name)
    if genre is not None:
        print(f'Movie {index + 1} - Genre:', genre)
    if language is not None:
        print(f'Movie {index + 1} - Language:', language)

    # Return the extracted data as a tuple
    return name, genre, language

async def get_show_details(context,url, index):
    page = await context.new_page()
    await page.goto(url)
   # Find the div elements of Show Details
    div_cinema_elements = await page.query_selector_all('div.MovieSessionsListingDesktop_movieSessions__YBUAu')
    print(f'Movie {index +1}:',url)
    for index_cinema, div_element in enumerate(div_cinema_elements):
        # Find the first anchor (<a>) element within the current div
        anchor_element = await div_element.query_selector('a')

        if anchor_element:
            # Get the "href" attribute value
            href_value = base_url + await anchor_element.get_attribute('href')
            print(f'Movie{index +1} Cinema URL {index_cinema +1}:', href_value)
        else:
            print(f'Movie{index +1} Cinema URL {index_cinema +1}:', ' - No anchor elements found.')

        # Get the text content of the <a> element
        text_content =await anchor_element.inner_html()
        print(f'Movie{index +1} Cinema Name {index_cinema +1}:', text_content)
        print()

    show_details :ShowDetails = None
    return show_details

      

async def scrape_website():
    async with async_playwright() as p:
        # Launch a Chromium browser instance
        browser = await p.chromium.launch()

        # Create a new browser context
        context = await browser.new_context()

        # Create a page in the context
        page = await context.new_page()

        # Navigate to the URL you want to scrape
        await page.goto('https://ticketnew.com/movies/chennai')

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
                # #Show Details
                # page = await context.new_page()
                # await page.goto(href_value)
                #  # Find the div elements of Show Details
                # div_cinema_elements = await page.query_selector_all('div.MovieSessionsListingDesktop_movieSessions__YBUAu')

                # for div_element in div_cinema_elements:
                #     # Find the first anchor (<a>) element within the current div
                #     anchor_element = await div_element.query_selector('a')

                #     if anchor_element:
                #         # Get the "href" attribute value
                #         href_value = base_url + await anchor_element.get_attribute('href')
                #         print(f'>>>>>Movie 1 - Href Value:', href_value)
                #         print()
                #     else:
                #         print(f'Movie 1 - No anchor elements found.')
                #         print()

                #     # Get the text content of the <a> element
                #     text_content =await anchor_element.inner_html()
                #     print("Text Content:", text_content)

                show_details = None
                show_details = await get_show_details(context=context,url=href_value,index=index)
                movie.showDetails = show_details
                movie_list.append(movie)

            await save_movie_list_json()
            await browser.close()

        else:
            print('No div elements with class name "DesktopRunningMovie_movieCard__SDJqf" were found.')

        # Close the browser
       

# Run the asynchronous scraping function
if __name__ == "__main__":
    asyncio.run(scrape_website())
