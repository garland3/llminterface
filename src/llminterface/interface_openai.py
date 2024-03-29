# %%
import sys
import traceback
import openai
from llminterface.chatconfig.config import settings

# Set the OpenAI API key
openai.api_key = settings.openaikey


class OpenAIChat:
    def __init__(self, model="gpt-3.5-turbo", system_message_content=None):
        self.model = model
        self.history = []
        self.responses = []
        if system_message_content == None:
            self.system_message = {
                "role": "system",
                "content": (
                    "You are an expert in everything, and have 10 years as a senior developer."
                    "Please kindly help answer these questions."
                ),
            }
        else:
            self.system_message = {
                "role": "system",
                "content": system_message_content,
            }
      
        self.list_of_results = []
        self.field_name = ""
        self.post_process_fn = None
        # self.llm_api_call_fn =
        self.return_value_on_error = ""
        self.llm_answer = ""
        self.user_message = ""
        self.max_tokens = 4000

    def start_dialog(self):
        self.history = []
        self.responses = []

    def maybe_make_history_shorter(self, messages):
        # esitamte the number of tokens, and cut the history if it is too long
        new_messages_reversed = []
        cnt = 0
        for m in messages[::-1]:
            content = m["content"]
            _tokens = len(content.split(" ")) + content.count(" ")
            cnt += _tokens
            if cnt > self.max_tokens:
                break
            new_messages_reversed.append(m)
        messages = new_messages_reversed[::-1]
        # print("The # of tokens is: ", cnt)
        return messages

    def c(self, user_message_txt, print_result=True):
        self.user_message = user_message_txt
        try:
            m = {"role": "user", "content": user_message_txt}
            messages = [self.system_message] + self.history + [m]
            messages = self.maybe_make_history_shorter(messages)
            r = openai.ChatCompletion.create(model=self.model, messages=messages)
            # pprint(r)
            result_txt = r.choices[0].message.content
            self.responses.append(result_txt)
            local_dict = {}
            local_dict["user_message"] = user_message_txt
            local_dict["result"] = result_txt
            self.list_of_results.append(local_dict)
            if self.post_process_fn is not None:
                result_txt = self.post_process_fn(result_txt)
        except Exception as e:
            print("Error in user_input: ", e)
            traceback.print_exc()
            result_txt = self.return_value_on_error
        self.history.append({"role": "user", "content": user_message_txt})
        self.history.append({"role": "assistant", "content": result_txt})
        self.llm_answer = result_txt
        if print_result:
            print(result_txt)
            return None
        return result_txt

    def __call__(self, user_message_txt, print_result=True):
        return self.c(user_message_txt, print_result)


# %%
def main():
    c = OpenAIChat()
    c.start_dialog()

    # use the args from the cmd line as the input
    prompt = " ".join(sys.argv[1:])

    c(prompt)


# %%
