from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()

class Vlan(Base):
	__tablename__ = 'vlan'

	id = Column(Integer, primary_key=True)
	vlan_id = Column(Integer, nullable=False)
	name = Column(String(250), nullable=False)
	description = Column(String(250), nullable=False)


#engine = create_engine('sqlite:///my_db.db')
#Base.metadata.create_all(engine)
