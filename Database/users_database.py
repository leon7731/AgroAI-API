from .Database_Engine import Base

from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, UUID


class Users_Table(Base):
    __tablename__ = "users" 

    email = Column(String, primary_key=True, nullable=False)
    
    user_id = Column(UUID, nullable=False)
    
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    
    password = Column(String, nullable=False)
    
    role = Column(Integer, nullable=False)
    
    working_status = Column(Boolean, nullable=False)
    
    created_at = Column(TIMESTAMP, nullable=False)
    

    
    
    