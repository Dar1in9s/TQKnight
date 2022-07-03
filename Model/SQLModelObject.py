from sqlalchemy import create_engine, Column, String, Integer, Text, UnicodeText
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import time
from config import Config

engine = create_engine("sqlite:///" + Config.DbFile)
Base = declarative_base(engine)


class Webshell(Base):
    __tablename__ = "webshell"
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    url = Column(String(100))
    type = Column(String(20), default="php")
    time = Column(String(30))
    passwd = Column(String(100))
    proxyId = Column(Integer, default=0)
    groupId = Column(Integer)
    httpHeader = Column(UnicodeText, default="[]")
    note = Column(Text, default="")

    def __init__(self):
        self.id = None
        self.time = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
        self.proxyId = 0
        self.type = "PHP"
        self.httpHeader = "[]"

    def eq(self, webshell):
        if self.url == webshell.url and self.type == webshell.type and self.time == webshell.time:
            if self.passwd == webshell.passwd and self.proxyId == webshell.proxyId and self.groupId == webshell.groupId:
                if self.httpHeader == webshell.httpHeader:
                    if self.note == webshell.note:
                        return True
        return False

    def setValueByWebshell(self, webshell):
        self.url = webshell.url
        self.passwd = webshell.passwd
        self.time = webshell.time
        self.type = webshell.type
        self.note = webshell.note
        self.httpHeader = webshell.httpHeader
        self.proxyId = webshell.proxyId
        self.groupId = webshell.groupId


class Proxy(Base):
    __tablename__ = "proxy"
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    name = Column(String(50))
    protocol = Column(String(10))
    server = Column(String(100))
    port = Column(String(10))
    user = Column(String(20))
    passwd = Column(String(100))

    def eq(self, proxy):
        if self.name == proxy.name and self.protocol == proxy.protocol and self.server == proxy.server:
            if self.port == proxy.port and self.user == proxy.user and self.passwd == proxy.passwd:
                return True
        return False

    def setValueByProxy(self, proxy):
        self.name = proxy.name
        self.protocol = proxy.protocol
        self.server = proxy.server
        self.port = proxy.port
        self.user = proxy.user
        self.passwd = proxy.passwd


class Group(Base):
    __tablename__ = "group"
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    name = Column(String(50))


class SQL:
    @staticmethod
    def select(model, where):
        result = []
        try:
            session = sessionMaker()
            if where:
                result = session.query(model).filter_by(**where).all()
            else:
                result = session.query(model).all()
            session.close()
        except Exception as e:
            print(e)
        return result

    @staticmethod
    def delete(model, where):
        try:
            session = sessionMaker()
            session.query(model).filter_by(**where).delete()
            session.commit()
            session.close()
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def update(model, new, where):
        try:
            session = sessionMaker()
            session.query(model).filter_by(**where).update(new)
            session.commit()
            session.close()
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def insert(model):
        try:
            session = sessionMaker()
            session.add(model)
            session.commit()
            session.flush()
            _id = model.id
            session.close()
            return _id
        except Exception as e:
            print(e)
            return False


Base.metadata.create_all()
sessionMaker = sessionmaker(bind=engine)