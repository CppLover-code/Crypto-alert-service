from datetime import datetime

from sqlalchemy import Boolean, DateTime ,ForeignKey, Numeric, String, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class Coin(Base):
    __tablename__ = "coins"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    coingecko_id: Mapped[str] = mapped_column(String(64), unique=True)
    symbol: Mapped[str] = mapped_column(String(16))
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    
    price: Mapped["Price | None"] = relationship(back_populates="coin")
    
class Price(Base):
    __tablename__ = "prices"
    __table_args__ = (UniqueConstraint("coin_id"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    coin_id: Mapped[int] = mapped_column(ForeignKey("coins.id"))
    value: Mapped[float] = mapped_column(Numeric(20, 8))
    updated_at: Mapped[datetime] = mapped_column(DateTime)
    coin: Mapped["Coin"] = relationship(back_populates="price")
    
class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    telegram_chat_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    notify_email: Mapped[bool] = mapped_column(Boolean, default=False)
    notify_telegram: Mapped[bool] = mapped_column(Boolean, default=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    