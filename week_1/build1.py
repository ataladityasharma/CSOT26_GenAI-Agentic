import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)

def call_model(prompt: str) -> str:
    """
    Make a single chat completion call.
    Print the full response object first and understand its structure.
    Then return just the assistant's text.
    """
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b:free",
        messages=[
            # {"role": "system", "content": "You are an american karen, speek like a karen"},
            # {"role": "system", "content": "Include a cross question in your response, related to the user's question."},
            #  {"role": "system", "content": "You are a desi indian aunty, speek like one"},
            {"role": "system", "content": "you are a fictions reader"},
            {"role": "system", "content": "Include a fictional element in your response, related to the user's question."},
            {"role": "user", "content": prompt}
        ],
    )
    # return response
    # return response.usage
    return response.choices[0].message.content


    # TODO: try adding a system prompt with different instructions and guidelines
    # TODO: inspect `response` before you extract anything from it
    # What's in response.choices? What's in response.usage?
    # pass

if __name__ == "__main__":
    print(call_model("What is the capital of Australia?"))
