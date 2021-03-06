# Import Splinter, PANDAS and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt
 
#10.5.3 Define function scrape_all
def scrape_all():
    # Setting the path to launch url
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
   
    news_title, news_paragraph = mars_news(browser)
    # Run all scraping functions and store results in dictionary
    data = { 
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres": mars_hemisphere(browser)}

    #stop webdriver & return data
    browser.quit()
    return data
 
# refactor code to make a function named mars_news 10.5.2
def mars_news(browser):
    # SCRAPE MARS NEWS
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)
   
    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)
 
    #Set up html parser
    html = browser.html
    news_soup = soup(html, 'html.parser')
    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # find the div with class as content title
        #slide_elem.find('div', class_='content_title')
        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # .get_text() gets just the text of the recent title
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    except AttributeError:
        return None, None
    # complete & show the result
    return news_title, news_p
 
 
# ### Featured Images
# Declare & Define function
def featured_image(browser):
# Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)
 
    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()
 
    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
 
    # Add try & except for handling errors
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
   
    except AttributeError:
        return None
    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    return img_url
 
# DEFINE FUNCTION
def mars_facts():
    try:
        # Create DF of HTML IMAGES
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None
# ASSIGN COLUMNS AND SET INDEX OF DATAFRAME
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)
# convert dataframe back to html, add bootstrap
    return df.to_html(classes="table table-striped")

def mars_hemisphere(browser):
    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    hemisphere_image_urls = []

    links = browser.find_by_css('a.product-item img')
    # Add try/except for error handling
    for i in range(len(links)):
        hemisphere = {}
        browser.find_by_css('a.product-item img')[i].click()
        sample_elem = browser.links.find_by_text('Sample').first
        hemisphere['img_url'] = sample_elem['href']
        hemisphere['title'] = browser.find_by_css('h2.title').text
        hemisphere_image_urls.append(hemisphere)
        browser.back()
    return hemisphere_image_urls
    
if __name__ == "__main__":
    print(scrape_all())
