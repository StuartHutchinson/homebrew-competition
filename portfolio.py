import price_checker

CRYPTO_LIST = [
	("BTC", "Bitcoin"),
	("ETH", "Ethereum"),
	("SOL", "Solana"),
]

class UserPortfolio():
    assets = {}

    def get_asset(self, asset):
        if asset in self.assets:
            return self.assets[asset]
        return None

    def add_asset(self, portfolio_item):
        asset = portfolio_item.asset
        self.assets[asset] = portfolio_item

    def to_html(self):
        html = ("<table><tr>"
                "<th>Asset</th>"
                "<th>Total Cost</th>"
                "<th>Current Value</th>"
                "<th>Profit/Loss</th></tr>"
                )
        for asset, portfolio_asset in self.assets.items():
            html += portfolio_asset.to_html()
        html += "</table>"
        return html

portfolio = UserPortfolio()

def add_asset(form):
    asset = form.asset.data
    item = portfolio.get_asset(asset)
    if not item:
        item = PortfolioAsset(asset)
        portfolio.add_asset(item)
    item.add_purchase(form)

class PortfolioAsset():
    def __init__(self, asset):
        self.asset = asset
        self.purchases = []

    def add_purchase(self, form):
        asset = form.asset.data
        purchase_price = form.purchase_price.data
        gbp = form.gbp.data
        crypto_amount = gbp / purchase_price

        purchase = AssetPurchase(asset, crypto_amount, gbp, purchase_price)
        self.purchases.append(purchase)

    def current_value_str(self) ->str:
        return '£{:.2f}'.format(self.current_value())

    def current_value(self):
        current_price = price_checker.get_asset_price(self.asset)
        return current_price * self.total_held()

    def total_held(self):
        total = 0
        for purchase in self.purchases:
            total += purchase.amount
        return total

    def total_cost(self):
        total = 0
        for purchase in self.purchases:
            total += purchase.gbp
        return total

    def get_render_color(self):
        color = "black"
        cost = self.total_cost()
        value = self.current_value()
        if cost > value:
            color = "red"
        elif cost < value:
            color = "green"
        return color

    def to_html(self):
        cost = self.total_cost()
        value = self.current_value()
        color = self.get_render_color()

        html = (f"<tr><td>{self.asset}</td>"
                f"<td>£{'{:.2f}'.format(cost)}</td>"
                f"<td>£{'{:.2f}'.format(value)}</td>"
                f"<td style='color:{color}; font-weight: bold'>£{'{:.2f}'.format(value-cost)}</td>"
                )
        return html


class AssetPurchase():
    def __init__(self, asset, amount, gbp, purchase_price):
        self.asset = asset
        self.amount = amount
        self.gbp = gbp
        self.purchase_price = purchase_price