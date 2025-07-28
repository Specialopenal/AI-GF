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
    text = text.replace("<think>", "")
    text = text.replace("</think>", "")
    text = text.replace("\n", "")
    return text

def AI_conversation (user_input):
    memory = load_memory(k=10)

    conversation = ConversationChain(
    llm=chat_model,
    memory=memory,
    verbose=False
    )

    raw_response = conversation.predict(input=user_input)
    response = clean_message(raw_response)

    save_memory(conversation.memory.retriever.vectorstore)

    return response




