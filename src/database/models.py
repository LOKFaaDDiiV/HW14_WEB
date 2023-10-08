from sqlalchemy import Column, Integer, String, Date, func, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Contact(Base):
    __tablename__ = 'contacts'
    id = Column("id", Integer, primary_key=True, index=True)
    firstname = Column("firstname", String(30))
    lastname = Column("lastname", String(30))
    phone_number = Column("phone", String(20))
    email = Column("email", String(40))
    born_date = Column("born_date", Date)
    user_id = Column('user_id', ForeignKey('users.id', ondelete='CASCADE'), default=None)
    user = relationship('User', backref="contacts")


class User(Base):
    __tablename__ = 'users'
    id = Column("id", Integer, primary_key=True)
    username = Column("username", String(50))
    email = Column("email", String(250), nullable=False, unique=True)
    password = Column("password", String(255), nullable=False)
    created_at = Column('created_at', DateTime, default=func.now())
    avatar = Column("avatar", String(255), nullable=True)
    refresh_token = Column("refresh_token", String(255), nullable=True)
    confirmed = Column(Boolean, default=False)
