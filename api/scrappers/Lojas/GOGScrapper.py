import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
from lxml import etree

class GOGScrapper():
    def __init__(self, driverName, data):
        self.driverName = driverName
        self.plataforma = data["P"]
        self.loja = data["L"]
        self.page = 1
        self.game_items_gog = {}
        self.game_items_list_gog = []
        self.options = Options()
        self.options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)
        self.driver.set_page_load_timeout(8)
        self.driver.get('https://www.gog.com/en/games?discounted=true&page=2')
        self.driver.maximize_window()

    def ReabrirDriver(self, offset):
        try:
            self.driver.set_page_load_timeout(15)
            self.driver.get('https://www.gog.com/en/games?discounted=true&page=' + str(offset))
            self.driver.maximize_window()
            time.sleep(0.5)
            self.driver.execute_script('window.scrollBy(0, document.body.scrollHeight)')
            time.sleep(0.5)
            self.driver.execute_script('window.scrollBy(0, document.body.scrollHeight)')
            time.sleep(0.5)
            html = self.driver.page_source
            web = BeautifulSoup(html, 'html.parser')
            return web
        except TimeoutException:
            self.driver.quit()
            return None
        except:
            pass

    def converter_preco_para_float(self, preco):
        try:
            preco = preco.replace('R$', '')
            return float(preco)
        except:
            return None

    def manager(self):
        try:
            while True:
                try:
                    site = self.ReabrirDriver(self.page)
                    dom = etree.HTML(str(site))
                except:
                    self.page += 1
                    continue
                games = dom.xpath("//a[contains(@class, 'product-tile--grid')]")

                for game in games:
                    try:
                        if len(game.xpath(".//span[contains(@class, 'final-value')]")) < 1:
                            continue
                        self.game_items_gog.update({'nome': game.xpath(".//div[contains(@class, 'product-tile__title')]")[0].get('title')})
                        self.game_items_gog.update({'precoDesconto': self.converter_preco_para_float(
                            game.xpath(".//span[contains(@class, 'final-value')]")[0].text)})
                        if len(game.xpath(".//span[contains(@class, 'base-value')]")) >= 1:
                            self.game_items_gog.update({'precoTotal': self.converter_preco_para_float(
                                game.xpath(".//span[contains(@class, 'base-value')]")[0].text)})
                        else:
                            self.game_items_gog.update({'precoTotal': self.converter_preco_para_float(
                                game.xpath(".//span[contains(@class, 'final-value')]")[0].text)})
                        self.game_items_gog.update({'plataforma': next(p["id"] for p in self.plataforma if p["nome"] == 'Computador')})
                        self.game_items_gog.update({'midia': 0})
                        self.game_items_gog.update({'link': game.get('href')})
                        self.game_items_gog.update({'loja': self.loja})
                        self.game_items_gog.update({'linkImagem': game.xpath(".//source")[0].get('srcset')[:game.xpath(".//source")[0].get('srcset').find(',')]})
                        self.game_items_list_gog.append(self.game_items_gog.copy())
                    except:
                        pass

                self.page += 1
                if (len(games) < 40 and site != None) or self.page >= 50:
                    self.driver.close()
                    break
        except:
            pass
        finally:
            return self.game_items_list_gog
