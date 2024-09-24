'''
Wisdom Omodiagbe
CS 325 Project 1
'''

import openai

# uses the ollama model on the local host
client = openai.OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="nokeyneeded",
)

def generate_output(text):
    response = client.chat.completions.create(
        model="phi3",
        temperature=0.7,
        n=1,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": text},
        ],
    )
    return response.choices[0].message.content


# get input from text file
with open("input.txt") as file:
    with open("output.txt", "w") as out:
        inputs = file.readlines() # read inputs
        for text in inputs:
            response = generate_output(text)
            out.write(response + "\n")
            
