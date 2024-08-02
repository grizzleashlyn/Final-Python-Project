-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema belt_exam_schema
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema belt_exam_schema
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `belt_exam_schema` DEFAULT CHARACTER SET utf8 ;
USE `belt_exam_schema` ;

-- -----------------------------------------------------
-- Table `belt_exam_schema`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `belt_exam_schema`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(45) NULL,
  `last_name` VARCHAR(45) NULL,
  `email` VARCHAR(45) NULL,
  `password` LONGTEXT NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `belt_exam_schema`.`trips`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `belt_exam_schema`.`trips` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `destination` MEDIUMTEXT NULL,
  `start_date` DATE NULL,
  `end_date` DATE NULL,
  `organizer` MEDIUMTEXT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `belt_exam_schema`.`booked_trips`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `belt_exam_schema`.`booked_trips` (
  `trip_id` INT NOT NULL,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`trip_id`, `user_id`),
  INDEX `fk_trips_has_users_users1_idx` (`user_id` ASC) VISIBLE,
  INDEX `fk_trips_has_users_trips_idx` (`trip_id` ASC) VISIBLE,
  CONSTRAINT `fk_trips_has_users_trips`
    FOREIGN KEY (`trip_id`)
    REFERENCES `belt_exam_schema`.`trips` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_trips_has_users_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `belt_exam_schema`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
