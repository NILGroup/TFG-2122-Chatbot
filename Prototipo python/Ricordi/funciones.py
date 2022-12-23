import random

def load_data(train, limit=0, split=0.8):
    train_data=train
    # Shuffle the data
    random.shuffle(train_data)
    texts, labels = zip(*train_data)
    # get the categories for each review
    cats = [{"POSITIVO": (False, True)[y == 1], "NEGATIVO": (False, True)[y == 0], "NEUTRO": (False, True)[y == 2]} for y in labels]

    # Splitting the training and evaluation data
    split = int(len(train_data) * split)
    return (texts[:split], cats[:split]), (texts[split:], cats[split:])

def load_data_phases(train, limit=0, split=0.8):
    train_data=train
    # Shuffle the data
    random.shuffle(train_data)
    texts, labels = zip(*train_data)
    # get the categories for each review
    cats = [{"INFANCIA": (False, True)[y == 0], "ADOLESCENCIA": (False, True)[y == 1], "JUVENTUD": (False, True)[y == 2], "ETAPA ADULTA": (False, True)[y == 3], "VEJEZ": (False, True)[y == 4], "INDETERMINADO": (False, True)[y == 5]} for y in labels]

    # Splitting the training and evaluation data
    split = int(len(train_data) * split)
    return (texts[:split], cats[:split]), (texts[split:], cats[split:])

def evaluate(tokenizer, textcat, texts, cats):
    docs = (tokenizer(text) for text in texts)
    tp = 0.0 # True positives
    fp = 1e-8 # False positives
    fn = 1e-8 # False negatives
    tn = 0.0 # True negatives
    for i, doc in enumerate(textcat.pipe(docs)):
        gold = cats[i]
    for label, score in doc.cats.items():
        if label not in gold:
            continue
        if label == "NEGATIVO":
            continue
        if score >= 0.5 and gold[label] >= 0.5:
            tp += 1.0
        elif score >= 0.5 and gold[label] < 0.5:
            fp += 1.0
        elif score < 0.5 and gold[label] < 0.5:
            tn += 1
        elif score < 0.5 and gold[label] >= 0.5:
            fn += 1
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    if (precision + recall) == 0:
        f_score = 0.0
    else:
        f_score = 2 * (precision * recall) / (precision + recall)
    return {"textcat_p": precision, "textcat_r": recall, "textcat_f": f_score}