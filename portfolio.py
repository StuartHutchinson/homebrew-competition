import price_checker

CRYPTO_LIST = [
	("BTC", "Bitcoin"),
	("ETH", "Ethereum"),
	("SOL", "Solana"),
]

user_portfolio = {}

def add_asset(asset, amount):
    if asset in user_portfolio:
        item = user_portfolio[asset]
        item.add_amount(amount)
    else:
        item = PortfolioItem(asset, amount)
        user_portfolio[asset] = item

class PortfolioItem():
    def __init__(self, asset, amount):
        self.asset = asset
        self.amount = amount

    def add_amount(self, amount):
        self.amount += amount

    def current_value(self) ->str:
        current_price = price_checker.get_asset_price(self.asset)
        return '£{:.2f}'.format(current_price * self.amount)