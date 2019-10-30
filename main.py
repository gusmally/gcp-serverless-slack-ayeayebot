import json
import random
import os
from flask import jsonify

with open('data.json', 'r') as e:
    image_data = e.read()
imagesByTerm = json.loads(image_data)


def verify_web_hook(form): 
    if not form or form.get('token') != os.environ['SLACK_TOKEN']:
        raise ValueError('Invalid request/credentials.')


def search_images(term):
    print(imagesByTerm)
    imageMatches = []
    
    for a in imagesByTerm:
        if str(term.lower()) in a:
            imageMatches.append(a[term.lower()])
            
    if len(imageMatches) > 1:
        choice = random.choice(imageMatches)

        message = {
            "response_type": "in_channel",
            "attachments": []
        }

        attachment = {}
        attachment['image_url'] = choice
        message['attachments'].append(attachment)
        return message
    elif len(imageMatches) == 1:
        image_url = imageMatches[0]

        message = {
            "response_type": "in_channel",
            "attachments": []
        }

        attachment = {}
        attachment["image_url"] = image_url
        print(image_url)
        message["attachments"].append(attachment)
        return message
    else:
        message = {
            "response_type": "ephemeral",
            "text": "no aye ayes matched that term :( _this form will hopefully one day support submissions_"
        }
        return message


def ayeaye_bot(request):
    if request.method != 'POST':
        return 'Only POST requests are accepted', 405
    
    print('request:');
    print(request.form['text'])

    verify_web_hook(request.form)
    search_response = search_images(request.form['text'])
    print(search_response)
    return jsonify(search_response)
