
import os
from transformers import AutoTokenizer


class TokenCounter:

    def __init__(self, model_id: str):
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_id,
            trust_remote_code=False
        )

    def count_text(self, text: str) -> int:
        tokens = self.tokenizer.encode(
            text,
            add_special_tokens=False
        )

        return len(tokens)

    def count_messages(self, messages: list[dict]) -> int:

        token_ids = self.tokenizer.apply_chat_template(
            messages,
            tokenize=True,
            add_generation_prompt=True
        )

        return len(token_ids)


if __name__ == "__main__":
    model_id = os.environ["LLM_MODEL"]

    counter = TokenCounter(model_id)

    text = "I am learning AI engineering."

    print("Text:", text)
    print("Token count:", counter.count_text(text))

    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": "Explain context windows."
        }
    ]

    print(
        "Conversation tokens:",
        counter.count_messages(messages)
    )
