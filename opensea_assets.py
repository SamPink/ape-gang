import requests
import pandas as pd

from parseApe import parse_ape_data

base_url = 'https://api.opensea.io/api/v1'
contract = '0x495f947276749ce646f68ac8c248420045cb7b5e'
collection = 'ape-gang'
all_apes = []


#apes2 = apes['assets'][0]

#name = apes['name']

def parse_ape(a):
    dic = {}

    dic['ape_id'] = a['name']

    df = pd.DataFrame(a['traits'])

    try:
        dic['Clothes'] = df[df.trait_type == 'Clothes'].value.item()
    except:
        dic['Clothes'] = None
    
    try:
        dic['Ears'] = df[df.trait_type == 'Ears'].value.item()
    except:
        dic['Ears'] = None
    
    try:
        dic['Hat'] = df[df.trait_type == 'Hat'].value.item()
    except:
        dic['Hat'] = None
    
    try:
        dic['Fur'] = df[df.trait_type == 'Fur'].value.item()
    except:
        dic['Fur'] = None

    try:
        dic['Mouth'] = df[df.trait_type == 'Mouth'].value.item()
    except:
        dic['Mouth'] = None
    
    try:
        dic['Eyes'] = df[df.trait_type == 'Eyes'].value.item()
    except:
        dic['Eyes'] = None
    
    try:
        dic['last_sale'] = int(a['last_sale']['total_price']) / 1000000000000000000
        dic['last_sale_date'] = a['last_sale']['created_date']
    except:
        dic['last_sale'] = None
        dic['last_sale_date'] = None
    
    return dic



df = pd.DataFrame()
for i in range(0, 3):
    #print(i)
    url = f"https://api.opensea.io/api/v1/assets?asset_contract_address=0x495f947276749ce646f68ac8c248420045cb7b5e&order_direction=desc&offset={i*50}&limit=50&collection=ape-gang"
    response = requests.request("GET", url)
    apes = response.json()
    for ape in apes['assets']:
        df = df.append(parse_ape(ape), ignore_index=True)
    print(i)
    #apes_parsed = [parse_ape_data(ape) for ape in apes['assets']]
    #df = pd.DataFrame(apes_parsed)

print(df)

df.to_csv('apes.csv')