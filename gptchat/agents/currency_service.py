import os
import requests

from core.base_agent import BaseToolAgent
from core.tool_function import tool_function


class CurrencyService(BaseToolAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("CURRENCY_API_KEY")

    @tool_function(
        name="get_exchange_rate",
        description="Get the exchange rate from USD to a target currency",
        parameters={
            "target_currency": {
                "type": "string",
                "description": "Target currency code (e.g., EUR, PLN, BYN). USD is always the base currency.",
            },
        },
    )
    def get_exchange_rate(self, target_currency: str):
        url = "https://api.exchangerate.host/live"
        params = {"currencies": target_currency.upper()}
        if self.api_key:
            params["access_key"] = self.api_key
        response = requests.get(url, params=params)
        data = response.json()
        rate = data.get("quotes", {}).get(f"USD{target_currency.upper()}")
        return {"rate": rate} if rate else {"error": "Rate not found"}


jopa = CurrencyService()
print(jopa.get_exchange_rate("BYN"))
