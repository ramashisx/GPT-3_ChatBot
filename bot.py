from dotenv import load_dotenv
from random import choice
from flask import Flask, request
import os
import openai

load_dotenv()
openai.api_key = "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"
completion = openai.Completion()

start_sequence = "\nBot:"
restart_sequence = "\n\nPerson:"
session_prompt = ""


def ask(question, chat_log=""):
    if chat_log == "":
        prompt_text = f'{"Person:"} {question}{start_sequence}'
    else:
        prompt_text = f'{chat_log}{restart_sequence} {question}{start_sequence}:'

    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt_text,
        temperature=0.8,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.3,
        stop=["\n"],
    )
    story = response['choices'][0]['text']
    return str(story)


def append_interaction_to_chat_log(question, answer, chat_log=""):
    if chat_log == "":
        return f'{"Person:"} {question}{start_sequence} {answer}'
    return f'{chat_log}{restart_sequence} {question}{start_sequence} {answer}'
