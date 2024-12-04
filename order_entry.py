import requests
import logging
from trading_app.constants import API_URL, ACCOUNT_ID
from trading_app.auth import Authenticator


class OrderEntry:
    def __init__(self):
        """
        Initializes the OrderEntry class with authentication and order endpoint details.
        """
        self.authenticator = Authenticator()
        self.token = self.authenticator.get_token()
        self.headers = {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}
        self.base_url = f"{API_URL}/orders"

    def place_market_order(self, symbol, quantity, side):
        """
        Place a market order.

        :param symbol: The symbol to trade.
        :param quantity: Quantity of the trade.
        :param side: "BUY" or "SELL".
        """
        try:
            payload = {
                "accountId": ACCOUNT_ID,
                "symbol": symbol,
                "quantity": quantity,
                "side": side,
                "orderType": "MARKET",
                "timeInForce": "GTC"
            }

            response = requests.post(self.base_url, json=payload, headers=self.headers)
            response.raise_for_status()

            order_data = response.json()
            logging.info(f"Market order placed: {order_data}")
            return order_data

        except requests.exceptions.RequestException as e:
            logging.error(f"Error placing market order: {e}")
            raise

    def place_limit_order(self, symbol, quantity, price, side):
        """
        Place a limit order.

        :param symbol: The symbol to trade.
        :param quantity: Quantity of the trade.
        :param price: Limit price.
        :param side: "BUY" or "SELL".
        """
        try:
            payload = {
                "accountId": ACCOUNT_ID,
                "symbol": symbol,
                "quantity": quantity,
                "side": side,
                "orderType": "LIMIT",
                "price": price,
                "timeInForce": "GTC"
            }

            response = requests.post(self.base_url, json=payload, headers=self.headers)
            response.raise_for_status()

            order_data = response.json()
            logging.info(f"Limit order placed: {order_data}")
            return order_data

        except requests.exceptions.RequestException as e:
            logging.error(f"Error placing limit order: {e}")
            raise

    def place_stop_order(self, symbol, quantity, stop_price, side):
        """
        Place a stop order.

        :param symbol: The symbol to trade.
        :param quantity: Quantity of the trade.
        :param stop_price: Stop price.
        :param side: "BUY" or "SELL".
        """
        try:
            payload = {
                "accountId": ACCOUNT_ID,
                "symbol": symbol,
                "quantity": quantity,
                "side": side,
                "orderType": "STOP",
                "stopPrice": stop_price,
                "timeInForce": "GTC"
            }

            response = requests.post(self.base_url, json=payload, headers=self.headers)
            response.raise_for_status()

            order_data = response.json()
            logging.info(f"Stop order placed: {order_data}")
            return order_data

        except requests.exceptions.RequestException as e:
            logging.error(f"Error placing stop order: {e}")
            raise

    def place_bracket_order(self, symbol, quantity, entry_price, stop_loss, take_profit, side, order_type="LIMIT"):
        """
        Place a bracket order.

        :param symbol: The symbol to trade.
        :param quantity: Quantity of the trade.
        :param entry_price: Entry price for the order.
        :param stop_loss: Stop-loss price.
        :param take_profit: Take-profit price.
        :param side: "BUY" or "SELL".
        :param order_type: Type of order (e.g., LIMIT or MARKET).
        """
        try:
            payload = {
                "accountId": ACCOUNT_ID,
                "symbol": symbol,
                "quantity": quantity,
                "side": side,
                "orderType": order_type,
                "price": entry_price,
                "timeInForce": "GTC",
                "bracket": {
                    "stopLoss": {
                        "price": stop_loss,
                        "orderType": "STOP"
                    },
                    "takeProfit": {
                        "price": take_profit,
                        "orderType": "LIMIT"
                    }
                }
            }

            response = requests.post(self.base_url, json=payload, headers=self.headers)
            response.raise_for_status()

            order_data = response.json()
            logging.info(f"Bracket order placed: {order_data}")
            return order_data

        except requests.exceptions.RequestException as e:
            logging.error(f"Error placing bracket order: {e}")
            raise

    def cancel_order(self, order_id):
        """
        Cancel an existing order.

        :param order_id: The ID of the order to cancel.
        """
        try:
            cancel_url = f"{self.base_url}/{order_id}/cancel"
            response = requests.post(cancel_url, headers=self.headers)
            response.raise_for_status()

            cancel_data = response.json()
            logging.info(f"Order canceled: {cancel_data}")
            return cancel_data

        except requests.exceptions.RequestException as e:
            logging.error(f"Error canceling order: {e}")
            raise

    def modify_order(self, order_id, new_price=None, new_quantity=None):
        """
        Modify an existing order.

        :param order_id: The ID of the order to modify.
        :param new_price: New price for the order.
        :param new_quantity: New quantity for the order.
        """
        try:
            payload = {
                "newPrice": new_price,
                "newQuantity": new_quantity
            }
            modify_url = f"{self.base_url}/{order_id}/modify"
            response = requests.put(modify_url, json=payload, headers=self.headers)
            response.raise_for_status()

            modify_data = response.json()
            logging.info(f"Order modified: {modify_data}")
            return modify_data

        except requests.exceptions.RequestException as e:
            logging.error(f"Error modifying order: {e}")
            raise

    def get_order_status(self, order_id):
        """
        Get the status of an existing order.

        :param order_id: The ID of the order to query.
        """
        try:
            status_url = f"{self.base_url}/{order_id}"
            response = requests.get(status_url, headers=self.headers)
            response.raise_for_status()

            status_data = response.json()
            logging.info(f"Order status retrieved: {status_data}")
            return status_data

        except requests.exceptions.RequestException as e:
            logging.error(f"Error retrieving order status: {e}")
            raise
