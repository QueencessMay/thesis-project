# sentiment/views.py
from django.shortcuts import render
from .forms import CSVForm
import tensorflow as tf
from transformers import DistilBertTokenizerFast, TFDistilBertForSequenceClassification
import random

# tokenizer = DistilBertTokenizerFast.from_pretrained('distilbert-base-uncased')
# model_path = 'FiouReia/beshybert'
# beshybert = TFDistilBertForSequenceClassification.from_pretrained(model_path)

def single(request):
  if request.method == "POST":
    text_input = request.POST.get('textarea_input', '')
    text_output = analyze_single_sentiment(text_input)
    context = {
      'result': text_output,
      'user_input': text_input,
    }
    return render(request, 'thesis_app/single.html', context)
  else:
    return render(request, 'thesis_app/single.html')

def multi(request):
  if request.method == 'POST':
    form = CSVForm(request.POST, request.FILES)
    if form.is_valid():
      file_input = request.FILES['csv']
      file_output = analyze_multiple_sentiment(file_input)
      context = {
        'num_positive': file_output['num_positive'],
        'num_negative': file_output['num_negative'],
      }
      return render(request, "thesis_app/multi.html", context)
  else:
    form = CSVForm()
  return render(request, "thesis_app/multi.html", { 'form': form })

def home(request):
  return single(request)

# Baguhin tong mga functions
def analyze_multiple_sentiment(file):
  # Insert our amazing sentiment analyzer here + File Reader XD
  results = {
    'num_positive': 5,
    'num_negative': 5,
  } # Nagbabago or smth
  return results 

def analyze_single_sentiment(input):
  # Insert our amazing sentiment analyzer here
  return random.choice([-1, 1]) # Number na lang ireturn nyo ah: 1 Positive, -1 Negative, 0 Default