from .Database_Engine import Base

from sqlalchemy import Column, String, UUID, Integer


class Roles_Table(Base):
    __tablename__ = "roles" 

    role_id = Column(Integer, 
                primary_key=True, 
                nullable=False)
    
    
    role_type = Column(String, nullable=False)

    

    
    
    