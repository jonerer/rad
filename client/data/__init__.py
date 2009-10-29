from sqlalchemy import create_engine

engine = create_engine("sqlite:///:memory:", echo=True)

import defs
from sqlalchemy.orm import sessionmaker

if __name__ == '__main__':
    # lite tester
    print "hax"
