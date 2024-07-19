-- Author: Eve Murphy
-- Student ID: 20049423
-- Date: 18/07/2024
-- Description: This script is an automatically-generated SQL dump of the latest testing integration
--              of the Summit database.
--              Execute query to fully restore the testing database.


-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jul 19, 2024 at 11:55 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `summit`
--

-- --------------------------------------------------------

--
-- Table structure for table `log`
--

CREATE TABLE `log` (
  `log_id` int(11) NOT NULL,
  `log_title` varchar(2000) NOT NULL,
  `log_body` varchar(2000) NOT NULL,
  `log_notes` varchar(2000) DEFAULT NULL,
  `log_type` enum('proposal','vote','general') NOT NULL DEFAULT 'general',
  `org_id` int(11) DEFAULT NULL,
  `log_timestamp` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `log`
--

INSERT INTO `log` (`log_id`, `log_title`, `log_body`, `log_notes`, `log_type`, `org_id`, `log_timestamp`) VALUES
(1, 'Proposal Created by Member 1', 'A new proposal titled \'test proposal log\' has been submitted.', '', 'proposal', 1, '2024-07-17 13:22:30'),
(2, 'Vote Submitted by Member 1', 'Member 1 voted yes on proposal 2.', '', 'vote', 1, '2024-07-17 13:46:44'),
(3, 'Proposal Created by Member 1', 'A new proposal titled \'test log 2\' has been submitted.', '', 'proposal', 1, '2024-07-17 13:47:29'),
(4, 'Vote Submitted by Member 3', 'Member 3 voted yes on proposal 2.', '', 'vote', 1, '2024-07-18 12:46:13'),
(5, 'Vote Submitted by Member 3', 'Member 3 voted no on proposal 3.', '', 'vote', 1, '2024-07-18 12:46:22');

-- --------------------------------------------------------

--
-- Table structure for table `member`
--

CREATE TABLE `member` (
  `member_id` int(11) NOT NULL,
  `member_firstname` varchar(45) NOT NULL,
  `member_lastname` varchar(45) NOT NULL,
  `member_role` varchar(45) NOT NULL,
  `member_level` varchar(45) NOT NULL,
  `member_email` varchar(45) NOT NULL,
  `member_password` varchar(45) NOT NULL,
  `team_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `member`
--

INSERT INTO `member` (`member_id`, `member_firstname`, `member_lastname`, `member_role`, `member_level`, `member_email`, `member_password`, `team_id`) VALUES
(1, 'Eve', 'Murphy', 'Worker', 'Admin', 'eve@5spice.com', 'test', 1),
(2, 'Roscoe', 'Birk', 'Worker', 'Member', 'roscoe@5spice.com', 'test', 2),
(3, 'Jago', 'Stephens', 'Worker', 'Rep', 'jago@5spice.com', 'test', 1);

-- --------------------------------------------------------

--
-- Table structure for table `organisation`
--

CREATE TABLE `organisation` (
  `org_id` int(11) NOT NULL,
  `org_name` varchar(100) NOT NULL,
  `org_code` int(5) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `organisation`
--

INSERT INTO `organisation` (`org_id`, `org_name`, `org_code`) VALUES
(1, 'Fivespice', 0),
(2, 'Dairyco', 1);

-- --------------------------------------------------------

--
-- Table structure for table `proposal`
--

CREATE TABLE `proposal` (
  `proposal_id` int(11) NOT NULL,
  `proposal_title` varchar(200) NOT NULL,
  `proposal_body` varchar(3000) NOT NULL,
  `proposal_priority` varchar(45) NOT NULL,
  `proposal_majority` int(11) NOT NULL,
  `proposal_status` varchar(45) NOT NULL,
  `proposal_timestamp` datetime NOT NULL,
  `proposal_notes` varchar(2000) DEFAULT NULL,
  `proposal_yes_votes` int(11) NOT NULL,
  `proposal_no_votes` int(11) NOT NULL,
  `member_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `proposal`
--

INSERT INTO `proposal` (`proposal_id`, `proposal_title`, `proposal_body`, `proposal_priority`, `proposal_majority`, `proposal_status`, `proposal_timestamp`, `proposal_notes`, `proposal_yes_votes`, `proposal_no_votes`, `member_id`) VALUES
(1, 'test proposal 1', 'testing proposal database and routing', 'Normal', 50, 'Open', '2024-07-17 11:31:05', NULL, 3, 0, 1),
(2, 'test proposal log', 'testing proposals log entry automation', 'Normal', 50, 'Open', '2024-07-17 14:22:30', NULL, 1, 1, 1),
(3, 'test log 2', 'body', 'Normal', 50, 'Open', '2024-07-17 14:47:29', NULL, 2, 1, 1);

-- --------------------------------------------------------

--
-- Table structure for table `team`
--

CREATE TABLE `team` (
  `team_id` int(11) NOT NULL,
  `team_name` varchar(100) NOT NULL,
  `org_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `team`
--

INSERT INTO `team` (`team_id`, `team_name`, `org_id`) VALUES
(1, 'Distribution', 1),
(2, 'Administration', 1),
(3, 'Sales And Marketing', 1);

-- --------------------------------------------------------

--
-- Table structure for table `thread`
--

CREATE TABLE `thread` (
  `thread_id` int(11) NOT NULL,
  `thread_content` varchar(2000) NOT NULL,
  `thread_timestamp` datetime NOT NULL,
  `thread_parent` int(11) DEFAULT NULL,
  `proposal_id` int(11) DEFAULT NULL,
  `member_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `thread`
--

INSERT INTO `thread` (`thread_id`, `thread_content`, `thread_timestamp`, `thread_parent`, `proposal_id`, `member_id`) VALUES
(1, 'this is my first proposal', '2024-07-18 11:27:29', NULL, 1, 1);

-- --------------------------------------------------------

--
-- Table structure for table `vote`
--

CREATE TABLE `vote` (
  `vote_id` int(11) NOT NULL,
  `vote_value` enum('yes','no') NOT NULL,
  `proposal_id` int(11) DEFAULT NULL,
  `member_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `vote`
--

INSERT INTO `vote` (`vote_id`, `vote_value`, `proposal_id`, `member_id`) VALUES
(1, 'yes', 1, 1),
(2, 'yes', 3, 1),
(3, 'yes', 1, 3),
(4, 'yes', 2, 3),
(5, 'no', 3, 3);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `log`
--
ALTER TABLE `log`
  ADD PRIMARY KEY (`log_id`),
  ADD KEY `org_id` (`org_id`);

--
-- Indexes for table `member`
--
ALTER TABLE `member`
  ADD PRIMARY KEY (`member_id`),
  ADD KEY `team_id` (`team_id`);

--
-- Indexes for table `organisation`
--
ALTER TABLE `organisation`
  ADD PRIMARY KEY (`org_id`);

--
-- Indexes for table `proposal`
--
ALTER TABLE `proposal`
  ADD PRIMARY KEY (`proposal_id`),
  ADD KEY `member_id` (`member_id`);

--
-- Indexes for table `team`
--
ALTER TABLE `team`
  ADD PRIMARY KEY (`team_id`),
  ADD KEY `org_id` (`org_id`);

--
-- Indexes for table `thread`
--
ALTER TABLE `thread`
  ADD PRIMARY KEY (`thread_id`),
  ADD KEY `proposal_id` (`proposal_id`),
  ADD KEY `member_id` (`member_id`);

--
-- Indexes for table `vote`
--
ALTER TABLE `vote`
  ADD PRIMARY KEY (`vote_id`),
  ADD KEY `proposal_id` (`proposal_id`),
  ADD KEY `member_id` (`member_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `log`
--
ALTER TABLE `log`
  MODIFY `log_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `member`
--
ALTER TABLE `member`
  MODIFY `member_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `organisation`
--
ALTER TABLE `organisation`
  MODIFY `org_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `proposal`
--
ALTER TABLE `proposal`
  MODIFY `proposal_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `team`
--
ALTER TABLE `team`
  MODIFY `team_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `thread`
--
ALTER TABLE `thread`
  MODIFY `thread_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `vote`
--
ALTER TABLE `vote`
  MODIFY `vote_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `log`
--
ALTER TABLE `log`
  ADD CONSTRAINT `log_ibfk_1` FOREIGN KEY (`org_id`) REFERENCES `organisation` (`org_id`);

--
-- Constraints for table `member`
--
ALTER TABLE `member`
  ADD CONSTRAINT `member_ibfk_1` FOREIGN KEY (`team_id`) REFERENCES `team` (`team_id`);

--
-- Constraints for table `proposal`
--
ALTER TABLE `proposal`
  ADD CONSTRAINT `proposal_ibfk_1` FOREIGN KEY (`member_id`) REFERENCES `member` (`member_id`);

--
-- Constraints for table `team`
--
ALTER TABLE `team`
  ADD CONSTRAINT `team_ibfk_1` FOREIGN KEY (`org_id`) REFERENCES `organisation` (`org_id`);

--
-- Constraints for table `thread`
--
ALTER TABLE `thread`
  ADD CONSTRAINT `thread_ibfk_1` FOREIGN KEY (`proposal_id`) REFERENCES `proposal` (`proposal_id`),
  ADD CONSTRAINT `thread_ibfk_2` FOREIGN KEY (`member_id`) REFERENCES `member` (`member_id`);

--
-- Constraints for table `vote`
--
ALTER TABLE `vote`
  ADD CONSTRAINT `vote_ibfk_1` FOREIGN KEY (`proposal_id`) REFERENCES `proposal` (`proposal_id`),
  ADD CONSTRAINT `vote_ibfk_2` FOREIGN KEY (`member_id`) REFERENCES `member` (`member_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
