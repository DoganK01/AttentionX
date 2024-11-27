import chainlit as cl
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch

MODEL_NAME = "DoganK01/mistral-7b-instruct-raft-ft"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, torch_dtype=torch.bfloat16)

generator = pipeline("text-generation", model=model, tokenizer=tokenizer)

chat_history = []

@cl.on_message
async def main(message: str):
    chat_history.append(f"User: {message}")
    conversation = "\n".join(chat_history)
    response = generator(conversation, max_length=1000, num_return_sequences=1, do_sample=True, temperature=0.7)
    generated_text = response[0]["generated_text"]
    bot_response = generated_text[len(conversation):].strip()
    chat_history.append(f"Bot: {bot_response}")
    await cl.Message(content=f"🤖: {bot_response}").send()
