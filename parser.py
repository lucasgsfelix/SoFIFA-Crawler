"""Responsible to treat all information collected from SoFIFA."""
import re
import os


def mount_query_link(player_name):
    """Mount a query link given a player name."""

    link = "https://sofifa.com/players?keyword="
    if " " in player_name:
        return link + player_name.replace(" ", "%20")

    return link + player_name


def mount_player_link(player_id):
    """ Link of player general info."""

    return "https://sofifa.com/player/" + str(player_id)


def mount_player_life_link(player_id, player_name):
    """ Link of real life info."""
    link = "https://sofifa.com/player/" + str(player_id)

    return link + '/' + player_name.replace(' ', '-') + '/live'


def get_page(link):
    """ Given a link it return the html page. """
    os.system('wget -O auxiliary.html ' + link + " --quiet")
    with open('auxiliary.html', 'r') as file:
        info = file.read()

    os.system('rm auxiliary.html')
    return info


def _match_positions(start_list, end_list):
    """ Match start and end positions. """

    if len(start_list) == 1:
        value = start_list[0]
        return {value: list(filter(lambda x: value < x, end_list))[0]}

    result = {}
    for start in start_list:
        for end in end_list:
            if start < end:
                result[start] = end
                break

    return result


def retrieve_in_tags(start_token, end_token, page, parse=False):
    """ Retrieve between tags.

        Given a start_token and a end_token, will retrieve
        all values between those two tags.

        return parsed values
    """
    start_pos = [(a.end()) for a in list(re.finditer(start_token, page))]
    if not start_pos:
        return None

    end_pos = [(a.start()) for a in list(re.finditer(end_token, page))]

    positions = _match_positions(start_pos, end_pos)

    pages = list(map(lambda x: page[x:positions[x]], positions))

    if parse:

        for index, pag in enumerate(pages):
            pages[index] = parse_in_tags(pag)

        if len(set(pages)) > 1:
            return pages

        if not pages:
            return None
        return pages[0]

    return pages


def cut_page(start_token, end_token, page):
    """ Cut the page.

        Cut the page in the start_token, and then
        the first token that matchs with the position
        bigger than the position of the start token.

        return cut of the page
    """
    start_pos = [(a.end()) for a in list(re.finditer(start_token, page))]

    if start_pos:
        start_pos = start_pos[0]
        end_pos = [(a.start()) for a in list(re.finditer(end_token, page))]
        end_pos = list(filter(lambda x: x > start_pos, end_pos))[0]

        return page[start_pos:end_pos]

    return page


def parse_in_tags(page, join=True):
    """ Parse between > and < tags. """

    if '>' in page:
        pages = []
        start_pos = [(a.end()) for a in list(re.finditer('>', page))]
        for pos in start_pos:
            aux = pos
            while aux <= len(page)-1 and page[aux] != '<':
                aux += 1
            pages.append(page[pos:aux])
        tokens_list = ['\t', '\n', '<', '>', '', '</th>', '<td>',
                       '<br>', '&nbsp;']
        for index, pag in enumerate(pages):
            pages[index] = remove_tokens(pag, tokens_list)

        if join:
            return ''.join(pages)

        return list(filter(lambda x: x not in ['', '&nbsp;'], pages))

    return page


def remove_tokens(page, tokens):
    """ Remove tokens from the page. """
    for token in tokens:
        page = list(filter((token).__ne__, page))

    if '  ' in ''.join(page):
        text_aux = ''
        for pag in ''.join(page).split(' '):
            if pag:
                text_aux += pag + ' '

        return ''.join(text_aux[:-1])

    return ''.join(page)


def get_unparsed_text(page, token):
    """ Return unparsed text given a regex or string"""
    start = [(a.start()) for a in list(re.finditer(token, page))]
    end = [(a.end()) for a in list(re.finditer(token, page))]
    positions = _match_positions(start, end)
    pages = list(map(lambda x: page[x:positions[x]], positions))

    return pages
