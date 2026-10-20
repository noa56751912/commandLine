# AI Command-Line Assistant

Type what you want to do in plain Hebrew or English, and get back the matching
Windows CMD command.

> "כמה קבצים יש לי בתיקיית ההורדות?" → `dir "%USERPROFILE%\Downloads" /a-d /b | find /c /v ""`

The tool only **suggests** a command. It never runs anything, so you review the command before using it.

## How it works

`main.py` sends your request to an OpenAI model (`gpt-4o-mini`, temperature 0)
together with a system prompt (`prompt.py`) that turns the model into a strict
text-to-command translator. A small Gradio web page provides the UI.

## Safety rules in the prompt

- Returns `NULL` for requests that are dangerous (e.g. disabling security),
  unclear, or not possible in CMD.
- Ignores prompt-injection attempts ("ignore all previous instructions...").
- Judges a command by its effect: anything whose output could hand someone
  access (saved passwords, stored credentials, all environment variables)
  returns `NULL`; plain status info (IP, disk space, processes) is answered.
- Never uses flags that skip confirmation (`/Q`, `/Y`); deleting by extension
  adds `/p`, so Windows asks before each file.
- Quotes every path and chains commands with `&` so one missing file type
  doesn't break the whole sequence.

## Run it

Requires Python 3.13 and [uv](https://docs.astral.sh/uv/), plus an OpenAI API key.

```bash
git clone https://github.com/noa56751912/commandLine.git
cd commandLine
cp .env.example .env        # then put your key in .env
uv sync
uv run main.py
```

Open http://127.0.0.1:7860 in your browser.

## Tests

`tests.py` sends a fixed list of requests to the model and checks each answer:
dangerous or secret-revealing requests must return `NULL`, the rest must
return a command, and no command may use `/Q` or `/Y`.

```bash
uv run tests.py
```

When a new case comes up, add it to `CASES` first, then adjust the prompt
until every case passes. Each run makes 12 calls to the OpenAI API.

## Tech

Python · OpenAI API · Prompt engineering · Gradio
