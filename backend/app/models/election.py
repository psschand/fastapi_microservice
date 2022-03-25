from tokenize import String
from typing import Optional
from enum import Enum
from datetime import datetime
from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from typing import List
from app.models.core import IDModelMixin, CoreModel
# from sqlalchemy import Column, Integer, String
# from sqlalchemy.dialects.postgresql import ARRAY
# from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, constr
from typing import (
    Deque, Dict, FrozenSet, List, Optional, Sequence, Set, Tuple, Union
)

# Base = declarative_base()

# class PartyType(str, Enum):
#     C = "Conservative"
#     L = "Labour"
#     SNP = "Scottish National Party"
#     LD = "Liberal Democrats"
#     G = "Green Party"
#     Ind = "Independent"

# class ConstituencyOrm(Base):
#     __tablename__ = 'constituencies'
#     id = Column(Integer, primary_key=True,autoincrement=True)
#     name: Column(String)
#     votesdata: Column(Integer,nullable=True)
#     winnervotes:  Column(Integer,nullable=True)
#     winnerparty:  Column(String,nullable=True)




class ConstituencyModel(BaseModel):
    # id:Optional[int] = None
    name: Optional[str] = None
    votesdata:Optional[str] = None
    
    winnervotes: Optional[int] = None
    winnerparty: Optional[str] = None

    # class Config:
    #     orm_mode = True

class ConstituencyPublic(IDModelMixin, ConstituencyModel):
    pass

class ConstituencyInDB(IDModelMixin, ConstituencyModel):
    id:Optional[int] = None
    name: Optional[str] = None
    votesdata:Optional[str] = None
    winnervotes: Optional[int] = None
    winnerparty: Optional[str] = None
# class PartyOrm(Base):
#     __tablename__ = 'party'
#     id = Column(Integer, primary_key=True,autoincrement=True)
#     party:  Column(String)
#     party_total_votes:  Column(Integer)
#     party_mp_number:  Column(Integer)
  



class PartyModel(BaseModel):
    """
    All common characteristics of  party resource
    """
    # id : Optional[int] = None
    name: Optional[str] = None
    party_total_votes: Optional[int] = None
    party_mp_number:Optional[int] = None

    # class Config:
    #     orm_mode = True

class MPPartyModel(BaseModel):
    """
    All common characteristics of  mps resource
    """

    name: Optional[str] = None
    party_mp_number:Optional[int] = None

class VotesPartyModel(BaseModel):
    """
    All common characteristics of  party resource
    """
    name: Optional[str] = None
    party_total_votes: Optional[int] = None
 

