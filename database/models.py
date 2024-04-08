from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    ...


class UnitLevel(Base):
    __tablename__ = 'level_unit'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    level: Mapped[str] = mapped_column(String(10), nullable=False)


class Banner(Base):
    __tablename__ = 'banner'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(15), unique=True)
    image: Mapped[str] = mapped_column(String(150), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)


class Units(Base):
    __tablename__ = 'units'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)
    level: Mapped[int] = mapped_column(Integer)
    size: Mapped[str] = mapped_column(String)
    price: Mapped[int] = mapped_column(Integer)
    exp: Mapped[int] = mapped_column(Integer)
    curr_exp: Mapped[int] = mapped_column(Integer)
    exp_per_kill: Mapped[int] = mapped_column(Integer)
    health: Mapped[int] = mapped_column(Integer)
    curr_health: Mapped[int] = mapped_column(Integer)
    armor: Mapped[int] = mapped_column(Integer)
    immune: Mapped[str] = mapped_column(String)
    ward: Mapped[str] = mapped_column(String)
    attack_type: Mapped[str] = mapped_column(String)
    attack_chance: Mapped[str] = mapped_column(String)
    attack_dmg: Mapped[int] = mapped_column(Integer)
    dot_dmg: Mapped[int] = mapped_column(Integer)
    attack_source: Mapped[str] = mapped_column(String)
    attack_ini: Mapped[int] = mapped_column(Integer)
    attack_radius: Mapped[str] = mapped_column(String)
    attack_purpose: Mapped[int] = mapped_column(Integer)
    prev_level: Mapped[str] = mapped_column(String)
    desc: Mapped[str] = mapped_column(String)
    photo: Mapped[str] = mapped_column(String)
    gif: Mapped[str] = mapped_column(String)
    slot: Mapped[int] = mapped_column(Integer)
    subrace: Mapped[str] = mapped_column(String)
    branch: Mapped[str] = mapped_column(String)
    attack_twice: Mapped[int] = mapped_column(Integer)
    regen: Mapped[int] = mapped_column(Integer)
    dyn_upd_level: Mapped[int] = mapped_column(Integer)
    upgrade_b: Mapped[str] = mapped_column(String)
    leadership: Mapped[int] = mapped_column(Integer)
    leader_cat: Mapped[str] = mapped_column(String)
    nat_armor: Mapped[int] = mapped_column(Integer)
    might: Mapped[int] = mapped_column(Integer)
    weapon_master: Mapped[int] = mapped_column(Integer)
    endurance: Mapped[int] = mapped_column(Integer)
    first_strike: Mapped[int] = mapped_column(Integer)
    accuracy: Mapped[int] = mapped_column(Integer)
    water_resist: Mapped[int] = mapped_column(Integer)
    air_resist: Mapped[int] = mapped_column(Integer)
    fire_resist: Mapped[int] = mapped_column(Integer)
    earth_resist: Mapped[int] = mapped_column(Integer)
    dotted: Mapped[int] = mapped_column(Integer)
