"""Get all the information about a player."""
import re
import parser


def get_player(player_id, player_name):
    """Return all info of a player."""

    link = parser.mount_player_link(player_id)
    page = parser.get_page(link)
    basic_info = get_basic_info(page, player_name, player_id)
    teams_info = get_player_team_info(page)
    get_attacking_info(page)
    get_defensive_info(page)
    get_skill_info(page)
    get_power_info(page)
    get_mentality_info(page)
    get_goalkeeping_info(page)
    get_movement_info(page)


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

    token = "Preferred Foot</label>"
    info['Foot'] = parser.retrieve_in_tags(token, '<', page)[0]

    token = "International Reputation</label>"
    info['Intern. Rep.'] = parser.retrieve_in_tags(token, '<',
                                                   page)[0]

    token = 'Weak Foot</label>'
    info['Weak Foot'] = parser.retrieve_in_tags(token, '<',
                                                page)[0]

    token = "Skill Moves</label>"
    info['Skills Moves'] = parser.retrieve_in_tags(token, '<',
                                                   page)[0]

    token = "Work Rate</label><span>"
    info['Work Rate'] = parser.retrieve_in_tags(token, '<',
                                                page)[0]

    token = "Release Clause</label><span>"
    info['Release Clause'] = parser.retrieve_in_tags(token, '<',
                                                     page)[0]

    return info


def get_player_team_info(page):
    """ Get the info of teams that a athlete plays."""

    start_token = r'a href="\/team\/[\d]+\/[\w]+\/"'
    start_token = re.compile(start_token)
    end_token = "</figure>"
    pages = parser.retrieve_in_tags(start_token,
                                    end_token, page)[0]
    team_info = _principal_team_info(pages)

    if len(pages) >= 2:  # there is a national team
        end_token = "/li></ul></div></div>"
        pages = parser.retrieve_in_tags(start_token,
                                        end_token, page)[1]
        national_info = _national_team_info(pages)

        return {**team_info, **national_info}

    return team_info


def get_defensive_info(page):
    """ Get a player defensive skills.
        Marking
        St. Tackle
        Sliding Tackle
    """


def get_attacking_info(page):
    """Get a player attacking skills.
        Crossing
        Finishing
        Heading Accuracy
        Short Passing
        Volleys
    """
    token = '<h5 class="bp3-heading">Attacking</h5>'
    attack_page = parser.retrieve_in_tags(token, '</div>', page)[0]

    skills = parser.retrieve_in_tags('>', '<', attack_page)

    skills = list(filter(lambda x : 
        (re.match(r'[\d]+', x) or re.match(r'[A-z ]+', x))
        and x != " ", skills))

    info = {}
    index = 0
    while index < len(skills) - 1:
        info[skills[index+1]] = skills[index]
        index = index + 2

    return info


def get_skill_info(page):
    """Get a player skills info.
        Dribbling
        Curve
        FK Accuracy
        Long Pass
        Ball Control
    """


def get_movement_info(page):
    """Get a player movement skills.
        Acceleration
        Sprint Speed
        Agility
        Reactions
        Balance
    """


def get_power_info(page):
    """Get a player power skills.
        Shot Power
        Jumping
        Stamina
        Strength
        Long Shots
    """


def get_mentality_info(page):
    """Get a player mentality skills.
        Aggression
        Interceptions
        Positioning
        Vision
        Penalties
        Composure
    """


def get_goalkeeping_info(page):
    """Get a player goalkeeping skills.
        GK Diving
        GK Handling
        GK Kicking
        GK Positioning
        GK Reflexes
    """


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


def _principal_team_info(page):
    """ Return the basic info of a players team.
        Team
        Team Position
        Team Skill
        Jersey Team
        Joined
        Contract
    """
    info = {}
    info['Team'] = parser.retrieve_in_tags(">", "<", page)[0]

    token = r'class="pos pos[\d]*">'
    token = re.compile(token)
    info['Team Position'] = parser.retrieve_in_tags(token,
                                                    '<', page)[0]

    token = r'span class="bp3-tag p p[\d]*">'
    token = re.compile(token)
    info['Team Skill'] = parser.retrieve_in_tags(token, '<',
                                                 page)[0]

    token = "Jersey Number</label>"
    info['Jersey'] = parser.retrieve_in_tags(token, "<", page)[0]

    token = "Joined</label>"
    info['Joined'] = parser.retrieve_in_tags(token, '<', page)[0]

    token = "Contract Valid Until</label>"
    info['Contract'] = parser.retrieve_in_tags(token, '<', page)[0]

    return info


def _national_team_info(page):
    """ Get the player national team info.
        Nat. Team
        Jersey Nat.
        Nat. Position
        Nat. Team Skill
    """
    info = {}
    info['Nat. Team'] = parser.retrieve_in_tags(">", "<", page)[0]

    token = "Jersey Number</label>"
    info['Jersey Nat.'] = parser.retrieve_in_tags(token, "<", page)[0]

    token = r'class="pos pos[\d]*">'
    token = re.compile(token)
    info['Nat. Position'] = parser.retrieve_in_tags(token,
                                                    '<', page)[0]

    token = r'span class="bp3-tag p p[\d]*">'
    token = re.compile(token)
    info['Nat. Team Skill'] = parser.retrieve_in_tags(token, '<',
                                                      page)[0]

    return info
