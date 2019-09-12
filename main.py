""" Responsible for the calling of functions. """
import parser
import player as pl
from header import PLAYERS as players_header


if __name__ == '__main__':

    with open("Input/players_list.txt", 'r') as file:
        PLAYERS = file.read().split('\n')
        PLAYERS.pop(0)  # removing header

        # 0 - players name, 1 - players id
        PLAYERS = list(map(lambda x: x.split('\t'),
                           PLAYERS))

    HEADER = True
    for player in PLAYERS:

        logs = pl.get_pages_changes(player[1])
        for log in logs:
            # player id, player name, edition, release
            if int(logs[log]) > 14:
                player_info = pl.get_players_info(player[1],
                                                  player[0], logs[log], log)

                parser.write_file(player_info, players_header,
                                  "Output/players_info.txt", HEADER)
                HEADER = False
