"""Get all the information about a player."""
import re
import parser


def get_player(player_id, player_name):
    """Return all info of a player."""
    link = parser.mount_player_link(player_id)
    page = parser.get_page(link)
    get_basic_info(page, player_name, player_id)


def get_basic_info(page, player_name, player_id):
    """ Get a player basic info.
        Here we will get:
        - Name
        - Complete Name
        - ID
        - Edition
        - Release
        - Birth Date
        - Birth Place
        - Height
        - Weight
        - Position
        - Value
        - Wage
        - Foot
        - Intern. Rep.
        - Weak Foot
        - Skills Moves
        - Work Rate
        - Body Type
        - Release Clause
    """
    info = {}
    info['Name'] = player_name
    info['Complete Name'] = _get_complete_name(page)
    info['Id'] = player_id
    info = _get_edition_release(page, info)
    info['Position'] = _get_position(page)
    info['Birth Date'] = _get_birth_date(page)
    info['Birth Place'] = _get_birth_place(page)
    info['Height'] = _get_height(page)
    info['Weight'] = _get_weight(page)

    token = r'Value&nbsp;[\n\t]*<span>'
    info['Value'] = parser.retrieve_in_tags(token, '<', page)[0]
    token = r'Wage&nbsp;[\n\t]*<span>'
    info['Wage'] = parser.retrieve_in_tags(token, '<', page)[0]


def get_teams_info(page):
    """ Get the info of teams that a athlete plays."""


def get_defensive_info(page):
    """ Get a player defensive skills."""


def get_attacking_info(page):
    """Get a player attacking skills."""


def get_skill_info(page):
    """Get a player skills info."""


def get_movement_info(page):
    """Get a player movement skills."""


def get_power_info(page):
    """Get a player power skills."""


def get_mentality_info(page):
    """Get a player mentality skills."""


def get_goalkeeping_info(page):
    """Get a player goalkeeping skills."""


def get_additional_info(link):
    """Get a player carrer info as injuries and titles."""


def get_comments(link):
    """Get users comments in a player page."""


def get_id_by_name(name):
    """Return the id of a player in SoFIFA given his name."""

    link = parser.mount_query_link(name)
    page = parser.get_page(link)

    token = 'href="/player/'
    start_pos = [(a.end()) for a in list(re.finditer(token, page))]

    if start_pos:
        pos = start_pos[0]
        player_id = ''
        while page[pos] != '/':
            player_id += page[pos]
            pos += 1

    return player_id


def _get_position(page):
    """Getting a player position"""
    token_re = r'class="pos pos[\d]*">[A-Z]*</span></li>'
    token_re = re.compile(token_re)
    positions = parser.get_unparsed_text(page, token_re)

    pos = []
    for position in positions:
        ans = parser.retrieve_in_tags('>', '<', position)[0]
        if ans is not None:
            pos.append(ans)

    return ' '.join(ans)


def _get_birth_date(page):
    """ Getting and parsing the birth date of a player."""
    token_re = r'class="pos pos[\d]*">[A-Z]*</span>[\',"()\d A-z]*</div>'
    token_re = re.compile(token_re)
    date = parser.get_unparsed_text(page, token_re)[0]
    date = parser.retrieve_in_tags("</span>", '</div>', date)[0]
    re_one = re.compile(r'\(')
    re_two = re.compile(r'\)')
    date = parser.retrieve_in_tags(re_one, re_two, date)[0]

    return date


def _get_edition_release(page, info):
    """Returns the edition and release of FIFA"""
    token = 'class="bp3-tag bp3-minimal bp3-intent-success">'
    aux = parser.retrieve_in_tags(token, '<', page)[0]
    aux = aux.split(' ')

    aux.pop(0)  # Removing the tag FIFA
    info['Edition'] = aux[0]

    aux.pop(0)  # Removing the edition
    info['Release'] = ''.join(aux)

    return info


def _get_birth_place(page):
    """ Getting the birth place of a player"""
    token_re = r'title="[A-z]*"><img alt="" src=""'
    token_re += r' data-src="https://cdn.sofifa.org/flags/[\d]*.png'
    token_re = re.compile(token_re)
    place = parser.get_unparsed_text(page, token_re)[0]

    return parser.retrieve_in_tags('title="', '"', place)[0]


def _get_weight(page):
    """Returns the players weight."""
    token = r'class="pos pos[\d]*">[A-Z]*</span>'
    token += r' .*\) [\d]*\'[\d]*\" [\w]*</div>'
    token = re.compile(token)
    weight = parser.get_unparsed_text(page, token)[0]

    return parser.retrieve_in_tags('" ', '<', weight)[0]


def _get_height(page):
    """Returns the players height"""
    token = r'class="pos pos[\d]*">[A-Z]*</span>'
    token += r' .*\) [\d]*\'[\d]*\"'
    token = re.compile(token)
    height = parser.get_unparsed_text(page, token)[0]

    return parser.retrieve_in_tags(r'\) ', '"', height)[0] + '"'


def _get_complete_name(page):
    """Return the complete of the player."""
    token = 'class="meta bp3-text-overflow-ellipsis">'
    name = parser.retrieve_in_tags(token, '<', page)
    return name[0][:-1]
