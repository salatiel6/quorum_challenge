from file_handler import FileHandler


def legistators_votes():
    legistators = FileHandler.reader('../dataset/legislators.csv')
    vote_results = FileHandler.reader('../dataset/vote_results.csv')
