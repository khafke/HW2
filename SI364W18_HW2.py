## SI 364
## Winter 2018
## HW 2 - Part 1

## This homework has 3 parts, all of which should be completed inside this file (and a little bit inside the /templates directory).

## Add view functions and any other necessary code to this Flask application code below so that the routes described in the README exist and render the templates they are supposed to (all templates provided are inside the templates/ directory, where they should stay).

## As part of the homework, you may also need to add templates (new .html files) to the templates directory.

#############################
##### IMPORT STATEMENTS #####
#############################
from flask import Flask, request, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import Form, StringField, SubmitField, RadioField, ValidationError
from wtforms.validators import DataRequired
import requests
import json

#####################
##### APP SETUP #####
#####################

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hardtoguessstring'

####################
###### FORMS #######
####################

class AlbumEntryForm(FlaskForm):
    album_name = StringField('Enter the name of an album', validators=[DataRequired()])
    album_rank = RadioField('How much do you like this album? (1 low, 3 high)', choices=[('1','1'), ('2','2'), ('3','3')], validators=[DataRequired()])
    submit = SubmitField("Sumbit")

####################
###### ROUTES ######
####################

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/user/<name>')
def hello_user(name):
    return '<h1>Hello {0}<h1>'.format(name)

#artist form

@app.route('/artistform')
def artist_form():
    return render_template('artistform.html')

#artist info

@app.route('/artistinfo',methods=["GET"])
def artist_info():
    artist = (request.args['artist'])
    url = "https://itunes.apple.com/search?term={}".format(artist)
    response = requests.get(url)
    responsejson = response.json()
    objects = (responsejson['results'])
    return render_template('artist_info.html', objects=objects)

#artist links

@app.route('/artistlinks')
def artist_links():
    return render_template('artist_links.html')

#specific artist

@app.route('/specific/song/<artist_name>')
def specific_artist(artist_name):
    url = "https://itunes.apple.com/search?term={}".format(artist_name)
    response = requests.get(url)
    responsejson = response.json()
    results = (responsejson['results'])
    return render_template('specific_artist.html', results=results)

#album entry

@app.route('/album_entry')
def album_entry():
    form_var = AlbumEntryForm()
    return render_template('album_entry.html',form=form_var)

#album_result

@app.route('/album_result', methods=['POST'])
def album_result():
    form = AlbumEntryForm()
    if form.validate_on_submit():
        name = form.album_name.data
        rank = form.album_rank.data
        return render_template('album_data.html', album_name = name, album_rank = rank)
    return "Sorry, no data available."



if __name__ == '__main__':
    app.run(use_reloader=True,debug=True)
