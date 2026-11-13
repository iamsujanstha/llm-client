
class Conversation:

    def __init__(
        self,
        client,
        context_manager,
        max_output_tokens=512,
        system_prompt="You are a helpful assistant."
    ):
        self.client = client
        self.context_manager = context_manager
        self.max_output_tokens = max_output_tokens

        self.system_message = {
            "role": "system",
            "content": system_prompt,
        }

        self.messages = [self.system_message.copy()]

    def send(self, user_input: str) -> str:

        if not user_input.strip():
            raise ValueError("Message cannot be empty")

        user_message = {
            "role": "user",
            "content": user_input,
        }

        request_messages = [
            *self.messages,
            user_message,
        ]

        # Fit messages within the available input budget.
        request_messages = self.context_manager.fit(
            request_messages
        )

        answer = self.client.chat(
            request_messages,
            max_tokens=self.max_output_tokens,
        )

        # Retain full application history.
        self.messages.extend([
            user_message,
            {
                "role": "assistant",
                "content": answer,
            },
        ])

        return answer

    def reset(self):
        self.messages = [self.system_message.copy()]
