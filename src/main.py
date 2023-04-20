import sys
sys.path.insert(1, "./")  # Sets 'src' directory as sources root

from controllers import legislators_votes

if __name__ == "__main__":
    legislators_votes()