from .. database.database import Base
from sqlalchemy import Column, ForeignKey, Integer, TIMESTAMP, Boolean, String, text, Float
from sqlalchemy.orm import relationship


class Commodities(Base):
    __tablename__ = 'commodities'

    id = Column(Integer, primary_key=True, nullable=False)
    name_bit = Column(String, unique=True, nullable=False)
    name_local = Column(String, unique=True, nullable=False)
    location = Column(String, nullable=False)
    sap = Column(String, nullable=False)
    inventory = Column(String, nullable=False)
    threshold = Column(Integer, nullable=False)
    per_pallet = Column(Integer, nullable=False)
    per_unit = Column(Float, nullable=False)
    unit_of_measurement = Column(String, nullable=False)
    type = Column(String, nullable=True)
    note = Column(String, nullable=True)
    balance_inactive = Column(Float, nullable=True)
    is_active = Column(Boolean, nullable=False)
    id_supplier = Column(Integer, ForeignKey(
        'suppliers.id', ondelete='CASCADE'), nullable=False)
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
    supplier = relationship('Suppliers', foreign_keys=[id_supplier])
