# sentiment/views.py
from django.shortcuts import render
import tensorflow as tf
from transformers import DistilBertTokenizerFast, TFDistilBertForSequenceClassification
import random

# tokenizer = DistilBertTokenizerFast.from_pretrained('distilbert-base-uncased')
# model_path = 'FiouReia/beshybert'
# beshybert = TFDistilBertForSequenceClassification.from_pretrained(model_path)

def single(request):
  if request.method == "POST":
    text_input = request.POST.get('textarea_input', '')
    text_output = perform_sentiment_analysis(text_input)
    context = {
      'result': text_output,
      'user_input': text_input,
    }
    return render(request, 'thesis_app/single.html', context)
  else:
    return render(request, 'thesis_app/single.html')

def multi(request):
  return render(request, "thesis_app/multi.html")

def home(request):
  return single(request)

def perform_sentiment_analysis(sentence):
  # Insert our amazing sentiment analyzer here
  return random.choice([-1, 1]) # Number na lang ireturn nyo ah: 1 Positive, -1 Negative, 0 Default