# Import Packages
import yaml
import os
import pandas as pd
from web3 import Web3
from pymongo import MongoClient
import requests
import time
from datetime import datetime

params_path = "params.yaml"


def read_params(config_path):
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config


config = read_params(params_path)

# Scrape Data and Save to CSV
try:
    ppnos = pd.read_csv(config["traits"]["pp_nos_csv"])
    nft_df = pd.read_csv(config["scrape"]["pp_traits_csv"])

    provider_url = config["scrape"]["provider_url"]
    w3 = Web3(Web3.HTTPProvider(provider_url))

    abi = config["scrape"]["abi"]
    contract_address = config["scrape"]["contract_address"]

    contract_instance = w3.eth.contract(address=contract_address, abi=abi)
    wallet_address = []
    for i in nft_df['number']:
        wallet_address.append(contract_instance.functions.ownerOf(int(i)).call())

    nft_df['address'] = wallet_address  # Appending addresses to DF

    nft_df.to_csv("ppmain.csv", index=False)  # Save to CSV

    sales_history = config["scrape"]["sales_history"]

    r = requests.get(sales_history)
    # Status Code Check
    if r.status_code == 200:
        sale = r.json()['sales']
        sales_df = pd.json_normalize(sale)  # JSON to DF
        sales_df.price = df.price.apply(lambda x: int(x) / 1000000000000000000)
        sales_df.endTime = sales_df.endTime.apply(lambda x: time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(x))))
        sales_df.to_csv("pphistory.csv", index=False)  # Save to CSV
    else:
        pass
        
except Exception as e:
    error = {"error": e}
