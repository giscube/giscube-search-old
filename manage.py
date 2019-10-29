""" Module for managing tasks through cli interface. """
from manager import Manager

from app import create_app
from app.models.document_index import create_table, drop_table


manager = Manager()


@manager.command
def create_index(name):
    """ Create index. """
    res = create_table(name)
    print(res)


@manager.command
def drop_index(name):
    """ Drop index. """
    res = drop_table(name)
    print(res)


@manager.command
def run():
    """ Starts server on port 8000. """
    create_app()


if __name__ == '__main__':
    manager.main()
