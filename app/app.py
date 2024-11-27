import chainlit as cl
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch
import logging
import os
import sys

MODEL_NAME = "DoganK01/mistral-7b-instruct-raft-ft"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, torch_dtype=torch.bfloat16)

generator = pipeline("text-generation", model=model, tokenizer=tokenizer)

@cl.on_chat_start
async def start_chat():
    await cl.Avatar(
        name="Chatbot", url="https://cdn-icons-png.flaticon.com/512/8649/8649595.png"
    ).send()
    await cl.Avatar(
        name="Error", url="https://cdn-icons-png.flaticon.com/512/8649/8649595.png"
    ).send()
    await cl.Avatar(
        name="You",
        url="https://media.architecturaldigest.com/photos/5f241de2c850b2a36b415024/master/w_1600%2Cc_limit/Luke-logo.png",
    ).send()
    cl.user_session.set(
        "message_history",
        [{"role": "system", "content": system_content}],
    )

@cl.on_message
async def on_message(message: cl.Message):
    message_history = cl.user_session.get("message_history")
    message_history.append({"role": "user", "content": message.content})
    logger.info("Question: [%s]", message.content)
    
    response = generator(message_history, max_length=1000, num_return_sequences=1, do_sample=True, temperature=0.7)
    generated_text = response[0]["generated_text"]
    message_history.append({"role": "assistant", "content": generated_text})
    await generated_text.send()
