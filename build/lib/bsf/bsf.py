from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pickle, os

class BSF:
    ORDER_FORM = "/html/body/div[1]/div/div[2]/div/div[1]/div[4]/div/"

    def __init__(self, executable_path="chromedriver91") -> None:
        self.driver = webdriver.Chrome(executable_path=executable_path)
        self.driver.get("https://accounts.binance.com/en/login")
        if not os.path.isdir("cookies"):
            os.mkdir("cookies")

    def connect(self, email, password):
        filename = f"cookies/{email}.pkl"
        cookies_saved = False
        if os.path.isdir(filename):
            cookies_saved = True
            cookies = pickle.load(open(filename, "rb"))
            for cookie in cookies: 
                try:
                    self.driver.add_cookie(cookie)
                except:
                    pass
        self.driver.find_element_by_name("email").send_keys(email)
        self.driver.find_element_by_name("password").send_keys(password)
        self.driver.find_element_by_id("click_login_submit").click()
        input("Click 'ENTER' when connected !")
        if not cookies_saved:
            pickle.dump( 
                self.driver.get_cookies(), 
                open(filename,"wb")
            )

    
    def get_avbl(self):
        return int(self.driver.find_element_by_xpath(
                f"""{self.ORDER_FORM}div[4]/div/div[1]/div/span"""
            ).text)

    def get_futures(self):
        self.driver.get("https://www.binance.com/en/futures/BTCUSDT")
        self.driver.find_element_by_id("tab-LIMIT").click()
    
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
                for i in range(pas): # Plus
                    self.driver.find_element_by_xpath(
                        """/html/body/div[16]/div/div[2]/div[2]/button[2]"""
                    ).click()
            else:
                for i in range(-pas): # Moins
                    self.driver.find_element_by_xpath(
                        """/html/body/div[16]/div/div[2]/div[2]/button[1]"""
                    ).click()
            self.driver.find_element_by_xpath(
                """/html/body/div[16]/div/div[2]/div[6]/button[2]"""
            ).click()

    def set_price(self, price):
        id_Price = self.driver.find_element_by_xpath(
                f"""{self.ORDER_FORM}div[4]/form/div[1]/div/input"""
            ).get_attribute("id")
        self.driver.execute_script(
            f"document.getElementById('{id_Price}').value={price};"
            )
        
        self.driver.find_element_by_xpath(
            f"""{self.ORDER_FORM}div[4]/form/div[3]/div[1]/div/div[9]"""
        ).click()

    def set_TPSL(self, TP, SL):
        # Make TP SL available
        self.driver.find_element_by_xpath(
            f"""{self.ORDER_FORM}div[4]/form/div[4]/div/label/div[1]"""
        ).click()
        # set TP
        id_TP = self.driver.find_element_by_xpath(
                f"""{self.ORDER_FORM}div[4]/form/div[4]/div[2]/div/input"""
            ).get_attribute("id")
        self.driver.execute_script(
            f"document.getElementById('{id_TP}').value={TP};"
        )
        # set SL
        id_SL = self.driver.find_element_by_xpath(
                f"""{self.ORDER_FORM}div[4]/form/div[4]/div[3]/div/input"""
            ).get_attribute("id")
        self.driver.execute_script(
            f"document.getElementById('{id_TP}').value={SL};"
        )

    def buy(self):
        self.driver.find_element_by_xpath(
            f"""{self.ORDER_FORM}div[4]/form/div[6]/button[1]"""
        ).click()

    def sell(self):
        self.driver.find_element_by_xpath(
            f"""{self.ORDER_FORM}div[4]/form/div[6]/button[2]"""
        ).click()
            

    