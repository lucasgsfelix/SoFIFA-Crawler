"""Responsible to call the browser to collect javascript comments"""
import time
import parser


class TimeOutException(Exception):
    """ Time out Exception Class."""


class ElementNotFound(Exception):
    """ Element not Found Exception Class."""


def scroll_down(driver, link, player_id):
    """Responsible to scroll down over a page"""

    driver.get(link)
    time.sleep(5)
    try:
        driver.get(link)
    except TimeOutException:
        time.sleep(10)
        driver.refresh()
        driver.get(link)

    page = driver.page_source

    script_height = "return document.body.scrollHeight"
    last_height = driver.execute_script(script_height)

    #  script_down = "bp3-button bp3-minimal bp3-fill pure-button text-center"
    scroll_script = "window.scrollTo(0, document.body.scrollHeight);"

    cont = 0
    sleep_time = 2
    while True:
        driver.execute_script(scroll_script)
        try:
            driver.find_element_by_id("commento-footer").click()
        except ElementNotFound:
            raise "Element not found."

        if cont % 10 == 0:
            sleep_time += 1
        time.sleep(sleep_time)

        new_height = driver.execute_script(script_height)
        if new_height == last_height:
            page = driver.page_source
            break
        last_height = new_height
        parser.parse_comments(page, player_id)
        cont += 1
