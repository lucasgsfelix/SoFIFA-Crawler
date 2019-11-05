"""Responsible to call the browser to collect javascript comments"""
import json
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

    scroll_script = "window.scrollTo(0, document.body.scrollHeight);"
    sleep_time, cont = 0.0, 0
    start_time = time.time()

    while True:

        try:
            driver.execute_script(scroll_script)
            driver.find_element_by_id("commento-footer").click()
        except:
            sleep_time += 0.1

        try:
            time.sleep(3 + sleep_time)
            new_height = driver.execute_script(script_height)

            if new_height == last_height:
                driver.execute_script(scroll_script)
                driver.find_element_by_id("commento-footer").click()
                time.sleep_time(sleep_time)
                driver.execute_script(scroll_script)
                driver.find_element_by_id("commento-footer").click()
                time.sleep_time(sleep_time)
                if new_height == driver.execute_script(script_height):
                    page = driver.page_source
                    break

            last_height = new_height
        except:
            sleep_time += 0.1

        if sleep_time > 10:
            sleep_time = 0

        try:
            page = driver.page_source
            page = json.dumps(page).replace(u'\\u003C',
                                            '<').replace(u'\\u003E', '>')
            amount = parser.parse_comments(page.replace('\\', ''),
                                           player_id, True)
            print(amount)
        except:
            break

        if time.time() - start_time > 3600 * cont: # Will save from hour to our
            cont += 1
            parser.parse_comments(page.replace('\\', ''), player_id)

    page = driver.page_source
    page = json.dumps(page).replace(u'\\u003C', '<').replace(u'\\u003E', '>')
    parser.parse_comments(page.replace('\\', ''), player_id)
