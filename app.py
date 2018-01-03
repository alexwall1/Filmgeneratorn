# -*- coding: UTF-8 -*- 

from flask import Flask,render_template
from flask import g
import markovify
import random
import json
import os

app=Flask(__name__)

def load_model_json():
	CURRENT_FILE=os.path.abspath(__file__)
	CURRENT_DIR=os.path.dirname(CURRENT_FILE)
	with open(CURRENT_DIR + '/model.json','r') as json_file:
		model_json=json.load(json_file)
		return model_json

def generate_movie():
	model_json=load_model_json()
	model=markovify.Text.from_dict(model_json,retain_original=False)
	plot=model.make_sentence_with_start("En film")
	title=model.make_short_sentence(40)
	return plot,title

@app.route('/')
def index():
	plot,title=generate_movie()
	if not plot or not title:
		return render_template('error.html')
	year=random.randint(1985,1995)
	genre=['Komedi','Skräck','Romantik','Erotik','Thriller','Dokumentär'][random.randint(0,5)].decode('utf-8')
	rating="%.1f" % random.uniform(0,2)
	return render_template('base.html',genre=genre,year=year,title=title.replace('.',''),rating=rating,plot=plot)
