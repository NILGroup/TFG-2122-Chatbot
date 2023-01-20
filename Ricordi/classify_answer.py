import spacy
from spacy.matcher import Matcher
from spacy.util import minibatch, compounding
from spacy.training.example import Example

import pandas as pd
import funciones

nlp = spacy.blank('es')

memories=pd.read_csv("recuerdos.csv")

memories = memories[['Recuerdo','Etapa']].dropna() 


textcat = nlp.add_pipe('textcat')

textcat.add_label("INFANCIA")
#textcat.add_label("ADOLESCENCIA")
textcat.add_label("JUVENTUD")
textcat.add_label("ETAPA ADULTA")
textcat.add_label("VEJEZ")
#textcat.add_label("INDETERMINADO")


memories['tuples'] = memories.apply(lambda row: (row['Recuerdo'],row['Etapa']), axis=1)
train =memories['tuples'].tolist()
print(train[:10])



(train_texts, train_cats), (dev_texts, dev_cats) = funciones.load_data_phases(train, limit=23486)


train_data = list(zip(train_texts,[{'cats': cats} for cats in train_cats]))
print(train_data[:10])


other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'textcat']
with nlp.disable_pipes(*other_pipes): 
    optimizer = nlp.begin_training()

    print("Training the model...")
    #print('{:^5}\t{:^5}\t{:^5}\t{:^5}'.format('LOSS', 'P', 'R', 'F'))
    print('{:^5}\t'.format('LOSS'))

    for i in range(8):
        losses = {}
        batches = minibatch(train_data, size=compounding(4., 32., 1.001))
        for batch in batches:
            texts, annotations = zip(*batch)
            example = []
            for i in range(len(texts)):
                doc = nlp.make_doc(texts[i])
                example.append(Example.from_dict(doc, annotations[i]))

            nlp.update(example, sgd=optimizer, drop=0.2, losses=losses)


        with nlp.use_params(optimizer.averages):
            scores = funciones.evaluate(nlp.tokenizer, textcat, dev_texts, dev_cats)

        '''print('{0:.3f}\t{1:.3f}\t{2:.3f}\t{3:.3f}'.format(losses['textcat'], scores['textcat_p'], scores['textcat_r'], scores['textcat_f']))'''
        print('{0:.3f}\t'.format(losses['textcat']))

def clasificar_etapas(text):
    categories = []
    
    doc = nlp(text)
    print('{}: {}'.format(text, doc.cats))
    
    '''if doc.cats['INFANCIA'] > doc.cats['ADOLESCENCIA'] and doc.cats['INFANCIA'] > doc.cats['JUVENTUD'] and doc.cats['INFANCIA'] > doc.cats['ETAPA ADULTA'] and doc.cats['INFANCIA'] > doc.cats['VEJEZ'] and doc.cats['INFANCIA'] > doc.cats['INDETERMINADO']:
        categories.append('infancia')
    elif doc.cats['ADOLESCENCIA'] > doc.cats['INFANCIA'] and doc.cats['ADOLESCENCIA'] > doc.cats['JUVENTUD'] and doc.cats['ADOLESCENCIA'] > doc.cats['ETAPA ADULTA'] and doc.cats['ADOLESCENCIA'] > doc.cats['VEJEZ'] and doc.cats['ADOLESCENCIA'] > doc.cats['INDETERMINADO']:
        categories.append('adolescencia')
    elif doc.cats['JUVENTUD'] > doc.cats['INFANCIA'] and doc.cats['JUVENTUD'] > doc.cats['ETAPA ADULTA'] and doc.cats['JUVENTUD'] > doc.cats['ADOLESCENCIA'] and doc.cats['JUVENTUD'] > doc.cats['VEJEZ'] and doc.cats['JUVENTUD'] > doc.cats['INDETERMINADO']:
        categories.append('juventud')
    elif doc.cats['ETAPA ADULTA'] > doc.cats['INFANCIA'] and doc.cats['ETAPA ADULTA'] > doc.cats['JUVENTUD'] and doc.cats['ETAPA ADULTA'] > doc.cats['ADOLESCENCIA'] and doc.cats['ETAPA ADULTA'] > doc.cats['VEJEZ'] and doc.cats['ETAPA ADULTA'] > doc.cats['INDETERMINADO']:
        categories.append('etapa adulta')
    elif doc.cats['VEJEZ'] > doc.cats['INFANCIA'] and doc.cats['VEJEZ'] > doc.cats['JUVENTUD'] and doc.cats['VEJEZ'] > doc.cats['ADOLESCENCIA'] and doc.cats['VEJEZ'] > doc.cats['ETAPA ADULTA'] and doc.cats['VEJEZ'] > doc.cats['INDETERMINADO']:
        categories.append('vejez')
    else:
        categories.append('indeterminado')'''

    if doc.cats['INFANCIA'] > doc.cats['JUVENTUD'] and doc.cats['INFANCIA'] > doc.cats['ETAPA ADULTA'] and doc.cats['INFANCIA'] > doc.cats['VEJEZ']:
        categories.append('infancia')
    elif doc.cats['JUVENTUD'] > doc.cats['INFANCIA'] and doc.cats['JUVENTUD'] > doc.cats['ETAPA ADULTA'] and doc.cats['JUVENTUD'] > doc.cats['VEJEZ']:
        categories.append('juventud')
    elif doc.cats['ETAPA ADULTA'] > doc.cats['INFANCIA'] and doc.cats['ETAPA ADULTA'] > doc.cats['JUVENTUD'] and doc.cats['ETAPA ADULTA'] > doc.cats['VEJEZ']:
        categories.append('etapa adulta')
    elif doc.cats['VEJEZ'] > doc.cats['INFANCIA'] and doc.cats['VEJEZ'] > doc.cats['JUVENTUD'] and doc.cats['VEJEZ'] > doc.cats['ETAPA ADULTA']:
        categories.append('vejez')



    print(categories)

    return categories

#clasificar_etapas("Cuando era pequeño me encantaba la pizza")

'''clasificar_etapas("Mi mejor recuerdo es el del nacimiento de mi hijo")
clasificar_etapas("Me dolió muchísimo cuando me rompí una pierna a los 22 años")
clasificar_etapas("Mi hermano y yo nos pasabamos las tardes haciendo puzzles")
clasificar_etapas("Durante la infancia estuvimos viviendo en Moratalaz")
clasificar_etapas("Mi pareja sufrió depresión después del parto")
clasificar_etapas("Mi tía siempre se dedicó a la pintura")
clasificar_etapas("Cuando estudiaba primero BUP teníamos tres gatos")'''

