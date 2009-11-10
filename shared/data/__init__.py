from sqlalchemy import create_engine
#ändra echo till false om du inte vill se SQL kod
engine = create_engine('sqlite:///tutorial.db', echo=True)

import defs
from sqlalchemy.orm import sessionmaker

if __name__ == '__main__':
    # lite tester

    print "hax"
