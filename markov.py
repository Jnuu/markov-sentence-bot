import re
import markovify
from janome.tokenizer import Tokenizer

def formatter(messages: list[str]) -> list[str]:
    formatted = []
    for message in messages:
        result = re.sub(
            "https?://[\w!\?/\+\-_~=;\.,\*&@#\$%\(\)'\[\]]+", "", message)
        result = re.sub("@[\w]+ ", "", result)
        result = re.sub("#[\w]+ ", "", result)
        result = re.sub(" ", "\n", result)
        result = re.sub("\n\n", "\n", result)
        result = re.sub("\n\n", "\n", result)
        result = result.replace('\u3000', '')
        formatted.append(result)
    
    return formatted

def make_model(messages: list[str]):
    messages = formatter(messages)
    t = Tokenizer()
    word_list = []

    for message in messages:
        words = t.tokenize(message, wakati = True)

        for word in words:
            word_list.append(word)

        word_list.append("\n")

    sentence_list = ' '.join(word_list)
    text_model = markovify.NewlineText(sentence_list, state_size=2)

    return text_model

def make_sentence(model) -> str:
    sentence = None
    sentences = []

    while sentence == None:
        sentence = model.make_sentence()
    
    sentence = sentence.replace(' ', '')

    return sentence