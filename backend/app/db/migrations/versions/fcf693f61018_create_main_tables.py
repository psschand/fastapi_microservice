"""create_main_tables

Revision ID: fcf693f61018
Revises:
Create Date: 2021-01-16 17:12:20.667046
filename: fcf693f61018_create_main_tables.py

"""
from alembic import op
import sqlalchemy as sa
import json



# def serializeList(entity) -> list:
#     return [{a:str(entity[a])} for a in entity]
    
def dict_to_json(value: dict):
  
    # CONVERT DICT TO A JSON STRING AND RETURN
    return json.dumps(value)


# revision identifiers, used by Alembic
revision = "fcf693f61018"
down_revision = None
branch_labels = None
depends_on = None


def create_constituency_table() -> None:


    party_table=op.create_table(
        "party",
        sa.Column('id', sa.Integer, primary_key=True,autoincrement=True),
        sa.Column("party", sa.Text, nullable=True),
        sa.Column("party_total_votes", sa.Numeric(10, 2), nullable=True),
        sa.Column("party_mp_number", sa.Numeric(10, 2), nullable=False),
    )


    constituency_table=op.create_table(
        "constituencies",
        # sa.Column('id', sa.Integer, primary_key=True,autoincrement=True),
        sa.Column("name", sa.Text),
        sa.Column("votesdata", sa.Text, nullable=True),
        sa.Column("winnervotes", sa.Numeric(10, 2), nullable=True),
        sa.Column("winnerparty", sa.Text, nullable=True),
    )
 
    op.create_table(
        'companies',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False),
    )

    op.create_table(
        'jobs',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('description', sa.String(), nullable=False),
        sa.Column('title', sa.String(100), nullable=False),
        sa.Column('company_id', sa.Integer, nullable=False),
        sa.ForeignKeyConstraint(('company_id',), ['companies.id'], ),
    )


    op.bulk_insert(
        party_table,
        [
        {"name": 'C', "party_total_votes": 24245425, "party_mp_number": 29},
        {"name": 'L', "party_total_votes": 353535, "party_mp_number": 19},
    ]
    )
    op.bulk_insert(
        constituency_table,
        [
        {"name": "Cardiff", "votesdata": dict_to_json({'C':1212, 'L':35345, 'UKIP':24242, 'LD':3563}), "winnervotes": 35345, "winnerparty": 'L'},
        {"name": "Wales", "votesdata": dict_to_json({'C':12312, 'L':35342, 'UKIP':12424, 'LD':32563}), "winnervotes": 35342, "winnerparty": 'L'},
    ]
    )


def upgrade() -> None:
    create_constituency_table()


def downgrade() -> None:
    op.drop_table("constituencies")
