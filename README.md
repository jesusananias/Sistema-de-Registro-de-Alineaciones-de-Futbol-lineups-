# Sistema-de-Registro-de-Alineaciones-de-Futbol-lineups-
Sistema que se encarga de ofrecer una api para registrar las alineaciones por partido de los equipos que se enfrentan en un partido.
# Link
https://josuecarrera22.pythonanywhere.com/stadiums
## Parametros
POST y PUT: json con {name, city}

DELETE: se agrega el id del registro en el link por ejemplo https://josuecarrera22.pythonanywhere.com/players/1

GET: sin parametros

# Link
https://josuecarrera22.pythonanywhere.com/teams
## Parametros
POST y PUT: json con {name, id_stadium}

DELETE: se agrega el id del registro en el link por ejemplo https://josuecarrera22.pythonanywhere.com/players/1

GET: sin parametros por ejemplo https://josuecarrera22.pythonanywhere.com/teams

# Link
https://josuecarrera22.pythonanywhere.com/players
## Parametros
POST y PUT: json con {name, lastname, number, id_team}

DELETE: se agrega el id del registro en el link por ejemplo https://josuecarrera22.pythonanywhere.com/players/1

GET: sin parametros

# Link
https://josuecarrera22.pythonanywhere.com/games
## Parametros
POST y PUT: json con {id_local_team, id_visitor_team, id_stadium}

DELETE: se agrega el id del registro en el link por ejemplo https://josuecarrera22.pythonanywhere.com/players/1

GET: sin parametros

# Link
https://josuecarrera22.pythonanywhere.com/lineups
## Parametros
POST y PUT: json con {id_game, id_player, position, titular(1 o 0)}

DELETE: se agrega el id del registro en el link por ejemplo https://josuecarrera22.pythonanywhere.com/players/1

GET: sin parametros
