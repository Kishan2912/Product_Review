from django.shortcuts import render
from .models import Review_Product

import nltk
# uncomment if its not downloaded
# nltk.download('vader_lexicon')
# nltk.download('punkt') 
# nltk.download('wordnet')
nltk.download('omw-1.4')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import sent_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import re
import string

sid = SentimentIntensityAnalyzer()
lemmatizer = WordNetLemmatizer()

def preprocess_data(text):
    text = text.lower()
    text = re.sub('\[.*?\]','',text)
    text = re.sub('[%s]'%re.escape(string.punctuation),'',text)
    text = re.sub('\w*\d\w*','',text)
    words = word_tokenize(text)
    all_words = [lemmatizer.lemmatize(word) for word in words]
    out = ' '.join(all_words)
    return out

def norm(sentiment_value,mx,mn):
    value = ((sentiment_value+1)*(mx-mn))/(2)
    return value

def out(words,mx,mn):
    words = preprocess_data(words)
    value = sid.polarity_scores(words)['compound']
    return norm(value,mx,mn)


# Create your views here.

def home(request):
    initial = Review_Product.objects.all()
    sm = 0
    k=0
    for j in initial:
        k+=1
        sm = sm + j.rating
        print(j.rating)
    
    initial_review = sm/k

    target = {"initial_review":initial_review}

    return render(request,'home.html',target)

def Analyze(request):
    products = Review_Product.objects.all()
    rate = 0
    n = 0
    for i in products:
        n+=1
        rate = rate + i.rating
    
    if request.method == 'POST':
        print('a')

        text = request.POST["review_text"]
        mx_review_value = 5
        mn_review_value = 0
        sentiment_response = out(text,mx_review_value,mn_review_value)
        p = Review_Product(text=text, rating= sentiment_response)
        p.save()
        total_rating = (rate+sentiment_response)/(n+1)
        value = {"text":text,
                "result":sentiment_response,
                "total":total_rating}
        
        return render(request,'Analyze.html',value)