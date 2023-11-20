import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
from lxml import etree

class EpicGamesScrapper():
    def __init__(self, driverName, data):
        self.driverName = driverName
        self.plataforma = data["P"]
        self.loja = data["L"]
        self.page = 0
        self.game_items_epicgames = {}
        self.game_items_list_epicgames = []

    def ReabrirDriver(self, offset):
        try:
            options = Options()
            options.add_experimental_option("detach", True)
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            driver.set_page_load_timeout(15)
            driver.get('https://store.epicgames.com/pt-BR/browse?sortBy=releaseDate&sortDir=DESC&priceTier=tierDiscouted&count=40&start=' + str(offset))
            driver.maximize_window()
            time.sleep(3)
            driver.execute_script('window.scrollBy(0, 1800)')
            time.sleep(3)
            driver.execute_script('window.scrollBy(0, 1800)')
            time.sleep(3)
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
            while True:
                try:
                    site = self.ReabrirDriver(self.page * 40)
                    dom = etree.HTML(str(site))
                except:
                    self.page += 1
                    continue
                games = dom.xpath('//li/div/div/a')

                for game in games:
                    try:
                        if len(game.xpath(".//div/div/div[2]/div[3]/div/div[2]/div/div[2]/span")) < 1:
                            continue
                        self.game_items_epicgames.update({'nome': game.xpath(".//div/div/div[2]/div[2]/div/div")[0].text})
                        self.game_items_epicgames.update({'precoDesconto': self.converter_preco_para_float(game.xpath(".//div/div/div[2]/div[3]/div/div[2]/div/div[2]/span")[0].text)})
                        if len(game.xpath(".//div/div/div[2]/div[3]/div/div[2]/div/div[1]/span/div")) >= 1:
                            self.game_items_epicgames.update({'precoTotal': self.converter_preco_para_float(game.xpath(".//div/div/div[2]/div[3]/div/div[2]/div/div[1]/span/div")[0].text)})
                        else:
                            self.game_items_epicgames.update({'precoTotal': self.converter_preco_para_float(game.xpath(".//div/div/div[2]/div[3]/div/div[2]/div/div[2]/span")[0].text)})
                        self.game_items_epicgames.update({'plataforma': next(p["id"] for p in self.plataforma if p["nome"] == 'Computador')})
                        self.game_items_epicgames.update({'midia': 0})
                        self.game_items_epicgames.update({'link': 'https://store.epicgames.com' + game.get('href')})
                        self.game_items_epicgames.update({'loja': self.loja})
                        self.game_items_epicgames.update({'linkImagem': game.xpath(".//img")[0].get('src')})
                        self.game_items_list_epicgames.append(self.game_items_epicgames.copy())
                    except:
                        pass

                self.page += 1
                if (len(games) < 35 and site != None) or self.page >= 125:
                    break
        except:
            pass
        finally:
            return self.game_items_list_epicgames

