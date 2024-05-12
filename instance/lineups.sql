CREATE TABLE IF NOT EXISTS `Stadiums` (
	`id` integer primary key NOT NULL UNIQUE,
	`name` TEXT NOT NULL,
	`city` TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS `Teams` (
	`id` integer primary key NOT NULL UNIQUE,
	`name` TEXT NOT NULL,
	`id_stadium` INTEGER NOT NULL,
FOREIGN KEY(`id_stadium`) REFERENCES `Stadiums`(`id`)
);
CREATE TABLE IF NOT EXISTS `Players` (
	`id` integer primary key NOT NULL UNIQUE,
	`name` TEXT NOT NULL,
	`lastname` TEXT NOT NULL,
	`number` INTEGER NOT NULL,
	`id_team` INTEGER NOT NULL,
FOREIGN KEY(`id_team`) REFERENCES `Teams`(`id`)
);
CREATE TABLE IF NOT EXISTS `GameDate` (
	`id` integer primary key NOT NULL UNIQUE,
	`timestamp` REAL NOT NULL
);
CREATE TABLE IF NOT EXISTS `GamePlace` (
	`id` integer primary key NOT NULL UNIQUE,
	`id_stadium` INTEGER NOT NULL,
FOREIGN KEY(`id_stadium`) REFERENCES `Stadiums`(`id`)
);
CREATE TABLE IF NOT EXISTS `Games` (
	`id` integer primary key NOT NULL UNIQUE,
	`id_local_team` INTEGER NOT NULL,
	`id_visitor_team` INTEGER NOT NULL,
	`id_game_place` INTEGER NOT NULL,
	`id_game_date` INTEGER NOT NULL,
FOREIGN KEY(`id_local_team`) REFERENCES `Teams`(`id`),
FOREIGN KEY(`id_visitor_team`) REFERENCES `Teams`(`id`),
FOREIGN KEY(`id_game_place`) REFERENCES `GamePlace`(`id`),
FOREIGN KEY(`id_game_date`) REFERENCES `GameDate`(`id`)
);
CREATE TABLE IF NOT EXISTS `Positions` (
	`id` integer primary key NOT NULL UNIQUE,
	`name` TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS `1715550984` (

);
CREATE TABLE IF NOT EXISTS `Lineups` (
	`id` integer primary key NOT NULL UNIQUE,
	`id_game` INTEGER NOT NULL,
	`id_player` INTEGER NOT NULL,
	`id_position` INTEGER NOT NULL,
	`titular` INTEGER NOT NULL,
FOREIGN KEY(`id_player`) REFERENCES `Players`(`id`),
FOREIGN KEY(`id_position`) REFERENCES `Positions`(`id`)
);

FOREIGN KEY(`id_stadium`) REFERENCES `Stadiums`(`id`)
FOREIGN KEY(`id_team`) REFERENCES `Teams`(`id`)

FOREIGN KEY(`id_stadium`) REFERENCES `Stadiums`(`id`)
FOREIGN KEY(`id_local_team`) REFERENCES `Teams`(`id`)
FOREIGN KEY(`id_visitor_team`) REFERENCES `Teams`(`id`)
FOREIGN KEY(`id_game_place`) REFERENCES `GamePlace`(`id`)
FOREIGN KEY(`id_game_date`) REFERENCES `GameDate`(`id`)


FOREIGN KEY(`id_player`) REFERENCES `Players`(`id`)
FOREIGN KEY(`id_position`) REFERENCES `Positions`(`id`)