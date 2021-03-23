/***********************************************
**                Music League Analysis
** File:   Music League DDL
** Desc:   Create database
** Auth:   Spencer Simon
** Date:   03/22/2021
************************************************/

-- -----------------------------------------------------
-- Schema music_league
-- -----------------------------------------------------

CREATE SCHEMA IF NOT EXISTS `music_league` DEFAULT CHARACTER SET latin1 ;
USE `music_league` ;

-- -----------------------------------------------------
-- Table `music_league`.`players`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `music_league`.`players` (
  `player_id` INT(10) NOT NULL,
  `name` VARCHAR(50) NOT NULL,
  `total_points` INT(10) NOT NULL,
  PRIMARY KEY (`player_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `music_league`.`artists`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `music_league`.`artists` (
  `artist_id` INT(10) NOT NULL,
  `name` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`artist_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `music_league`.`songs`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `music_league`.`songs` (
  `song_id` INT(10) NOT NULL,
  `title` VARCHAR(130) NOT NULL,
  `artist_id` INT(10) NOT NULL,
  PRIMARY KEY (`song_id`),
  FOREIGN KEY (`artist_id`) REFERENCES `artists`(artist_id)
  ON DELETE NO ACTION ON UPDATE NO ACTION)
/*  CONSTRAINT `artists_songs_fk`
    FOREIGN KEY (`artist_id`)
    REFERENCES `music_league`.`artists` (`artist_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)*/
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `music_league`.`rounds`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `music_league`.`rounds` (
  `round_id` INT(10) NOT NULL,
  `name` VARCHAR(80) NOT NULL,
  `date` TIMESTAMP NOT NULL,
  PRIMARY KEY (`round_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;

-- -----------------------------------------------------
-- Table `music_league`.`results`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `music_league`.`results` (
  `result_id` INT(10) NOT NULL,
  `place` INT(10) NOT NULL,
  `total_points_earned` INT(10) NOT NULL,
  `submitter_id` INT(10) NOT NULL,
  `round_id` INT(10) NOT NULL,
  `song_id` INT(10) NOT NULL,
  PRIMARY KEY (`result_id`),
  FOREIGN KEY (`submitter_id`) REFERENCES `players`(`player_id`)
  ON DELETE NO ACTION ON UPDATE NO ACTION,
  FOREIGN KEY (`round_id`) REFERENCES `rounds`(`round_id`)
  ON DELETE NO ACTION ON UPDATE NO ACTION,
FOREIGN KEY (`song_id`) REFERENCES `songs`(`song_id`)
  ON DELETE NO ACTION ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;

-- -----------------------------------------------------
-- Table `music_league`.`votes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `music_league`.`votes` (
  `vote_id` INT(10) NOT NULL,
  `points_given` INT(10) NOT NULL,
  `voter_id` INT(10) NOT NULL,
  `result_id` INT(10) NOT NULL,
  PRIMARY KEY (`vote_id`),
 FOREIGN KEY (`result_id`) REFERENCES `results`(`result_id`)
  ON DELETE NO ACTION ON UPDATE NO ACTION,
  FOREIGN KEY (`voter_id`) REFERENCES `players`(`player_id`)
  ON DELETE NO ACTION ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;
