"""
Program Title: Game Reviews Sentiment Analysis Web App Views

Programmers: 
- Queencess May Munsayac
- Jehan Batang
- Jon Ray Mabalot
- Job Adrian Suaviso

Where the program fits in the general system designs: 
This Python script contains views for a sentiment analysis web application using Django. 
It provides functionality to analyze single and multiple game reviews with or without emojis and emoticons.

Date written and revised: 
Written: 2023-10-20
Revised: 2024-02-8

Purpose:
The purpose of this script is to define views for processing user requests and rendering appropriate HTML templates. 
It interacts with models and preprocessing functions to perform sentiment analysis on input data (game reviews).

Data structures, algorithms, and control:
- Data Structures: 
  - Dictionary for storing sentiment analysis results.
  - Lists for storing game review data and sentiments.
- Algorithms:
  - Sentiment analysis using the DistilBERT model
  - Batch processing of game reviews for efficiency.
- Control:
  - Django views for handling user requests and rendering templates.
  - Session management is utilized to store and retrieve data across different views.
  - Conditional statements and exception handling to manage the flow of execution and handle errors effectively.
"""

# Imports
import csv
import pandas as pd
import tensorflow as tf
from django.shortcuts import redirect, render
from django.apps import apps
from django.http import HttpResponse, HttpResponseServerError
from .forms import CSVForm
from .preprocessing import preprocess


# Views for one game review with or without emojis and emoticons

"""
View for analyzing a single game review without emojis and emoticons.
@param request (HttpRequest) object containing user input
@return rendered HTML template with analysis result
"""
def view_single_without(request):
    request.session['model_type'] = 'without'
    if request.method == "POST":
        try:
            model = apps.get_app_config('thesis_app').model_without
            text_input = request.POST.get('textarea_input', '')
            text_input_preprocessed = preprocess.preprocess_text(text_input, 'with')
            text_output = analyze_single(text_input_preprocessed, model)

            context = {
                'result': text_output,
                'user_input': text_input,
            }
            return render(request, 'thesis_app/single-without.html', context)
        except Exception as e:
            return HttpResponseServerError(f"An error occurred during single review analysis: {str(e)}")
    else:
        return render(request, 'thesis_app/single-without.html')

"""
View for analyzing a single game review with emojis and emoticons.
@param request (HttpRequest) object containing user input
@return rendered HTML template with analysis result
"""
def view_single_with(request):
    request.session['model_type'] = 'with'
    if request.method == "POST":
        try:
            model = apps.get_app_config('thesis_app').model_with
            text_input = request.POST.get('textarea_input', '')
            text_input_preprocessed = preprocess.preprocess_text(text_input, 'with')
            text_output = analyze_single(text_input_preprocessed, model)

            context = {
                'result': text_output,
                'user_input': text_input,
            }
            return render(request, 'thesis_app/single-with.html', context)
        except Exception as e:
            return HttpResponseServerError(f"An error occurred during single review analysis: {str(e)}")
    else:
        return render(request, 'thesis_app/single-with.html')

"""
View for redirecting to the single game review analysis page.
@param request (HttpRequest) object
@return rendered HTML template for single review analysis
"""
def view_home(request):
  return view_single_without(request)


# Views for multiple game reviews with or without emojis and emoticons

"""
View for analyzing multiple game reviews.
@params request (HttpRequest) object containing user input, option (str) string captured from the URL representing the analysis option 
@return rendered HTML template with form for uploading CSV file
"""
def view_multi(request, option):
    if request.method == 'POST':
        try:
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
        except Exception as e:
            return HttpResponseServerError(f"An error occurred during multi-review analysis: {str(e)}")
    else:
        form = CSVForm()

    context = {
        'form': form,
        'option': option
    }   
    return render(request, "thesis_app/multi.html", context)

"""
View for displaying results of multiple game reviews analysis.
@params request (HttpRequest) object containing session data, option (str) string captured from the URL representing the analysis option
@return rendered HTML template with analysis results
"""
def view_multi_result(request, option):
    try:
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
    except Exception as e:
        return HttpResponseServerError(f"An error occurred while rendering the multi-result page: {str(e)}")

"""
View for downloading analysis results as a CSV file.
@params request (HttpRequest) object containing session data, option (str) string captured from the URL representing the analysis option
@return csv file download response
"""
def download_result(request, option):
    try:
        model = request.session.get('model', [])
        file_result = request.session.get('file_output', {})
        filename = option + '_results.csv'
        return generate_csv(file_result['results'], filename)
    except Exception as e:
        return HttpResponseServerError(f"An error occurred during downloading the result: {str(e)}")


# Helper functions

"""
Analyze a single game review using the specified model.
@params input (str) game review, model (DistilBERT) 
@return sentiment (int) label for the game review 
"""
def analyze_single(input, model):
  if not input:
    return -1
  
  tokenizer = apps.get_app_config('thesis_app').tokenizer
  inputs = tokenizer(input, return_tensors="tf")
  outputs = model(inputs)
  sentiment = tf.argmax(outputs.logits, axis=1).numpy()[0]

  return sentiment

"""
Analyzes multiple game reviews from a CSV file.
@params file (CSV file) containing game reviews, model (DistilBERT), review_type (str) type of game review
@return dictionary containing analysis results
"""
def analyze_file(file, model, review_type):
    try:
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
    except Exception as e:
        return HttpResponseServerError(f"An error occurred during file analysis: {str(e)}")

"""
Analyzes multiple game reviews using the specified model.
@params reviews (list) list of processed game reviews, model (DistilBERT)
@return sentiments (list) sentiment labels for each game review     
"""
def analyze_batch(reviews, model):
    try:
        tokenizer = apps.get_app_config('thesis_app').tokenizer
        inputs = tokenizer(reviews, return_tensors="tf", padding=True, truncation=True)
        outputs = model(inputs)
        sentiments = tf.argmax(outputs.logits, axis=1).numpy().tolist()
        return sentiments
    except Exception as e:
        return HttpResponseServerError(f"An error occurred during batch analysis: {str(e)}")

"""
Generate a CSV file from analysis results data.
@params data (list) list of analysis results, filename (str) name of the CSV file
@return csv file download response
"""
def generate_csv(data, filename):
    try:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        writer = csv.writer(response)
        writer.writerow(['Review', 'Sentiment'])

        for row in data:
            writer.writerow([row['review'], row['sentiment']])

        return response
    except Exception as e:
        return HttpResponseServerError(f"An error occurred during CSV generation: {str(e)}")