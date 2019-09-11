""" Module responsible to collect all coments about a player. """
import crawler
import parser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def get_comments(player_id):
    """Get users comments in a player page."""
    driver = webdriver.Chrome()
    link = parser.mount_player_comments_link(player_id)
    crawler.scroll_down(driver, link)
