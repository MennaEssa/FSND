#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for , abort , jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from sys import exc_info;
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

# TODO_DONE: connect to a local postgresql database
migrate = Migrate(app , db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    # TODO_DONE: implement any missing fields, as a database migration using Flask-Migrate
    #refering to same elements used in show_venue.html
    #past_shows_count and upcoming_shows will be calculated at the route
    genres = db.Column(db.String(120))
    website = db.Column(db.String())
    seeking_talent = db.Column(db.Boolean , default=False)
    seeking_description = db.Column(db.String())
    shows = db.relationship('Show', backref='venue', lazy=True , passive_deletes=True)


class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    # TODO_DONE : implement any missing fields, as a database migration using Flask-Migrate 
    #essentially very similar to venues model
    website = db.Column(db.String())
    seeking_venue = db.Column(db.Boolean , default=False)
    seeking_description = db.Column(db.String())
    shows = db.relationship('Show', backref='artist', lazy=True , passive_deletes=True)


class Show(db.Model):
  __tablename__ = 'show'
  # TODO_DONE Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
  artist_id = db.Column( db.Integer , db.ForeignKey('artist.id' , ondelete='CASCADE' ) , nullable=False , primary_key=True)
  venue_id = db.Column( db.Integer , db.ForeignKey('venue.id' , ondelete='CASCADE') , nullable = False , primary_key=True)
  start_time = db.Column(db.DateTime , nullable=False)

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO_DONE: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  # data=[{
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "venues": [{
  #     "id": 1,
  #     "name": "The Musical Hop",
  #     "num_upcoming_shows": 0,
  #   }, {
  #     "id": 3,
  #     "name": "Park Square Live Music & Coffee",
  #     "num_upcoming_shows": 1,
  #   }]
  # }, {
  #   "city": "New York",
  #   "state": "NY",
  #   "venues": [{
  #     "id": 2,
  #     "name": "The Dueling Pianos Bar",
  #     "num_upcoming_shows": 0,
  #   }]
  # }]
  data=[]

  try:
    #get all distinct locations
    locations = db.session.query(Venue.city , Venue.state ).group_by(Venue.city , Venue.state).all()

    #get venues for specific location
    for city,state in locations :

      venues_list=[]
      location_venues=Venue.query.filter(Venue.city==city , Venue.state == state).all()
      print(location_venues)

      for location_venue in location_venues:
        n_upcoming_shows = Show.query.filter(Show.venue_id == location_venue.id , Show.start_time > datetime.now()).count()
        venues_dict = {
          "id" : location_venue.id,
          "name" : location_venue.name,
          "num_upcoming_shows" : n_upcoming_shows
        }
        venues_list.append(venues_dict)

      data.append({
        "city" : city,
        "state" : state,
        "venues" : venues_list
      })

  except:
    print(exc_info())
    abort(500)

  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO_DONE: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  try:
    search_term = request.form.get('search_term', '')
    search_result = Venue.query.filter( Venue.name.ilike("%"+search_term+"%")).all()
    response_data=[]
    for result in search_result:
      response_data.append( {
        "id": result.id,
        "name" : result.name,
        "num_upcoming_shows": Show.query.filter(Show.venue_id == result.id , Show.start_time > datetime.now()).count()
      })

    response={
    "count": len(search_result),
    "data": response_data
    }
  except:
    print(exc_info())
    abort(500)

  
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO_DONE: replace with real venue data from the venues table, using venue_id
  # data3={
  #   "id": 3,
  #   "name": "Park Square Live Music & Coffee",
  #   "genres": ["Rock n Roll", "Jazz", "Classical", "Folk"],
  #   "address": "34 Whiskey Moore Ave",
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "415-000-1234",
  #   "website": "https://www.parksquarelivemusicandcoffee.com",
  #   "facebook_link": "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
  #   "seeking_talent": False,
  #   "image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #   "past_shows": [{
  #     "artist_id": 5,
  #     "artist_name": "Matt Quevedo",
  #     "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
  #     "start_time": "2019-06-15T23:00:00.000Z"
  #   }],
  #   "upcoming_shows": [{
  #     "artist_id": 6,
  #     "artist_name": "The Wild Sax Band",
  #     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #     "start_time": "2035-04-01T20:00:00.000Z"
  #   }, {
  #     "artist_id": 6,
  #     "artist_name": "The Wild Sax Band",
  #     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #     "start_time": "2035-04-08T20:00:00.000Z"
  #   }, {
  #     "artist_id": 6,
  #     "artist_name": "The Wild Sax Band",
  #     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #     "start_time": "2035-04-15T20:00:00.000Z"
  #   }],
  #   "past_shows_count": 1,
  #   "upcoming_shows_count": 1,
  # }
  #data = list(filter(lambda d: d['id'] == venue_id, [data1, data2, data3]))[0]
  data={}
  try:
    #return a list of tuples of the (Venue  , show object) since the venue is the same in all entries , I will use the first one to
    #populate artist info.
    join_venues_shows = db.session.query(Venue, Show).outerjoin(Show, Venue.id == Show.venue_id).filter(Venue.id == venue_id).all()
    venue_info = join_venues_shows[0][0]
    data = { 'id' : venue_info.id,
            'name': venue_info.name,
            'genres' : venue_info.genres.split(','),
            'address' : venue_info.address,
            'city' : venue_info.city,
            'state' : venue_info.state,
            'phone' : venue_info.phone,
            'seeking_talent': venue_info.seeking_talent,
            'seeking_description': venue_info.seeking_description,
            'website' : venue_info.website,
            'facebook_link' : venue_info.facebook_link,
            'image_link' : venue_info.image_link,
            'past_shows' : [],
            'upcoming_shows' : [],
            'past_shows_count' : 0,
            'upcoming_shows_count' : 0
    }

    #populate the shows
    for _,venue_show in join_venues_shows:
      if venue_show is None:
        continue
      show_artist_info = {
          'artist_id' : venue_show.artist.id,
          'artist_name' : venue_show.artist.name,
          'artist_image_link' : venue_show.artist.image_link,
          'start_time': str(venue_show.start_time)
        }
      if venue_show.start_time > datetime.now():
        data['upcoming_shows_count']+=1
        data['upcoming_shows'].append(show_artist_info)
      else:
        data['past_shows_count']+=1
        data['past_shows'].append(show_artist_info)

  except:
    print(exc_info())
    abort(500)

  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  error=False
  venue_form = VenueForm(request.form)

  try:
    new_venue = Venue(
      name = venue_form.name.data ,
      city=venue_form.city.data,
      state = venue_form.state.data,
      phone = venue_form.phone.data,
      image_link = venue_form.image_link.data,
      facebook_link = venue_form.facebook_link.data,
      address = venue_form.address.data,
      #website = venue_form.website.data,
    )
    db.session.add(new_venue)
    db.session.commit()
  except:
    error=True
    db.session.rollback()
    print(exc_info())
  
  finally:
    db.session.close()

  # TODO_DONE: modify data to be the data object returned from db insertion
  if not error:
    # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  else:
    # TODO_DONE: on unsuccessful db insert, flash an error instead.
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO_Done: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  error = False
  try:
    venue= db.session.query(Venue).filter(Venue.id==venue_id).first()
    db.session.delete(venue)
    db.session.commit()
  except:
    print(exc_info())
    error = True
    db.session.rollback()
  finally:
    db.session.close()
  if error:
    flash("Failed to delete venue")
    abort(500)
  return jsonify({'success': False})

  # TODO_DONE BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  # js in statics/js/script.js and button in templates/show_venue.html


#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO_DONE: replace with real data returned from querying the database
  # data=[{
  #   "id": 4,
  #   "name": "Guns N Petals",
  # }, {
  #   "id": 5,
  #   "name": "Matt Quevedo",
  # }, {
  #   "id": 6,
  #   "name": "The Wild Sax Band",
  # }]
  data=[]
  try:
    artists = Artist.query.all()
    for artist in artists:
      data.append({
        "id":artist.id,
        "name": artist.name
      })
  except:
    print(exc_info())
    abort(500)

  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO_DONE: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  # response={
  #   "count": 1,
  #   "data": [{
  #     "id": 4,
  #     "name": "Guns N Petals",
  #     "num_upcoming_shows": 0,
  #   }]
  # }

  try:
    search_term = request.form.get('search_term', '')
    search_result = Artist.query.filter( Artist.name.ilike("%"+search_term+"%")).all()
    response_data=[]
    for result in search_result:
      response_data.append( {
        "id": result.id,
        "name" : result.name,
        "num_upcoming_shows": Show.query.filter(Show.artist_id == result.id , Show.start_time > datetime.now()).count()
      })

    response={
    "count": len(search_result),
    "data": response_data
    }

  except:
    print(exc_info())
    abort(500)
    
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given venue_id
  # TODO_DONE: replace with real artist data from the artist table, using artist_id
  # data1={
  #   "id": 4,
  #   "name": "Guns N Petals",
  #   "genres": ["Rock n Roll"],
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "326-123-5000",
  #   "website": "https://www.gunsnpetalsband.com",
  #   "facebook_link": "https://www.facebook.com/GunsNPetals",
  #   "seeking_venue": True,
  #   "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
  #   "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
  #   "past_shows": [{
  #     "venue_id": 1,
  #     "venue_name": "The Musical Hop",
  #     "venue_image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
  #     "start_time": "2019-05-21T21:30:00.000Z"
  #   }],
  #   "upcoming_shows": [],
  #   "past_shows_count": 1,
  #   "upcoming_shows_count": 0,
  # }
  # data2={
  #   "id": 5,
  #   "name": "Matt Quevedo",
  #   "genres": ["Jazz"],
  #   "city": "New York",
  #   "state": "NY",
  #   "phone": "300-400-5000",
  #   "facebook_link": "https://www.facebook.com/mattquevedo923251523",
  #   "seeking_venue": False,
  #   "image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
  #   "past_shows": [{
  #     "venue_id": 3,
  #     "venue_name": "Park Square Live Music & Coffee",
  #     "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #     "start_time": "2019-06-15T23:00:00.000Z"
  #   }],
  #   "upcoming_shows": [],
  #   "past_shows_count": 1,
  #   "upcoming_shows_count": 0,
  # }
  # data3={
  #   "id": 6,
  #   "name": "The Wild Sax Band",
  #   "genres": ["Jazz", "Classical"],
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "432-325-5432",
  #   "seeking_venue": False,
  #   "image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #   "past_shows": [],
  #   "upcoming_shows": [{
  #     "venue_id": 3,
  #     "venue_name": "Park Square Live Music & Coffee",
  #     "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #     "start_time": "2035-04-01T20:00:00.000Z"
  #   }, {
  #     "venue_id": 3,
  #     "venue_name": "Park Square Live Music & Coffee",
  #     "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #     "start_time": "2035-04-08T20:00:00.000Z"
  #   }, {
  #     "venue_id": 3,
  #     "venue_name": "Park Square Live Music & Coffee",
  #     "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #     "start_time": "2035-04-15T20:00:00.000Z"
  #   }],
  #   "past_shows_count": 0,
  #   "upcoming_shows_count": 3,
  # }
  #data = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]
  data={}
  try:
    #return a list of tuples of the (Artist  , show object) since the arists is the same in all entries , I will use the first one to
    #populate artist info.
    join_artists_shows = db.session.query(Artist, Show).outerjoin(Show, Artist.id == Show.artist_id).filter(Artist.id == artist_id).all()
    artist_info = join_artists_shows[0][0]
    data = { 'id' : artist_info.id,
            'name': artist_info.name,
            'genres' : artist_info.genres.split(','),
            'city' : artist_info.city,
            'state' : artist_info.state,
            'phone' : artist_info.phone,
            'seeking_venue': artist_info.seeking_venue,
            'seeking_description': artist_info.seeking_description,
            'website' : artist_info.website,
            'facebook_link' : artist_info.facebook_link,
            'image_link' : artist_info.image_link,
            'past_shows' : [],
            'upcoming_shows' : [],
            'past_shows_count' : 0,
            'upcoming_shows_count' : 0
    }

    #populate the shows
    for _,artist_show in join_artists_shows:
      if artist_show is None:
        continue
      show_venue_info = {
          'venue_id' : artist_show.venue.id,
          'venue_name' : artist_show.venue.name,
          'venue_image_link' : artist_show.venue.image_link,
          'start_time': str(artist_show.start_time)
        }
      if artist_show.start_time > datetime.now():
        data['upcoming_shows_count']+=1
        data['upcoming_shows'].append(show_venue_info)
      else:
        data['past_shows_count']+=1
        data['past_shows'].append(show_venue_info)

  except:
    print(exc_info())
    abort(500)

  return render_template('pages/show_artist.html', artist=data)


#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  # artist={
  #   "id": 4,
  #   "name": "Guns N Petals",
  #   "genres": ["Rock n Roll"],
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "326-123-5000",
  #   "website": "https://www.gunsnpetalsband.com",
  #   "facebook_link": "https://www.facebook.com/GunsNPetals",
  #   "seeking_venue": True,
  #   "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
  #   "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
  # }
  # TODO_DONE: populate form with fields from artist with ID <artist_id>
  try:
    artist= Artist.query.get(artist_id).__dict__
  except:
    print(exc_info())
    abort(500)
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO_DONE: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  error=False
  try:
    artist_form = ArtistForm(request.form)
    artist = Artist.query.get(artist_id)
    artist.name = artist_form.name.data
    artist.genres = artist_form.genres.data
    artist.city = artist_form.city.data
    artist.state = artist_form.state.data
    artist.phone = artist_form.phone.data
    artist.facebook_link = artist_form.facebook_link.data
    artist.image_link = artist_form.image_link.data
    db.session.add(artist)
    db.session.commit()
  except:
    db.session.rollback()
    flash("failed to update artist's data")
    print(exc_info())
    error=True
  finally:
    db.session.close()

  if error:
    abort(500)
    
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  # venue={
  #   "id": 1,
  #   "name": "The Musical Hop",
  #   "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
  #   "address": "1015 Folsom Street",
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "123-123-1234",
  #   "website": "https://www.themusicalhop.com",
  #   "facebook_link": "https://www.facebook.com/TheMusicalHop",
  #   "seeking_talent": True,
  #   "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
  #   "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
  # }
  # TODO_DONE: populate form with values from venue with ID <venue_id>
  venue= Venue.query.get(venue_id).__dict__
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO_DONE: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  error=False
  try:
    venue_form = VenueForm(request.form)
    venue = Venue.query.get(venue_id)
    venue.name = venue_form.name.data
    venue.genres = venue_form.genres.data
    venue.city = venue_form.city.data
    venue.state = venue_form.state.data
    venue.phone = venue_form.phone.data
    venue.facebook_link = venue_form.facebook_link.data
    venue.image_link = venue_form.image_link.data
    db.session.add(venue)
    db.session.commit()
  except:
    db.session.rollback()
    flash("failed to update venue's data")
    print(exc_info())
    error=True
  finally:
    db.session.close()

  if error:
    abort(500)
    
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO_DONE: insert form data as a new Venue record in the db, instead
  error=False
  try:
    artist_form = ArtistForm(request.form)
    new_artist = Artist(
      name = artist_form.name.data,
      city=artist_form.city.data,
      state = artist_form.state.data,
      phone = artist_form.phone.data,
      image_link = artist_form.image_link.data,
      facebook_link = artist_form.facebook_link.data,
      genres = artist_form.genres.data
    )
    db.session.add(new_artist)
    db.session.commit()
  except:
    error=True
    db.session.rollback()
    print(exc_info())
  
  finally:
    db.session.close()

  # TODO_DONE: modify data to be the data object returned from db insertion
  if not error:
    # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  else:
    # TODO_DONE: on unsuccessful db insert, flash an error instead.
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO_DONE: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  # data=[{
  #   "venue_id": 1,
  #   "venue_name": "The Musical Hop",
  #   "artist_id": 4,
  #   "artist_name": "Guns N Petals",
  #   "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
  #   "start_time": "2019-05-21T21:30:00.000Z"
  # }, {
  #   "venue_id": 3,
  #   "venue_name": "Park Square Live Music & Coffee",
  #   "artist_id": 5,
  #   "artist_name": "Matt Quevedo",
  #   "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
  #   "start_time": "2019-06-15T23:00:00.000Z"
  # }, {
  #   "venue_id": 3,
  #   "venue_name": "Park Square Live Music & Coffee",
  #   "artist_id": 6,
  #   "artist_name": "The Wild Sax Band",
  #   "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #   "start_time": "2035-04-01T20:00:00.000Z"
  # }, {
  #   "venue_id": 3,
  #   "venue_name": "Park Square Live Music & Coffee",
  #   "artist_id": 6,
  #   "artist_name": "The Wild Sax Band",
  #   "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #   "start_time": "2035-04-08T20:00:00.000Z"
  # }, {
  #   "venue_id": 3,
  #   "venue_name": "Park Square Live Music & Coffee",
  #   "artist_id": 6,
  #   "artist_name": "The Wild Sax Band",
  #   "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #   "start_time": "2035-04-15T20:00:00.000Z"
  # }]
  data=[]
  error = False 
  try:
    shows = Show.query.all()
    for show in shows:      
      data.append({'venue_id' : show.venue_id,
                   'artist_id' : show.artist_id,
                   'venue_name' : show.venue.name,
                   'artist_name' : show.artist.name,
                   'start_time' : str(show.start_time)

          })
  except:
    error=True
    abort(500)
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO_DONE: insert form data as a new Show record in the db, instead
  show_form = ShowForm(request.form)
  error=False
  try:
    new_show = Show(artist_id=show_form.artist_id.data ,
                  venue_id = show_form.venue_id.data,
                   start_time = show_form.start_time.data)
    db.session.add(new_show)
    db.session.commit()
  except:
    error=True
    db.session.rollback()
    print(exc_info())
  finally:
    db.session.close()
  if not error:
    # on successful db insert, flash success
    flash('Show was successfully listed!')
  else:
    # TODO_DONE: on unsuccessful db insert, flash an error instead.
    flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
