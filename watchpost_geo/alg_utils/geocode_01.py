import googlemaps

KEY = 'AIzaSyBYoU0ZrNNsAK-56cJBMK2LooCa5RtgqfQ'
gmaps = googlemaps.Client(key=KEY)

tipo_bairro = 'sublocality_level_1'
tipo_cidade = 'administrative_area_level_2'
tipo_estado = 'administrative_area_level_1'
tipo_pais = 'country'

bairro = gmaps.geocode('VIA SUL, passo fundo, rs brasil', language='pt-BR', region='br')[0]

for i in bairro:
    print(i, ' - ', bairro[i])
# print(bairro)