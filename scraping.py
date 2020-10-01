# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt

def scrape_all():
    # Initiate headless driver for deployment
    browser = Browser("chrome", executable_path="chromedriver", headless=True)

    # Set news title and paragraph variables
    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data

def mars_news(browser):

    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    
    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)
        # 1. Searching for elements with a specific combination of tag (ul and li) and attribute 
        #    (item_list and slide, respectively).
        # 2. Telling browser to wait one second before searching for components. The optional delay is useful because 
        #    sometimes dynamic pages take a while to load, especially if they are image-heavy.

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')
    
    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('ul.item_list li.slide')
            # - Parent element: this element hold all of the other elem,ents within it, and will be referenced when 
            #   filtering results further.
            # - 'ul.item_list li.slide' pinpoints the <li /> tag with the class of slide and the <ul /> tag with a 
            #   class of item_list

        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find("div", class_='content_title').get_text()
            # .get_text() when chained onto .find(), only returns the text of an element

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_="article_teaser_body").get_text()

    except AttributeError:
        return None, None

    return news_title, news_p
 
 
def featured_image(browser):
    # Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()

    # Find the more info button and click that
    browser.is_element_present_by_text('more info', wait_time=1)
        # Search for element that has the provided text, ex. “more info.”
        # 'wait_time=1' allows browser to fully load while searching for element.
    more_info_elem = browser.links.find_by_partial_text('more info')
        # Variable to employ 'browser.links.find_by_partial_text()'
        # take string: 'more info', to find link associated with "more info" text
    more_info_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")
            # - 'figure.lede' references the <figure /> tag and its class, lede
            # - 'a' is the next tag nested inside the <figure /> tag
            # - An 'img' tag is also nested within this HTML, so we’ve included that as well
            # - '.get("src")' pulls the link to the image
    
    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'

    return img_url

def mars_facts():
    
    try:
        # use 'read_html" to scrape the facts table into a dataframe
        df = pd.read_html('http://space-facts.com/mars/')[0]
            # 'read.html()' searches for and returns a list of tables found in th HTML
            # '[0]' specifies index of 0, tells Pandas to pull only first table it encounters
    except BaseException:
        return None
    
    df.columns=['description', 'value']
        # Assign column to new DF
    df.set_index('description', inplace=True)
        # Sets Description column to table's index.
            #'inplace=True' means updated index will remain in place w/o having to reassign DF to a new variable

    # Convert DF back to an HTML
    return df.to_html()

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())