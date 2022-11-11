import os
import xml.etree.ElementTree as ET
from heapq import nlargest
from string import punctuation

import pandas as pd
import spacy
from flask import Flask, render_template, request
from spacy.lang.en.stop_words import STOP_WORDS
from werkzeug.utils import secure_filename

from update_summarizer.main.cosine import cosine_similarity

nlp = spacy.load('en_core_web_sm')

stopwords = list(STOP_WORDS)


new_docs = {
    'topic': [],
    'file': [],
    'text': [],
    'cnt': []
}

docs = {
    'topic': [],
    'text': [],
    'summary': [],
}

summarized_df = pd.DataFrame(data=new_docs)
summarized_df.to_csv('summarized.csv', index=False)


topic = ''
cnt = 0
cnt2 = 0

num = 0


def remove_slash_n(s: str) -> str:
    """remove newline form a string"""
    return s.replace('\n', '')


def getSummary(text):
    doc = nlp(text)
    tokens = [token.text for token in doc]

    punctuation1 = punctuation + '\n' + '\n\n'

    word_frequencies = {}
    for word in doc:
        if word.text.lower() not in stopwords:
            if word.text.lower() not in punctuation1:
                if word.text not in word_frequencies.keys():
                    word_frequencies[word.text] = 1
                else:
                    word_frequencies[word.text] += 1

    max_frequencys = max(word_frequencies.values())

    for word in word_frequencies.keys():
        word_frequencies[word] = word_frequencies[word]/max_frequencys

    sentence_tokens = [sent for sent in doc.sents]

    sentence_score = {}
    for sent in sentence_tokens:  # create a dictionary for sen tokens
        for word in doc:
            if word.text.lower() in word_frequencies.keys():
                if sent not in sentence_score.keys():
                    sentence_score[sent] = word_frequencies[word.text.lower()]
                else:
                    sentence_score[sent] += word_frequencies[word.text.lower()]

    select_length = int(len(sentence_tokens)*0.05)
    summary = nlargest(select_length, sentence_score, key=sentence_score.get)
    final_summary = [word.text for word in summary]
    summary = ' '.join(final_summary)
    return summary


def fileRead(file_p, topic):  # read the file and save it to csv file
    t = ''
    global cnt
    with open(file_p, 'r') as f:
        data = f.read()
        tree = ET.parse(file_p)
        try:
            headline_tag = tree.getroot().find('HEADLINE')
            headline = remove_slash_n(headline_tag.text)
        except:
            headline = None
        try:
            date_line_tag = tree.getroot().find('DATELINE')
            date_line = remove_slash_n(date_line_tag.text)
        except:
            date_line = ' '
        paragraphs = [remove_slash_n(p.text)
                      for p in tree.getroot().find('TEXT').findall('P')]
        text = ' '.join(paragraphs)
        cnt = len(text)
        m = cosine_similarity(text)  # call the cosine similarity function
        print('Cosine Similarity :'+str(m))

        if m > 0.8:
            g = 'Similarity found'
            print(g)
        else:
            g = 'No Similarity found'
            print(g)
            t += text
            print(topic)
            new_docs['topic'].append(topic)
            new_docs['file'].append(file_p)
            new_docs['text'].append(text)
            new_docs['cnt'].append(cnt)
            summarized_df = pd.DataFrame(data=new_docs)
            summarized_df.to_csv('summarized.csv', index=False)
    return t


def getSummery2(t):  # joint the text of all the files and Summarize it and save it to csv file
    msg = ''
    global topic
    global cnt, cnt2
    docs['topic'].append(topic)
    docs['text'].append(t)
    cnt = len(t)
    msg = getSummary(t)

    docs['summary'].append(msg)
    summarized_df_new = pd.DataFrame(data=docs)
    summarized_df_new.to_csv('summarized_new.csv', index=False)
    return msg


# @app.route('/filee', methods=['GET', 'POST'])
def filee():  # get how many files to upload
    global num
    if request.method == 'POST':
        num = request.form['num']
        if num is None:
            num = 2
        else:
            num = int(num)
        num = int(num)
        return render_template('file_upload.html', num=num)


# @app.route('/fileu', methods=['GET', 'POST'])
def file():  # upload files
    global topic
    global num
    c = ''
    m = ''
    msg = ''
    target = os.path.join(os.getcwd(), 'files/')
    if not os.path.isdir(target):
        os.mkdir(target)
    if request.method == 'POST':
        topic = request.form['topic']
        num = int(num)
        for i in range(0, num):

            file = request.files['file'+str(i)]
            filename = secure_filename(file.filename)
            destination = "/".join([target, filename])
            file.save(destination)
            file_p = destination
            # read files and save the text of all files in c
            c += fileRead(file_p, topic)
            if c == '':
                m = " Similer Document Found"
            else:
                msg = getSummery2(c)

    return render_template('file_upload.html', m=m, msg=msg, num=num)
