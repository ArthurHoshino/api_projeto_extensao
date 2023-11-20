from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
from lxml import etree

class MagaluScrapper():
    def __init__(self, driverName, data):
        self.driverName = driverName
        self.plataforma = data["P"]
        self.loja = data["L"]
        self.game_items_magalu = {}
        self.game_items_list_magalu = []
        self.total_paginas = 0
        self.page = 1
        self.url_index = 0
        self.urls = {
                0: 'https://www.magazineluiza.com.br/busca/switch/?filters=entity---game&page=',

                1: 'https://www.magazineluiza.com.br/busca/ps4/?filters=entity---game&page=',
                2: 'https://www.magazineluiza.com.br/busca/ps5/?filters=entity---game&page=',

                3: 'https://www.magazineluiza.com.br/busca/xbox/?filters=entity---game&page=',
               }

        self.urls_plataforma = {
                0: 'Nintendo',

                1: 'PlayStation',
                2: 'PlayStation',

                3: 'Xbox',
               }

    def ReabrirDriver(self, url, offset):
        try:
            options = Options()
            options.add_experimental_option("detach", True)
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            driver.set_page_load_timeout(15)
            driver.get(url + str(offset))
            driver.maximize_window()
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
                self.page = 1
                while True:
                    if self.page == self.total_paginas or self.page >= 50:
                        break
                    else:
                        site = self.ReabrirDriver(self.urls[self.url_index], self.page)
                        dom = etree.HTML(str(site))
                        self.total_paginas = dom.xpath("//a[contains(@data-testid, 'pagination-item')]")[-1].text
                        games = dom.xpath("//a[contains(@data-testid, 'product-card-container')]")

                        for game in games:
                            if len(game.xpath(".//p[contains(@data-testid, 'price-value')]")) < 1:
                                continue
                            self.game_items_magalu.update({'nome': game.xpath(".//h2[contains(@data-testid, 'product-title')]")[0].text})
                            self.game_items_magalu.update({'precoDesconto': self.converter_preco_para_float(game.xpath(".//p[contains(@data-testid, 'price-value')]")[0].text)})
                            if len(game.xpath(".//p[contains(@data-testid, 'price-original')]")) >= 1:
                                self.game_items_magalu.update({'precoTotal': self.converter_preco_para_float(game.xpath(".//p[contains(@data-testid, 'price-original')]")[0].text)})
                            else:
                                self.game_items_magalu.update({'precoTotal': self.converter_preco_para_float(game.xpath(".//p[contains(@data-testid, 'price-value')]")[0].text)})
                            self.game_items_magalu.update({'plataforma': next(p["id"] for p in self.plataforma if p["nome"] == self.urls_plataforma[self.url_index])})
                            self.game_items_magalu.update({'midia': 1})
                            self.game_items_magalu.update({'link': 'https://www.magazineluiza.com.br/' + game.get('href')})
                            self.game_items_magalu.update({'loja': self.loja})
                            self.game_items_magalu.update({'linkImagem': game.xpath(".//img")[0].get('src')})
                            self.game_items_list_magalu.append(self.game_items_magalu.copy())

                        self.page += 1

                self.url_index += 1
                if self.url_index >= 4:
                    break
        except:
            pass
        finally:
            return self.game_items_list_magalu
