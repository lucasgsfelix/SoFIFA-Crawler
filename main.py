""" Responsible for the calling of functions. """
import player


if __name__ == '__main__':

    with open("Input/players_list.txt", 'r') as file:
        players = file.read().split('\n')
        players.pop(0) # removing header

        # 0 - players name, 1 - players id
        players = list(map(lambda x: x.split('\t'),
                                             players))

    for player in players:

        logs = player.get_pages_changes(players[1])
        for log in logs:
            # player id, player name, edition, release
            player_info = parser.get_players_info(player[1],
                                    player[0], logs[log], log)


    