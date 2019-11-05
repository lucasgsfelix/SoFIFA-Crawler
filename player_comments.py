""" Module responsible to collect all coments about a player. """
import parser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
#from selenium.webdriver.firefox.options import Options as FirefoxOptions
import crawler


def get_comments(player_id):
    """Get users comments in a player page."""
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    #chrome_options.add_argument("--headless")
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    link = parser.mount_player_comments_link(player_id)
    crawler.scroll_down(driver, link, player_id)
    driver.close()
