import json
import os
from lib.insight_api import Insight


def fetch_tx_record(address='XkbRp5aT5vGnYi7obCGvmX2FAQV34u6Dfw'):
    info = insight_api.fetch_wallet_info(address)

    print(info)

    pass


def prepare_sankey(tx_data):

    pass


def save_data(payload, filename):

    # Set current working directory based on where the file is that we're running
    dirname = os.path.dirname(os.path.abspath(__file__))

    # Add .json to the filename if it isn't present
    if ".json" not in filename:
        filename = filename + '.json'
    else:

        pass

    absolute_file_path = os.path.abspath(os.path.join(dirname, filename))

    with open(absolute_file_path, 'w') as dest:
        json.dump(payload, dest)

    return True


def read_json(filename):
    cache_dir = '../_cache/'
    dirname = os.path.dirname(os.path.abspath(__file__))
    absolute_cache_dir = os.path.abspath(os.path.join(dirname, cache_dir))
    filename = filename + '.json'
    absolute_file_path = os.path.abspath(os.path.join(absolute_cache_dir, filename))

    try:
        with open(absolute_file_path, 'r') as json_stuff:
            data_dict = json.loads(json_stuff)
    except TypeError as e:
        try:
            with open(absolute_file_path, 'r') as json_stuff:
                json_stuff = json_stuff.read()
                data_dict = json.loads(json_stuff)
        except Exception as e:
            print(e)
            data_dict = {}
    return data_dict


if __name__ == '__main__':
    # Instantiate the Insight API class
    insight_api = Insight()

    # Set test address variable
    test_address = 'XkbRp5aT5vGnYi7obCGvmX2FAQV34u6Dfw'

    fetch_tx_record(test_address)

