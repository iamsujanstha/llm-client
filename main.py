
import os
from llm_client import LLMClient

model_id = os.getenv("LLM_MODEL")

client = LLMClient()

#Level 1
# try:
#     answer = client.chat([
#         {
#             "role": "user",
#             "content": "What is Retrieval Augmented Generation?"
#         }
#     ])

#     print("LLM Response:", answer)

try:
    messages = [
        {
            "role": "user",
            "content": "Explain microservices architecture."
        }
    ]

    for chunk in client.stream_chat(messages):
        print(chunk, end="", flush=True)

    print()

finally:
    client.close()

