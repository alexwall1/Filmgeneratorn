# -*- coding: UTF-8 -*- 

from flask import Flask,render_template,session
from flask import g
import markovify
import random
import json
import os
import sqlite3
import os

CURRENT_FILE=os.path.abspath(__file__)
CURRENT_DIR=os.path.dirname(CURRENT_FILE)
DATABASE=CURRENT_DIR+'/movies.db'

app=Flask(__name__)
app.secret_key=os.urandom(24)

def get_db():
	db=getattr(g,'_database',None)
	if db is None:
		db=g._database=sqlite3.connect(DATABASE)
	return db

@app.teardown_appcontext
def close_connection(exception):
	db=getattr(g,'_database',None)
	if db is not None:
		db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def load_model_json():
	with open(CURRENT_DIR + '/model.json','r') as json_file:
		model_json=json.load(json_file)
		return model_json

def generate_movie():
	model_json=load_model_json()
	model=markovify.Text.from_dict(model_json,retain_original=False)
	movie={}
	movie['plot']=model.make_sentence_with_start("En film")
	title=model.make_short_sentence(40)
	if movie['plot'] is None or title is None:
		raise Exception('Generator did not finish')
	movie['title']=title.replace('.','')
	movie['genre']=['Komedi','Skräck','Romantik','Erotik','Thriller','Dokumentär'][random.randint(0,5)].decode('utf-8')
	return movie

def save_movie_to_db(movie):
	cur=get_db()
	if 'id' in movie:
		query="update movie set rating = rating + 1 where id = ?"
		cur.execute(query,(str(movie['id'])))
	else:
		query="insert into movie (title,plot,genre) values (?,?,?)"
		cur.execute(query,(movie['title'],movie['plot'],movie['genre']))
	cur.commit()
	cur.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.route('/like',methods=['POST'])
def like():
	save_movie_to_db(session['latest_movie'])
	return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 
	
@app.route('/')
def index():
	try:
		if random.random()>0.5:
			movie=generate_movie()
		else:
			random_movie=query_db('select * from movie order by rating * random() limit 1', one=True)
			movie={'id':random_movie[0],'title':random_movie[1],'plot':random_movie[2],'genre':random_movie[3]}
		session['latest_movie']=movie
		return render_template('base.html',movie=movie)
	except:
		return render_template('error.html')
