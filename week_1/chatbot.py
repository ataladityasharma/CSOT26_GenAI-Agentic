import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class ChatAgent:
    def __init__(
        self,
        model: str,
        max_turns: int = 5,
        system_prompt: str = "You are a helpful assistant."
    ):
        self.model = model
        self.max_turns = max_turns
        self.last_usage = None

        self.messages = [
            {
                "role": "system",
                "content": system_prompt
            }
        ]

        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.environ["OPENROUTER_API_KEY"],
        )

    def trim_history(self):
        """
        Keep only the last N conversation turns.
        Each turn = user + assistant pair.
        """
        max_messages = 1 + (self.max_turns * 2)

        while len(self.messages) > max_messages:
            self.messages.pop(1)
            self.messages.pop(1)

    def call_model(self):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
        )

        self.last_usage = response.usage

        return response.choices[0].message.content

    def reset(self):
        self.messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            }
        ]

        self.last_usage = None

    def run(self):
        print(f"\nUsing model: {self.model}")
        print("Type 'exit' to quit.")
        print("Commands: /reset, /tokens\n")

        while True:
            user_input = input("[YOU] ")

            if user_input.lower() in ["exit", "quit"]:
                print("Goodbye!")
                break

            if user_input == "/reset":
                self.reset()
                print("[SYSTEM] Conversation history cleared.")
                continue

            if user_input == "/tokens":
                if self.last_usage:
                    print(self.last_usage)
                else:
                    print("[SYSTEM] No API calls made yet.")
                continue

            self.messages.append(
                {
                    "role": "user",
                    "content": user_input
                }
            )

            self.trim_history()

            assistant_reply = self.call_model()

            self.messages.append(
                {
                    "role": "assistant",
                    "content": assistant_reply
                }
            )

            self.trim_history()

            print(f"[MODEL] {assistant_reply}")


def choose_model():
    models = [
        "openai/gpt-oss-120b:free",
        "openai/gpt-oss-20b:free"
    ]

    print("Available Models:\n")

    for i, model in enumerate(models, start=1):
        print(f"{i}. {model}")

    while True:
        choice = input("\nSelect model (1-2): ")

        if choice in ["1", "2"]:
            return models[int(choice) - 1]

        print("Invalid choice.")


if __name__ == "__main__":
    selected_model = choose_model()

    agent = ChatAgent(
        model=selected_model,
        max_turns=5
    )

    agent.run()