import price_checker

CRYPTO_LIST = [
	("BTC", "Bitcoin"),
	("ETH", "Ethereum"),
	("SOL", "Solana"),
]

class AssetPurchase:
    """Represents the purchase of an asset
    asset - what asset was purchased eg BTC
    amount - how many of the asset were purchased
    gbp - how much the purchase cost
    purchase_price - the current price of one the assets at the time of purchase.
    gbp = amount * purchase_price"""
    def __init__(self, asset, amount, gbp, purchase_price):
        self.asset = asset
        self.amount = amount
        self.gbp = gbp
        self.purchase_price = purchase_price

class PortfolioAsset:
    """The amount of a given asset that is in the portfolio. Simply an asset (eg BTC) along with a list of AssetPurchases"""
    def __init__(self, asset):
        self.asset = asset
        self.purchases = []

    def add_purchase(self, asset, gbp, purchase_price):
        """
        :param asset: what asset was purchased
        :param gbp: cost of the purchase in GBP
        :param purchase_price: the market rate at the time of the purchase
        """
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

class UserPortfolio:
    """A class to represent the crypto assets a user has purchased.
    Simply contains a dict portfolio_assets which maps from the asset (eg BTC) to the PortfolioAsset"""
    portfolio_assets = {}

    def get_asset(self, asset) -> PortfolioAsset:
        if asset in self.portfolio_assets:
            return self.portfolio_assets[asset]
        return None

    def add_asset(self, portfolio_asset):
        asset = portfolio_asset.asset
        self.portfolio_assets[asset] = portfolio_asset

    def to_html(self):
        html = ("<table><tr>"
                "<th>Asset</th>"
                "<th>Total Cost</th>"
                "<th>Current Value</th>"
                "<th>Profit/Loss</th></tr>"
                )
        for asset, portfolio_asset in self.portfolio_assets.items():
            html += portfolio_asset.to_html()
        html += "</table>"
        return html

def add_asset(form):
    asset = form.asset.data
    portfolio_item = portfolio.get_asset(asset)
    if not portfolio_item:
        portfolio_item = PortfolioAsset(asset)
        portfolio.add_asset(portfolio_item)

    asset = form.asset.data
    purchase_price = form.purchase_price.data
    gbp = form.gbp.data
    portfolio_item.add_purchase(asset, gbp, purchase_price)

def add_test_data(portfolio, asset, gbp, price):
    portfolio_asset = PortfolioAsset(asset)
    portfolio.add_asset(portfolio_asset)
    portfolio_asset.add_purchase(purchase_price=price, gbp=gbp, asset=asset)

portfolio = UserPortfolio()
#initialise with test data
add_test_data(portfolio, "BTC", 100, 45000)
add_test_data(portfolio, "ETH", 80, 2000)