""" Responsible for the calling of functions. """
import main
import player_comments


if __name__ == '__main__':

    PLAYERS = main.read_file()

    HEADER = True
    for player in PLAYERS:
        player_comments.get_comments(player[1])
        print("Terminou o jogador: ", player[0])
