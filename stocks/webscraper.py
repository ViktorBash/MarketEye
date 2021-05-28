import requests
import os
import json


class TwitterAPI:
    def __init__(self, ticker: str, token: str, max_tweets=5):
        self.text_list = []
        self.ticker = ticker
        self.token = token
        self.headers = {"Authorization": f"Bearer {self.token}"}
        rules = self.get_rules()
        self.delete_all_rules(rules)
        self.rules_set = self.set_rules()
        self.max_tweets = max_tweets
        self.counter = 0

    def start_scraping(self):
        self.get_stream()

    def get_rules(self):
        response = requests.get(
            "https://api.twitter.com/2/tweets/search/stream/rules", headers=self.headers
        )
        if response.status_code != 200:
            raise Exception(
                "Cannot get rules (HTTP {}): {}".format(response.status_code, response.text)
            )
        # print(json.dumps(response.json()))
        return response.json()

    def delete_all_rules(self, rules):
        if rules is None or "data" not in rules:
            return None

        ids = list(map(lambda rule: rule["id"], rules["data"]))
        payload = {"delete": {"ids": ids}}
        response = requests.post(
            "https://api.twitter.com/2/tweets/search/stream/rules",
            headers=self.headers,
            json=payload
        )
        if response.status_code != 200:
            raise Exception(
                "Cannot delete rules (HTTP {}): {}".format(
                    response.status_code, response.text
                )
            )
        # print(json.dumps(response.json()))

    def set_rules(self):
        # You can adjust the rules if needed
        sample_rules = [
            {"value": self.ticker, "tag": ""},
        ]
        payload = {"add": sample_rules}
        response = requests.post(
            "https://api.twitter.com/2/tweets/search/stream/rules",
            headers=self.headers,
            json=payload,
        )
        if response.status_code != 201:
            raise Exception(
                "Cannot add rules (HTTP {}): {}".format(response.status_code, response.text)
            )
        # print(json.dumps(response.json()))

    def get_stream(self):
        response = requests.get(
            "https://api.twitter.com/2/tweets/search/stream", headers=self.headers, stream=True,
        )
        # print(response.status_code)
        if response.status_code != 200:
            raise Exception(
                "Cannot get stream (HTTP {}): {}".format(
                    response.status_code, response.text
                )
            )

        for response_line in response.iter_lines():
            if response_line:
                self.counter += 1
                dict_response = json.loads(response_line)
                data = dict_response['data']
                result = data['text']
                self.text_list.append(result)

                # We have reached the max amount of tweets, so we quit
                if self.counter >= self.max_tweets:
                    break


# Testing purposes
if __name__ == "__main__":
    # Example call
    api_instance = TwitterAPI("TSLA", os.environ.get("BEARER_TOKEN"), 3)
    api_instance.start_scraping()
    print(api_instance.text_list)
