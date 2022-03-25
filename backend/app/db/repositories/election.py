from app.db.repositories.base import BaseRepository
from app.models.election import PartyModel, ConstituencyModel,ConstituencyPublic,ConstituencyInDB
import json
import pandas 
from app.core.config import DATABASE_URL,POSTGRES_USER,POSTGRES_PASSWORD,POSTGRES_SERVER,POSTGRES_PORT , POSTGRES_DB

from sqlalchemy import create_engine

connect = "postgresql+psycopg2://%s:%s@%s:5432/%s" % (POSTGRES_USER,POSTGRES_PASSWORD,POSTGRES_SERVER,POSTGRES_DB )

def json_to_dict(value: str):
  
    # CONVERT json string to Dict RETURN
    return json.loads(value)

GET_ELECTIONRESULT_BY_NAME_QUERY = """
    SELECT name, votesdata, winnervotes, winnerparty
    FROM constituencies
    WHERE name = :name;
"""

GET_ELECTIONRESULT_VOTES_BY_Party_QUERY = """
    SELECT name, party_total_votes
    FROM party
    WHERE name = :name;
"""

GET_ELECTIONRESULT_MP_BY_Party_QUERY = """
    SELECT name, party_mp_number
    FROM party
    WHERE name = :name;
"""
def to_alchemy(df,tablename):
        """
        Using a dummy table to test this call library
        POSTGRES_USER,POSTGRES_PASSWORD,POSTGRES_SERVER,POSTGRES_PORT , POSTGRES_DB
        """
        print(DATABASE_URL)
        engine = create_engine(connect)
        
        
        df.to_sql(
            tablename,
            con=engine, 
            index=False, 
            if_exists='replace'
        )
        print("to_sql() done (sqlalchemy)")

class ConstituencyRepository(BaseRepository):
    """"
    All database actions associated with the constituency resource
    """

 

    async def get_constituency_by_Name(self, *, name: str) -> ConstituencyModel:
        constituency = await self.db.fetch_one(query=GET_ELECTIONRESULT_BY_NAME_QUERY, values={"name": name})


        if not constituency:
            return None

        return ConstituencyModel(**constituency)


class PartyRepository(BaseRepository):
    """"
    All database actions associated with the party resource
    """        

    async def get_votes_by_party(self, *, name: str) -> PartyModel:
        party = await self.db.fetch_one(query=GET_ELECTIONRESULT_VOTES_BY_Party_QUERY, values={"name": name})

        # print("-----------------------",party)
        # for k,v in party.items():
        #     print(k,v)
        if not party:
            return None

        return PartyModel(**party)   

    async def get_mp_by_party(self, *, name: str) -> PartyModel:
        party = await self.db.fetch_one(query=GET_ELECTIONRESULT_MP_BY_Party_QUERY, values={"name": name})


         
        if not party:
            return None

        return PartyModel(**party)   


        
    #----------------------------------------------------------------
    # SqlAlchemy Only
    #----------------------------------------------------------------

    



# postgresql://postgres:postgres@db:5432/postgres