# sentiment/views.py
from django.shortcuts import render
from .forms import CSVForm
import tensorflow as tf
from transformers import DistilBertTokenizerFast, TFDistilBertForSequenceClassification

# Analyze sentiment of one game review with or without emojis and emoticons

def view_single_without(request):
  if request.method == "POST":
    path = 'FiouReia/distilbert-uncased-without-emojis-emoticons'
    model = TFDistilBertForSequenceClassification.from_pretrained(path)

    text_input = request.POST.get('textarea_input', '')
    text_output = analyze_single(text_input, model)

    context = {
      'result': text_output,
      'user_input': text_input,
    }
    return render(request, 'thesis_app/single-without.html', context)
  else:
    return render(request, 'thesis_app/single-without.html')

def view_single_with(request):
  if request.method == "POST":
    path = 'FiouReia/distilbert-uncased-with-emojis-emoticons'
    model = TFDistilBertForSequenceClassification.from_pretrained(path)

    text_input = request.POST.get('textarea_input', '')
    text_output = analyze_single(text_input, model)

    context = {
      'result': text_output,
      'user_input': text_input,
    }
    return render(request, 'thesis_app/single-with.html', context)
  else:
    return render(request, 'thesis_app/single-with.html')
  
def analyze_single(input, model):
  if not input:
    return -1
  tokenizer = DistilBertTokenizerFast.from_pretrained('distilbert-base-uncased')
  inputs = tokenizer(input, return_tensors="tf")
  outputs = model(inputs)
  sentiment = tf.argmax(outputs.logits, axis=1).numpy()[0]
  return sentiment

# Analyze sentiment of multiple game reviews with or without emojis and emoticons

def multi(request):
  if request.method == 'POST':
    form = CSVForm(request.POST, request.FILES)

    if form.is_valid():
      file_input = request.FILES['csv']

      # if file_input:
      #   if file_input.name.endswith('.csv'):
      #     try:
      #       csv.reader(file_input)
      #     except csv.Error:
      #       return render(request, "thesis_app/multi.html", { 'isError': True })

      file_output = analyze_multiple_sentiment(file_input)
      context = {
        'num_positive': file_output['num_positive'],
        'num_negative': file_output['num_negative'],
      }
      return render(request, "thesis_app/multi.html", context)
  else:
    form = CSVForm()
  return render(request, "thesis_app/multi.html", { 'form': form })

def analyze_multiple_sentiment(file):
  results = {
    'num_positive': 5,
    'num_negative': 5,
  } 
  return results 

def home(request):
  return view_single_without(request)