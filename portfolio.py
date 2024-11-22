from sqlalchemy import Boolean
from flask_login import current_user

import price_checker
from data import data_manager
from entities import AssetPurchase


def get_render_color(cost, value):
    color = "black"
    if cost > value:
        color = "red"
    elif cost < value:
        color = "green"
    return color

def add_test_data(portfolio, asset, gbp, price):
    purchase = AssetPurchase.create_test_data(price=price, gbp=gbp, asset=asset)
    portfolio.add_purchase(purchase)

def get_current_user_portfolio():
    current_user_portfolio = UserPortfolio()
    print(len(current_user_portfolio.portfolio_assets))
    if current_user.is_authenticated:
        print(f"current user is {current_user.username}")
        purchases = data_manager.get_purchases_for_user(current_user.id)
        for purchase in purchases:
            current_user_portfolio.add_purchase(purchase)
    else:
        print("generating test data - no user logged in")
        # initialise with test data
        add_test_data(current_user_portfolio, "BTC", 100, 45000)
        add_test_data(current_user_portfolio, "ETH", 80, 2000)
    print(len(current_user_portfolio.portfolio_assets))
    return current_user_portfolio

class UserPortfolio:
    """A class to represent the crypto assets a user has purchased.
    Simply contains a dict portfolio_assets which maps from the asset (e.g. BTC) to a list of AssetPurchases"""

    def __init__(self):
        self.portfolio_assets = {} #asset: list[AssetPurchases]

    def write_asset_html(self, asset):
        cost = self.total_cost_of_asset(asset)
        value = self.current_value_of_asset(asset)
        color = get_render_color(cost, value)

        html = (f"<tr><td>{asset}</td>"
                f"<td>£{'{:.2f}'.format(cost)}</td>"
                f"<td>£{'{:.2f}'.format(value)}</td>"
                f"<td style='color:{color}; font-weight: bold'>£{'{:.2f}'.format(value - cost)}</td>"
                )
        return html

    def to_html(self):
        html = ("<table><tr>"
                "<th>Asset</th>"
                "<th>Total Cost</th>"
                "<th>Current Value</th>"
                "<th>Profit/Loss</th></tr>"
                )
        for asset, asset_purchases in self.portfolio_assets.items():
            html += self.write_asset_html(asset)
        html += "</table>"
        return html

    def add_purchase(self, purchase: data_manager.AssetPurchase):
        asset = purchase.asset
        #if we don't already own some of this asset then create an empty list in the dictionary
        if asset not in self.portfolio_assets:
            self.portfolio_assets[asset] = []
        self.portfolio_assets[asset].append(purchase)

    def current_value_of_asset(self, asset, as_string: Boolean = False):
        """What is the value of the given asset in this portfolio?
        Looks up the current price and calculates the total value of the held assets
        Can return a formatted string or a float depending on the as_string variable"""
        current_price = price_checker.get_asset_price(asset)
        current_value = current_price * self.total_held_of_asset(asset)
        if as_string:
            return self.format_currency(current_value())
        else:
            return current_value

    def total_held_of_asset(self, asset):
        """
        How many of the given asset are in the portfolio
        :param asset: The asset to check (e.g. BTC)
        :return: the total number held.
        """
        total = 0
        if asset in self.portfolio_assets:
            for purchase in self.portfolio_assets[asset]:
                total += purchase.amount
        return total

    def total_cost_of_asset(self, asset):
        """
        How much fiat has the user spent on the given asset?
        :param asset: the asset to check
        :return: the total cost in gbp, including any purchase fees
        """
        total = 0
        if asset in self.portfolio_assets:
            purchases: list[AssetPurchase] = self.portfolio_assets[asset]
            for purchase in purchases:
                total += purchase.gbp_total
        return total

    def total_cost(self):
        """What is the total cost of the portfolio as a float"""
        total = 0
        for asset in self.portfolio_assets:
            total += self.total_cost_of_asset(asset)
        return total

    def total_value(self):
        """What is the total current value of all the assets in the portfolio as a float"""
        total = 0
        for asset in self.portfolio_assets:
            total += self.current_value_of_asset(asset)
        return total

    def total_profit(self):
        """How much is the portfolio up (or down)"""
        return self.total_value() - self.total_cost()

    def format_currency(self, currency: float) -> str:
        return '£{:.2f}'.format(currency)

    def profit_color(self):
        return get_render_color(self.total_cost(), self.total_value())