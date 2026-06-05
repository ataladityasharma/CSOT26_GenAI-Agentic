import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)

def run_chatbot():
    messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]
    
    print("Chat started. Type 'exit' to quit.\n")

    while True:
        # TODO: take user input
        user_input = input("[YOU] ") 

        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        if user_input == "/reset":
            messages = [
                {"role": "system", "content": "You are a helpful assistant."}
            ]
            last_usage = None
            print("[SYSTEM] Conversation history cleared.")
            continue
        if user_input == "/tokens":
            if last_usage:
                print(last_usage)
            else:
                print("[SYSTEM] No API calls made yet.")
            continue

        # TODO: append the user turn to messages
        messages.append({"role": "user", "content": user_input})

        # TODO: call the API with the full messages list
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b:free",
            messages=messages,
        ) 
        last_usage = response.usage

        # TODO: extract the assistant's reply
        assistant_reply = response.choices[0].message.content

        # TODO: append the assistant turn to messages
        messages.append({"role": "assistant", "content": assistant_reply})

        # TODO: print the reply
        print(f"[MODEL] {assistant_reply}")
 
    return 

if __name__ == "__main__":
    run_chatbot()