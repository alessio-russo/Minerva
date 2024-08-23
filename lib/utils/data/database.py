from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from lib.blog.section import Section
from lib.utils.data.base import Base
from sqlalchemy.pool import NullPool

class Database:
    _instance = None
    _engine = None
    _session = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance._init()
        return cls._instance

    def _init(self):
        self._engine = create_engine("sqlite+pysqlite:///:memory:", connect_args={'check_same_thread': False})
        # cls._instance._engine = create_engine("sqlite:///site_map.db")
        Base.metadata.create_all(bind=self._engine)
        Session = sessionmaker(bind=self._engine)
        self._session = Session()

    def create_record(self, record):
        self._session.add(record)
        self._session.commit()

    def print(self):
        return self._session.query(Section).all()

    @property
    def session(self):
        return self._session