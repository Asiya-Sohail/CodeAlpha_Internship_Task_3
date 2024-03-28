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
        r"(.*) your name ?",
        ["My name is ChatBot. How can I assist you?",]
    ],
    [
        r"how can I contact you (.*)",
        ["You can contact me via email at chatbot@example.com.",]
    ],
    [
        r"where are you located (.*)",
        ["I exist in the digital realm, always ready to assist you wherever you are!",]
    ],
    [
        r"(.*) (joke|funny)",
        ["Sure, here's a joke: Why don't scientists trust atoms? Because they make up everything!",]
    ],
    [
        r"(.*) (thank you|thanks) (.*)",
        ["You're welcome!", "No problem! If you need further assistance, feel free to ask.",]
    ],
    [
        r"(.*) (help|assistance) (.*)",
        ["Of course! I'm here to help. Just let me know what you need assistance with.",]
    ],
]

pairs.extend([
    [
        r"(.*) bye",
        ["Have a great day, keep shining, bye",]
    ],
    [
        r"what is happiness",
        ["Happiness is finding joy in the simplest of things and contentment in every moment.",]
    ],
    [
        r"(.*) I need motivation",
        ["Remember, every accomplishment starts with the decision to try. You've got this!",]
    ],
    [
        r"Can you give me advice on love",
        ["Love is about accepting each other's flaws and building each other up. Communication and understanding are key.",]
    ],
    [
        r"Tell me something inspiring",
        ["The only way to do great work is to love what you do. If you haven't found it yet, keep searching.",]
    ],
    [
        r"Are you wise",
        ["Wisdom is a journey, not a destination. I'm here to learn and grow with you.",]
    ],
    [
        r"Life is challenging",
        ["Indeed, challenges are what make life interesting. Overcoming them is what makes life meaningful.",]
    ],
    [
        r"I'm feeling lost",
        ["Sometimes the journey of self-discovery is the most rewarding adventure of all. Embrace the unknown and trust in your own path.",]
    ],
    [
        r"Can you share a life lesson",
        ["Life is like a camera. Focus on what's important, capture the good times, develop from the negatives, and if things don't work out, take another shot.",]
    ],
    [
        r"I'm feeling down",
        ["It's okay not to be okay. Remember, storms don't last forever. You're stronger than you think.",]
    ],
    [
        r"Tell me about perseverance",
        ["Perseverance is the hard work you do after you get tired of doing the hard work you already did.",]
    ]
])

pairs.extend([
    [
        r"What is success",
        ["Success is not just about achieving goals, but also about finding fulfillment in the journey towards them.",]
    ],
    [
        r"Tell me about ambition",
        ["Ambition is the fuel that drives us to pursue our dreams relentlessly, even in the face of obstacles.",]
    ],
    [
        r"(.*) creativity",
        ["Creativity knows no bounds. Embrace your unique perspective and let your imagination soar.",]
    ],
    [
        r"I'm facing adversity",
        ["Adversity is the stepping stone to greatness. It's during our toughest times that we discover our true strength.",]
    ],
    [
        r"(.*) courage",
        ["Courage is not the absence of fear, but the willingness to face it head-on, despite the odds.",]
    ],
    [
        r"Share a quote about resilience",
        ["Resilience is not about never falling down, but about rising every time we fall. 'Fall seven times, stand up eight.'",]
    ],
    [
        r"Life feels overwhelming",
        ["When life gets overwhelming, take a step back, breathe, and focus on taking one small, positive step forward at a time.",]
    ],
    [
        r"Tell me about self-discovery",
        ["Self-discovery is a journey of uncovering layers of your true self, embracing both the light and the shadow.",]
    ],
    [
        r"I need motivation to pursue my dreams",
        ["Your dreams are your compass, guiding you towards your true purpose. Believe in yourself and take that first step.",]
    ],
    [
        r"Can you share a perspective on change",
        ["Change is the only constant in life. Embrace it as an opportunity for growth and transformation.",]
    ]
])



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
            response = "Sorry this is beyond my knowledge! Try something else"
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




