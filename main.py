import prompt
import gradio as gr
from openai import OpenAI
import os
from dotenv import load_dotenv
import json
load_dotenv()
client=OpenAI()
prompt.SYSTEM_PROMPT = prompt.SYSTEM_PROMPT

def generate_cli_command(user_input):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=[
            {"role": "system", "content": prompt.SYSTEM_PROMPT},
            {"role": "user", "content": user_input}
        ]
    )
    return response.choices[0].message.content.strip()

def main():
    app = gr.Interface(fn=generate_cli_command, inputs="text", outputs="text")
    app.launch()


if __name__ == "__main__":
    main()
