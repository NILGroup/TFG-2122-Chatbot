import spacy
from spacy.matcher import Matcher
from spacy.util import minibatch, compounding
from spacy.training.example import Example

import pandas as pd
import funciones

nlp = spacy.blank('es')

reviews=pd.read_csv("recuerdos.csv")

reviews = reviews[['Recuerdo','IND']].dropna()
reviews.head(10)


textcat = nlp.add_pipe('textcat')
print(nlp.pipe_names)

textcat.add_label("POSITIVO")
textcat.add_label("NEGATIVO")

reviews['tuples'] = reviews.apply(lambda row: (row['Recuerdo'],row['IND']), axis=1)
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
    for i in range(8):
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