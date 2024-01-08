import datetime

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, DateTime, Date, Float, Time
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import declarative_base, relationship, registry

Base = declarative_base()


class Role(Base):
    __tablename__ = 'Role'

    ID_Role = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(128), unique=True, nullable=False)
    IsAdmin = Column(Boolean, nullable=False)
    AdminLevel = Column(Integer, default=64)

    permissions = relationship("Permission", backref="role_associated")

class Permission(Base):
    __tablename__ = 'Permission'

    ID = Column(Integer, primary_key=True, autoincrement=True)
    ID_Role = Column(Integer, ForeignKey('Role.ID_Role', ondelete='CASCADE'), nullable=False)
    Name = Column(String(64), nullable=False)

    role = relationship("Role", back_populates="permissions")


class Group(Base):
    __tablename__ = 'Group'

    ID_Group = Column(Integer, primary_key=True, autoincrement=True)
    ID_BasicRole = Column(Integer, ForeignKey('Role.ID_Role', ondelete='SET NULL'))
    Name = Column(String(50), unique=True, nullable=False)
    Icon = Column(Text)
    Description = Column(Text)

    basic_role = relationship("Role", backref="roles")
    accountgroups = relationship("AccountGroup", backref="group_associated")

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

    # vote_accounts = relationship("VoteAccount", back_populates="account")
    # sender_complaints = relationship("Complaint", foreign_keys=[Complaint.Sender], back_populates="sender_account")
    # suspected_complaints = relationship("Complaint", foreign_keys=[Complaint.Suspected],
    #                                    back_populates="suspected_account")
    accountgroups = relationship("AccountGroup", backref="account_associated")

class AccountGroup(Base):
    __tablename__ = 'AccountGroup'

    ID = Column(Integer, primary_key=True, autoincrement=True)
    ID_Group = Column(Integer, ForeignKey('Group.ID_Group', ondelete='CASCADE'), nullable=False)
    ID_Account = Column(Integer, ForeignKey('Account.ID_Account', ondelete='CASCADE'), nullable=False)
    ID_Role = Column(Integer, ForeignKey('Role.ID_Role', ondelete='SET NULL'))

    account = relationship("Account", back_populates="accountgroups")
    group = relationship("Group", back_populates="accountgroups")
    role = relationship("Role", back_populates="roles")


class RegisterToken(Base):
    __tablename__ = 'RegisterToken'

    ID_RegisterToken = Column(Integer, primary_key=True, autoincrement=True)
    ID_Group = Column(Integer, ForeignKey('Group.ID_Group', ondelete='CASCADE'), nullable=False)
    Text = Column(Text, unique=True, nullable=False)
    ID_Role = Column(Integer, ForeignKey('Role.ID_Role', ondelete='SET NULL'))

    group = relationship("Group", back_populates="tokens")
    role = relationship("Role")


class Recovery(Base):
    __tablename__ = 'Recovery'

    ID_Recovery = Column(Integer, primary_key=True, autoincrement=True)
    ID_Account = Column(Integer, ForeignKey('Account.ID_Account', ondelete='CASCADE'), nullable=False)
    Hash = Column(Text)
    WaitingForGeneration = Column(Boolean, nullable=False)

    account = relationship("Account", back_populates="recoveries")


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
    Type = Column(String(1))
    DateAdd = Column(Date, nullable=False)

    group = relationship("Group", back_populates="infos")
    account = relationship("Account", back_populates="infos")
    tags = relationship("Tag", secondary="InfoTag")


class InfoTag(Base):
    __tablename__ = 'InfoTag'

    ID_InfoTag = Column(Integer, primary_key=True, autoincrement=True)
    ID_Tag = Column(Integer, ForeignKey('Tag.ID_Tag', ondelete='CASCADE'), nullable=False)
    ID_InfoBase = Column(Integer, ForeignKey('InfoBase.ID_InfoBase', ondelete='CASCADE'), nullable=False)

    tag = relationship("Tag")
    info = relationship("InfoBase", back_populates="tags")


class ForumAsk(Base):
    __tablename__ = 'ForumAsk'

    ID_ForumAsk = Column(Integer, primary_key=True, autoincrement=True)
    ID_InfoBase = Column(Integer, ForeignKey('InfoBase.ID_InfoBase', ondelete='CASCADE'), nullable=False)
    Solved = Column(Boolean, default=False)

    info = relationship("InfoBase", back_populates="forum_asks")


class News(Base):
    __tablename__ = 'News'

    ID_News = Column(Integer, primary_key=True, autoincrement=True)
    ID_InfoBase = Column(Integer, ForeignKey('InfoBase.ID_InfoBase', ondelete='CASCADE'), nullable=False)
    Images = Column(Text)
    Moderated = Column(Boolean, default=False)

    info_base = relationship("InfoBase", back_populates="news")


class Task(Base):
    __tablename__ = 'Task'

    ID_Task = Column(Integer, primary_key=True, autoincrement=True)
    ID_InfoBase = Column(Integer, ForeignKey('InfoBase.ID_InfoBase', ondelete='CASCADE'), nullable=False)
    Deadline = Column(DateTime)
    Moderated = Column(Boolean, default=False)

    info_base = relationship("InfoBase", back_populates="tasks")


class TaskAccount(Base):
    __tablename__ = 'TaskAccount'

    ID = Column(Integer, primary_key=True, autoincrement=True)
    ID_Account = Column(Integer, ForeignKey('Account.ID_Account', ondelete='CASCADE'), nullable=False)
    NeedHelp = Column(Boolean, nullable=False)
    Finished = Column(Boolean, nullable=False)
    Priority = Column(Integer, nullable=False)
    Progress = Column(Integer, nullable=False)

    account = relationship("Account", back_populates="task_accounts")


class Information(Base):
    __tablename__ = 'Information'

    ID_Information = Column(Integer, primary_key=True, autoincrement=True)
    ID_InfoBase = Column(Integer, ForeignKey('InfoBase.ID_InfoBase', ondelete='CASCADE'), nullable=False)
    Contents = Column(Text)
    Type = Column(String(1))

    info_base = relationship("InfoBase", back_populates="information")


class Meeting(Base):
    __tablename__ = 'Meeting'

    ID_Meeting = Column(Integer, primary_key=True, autoincrement=True)
    ID_InfoBase = Column(Integer, ForeignKey('InfoBase.ID_InfoBase', ondelete='CASCADE'), nullable=False)
    Starts = Column(DateTime, nullable=False)
    Place = Column(String(30))

    info_base = relationship("InfoBase", back_populates="meetings")


class MeetingRespond(Base):
    __tablename__ = 'MeetingRespond'

    ID = Column(Integer, primary_key=True, autoincrement=True)
    ID_Meeting = Column(Integer, ForeignKey('Meeting.ID_Meeting', ondelete='CASCADE'), nullable=False)
    ID_Account = Column(Integer, ForeignKey('Account.ID_Account', ondelete='CASCADE'), nullable=False)
    Surety = Column(Float, nullable=False)
    Start = Column(Time, nullable=False)
    End = Column(Time, nullable=False)
    Reason = Column(String(100))

    account = relationship("Account", back_populates="meeting_responds")
    meeting = relationship("Meeting", back_populates="meeting_responds")


class Vote(Base):
    __tablename__ = 'Vote'

    ID_Vote = Column(Integer, primary_key=True, autoincrement=True)
    ID_InfoBase = Column(Integer, ForeignKey('InfoBase.ID_InfoBase', ondelete='CASCADE'), nullable=False)
    Anonymous = Column(Boolean, nullable=False)
    MultAnswer = Column(Boolean, nullable=False)

    info_base = relationship("InfoBase", back_populates="votes")


class VoteItem(Base):
    __tablename__ = 'VoteItem'

    ID_VoteItem = Column(Integer, primary_key=True, autoincrement=True)
    ID_Vote = Column(Integer, ForeignKey('Vote.ID_Vote', ondelete='CASCADE'), nullable=False)
    Title = Column(String(20))

    vote = relationship("Vote", back_populates="vote_items")


class VoteAccount(Base):
    __tablename__ = 'VoteAccount'

    ID = Column(Integer, primary_key=True, autoincrement=True)
    ID_VoteItem = Column(Integer, ForeignKey('VoteItem.ID_VoteItem', ondelete='CASCADE'), nullable=False)
    ID_Account = Column(Integer, ForeignKey('Account.ID_Account', ondelete='CASCADE'), nullable=False)

    vote_item = relationship("VoteItem", back_populates="vote_accounts")
    account = relationship("Account", back_populates="vote_accounts")


class Comment(Base):
    __tablename__ = 'Comment'

    ID_Comment = Column(Integer, primary_key=True, autoincrement=True)
    ID_InfoBase = Column(Integer, ForeignKey('InfoBase.ID_InfoBase', ondelete='CASCADE'), nullable=False)
    Rank = Column(Integer, nullable=False)
    Text = Column(Text)
    Attachments = Column(LONGTEXT)

    info_base = relationship("InfoBase", back_populates="comments")


class Complaint(Base):
    __tablename__ = 'Complaint'

    ID_Complaint = Column(Integer, primary_key=True, autoincrement=True)
    ID_Group = Column(Integer, ForeignKey('Group.ID_Group', ondelete='CASCADE'), nullable=False)
    Sender = Column(Integer, ForeignKey('Account.ID_Account', ondelete='CASCADE'), nullable=False)
    Suspected = Column(Integer, ForeignKey('Account.ID_Account', ondelete='CASCADE'), nullable=False)
    Reason = Column(String(400))
    DateTime = Column(DateTime)
    Moderated = Column(Boolean, default=0)

    group = relationship("Group", back_populates="complaints")
    sender_account = relationship("Account", foreign_keys=[Sender])
    suspected_account = relationship("Account", foreign_keys=[Suspected])



