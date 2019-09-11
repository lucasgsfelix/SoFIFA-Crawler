import time


class TimeOutException(Exception):
    """ Time out Exception Class."""


def scroll_down(driver, link):
    """Responsible to scroll down over a page"""

    driver.get(link)
    time.sleep(5)
    driver.switch_to.frame(driver.find_element_by_tag_name("is-preload"))
    html = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
    print(html)
    print("OIOIO")
    exit()
    try:
        driver.get(link)
    except TimeOutException:
        time.sleep(10)
        driver.refresh()
        driver.get(link)

    try:
        html = driver.page_source
    except:
        script = "return document.getElementsByTagName"
        script += "('html')[0].innerHTML"
        html = driver.execute_script(script)

    script_height = "return document.body.scrollHeight"
    last_height = driver.execute_script(script_height)

    script_down = "bp3-button bp3-minimal"
    script_down += "bp3-fill pure-button text-center"
    scroll_script = "window.scrollTo(0, document.body.scrollHeight);"

    while True:
        driver.execute_script(scroll_script)
        try:
            driver.find_element_by_class_name(script_down).click()
        except:
            pass
        time.sleep(2)

        new_height = driver.execute_script(script_height)
        if new_height == last_height:
            html = driver.page_source
            break
        last_height = new_height
