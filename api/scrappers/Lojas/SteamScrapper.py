import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from lxml import etree

class SteamScrapper():
    def __init__(self, driverName, data):
        self.driverName = driverName
        self.plataforma = data["P"]
        self.loja = data["L"]
        self.game_items_steam = {}
        self.game_items_list_steam = []
        self.games_to_analyze = 1000
        self.tries = 0
        self.total_tries = 0

    def ReabrirDriver(self):
        try:
            options = Options()
            options.add_experimental_option("detach", True)
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            driver.set_page_load_timeout(15)
            driver.get('https://store.steampowered.com/search/?specials=1&ndl=1')
            driver.maximize_window()

            while len(driver.find_elements(By.XPATH,'//a[contains(@class, "search_result_row ds_collapse_flag")]')) < self.games_to_analyze:
                try:
                    time.sleep(3)
                    driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
                except:
                    pass

            html = driver.page_source
            web = BeautifulSoup(html, 'html.parser')
            driver.quit()
            return web
        except TimeoutException:
            driver.quit()
            return None
        except:
            pass

    def converter_preco_para_float(self, preco):
        try:
            preco = preco.replace('R$', '')
            preco = preco.replace(',', '.')
            return float(preco)
        except:
            return None

    def manager(self):
        try:
            site = self.ReabrirDriver()
            dom = etree.HTML(str(site))
            games = dom.xpath("//a[contains(@data-gpnav, 'item')]")

            for game in games:
                if len(game.xpath(".//div[contains(@class, 'discount_final_price')]")) < 1:
                    continue
                self.game_items_steam.update(
                    {'nome': game.xpath(".//span[contains(@class, 'title')]")[0].text})
                self.game_items_steam.update({'precoDesconto': self.converter_preco_para_float(
                    game.xpath(".//div[contains(@class, 'discount_final_price')]")[0].text)})
                if len(game.xpath(".//div[contains(@class, 'discount_original_price')]")) >= 1:
                    self.game_items_steam.update({'precoTotal': self.converter_preco_para_float(
                        game.xpath(".//div[contains(@class, 'discount_original_price')]")[0].text)})
                else:
                    self.game_items_steam.update({'precoTotal': self.converter_preco_para_float(
                        game.xpath(".//div[contains(@class, 'discount_final_price')]")[0].text)})
                self.game_items_steam.update({'plataforma': next(p["id"] for p in self.plataforma if p["nome"] == 'Computador')})
                self.game_items_steam.update({'midia': 0})
                self.game_items_steam.update(
                    {'link': game.get('href')})
                self.game_items_steam.update({'loja': self.loja})
                self.game_items_steam.update({'linkImagem': game.xpath(".//img")[0].get('src').replace('capsule_sm_120', 'header')})
                self.game_items_list_steam.append(self.game_items_steam.copy())
                if len(self.game_items_list_steam) >= 500:
                    break

        except:
            pass
        finally:
            return self.game_items_list_steam
