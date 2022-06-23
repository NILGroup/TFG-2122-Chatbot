from itertools import groupby
from collections import Counter
import spacy

nlp = spacy.load('es_core_news_sm')

texto = "En mi casa, una cena típica consiste en carne, generalmente pollo o cerdo, verduras, pan y ensalada"
texto2 = "Mi madre también cocina pasta a menudo. En invierno, se usa el horno para cocinar, pero en verano y parte del otoño, solo usamos la parrilla. En las vacaciones que celebramos con toda la familia, alguien cocina unos pavos (tengo una familia muy grande) y otros cocinan los otros platos pequeños. Cuando es el cumpleaños de alguien de la familia, mi abuela y yo horneamos el pastel y su tipo depende del que prefiera la persona. Mi abuela usa una mezcla de pastel del supermercado, pero todos los pasteles que horneo yo son caseros. Uso harina, azúcar, mantequilla, huevos y chocolate si la persona quiere. En los fines de semana, a veces mi madre, mi hermano mayor y yo cocinamos juntos unas pizzas para toda la familia, pero solamente hacemos eso cuando es domingo y toda la familia está en casa. La pizza no es toda casera porque usamos masa y salsa compradas, pero nuestro método de hacerla es original y cocinamos más que cuando pedimos pizza de una pizzería. Soy de San Luis, y en esta región, la pizza de corteza delgada, los ravioles fritos, y la torta de mantequilla viscosa son tradicionales. La pizza consiste de masa delgada, salsa roja, y un queso que se llama provel y solamente hay en San Luis. En mi familia, el meatloaf, la lasaña, y arroz con pollo son unas cenas tradicionales porque a mi padre le gustan mucho. Recuerdo que a veces no me apetecían nada, especialmente cuando tenía que comer verduras con ellas, y mi madre insistía en que las comiese, si no, no me dejaba irme. Cuando era niña, odiaba las verduras, especialmente el brócoli, y las ciruelas pasas. Ahora me encantan las verduras y las como todos los días. Pero todavía odio ciruelas pasas porque asocio malos recuerdos con ellas. Cuando era niña me encantaba el helado, ¡y todavía me encanta hoy!"


def read(text):
    rawText = text.replace('\n', '')
    rawText = rawText.replace('\t', '')
    rawText = rawText.replace(',', '')
    texts = rawText.lower()

    return nlp(texts)


def synthesis(doc):

    relevant_doc = [token for token in doc if not token.is_stop and
                    not token.is_punct or token.text == '.']

    only_words = [list(group) for k, group in groupby(relevant_doc, lambda x: x.text == ".") if not k]
    
    print(only_words)

    for sentence in only_words:
        for token in sentence:
            if len(token) == 1:
                sentence.remove(token)

    return only_words


def lemmatize(only_words):
    only_lemmas = []

    for sentence in only_words:
        new_sentence = [token.lemma_ for token in sentence]
        only_lemmas.append(new_sentence)

    return only_lemmas


def categorize(only_words):
    verbs = []
    nouns = []
    adjectives = []

    for sentence in only_words:
        verbs += [token.lemma_ for token in sentence if token.pos_ == "VERB"]
        nouns += [token.lemma_ for token in sentence if token.pos_ == "NOUN"]
        adjectives += [token.lemma_ for token in sentence if token.pos_ == "ADJ"]
    verbCount = Counter(word for word in verbs)
    nounCount = Counter(word for word in nouns)
    adjectiveCount = Counter(word for word in adjectives)

    most_common_verbs = [t[0] for t in verbCount.most_common(30)]
    most_common_nouns = [t[0] for t in nounCount.most_common(30)]
    most_common_adjectives = [t[0] for t in adjectiveCount.most_common(30)]

    most_common_words = most_common_verbs + most_common_nouns + most_common_adjectives

    return [most_common_words, most_common_verbs, most_common_nouns, most_common_adjectives]


def get_most_common_words(only_words):
    return categorize(only_words)[0]


def get_most_common_verbs(only_words):
    return categorize(only_words)[1]


def get_most_common_nouns(only_words):
    return categorize(only_words)[2]


def get_most_common_adjectives(only_words):
    return categorize(only_words)[3]


def commons_in_sentence(sentence, only_words):
    return [word for word in sentence if word in get_most_common_words(only_words)]


def commons_in_text(only_lemmas, only_words):
    most_common_in_texts = []


    for sentence in only_lemmas:
        new_sentence = commons_in_sentence(sentence, only_words)
        most_common_in_texts.append(new_sentence)

    return most_common_in_texts


def get_relations(most_common_in_texts, only_words):
    relations = {}

    mcv = get_most_common_verbs(only_words)
    mcn = get_most_common_nouns(only_words)
    mca = get_most_common_adjectives(only_words)


    for sentence in most_common_in_texts:
        for word in sentence:
            if word not in relations:
                relations[word] = []
            for related_word in sentence:
                if related_word != word and related_word not in (x[0] for x in relations[word]):
                    if related_word in mcv:
                        relations[word].append([related_word, 'VER'])
                    elif related_word in mcn:
                        relations[word].append([related_word, 'SUS'])
                    elif related_word in mca:
                        relations[word].append([related_word, 'ADJ'])

    return relations

def analyze(text):
    doc = read(text)
    only_words = synthesis(doc)
    common_lemmas = get_most_common_words(only_words)
    return common_lemmas


def compare(lemmas_answer, lemmas_question):
    print(set(lemmas_answer))
    print(set(lemmas_question))
    common = set(lemmas_answer) & set(lemmas_question)
    return len(common)



'''docs = read(texto)
print("DOOOOOOOCSSSSSSSSSSSSSSSS")
print(docs)
only_words = synthesis(docs)
print("WOOOOOOOORDSSSSSSSSSSSSSSS")
print(only_words)
only_lemmas = lemmatize(only_words)
print("LEMMMAAAAAAAAAAAAAAAAAAAAAAAAAAASSSSSSSSSS")
print(only_lemmas)
[most_common_words, most_common_verbs, most_common_nouns, most_common_adjectives] = categorize(only_words)
print("common WORDSSSSSSSSS")
print(most_common_words)
print("common VERBSSSSSSSSSSS")
print(most_common_verbs)
print("common NOOOOUNSSSSSSSSSSS")
print(most_common_nouns)
print("common adJJJJJJJJJJJJJJJ")
print(most_common_adjectives)

most_common_in_texts = commons_in_text(only_lemmas, only_words)
print("COMMMOOOONS TEXTSSSSSSSSSSSS")
print(most_common_in_texts)
relations = get_relations(most_common_in_texts, only_words)
print("RELAAAAAAAAAATIOOOOONS")
print(relations)'''