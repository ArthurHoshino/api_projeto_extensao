import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
from lxml import etree

class ZoomScrapper():
    def __init__(self, driverName, data):
        self.driverName = driverName
        self.plataforma = data["P"]
        self.loja = data["L"]
        self.page = 1
        self.game_items_zoom = {}
        self.game_items_list_zoom = []
        self.url_index = 0
        self.urls = {
                0: 'https://www.zoom.com.br/jogos-nintendo-switch?page=',
                1: 'https://www.zoom.com.br/jogos-wii?page=',
                2: 'https://www.zoom.com.br/jogos-nintendo-ds?page=',

                3: 'https://www.zoom.com.br/jogos-ps2?page=',
                4: 'https://www.zoom.com.br/jogos-ps3?page=',
                5: 'https://www.zoom.com.br/jogos-ps4?page=',
                6: 'https://www.zoom.com.br/jogos-ps5?page=',

                7: 'https://www.zoom.com.br/jogos-xbox-360?page=',
                8: 'https://www.zoom.com.br/jogos-xbox-one?page=',
                9: 'https://www.zoom.com.br/jogos-xbox-series?page='
               }

        self.urls_plataforma = {
                0: 'Nintendo',
                1: 'Nintendo',
                2: 'Nintendo',

                3: 'PlayStation',
                4: 'PlayStation',
                5: 'PlayStation',
                6: 'PlayStation',

                7: 'Xbox',
                8: 'Xbox',
                9: 'Xbox',
               }

    def ReabrirDriver(self, url, offset):
        try:
            options = Options()
            options.add_experimental_option("detach", True)
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            driver.set_page_load_timeout(15)
            driver.get(url + str(offset))
            driver.maximize_window()
            time.sleep(0.5)
            driver.execute_script('window.scrollBy(0, document.body.scrollHeight)')
            time.sleep(0.5)
            driver.execute_script('window.scrollBy(0, document.body.scrollHeight)')
            time.sleep(0.5)
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
                    try:
                        site = self.ReabrirDriver(self.urls[self.url_index], self.page)
                        dom = etree.HTML(str(site))
                    except:
                        self.page += 1
                        continue
                    games = dom.xpath("//a[contains(@class, 'ProductCard_ProductCard_Inner')]")

                    for game in games:
                        try:
                            if len(game.xpath(".//p[contains(@class, 'Text_Text')]")) < 1:
                                continue
                            self.game_items_zoom.update({'nome': game.xpath(".//h2[contains(@class, 'Text_Text')]")[0].text})
                            self.game_items_zoom.update({'precoDesconto': self.converter_preco_para_float(game.xpath(".//p[contains(@class, 'Text_Text')]")[0].text)})
                            self.game_items_zoom.update({'precoTotal': self.converter_preco_para_float(game.xpath(".//p[contains(@class, 'Text_Text')]")[0].text)})
                            self.game_items_zoom.update({'plataforma': next(p["id"] for p in self.plataforma if p["nome"] == self.urls_plataforma[self.url_index])})
                            self.game_items_zoom.update({'midia': 1})
                            self.game_items_zoom.update({'link': 'https://www.zoom.com.br' + game.get('href')})
                            self.game_items_zoom.update({'loja': self.loja})
                            self.game_items_zoom.update({'linkImagem': game.xpath(".//img")[0].get('src')})
                            self.game_items_list_zoom.append(self.game_items_zoom.copy())
                        except:
                            pass

                    self.page += 1
                    if (len(games) < 20 and site != None) or self.page >= 125:
                        break

                self.url_index += 1
                if self.url_index >= 10:
                    break

        except:
            pass
        finally:
            return self.game_items_list_zoom
