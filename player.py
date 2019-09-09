"""Get all the information about a player."""
import re
import parser


def get_players_info(player_id, player_name, edition, release):
    """ Responsible to call"""
    info = {}
    info['Edition'] = edition
    info['Release'] = release
    info['Name'] = player_name
    info['Id'] = player_id

    link = parser.mount_player_link(player_id, edition, release)
    page = parser.get_page(link)
    get_player(page, info, player_id)


def get_player(page, info, player_id):
    """Return all info of a player."""

    basic_info = get_basic_info(page)
    basic_info = {**basic_info, **info}
    teams_info = get_player_team_info(page)
    attack_info = get_attacking_info(page)
    def_info = get_defensive_info(page)
    skill_info = get_skill_info(page)
    power_info = get_power_info(page)
    mental_info = get_mentality_info(page)
    goal_info = get_goalkeeping_info(page)
    move_info = get_movement_info(page)
    tags_info = get_tags(page)

    link = parser.mount_player_life_link(player_id)
    page = parser.get_page(link)
    add_info = get_add_info(page)

    return {**basic_info, **teams_info, **attack_info,
            **def_info, **skill_info, **power_info,
            **mental_info, **goal_info, **move_info,
            **tags_info, **add_info}


def get_add_info(page):
    """ Getting additional info. """

    sidelines_info = get_sidelines(page)
    titles_info = get_titles(page)

    return {**sidelines_info, **titles_info}


def get_basic_info(page):
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
    info['Complete Name'] = _get_complete_name(page)
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


def get_tags(page):
    """ Get tags with players topics."""

    info = {}
    token = '<div class="mt-2">'
    tags = parser.retrieve_in_tags(token, "</div>", page)[0]
    tags = parser.retrieve_in_tags("#", "<", tags)
    info['Tags'] = tags

    return info


def get_player_team_info(page):
    """ Get the info of teams that a athlete plays."""

    start_token = r'a href="\/team\/[\d]+\/[\w]+\/"'
    start_token = re.compile(start_token)
    end_token = "</figure>"
    pages = parser.retrieve_in_tags(start_token,
                                    end_token, page)[0]
    team_info = _principal_team_info(pages)

    national_info = {"Nat. Team": None,
                     "Jersey Nat.": None,
                     "Nat. Position": None,
                     "Nat. Team Skill": None}
    if len(pages) >= 2:  # there is a national team
        end_token = "/li></ul></div></div>"
        pages = parser.retrieve_in_tags(start_token,
                                        end_token, page)[1]
        national_info = _national_team_info(pages)

    return {**team_info, **national_info}


def get_defensive_info(page):
    """ Get a player defensive skills.
        Marking
        St. Tackle
        Sliding Tackle
    """
    token = '<h5 class="bp3-heading">Defending</h5>'
    def_page = parser.retrieve_in_tags(token, '</div>', page)[0]

    return _parse_skills(def_page)


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

    return _parse_skills(attack_page)


def get_skill_info(page):
    """Get a player skills info.
        Dribbling
        Curve
        FK Accuracy
        Long Pass
        Ball Control
    """
    token = '<h5 class="bp3-heading">Skill</h5>'
    skill_page = parser.retrieve_in_tags(token, '</div>', page)[0]

    return _parse_skills(skill_page)


def get_movement_info(page):
    """Get a player movement skills.
        Acceleration
        Sprint Speed
        Agility
        Reactions
        Balance
    """
    token = '<h5 class="bp3-heading">Movement</h5>'
    mov_page = parser.retrieve_in_tags(token, '</div>', page)[0]

    return _parse_skills(mov_page)


def get_power_info(page):
    """Get a player power skills.
        Shot Power
        Jumping
        Stamina
        Strength
        Long Shots
    """
    token = '<h5 class="bp3-heading">Power</h5>'
    power_page = parser.retrieve_in_tags(token, '</div>', page)[0]

    return _parse_skills(power_page)


def get_mentality_info(page):
    """Get a player mentality skills.
        Aggression
        Interceptions
        Positioning
        Vision
        Penalties
        Composure
    """
    token = '<h5 class="bp3-heading">Mentality</h5>'
    mental_page = parser.retrieve_in_tags(token, '</div>', page)[0]

    return _parse_skills(mental_page)


def get_goalkeeping_info(page):
    """Get a player goalkeeping skills.
        GK Diving
        GK Handling
        GK Kicking
        GK Positioning
        GK Reflexes
    """
    token = '<h5 class="bp3-heading">Goalkeeping</h5>'
    goal_page = parser.retrieve_in_tags(token, '</div>', page)[0]

    return _parse_skills(goal_page)


def get_sidelines(page):
    """Get injuries and expulsions."""

    start = '<h4 class="bp3-heading">Sidelined</h4>'
    end = '</table></div></article>'
    tokens = ['Description', 'Start Date', 'End Date']
    add_info = _add_info_parser(start, end, page, tokens)

    info = []
    for index in range(0, len(add_info), 2):
        sideline = {}
        sideline['Sideline'] = add_info[index]
        sideline['Date'] = add_info[index+1]
        info.append(sideline)

    sideline = {}
    sideline['Sidelines'] = info

    return sideline


def _add_info_parser(start, end, page, tokens):
    """Return the fileds of additional info"""

    add_info = parser.retrieve_in_tags(start, end, page)[0]
    add_info = parser.retrieve_in_tags('>', '<', add_info)
    add_info = list(filter(lambda x: '>' not in x and
                           x not in tokens
                           and not re.match(r'[\s,]+', x),
                           add_info))
    return add_info


def get_titles(page):
    """Get a player earned titles"""

    start = '<h4 class="bp3-heading">Trophies</h4>'
    end = '<div class="spacing">'
    tokens = ['Club Domestic']
    add_info = _add_info_parser(start, end, page, tokens)

    info, seasons, titles = [], [], {}
    # League, State, \# Winnings, \# Competition, Seasons
    flag = True
    for token in add_info:
        if re.match(r'[\d]+x', token):
            #  Will be the number of winning ou runner-up
            continue
        elif re.match(r'[\d]{4}\/[\d]{4}', token):
            # The season as winner ou runner-up
            seasons.append(token)
        elif re.match(r'[\d]{4}', token):
            # The season as winner ou runner-up
            seasons.append(token)
        elif token.lower() in ('winner', 'runner-up'):
            # He win a competition
            state = token
        else:
            # will be name of the competition
            if not flag:
                titles[state] = seasons
                info.append(titles)

            flag = False
            titles, seasons = {}, []
            titles['League'] = token.replace('  ', '')

    sideline = {}
    sideline['Competitions'] = info

    return sideline


def get_comments(page):
    """Get users comments in a player page."""
    # TODO


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


def _parse_skills(page):
    """ """
    skills = parser.retrieve_in_tags('>', '<', page)

    skills = list(filter(lambda x: x != " " and
                         (re.match(r'[\d]+', x)
                          or re.match(r'[A-z ]+', x)),
                         skills))

    info = {}
    index = 0
    while index < len(skills) - 1:
        info[skills[index+1]] = skills[index]
        index = index + 2

    return info
