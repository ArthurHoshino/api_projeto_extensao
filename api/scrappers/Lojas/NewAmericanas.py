from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
from lxml import etree

class AmericanasScrapper():
    def __init__(self, driverName, data) -> None:
        self.page = 0
        self.game_items_americanas = {}
        self.game_items_list_americanas = []
        self.url_index = 0
        self.urls = {
            0: 'https://www.americanas.com.br/categoria/games/jogos-para-consoles/nintendo/g/tipo-de-produto-Jogo/tipo-de-produto-Game?limit=24&offset=',
            1: 'https://www.americanas.com.br/categoria/games/jogos-para-consoles/playstation/g/tipo-de-produto-Jogo/tipo-de-produto-Game?limit=24&offset=',
            2: 'https://www.americanas.com.br/categoria/games/jogos-para-consoles/xbox/g/tipo-de-produto-Jogo/tipo-de-produto-Game?limit=24&offset='
        }
        self.urls_plataforma = {
            0: 'Nintendo',
            1: 'PlayStation',
            2: 'Xbox'
        }
        self.driverName = driverName
        self.plataforma = data["P"]
        self.loja = data["L"]

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
                self.page = 0

                while True:
                    print(f'Pagina:     {self.page + 1}\nPlataforma: {self.urls_plataforma[self.url_index]}')
                    try:
                        site = self.ReabrirDriver(self.urls[self.url_index], self.page * 24)
                        dom = etree.HTML(str(site))
                    except:
                        self.page += 1
                        continue
                    games = dom.xpath("//div[contains(@class, 'inStockCard__Wrapper')]")
                    print(len(games))
                    print()

                    for game in games:
                        try:
                            if len(game.xpath(".//span[contains(@class, 'price__PromotionalPrice')]")) < 1:
                                continue
                            self.game_items_americanas.update({'nome': game.xpath(".//h3[contains(@class, 'product-name__Name')]")[0].text})
                            self.game_items_americanas.update({'precoDesconto': self.converter_preco_para_float(game.xpath(".//span[contains(@class, 'price__PromotionalPrice')]")[0].text)})
                            if len(game.xpath(".//span[contains(@class, 'price__Price')]")) >= 1:
                                self.game_items_americanas.update({'precoTotal': self.converter_preco_para_float(game.xpath(".//span[contains(@class, 'price__Price')]")[0].text)})
                            else:
                                self.game_items_americanas.update({'precoTotal': self.converter_preco_para_float(game.xpath(".//span[contains(@class, 'price__PromotionalPrice')]")[0].text)})
                            self.game_items_americanas.update({'plataforma': next(p['id'] for p in self.plataforma if p['nome'] == self.urls_plataforma[self.url_index])})
                            self.game_items_americanas.update({'midia': 1})
                            self.game_items_americanas.update({'link': 'https://www.americanas.com.br' + game.xpath(".//a")[0].get('href')})
                            self.game_items_americanas.update({'loja': self.loja})
                            self.game_items_americanas.update({'linkImagem': game.xpath(".//source")[0].get('srcset')})
                            self.game_items_list_americanas.append(self.game_items_americanas.copy())
                        except:
                            pass

                    self.page += 1
                    if (len(games) < 20 and site != None) or self.page >= 125:
                        break
                    break

                self.url_index += 1
                if self.url_index >= 3:
                    break

        except:
            pass
        finally:
            return self.game_items_list_americanas
