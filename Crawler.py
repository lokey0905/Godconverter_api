import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

driver = uc.Chrome()

def get_nhentai_data(url):
    driver.get(url)

    title = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "pretty"))).text
    thumbnail = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "lazyload"))).get_attribute("src")


    data = {"title": title, "thumbnail": thumbnail}
    return data


def get_wnacg_data(url):
    content_url = url.replace("photos-slide", "photos-index")
    driver.get(content_url)
    
    title = driver.find_element(By.CSS_SELECTOR, "div.asTB img").get_attribute("alt")
    thumbnail = driver.find_element(By.CSS_SELECTOR, "div.asTB img").get_attribute("src").replace("////", "https://")

    
    data = {"title": title, "thumbnail": thumbnail}
    return data


def get_18comic_data(url):
    content_url = url.replace("photo", "album")
    driver.get(content_url)

    title = driver.find_element(By.CSS_SELECTOR, "h1.book-name").text
    thumbnail = driver.find_element(By.CSS_SELECTOR, 'img[itemprop="image"]').get_attribute('src')
    
    data = {"title": title, "thumbnail": thumbnail}
    return data

def get_pixiv_data(url):
    driver.get(url)

    title = driver.title.split(" - ")[0]
    if "R-18" in driver.page_source:
        thumbnail = "https://icons.veryicon.com/png/o/commerce-shopping/soft-designer-online-tools-icon/delete-77.png"
    else:
        thumbnail = url.replace("https://www.pixiv.net/artworks/", "https://embed.pixiv.net/decorate.php?illust_id=")

    
    data = {"title": title, "thumbnail": thumbnail}
    return data

def get_data(url):
    data = {}  # 先給一個空的字典
    if 'nhentai' in url:
        data = get_nhentai_data(url)
    elif 'wnacg' in url:
        data = get_wnacg_data(url)
    elif '18comic' in url:
        data = get_18comic_data(url)
    elif 'pixiv' in url:
        data = get_pixiv_data(url)
        
    json_data = json.dumps(data, ensure_ascii=False)
    return json_data

@app.route('/get_data', methods=['GET'])
def input():
    url = request.args.get('url')
    data = get_data(url)
    return data