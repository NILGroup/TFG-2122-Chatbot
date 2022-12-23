from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

# Create a new chat bot named Ricorda
chatbot = ChatBot('Ricorda')

trainer = ListTrainer(chatbot)

trainer.train([
    "Buenos días, ¿cómo te llamas?",
    "Me llamo Pablo",
    "¿Cómo te encuentras hoy?",
    "Bien",
    "Eso es muy buena señal."
])

trainer.train(
    "chatterbot.corpus.spanish"
)

print("¿Cómo te encuentras hoy?")
var = input()

response = chatbot.get_response(var)

print(response)