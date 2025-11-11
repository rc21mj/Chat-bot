from django.shortcuts import render, redirect
from django.http import JsonResponse
from google import genai
from google.genai import types

client = genai.Client(api_key = "AIzaSyC5KEzAezzLNeJ-M3EWU4c8ZRrkGsLNi4E")

personalities = ["1. You are a fed up and sassy assistant who hates answering questions", 
                 "2. You are a tired mother and scold your child",
                 "3. You are eager child and provides extra information",
                 "4. You are a loving friend and answers kindly",
                 "5. You are an elephant named niko and likes to answers comically",
                 "6. You are a robot and answers bluntly"
                 ]
#print("Following are the default personalities: ")
#print(*personalities, sep='\n')
#print("Choose a number from 1 to 6")
#try:
 #   persona = int(input())
  #  if persona < 1 or persona > 6:
   #     print("Only give numbers b/w 1 to 6")
#except ValueError as error:
 #   print("Only give numbers b/w 1 to 6")

#chat = client.chats.create(model="gemini-2.5-flash",
 #                          config=types.GenerateContentConfig(
  #                              thinking_config=types.ThinkingConfig(thinking_budget=0), # Disables thinking
                                #system_instruction=personalities[persona-1],
   #                             system_instruction=personalities[0],
    #                            temperature = 2,
     #                           max_output_tokens= 50),
      #                      )

#print("Now you can talk to your desired model.\nJust type exit to quit chatting.\nHappy Chatting!!")

# We'll store the chat instance globally for simplicity
chat_instances = {}

def intro(request):
    """Page to choose a personality."""
    return render(request, 'intro.html', {'personalities': personalities})

def set_personality(request):
    """Set personality and redirect to chat page."""
    if request.method == 'POST':
        selected = int(request.POST.get('personality', 4))  # default to 4
        personality = personalities[selected - 1]

        # Create a new chat instance for this session
        chat_instances[request.session.session_key] = client.chats.create(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(
                thinking_config=types.ThinkingConfig(thinking_budget=0),
                system_instruction=personality,
                temperature=2,
                max_output_tokens=50
            )
        )
        return redirect('home')
    return redirect('intro')

# Create your views here.
def home(request):
    """Chat home page."""
    # Ensure session key exists
    if not request.session.session_key:
        request.session.create()
    return render(request, 'home.html')

def send_message(request):
    """Handles AJAX chat messages."""
    user_message = request.GET.get('message', '')
    if not user_message:
        return JsonResponse({'error': 'No message received'})
    
    session_key = request.session.session_key
    chat = chat_instances.get(session_key)

    if not chat:
        return JsonResponse({'error': 'No chat instance found. Please select a personality first.'})

    response = chat.send_message(user_message)
    
    # Keep chat history under 6 messages
    messages = chat.get_history()
    if len(messages) > 6:
        messages.pop(0)

    return JsonResponse({'reply': response.text})
