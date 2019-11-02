'''
Created on Oct 31, 2019

@author: shivani.chauhan
'''
from flask import Flask, Response, render_template, request, jsonify
import json
# from src.readtsv import Logic
from flask_restplus import Resource, Api, reqparse
from flask_cors import CORS
from flask_restplus import Api, reqparse
import datetime
import logging
from src.readtsv import Logic

app = Flask(__name__)
CORS(app)

api = Api(app, version='1.0', title='Autocomplete', description='World of Fuzzy Search')
nm_space = api.namespace("", description="A restful web service that allow to do fuzzy search..!")

logger=logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
fmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(fmt)
logger.addHandler(ch)

#created a parser to accept the user input, We can provide the input in the Swagger UI as well.
parser = reqparse.RequestParser()
parser.add_argument('input', type=str, help='Type the letter to see autocomplete feature..!')

# A GET request which accepts the user input and provides a json response containing top 25 matches based on ranking.
@nm_space.route('/search')
class autocomplete(Resource):
    @nm_space.expect(parser)
    def get(self):
        args = parser.parse_args()
        logic = Logic()
        try:
            start_time = datetime.datetime.now()
            list_of_words=[]
            input = args['input']
            if input == '':
                return Response('We need a input string..!', status = 500, mimetype = 'application/json')
            else:
                input_related_words = logic.search_word(input.lower())
                words = logic.sorting(input_related_words, input.lower())
                if len(words)==0:
                    return Response("{" + "\"Message\":\"No words found\"}", status = 404, mimetype = 'application/json')
                for word in words :
                    list_of_words.append(word[0])
                
        except Exception as e:
            end_time = datetime.datetime.now()
            time_elapsed = end_time - start_time
            logger.error('Some error occurred, please check logs : ' +str(e))
            logger.info("API Response Time (On Failure) : " + str(time_elapsed))
            return Response(str(e), mimetype='text/plain', status=500)
        
        end_time = datetime.datetime.now()
        time_elapsed = end_time - start_time 
        logger.info("API Response Time : " + str(time_elapsed))
        return Response(json.dumps(list_of_words), mimetype='application/json', status=200) 
            
# A Get request that takes user input and returns input string and its frequency as key value pair.
@nm_space.route('/wordcount')
class show_word_freq(Resource):
      
    @nm_space.expect(parser)
    def get(self):
        args = parser.parse_args()
        logic = Logic()
        dic = {}
        try:
            start_time = datetime.datetime.now()
            input = args['input']
            if input == '':
                return Response('We need a input string..!', status = 500, mimetype = 'application/json')
            else:
                related_words = logic.search_word(input.lower())
                words = logic.sorting(related_words, input.lower())
                if len(words)==0:
                    return Response('No words found..!', status = 404, mimetype = 'text/plain')
                else:
                    for tup in words :
                        if input == tup[0]:
                            dic[tup[0]] = tup[1]       
        except Exception as e:
            end_time = datetime.datetime.now()
            time_elapsed = end_time - start_time
            logger.error('Some error occurred, please check logs : ' +str(e))
            logger.info("API Response Time (On Failure) : " + str(time_elapsed))
            return Response(str(e), mimetype='text/plain', status=500)
        
        end_time = datetime.datetime.now()
        time_elapsed = end_time - start_time 
        logger.info("API Response Time : " + str(time_elapsed))
        return Response(json.dumps(dic), status = 200, mimetype = 'application/json')
                        

if __name__ == '__main__':
    app.run(debug=True)
