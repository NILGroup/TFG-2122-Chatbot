import spacy
from spacy.matcher import Matcher
from spacy.util import minibatch, compounding
from spacy.training.example import Example

import pandas as pd
import funciones

nlp = spacy.blank('es')

reviews=pd.read_csv("IMDB_dataset.csv", error_bad_lines=False)
#on_bad_lines='skip'

reviews = reviews[['review_es','sentimiento']].dropna()
reviews.head(10)


textcat = nlp.add_pipe('textcat')
print(nlp.pipe_names)

textcat.add_label("POSITIVO")
textcat.add_label("NEGATIVO")

reviews['tuples'] = reviews.apply(lambda row: (row['review_es'],row['sentimiento']), axis=1)
train =reviews['tuples'].tolist()
print(train[:10])


# Calling the load_data() function
(train_texts, train_cats), (dev_texts, dev_cats) = funciones.load_data(train, limit=23486)

# Processing the final format of training data
train_data = list(zip(train_texts,[{'cats': cats} for cats in train_cats]))
print(train_data[:10])



# Disabling other components
other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'textcat']
with nlp.disable_pipes(*other_pipes): # only train textcat
    optimizer = nlp.begin_training()

    print("Training the model...")
    #print('{:^5}\t{:^5}\t{:^5}\t{:^5}'.format('LOSS', 'P', 'R', 'F'))
    print('{:^5}\t'.format('LOSS'))

    # Performing training
    for i in range(2):
        losses = {}
        batches = minibatch(train_data, size=compounding(4., 32., 1.001))
        for batch in batches:
            texts, annotations = zip(*batch)
            example = []
            # Update the model with iterating each text
            for i in range(len(texts)):
                doc = nlp.make_doc(texts[i])
                example.append(Example.from_dict(doc, annotations[i]))

            #losses = textcat.rehearse(example, sgd=optimizer)
            nlp.update(example, sgd=optimizer, drop=0.2, losses=losses)

        # Calling the evaluate() function and printing the scores

        with nlp.use_params(optimizer.averages):
            scores = funciones.evaluate(nlp.tokenizer, textcat, dev_texts, dev_cats)
        '''print('{0:.3f}\t{1:.3f}\t{2:.3f}\t{3:.3f}'
        .format(losses['textcat'], scores['textcat_p'],
        scores['textcat_r'], scores['textcat_f']))'''
        print('{0:.3f}\t'.format(losses['textcat']))

test_text="Mi abuela se murio en 1998"
test_text2="De pequeña pasaba mucho tiempo con mis abuelos, íbamos al parque y me me encantaba jugar con mi hermano a ser piratas"
doc = nlp(test_text)
doc2 = nlp(test_text2)
print('{}: {}'.format(test_text, doc.cats))
print('{}: {}'.format(test_text2, doc2.cats))

def clasificar_emocion(text):
    categories = []
    
    doc = nlp(text)
    print('{}: {}'.format(text, doc.cats))

    '''if doc.cats['NEGATIVO'] > doc.cats['POSITIVO'] and doc.cats['NEGATIVO'] > doc.cats['NEUTRO']:
        categories.append('negativo')
    elif doc.cats['POSITIVO'] > doc.cats['NEGATIVO'] and doc.cats['POSITIVO'] > doc.cats['NEUTRO']:
        categories.append('positivo')
    else:
        categories.append('neutro')'''

    if doc.cats['NEGATIVO'] > doc.cats['POSITIVO']:
        categories.append('negativo')
    else:
        categories.append('positivo')
    
    print(categories)

    return categories


clasificar_emocion("Mi abuela se murio en 1998")
clasificar_emocion("Mi mejor recuerdo es el del nacimiento de mi hijo")
clasificar_emocion("Tengo 23 años")
clasificar_emocion("Me dolió muchísimo cuando me rompí una pierna")
clasificar_emocion("Mi hermano y yo nos pasabamos las tardes haciendo puzzles")
clasificar_emocion("Durante la infancia estuvimos viviendo en Moratalaz")
clasificar_emocion("Mi pareja sufrió depresión después del parto")

while True:
    print(f"Introduzca el texto: ")
    texto = input()
    print(f"El texto es: {texto}")
    clasificar_emocion(texto)