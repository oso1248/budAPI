from sqlalchemy import Column, ForeignKey, Integer, TIMESTAMP, String, text
from .. database.database import Base
from sqlalchemy.orm import relationship


class ManpowerIndividual(Base):
    __tablename__ = 'manpower_individual'

    id = Column(Integer, primary_key=True, nullable=False)
    shift = Column(Integer, nullable=False)
    id_users = Column(Integer, ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False)
    id_jobs = Column(Integer, ForeignKey(
        'jobs.id', ondelete='CASCADE'), nullable=False)
    note = Column(String, nullable=True)
    created_by = Column(Integer, ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))

    brewer = relationship('Users', foreign_keys=[id_users])
    job = relationship('Jobs', foreign_keys=[id_jobs])
    creator = relationship('Users', foreign_keys=[created_by])


class ManpowerGroup(Base):
    __tablename__ = 'manpower_group'

    id = Column(Integer, primary_key=True, nullable=False)
    shift = Column(Integer, nullable=False)
    note = Column(String, nullable=True)
    created_by = Column(Integer, ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))

    creator = relationship('Users', foreign_keys=[created_by])
