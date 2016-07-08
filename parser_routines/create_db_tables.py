from engine import engine
from models import Base, City


def main():
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    main()
