from splinter import Browser
import pandas as pd
from bs4 import BeautifulSoup as bs
import time
from webdriver_manager.chrome import ChromeDriverManager

def scrape_info():

    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Visit Mars news site
    url = "https://redplanetscience.com/"
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Get news titles
    news_titles = soup.find_all('div', class_='content_title')

    # Get news paragraphs
    paragraphs = soup.find_all('div', class_='article_teaser_body')
    
    # Assign first result to variables
    news_title = news_titles[0].text
    paragraph = paragraphs[0].text

    # Visit Mars Image site
    url2 = "https://spaceimages-mars.com"
    browser.visit(url2)

    # Click full image
    browser.click_link_by_partial_text('FULL IMAGE')

    # Search image source
    html = browser.html
    img_soup = bs(html, 'html.parser')

    # find the relative image url
    img_1 = img_soup.find('img', class_='fancybox-image').get('src')

    # Esablish base URL
    feature_image_url = f'https://spaceimages-mars.com/{img_1}'

    # Visit Mars Facts site
    df = pd.read_html('https://galaxyfacts-mars.com/')[1]

    # Clean table format
    df.columns=['Features', 'Values']
    df.set_index('Features', inplace=True)

    mars_info = df.to_html()

    # Visit Mars Hemispheres site
    url = "https://marshemispheres.com/"
    browser.visit(url)

    hemi_url = []

    # Loop to retreive hemisphere titles and urls
    for hemi in range(4):
         
        # Click each hemisphere link
        browser.links.find_by_partial_text('Hemisphere')[hemi].click()
    
        # Scrape page into Soup
        html = browser.html
        hemi_soup = bs(html, "html.parser")
    
        # Scrape title and image url
        title = hemi_soup.find('h2', class_='title').text
        image = hemi_soup.find('li').a.get('href')

        #Sore data into hemispheres dictionary
        hemi = {}
        hemi['title'] = title
        hemi['image'] = f'https://marshemispheres.com/{image}'
        hemi_url.append(hemi)
    
        # Browse back to repeat
        browser.back()

    # Store data in a dictionary
    mars_data = {
        "News Title": news_title,
        "Paragraph": paragraph,
        "Feature Image": feature_image_url,
        "Mars Info": mars_info,
        "Hemisphere": hemi
    }

    browser.quit()

    return mars_data