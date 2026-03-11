import os
from core.loader import load_list, load_commands
from core.resolver import Resolver
from core.memory import Memory
from core.command_engine import CommandEngine
from core.classifier import IntentClassifier
from core.router import route

os.chdir(os.path.dirname(os.path.abspath(__file__)))

items = load_list("data/items.txt")
commands = load_commands("data/commands.txt")

resolver = Resolver(items)
engine = CommandEngine(commands)
classifier = IntentClassifier()
memory = Memory()

print("Minecraft AI Assistant ready!")
print("Type 'exit' to quit.\n")

while True:
    msg = input("User: ")
    if msg.lower() == "exit":
        break
    result = route(
        msg,
        classifier,
        engine,
        resolver,
        memory
    )
    print(f"{result['type'].upper()}: {result['result']}\n")
