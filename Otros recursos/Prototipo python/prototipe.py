import spacy
from spacy.matcher import Matcher
from spacy.util import minibatch, compounding
from spacy.training.example import Example

import pandas as pd
import functions

#nlp = spacy.load("en_core_web_sm")
nlp = spacy.blank('en')

reviews=pd.read_csv("https://raw.githubusercontent.com/hanzhang0420/Women-Clothing-E-commerce/master/Womens%20Clothing%20E-Commerce%20Reviews.csv")

reviews = reviews[['Review Text','Recommended IND']].dropna()
reviews.head(10)


textcat = nlp.add_pipe('textcat')
nlp.pipe_names

textcat.add_label("POSITIVE")
textcat.add_label("NEGATIVE")

reviews['tuples'] = reviews.apply(lambda row: (row['Review Text'],row['Recommended IND']), axis=1)
train =reviews['tuples'].tolist()
print(train[:10])


# Calling the load_data() function
(train_texts, train_cats), (dev_texts, dev_cats) = functions.load_data(train, limit=23486)

# Processing the final format of training data
train_data = list(zip(train_texts,[{'cats': cats} for cats in train_cats]))
print(train_data[:10])



# Disabling other components
other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'textcat']
with nlp.disable_pipes(*other_pipes): # only train textcat
    #optimizer = nlp.create_optimizer()
    optimizer = nlp.begin_training()

    print("Training the model...")
    print('{:^5}\t{:^5}\t{:^5}\t{:^5}'.format('LOSS', 'P', 'R', 'F'))


    #optimizer = nlp.resume_training()


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
        #with textcat.model.use_params(optimizer.averages):
        with nlp.use_params(optimizer.averages):
            scores = functions.evaluate(nlp.tokenizer, textcat, dev_texts, dev_cats)
        print('{0:.3f}\t{1:.3f}\t{2:.3f}\t{3:.3f}'
        .format(losses['textcat'], scores['textcat_p'],
        scores['textcat_r'], scores['textcat_f']))

test_text="I hate this dress"
doc = nlp(test_text)
print(doc.cats)

print(nlp("My grandmother died in 1998").cats)
print(nlp("My best memory is from my child's birth").cats)
print(nlp("I am 23 years old").cats)
print(nlp("It hurt very bad when I fractured my leg").cats)
print(nlp("My brother and I spent our evenings making puzzles").cats)
print(nlp("During my childhood we lived in London").cats)
print(nlp("My girlfrind suffered depression after giving birth").cats)