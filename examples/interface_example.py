# %%
from llminterface.interface_openai import OpenAIChat
# def main():
c = OpenAIChat()
c.start_dialog()
c("Hello")

# %%
c("Given a csv file with 'temp' as a column and some other columns. Use flaml, automl to predict the temp column. Write the code. ")

# %%
c("can you write some fake data to test the code?")

# %%