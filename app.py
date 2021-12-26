import requests
import os
import uuid
from dotenv import load_dotenv
from flask import Flask, render_template, request
load_dotenv()

app = Flask(__name__)


@app.route('/', methods=['get'])
def index():
    return render_template('start.html')



@app.route('/', methods=['post'])
def index_post():
    original_text = request.form['text']
    target_language = request.form['language']

    key = os.environ['key']
    endpoint = os.environ['endpoint']
    location = os.environ['location']

    path = '/translate?api-version=3.0'

    target_language_parameter = '&to=' + target_language

    constructed_url = endpoint + path + target_language_parameter

    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    body = [{'text': original_text}]

    translator_request = requests.post(
        constructed_url, headers=headers, json=body)

    translator_response = translator_request.json()

    translated_text = translator_response[0]['translations'][0]['text']

    return render_template(
        'result.html',
        translated_text=translated_text,
        original_text=original_text,
        target_language=target_language
    )