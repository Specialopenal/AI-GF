from langchain_ollama import ChatOllama
from langchain.chains import ConversationChain
from memory import load_memory, save_memory
import re
import json
from pathlib import Path
import warnings


warnings.filterwarnings(
  "ignore",
  message=".*encoder_attention_mask.*will be removed in version.*"
)

with open("config.json", "r") as f:
    config = json.load(f)

chat_model = ChatOllama(**config)

def clean_message(text: str) -> str:
    pattern = r"<think>.*?</think>"
    cleaned = re.sub(pattern, "", text, flags=re.DOTALL).strip()
    return cleaned

def main ():
    memory = load_memory(k=10)

    conversation = ConversationChain(
        llm=chat_model,
        memory=memory,
        verbose=False
        )

    while True:

        user_input = input("User: ")
        print("")

        if user_input == "exit":
            print("End conversation")
            break
        
        raw_response = conversation.predict(input=user_input)
        response = clean_message(raw_response)

        print(f"Bot: {response}\n")

        save_memory(conversation.memory.retriever.vectorstore)


if __name__ == "__main__":
    main()



