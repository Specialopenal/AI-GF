import tkinter as tk
from tkinter import scrolledtext
from main import AI_conversation

def send_message():
    msg = entry.get()
    if msg:
        chat_box.config(state=tk.NORMAL)
        chat_box.insert(tk.END, "You: " + msg + "\n")
        chat_box.insert(tk.END, "Bot: " + get_bot_reply(msg) + "\n")
        chat_box.config(state=tk.DISABLED)
        entry.delete(0, tk.END)

def get_bot_reply(message):
    return AI_conversation(message)

root = tk.Tk()
root.title("Chat Room")

chat_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=50, state=tk.DISABLED)
chat_box.pack(padx=10, pady=10)

entry = tk.Entry(root, width=60)
entry.pack(side=tk.LEFT, padx=10)

send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack(side=tk.LEFT)

root.mainloop()
