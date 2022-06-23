import text_analysis
import mongobd

def choose_question(answer):
    questions = mongobd.every_unasked_question()
    lemmas_answer = text_analysis.analyze(answer)
    print(lemmas_answer)

    if questions:
        best = 0
        best_question = questions[0]
        for question in questions:
            print(question)
            print(best)
            print(best_question)
            lemmas_question = text_analysis.analyze(question)
            length = text_analysis.compare(lemmas_answer, lemmas_question)
            print("-----------------------------------------------")
            if length > best:
                best = length
                best_question = question

        return best_question
    else:
        return None
