from selenium import webdriver
from selenium.webdriver.common.by import By
from loguru import logger
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException


def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--log-level=3")
    options.add_argument("--start-maximized")
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
    return driver
    

def get_giphy_views(url):
    views_count = 0
    try:
        driver = get_driver()
        driver.get(url)
        if "media" in url and "giphy" in url:
            try:
                wait = WebDriverWait(driver, 30)
                media = wait.until(EC.presence_of_element_located((By.CLASS_NAME,"media_gif__MBeQG")))
                media.click()
            except NoSuchElementException as e:
                logger.error("NoSuchElementException occurred: {}".format(e))
                driver.quit()
                return "Invalid link."
            except Exception as e:
                logger.error(e)
        try:
            if "giphy" in url:
                views_count = driver.find_element(By.CLASS_NAME,"ViewCountContainer-sc-15ri43l").text
            else:
                driver.quit()
                return "Invalid url"
        except NoSuchElementException as e:
            logger.error("NoSuchElementException occurred: {}".format(e))
        except Exception as e:
            logger.error(e)
        logger.info(views_count)
        driver.quit()
        return views_count

    except Exception as e:
        logger.error(e)


if __name__ == "__main__":
    pass