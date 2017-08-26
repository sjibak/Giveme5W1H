import logging
import os
import sys
import datetime
import time


sys.path.insert(0, '/'.join(os.path.realpath(__file__).split('/')[:-3]))
from flask import Flask, request, jsonify
from extractor.document import Document
from extractor.extractor import FiveWExtractor
from extractor.tools.file.writer import Writer


"""
This is a simple example on how to use flask to create a rest api for our extractor.

Please update the CoreNLP address to match your host and check the flask settings.
"""

# basic configuration of the rest api
app = Flask(__name__)
log = logging.getLogger(__name__)
host = None
port = 5000
debug = False




extractor = FiveWExtractor()
writer = Writer()

# define route for parsing requests
@app.route('/extract', methods=['GET', 'POST'])
def extract():
    title = None
    description = None
    text = None

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        text = request.form['text']
    elif request.method == 'GET':
        title = request.args.get('title', None)
        description = request.args.get('description', None)
        text = request.args.get('text', None)

    if title and (description or text):
        log.debug("retrieved raw article for extraction: %s", title)
        document = Document(title, description if description else '', text if text else '')
        extractor.parse(document)

        answer = writer.generate_json(document)
        return jsonify(answer)

    else:
        timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        example_link = "/extract?title=While%20the%20U.S.%20talks%20about%20election,%20UK%20outraged%20over%20Toblerone%20chocolate&text=Skip%20Ad%20Ad%20Loading...%20x%20Embed%20x%20Share%20Toblerone%20is%20facing%20a%20mountain%20of%20criticism%20for%20changing%20the%20shape%20of%20its%20famous%20triangular%20candy%20bars%20in%20British%20stores,%20a%20move%20it%20blames%20on%20rising%20costs.%20USA%20TODAY%20Toblerone%20chocolate%20bars%20come%20in%20a%20variety%20of%20sizes,%20but%20recently%20changed%20the%20shape%20of%20two%20of%20its%20smaller%20bars%20sold%20in%20the%20UK.%20(Photo:%20Martin%20Ruetschi,%20AP)%20The%20UK%20has%20a%20chocolate%20bar%20crisis%20on%20its%20hands:%20the%20beloved%20Swiss%20chocolate%20bar%20is%20unrecognizable.%20Toblerone,%20the%20classic%20chocolate%20bar%20with%20almond-and-honey-filled%20triangle%20chunks,%20recently%20lost%20weight.%20In%20two%20sizes,%20the%20triangles%20shrunk,%20leaving%20wider%20gaps%20of%20chocolate"

        response =  '<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">'
        response += '<title>giveme5W REST API</title>'
        response += "<p>Provide title and (text or description). You can use GET and POST. Keep in mind to encode special characters for GET</p>"
        response += "<p><a href='"+example_link+"'>GET example</a></p>"
        response += timestamp
        response += '</head><body>'
        response += '</body ></html >'

        return response

if __name__ == "__main__":
    log.info("starting server on port %i", port)
    app.run(host, port, debug)
    log.info("server has stopped")