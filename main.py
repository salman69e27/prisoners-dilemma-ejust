import importlib
from judge import Judge
from os import getcwd, listdir
from os.path import join, isfile

path = join(getcwd(), 'players')


def is_numerical(string):
    try:
        int(string)
        return True
    except ValueError:
        return False


if __name__ == '__main__':
    judge = Judge()
    for file in listdir(path):
        if not isfile(join(path, file)):
            continue
        print(file)
        file_id, file_ext = file.split('.')
        if is_numerical(file_id) and (file_ext == 'py'):
            mod = importlib.import_module('players.'+file_id)
            player = getattr(mod, 'Player')
            player.id = file_id
            judge.add_player(player())
    for match in judge.matches():
        match.play()
        print(match.result)
