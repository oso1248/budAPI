from sqlalchemy import Column, ForeignKey, Integer, TIMESTAMP, String, text, Numeric
from sqlalchemy.dialects.postgresql import UUID
from .. database.database import Base
from sqlalchemy.orm import relationship


class InvMaterial(Base):
    __tablename__ = 'inv_material'

    id = Column(Integer, primary_key=True, nullable=False)
    total_pallets = Column(Integer, nullable=False)
    total_units = Column(Numeric(scale=2, precision=9), nullable=False)
    total_per_unit = Column(Numeric(scale=2, precision=9), nullable=False)
    total_end = Column(Numeric(scale=2, precision=9), nullable=False)
    note = Column(String, nullable=True)
    # inv_uuid = Column(String, nullable=False)
    inv_uuid = Column(UUID(as_uuid=True), nullable=False)
    id_commodity = Column(Integer, ForeignKey(
        'commodities.id', ondelete='CASCADE'), nullable=False)
    created_by = Column(Integer, ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))

    creator = relationship('Users', foreign_keys=[created_by])
    parent = relationship('Commodities', foreign_keys=[id_commodity])
