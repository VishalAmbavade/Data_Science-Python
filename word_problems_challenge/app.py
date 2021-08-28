import json
import pandas as pd
import spacy
from spacy import displacy
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from collections import Counter
from flask import Flask, render_template, url_for, request, jsonify
from flaskext.markdown import Markdown

nlp = spacy.load('en_core_web_sm')  

app = Flask(__name__)
Markdown(app)

@app.route('/')
def index():
    return render_template('index.html')


#### Following function extract the requiredd values such as entities, raw text, labels and other parameters

@app.route('/values', methods=["POST", "GET"])
def get_values():
    ### rawtext is value (problem) that user inputs in the lask app
    rawtext = request.form['rawtext']
    ##3 nlp = spacy.load('en_core_web_sm')
    doc = nlp(rawtext)
    l = []
    for X in doc:
        l.append([X, X.ent_iob_, X.ent_type_])
    itemDict = {str(item[0]): item[1:] for item in l}
    itemDict
    lengthOfEntities = len(doc.ents)
    ### Labels are entities
    labels = [x.label_ for x in doc.ents]
    labelCount = Counter(labels)
    items = [x.text for x in doc.ents]
    ### Top 3 items(entities) that appeared in the word problem, are stored here
    itemsCount = Counter(items).most_common(3)
    
    coeff = []
    ### Variables are used to store the cardinal or numerical (cardinal + percent + money + quantity)
    ### values. So that, equations could be formed using these variables in future.
    var = ['x1', 'x2', 'x3', 'x4', 'x5', 'x6']
    for i in range(len(labels)):
        if labels[i] == 'CARDINAL' or labels[i] == 'PERCENT' or labels[i] == 'MONEY' or labels[i] == 'QUANTITY':
            coeff.append(items[i])
    ### The labels from which coefficients are extracted are chosen based on the EDA performed on the whole
    ### dataset. 
    a_dict = {key:value for key, value in zip(var, coeff)}

    return jsonify(rawtext=rawtext, itemDict = itemDict, lengthOfEntities = lengthOfEntities, labelCount = labelCount,
    items = items, itemsCount = itemsCount, a_dict = a_dict)
    #"lengthOfEntities":lengthOfEntities, "labelCount":labelCount,"items":items, "itmesCount":itmesCount


#### The following function is for testing purpose. It was used for output in user readable format
'''
@app.route('/extract', methods=["GET", "POST"])
def extract():
    if request.method == 'POST':
        rawtext = request.form['rawtext']
        doc = nlp(rawtext)
        result = displacy.render(doc, style='ent') 
        result2 = displacy.render(doc, style='dep', jupyter = True, options = {'distance': 120})
        l = []
        for X in doc:
            l.append([X, X.ent_iob_, X.ent_type_])
        itemDict = {item[0]: item[1:] for item in l}
        itemDict
        lengthOfEntities = len(doc.ents)
        labels = [x.label_ for x in doc.ents]
        labelCount = Counter(labels)
        items = [x.text for x in doc.ents]
        itmesCount = Counter(items).most_common(3)

    return render_template('results.html', rawtext = rawtext, result = result, result2 = result2, l = l, 
    lengthOfEntities=lengthOfEntities, labelCount = labelCount, itmesCount = itmesCount)
'''


if __name__ == 'main':
    app.run(debug = True)