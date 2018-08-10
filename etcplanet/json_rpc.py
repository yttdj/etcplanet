import settings
import urllib.request
import datetime
import json
import math

ADD_SIZE   = 42
REW_INIT   = 5
REW_ERA    = 5e6
REW_DEC    = 0.8
REW_UNC    = 1 / 32
ATTO_CONV  = 1e-18
HEXADEC    = 16
N_DISPLAY  = 10
SEARCH_URL = "/search/?search="
HEADER     = {"Content-Type" : "application/json"}

def postprocess_account(result):
        api             = "eth_getTransactionCount"
        search          = result["address"]
        result["nonce"] = json_rpc_(api, [search])["result"]
        result["url"]   = SEARCH_URL + result["address"]
        if result["eth_getCode"] != "0x":
                api     = "eth_getStorageAt"
                search  = result["address"]
                storage = []
                for i in range(result["prev"] + N_DISPLAY, result["next"]):
                        value = json_rpc_(api, [search, hex(i)])["result"]
                        storage.append((i, value))
                result["storage"] = storage
        for e in ["eth_getBalance", "nonce"]:
                result[e] = int(result[e], HEXADEC)

def postprocess_transaction(result):
        api                 = "eth_getBlockByNumber"
        search              = result["blockNumber"]
        result["block"]     = json_rpc_(api, [search, False])["result"]
        api                 = "eth_getTransactionReceipt"
        search              = result["hash"]
        result["gasUsed"]   = json_rpc_(api, [search])["result"]["gasUsed"]
        utc                 = datetime.datetime.utcfromtimestamp
        result["timestamp"] = utc(int(result["block"]["timestamp"], HEXADEC))
        result["timestamp"] = str(result["timestamp"])
        for e in ["blockNumber",
                  "gas",
                  "gasPrice",
                  "gasUsed",
                  "nonce",
                  "transactionIndex",
                  "v",
                  "value"]:
                result[e] = int(result[e], HEXADEC)

def get_reward(result):
        reward_base   = (int(result["number"], HEXADEC) - 1) // REW_ERA
        reward_base   = REW_INIT * REW_DEC ** reward_base
        reward_base   = round(reward_base,   -int(math.log10(ATTO_CONV)))
        reward_uncles = len(result["uncles"]) * REW_UNC * reward_base
        reward_uncles = round(reward_uncles, -int(math.log10(ATTO_CONV)))
        reward_gas    = 0
        for e in result["transactions"]:
                api         = "eth_getTransactionByHash"
                gas_price   = json_rpc_(api, [e])["result"]
                gas_price   = int(gas_price["gasPrice"], HEXADEC)
                api         = "eth_getTransactionReceipt"
                gas_used    = json_rpc_(api, [e])["result"]
                gas_used    = int(gas_used["gasUsed"], HEXADEC)
                reward_gas += ATTO_CONV * gas_price * gas_used

        return reward_base + reward_uncles + reward_gas

def postprocess_block(result):
        result["reward"]    = get_reward(result)
        utc                 = datetime.datetime.utcfromtimestamp
        result["timestamp"] = str(utc(int(result["timestamp"], HEXADEC)))
        result["url"]       = SEARCH_URL + str(int(result["number"], HEXADEC))
        beg                 = result["prev"] + N_DISPLAY
        end                 = len(result["transactions"])
        end                 = min(end, result["next"])
        for i, e in enumerate(result["transactions"][beg:end]):
                result["transactions"][beg + i] = (beg + i, e, SEARCH_URL + e)
        result["transactions"] = result["transactions"][beg:end]
        for e in ["gasLimit", "gasUsed", "number", "size"]:
                result[e] = int(result[e], HEXADEC)

def json_rpc_(api, args):
        request = {"method" : api, "params" : args, "jsonrpc" : "2.0", "id" : 1}
        request = json.dumps(request).encode()
        url     = urllib.request.Request(settings.PARITY_URL, headers = HEADER)
        result  = urllib.request.urlopen(url, request).read().decode()
        result  = json.loads(result)

        return result

def json_rpc(get):
        search = get["search"].strip().lower()
        if   len(search) <  ADD_SIZE - 2:
                api    = "eth_getBlockByNumber"
                result = json_rpc_(api, [hex(int(search)), False])["result"]
        elif len(search) <= ADD_SIZE:
                result = {"address" : search}
                for api in ["eth_getBalance", "eth_getCode"]:
                        result[api] = json_rpc_(api, [search])["result"]
        else:
                api    = "eth_getTransactionByHash"
                result = json_rpc_(api, [search])["result"]
                if not result:
                        api    = "eth_getBlockByHash"
                        result = json_rpc_(api, [search, False])["result"]
        result["type"] = api[len("eth_get"):api.find("By")].lower()
        if result["type"] not in ["block", "transaction"]:
                result["type"] = "account"
        if "beg" in get:
                result["prev"] = int(get["beg"]) - N_DISPLAY
                result["next"] = int(get["beg"]) + N_DISPLAY
        else:
                result["prev"] = -N_DISPLAY
                result["next"] = N_DISPLAY
        globals()["postprocess_" + result["type"]](result)

        return result
