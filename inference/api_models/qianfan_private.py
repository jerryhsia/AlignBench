from inference.models import api_model
import json
import requests
import time
import os

def single_turn_wrapper(text):
    return [{"role": "user", "content": text}]

class qianfan_private(api_model):
    def __init__(self, workers=10):
        self.model_name = "qianfan-private"
        self.temperature = 0.7
        self.workers = workers

    def get_api_result(self, prompt):
        question = prompt["question"]
        temperature = prompt.get("temperature", self.temperature)

        api_key = os.environ.get('QIANFAN_API_KEY', '')
        api_url = os.environ.get('QIANFAN_API_URL', '')
        api_timeout = os.environ.get('QIANFAN_API_TIMEOUT', '240')
        api_debug = os.environ.get('QIANFAN_API_DEBUG', '').lower()
        api_debug = api_debug == 'true' or api_debug == 'on' or api_debug == '1'

        if len(api_url) == 0:
            raise Exception("QIANFAN_API_URL is empty")

        header = {
            "Content-Type": "application/json"
        }

        start = time.time()

        if len(api_key) > 0:
            header["Authorization"] = "Bearer " + api_key

        messages = single_turn_wrapper(question)
        data = {"messages": messages}
        data = json.dumps(data, ensure_ascii=False)

        try:
            response = requests.post(api_url, data=data, headers=header, timeout=int(api_timeout))

            if api_debug:
                print('[DEBUG] cost:%.2f request:%s \033[32m<--------------->\033[0m response:%s' % (
                time.time() - start, data, response.text))

            response = json.loads(response.text)
            return response['result']
        except Exception as e:
            if api_debug:
                print('[DEBUG] cost:%.2f request:%s' % (time.time() - start, data))
            raise e
