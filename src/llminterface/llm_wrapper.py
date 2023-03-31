# %%
import os
import json
import datetime
import sys
from typing import List, Dict

from llminterface.interface_openai import OpenAIChat


class ChatSession:
    def __init__(self, name: str, model: str = "gpt-3.5-turbo"):
        self.name = name
        self.model = model
        self.chat = OpenAIChat(model=self.model)
        self.history = []
        self.folder = os.path.expanduser("~/.llminterface")
        self.filename = os.path.join(self.folder, f"{self.name}.json")

    def start_dialog(self):
        self.chat.start_dialog()
        self.history = []
        
    def s(self):
        self.start_dialog()

    def send_message(self, message: str, print_result=False):
        if len(self.history)>0:
            self.chat.history = self.history
        self.chat.c(message, print_result=print_result)
        result_txt = self.chat.llm_answer
        # print(result_txt)
        self.history.append(
            {
                # "timestamp": str(datetime.datetime.now()),
                "role": "user",
                "content": message,
            }
        )
        self.history.append(
            {
                # "timestamp": str(datetime.datetime.now()),
                "role": "assistant",
                "content": result_txt,
            }
        )
        # print("new history", self.history)
        self.save_history()
        return result_txt
    
    def __call__(self, message: str, print_result=True):
        return self.send_message(message, print_result)

    def load_history(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                self.history = json.load(f)
        else:
            print(f"No history found for '{self.name}' session.")

    def save_history(self):
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)
        with open(self.filename, "w") as f:
            json.dump(self.history, f)

    def show_history(self):
        for item in self.history:
            # print(f"{item['timestamp']} - {item['role']}: {item['content']}")
            print(f"{item['role']}: {item['content']}")


    def clear_history(self):
        self.history = []
        self.save_history()
        print(f"History cleared for '{self.name}' session.")

    def delete_history(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)
            print(f"History deleted for '{self.name}' session.")
        else:
            print(f"No history found for '{self.name}' session.")

    def list_sessions(cls) -> List[str]:
        return [
            os.path.splitext(f)[0]
            for f in os.listdir(cls.folder)
            if os.path.isfile(os.path.join(cls.folder, f))
        ]

    @classmethod
    def load_session(cls, name: str) -> "ChatSession":
        session = cls(name)
        session.load_history()
        return session

    def __str__(self) -> str:
        return f"ChatSession(name='{self.name}', model='{self.model}')"
    
# create default session if it doesn't exist
def make_default_session():
    # test if the file exists
    default_session_filename = os.path.join(os.path.expanduser("~/.llminterface"), "default.json")
    if not os.path.exists(default_session_filename):
        print("Creating default session")
    
        session = ChatSession("default")
        session.start_dialog()
    else:
        # print("Default session already exists")
        session = ChatSession.load_session("default")
    return session
        

def main():
    c = make_default_session()
    # use the args from the cmd line as the input
    prompt = " ".join(sys.argv[1:])
    c(prompt)
    
# # %%
# cs = ChatSession("test1")
# # %%
# cs.start_dialog()
# # %%
# cs("Hello")
# # %%
# cd2 = ChatSession.load_session("test1")
# # %%
# cd2.show_history()
# # %%
# cd2("what is the capital of france?")
# %%
