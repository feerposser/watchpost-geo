import csv
import googlemaps
import time
from difflib import SequenceMatcher

from bairros.models import ModelBairro
from cidades.manage_data import Cidade

nome_cidade = 'Tapejara'

tipo_bairro = 'sublocality_level_1'
tipo_cidade = 'administrative_area_level_2'
tipo_estado = 'administrative_area_level_1'
tipo_pais = 'country'

KEY = 'AIzaSyBYoU0ZrNNsAK-56cJBMK2LooCa5RtgqfQ'
gmaps = googlemaps.Client(key=KEY)

cidade = Cidade(nome_cidade)

city_bounds = cidade.get_city_bounds()

relatorio_path = 'C:/WATCHPOST-GEO/watchpost_geo/alg_utils/relatorio_testes_insercao_bairros_tapejara.txt'
file = open(relatorio_path, 'a')
file.writelines("Data e hora:" + time.strftime("%d-%m-%Y %H:%M:%S"))
file.writelines("\n\n")
file.close()

reader = csv.reader(open('alg_utils/bairros_tapejara.csv'), delimiter=';')


def cria_bairro(data={}, tipo='insere'):
    b = ModelBairro()
    if tipo == 'insere':
        try:
            b.cidade = cidade.get_city()
            b.nome = data['nome']
            b.bounds_northeast_lat = data['bounds_northeast_lat']
            b.bounds_northeast_lng = data['bounds_northeast_lng']
            b.bounds_southwest_lat = data['bounds_southwest_lat']
            b.bounds_southwest_lng = data['bounds_southwest_lng']
            b.latitude = data['latitude']
            b.longitude = data['longitude']
            b.endereco = data['endereco']
            b.status = data['status']
            b.save()
            return True, b

        except Exception as e:
            print("1 Problema ao salvar o bairro:", e)
            return False, e
    else:
        try:
            b.cidade = cidade.get_city()
            b.nome = data['nome']
            b.status = 'I'
            b.save()
            print('aquuiiiii', b)
            return True, b
        except Exception as e:
            print('2 Problema ao salvar o bairro:', e)
            return False, e


def escreve_relatorio(frase, step=1):
    with open(relatorio_path, "a") as file:
        for linha in frase:
            linha = str(linha)
            file.writelines(linha + "\n")
        file.writelines("\n"*step)


counter = 0
show_time = 0
fora_indice = 0
not_bairro = 0
fora_lista_nomes = 0
nao_api = 0

for i in reader:
    counter += 1
    bairro = None
    long_name = i[0]

    try:
        print(counter, 'Local:', i[0])
        escreve_relatorio([str(counter) + ' - ' + i[0]])
        bairro = gmaps.geocode(address=str(i[0]) + ' PASSO FUNDO',
                               language='pt-BR',
                               region='br',
                               bounds=city_bounds)[0]

    except IndexError as e:
        fora_indice += 1
        erro = ["->Erro de indice. Bairro não encontrado. %s " % e]
        print(*erro)
        escreve_relatorio(erro, step=5)

    try:
        if bairro:
            """
            1. Verificar se é um bairro
            2. Verificar se está em PF
            3. Verificar se os nomes batem
            """
            nomes = []

            if tipo_bairro in bairro['types']:
                for j in bairro['address_components']:
                    if tipo_bairro in j['types']:
                        nomes.append(str(j['long_name']).upper())
                        nomes.append('Endereço completo: ' + bairro['formatted_address'])
                        long_name = str(j['long_name']).upper()

                if SequenceMatcher(None, i[0], nomes[0]).ratio() > 0.3:
                    print("SHOW!!!", nomes)
                    escreve_relatorio(['Estava na lista de nomes %s' % nomes])

                    insere_banco = cria_bairro(data={
                        'nome': long_name,
                        'bounds_northeast_lat':
                            bairro['geometry']['bounds']['northeast']['lat'],
                        'bounds_northeast_lng':
                            bairro['geometry']['bounds']['northeast']['lng'],
                        'bounds_southwest_lat':
                            bairro['geometry']['bounds']['southwest']['lat'],
                        'bounds_southwest_lng':
                            bairro['geometry']['bounds']['southwest']['lng'],
                        'latitude': bairro['geometry']['location']['lat'],
                        'longitude': bairro['geometry']['location']['lng'],
                        'endereco': bairro['formatted_address'],
                        'status': 'A'}
                    )

                    if insere_banco[0]:
                        show_time += 1
                        escreve_relatorio(["Bairro inserido no banco de dados. ID:", str(insere_banco[1].id)], step=3)
                    else:
                        raise Exception("::::::::::::::Erro ao inserir no banco de dados.")
                else:
                    erro = ["Não está na lista de nomes %s" % nomes]
                    fora_lista_nomes += 1
                    raise Exception(erro)
            else:
                erro = ["Não é bairro segundo a API %s " % bairro['types'],
                        'Endereço completo encontrado: %s' % bairro['formatted_address'],
                        'componentes de endereço: %s' % bairro['address_components']]
                nao_api += 1
                raise Exception(erro)

            nomes.clear()

        else:
            not_bairro += 1
            erro = ["Não foi encontrado"]
            raise Exception(erro)

    except Exception as e:
        print('\n\n\t---->', repr(e))
        escreve_relatorio([e], step=5)
        bl = cria_bairro(data={'nome': long_name or 'Bairro Indefinido'}, tipo='deu ruim')
        escreve_relatorio(["Adicionado como indefinido:", "id: %s" % bl[1].id])

print('\n\n\n\n\nShowtime->', show_time)
print('fora_indice->', fora_indice)
print('not_bairro->', not_bairro)
print('fora_lista_nomes->', fora_lista_nomes)
print('nao_api->', nao_api)



# {'geometry': {'bounds': {'northeast': {'lat': -28.2331624, 'lng': -52.3696721},
#                          'southwest': {'lat': -28.2576109, 'lng': -52.3941625}},
#               'location': {'lat': -28.2455429, 'lng': -52.3852925},
#               'location_type': 'APPROXIMATE',
#               'viewport': {'northeast': {'lat': -28.2331624, 'lng': -52.3696721},
#                            'southwest': {'lat': -28.2576109, 'lng': -52.3941625}}
#               },
#  'place_id': 'ChIJ14-XL3PA4pQRKiOKfYVyx2E',
#  'address_components': [
#     {'short_name': 'Petrópolis', 'types': ['political', 'sublocality', 'sublocality_level_1'],
#      'long_name': 'Petrópolis'},
#     {'short_name': 'Passo Fundo', 'types': ['administrative_area_level_2', 'political'], 'long_name': 'Passo Fundo'},
#     {'short_name': 'RS', 'types': ['administrative_area_level_1', 'political'], 'long_name': 'Rio Grande do Sul'},
#     {'short_name': 'BR', 'types': ['country', 'political'], 'long_name': 'Brasil'}
#   ],
#  'types': ['political', 'sublocality', 'sublocality_level_1'],
#  'formatted_address': 'Petrópolis, Passo Fundo - RS, Brasil'}
