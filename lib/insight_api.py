import requests
import json
from json import JSONDecodeError
import random
from multiprocessing import Pool
from functools import partial


class Insight:

    def __init__(self):
        self.url_round_robin()

    @classmethod
    def url_round_robin(self):
        """
            Sets the base API URL for the Insight Explorer that we'll be using.  
        """

        base_url_1 = 'https://insight.dashevo.org/'
        base_url_2 = 'https://insight.dash.org'
        urls = [base_url_1, base_url_2]

        url_selected = random.choice(urls)

        self.url = url_selected

        return url_selected

    @classmethod
    def fetch_block_txs(self, block_height):
        """
            Fetch all transactions in a specific block
        """

        # Get block hash from height
        block_height_url = "{}/insight-api-dash/block-index/{}".format(self.url_round_robin(),block_height)
        response = requests.get(block_height_url)

        block_hash = response.json()['blockHash']

        # Get transaction in block hash
        block_hash_url = "{}/insight-api-dash/txs/?block={}".format(self.url_round_robin(), block_hash)
        response = requests.get(block_hash_url)

        block_txs = response.json()['txs']

        return block_txs

    @classmethod
    def get_wallet_tx(self, address):
        """
        Fetch all transactions belonging to a specific address
        """

        fetch_wallet_url = "{}/insight-api-dash/addr/{}".format(self.url_round_robin(), address)
        response = requests.request("GET", fetch_wallet_url)

        try:
            transaction_list = json.loads(response.text)['transactions']  # Temporarily disabled for GetFreeDash
            # transaction_list = json.loads(response.text)
            # print(transaction_list)
            return transaction_list

        except KeyError:
            return []

    @classmethod
    def fetch_transaction_history(self, txid, address):
        """
        Fetch info on a specific txid
        """

        fetch_tx_url = "{}/insight-api-dash/tx/{}".format(self.url_round_robin(), txid)
        response = requests.request("GET", fetch_tx_url)

        outgoing_tx = []
        incoming_tx = []

        try:
            transaction_info = json.loads(response.text)

            for vout in transaction_info['vout']:
                amount_to_address = float(vout['value'])
                try:
                    trans_dict = {
                        "amount": amount_to_address,
                        "sent_to": vout['scriptPubKey']['addresses']
                    }

                    outgoing_tx.append(trans_dict)

                except KeyError or UnboundLocalError:
                    print("Found no information on TXID: {}".format(vout['spentTxId']))
                    continue

            for vin in transaction_info['vin']:
                amount_to_address = float(vin['value'])
                try:
                    trans_dict = {
                        "amount": amount_to_address,
                        "sent_from": vin['addr']
                    }

                    incoming_tx.append(trans_dict)
                except KeyError or UnboundLocalError:
                    print("Found no information on TXID: {}".format(vin['txid']))
                    continue

            return incoming_tx, outgoing_tx

        except JSONDecodeError:
            print("Error with that transaction")
            null_dict = {
                "amount": 'Null',
                "time": 'Null',
                "date": 'Null',
                "type": 'Null'
            }
            return null_dict

    @classmethod
    def fetch_wallet_info(self, address):
        """
            Performs multi-threaded fetching of transaction history for a given address, tying together 
        """

        transaction_list = self.get_wallet_tx(address)
        num_of_processes = 2
        p = Pool(num_of_processes)
        matching_tx = p.map(partial(self.fetch_transaction_history, address=address), transaction_list)
        p.close()
        p.join()

        cleaned_transactions = []

        for tx_info in matching_tx:
            if tx_info is not False:
                cleaned_transactions.append(tx_info)
            else:
                continue

        return cleaned_transactions


if __name__ == '__main__':
    pass