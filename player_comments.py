""" Module responsible to collect all coments about a player. """
import parser
from selenium import webdriver
import crawler


def get_comments(player_id):
    """Get users comments in a player page."""
    driver = webdriver.Chrome()
    link = parser.mount_player_comments_link(player_id)
    crawler.scroll_down(driver, link, player_id)
    driver.close()
