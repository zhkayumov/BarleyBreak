# `random` module is used to shuffle field, see:
# https://docs.python.org/3/library/random.html#random.shuffle
import random
import signal
import sys

# Empty tile, there's only one empty cell on a field:
EMPTY_MARK = 'x'

# Dictionary of possible moves if a form of:
# key -> delta to move the empty tile on a field.
MOVES = {
    'w': -4,
    's': 4,
    'a': -1,
    'd': 1,
}


def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    sys.exit(0)


def shuffle_field():
    """
    This function is used to create a field at the very start of the game.

    :return: list with 16 randomly shuffled tiles,
        one of which is a empty space.
    """
    field = [i for i in range(0, 16)]
    random.shuffle(field)
    return field


def print_field(field):
    """
    This function prints field to user.

    :param field: current field state to be printed.
    :return: None

    """
    for n in range(0, 4):
        row = [EMPTY_MARK if str(i) == '0' else str(i) for i in field[n * 4: (n + 1) * 4]]
        # print(str(field[n * 4: (n + 1) * 4]).replace('0', EMPTY_MARK))
        print(
            row[0] + '\t'
            + row[1] + '\t'
            + row[2] + '\t'
            + row[3] + '\t'
        )


def is_game_finished(field):
    """
    This function checks if the game is finished.

    :param field: current field state.
    :return: True if the game is finished, False otherwise.
    """
    etalon = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]
    if field == etalon:
        return True
    else:
        return False


def swap_positions(field, pos1, pos2):
    # Storing the two elements
    # as a pair in a tuple variable get
    get = field[pos1], field[pos2]

    # unpacking those elements
    field[pos2], field[pos1] = get

    return field


def perform_move(field, key):
    """
    Moves empty-tile inside the field.

    :param field: current field state.
    :param key: move direction.
    :return: new field state (after the move).
    :raises: IndexError if the move can't me done.
    """
    user_move = MOVES[key]
    where_zero = 0
    for i in range(0, len(field)):
        if field[i] == 0:
            where_zero = i
            break
    if (key == 'a' and where_zero in (0, 4, 8, 12)) or \
            (key == 'w' and where_zero in (0, 1, 2, 3)) or \
            (key == 's' and where_zero in (15, 14, 13, 12)) or \
            (key == 'd' and where_zero in (3, 7, 11, 15)):
        raise IndexError
    new_field = swap_positions(field, where_zero, where_zero + user_move)
    return new_field


def handle_user_input():
    """
    Handles user input.

    List of accepted moves:
        'w' - up,
        's' - down,
        'a' - left,
        'd' - right

    :return: <str> current move.
    """
    aval_keys = ('a', 's', 'd', 'w')
    a = str(input())
    if a in aval_keys:
        return a
    else:
        raise KeyError


def main():
    """
    The main function. It starts when the program is called.

    It also calls other functions.
    :return: None
    """
    signal.signal(signal.SIGINT, signal_handler)
    field = shuffle_field()
    print_field(field)
    while 1:
        try:
            print('Enter wasd ')
            move = handle_user_input()
            perform_move(field, move)
        except IndexError:
            print('Incorrect move')
        except KeyError:
            print('Incorrect input')
        print_field(field)
        if is_game_finished(field):
            print('Game finished!')
            break


if __name__ == '__main__':
    # See what this means:
    # http://stackoverflow.com/questions/419163/what-does-if-name-main-do
    main()
