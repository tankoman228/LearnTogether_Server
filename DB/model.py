import datetime

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, DateTime, Date, Float, Time
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import declarative_base, relationship, registry, backref

Base = declarative_base()


class Role(Base):
    __tablename__ = 'Role'

    ID_Role = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(128), unique=True, nullable=False)
    IsAdmin = Column(Boolean, nullable=False)
    AdminLevel = Column(Integer, default=64)

    permissions = relationship("Permission", backref="role", passive_deletes=True)


class Permission(Base):
    __tablename__ = 'Permission'

    ID = Column(Integer, primary_key=True, autoincrement=True)
    ID_Role = Column(Integer, ForeignKey('Role.ID_Role', ondelete='CASCADE'), nullable=False)
    Name = Column(String(64), nullable=False)


class Group(Base):
    __tablename__ = 'Group'

    ID_Group = Column(Integer, primary_key=True, autoincrement=True)
    ID_BasicRole = Column(Integer, ForeignKey('Role.ID_Role', ondelete='SET NULL'))
    Name = Column(String(50), unique=True, nullable=False)
    Icon = Column(Text)
    Description = Column(Text)

    basic_role = relationship("Role", backref=backref("groups", uselist=True), foreign_keys=[ID_BasicRole])


class Account(Base):
    __tablename__ = 'Account'

    ID_Account = Column(Integer, primary_key=True, autoincrement=True)
    Username = Column(String(70), unique=True, nullable=False)
    Password = Column(Text, nullable=False)
    RecoveryContact = Column(String(60))
    Title = Column(String(70), nullable=False)
    Icon = Column(Text)
    About = Column(Text)
    Rating = Column(Integer, default=0)
    LastSeen = Column(DateTime, default=datetime.datetime.utcnow)

    account_groups = relationship("AccountGroup", backref="account", passive_deletes=True)


class AccountGroup(Base):
    __tablename__ = 'AccountGroup'

    ID = Column(Integer, primary_key=True, autoincrement=True)
    ID_Group = Column(Integer, ForeignKey('Group.ID_Group', ondelete='CASCADE'), nullable=False)
    ID_Account = Column(Integer, ForeignKey('Account.ID_Account', ondelete='CASCADE'), nullable=False)
    ID_Role = Column(Integer, ForeignKey('Role.ID_Role', ondelete='SET NULL'))

    group = relationship("Group", backref="account_groups", passive_deletes=True)
    role = relationship("Role", backref="account_groups", foreign_keys=[ID_Role])


class RegisterToken(Base):
    __tablename__ = 'RegisterToken'

    ID_RegisterToken = Column(Integer, primary_key=True, autoincrement=True)
    ID_Group = Column(Integer, ForeignKey('Group.ID_Group', ondelete='CASCADE'), nullable=False)
    Text = Column(Text, unique=True, nullable=False)
    ID_Role = Column(Integer, ForeignKey('Role.ID_Role', ondelete='SET NULL'))

    group = relationship("Group", backref=backref("register_tokens", uselist=True), passive_deletes=True)
    role = relationship("Role", backref=backref("register_tokens", uselist=True), foreign_keys=[ID_Role])


class Recovery(Base):
    __tablename__ = 'Recovery'

    ID_Recovery = Column(Integer, primary_key=True, autoincrement=True)
    ID_Account = Column(Integer, ForeignKey('Account.ID_Account', ondelete='CASCADE'), nullable=False)
    Hash = Column(Text)
    WaitingForGeneration = Column(Boolean, nullable=False)


class Tag(Base):
    __tablename__ = 'Tag'

    ID_Tag = Column(Integer, primary_key=True, autoincrement=True)
    Text = Column(String(32), nullable=False, unique=True)


class InfoBase(Base):
    __tablename__ = 'InfoBase'

    ID_InfoBase = Column(Integer, primary_key=True, autoincrement=True)
    ID_Group = Column(Integer, ForeignKey('Group.ID_Group', ondelete='CASCADE'), nullable=False)
    ID_Account = Column(Integer, ForeignKey('Account.ID_Account', ondelete='SET NULL'))
    Title = Column(String(150), nullable=False)
    Text = Column(Text)
    Type = Column(String(1)) # a = ask,
    WhenAdd = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    Rate = Column(Float, nullable=False, default=0.0)

    account = relationship("Account")

    tags = relationship("InfoTag", backref="infobase", passive_deletes=True)
    forum_ask = relationship("ForumAsk", uselist=False, back_populates="infobase")
    news = relationship("News", uselist=False, back_populates="infobase")
    task = relationship("Task", uselist=False, back_populates="infobase")
    information = relationship("Information", uselist=False, back_populates="infobase")
    meeting = relationship("Meeting", uselist=False, back_populates="infobase")
    votes = relationship("Vote", backref="infobase", passive_deletes=True)


class InfoTag(Base):
    __tablename__ = 'InfoTag'

    ID_InfoTag = Column(Integer, primary_key=True, autoincrement=True)
    ID_Tag = Column(Integer, ForeignKey('Tag.ID_Tag', ondelete='CASCADE'), nullable=False)
    ID_InfoBase = Column(Integer, ForeignKey('InfoBase.ID_InfoBase', ondelete='CASCADE'), nullable=False)

    tag = relationship("Tag", backref="info_tags", passive_deletes=True)


class ForumAsk(Base):
    __tablename__ = 'ForumAsk'

    ID_ForumAsk = Column(Integer, primary_key=True, autoincrement=True)
    ID_InfoBase = Column(Integer, ForeignKey('InfoBase.ID_InfoBase', ondelete='CASCADE'), nullable=False)
    Solved = Column(Boolean, default=False)

    infobase = relationship("InfoBase", back_populates="forum_ask")


class News(Base):
    __tablename__ = 'News'

    ID_News = Column(Integer, primary_key=True, autoincrement=True)
    ID_InfoBase = Column(Integer, ForeignKey('InfoBase.ID_InfoBase', ondelete='CASCADE'), nullable=False)
    Images = Column(Text)
    Moderated = Column(Boolean, default=False)

    infobase = relationship("InfoBase", back_populates="news")


class Task(Base):
    __tablename__ = 'Task'

    ID_Task = Column(Integer, primary_key=True, autoincrement=True)
    ID_InfoBase = Column(Integer, ForeignKey('InfoBase.ID_InfoBase', ondelete='CASCADE'), nullable=False)
    Deadline = Column(DateTime)
    Moderated = Column(Boolean, default=False)

    infobase = relationship("InfoBase", back_populates="task")


class TaskAccount(Base):
    __tablename__ = 'TaskAccount'

    ID = Column(Integer, primary_key=True, autoincrement=True)
    ID_Account = Column(Integer, ForeignKey('Account.ID_Account', ondelete='CASCADE'), nullable=False)
    NeedHelp = Column(Boolean, nullable=False)
    Finished = Column(Boolean, nullable=False)
    Priority = Column(Integer, nullable=False)
    Progress = Column(Integer, nullable=False)

    account = relationship("Account", backref="task_accounts", passive_deletes=True)


class Information(Base):
    __tablename__ = 'Information'

    ID_Information = Column(Integer, primary_key=True, autoincrement=True)
    ID_InfoBase = Column(Integer, ForeignKey('InfoBase.ID_InfoBase', ondelete='CASCADE'), nullable=False)
    Contents = Column(Text)
    Type = Column(String(1))

    infobase = relationship("InfoBase", back_populates="information")


class Meeting(Base):
    __tablename__ = 'Meeting'

    ID_Meeting = Column(Integer, primary_key=True, autoincrement=True)
    ID_InfoBase = Column(Integer, ForeignKey('InfoBase.ID_InfoBase', ondelete='CASCADE'), nullable=False)
    Starts = Column(DateTime, nullable=False)
    Place = Column(String(30))

    infobase = relationship("InfoBase", back_populates="meeting")
    responses = relationship("MeetingRespond", backref="meeting", passive_deletes=True)


class MeetingRespond(Base):
    __tablename__ = 'MeetingRespond'

    ID = Column(Integer, primary_key=True, autoincrement=True)
    ID_Meeting = Column(Integer, ForeignKey('Meeting.ID_Meeting', ondelete='CASCADE'), nullable=False)
    ID_Account = Column(Integer, ForeignKey('Account.ID_Account', ondelete='CASCADE'), nullable=False)
    Surety = Column(Float, nullable=False)
    Start = Column(Time, nullable=False)
    End = Column(Time, nullable=False)
    Reason = Column(String(100))

    account = relationship("Account", backref="meeting_responds", passive_deletes=True)


class Vote(Base):
    __tablename__ = 'Vote'

    ID_Vote = Column(Integer, primary_key=True, autoincrement=True)
    ID_InfoBase = Column(Integer, ForeignKey('InfoBase.ID_InfoBase', ondelete='CASCADE'), nullable=False)
    Anonymous = Column(Boolean, nullable=False)
    MultAnswer = Column(Boolean, nullable=False)

    items = relationship("VoteItem", backref="vote", passive_deletes=True)


class VoteItem(Base):
    __tablename__ = 'VoteItem'

    ID_VoteItem = Column(Integer, primary_key=True, autoincrement=True)
    ID_Vote = Column(Integer, ForeignKey('Vote.ID_Vote', ondelete='CASCADE'), nullable=False)
    Title = Column(String(20))

    vote_accounts = relationship("VoteAccount", backref="vote_item", passive_deletes=True)


class VoteAccount(Base):
    __tablename__ = 'VoteAccount'

    ID = Column(Integer, primary_key=True, autoincrement=True)
    ID_VoteItem = Column(Integer, ForeignKey('VoteItem.ID_VoteItem', ondelete='CASCADE'), nullable=False)
    ID_Account = Column(Integer, ForeignKey('Account.ID_Account', ondelete='CASCADE'), nullable=False)

    account = relationship("Account", backref="vote_accounts", passive_deletes=True)


class Comment(Base):
    __tablename__ = 'Comment'

    ID_Comment = Column(Integer, primary_key=True, autoincrement=True)
    ID_InfoBase = Column(Integer, ForeignKey('InfoBase.ID_InfoBase', ondelete='CASCADE'), nullable=False)
    ID_Account = Column(Integer, ForeignKey('Account.ID_Account', ondelete='CASCADE'), nullable=False)

    Text = Column(Text)
    Attachments = Column(LONGTEXT)
    WhenAdd = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)

    infobase = relationship("InfoBase", backref="comments", passive_deletes=True)
    account = relationship("Account")


class Rank(Base):
    __tablename__ = 'Rank'

    ID_Rank = Column(Integer, primary_key=True, autoincrement=True)
    ID_InfoBase = Column(Integer, ForeignKey('InfoBase.ID_InfoBase', ondelete='CASCADE'), nullable=False)
    ID_Account = Column(Integer, ForeignKey('Account.ID_Account', ondelete='CASCADE'), nullable=False)

    Value = Column(Integer)

    infobase = relationship("InfoBase", backref="rates", passive_deletes=True)
    account = relationship("Account")


class Complaint(Base):
    __tablename__ = 'Complaint'

    ID_Complaint = Column(Integer, primary_key=True, autoincrement=True)
    ID_Group = Column(Integer, ForeignKey('Group.ID_Group', ondelete='CASCADE'), nullable=False)
    Sender = Column(Integer, ForeignKey('Account.ID_Account', ondelete='CASCADE'), nullable=False)
    Suspected = Column(Integer, ForeignKey('Account.ID_Account', ondelete='CASCADE'), nullable=False)
    Reason = Column(String(400))
    DateTime = Column(DateTime)
    Moderated = Column(Boolean, default=0)

    group = relationship("Group", backref="complaints", passive_deletes=True)
    sender = relationship("Account", foreign_keys=[Sender], backref="sent_complaints", passive_deletes=True)
    suspected = relationship("Account", foreign_keys=[Suspected], backref="received_complaints", passive_deletes=True)
