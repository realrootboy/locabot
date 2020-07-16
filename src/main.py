from bot import Locatransbot
from database.main import Database
from createDb import loadDb

# from mainFolder.folder2.file4 import Myclass


def main():
    loadDb()
    bot = Locatransbot()
    bot.start()


if __name__ == '__main__':
    main()
