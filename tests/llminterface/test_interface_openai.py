import unittest

from llminterface.interface_openai import OpenAIChat


class TestOpenAIChat(unittest.TestCase):
    def test_start_dialog(self):
        chat = OpenAIChat()
        chat.history = [{"content": "Hi", "role": "user"}]
        chat.responses = [{"content": "Hello", "role": "system"}]

        chat.start_dialog()

        self.assertEqual(chat.history, [])
        self.assertEqual(chat.responses, [])

    def test_maybe_make_history_shorter(self):
        chat = OpenAIChat()
        messages = [
            {"content": "This is a message with many tokens. first", "role": "user"},  # 8+7 = 15
            {
                "content": "This is another message with many tokens",
                "role": "system",
            },  # 7+6 = 13. Total: 28
            {"content": "This is a short message. last", "role": "user"},  # 6+5 = 11. 43 total.
        ]

        chat.max_tokens = 34

        shortened_messages = chat.maybe_make_history_shorter(messages)
        assert len(shortened_messages) == 2
        assert shortened_messages[0]["content"] == "This is another message with many tokens"

        # self.assertEqual(shortened_messages, expected_shortened_messages)
