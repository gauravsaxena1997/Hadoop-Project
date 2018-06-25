from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import auth
from django.views.generic import View
from .forms import userinput
from django.template import loader
from django.http import HttpResponse
# extra
import tweepy
from TwitterAPI import TwitterAPI
import urllib
from textblob import TextBlob
from tweepy.streaming import json
import pyrebase
from django.http import HttpResponseRedirect

from .sentimeter import primary

def twitter (request):
    user_input = userinput()
    return render(request, "twitter.html")

def analyse(request):
    user_input = request.GET['hash']
    no_of_tweets = int(request.GET['no_of_tweets'])
    print (user_input)
    print (no_of_tweets)
    data = primary(user_input,no_of_tweets)
    return render(request, "result.html", {'data': data})
