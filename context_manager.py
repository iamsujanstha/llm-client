
from typing import Any

from token_counter import TokenCounter


class ContextManager:

    def __init__(
        self,
        token_counter: TokenCounter,
        input_budget: int,
    ):
        if input_budget <= 0:
            raise ValueError("Input budget must be positive")

        self.token_counter = token_counter
        self.input_budget = input_budget

    def fit(
        self,
        messages: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:

        system_messages = [
            message.copy()
            for message in messages
            if message["role"] == "system"
        ]

        conversation = [
            message.copy()
            for message in messages
            if message["role"] != "system"
        ]

        removed_turns = 0

        while True:

            candidate = system_messages + conversation

            token_count = self.token_counter.count_messages(
                candidate
            )

            if token_count <= self.input_budget:
                print(
                    f"[Context] {token_count}/"
                    f"{self.input_budget} tokens"
                )

                print(
                    f"[Context] Removed {removed_turns} old turns"
                )

                return candidate

            # Remove only a complete user-assistant exchange.
            if (
                len(conversation) >= 2
                and conversation[0]["role"] == "user"
                and conversation[1]["role"] == "assistant"
            ):
                conversation = conversation[2:]
                removed_turns += 1

            else:
                raise ValueError(
                    "Cannot fit request into context budget. "
                    "Latest message or system instructions may "
                    "be too large."
                )
