import flair
import re


def get_sentiment(text: str):
    """Given a cleaned string, sentiment will be returned in the form of a Sentence class"""
    sentiment_model = flair.models.TextClassifier.load("en-sentiment")
    sentence = flair.data.Sentence(text)
    sentiment_model.predict(sentence)
    return sentence


def clean_string(text: str):
    whitespace = re.compile(r"\s+")
    web_address = re.compile(r"(?i)http(s):\/\/[a-z0-9.~_\-\/]+")
    user = re.compile(r"(?i)@[a-z0-9_]+")

    text = whitespace.sub(" ", text)
    text = web_address.sub(" ", text)
    text = user.sub(" ", text)
    return text


if __name__ == "__main__":
    pass
    # sentiment_model = get_sentiment("Hello, how are you?")
    # sentiment_model = sentiment_model.labels[0].score
    # print(type(sentiment_model))
    # print(sentiment_model)
