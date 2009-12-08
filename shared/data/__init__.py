# coding: utf-8
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
#ändra echo till false om du inte vill se SQL kod

from sqlalchemy.orm import sessionmaker
from defs import *

_session = None
_engine = None
_dbfile = None

def get_session(db="sqlite:///client/db.db", echo=False):
    global _session, _engine
    if _dbfile is None or _dbfile != db:
        # new db
        _engine = create_engine(db, echo=echo)
        # worksade inte: :S
        #_session = sessionmaker(bind=_engine, expire_on_commit=False)()
        _session = sessionmaker(bind=_engine)()
    return _session

def create_tables():
    global _engine
    from defs import Base
    if _engine is None:
        print "är none"
        get_session()
    Base.metadata.create_all(_engine)

if __name__ == '__main__':
    # lite tester

    print "hax"
