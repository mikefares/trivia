#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json, sys
from time import timezone
from unicodedata import name
from urllib import response
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, abort
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
import collections
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# TODO: connect to a local postgresql database
collections.Callable = collections.abc.Callable
#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    num_upcoming_shows = db.Column(db.Integer)
    num_past_shows = db.Column(db.Integer)
    website_link = db.Column(db.String(500))
    seeking_talent = db.Column(db.String(120))
    seeking_description = db.Column(db.String(120))
    shows = db.relationship('Show', backref='Venue', lazy=True)

    def __repr__(self):
      return f'<Venue {self.id}, {self.name}, {self.city}, {self.state}, {self.address}, {self.phone}, {self.genres}, {self.image_link}, {self.facebook_link}, {self.num_upcoming_shows} ,{self.num_past_shows}, {self.website_link}, {self.seeking_talent}, {self.seeking_description}>'

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    num_upcoming_shows = db.Column(db.Integer)
    num_past_shows = db.Column(db.Integer)
    website_link = db.Column(db.String(500))
    seeking_venue = db.Column(db.String(120))
    seeking_description = db.Column(db.String(120))
    shows = db.relationship('Show', backref='Artist', lazy=True)

    def __repr__(self):
      return f'<Venue {self.id}, {self.name}, {self.city}, {self.state}, {self.phone}, {self.genres}, {self.image_link}, {self.facebook_link}, {self.num_upcoming_shows} ,{self.num_past_shows}, {self.website_link}, {self.seeking_venue} ,{self.seeking_description}>'

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

class Show(db.Model):
  __tablename__ = 'Show'

  venue_id = db.Column(db.Integer, db.ForeignKey(Venue.id), primary_key = True)
  artist_id = db.Column(db.Integer, db.ForeignKey(Artist.id), primary_key = True)
  start_time = db.Column(db.DateTime(timezone=True))

  def __repr__(self):
    return f'<Show {self.venue_id}, {self.artist_id}, {self.start_time}>'
#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

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
  # TODO: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
# try:
#     allArtists = Artist.query.all()

#     data = []
#     for allArtist in allArtists:
#       data.append({
#         "id": allArtist.id,
#         "name": allArtist.name
#       })
#   except:
#     print(sys.exc_info())

#   return render_template('pages/artists.html', artists=data)

  try:
    allVenues = Venue.query.order_by('id').all()
    upcoming = Venue.query.join(Show).filter(Show.start_time > datetime.now()).count()

    data = []
    for allVenue in allVenues:
      data += [{"city": allVenue.city,
        "state": allVenue.state,
        "venues": [{
          "id": allVenue.id,
          "name": allVenue.name,
          "upcoming_shows": upcoming
        }]
      }]
  except:
    print(sys.exc_info())

  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on venues with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  # response={
  #   "count": 1,
  #   "data": [{
  #     "id": 2,
  #     "name": "The Dueling Pianos Bar",
  #     "num_upcoming_shows": 0,
  #   }]
  # }
  search_term = request.form.get('search_term', '')
  word = format(search_term.lower())

  key = '%{}%'.format(word)
  results = Venue.query.filter(Venue.name.ilike(key) | Venue.state.ilike(key) | Venue.city.ilike(key)).all()

  response={
    "count": len(results),
    "data": results
  }

  return render_template('pages/search_venues.html', results=response, search_term=search_term)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id

  all_venues = Venue.query.filter_by(id=venue_id).first()

  
  query_upcoming_show = db.session.query(Show.start_time, Artist.id, Artist.name, Artist.image_link).join(Venue,Artist).filter(Show.start_time > datetime.today(), Show.venue_id == all_venues.id).all() 
  query_past_show = db.session.query(Show.start_time, Artist.id, Artist.name, Artist.image_link).join(Venue,Artist).filter(Show.start_time < datetime.today(), Show.venue_id == all_venues.id).all() 

  upcoming_shows = []
  for start_time, artist_id, artist_name, image_link in query_upcoming_show:
    upcoming_shows += [{
      "artist_id": artist_id,
      "artist_name": artist_name,
      "artist_image_link": image_link,
      "start_time": format_datetime(str(start_time))
    }]

  
  past_shows = []
  for start_time, artist_id, artist_name, image_link in query_past_show:
    past_shows += [{
      "artist_id": artist_id,
      "artist_name": artist_name,
      "artist_image_link": image_link,
      "start_time": format_datetime(str(start_time))
    }]



  data={
    "id": all_venues.id,
    "name": all_venues.name,
    "genres": all_venues.genres.split(","),
    "city": all_venues.city,
    "state": all_venues.state,
    "address": all_venues.address,
    "phone": all_venues.phone,
    "website_link": all_venues.website_link,
    "facebook_link": all_venues.facebook_link,
    "seeking_talent": all_venues.seeking_talent,
    "seeking_description": all_venues.seeking_description,
    "image_link": all_venues.image_link,
    "past_shows_count": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows)
  }

 
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  form = VenueForm(request.form)

  if form.validate():
    try:
      name = request.form.get('name')
      city = request.form.get('city') 
      state = request.form.get('state')
      address = request.form.get('address')
      phone = request.form.get('phone')
      genres = request.form.get('genres')
      image_link =request.form.get('image_link')
      facebook_link = request.form.get('facebook_link') 
      website_link = request.form.get('website_link')
      seeking_talent = request.form.get('seeking_talent') 
      seeking_description = request.form.get('seeking_description')

      venue = Venue (name=name, city=city, state=state, address=address, phone=phone, genres=genres, image_link=image_link, facebook_link=facebook_link, website_link=website_link, seeking_talent=seeking_talent, seeking_description=seeking_description)
      db.session.add(venue)
      db.session.commit()

    # on successful db insert, flash success
      flash('Venue ' + request.form['name'] + ' was successfully listed!')
    # TODO: on unsuccessful db insert, flash an error instead.
    except:
      db.session.rollback()
      flash('An error occurred. Venue ' + venue.name + ' could not be listed.')
    # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    finally:
      db.session.close()
  else:
    for field, error_message in form.errors.items():
      flash("The " + field + " field has an error: " + str(error_message) )

  return render_template('pages/home.html')


# Delete Venue
# --------------------------------------------------------------------
@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  try:
    delete_venue = Venue.query.get(venue_id)
    db.session.delete(delete_venue)
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return redirect(url_for('venues'))

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database

  try:
    allArtists = Artist.query.all()

    data = []
    for allArtist in allArtists:
      data.append({
        "id": allArtist.id,
        "name": allArtist.name
      })
  except:
    print(sys.exc_info())

  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
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

  search_term = request.form.get('search_term', '')
  word = format(search_term.lower())

  key = '%{}%'.format(word)
  results = Artist.query.filter(Artist.name.ilike(key) | Artist.city.ilike(key) | Artist.state.ilike(key)).all()

  response={
    "count": len(results),
    "data": results
  }

  return render_template('pages/search_artists.html', results=response, search_term=search_term)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
  
    
  all_artist = Artist.query.filter_by(id=artist_id).first()

  upcoming_show_query = db.session.query(Show.start_time, Artist.id, Artist.name, Artist.image_link).join(Venue,Artist).filter(Show.start_time > datetime.today(), Show.venue_id == all_artist.id).all() 
  past_show_query = db.session.query(Show.start_time, Artist.id, Artist.name, Artist.image_link).join(Venue,Artist).filter(Show.start_time < datetime.today(), Show.venue_id == all_artist.id).all() 

  upcoming_shows = []
  for start_time, venue_id, venue_name, image_link in upcoming_show_query:
    upcoming_shows += ({
        "venue_id": venue_id,
        "venue_name": venue_name,
        "venue_image_link": image_link,
        "start_time": format_datetime(str(start_time))
      })

  past_shows = []
  for start_time, venue_id, venue_name, image_link in past_show_query:
    past_shows += ({
        "venue_id": venue_id,
        "venue_name": venue_name,
        "venue_image_link": image_link,
        "start_time": format_datetime(str(start_time))
      })


  data={
    "id": artist_id,
    "name": all_artist.name,
    "genres": all_artist.genres.split(","),
    "city": all_artist.city,
    "state": all_artist.state,
    "phone": all_artist.phone,
    "website_link": all_artist.website_link,
    "facebook_link": all_artist.facebook_link,
    "seeking_venue": all_artist.seeking_venue,
    "seeking_description": all_artist.seeking_description,
    "image_link": all_artist.image_link,
    "past_shows_count": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows)
  }
  
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  artist = Artist.query.get_or_404(artist_id)
  form = ArtistForm(obj=artist)
  
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):

  artist_update = Artist.query.get(artist_id)
  try:
    artist_update.name = request.form.get('name')
    artist_update.city = request.form.get('city') 
    artist_update.state = request.form.get('state')
    artist_update.phone = request.form.get('phone')
    artist_update.genres = request.form.get('genres')
    artist_update.image_link =request.form.get('image_link')
    artist_update.facebook_link = request.form.get('facebook_link') 
    artist_update.website_link = request.form.get('website_link')
    artist_update.seeking_venue = request.form.get('seeking_venue') 
    artist_update.seeking_description = request.form.get('seeking_description')
    db.session.commit()

    flash(artist_update.name + "'s details successfully updated")

  except:
    db.session.rollback()
    flash('An error occured, ' + artist_update.name + "'s details update was unsuccessful")
  finally:
    db.session.close()
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  venue = Venue.query.get_or_404(venue_id)
  form = VenueForm(obj=venue)
  
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  venue_update = Venue.query.get(venue_id)
  try:
    venue_update.name = request.form.get('name')
    venue_update.city = request.form.get('city') 
    venue_update.state = request.form.get('state')
    venue_update.address = request.form.get('address')
    venue_update.phone = request.form.get('phone')
    venue_update.genres = request.form.get('genres')
    venue_update.image_link =request.form.get('image_link')
    venue_update.facebook_link = request.form.get('facebook_link') 
    venue_update.website_link = request.form.get('website_link')
    venue_update.seeking_talent = request.form.get('seeking_talent') 
    venue_update.seeking_description = request.form.get('seeking_description')

    db.session.commit()
    flash(venue_update.name + "'s details successfully updated")
  except:
    db.session.rollback()
    flash('An error occured, ' + venue_update.name + "'s details update was unsuccessful")

  finally:
    db.session.close()

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
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  form = ArtistForm(request.form)
  
  if form.validate():
    try:
      name = request.form.get('name')
      city = request.form.get('city') 
      state = request.form.get('state')
      phone = request.form.get('phone')
      genres = request.form.get('genres')
      image_link =request.form.get('image_link')
      facebook_link = request.form.get('facebook_link') 
      website_link = request.form.get('website_link')
      seeking_venue = request.form.get('seeking_venue') 
      seeking_description = request.form.get('seeking_description')

      artist = Artist(name=name, city=city, state=state, phone=phone, genres=genres, image_link=image_link, facebook_link=facebook_link, website_link=website_link, seeking_venue=seeking_venue, seeking_description=seeking_description)
      db.session.add(artist)
      db.session.commit()
    # on successful db insert, flash success
      flash('Venue ' + request.form['name'] + ' was successfully listed!')
    # TODO: on unsuccessful db insert, flash an error instead.
    except:
      db.session.rollback()
      flash('An error occurred. Venue ' + artist.name + ' could not be listed.')
    # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    finally:
      db.session.close()
  else:
    for field, error_message in form.errors.items():
      flash("The " + field + " field has an error: " + str(error_message) )

  return render_template('pages/home.html')



#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  
  
  allShow = Show.query.all()
  data = []
  for show in allShow:
    artist = db.session.query(Artist.name, Artist.image_link).filter(Artist.id == show.artist_id).one()
    venue = db.session.query(Venue.name).filter(Venue.id == show.venue_id).one()
    data += [{
      "venue_id": show.venue_id,
      "venue_name": venue.name,
      "artist_id": show.artist_id,
      "artist_name": artist.name,
      "artist_image_link": artist.image_link,
      "start_time": format_datetime(str(show.start_time))
    }]

  return render_template('pages/shows.html', shows=data)  
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


@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  form = ShowForm(request.form)
  error = False

  if form.validate():
    try:
      artist_id = request.form.get('artist_id')
      venue_id = request.form.get('venue_id')
      start_time = request.form.get('start_time')

      show = Show(artist_id=artist_id, venue_id=venue_id, start_time=start_time)
      db.session.add(show)
      db.session.commit()
      
    # on successful db insert, flash success
      flash('Show was successfully listed!')
    except: 
      error = True
      db.session.rollback()
      flash('An error occurred. Show could not be listed.')
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    finally:
      db.session.close()
  else:
    abort (400)
    
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
