from bot import Locatransbot
from database.main import Database

# from mainFolder.folder2.file4 import Myclass


def main():
    Database.Base.metadata.create_all(Database.engine)
    bot = Locatransbot()
    bot.start()


if __name__ == '__main__':
    main()
