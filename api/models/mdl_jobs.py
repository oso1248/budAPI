from .. database.database import Base
from sqlalchemy import Column, ForeignKey, Integer, TIMESTAMP, Boolean, String, text
from sqlalchemy.orm import relationship


class Jobs(Base):
    __tablename__ = 'jobs'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, unique=True, nullable=False)
    area = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False)
    is_work_restriction = Column(Boolean, nullable=False)
    created_by = Column(Integer, ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False)
    updated_by = Column(Integer, ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))

    creator = relationship('Users', foreign_keys=[created_by])
    updater = relationship('Users', foreign_keys=[updated_by])


class BridgeUsersJobs(Base):
    __tablename__ = 'bridge_users_jobs'
    id_users = Column(Integer, ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False, primary_key=True)
    id_jobs = Column(Integer, ForeignKey(
        'jobs.id', ondelete='CASCADE'), nullable=False, primary_key=True)
    skap = Column(Integer, nullable=False)
    created_by = Column(Integer, ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False)
    updated_by = Column(Integer, ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))

    creator = relationship('Users', foreign_keys=[created_by])
    updater = relationship('Users', foreign_keys=[updated_by])
