from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from flask_login import UserMixin, current_user

from data.data_manager import db

class User(db.Model, UserMixin):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)

    purchases: Mapped[list["AssetPurchase"]] = relationship(back_populates="owner")

    def __init__(self, username, password):
        self.username = username
        self.password = password

class AssetPurchase(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    date: Mapped[datetime] = mapped_column(nullable=False)
    asset: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)
    gbp_total: Mapped[float] = mapped_column(nullable=False)
    fees: Mapped[float] = mapped_column(nullable=False)
    amount: Mapped[float] = mapped_column(nullable=False)

    owner: Mapped["User"] = relationship(back_populates="purchases")

    def __init__(self, owner_id, date, asset, price, gbp_total, fees, owner):
        self.owner_id = owner_id
        self.date = date
        self.asset = asset
        self.price = price
        self.gbp_total = gbp_total
        self.fees = fees
        self.amount = (self.gbp_total - self.fees) / self.price
        self.owner = owner

    @classmethod
    def create_from_form(cls, form):
        return cls(
            owner_id = -1 if not current_user.is_authenticated else current_user.id,
            date = form.date.data,
            asset = form.asset.data,
            price = form.price.data,
            gbp_total = form.gbp.data,
            fees = form.fees.data,
            owner = current_user)

    @classmethod
    def create_test_data(cls, price, asset, gbp):
        return cls(
            owner_id = -1,
            date = datetime.now(),
            asset = asset,
            price = price,
            gbp_total = gbp,
            fees = 0,
            owner = None)