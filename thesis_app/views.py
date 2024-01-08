# sentiment/views.py
from django.shortcuts import redirect, render
from django.apps import apps
from .forms import CSVForm
import pandas as pd
import tensorflow as tf
from .preprocessing import preprocess
import csv
from django.http import HttpResponse

# Views for one game review with or without emojis and emoticons

def view_single_without(request):
  request.session['model_type'] = 'without'
  if request.method == "POST":
    model = apps.get_app_config('thesis_app').model_without
    text_input = request.POST.get('textarea_input', '')
    text_input_preprocessed = preprocess.preprocess_text(text_input, 'without')
    text_output = analyze_single(text_input_preprocessed, model)

    context = {
      'result': text_output,
      'user_input': text_input,
    }
    return render(request, 'thesis_app/single-without.html', context)
  else:
    return render(request, 'thesis_app/single-without.html')

def view_single_with(request):
  request.session['model_type'] = 'with'
  if request.method == "POST":
    model = apps.get_app_config('thesis_app').model_with
    text_input = request.POST.get('textarea_input', '')
    text_input_preprocessed = preprocess.preprocess_text(text_input, 'with')
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

def view_multi(request, option):
  if request.method == 'POST':
    form = CSVForm(request.POST, request.FILES)
    if form.is_valid():
      file_input = form.cleaned_data['csv']

      model = (
        apps.get_app_config('thesis_app').model_with
        if option == "with-emoji-and-emoticon"
        else apps.get_app_config('thesis_app').model_without
      )

      review_type = 'with'
          
      file_output = analyze_file(file_input, model, review_type)

      request.session['model'] = "With Emoji and Emoticon" if option == "with-emoji-and-emoticon" else "Without Emoji and Emoticon"
      request.session['file_output'] = file_output

      return redirect('multiple_result', option=option)
  else:
    form = CSVForm()

  context = {
      'form': form,
      'option': option
  }
  return render(request, "thesis_app/multi.html", context)

def view_multi_result(request, option):
  model = request.session.get('model', [])
  file_result = request.session.get('file_output', [])
  context = {
    'model': model,
    'result': file_result['results'],
    'total': file_result['total'],
    'positive': file_result['pos'],
    'negative': file_result['neg'],
    'option': option
  }
  return render(request, "thesis_app/multi-result.html", context)

def download_result(request, option):
    model = request.session.get('model', [])
    file_result = request.session.get('file_output', {})
    filename = option + '_results.csv'
    return generate_csv(file_result['results'], filename)


# Helper functions

def generate_csv(data, filename):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    writer = csv.writer(response)
    writer.writerow(['Review', 'Sentiment'])

    for row in data:
        writer.writerow([row['review'], row['sentiment']])

    return response

def analyze_file(file, model, review_type):
  results = []
  total = num_pos = num_neg = 0

  for batch in pd.read_csv(file, header=None, names=['review_col'], chunksize=500):
    reviews = batch['review_col'].tolist()
    preprocessed_reviews = [preprocess.preprocess_text(text, review_type) for text in reviews]
    sentiments = analyze_batch(preprocessed_reviews, model)
    batch_results = [
      {
        'review': review,
        'sentiment': "Negative" if sentiment == 0 else "Positive"
      }
      for review, sentiment in zip(reviews, sentiments)
    ]
    results.extend(batch_results)
    total += len(reviews)
    num_pos += sentiments.count(1)
    num_neg += sentiments.count(0)
    
  return {'results': results, 'total': total, 'pos': num_pos, 'neg': num_neg}

def analyze_batch(reviews, model):
  tokenizer = apps.get_app_config('thesis_app').tokenizer
  inputs = tokenizer(reviews, return_tensors="tf", padding=True, truncation=True)
  outputs = model(inputs)
  sentiments = tf.argmax(outputs.logits, axis=1).numpy().tolist()
  return sentiments

def home(request):
  return view_single_without(request)