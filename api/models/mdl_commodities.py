from .. database.database import Base
from sqlalchemy import Column, ForeignKey, Integer, TIMESTAMP, Boolean, String, text, Float, Numeric
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
    type = Column(String, nullable=False)
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


class CommoditiesBridge(Base):
    __tablename__ = 'bridge_commodities'

    id_commodity = Column(Integer, ForeignKey(
        'commodities.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    id_brand_brewing = Column(Integer, ForeignKey(
        'brand_brewing.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    id_brewhouse = Column(Integer, primary_key=True, nullable=False)
    amount_per_brew = Column(Numeric(scale=2, precision=9), nullable=False)

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
    commodity = relationship('Commodities', foreign_keys=[id_commodity])
    brand = relationship('BrandBrw', foreign_keys=[id_brand_brewing])
