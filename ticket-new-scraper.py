import asyncio
from playwright.async_api import async_playwright
import json
import csv

class Movie:
    def __init__(self, name, genre, language, url):
        self.name = name
        self.genre = genre
        self.language = language
        self.url = url

movie_list = []

def save_movie_list():
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
                # element_text = await div_element.text_content()
                name = await div_element.query_selector('.name')
               # print(f'Div {index + 1} text:',name, element_text)

                # Find all script elements with type "application/ld+json" within the current div
                script_element = await div_element.query_selector('script[type="application/ld+json"]')

                # Print script elements content
                if script_element:
                    print(f'Movie {index + 1} - Scripts with type "application/ld+json":')
                    script_content = await script_element.text_content()
                    # print(script_content)
                    try:
                        json_data = json.loads(script_content)
                        movie = Movie(
                            name=json_data['name'],
                            genre=json_data['genre'],
                            language=json_data["inLanguage"],
                            url=""
                            )
                        movie_list.append(movie)
                        if 'name' in json_data:
                            print('Name:', json_data['name'])
                        if 'inLanguage' in json_data:
                            print('Language:', json_data['inLanguage'])
                        if 'genre' in json_data:
                            print('Genre:', json_data['genre'])
                            
                    except json.JSONDecodeError:
                        print('Invalid JSON content in script.')
                else:
                    print(f'Movie {index + 1} - No scripts with type "application/ld+json" found.')

            save_movie_list()


        else:
            print('No div elements with class name "DesktopRunningMovie_movieCard__SDJqf" were found.')

        # Close the browser
        await browser.close()

# Run the asynchronous scraping function
if __name__ == "__main__":
    asyncio.run(scrape_website())
