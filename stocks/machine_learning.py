import flair
import re


class SentimentClass:
    def __init__(self):
        self.text_classification_model = flair.models.TextClassifier.load("en-sentiment")

    def get_sentiment(self, text: str):
        sentence_model = flair.data.Sentence(text)
        self.text_classification_model.predict(sentence_model)
        return sentence_model


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
    new_class = SentimentClass()
    new_class.get_sentiment("HELLO, how are you")
