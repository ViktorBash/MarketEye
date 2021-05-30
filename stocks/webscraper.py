from requests_html import HTMLSession


def webscrape(ticker: str, amount: int):
    session = HTMLSession()
    url = f"https://twitter.com/search?q={ticker.upper()}&src=typed_query&f=live"
    r = session.get(url)
    r.html.render(sleep=1, keep_page=True, scrolldown=1)

    result = []
    tweets = r.html.find("article")
    for tweet in tweets:
        result.append(tweet.text)

    # Returns a list of <str> tweets
    return result


if __name__ == "__main__":
    result = webscrape("abbv", 1)
    print(result)
    print(len(result))

