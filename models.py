from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#Equipos
class Stadiums(db.Model):
	__tablename__ = "stadiums"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50), nullable=False)
	city = db.Column(db.String(20), nullable=False)

class Teams(db.Model):
	__tablename__ = "teams"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50), unique=True)
	id_stadium = db.Column(db.Integer, db.ForeignKey('stadiums.id'))
	stadium = db.relationship('Stadiums', backref=db.backref('teams'))

class Players(db.Model):
	__tablename__ = "players"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20), nullable=False)
	lastname = db.Column(db.String(20), nullable=False)
	number = db.Column(db.Integer, nullable=False)
	id_team = db.Column(db.Integer, db.ForeignKey('teams.id'))
	team = db.relationship('Teams', backref=db.backref('players'))

class GameDate(db.Model):
	__tablename__ = "gamedate"
	id = db.Column(db.Integer, primary_key=True)
	timestamp = db.Column(db.DateTime, default=datetime.now)

class GamePlace(db.Model):
	__tablename__ = "gameplace"
	id = db.Column(db.Integer, primary_key=True)
	id_stadium = db.Column(db.Integer, db.ForeignKey('stadiums.id'))
	stadium = db.relationship('Stadiums', backref=db.backref('game_place'))

class Games(db.Model):
	__tablename__ = "games"
	id = db.Column(db.Integer, primary_key=True)
	id_game_date = db.Column(db.Integer, db.ForeignKey('gamedate.id'))
	id_game_place = db.Column(db.Integer, db.ForeignKey('gameplace.id'))
	id_local_team = db.Column(db.Integer, db.ForeignKey('teams.id'))
	id_visitor_team = db.Column(db.Integer, db.ForeignKey('teams.id'))
	game_date = db.relationship('GameDate', backref=db.backref('gamed'), foreign_keys=[id_game_date])
	game_place = db.relationship('GamePlace', backref=db.backref('gamep'), foreign_keys=[id_game_place])
	
class Positions(db.Model):
	__tablename__ = "positions"
	id = db.Column(db.Integer, primary_key=True)
	id_nombre = db.Column(db.String(15), nullable=False)

class Lineups(db.Model):
	__tablename__ = "lineups"
	id = db.Column(db.Integer, primary_key=True)
	id_game = db.Column(db.Integer, db.ForeignKey('games.id'))
	id_player = db.Column(db.Integer, db.ForeignKey('players.id'))
	id_position = db.Column(db.Integer, db.ForeignKey('positions.id'))
	titular = db.Column(db.Boolean, nullable=False)
	game = db.relationship('Games', backref=db.backref('lineupsg'))
	player = db.relationship('Players', backref=db.backref('lineupsp'))
	position = db.relationship('Positions', backref=db.backref('lineupspo'))
