-- Railway Reservation System: schema + sample data
-- Run once:  mysql -u root -p < railway_schema.sql

CREATE DATABASE IF NOT EXISTS railway_reservation;
USE railway_reservation;

-- Drop in dependency order so the script can be re-run for a fresh start
DROP TABLE IF EXISTS bookings;
DROP TABLE IF EXISTS passengers;
DROP TABLE IF EXISTS trains;

-- One row per train. Seats are only a COUNT (no seat numbers), first come first serve.
CREATE TABLE trains (
    train_id     INT          PRIMARY KEY,
    train_name   VARCHAR(50)  NOT NULL,
    start_point  VARCHAR(30)  NOT NULL,
    end_point    VARCHAR(30)  NOT NULL,
    start_time   DATETIME     NOT NULL,
    end_time     DATETIME     NOT NULL,
    total_seats  INT          NOT NULL CHECK (total_seats >= 0)
);

-- One row per person. Phone number identifies a passenger.
CREATE TABLE passengers (
    phone  CHAR(10)     PRIMARY KEY,
    name   VARCHAR(40)  NOT NULL
);

-- One row per ticket. A cancelled ticket stays on record with status CANCELLED,
-- and its seat becomes free again (seats left = total_seats - CONFIRMED tickets).
CREATE TABLE bookings (
    ticket_id  INT AUTO_INCREMENT PRIMARY KEY,
    train_id   INT      NOT NULL,
    phone      CHAR(10) NOT NULL,
    booked_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status     ENUM('CONFIRMED','CANCELLED') NOT NULL DEFAULT 'CONFIRMED',
    FOREIGN KEY (train_id) REFERENCES trains(train_id),
    FOREIGN KEY (phone)    REFERENCES passengers(phone),
    INDEX idx_train_status (train_id, status)
) AUTO_INCREMENT = 100000;

-- Sample data (the first three match the report's Guwahati -> Delhi screenshot)
INSERT INTO trains VALUES
(100234, 'Rajdhani Express',      'Guwahati', 'Delhi',   '2026-10-20 06:30:00', '2026-10-21 09:45:00', 3),
(101252, 'Northeast Express',     'Guwahati', 'Delhi',   '2026-10-20 14:15:00', '2026-10-22 03:10:00', 5),
(234587, 'Brahmaputra Mail',      'Guwahati', 'Delhi',   '2026-10-21 20:00:00', '2026-10-23 08:30:00', 2),
(110011, 'Shatabdi Express',      'Delhi',    'Jaipur',  '2026-10-20 06:05:00', '2026-10-20 10:40:00', 4),
(110022, 'Pink City Express',     'Delhi',    'Jaipur',  '2026-10-20 17:30:00', '2026-10-20 22:50:00', 3),
(120045, 'Mumbai Superfast',      'Delhi',    'Mumbai',  '2026-10-22 16:00:00', '2026-10-23 08:15:00', 6),
(130077, 'Kolkata Duronto',       'Delhi',    'Kolkata', '2026-10-22 22:00:00', '2026-10-23 17:30:00', 4);
