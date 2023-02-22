import math
import os
import string
import xml.etree.ElementTree as ET
from heapq import nlargest
from string import punctuation

import chardet
import nltk.data
import pandas as pd
import spacy
from bangla_stemmer.stemmer.stemmer import BanglaStemmer
from bnlp import NLTKTokenizer
from bnlp.corpus import digits, punctuations, stopwords
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from nltk import tokenize
from spacy.lang.en.stop_words import STOP_WORDS
from werkzeug.utils import secure_filename

from update_summarizer import db
from update_summarizer.main.cosine import cosine_similarity
from update_summarizer.main.utils import web_scrap_return_text

nlp = spacy.load('en_core_web_sm')

stopwords = list(STOP_WORDS)

import nltk

nltk.download("punkt")
nltk.download("stopwords")

from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize

main = Blueprint("main", __name__)

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

def get_summary_link(text):

    bnltk = NLTKTokenizer()
    text_sentences=bnltk.sentence_tokenize(text)
    sentence_count = len(text_sentences)
    wordFrequencyAllSentences = {} #dictionary to store dictionary of  sentences and wordFrequencyPerSentence
    TFwordAllSentences = {} #dictionary to store dictionary of  sentences and TFWordPerSentence

    for sentence in text_sentences:
        word_list=bnltk.word_tokenize(sentence)
        # pre-processing
        word_list=BanglaStemmer().stem(word_list) # word stemming
        word_list=[word for word in word_list if word not in punctuations] # removing punctuations
        word_list=[word for word in word_list if word not in stopwords] # removing stopwords
        word_list=[word for word in word_list if word not in digits] # removing digits
        #calculating word frequency
        wordFrequencyPerSentence = {} # dictionary to store word and its count
    
    for sentence in text_sentences:
        for word in word_list:        
            wordFrequencyPerSentence[word]=word_list.count(word) # repeating words will just overwrite the count of words so no problem
            #print(wordFrequencyPerSentence[word])
            wordFrequencyAllSentences[sentence] = wordFrequencyPerSentence
            #print(wordFrequencyAllSentences)
        
        #calculating TF

        TFWordPerSentence = {} # dictionary to store word and TF(word)
        for word in word_list:        
            TFWordPerSentence[word]=word_list.count(word) / len(word_list)
            TFwordAllSentences[sentence] = TFWordPerSentence

        #create a matrix of sentences and words
    
    termFrequencyMatrix = wordFrequencyAllSentences; 
    
    #counting word frequency in all sentences
    allWords=bnltk.word_tokenize(text)
    allWords=BanglaStemmer().stem(allWords) # word stemming
    allWords=[word for word in allWords if word not in punctuations] # removing punctuations
    allWords=[word for word in allWords if word not in stopwords] # removing stopwords
    allWords=[word for word in allWords if word not in digits] # removing digits

    allWords=set(allWords) # getting unique words in text

    word_count= dict()
    for word in allWords:
        count=0
        for sentence in text_sentences:
            if(word in sentence): # check if word is present in sentence            
                count=count+1 # count sentene
        word_count[word]=count

    #calculating IDF
    IDFwordsAllSentences = {} #dictionary to store dictionary of  sentences and IDFwordPerSentence

    totalSentences=len(text_sentences) ## for using in formula

    for sentence in text_sentences:
        IDFwordPerSentence = {} # dictionary to store word and its IDF
        
        for word in word_list:
            if(word_count[word]==0):
                pass
            else:
                IDFwordPerSentence[word]= math.log10(totalSentences / word_count[word]) # repeating words will just overwrite the count of words so no problem
                IDFwordsAllSentences[sentence] = IDFwordPerSentence

    #calculating TF-IDF for each word in each sentence
    TF_IFDwordAllSentences=TFwordAllSentences

    for key1, value1 in TFwordAllSentences.items():
            #print(key1)
            #print(value1)
            for key2, value2 in value1.items():
                TF_IFDwordAllSentences[key1][key2]=TFwordAllSentences[key1][key2] * IDFwordsAllSentences[key1][key2]
                #print(value2)
                break

    #calculating weight of each sentence
    weight_sentences={} # for storing weights of all sentences

    for key1, value1 in TF_IFDwordAllSentences.items():
        x=0 # initial score for a sentence
        for key2, value2 in value1.items():
            x=x+TF_IFDwordAllSentences[key1][key2] # weight of a sentence is the sum of tf_idf / length of sentence
        weight_sentences[key1]=x / len(key1)

    #calculating threshold
    averageSentenceWeight = sum(list(weight_sentences.values())) / len(weight_sentences)

    #generating summary
    summary=''
    for key, value in weight_sentences.items():
        if(value > averageSentenceWeight):
            summary=summary+key+' '
    
    return summary


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

    select_length = int(len(sentence_tokens)*0.1 if num == 0 else 0.05)
    summary = nlargest(select_length, sentence_score, key=sentence_score.get)
    final_summary = [word.text for word in summary]
    summary = ' '.join(final_summary)
    return summary

df=pd.read_csv('merged2.csv')

@main.route("/summary-text", methods=["POST"])
@login_required
def summary_text():
    profile = current_user.profile
    if profile.summary_left == 0:
        flash('You have 0 summary token left. Come back tomorrow.', 'danger')
        return redirect(url_for('main.homepage'))
    
    summary=''
    if request.method=="POST":
        text = request.form['text']
        

        #print(text)
        num=1
        summary=df['text'][0]

        #summary =getSummary(text)
        #print(summary)
        profile.summary_left = profile.summary_left - 1
        db.session.commit()
    return redirect(url_for('main.summarizer', text=text))
         



def fileRead(file_p, topic):  # read the file and save it to csv file
    t = ''
    global cnt
    with open(file_p, 'r') as f:
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
        else:
            g = 'No Similarity found'
            t += text
            new_docs['topic'].append(topic)
            new_docs['file'].append(file_p)
            new_docs['text'].append(text)
            new_docs['cnt'].append(cnt)
            summarized_df = pd.DataFrame(data=new_docs)
            summarized_df.to_csv('summarized.csv', index=False)
    return t


# joint the text of all the files and Summarize it and save it to csv file
def getSummery2(file_p, t):
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
    try:
        os.unlink(file_p)
    except Exception as e:
        print(e)
    return msg


@main.route("/", methods=["GET"])
def homepage():
    return render_template("main/homepage.html")


@main.route("/premium", methods=["GET"])
def premium():
    return render_template("main/premium.html")


@main.route("/subscription-pack", methods=["GET"])
def subscription_pack():
    return render_template("main/subscription_pack.html")


@main.route("/about-us", methods=["GET"])
def about_us():
    return render_template("main/about_us.html")


@main.route("/help", methods=["GET"])
def help():
    return render_template("main/help.html")

@main.route("/summary-file", methods=["POST"])
@login_required
def link_summary():
    links = request.form
    text = ''
    m = ''
    msg = ''

    if len(links) == 0:
        return redirect(url_for('main.homepage'))

    for i in range(1, len(links)+1):
        temp = web_scrap_return_text(request.form.get(f'link-input-{i}'))
        text += (' ' + temp)
    
    msg = get_summary_link(text)
    
    return redirect(url_for('main.summarizer', m=m, msg=msg))


@main.route("/summary-file", methods=["POST"])
@login_required
def file_upload():
    profile = current_user.profile
    if profile.summary_left == 0:
        flash('You have 0 summary token left. Come back tomorrow.', 'danger')
        return redirect(url_for('main.homepage'))

    global topic
    global num
    c = ''
    m = ''
    msg = ''
    target = os.path.join(os.getcwd(), 'files/')
    if not os.path.isdir(target):
        os.mkdir(target)
    topic = request.form.get('topic')
    number = request.form.get('file-count')
    for i in range(1, int(number)+1):
        file = request.files.get(f'file-input-{i}')
        filename = secure_filename(file.filename)
        destination = "/".join([target, filename])
        
        file.save(destination)
        file_p = destination
        # read files and save the text of all files in c
        print('file_p: ', file_p)
        c += fileRead(file_p, topic)
        if c == '':
            m = "Similer Document Found"
        else:
            msg = getSummery2(file_p, c)
            profile.summary_left = profile.summary_left - 1
            db.session.commit()

    return redirect(url_for('main.summarizer', m=m, msg=msg))


@main.route("/summary-generate", methods=["GET"])
def summarizer():
    summary = request.args.get('text')

    if summary == '':
        flash('Enter text first', category='danger')
    else:
        summary = df['text'][0]
    m = request.args.get('m')
    msg = request.args.get('msg')
    if m:
        flash(m, category='primary')

    
    return render_template("main/homepage.html", msg=msg,summary=summary)