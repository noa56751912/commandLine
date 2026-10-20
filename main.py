import prompt
import gradio as gr
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()


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
    app = gr.Interface(
        fn=generate_cli_command,
        inputs=gr.Textbox(label="What do you want to do?"),
        outputs=gr.Textbox(label="Command"),
        title="AI Command-Line Assistant",
        description="Describe a task in Hebrew or English and get the matching Windows CMD command. "
                    "Returns NULL for unclear or dangerous requests.",
        examples=["כמה קבצים יש לי בתיקיית ההורדות?", "List the files on my desktop"],
    )
    app.launch()


if __name__ == "__main__":
    main()
