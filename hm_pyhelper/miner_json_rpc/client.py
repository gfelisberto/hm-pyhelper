import requests
from hm_pyhelper.miner_json_rpc.exceptions import MinerConnectionError
from hm_pyhelper.miner_json_rpc.exceptions import MinerMalformedURL
from hm_pyhelper.miner_json_rpc.exceptions import MinerRegionUnset


class Client(object):

    def __init__(self, url='http://helium-miner:4467'):
        self.url = url

    def __fetch_data(self, method, **kwargs):
        '''
        try:
            response = requests.request(method, self.url, **kwargs)
            parsed = parse(response.json())
            return parsed.result
        except requests.exceptions.ConnectionError:
            raise MinerConnectionError(
                "Unable to connect to miner %s" % self.url
            )
        except requests.exceptions.MissingSchema:
            raise MinerMalformedURL(
                "Miner JSONRPC URL '%s' is not a valid URL"
                % self.url
            )
        '''
        req_body = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": method,
            "params": {}
        }
        resp = requests.post(self.URL, json=req_body)

        if resp.status_code != 200:
            raise Exception("Error happened")

        return resp.json().get('result')

    def get_height(self):
        return self.__fetch_data('info_height')

    def get_region(self):
        region = self.__fetch_data('info_region')
        if not region.get('region'):
            raise MinerRegionUnset(
                "Miner at %s does not have an asserted region"
                % self.url
            )
        return region

    def get_summary(self):
        return self.__fetch_data('info_summary')

    def get_peer_addr(self):
        return self.__fetch_data('peer_addr')

    def get_peer_book(self):
        return self.__fetch_data('peer_book')

    def get_firmware_version(self):
        summary = self.get_summary()
        return summary.get('firmware_version')
