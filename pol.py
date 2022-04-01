from web3 import Web3
from web3 import exceptions
import requests
import json
import time


#web3 connection 
polygon_url= "https://polygon-mainnet.g.alchemy.com/v2/TmzbTUjxJsxN9jVjnCXqYUzvk8culqq1"
web3 = Web3(Web3.HTTPProvider(polygon_url))

from web3.middleware import geth_poa_middleware
web3.middleware_onion.inject(geth_poa_middleware, layer=0)



#take mails from file
def take_mails():
    f = open("mails.txt", "r")
    mail_list = f.readlines()
    return mail_list

#take wallets from privatekey 
def take_wallets():
    f = open("wallets.txt", "r")
    wallet_list = f.readlines()
    return wallet_list

#req 1


def take_local_id(session, email): #to auth u need local id key
    headers = {
        'authority': 'www.googleapis.com',
        'sec-ch-ua': '"(Not(A:Brand";v="8", "Chromium";v="100"',
        'x-client-version': 'Chrome/JsCore/8.10.0/FirebaseUI-web',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4862.0 Safari/537.36',
        'x-firebase-locale': 'en',
        'sec-ch-ua-platform': '"Windows"',
        'accept': '*/*',
        'origin': 'https://crazydefenseheroes.com',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://crazydefenseheroes.com/',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    params = (
        ('key', 'AIzaSyDDnsV0OdAnfWGwEZDGrFiORA6qWe_3r2A'),
    )

    json_data = {
        'email': email,
        'password': '14022014',
        'returnSecureToken': True,
    }

    resp = session.post('https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword', headers=headers, params=params, json=json_data)
    response_json = resp.json()
    local_id = response_json["localId"]
    return local_id


def take_uniq_id(session, player_id):

    headers = {
        'authority': 'cdh-web-api-dot-tower-token-firestore.df.r.appspot.com',
        'sec-ch-ua': '"(Not(A:Brand";v="8", "Chromium";v="100"',
        'accept': 'application/json',
        'sec-ch-ua-mobile': '?0',
        'x-access-token': '',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4862.0 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
        'origin': 'https://crazydefenseheroes.com',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://crazydefenseheroes.com/',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    json_data = {
        'playerId': player_id,
    }

    resp = session.post('https://cdh-web-api-dot-tower-token-firestore.df.r.appspot.com/star_chest/id_generator', headers=headers, json=json_data)
    response_json= resp.json()
    id = response_json["id"]
    return id

#uniq id to acc to transact this to claim
def take_player_id(session, local_id):
    
    headers = {
        'authority': 'tower-token-firestore.df.r.appspot.com',
        'sec-ch-ua': '"(Not(A:Brand";v="8", "Chromium";v="100"',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4862.0 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
        'content-type': 'text/plain;charset=UTF-8',
        'accept': '*/*',
        'origin': 'https://crazydefenseheroes.com',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://crazydefenseheroes.com/',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    data = {"Firebaseuuid": local_id, "SiwaId":"","CdhPlayerId":""}
    resp = session.post('https://tower-token-firestore.df.r.appspot.com/login/id', headers=headers, data=json.dumps(data))

    response_json= resp.json()
    
    player_id = response_json["CdhPlayerId"]
    
    return player_id


#get reward history

def take_reward_hist(session, playerId):
    headers = {
        'authority': 'cdh-web-api-dot-tower-token-firestore.df.r.appspot.com',
        'sec-ch-ua': '"(Not(A:Brand";v="8", "Chromium";v="100"',
        'accept': 'application/json',
        'sec-ch-ua-mobile': '?0',
        'x-access-token': '',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4862.0 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
        'origin': 'https://crazydefenseheroes.com',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://crazydefenseheroes.com/',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    json_data = {
        'playerId': playerId,
    }

    resp = session.post('https://cdh-web-api-dot-tower-token-firestore.df.r.appspot.com/star_chest/get_star_chest_info', headers=headers, json=json_data)
    response_json =resp.json()
    result = len(response_json["calender_info"])
    return result

#main

def main(web3):
    wallets_complite = 0
    wallets_error= 0
    errored_wallets = []
    
    
    wallet_list = take_wallets()
    mails_list= take_mails()
   
    farm_address = Web3.toChecksumAddress(0xe57dad9c809c5ff0162b17d220917089d4cc7075)
    farm_abi = json.loads('''[{"inputs":[{"internalType":"string","name":"_name","type":"string"},{"internalType":"string","name":"_version","type":"string"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"userAddress","type":"address"},{"indexed":false,"internalType":"uint256","name":"blockTimestamp","type":"uint256"},{"indexed":false,"internalType":"string","name":"uniqueUuid","type":"string"}],"name":"DailyTrackerCheckInDone","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"userAddress","type":"address"},{"indexed":false,"internalType":"address payable","name":"relayerAddress","type":"address"},{"indexed":false,"internalType":"bytes","name":"functionSignature","type":"bytes"}],"name":"MetaTransactionExecuted","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"account","type":"address"}],"name":"Paused","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"account","type":"address"}],"name":"Unpaused","type":"event"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"_dailyTrackerTimestampDays","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"","type":"string"}],"name":"_dailyUserUuid","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"userAddress","type":"address"}],"name":"checkDailyTimestampValidity","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"checkDailyTimestampValidity","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"uniqueUuid","type":"string"}],"name":"checkDailyUuidValidity","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"uniqueUuid","type":"string"}],"name":"dailyLog","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"userAddress","type":"address"},{"internalType":"bytes","name":"functionSignature","type":"bytes"},{"internalType":"bytes32","name":"sigR","type":"bytes32"},{"internalType":"bytes32","name":"sigS","type":"bytes32"},{"internalType":"uint8","name":"sigV","type":"uint8"}],"name":"executeMetaTransaction","outputs":[{"internalType":"bytes","name":"","type":"bytes"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"}],"name":"getNonce","outputs":[{"internalType":"uint256","name":"nonce","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"pause","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"paused","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"unpause","outputs":[],"stateMutability":"nonpayable","type":"function"}]''')
    farm_contract = web3.eth.contract(address=farm_address, abi=farm_abi)
    mail_index = 0
    for wallet in wallet_list:
        
        session = requests.session()
        wallet=wallet.strip()
        privateKey= wallet
        account = web3.eth.account.privateKeyToAccount(privateKey)
        publicKey = account.address
        web3.eth.defaultAccount = account.address
        print(web3.isConnected(), "Account now -->", mail_index+1)

        mail_and_pass=mails_list[mail_index]
        mail=mail_and_pass.split(":")
        mail=mail[0]
            
            
            
            
        try:
            local_id = take_local_id(session, mail)
            player_id = take_player_id(session, local_id)
            uniq_id = take_uniq_id(session, player_id)
            reward_history = take_reward_hist(session, player_id)
                
            try:
                nonce = web3.eth.getTransactionCount(web3.eth.defaultAccount)
                tx = farm_contract.functions.dailyLog(str(uniq_id)).buildTransaction({"nonce": nonce, "maxFeePerGas": Web3.toWei(42, 'gwei'), "maxPriorityFeePerGas": Web3.toWei(33, 'gwei')})
                signed_tx=web3.eth.account.signTransaction(tx, private_key= privateKey)
                res = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
                res = res.hex()
                
                reward_history_after = take_reward_hist(session, player_id)
                if reward_history_after> reward_history:
                    status="Claimed"
                else:
                    status = "Unclaimed"
                    
                print(publicKey, status, res)  
                    
                #print(publicKey, res)
                wallets_complite+=1
            except exceptions.SolidityError as error:
                print(account.address, error)
                
            
            
            


        except KeyError as errorr:
            errored_wallets.append(account.address)
            print(account.address, errorr)
            wallets_error+=1
        
            
        session.close()
        mail_index+=1
    

    print("Wallets unclaimed --> ", errored_wallets,  "\n", "Total uncomplite: ",  wallets_error)

if __name__ == '__main__':
    main(web3)