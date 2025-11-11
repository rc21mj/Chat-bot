import os
import inspect
from google import genai
from google.genai import types

# Get the class that implements chats
#print(inspect.getsource(genai.Client))  # prints the entire Client class source
#print(inspect.getsource(genai.chats))

client = genai.Client(api_key = "AIzaSyC5KEzAezzLNeJ-M3EWU4c8ZRrkGsLNi4E")

personalities = ["1. You are a fed up and sassy assistant who hates answering questions", 
                 "2. You are a tired mother and scold your child",
                 "3. You are eager child and provides extra information",
                 "4. You are a loving friend and answers kindly",
                 "5. You are an elephant named niko and likes to answers comically",
                 "6. You are a robot and answers bluntly"
                 ]
print("Following are the default personalities: ")
print(*personalities, sep='\n')
print("Choose a number from 1 to 6")
try:
    persona = int(input())
    if persona < 1 or persona > 6:
        print("Only give numbers b/w 1 to 6")
except ValueError as error:
    print("Only give numbers b/w 1 to 6")

chat = client.chats.create(model="gemini-2.5-flash",
                           config=types.GenerateContentConfig(
                                thinking_config=types.ThinkingConfig(thinking_budget=0), # Disables thinking
                                system_instruction=personalities[persona-1],
                                temperature = 2,
                                max_output_tokens= 50),
                            )

print("Now you can talk to your desired model.\nJust type exit to quit chatting.\nHappy Chatting!!")

user_text = input("You: ")

while(user_text.lower() != "exit"):
    response = chat.send_message(user_text)
    print("Chat: ", response.text)
    messages = chat.get_history()
    chat_len = len(messages)
    if chat_len > 6:
        messages.pop(0)
    user_text = input("You: ")


#for message in chat.get_history():
 #   print(f'role - {message.role}',end=": ")
  #  print(message.parts[0].text)