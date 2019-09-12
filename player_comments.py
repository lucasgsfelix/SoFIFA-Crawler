""" Module responsible to collect all coments about a player. """
import parser
from selenium import webdriver
import crawler
from header import COMMENTS as COMMENTS_HEADER


def get_comments(player_id, header=False):
    """Get users comments in a player page."""
    driver = webdriver.Chrome()
    link = parser.mount_player_comments_link(player_id)
    player_comments = crawler.scroll_down(driver, link, player_id)
    file = "Output/player_comments.txt"
    parser.write_file(player_comments, file, COMMENTS_HEADER, header)
    driver.close()
