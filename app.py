from flask import Flask, request, jsonify, abort
from datetime import datetime, timedelta
from models import db, Stadiums, Teams, Players, Games, GameDate, GamePlace, Positions, Lineups
from functools import wraps
import jwt

#Configuracion
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lineups.db'
app.config['SECRET_KEY'] = 'MonasterioJesus2003'
db.init_app(app)

#Rutas
@app.route('/stadiums', methods=['POST'])
def create_stadiums():
	data = request.get_json()
	nuevo_estadio = Stadiums(**data)
	if Stadiums.query.filter_by(name=nuevo_estadio.name).first():
		return jsonify({'error': 'Estadio ya existe'}), 401
	db.session.add(nuevo_estadio)
	db.session.commit()
	return jsonify({'id': nuevo_estadio.id, 'mensaje': 'Guardado exitosamente'}), 201

@app.route('/teams', methods=['POST'])
def create_teams():
	data = request.get_json()
	id_stadium = data.get('id_stadium')
	if Teams.query.filter_by(name=data['name']).first():
		return jsonify({'error': 'Equipo ya existe'}), 401
	id_stadium=Stadiums.query.get(id_stadium)
	if not id_stadium:
		return jsonify({'error': 'stadium_id no existe'}), 404
	nuevo_equipo = Teams(stadium=id_stadium, **data)
	db.session.add(nuevo_equipo)
	db.session.commit()
	return jsonify({'id': nuevo_equipo.id, 'mensaje': 'Guardado exitosamente'}), 201

@app.route('/players', methods=['POST'])
def create_players():
	data = request.get_json()
	id_team = data.get('id_team')
	team = Teams.query.get(id_team)
	if not team:
		return jsonify({'error': 'id_team no existe'}), 404
	nuevo_jugador = Players(team=team, **data)
	db.session.add(nuevo_jugador)
	db.session.commit()
	return jsonify({'id': nuevo_jugador.id, 'mensaje': 'Guardado exitosamente'}), 201

@app.route('/games', methods=['POST'])
def create_games():
	data = request.get_json()
	id_local_team = data.get('id_local_team')
	id_visitor_team = data.get('id_visitor_team')
	if (not Teams.query.get(id_local_team)) or (not Teams.query.get(id_visitor_team)):
		return jsonify({'error': 'Alguno de los equipos no existe'}), 404
	game_date = GameDate(timestamp=datetime.now())
	db.session.add(game_date)
	db.session.commit()
	id_stadium = data.get('id_stadium')
	if not Stadiums.query.get(id_stadium):
		return jsonify({'error': 'stadium_id no existe'}), 404
	nuevo_juego = Games(id_local_team=id_local_team, id_visitor_team=id_visitor_team, id_game_date=game_date.id, id_game_place=id_stadium)
	db.session.add(nuevo_juego)
	db.session.commit()
	return jsonify({'id': nuevo_juego.id, 'mensaje': 'Guardado exitosamente'}), 201

@app.route('/lineups', methods=['POST'])
def create_lineups():
	data = request.get_json()
	id_juego = data.get('id_game')
	id_jugador = data.get('id_player')
	id_posicion = data.get('id_position')
	juego = Games.query.get(id_juego)
	jugador = Players.query.get(id_jugador)
	posicion = Positions(id_nombre=id_posicion)
	db.session.add(posicion)
	db.session.commit()
	if not juego or not jugador or not posicion:
		return jsonify({'error': 'Juego o Jugador o Posicion no existe.'}), 404
	nuevo_lineup = Lineups(game=juego, player=jugador, position=posicion, **data)
	db.session.add(nuevo_lineup)
	db.session.commit()
	return jsonify({'id': nuevo_lineup.id, 'mensaje': 'Guardado exitosamente'}), 201

#Rutas modificar
@app.route('/stadiums/<int:id_stadium>', methods=['PUT'])
def update_stadium(id_stadium):
	estadio = Stadiums.query.get(id_stadium)
	if not estadio:
		return jsonify({'error': 'estadio no existe'}), 404
	data = request.get_json()
	estadio.name = data.get('name', estadio.name)
	estadio.city = data.get('city', estadio.city)
	db.session.commit()
	return jsonify({'mensaje': 'Estadio actualizado'}), 200

@app.route('/teams/<int:id_team>', methods=['PUT'])
def update_team(id_team):
	equipo = Teams.query.get(id_team)
	if not equipo:
		return jsonify({'error': 'equipo no existe'}), 404
	data = request.get_json()
	equipo.name = data.get('name', equipo.name)
	db.session.commit()
	return jsonify({'mensaje': 'Equipo actualizado'}), 200

@app.route('/players/<int:id_player>', methods=['PUT'])
def update_player(id_player):
	jugador = Players.query.get(id_player)
	if not jugador:
		return jsonify({'error': 'jugador no existe'}), 404
	data = request.get_json()
	jugador.name = data.get('name', jugador.name)
	jugador.lastname = data.get('lastname', jugador.lastname)
	jugador.number = data.get('number', jugador.number)
	db.session.commit()
	return jsonify({'mensaje': 'Jugador actualizado'}), 200

@app.route('/lineups/<int:id_lineup>', methods=['PUT'])
def update_lineup(id_lineup):
	lineup = Lineups.query.get(id_player)
	if not lineup:
		return jsonify({'error': 'lineup no existe'}), 404
	data = request.get_json()
	lineup.titular = data.get('titular', lineup.titular)
	db.session.commit()
	return jsonify({'mensaje': 'lineup actualizado'}), 200


# Ruta para DELETE
@app.route('/stadiums/<int:id_stadium>', methods=['DELETE'])
def delete_usuario(id_stadium):
    estadio = Stadiums.query.get(id_stadium)
    if not estadio:
        return jsonify({'message': 'Estadio no existe'}), 404
    db.session.delete(estadio)
    db.session.commit()
    return jsonify({'message': 'estadio eliminado'}), 200

@app.route('/teams/<int:id_team>', methods=['DELETE'])
def delete_team(id_team):
    equipo = Teams.query.get(id_team)
    if not equipo:
        return jsonify({'message': 'Equipo no existe'}), 404
    db.session.delete(equipo)
    db.session.commit()
    return jsonify({'message': 'Equipo eliminado'}), 200

@app.route('/players/<int:id_player>', methods=['DELETE'])
def delete_player(id_player):
    jugador = Players.query.get(id_player)
    if not jugador:
        return jsonify({'message': 'Jugador no existe'}), 404
    db.session.delete(jugador)
    db.session.commit()
    return jsonify({'message': 'Jugador eliminado'}), 200

@app.route('/games/<int:id_game>', methods=['DELETE'])
def delete_game(id_game):
    juego = Games.query.get(id_game)
    if not juego:
        return jsonify({'message': 'Juego no encontrado'}), 404
    db.session.delete(juego)
    db.session.commit()
    return jsonify({'message': 'Juego eliminado'}), 200

@app.route('/lineups/<int:id_lineup>', methods=['DELETE'])
def delete_lineup(id_lineup):
    lineup = Lineups.query.get(id_lineup)
    if not lineup:
        return jsonify({'message': 'Lineups no encontrados'}), 404
    db.session.delete(lineup)
    db.session.commit()
    return jsonify({'message': 'Lineup eliminado'}), 200

# Ruta para RESULT
@app.route('/stadiums', methods=['GET'])
def get_stadiums():
    estadios = Stadiums.query.all()
    output = []
    for estadio in estadios:
        estadio_data = {'id': estadio.id, 'name': estadio.name, 'city': estadio.city}
        output.append(estadio_data)
    return jsonify({'estadios': output}), 200

@app.route('/teams', methods=['GET'])
def get_teams():
    equipos = Teams.query.all()
    output = []
    for equipo in equipos:
        equipo_data = {'id': equipo.id, 'name': equipo.name, 'id_stadium': equipo.id_stadium}
        output.append(equipo_data)
    return jsonify({'equipos': output}), 200

@app.route('/players', methods=['GET'])
def get_players():
    jugadores = Players.query.all()
    output = []
    for jugador in jugadores:
        jugador_data = {'id': jugador.id, 'name': jugador.name, 'lastname': jugador.lastname, 'number': jugador.number, 'id_team': jugador.id_team}
        output.append(jugador_data)
    return jsonify({'jugador': output}), 200

@app.route('/games', methods=['GET'])
def get_games():
    juegos = Games.query.all()
    output = []
    for juego in juegos:
        juego_data = {'id': juego.id, 'id_game_date': juego.id_game_date, 'id_game_place': juego.id_game_place, 'id_local_team': juego.id_local_team, 'id_visitor_team': juego.id_visitor_team}
        output.append(juego_data)
    return jsonify({'juegos': output}), 200

@app.route('/lineups', methods=['GET'])
def get_lineups():
    lineups = Lineups.query.all()
    output = []
    for lineup in lineups:
        lineup_data = {'id': lineup.id, 'id_game': lineup.id_game, 'id_player': lineup.id_player, 'id_position': lineup.id_position, 'titular': lineup.titular}
        output.append(lineup_data)
    return jsonify({'lineups': output}), 200

@app.route('/gamedates', methods=['GET'])
def get_gamedates():
    fechas = GameDate.query.all()
    output = []
    for fecha in fechas:
        fecha_data = {'id': fecha.id, 'timestamp': fecha.timestamp}
        output.append(fecha_data)
    return jsonify({'fechas': output}), 200

@app.route('/gameplaces', methods=['GET'])
def get_gameplaces():
    lugares = GamePlace.query.all()
    output = []
    for lugar in lugares:
        lugar_data = {'id': lugar.id, 'id_stadium': lugar.id_stadium}
        output.append(lugar_data)
    return jsonify({'lugares': output}), 200

@app.route('/positions', methods=['GET'])
def get_positions():
    positions = Positions.query.all()
    output = []
    for position in positions:
        position_data = {'id': position.id, 'id_nombre': position.id_nombre}
        output.append(position_data)
    return jsonify({'posiciones': output}), 200

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')