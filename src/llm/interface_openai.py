# %%
from collections import OrderedDict
import json
import traceback
import openai
from tqdm import tqdm
from chatconfig.config import settings
# Set the OpenAI API key
openai.api_key = settings.openaikey
from pprint import pprint


class OpenAIChat:
    def __init__(self, model="gpt-3.5-turbo"):
        self.model = model
        self.history = []
        self.responses = []
        self.system_message = {
            "role": "system",
            "content": "You are an expert in everything, and have 10 years as a senior developer. Please kindly help answer these questions.",
        }
        self.list_of_results = []
        self.field_name = ""
        self.post_process_fn = None
        # self.llm_api_call_fn = 
        self.return_value_on_error = ""
        self.llm_answer = ""
        self.user_message = ""

    def start_dialog(self):
        self.history = []
        self.responses = []

    def c(self, user_message_txt, print_result=True):
        self.user_message = user_message_txt
        try:
            m = {"role": "user", "content": user_message_txt}
            messages = [self.system_message] + self.history + [m]
            # print("messages: ", messages)
            # pprint(messages)
            r = openai.ChatCompletion.create(
                model=self.model,
                messages=messages
              
            )
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

# def main():
c = OpenAIChat()
c.start_dialog()
c("Hello")

# %%
c("Given a csv file with 'temp' as a column and some other columns. Use flaml, automl to predict the temp column. Write the code. ")

# %%
c("can you write some fake data to test the code?")
# %%


# class OpenAIChat:
#     def __init__(self, model="gpt-3.5-turbo"):
#         self.model = model
#         self.history = []
#         self.responses = []
#         self.sytem_message = {
#             "role": "system",
#             "content": "You are an expert in everything, and have 10 years as a senior developer. Please kindly help answer these questions.",
#         }
#         self.list_of_results = []
#         self.job_description = "Please take this headline and make a 4 sentence article that is interesting and informative.  The headline is: "
#         self.field_name = ""
#         self.post_proessss_fn = None
#         self.llm_api_call_fn = openai.ChatCompletion.create
#         self.return_value_on_error = ""

#     def complete_chat(self, user_message_txt):
#         try:
#             # print("Complete chat called with: ", user_message_txt)
#             txt = self.job_description + user_message_txt
#             m = {"role": "user", "content": txt}
#             messages = [self.sytem_message, m]
#             r = self.llm_api_call_fn(model=self.model, messages=messages)
#             result_txt = r.choices[0].message.content
#             local_dict = {}
#             # add the usermessage to the dict, job description to the dict, and the result to the dict
#             local_dict["user_message"] = user_message_txt
#             local_dict["job_description"] = self.job_description
#             local_dict["result"] = result_txt
#             self.list_of_results.append(local_dict)
#             open("temp.txt", "w").write(result_txt)
#             print("LLM wrote: ", result_txt)
#             if self.post_proessss_fn is not None:
#                 result_txt = self.post_proessss_fn(result_txt)
#                 print("Post process wrote: ", result_txt)
#         except Exception as e:
#             print("Error in complete_chat: ", e)
#             traceback.print_exc()
#             result_txt = self.return_value_on_error
#         return result_txt
