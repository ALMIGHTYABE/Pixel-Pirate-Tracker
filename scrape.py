# Import Packages
import yaml
import os
import pandas as pd
from web3 import Web3
from pymongo import MongoClient

params_path = "params.yaml"

def read_params(config_path):
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config

config = read_params(params_path)

# Scrape Data
try:
    ppnos = pd.read_csv(config["traits"]["pp_nos_csv"])
    nft_df = pd.read_csv(config["scrape"]["pp_traits_csv"])

    provider_url = config["scrape"]["provider_url"]
    w3 = Web3(Web3.HTTPProvider(provider_url))

    abi = config["scrape"]["abi"]
    contract_address = config["scrape"]["contract_address"]

    contract_instance = w3.eth.contract(address = contract_address, abi = abi)
    wallet_address = []
    for i in nft_df['number']:
        wallet_address.append(contract_instance.functions.ownerOf(int(i)).call())

    nft_df['address'] = wallet_address # Appending addresses to DF
    nft_df['Batch'] = ppnos['Batch'] # Appending Batch Number to DF
    nft_df['Type'] = ppnos['Type'] # Appending Type to DF
except Exception as e:
    error = {"error": e}

# Save to CSV
try:
    nft_df.to_csv("ppmain.csv", index=False)
except Exception as e:
    error = {"error": e}