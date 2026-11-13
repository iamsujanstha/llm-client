
import os
from llm_client import LLMClient

from conversation import Conversation


model_id = os.getenv("LLM_MODEL")

client = LLMClient()

conversation = Conversation(
    client,
    system_prompt="You are a helpful technical assistant."
)


#Level 1
# try:
#     answer = client.chat([
#         {
#             "role": "user",
#             "content": "What is Retrieval Augmented Generation?"
#         }
#     ])

#     print("LLM Response:", answer)

#Level 2
# try:
#     messages = [
#         {
#             "role": "user",
#             "content": "Explain microservices architecture."
#         }
#     ]

#     for chunk in client.stream_chat(messages):
#         print(chunk, end="", flush=True)

#     print()


try:
    while True:
        user_input = input("\nYou: ").strip()

        if user_input.lower() in ["/exit", "/quit"]:
            break

        if user_input.lower() == "/reset":
            conversation.reset()
            print("Conversation reset.")
            continue

        if not user_input:
            continue

        try:
            answer = conversation.send(user_input)
            print(f"\nAssistant: {answer}")

        except (RuntimeError, ValueError) as error:
            print(f"Error: {error}")


finally:
    client.close()

