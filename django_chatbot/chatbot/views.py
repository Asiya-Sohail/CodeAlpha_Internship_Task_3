from django.shortcuts import render, redirect
from django.http import JsonResponse

from django.contrib import auth
from django.contrib.auth.models import User

import nltk
from nltk.chat.util import Chat, reflections

# Define pairs of patterns and responses
pairs = [
    [
        r"(hi|hello|bro|dude)",
        ["Hey, how can I assist you? ",]
    ],
    [
        r"can you teach me (.*)",
        ["Sorry I have limited knowledge, Try something else.",]
    ],
    [
        r"my name is (.*)",
        ["Hello %1, how can I assist you today?", "Hi %1, what can I do for you?",]
    ],
    [
        r"what is your name?",
        ["My name is ChatBot and I'm here to help.", "You can call me ChatBot.",]
    ],
    [
        r"how are you ?",
        ["I'm doing well, thank you!", "I'm fine, thank you for asking.",]
    ],
    [
        r"(.*) your name ?",
        ["My name is ChatBot. How can I assist you?",]
    ],
    [
        r"what can you do ?",
        ["I can help you with various tasks like providing information, answering questions, or just having a conversation.",]
    ],
    [
        r"how can I contact you ?",
        ["You can contact me via email at chatbot@example.com.",]
    ],
    [
        r"where are you located ?",
        ["I exist in the digital realm, always ready to assist you wherever you are!",]
    ],
    [
        r"do you have trust issues ?",
        ["Hehe, I only response to my favourite ones",]
    ],
    [
        r"(.*) do you like me? ",
        ["As long as you are not going to another chatbot, I like you!",]
    ],
    [
        r"(.*) (weather|temperature) in (.*)",
        ["The weather in %3 is currently unavailable.", "Sorry, I don't have access to real-time weather information.",]
    ],
    [
        r"(.*) (movie|film)",
        ["I can't play movies, but I can suggest some popular movies for you to watch.",]
    ],
    [
        r"(.*) (play|song|music) ",
        ["I'm not capable of playing music, but I can recommend some great songs if you'd like!",]
    ],
    [
        r"(.*) (good morning|good afternoon|good evening)",
        ["Good %1! How can I assist you today?", "Hello! What can I do for you %1?",]
    ],
    [
        r"(.*) (thank you|thanks) (.*)",
        ["You're welcome!", "No problem! If you need further assistance, feel free to ask.",]
    ],
    [
        r"(.*)(how|what) (.*)",
        ["I'm here to provide assistance. Please specify your question or request.",]
    ],
    [
        r"(.*)(can|could) you (.*)",
        ["I can certainly try. Please specify what you need assistance with.",]
    ],
    [
        r"(.*) (recommend|suggest) (.*)",
        ["Sure! I can recommend books, movies, music, and more. Just let me know what you're interested in.",]
    ],
    [
        r"(.*)(favorite|favourite) (.*)",
        ["I don't have personal preferences, but I can recommend popular choices based on your interests.",]
    ],
    [
        r"(.*) (help|assistance) (.*)",
        ["Of course! I'm here to help. Just let me know what you need assistance with.",]
    ],
    [
        r"(.*) (learn|study|education) (.*)",
        ["I can provide information on various topics. What would you like to learn about?",]
    ],
    [
        r"(.*) (sports|team|athlete) (.*)",
        ["I can provide information about sports, teams, and athletes. What are you interested in?",]
    ],
    [
        r"(.*) (news|current events) (.*)",
        ["I can provide updates on current events and news topics. What specific news are you interested in?",]
    ],
    [
        r"(.*) (joke|funny) (.*)",
        ["Sure, here's a joke: Why don't scientists trust atoms? Because they make up everything!",]
    ],
    [
        r"(.*) (fact|interesting) (.*)",
        ["Did you know? The shortest war in history was between Britain and Zanzibar on August 27, 1896. Zanzibar surrendered after just 38 minutes!",]
    ],
    [
        r"(.*) (birthdays|special occasion) (.*)",
        ["Happy birthday/special occasion! Wishing you a fantastic day filled with joy and happiness.",]
    ],
    [
        r"(.*) (hobby|interest) (.*)",
        ["I'm interested in helping you discover new hobbies or learning more about your current interests. What are you passionate about?",]
    ],
    [
        r"(.*) (food|recipe) (.*)",
        ["I can suggest recipes or provide information about different cuisines. What type of food are you interested in?",]
    ],
    [
        r"(.*) (health|wellness) (.*)",
        ["I can provide general health tips and information about maintaining wellness. What health-related topics are you curious about?",]
    ],
    [
        r"(.*) (technology|innovation) (.*)",
        ["I'm interested in technology and innovation too! What specific tech topics would you like to discuss?",]
    ],
    [
        r"(.*) (travel|destination) (.*)",
        ["I can recommend travel destinations and provide information about popular tourist spots. Where would you like to go?",]
    ],
    [
        r"(.*) (pet|animal) (.*)",
        ["I love animals too! What kind of pets do you have or are interested in?",]
    ],
    [
        r"(.*) (language|linguistics) (.*)",
        ["Languages are fascinating! What aspects of language or linguistics are you interested in?",]
    ],
    [
        r"(.*) (relationship|love) (.*)",
        ["Relationships can be complex. How can I assist you with relationship advice or information?",]
    ],
    [
        r"(.*) (philosophy|ethics) (.*)",
        ["Philosophy and ethics are profound subjects. What specific questions or topics would you like to explore?",]
    ],
    [
        r"(.*) (politics|government) (.*)",
        ["Politics can be a contentious topic. What political issues or government systems are you interested in discussing?",]
    ],
    [
        r"(.*) (environment|sustainability) (.*)",
        ["Protecting the environment is crucial. How can I assist you with information or tips on sustainability?",]
    ],
    [
        r"(.*) (history|historical event) (.*)",
        ["History is full of fascinating events. What historical period or event are you interested in learning more about?",]
    ],
    [
        r"(.*) (work|job|career) (.*)",
        ["I can provide career advice or information about different professions. What specific career-related questions do you have?",]
    ],
    [
        r"(.*) (art|creative) (.*)",
        ["Artistic expression is wonderful. What forms of art or creative endeavors are you passionate about?",]
    ],
    [
        r"(.*) (finance|money) (.*)",
        ["Financial literacy is important. How can I assist you with financial advice or information?",]
    ]
]

nltk.download('punkt')
nltk.download('wordnet')

def ask_chatbot(user_input):
    # Create a ChatBot with the defined pairs
    chat = Chat(pairs, reflections)
    response = chat.respond(user_input)
    return response

# Create your views here.
def chatbot(request):
    if request.method == "POST":
        message = request.POST.get('message')
        print(ask_chatbot(message))
        response = ask_chatbot(message)
        if response == None:
            response("Sorry this is beyond my knowledge! Try something else")
        return JsonResponse({'message' : message, 'response' : response})
    return render(request, 'chatbot.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('chatbot')
        else:
            error_message = 'Invalid username or password'
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            try:
                user = User.objects.create_user(username, email, password1)
                user.save()
                auth.login(request, user)
                return redirect('chatbot')
            except:
                error_message = "Error creating an account"
                return render(request, 'register.html', {'error_message' : error_message})

        else:
            error_message = "Password don't match"
            return render(request, 'register.html', {'error_message' : error_message})
    
    return render(request, 'register.html')

def logout(request):
    auth.logout(request)
    return redirect('login')
    #return render(request, "login.html")




