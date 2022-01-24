from .. database.database import Base
from sqlalchemy import Column, ForeignKey, Integer, TIMESTAMP, Boolean, String, text
from sqlalchemy.orm import relationship


class BrandBrw(Base):
    __tablename__ = 'brand_brewing'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, unique=True, nullable=False)
    is_organic = Column(Boolean, nullable=False)
    is_hop_kettle = Column(Boolean, nullable=False)
    is_hop_dry = Column(Boolean, nullable=False)
    is_addition = Column(Boolean, nullable=False)
    note = Column(String, nullable=True)
    methods_acx = Column(String, nullable=True)
    methods_csx = Column(String, nullable=True)
    is_active = Column(Boolean, nullable=False)
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
    children = relationship('BrandFin', backref='brand_brewing',
                            primaryjoin='BrandBrw.id == BrandFin.id_brewing', viewonly=True)


class BrandFin(Base):
    __tablename__ = 'brand_finishing'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, unique=True, nullable=False)
    is_pre_injection = Column(Boolean, nullable=False)
    is_post_injection = Column(Boolean, nullable=False)
    is_bypass = Column(Boolean, nullable=False)
    is_organic = Column(Boolean, nullable=False)
    note = Column(String, nullable=True)
    methods_filters = Column(String, nullable=True)
    methods_releasing = Column(String, nullable=True)
    is_active = Column(Boolean, nullable=False)
    id_brewing = Column(Integer, ForeignKey(
        'brand_brewing.id', ondelete='CASCADE'), nullable=False)
    created_by = Column(Integer, ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False)
    updated_by = Column(Integer, ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))

    parent = relationship('BrandBrw', foreign_keys=[id_brewing])
    creator = relationship('Users', foreign_keys=[created_by])
    updater = relationship('Users', foreign_keys=[updated_by])
    children = relationship('BrandPck', backref='brand_finishing',
                            primaryjoin='BrandFin.id == BrandPck.id_finishing', viewonly=True)


class BrandPck(Base):
    __tablename__ = 'brand_packaging'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, unique=True, nullable=False)
    is_organic = Column(Boolean, nullable=False)
    note = Column(String, nullable=True)
    is_active = Column(Boolean, nullable=False)
    id_finishing = Column(Integer, ForeignKey(
        'brand_finishing.id', ondelete='CASCADE'), nullable=False)
    created_by = Column(Integer, ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False)
    updated_by = Column(Integer, ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))

    parent = relationship('BrandFin', foreign_keys=[id_finishing])
    creator = relationship('Users', foreign_keys=[created_by])
    updater = relationship('Users', foreign_keys=[updated_by])


class BrandBrwMeth(Base):
    __tablename__ = 'methods_brewing'

    id = Column(Integer, primary_key=True, nullable=False)
    method = Column(String, unique=True, nullable=False)
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


class BrandFinMeth(Base):
    __tablename__ = 'methods_finishing'

    id = Column(Integer, primary_key=True, nullable=False)
    method = Column(String, unique=True, nullable=False)
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
