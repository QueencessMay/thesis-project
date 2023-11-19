# sentiment/views.py
from django.shortcuts import redirect, render
from django.apps import apps
from .forms import CSVForm
import pandas as pd
import tensorflow as tf
from . import Preprocessing


# Views for one game review with or without emojis and emoticons

def view_single_without(request):
  if request.method == "POST":
    model = apps.get_app_config('thesis_app').model_without
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
    model = apps.get_app_config('thesis_app').model_with
    text_input = request.POST.get('textarea_input', '')
    text_input_preprocessed = Preprocessing.preprocess_text(text_input)
    text_output = analyze_single(text_input_preprocessed, model)

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
  tokenizer = apps.get_app_config('thesis_app').tokenizer
  inputs = tokenizer(input, return_tensors="tf")
  outputs = model(inputs)
  sentiment = tf.argmax(outputs.logits, axis=1).numpy()[0]
  return sentiment


# Views for multiple game reviews with or without emojis and emoticons

def view_multi(request):
  if request.method == 'POST':
    form = CSVForm(request.POST, request.FILES)
    if form.is_valid():
      file_input = form.cleaned_data['csv']
      model_input = form.cleaned_data['model_field']
      
      model = apps.get_app_config('thesis_app').model_with if model_input == "opt_with" else apps.get_app_config('thesis_app').model_without
      file_output = analyze_file(file_input, model)

      request.session['model'] = "With Emojis and Emoticons" if model_input == "opt_with" else "Without Emojis and Emoticons"
      request.session['file_output'] = file_output
      return redirect('multiple_result')
  else:
    form = CSVForm()
  return render(request, "thesis_app/multi.html", { 'form': form }) 

def view_multi_result(request):
  model = request.session.get('model', [])
  file_result = request.session.get('file_output', [])
  context = {
    'model' : model,
    'result': file_result
  }
  return render(request, "thesis_app/multi-result.html", context)


# Helper functions

def analyze_file(file, model):
  results = []

  for batch in pd.read_csv(file, header=None, names=['review_col'], chunksize=500):
    reviews = batch['review_col'].tolist()
    preprocessed_reviews = [Preprocessing.preprocess_text(text) for text in reviews]
    sentiments = analyze_batch(preprocessed_reviews, model)
    batch_results = [
      {
        'review': review,
        'sentiment': "Negative" if sentiment == 0 else "Positive"
      }
      for review, sentiment in zip(reviews, sentiments)
    ]
    results.extend(batch_results)

  return results

def analyze_batch(reviews, model):
  tokenizer = apps.get_app_config('thesis_app').tokenizer
  inputs = tokenizer(reviews, return_tensors="tf", padding=True, truncation=True)
  outputs = model(inputs)
  sentiments = tf.argmax(outputs.logits, axis=1).numpy().tolist()
  return sentiments

def home(request):
  return view_single_without(request)