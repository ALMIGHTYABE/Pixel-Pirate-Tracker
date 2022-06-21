# Import Packages
import yaml
import requests
import pandas as pd

params_path = "params.yaml"


def read_params(config_path):
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config


config = read_params(params_path)

# Scrape Data
try:
    ppnos = pd.read_csv(config["traits"]["pp_nos_csv"])
    hedgey_url = config["traits"]["hedgey_url"]
    nft_list = []

    nft_list.append(config["traits"]["manual_addition"])  # Manual Addition

    for i in ppnos['Number']:
        nft = requests.get(hedgey_url + str(i))
        # Status Code Check
        if nft.status_code == 200:
            # Name Check
            name = nft.json()['name']
            try:
                index = name.index('#')
            except ValueError:
                index = len(name)
            if name[:index].strip() == "Pixel Pirates":
                number = name[index + 1:]
                image = nft.json()['image']
                date = nft.json()['date']
                Background = nft.json()['attributes'][0]['value']
                Base = nft.json()['attributes'][1]['value']
                Outfit = nft.json()['attributes'][2]['value']
                Necklace = nft.json()['attributes'][3]['value']
                Eye = nft.json()['attributes'][4]['value']
                Beard = nft.json()['attributes'][5]['value']
                Hair = nft.json()['attributes'][6]['value']
                Hat = nft.json()['attributes'][7]['value']
                Hand_Accessories = nft.json()['attributes'][8]['value']
                Shoulder = nft.json()['attributes'][9]['value']
                Mouth = nft.json()['attributes'][10]['value']
                Unlock_Date = nft.json()['attributes'][13]['value']
                nft_list.append({'name': name, 'number': number, 'image': image, 'date': date, 'Background': Background,
                                 'Base': Base, 'Outfit': Outfit, 'Necklace': Necklace, 'Eye': Eye, 'Beard': Beard,
                                 'Hair': Hair, 'Hat': Hat, 'Hand_Accessories': Hand_Accessories, 'Shoulder': Shoulder,
                                 'Mouth': Mouth, 'Unlock_Date': Unlock_Date})

    nft_df = pd.DataFrame(nft_list)  # List to df
    nft_df['Batch'] = ppnos['Batch']  # Appending Batch Number to DF
    nft_df['Type'] = ppnos['Type']  # Appending Type to DF

    # Rarity Score Computation
    traits = ['Background', 'Base', 'Outfit', 'Necklace', 'Eye', 'Beard', 'Hair', 'Hat', 'Hand_Accessories', 'Shoulder',
              'Mouth']  # Trait List

    for i in traits:  # Score Computation
        trait_score = []
        for j in nft_df[i]:
            score = 1 / (sum(nft_df[i] == j) / nft_df[i].count())
            trait_score.append(score)
        name = i + " Score"
        nft_df[name] = trait_score

    nft_df['Bonus Score'] = 0  # Bonus Score based on NFT Type
    nft_df.loc[nft_df['Type'] == "Legendary", 'Bonus Score'] = 5000
    nft_df.loc[nft_df['Type'] == "Specials", 'Bonus Score'] = 2000

    score_list = ['Bonus Score', 'Background Score', 'Base Score', 'Outfit Score', 'Necklace Score', 'Eye Score',
                  'Beard Score', 'Hair Score', 'Hat Score', 'Hand_Accessories Score', 'Shoulder Score', 'Mouth Score']

    nft_df['Total Score'] = nft_df[score_list].sum(axis=1)  # Summation of Scores

    nft_df = nft_df.reindex(
        columns=['name', 'number', 'image', 'date', 'Batch', 'Type', 'Total Score', 'Bonus Score', 'Background',
                 'Background Score', 'Base', 'Base Score', 'Outfit', 'Outfit Score',
                 'Necklace', 'Necklace Score', 'Eye', 'Eye Score', 'Beard', 'Beard Score', 'Hair', 'Hair Score', 'Hat',
                 'Hat Score', 'Hand_Accessories', 'Hand_Accessories Score', 'Shoulder', 'Shoulder Score', 'Mouth',
                 'Mouth Score',
                 'Unlock_Date'])  # Ordering of Columns

except Exception as e:
    error = {"error": e}

# Save to CSV
try:
    nft_df.to_csv("pp.csv", index=False)
except Exception as e:
    error = {"error": e}
