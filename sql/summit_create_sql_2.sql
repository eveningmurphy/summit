-- EVE MURPHY 20049423 COMPUTING PROJECT
-- Summit application SQL database creation script

-- Create the summit schema
CREATE DATABASE IF NOT EXISTS summit;
USE summit;

-- Clear old tables if present
DROP TABLE IF EXISTS organisation;
DROP TABLE IF EXISTS team;
DROP TABLE IF EXISTS member;
DROP TABLE IF EXISTS proposal;
DROP TABLE IF EXISTS thread;
DROP TABLE IF EXISTS log;
DROP TABLE IF EXISTS vote;

-- Create Organisation Table
CREATE TABLE organisation (
    org_id INT NOT NULL AUTO_INCREMENT,
    org_name VARCHAR(100) NOT NULL,
    org_code INT(5) NOT NULL,
    PRIMARY KEY (org_id)
);

-- Create Team Table
CREATE TABLE team (
    team_id INT NOT NULL AUTO_INCREMENT,
    team_name VARCHAR(100) NOT NULL,
    org_id INT,
    FOREIGN KEY (org_id) REFERENCES organisation(org_id),
    PRIMARY KEY(team_id)
);

-- Create Member Table
CREATE TABLE member (
    member_id INT NOT NULL AUTO_INCREMENT,
    member_firstname VARCHAR(45) NOT NULL,
    member_lastname VARCHAR(45) NOT NULL,
    member_role VARCHAR(45) NOT NULL,
    member_level VARCHAR(45) NOT NULL,
    member_email VARCHAR(45) NOT NULL,
    member_password VARCHAR(45) NOT NULL,
    team_id INT,
    FOREIGN KEY (team_id) REFERENCES team(team_id),
    PRIMARY KEY(member_id)
);

-- Create Proposal Table
CREATE TABLE proposal (
    proposal_id INT NOT NULL AUTO_INCREMENT,
    proposal_title VARCHAR(200) NOT NULL,
    proposal_body VARCHAR(3000) NOT NULL,
    proposal_priority VARCHAR(45) NOT NULL,
    proposal_majority INT NOT NULL,
    proposal_status VARCHAR(45) NOT NULL,
    proposal_timestamp DATETIME NOT NULL,
    proposal_notes VARCHAR(2000),
    proposal_yes_votes INT NOT NULL,
    proposal_no_votes INT NOT NULL,
    member_id INT,
    FOREIGN KEY (member_id) REFERENCES member(member_id),
    PRIMARY KEY (proposal_id)
);

-- Create Thread Table
CREATE TABLE thread (
    thread_id INT NOT NULL AUTO_INCREMENT,
    thread_content VARCHAR(2000) NOT NULL,
    thread_timestamp DATETIME NOT NULL,
    thread_parent INT,
    proposal_id INT,
    member_id INT,
    FOREIGN KEY (proposal_id) REFERENCES proposal(proposal_id),
    FOREIGN KEY (member_id) REFERENCES member(member_id),
    PRIMARY KEY(thread_id)
);

-- Create Log Table
CREATE TABLE log (
    log_id INT NOT NULL AUTO_INCREMENT,
    log_title VARCHAR(2000) NOT NULL,
    log_body VARCHAR(2000) NOT NULL,
    log_notes VARCHAR(2000),
    -- Added during implementation
    log_type ENUM('proposal', 'vote', 'general') NOT NULL DEFAULT 'general',
    -- Added during implementation
    log_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    org_id INT,
    FOREIGN KEY (org_id) REFERENCES organisation(org_id),
    PRIMARY KEY(log_id)
);

-- Create Vote Table
CREATE TABLE vote (
    vote_id INT NOT NULL AUTO_INCREMENT,
    vote_value ENUM('yes', 'no') NOT NULL,
    proposal_id INT,
    member_id INT,
    FOREIGN KEY (proposal_id) REFERENCES proposal(proposal_id),
    FOREIGN KEY (member_id) REFERENCES member(member_id),
    PRIMARY KEY (vote_id)
);

-- Set all tables to autoincrement ids from 1
ALTER TABLE organisation AUTO_INCREMENT = 1;
ALTER TABLE team AUTO_INCREMENT = 1;
ALTER TABLE member AUTO_INCREMENT = 1;
ALTER TABLE proposal AUTO_INCREMENT = 1;
ALTER TABLE thread AUTO_INCREMENT = 1;
ALTER TABLE log AUTO_INCREMENT = 1;
ALTER TABLE vote AUTO_INCREMENT = 1;

-- Populate test 1

-- Insert data into Organisation Table
INSERT INTO organisation (org_name, org_code) VALUES
('Fivespice', '0000'),
('Dairyco', '0001');

-- Insert data into Team Table
INSERT INTO team (team_name, org_id) VALUES
('Distribution', '1'), -- All teams for Fivespice food co-op
('Administration', '1'),
('Sales And Marketing', '1');

-- Insert data into Member Table
INSERT INTO member (member_firstname, member_lastname,
member_role, member_level, member_email, member_password, team_id) VALUES
-- Test workers with admin & rep status in distro team
('Eve','Murphy','Worker','Admin','eve@5spice.com','test','1'),
('Roscoe','Birk','Worker','Member','roscoe@5spice.com','test','2'),
('Jago','Stephens','Worker','Rep','jago@5spice.com','test','1');