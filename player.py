"""Get all the information about a player."""
import re
import parser


def get_players_info(player_id, player_name, edition, release):
    """ Responsible to call all methods"""
    info = {}
    info['Name'] = player_name
    info['Id'] = player_id
    info['Edition'] = edition
    info['Release'] = release

    link = parser.mount_player_link(player_id, edition, release)
    print(link)
    page = parser.get_page(link)
    return get_player(page, info, player_id)


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
        - Overall
        - Potential
    """
    info = {}
    info['Complete Name'] = _get_complete_name(page)
    info['Release Date'] = _get_edition_release(page)
    info['Position'] = _get_position(page)
    info['Birth Date'] = _get_birth_date(page)
    info['Birth Place'] = _get_birth_place(page)
    info['Height'] = _get_height(page)
    info['Weight'] = _get_weight(page).replace('lbs', '')

    token = r'Value&nbsp;[\n\t]*<span>'
    info['Value'] = parser.retrieve_in_tags(token, '<', page)
    token = r'Wage&nbsp;[\n\t]*<span>'
    info['Wage'] = parser.retrieve_in_tags(token, '<', page)

    token = "Preferred Foot</label>"
    info['Foot'] = parser.retrieve_in_tags(token, '<', page)

    token = "International Reputation</label>"
    info['Intern. Rep.'] = parser.retrieve_in_tags(token, '<',
                                                   page)

    token = 'Weak Foot</label>'
    info['Weak Foot'] = parser.retrieve_in_tags(token, '<',
                                                page)

    token = "Skill Moves</label>"
    info['Skill Moves'] = parser.retrieve_in_tags(token, '<',
                                                  page)
    token = "Work Rate</label><span>"
    info['Work Rate'] = parser.retrieve_in_tags(token, '<',
                                                page)

    token = "Release Clause</label><span>"
    info['Release Clause'] = parser.retrieve_in_tags(token, '<',
                                                     page)

    token = r'class="bp3-tag p p[\d]+">[\d]+</span>.* Overall Rating'
    token = re.compile(token)
    aux = parser.get_unparsed_text(page, token)[0]
    info['Overall'] = parser.retrieve_in_tags('>', '<', aux)

    token = r'class="bp3-tag p p[\d]+">[\d]+</span>.* Potential&nbsp'
    token = re.compile(token)
    aux = parser.get_unparsed_text(page, token)[0]
    info['Potential'] = parser.retrieve_in_tags('>', '<', aux)

    info = _set_none(info)

    return info


def _set_none(info):
    '''Removing from the list the not None Values'''
    for key in info:
        if isinstance(info[key], list):
            info[key] = info[key][0]

    return info


def get_tags(page):
    """ Get tags with players topics."""

    info = {}
    token = '<div class="mt-2">'
    tags = parser.retrieve_in_tags(token, "</div>", page)[0]
    tags = parser.retrieve_in_tags("#", "<", tags)
    if tags is not None:
        info['Tags'] = str(len(tags))
    else:
        info['Tags'] = tags

    return info


def get_player_team_info(page):
    """ Get the info of teams that a athlete plays."""

    start_token = r'a href="\/team\/[\d]+\/[\w-]+\/"'
    start_token = re.compile(start_token)
    flag = False
    try:
        end_token = "</figure>"
        pages = parser.retrieve_in_tags(start_token,
                                        end_token, page)[0]
    except:
        end_token = '<div class="operation spacing">'
        pages = parser.retrieve_in_tags(start_token,
                                        end_token, page)[0]
        flag = True

    team_info = _principal_team_info(pages)

    national_info = {"Nat. Team": None,
                     "Jersey Nat.": None,
                     "Nat. Position": None,
                     "Nat. Team Skill": None}

    if not flag:  # there is a national team
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
    if start in page:
        add_info = _add_info_parser(start, end, page, tokens)
    else:
        return {'Expulsions': None, 'Injuries': None}

    info = []
    index = 0
    while index < len(add_info)-1:
        sideline = {}
        if re.match(r'[\w/ ]*', add_info[index]):
            sideline['Sideline'] = add_info[index]
            index += 1
        if re.match(r'[\d]{2}/[\d]{2}/[\d]{2}', add_info[index]):
            sideline['Start Date'] = add_info[index]
            index += 1
        if re.match(r'[\d]{2}/[\d]{2}/[\d]{2}', add_info[index]):
            sideline['End Date'] = add_info[index]
            index += 1

        info.append(sideline)

    # sideline['History'] = info All sideline history
    expulsion, injury = 0, 0
    for sideline in info:
        if 'Suspended' in sideline.values():
            expulsion += 1
        else:
            injury += 1

    sideline = {}
    sideline['Expulsions'] = str(expulsion)
    sideline['Injuries'] = str(injury)

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
    tokens = ['Club Domestic', 'National', 'Club International']
    add_info = _add_info_parser(start, '<div class="spacing">',
                                page, tokens)

    info, titles, flag, state = [], {}, True, None
    # League, State, \# Winnings, \# Competition, Seasons
    seasons_winning, seasons_running = [], []
    for token in add_info:
        if re.match(r'[\d]+x', token):
            #  Will be the number of winning ou runner-up
            continue
        elif (re.match(r'[\d]{4}\/[\d]{4}', token) or
              re.match(r'[\d]{4}[ A-z/]*', token)):
            # The season as winner ou runner-up
            if state.lower() == 'winner':
                seasons_winning.append(token)
            else:
                seasons_running.append(token)
        elif token.lower() in ('winner', 'runner-up'):
            # He was in a competition
            state = token
        else:
            # will be name of the competition
            if not flag:
                titles['Win'] = seasons_winning
                titles['Runner-Up'] = seasons_running
                seasons_winning, seasons_running = [], []
                info.append(titles)
                state = None

            flag = False
            titles = {}
            titles['League'] = token.replace('  ', '')

    sideline = {}
    # sideline['Competitions'] = info Here we can get all competition historys
    win, lose = 0, 0
    for competition in info:
        win += len(competition['Win'])
        lose += len(competition['Runner-Up'])

    sideline['Win Comp.'] = str(win)
    sideline['Lose Comp.'] = str(lose)

    return sideline


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
        ans = parser.retrieve_in_tags('>', '<', position)
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

    return parser.parse_date(date)


def _get_edition_release(page):
    """Returns the edition and release of FIFA"""
    token = 'class="bp3-tag bp3-minimal bp3-intent-success">'
    aux = parser.retrieve_in_tags(token, '<', page)[0]
    aux = aux.split(' ')

    aux.pop(0)  # Removing the tag FIFA
    aux.pop(0)  # Removing the edition

    return parser.parse_date(' '.join(aux))


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
    info['Team'] = parser.retrieve_in_tags(">", "<", page)

    token = r'class="pos pos[\d]*">'
    token = re.compile(token)
    info['Team Position'] = parser.retrieve_in_tags(token,
                                                    '<', page)

    token = r'span class="bp3-tag p p[\d]*">'
    token = re.compile(token)
    info['Team Skill'] = parser.retrieve_in_tags(token, '<',
                                                 page)

    token = "Jersey Number</label>"
    info['Jersey'] = parser.retrieve_in_tags(token, "<", page)

    token = "Joined</label>"
    info['Joined'] = parser.retrieve_in_tags(token, '<', page)
    info['Joined'] = parser.parse_date(info['Joined'])

    token = "Contract Valid Until</label>"
    info['Contract'] = parser.retrieve_in_tags(token, '<', page)

    info = _set_none(info)

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
    """Parse players skills . """
    skills = parser.retrieve_in_tags('>', '<', page)

    skills = list(filter(lambda x: x != " " and
                         (re.match(r'[\d]+', x)
                          or re.match(r'[A-z ]+', x)),
                         skills))

    info = {}
    index = 0
    while index < len(skills) - 1:
        if skills[index + 1][0] == ' ':
            info[skills[index+1][1:]] = skills[index]
        else:
            info[skills[index+1]] = skills[index]
        index = index + 2

    return info


def get_pages_changes(player_id):
    """Get all changelinks of a player."""
    link = parser.mount_player_changelog_link(player_id)
    page = parser.get_page(link)

    token = '/player/' + str(player_id) + '/'
    token += r'[A-z\-]+\/[\d]+\/[\d]+\/'
    token = re.compile(token)

    links = set(parser.get_unparsed_text(page, token))
    releases = list(map(lambda x: x.split('/')[-2], links))
    edition = list(map(lambda x: x.split('/')[-3], links))

    dict_logs = {}
    for index, release in enumerate(releases):
        # {release:version}
        dict_logs[release] = edition[index]

    return dict_logs
