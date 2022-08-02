# Import Splinter, BeautifulSoup, and Pandas
from bs4 import BeautifulSoup as soup
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# Setup Splinter with an Executable Path
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

# Set up the HTML parser for a BeautifulSoup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')
# Assign 'slide_elem' as the variable to look for the <div /> parent element and its descendents
slide_elem = news_soup.select_one('div.list_text')


# ### Scraping Article Titles from RedPlanetScience.com
# 
# ![RedPlanetScienceScrape.png](attachment:RedPlanetScienceScrape.png)

# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### Featured Images
# Image Scraping
# 
# ![SpaceImages-Mars_Scrape-2.png](attachment:SpaceImages-Mars_Scrape-2.png)

# Visit 'SpaceImages-Mars' URL
url = 'https://spaceimages-mars.com'
browser.visit(url)

# Find and click the 'Full Image' button (there are three instances of '<button', the Full Image button is the 2nd)
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# We want the generic placeholder for the image (fancybox-image), not the specific name that will change depending on each image
# ![data-10-3-4-3-use-dev-tools-to-view-the-img-with-fancybox-class.png](attachment:data-10-3-4-3-use-dev-tools-to-view-the-img-with-fancybox-class.png)

# Find the relative image url 
    # An img tag is nested within this HTML, so we've included it.
    # .get('src') pulls the link to the image.
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# But if we copy and paste this 'img_url_rel' link into a browser, it won't work. This is because it's only a partial link, as the base URL isn't included. If we look at our address bar in the webpage, we can see the entire URL up there already; we just need to add the first portion ('https://spaceimages-mars.com') to our app.

# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ### Scraping a Table of Mars facts

# Pandas function read_html() specifically searches for and returns a list of tables found in the HTML. 
# By specifying an index of 0, we're telling Pandas to pull only the first table it encounters
df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df

# Pandas also has a way to easily convert our DataFrame back into HTML-ready code using the .to_html() function.
df.to_html()

# end the automated browsing session to avoid it running indefinitely in the background
browser.quit()
