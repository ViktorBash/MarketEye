from requests_html import HTMLSession
import gc


def webscrape(ticker: str, top_results=False):
    session = HTMLSession()
    url = f"https://twitter.com/search?q=%24{ticker}%20lang%3Aen&src=typed_query"
    if not top_results:
        url += "&f=live"

    r = session.get(url)
    r.html.render(sleep=1, keep_page=True, scrolldown=1)
    session.close()

    result = []
    tweets = r.html.find("article")  # A tweet object currently is the whole tweet textbox, including username/handle

    # Loop through each tweet and extract ONLY the text that is the actual tweet, not the handles or anything else
    for tweet in tweets:
        textbox = tweet.find("div")
        for div in textbox:
            if "lang" in div.attrs:  # The <div> with the "lang" class is the actual tweet, other <div> elements are
                # irrelevant
                result.append(div.text)
    # Returns a list of <str> tweets
    return result


if __name__ == "__main__":
    test = webscrape("MMM")
    print(test)

