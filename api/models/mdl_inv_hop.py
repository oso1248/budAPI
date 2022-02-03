from sqlalchemy import Column, ForeignKey, Integer, TIMESTAMP, String, text, Numeric
from sqlalchemy.dialects.postgresql import UUID
from .. database.database import Base
from sqlalchemy.orm import relationship


class InvLastBrews(Base):
    __tablename__ = 'inv_last_brews'
    inv_uuid = Column(UUID(as_uuid=True), primary_key=True,
                      server_default=text('gen_random_uuid()'))
    bh_1 = Column(String, nullable=False)
    bh_2 = Column(String, nullable=False)
    created_by = Column(Integer, ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))

    creator = relationship('Users', foreign_keys=[created_by])


class InvHop(Base):
    __tablename__ = 'inv_hop'

    id = Column(Integer, primary_key=True, nullable=False)
    total_pallets = Column(Integer, nullable=False)
    total_units = Column(Numeric(scale=2, precision=9), nullable=False)
    total_per_unit = Column(Numeric(scale=2, precision=9), nullable=False)
    total_end = Column(Numeric(scale=2, precision=9), nullable=False)
    lot_number = Column(String, nullable=False)
    note = Column(String, nullable=True)
    inv_uuid = Column(UUID(as_uuid=True), ForeignKey(
        'inv_last_brews.inv_uuid', ondelete='CASCADE'), nullable=False)
    id_commodity = Column(Integer, ForeignKey(
        'commodities.id', ondelete='CASCADE'), nullable=False)
    created_by = Column(Integer, ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))

    creator = relationship('Users', foreign_keys=[created_by])
    parent = relationship('Commodities', foreign_keys=[id_commodity])
    lastbrews = relationship('InvLastBrews', foreign_keys=[inv_uuid])
