# %%
from llminterface.llm_wrapper import ChatSession

cs = ChatSession()
# %%
cs.start_dialog()
# %%
cs("Hello")
# %%
cd2 = ChatSession.load_session("test1")
# %%
cd2.show_history()
# %%
cd2("what is the capital of france?")
# %%
cs.name
# %%
