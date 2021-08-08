import importlib
import prisoners_dilemma
from os import getcwd, listdir
from os.path import join, isfile


path = join(getcwd(), 'bots')


if __name__ == '__main__':
    judge = prisoners_dilemma.Judge()

    print("prisoners_dilemma: Reading bots files")

    for file in listdir(path):
        if not isfile(join(path, file)):
            continue

        file_id, file_ext = file.split('.')

        if (file_ext == 'py') and (file_id not in ["__init__", "base"]):
            print("prisoners_dilemma: processing", file)

            mod = importlib.import_module('bots.'+file_id)
            bot = getattr(mod, 'Bot')
            judge.register_player(bot)

    for match in judge.matches():
        match.play()
        print(match.result)
