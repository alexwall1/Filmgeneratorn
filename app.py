# -*- coding: UTF-8 -*- 

from flask import Flask,render_template
from flask import g
import csv
import markovify
import random

app=Flask(__name__)

def get_corpus():
	corpus=getattr(g,'_corpus',None)
	if corpus is None:
		with open('FilmReg85_95_utf8.csv','r') as csv_file:
			reader=csv.reader(csv_file,delimiter=',')
			corpus=[]
			for row in reader:
				if row[52]=='Spelfilm' and row[53]=='Långfilm' and row[56]:
					corpus.append(row[56])
		g._corpus=corpus
	return corpus

def generate_movie():
	corpus=getattr(g,'_corpus',None)
	if corpus is None:
		corpus=get_corpus()
	text_model=markovify.Text(corpus,retain_original=False)
	plot=text_model.make_sentence_with_start("En film")
	title=text_model.make_short_sentence(40)
	return plot,title

@app.route('/')
def index():
	plot,title=generate_movie()
	if not plot or not title:
		return render_template('error.html')
	year=random.randint(1985,1995)
	genre=['Komedi','Skräck','Romantik','Erotik','Thriller','Dokumentär'][random.randint(0,5)].decode('utf-8')
	rating="%.1f" % random.uniform(0,2)
	return render_template('base.html',genre=genre,year=year,title=title.replace('.','').decode('utf-8'),rating=rating,plot=plot.decode('utf-8'))
