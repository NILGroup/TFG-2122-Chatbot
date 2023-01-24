from numpy import object0
import spacy
from spacy.matcher import Matcher

import pandas as pd

nlp = spacy.load("es_core_news_sm")
matcher = Matcher(nlp.vocab)

print("Escribe una frase: ")
var = input()
doc = nlp(var)

for token in doc:
    print(token.text, token.pos_, token.dep_, token.head.text, token.is_alpha, token.is_digit, token.is_punct)

pattern = [{"TEXT":"pequeño"}]
p2 = [{"LEMMA":"infancia"}]
p3 = [{"TEXT":"niño"}]
p4 = [{"TEXT":"1 - 13 años"}]
p5 = [{"POS":"NOUN"}]

matcher.add("INFANCIA_PATTERN", [pattern]);
matches = matcher(doc)
print("Total matches found:", len(matches))

for match_id, start, end in matches:
    match_span = doc[start:end]
    print(match_span.text)