import json
from typing import List

import pandas as pd
from fastapi import APIRouter, Body, Depends, HTTPException, UploadFile,File

from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND

from app.models.election import PartyModel,ConstituencyModel,ConstituencyPublic,MPPartyModel,VotesPartyModel

from app.db.repositories.election import ConstituencyRepository,PartyRepository
from app.api.dependencies.database import get_repository
from app.api.dependencies.dataload import Convert
from app.db.repositories.election import to_alchemy


router = APIRouter()

def serializeList(entity) -> list:
    return [{a:str(entity[a])} for a in entity]

@router.get("/")
async def get_all_constituencies() -> List[dict]:
    constituencies = [
        {"name": "Cardiff", "votesdata": {'C':1212, 'L':35345, 'UKIP':24242, 'LD':3563}, "winnervotes": 35345, "winnerparty": 'L'},
        {"name": "Wales", "votesdata": {'C':12312, 'L':35342, 'UKIP':12424, 'LD':32563}, "winnervotes": 35342, "winnerparty": 'L'},
    ]

    return constituencies


@router.get("/{name}/",response_model=ConstituencyModel,  name="constituencies:get-constituency-by-name")
async def get_constituency_by_name(
    name: str, constituency_repo: ConstituencyRepository = Depends(get_repository(ConstituencyRepository))
) -> ConstituencyModel :
    constituency = await constituency_repo.get_constituency_by_Name(name=name)
    
    constituency.votesdata=constituency.votesdata.replace("\"", "");
    

    if not constituency:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="No constituency found with that id.")

    return constituency

@router.get("/votesperparty/{name}/",response_model=VotesPartyModel,  name="party:get-votes-per-party")
async def get_votes_per_party(
     name: str,party_repo: PartyRepository = Depends(get_repository(PartyRepository))
) -> VotesPartyModel :
    party = await party_repo.get_votes_by_party(name=name)
    print(party)
    if not party:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="No data for votes found .")

    return party


@router.get("/mpsperparty/{name}/",response_model=MPPartyModel,  name="party:get-mps-per-party")
async def get_mps_per_party(
     name: str,party_repo: PartyRepository = Depends(get_repository(PartyRepository))
) -> MPPartyModel :
    party = await party_repo.get_mp_by_party(name=name)
    print(party)
    if not party:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="No mp  found .")

    return party    


@router.post("/uploadcsv")
async def upload_new_datafile(csv_file: UploadFile = File(...)):
    df = pd.read_csv(csv_file.file,sep='\t', skiprows=0, header=None)
    
    print(df)

    li=[]    
    mpdict={'C':0,'L':0,'LD':0,'G':0,'IND':0,'SNP':0,'UKIP':0}
    votesdict={'C':0,'L':0,'LD':0,'G':0,'IND':0,'SNP':0,'UKIP':0}

    for index, row in df.iterrows():
        spr=row[0].split(",")
        datadict=Convert(spr[1:])
        keymax = max(datadict, key= lambda x: datadict[x])
        # print(Keymax)
        # print(datadict[Keymax])
        d={}
        d['name']=spr[0]
        d['votesdata']=json.dumps(datadict)
        d['winnervotes']=datadict[keymax]
        d['winnerparty']=keymax

        for k,v in datadict.items():
            votesdict[k.strip().upper()] = int(datadict[k]) + votesdict[k.strip().upper()]
        
        print(mpdict[keymax.strip().upper()])
        mpdict[keymax.strip().upper()] = mpdict[keymax.strip().upper()]+1

        li.append(d)
    # return json.loads(df.to_json())
    df_constituency = pd.DataFrame(li)
    to_alchemy(df_constituency,'constituencies')

    # party table
    li_party=[]
    for party in ['C','L','LD','G','IND','SNP','UKIP']:
        d_party={}
        d_party['name']=party
        d_party['party_mp_number']=mpdict[party]
        d_party['party_total_votes']=votesdict[party]
        li_party.append(d_party)
    df_party = pd.DataFrame(li_party)
    to_alchemy(df_party,'party')    
    
    return [li,li_party]
