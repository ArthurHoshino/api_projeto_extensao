import json
from website.models import *
from website.serializers import *
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.scrappers.Lojas.KabumScrapper import KabumScrapper
from api.scrappers.Lojas.TerabyteScrapper import TerabyteScrapper
from api.scrappers.Lojas.AmericanasScrapper import AmericanasScrapper
from api.scrappers.Lojas.BuscapeScrapper import BuscapeScrapper
from api.scrappers.Lojas.CasasBahiaScrapper import CasaBahiaScrapper
from api.scrappers.Lojas.EpicGamesScrapper import EpicGamesScrapper
from api.scrappers.Lojas.GOGScrapper import GOGScrapper
from api.scrappers.Lojas.MagaluScrapper import MagaluScrapper
from api.scrappers.Lojas.NuuvemScrapper import NuuvemScrapper
from api.scrappers.Lojas.SteamScrapper import SteamScrapper
from api.scrappers.Lojas.SubmarinoScrapper import SubmarinoScrapper
from api.scrappers.Lojas.ZoomScrapper import ZoomScrapper

# Global variables
driverName = "chrome"

@api_view(['GET', 'POST'])
def kabum_list(request, format=None):
    if request.method == 'GET':
        data = Produto.objects.all()
        serializer = ProdutoSerializer(data, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = get_plataforma_loja("Kabum")
        scrapperResponse = KabumScrapper(driverName, data).manager()
        return salvarBanco(scrapperResponse)

@api_view(['GET', 'POST'])
def terabyte_list(request, format=None):
    if request.method == 'GET':
        data = Produto.objects.all()
        serializer = ProdutoSerializer(data, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = get_plataforma_loja("Terabyte")
        scrapperResponse = TerabyteScrapper(driverName, data).manager()
        return salvarBanco(scrapperResponse)
    
@api_view(['GET', 'POST'])
def americanas_list(request, format=None):
    if request.method == 'GET':
        data = Produto.objects.all()
        serializer = ProdutoSerializer(data, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = get_plataforma_loja("Americanas")
        scrapperResponse = AmericanasScrapper(driverName, data).manager()
        return salvarBanco(scrapperResponse)
    
@api_view(['GET', 'POST'])
def buscape_list(request, format=None):
    if request.method == 'GET':
        data = Produto.objects.all()
        serializer = ProdutoSerializer(data, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = get_plataforma_loja("Buscape")
        scrapperResponse = BuscapeScrapper(driverName, data).manager()
        return salvarBanco(scrapperResponse)
    
@api_view(['GET', 'POST'])
def casasbahia_list(request, format=None):
    if request.method == 'GET':
        data = Produto.objects.all()
        serializer = ProdutoSerializer(data, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = get_plataforma_loja("Casas Bahia")
        scrapperResponse = CasaBahiaScrapper(driverName, data).manager()
        return salvarBanco(scrapperResponse)
    
@api_view(['GET', 'POST'])
def epicgames_list(request, format=None):
    if request.method == 'GET':
        data = Produto.objects.all()
        serializer = ProdutoSerializer(data, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = get_plataforma_loja("Epic Games")
        scrapperResponse = EpicGamesScrapper(driverName, data).manager()
        return salvarBanco(scrapperResponse)

@api_view(['GET', 'POST'])
def gog_list(request, format=None):
    if request.method == 'GET':
        data = Produto.objects.all()
        serializer = ProdutoSerializer(data, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = get_plataforma_loja("GoG")
        scrapperResponse = GOGScrapper(driverName, data).manager()
        return salvarBanco(scrapperResponse)

@api_view(['GET', 'POST'])
def magalu_list(request, format=None):
    if request.method == 'GET':
        data = Produto.objects.all()
        serializer = ProdutoSerializer(data, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = get_plataforma_loja("Magazine L.")
        scrapperResponse = MagaluScrapper(driverName, data).manager()
        return salvarBanco(scrapperResponse)

@api_view(['GET', 'POST'])
def nuuvem_list(request, format=None):
    if request.method == 'GET':
        data = Produto.objects.all()
        serializer = ProdutoSerializer(data, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = get_plataforma_loja("Nuuvem")
        scrapperResponse = NuuvemScrapper(driverName, data).manager()
        return salvarBanco(scrapperResponse)

@api_view(['GET', 'POST'])
def steam_list(request, format=None):
    if request.method == 'GET':
        data = Produto.objects.all()
        serializer = ProdutoSerializer(data, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = get_plataforma_loja("Steam")
        scrapperResponse = SteamScrapper(driverName, data).manager()
        return salvarBanco(scrapperResponse)

@api_view(['GET', 'POST'])
def submarino_list(request, format=None):
    if request.method == 'GET':
        data = Produto.objects.all()
        serializer = ProdutoSerializer(data, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = get_plataforma_loja("Submarino")
        scrapperResponse = SubmarinoScrapper(driverName, data).manager()
        return salvarBanco(scrapperResponse)

@api_view(['GET', 'POST'])
def zoom_list(request, format=None):
    if request.method == 'GET':
        data = Produto.objects.all()
        serializer = ProdutoSerializer(data, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = get_plataforma_loja("Zoom")
        scrapperResponse = ZoomScrapper(driverName, data).manager()
        return salvarBanco(scrapperResponse)

@api_view(['GET', 'POST'])
def plataforma_e_loja(request, format=None):
    if request.method == 'GET':
        plataformaData = Plataforma.objects.all()
        lojaData = Loja.objects.all()

        plataformaSerializer = PlataformaSerializer(plataformaData, many=True)
        lojaSerializer = LojaSerializer(lojaData, many=True)
        
        data = {
            "P": plataformaSerializer.data,
            "L": lojaSerializer.data
        }
        return Response(data)
    
    elif request.method == "POST":
        plataformaSerializer = PlataformaSerializer(data=[
            {"nome": 'Computador'},
            {"nome": 'PlayStation'},
            {"nome": 'Xbox'},
            {"nome": 'Nintendo'},
        ], many=True)

        lojaSerializer = LojaSerializer(data=[
            {"nome": 'Steam'},
            {"nome": 'Nuuvem'},
            {"nome": 'GoG'},
            {"nome": 'Epic Games'},
            {"nome": 'Buscape'},
            {"nome": 'Zoom'},
            {"nome": 'Americanas'},
            {"nome": 'Magazine L.'},
            {"nome": 'Submarino'},
            {"nome": 'Casas Bahia'},
            {"nome": 'Kabum'},
            {"nome": 'Terabyte'},
        ], many=True)

        if plataformaSerializer.is_valid() and lojaSerializer.is_valid():
            plataformaSerializer.save()
            lojaSerializer.save()
            return Response({
                "plataforma": plataformaSerializer.data,
                "loja": lojaSerializer.data
            }, status=status.HTTP_201_CREATED) 
        return Response({
            "plataforma": plataformaSerializer.errors,
            "loja": lojaSerializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

def get_plataforma_loja(loja):
    plataformaData = Plataforma.objects.all()
    lojaData = Loja.objects.filter(nome=loja)

    plataformaSerializer = PlataformaSerializer(plataformaData, many=True)
    lojaSerializer = LojaSerializer(lojaData, many=True)
    
    data = {
        "P": json.loads(json.dumps(plataformaSerializer.data)),
        "L": json.loads(json.dumps(lojaSerializer.data))[0]["id"]
    }
    return data

def salvarBanco(data):
    serializer = ProdutoSerializer(data=data, many=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)