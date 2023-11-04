-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 03, 2023 at 02:31 PM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.0.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `skanin_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `history`
--

CREATE TABLE `history` (
  `history_id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `stress_id` smallint(6) NOT NULL,
  `date_transaction` timestamp(6) NOT NULL DEFAULT current_timestamp(6),
  `rice_image` longblob NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `rice_stress`
--

CREATE TABLE `rice_stress` (
  `stress_id` smallint(6) NOT NULL,
  `stress_name` varchar(50) NOT NULL,
  `stress_type` varchar(50) NOT NULL,
  `stress_level` tinyint(4) NOT NULL,
  `description` varchar(150) NOT NULL,
  `description_src` varchar(255) NOT NULL,
  `recommendation` varchar(150) NOT NULL,
  `recommendation_src` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `user_id` int(11) NOT NULL,
  `username` varchar(32) NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(32) NOT NULL,
  `date_created` timestamp(6) NOT NULL DEFAULT current_timestamp(6),
  `first_name` text NOT NULL,
  `last_name` text NOT NULL,
  `contact` varchar(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_id`, `username`, `password`, `email`, `date_created`, `first_name`, `last_name`, `contact`) VALUES
(7, 'neal', '07f7032ec4e91bef180454f517210a26a2dc5b0f', 'qnbjjmatira@gmail.com', '2023-11-01 15:33:50.597530', 'Neal Barton James', 'Matira', '09156855546'),
(17, 'newest_test', 'f4623cf28741bd0f6e0ecbee29bb060e5ab8092b', 'test@test.com', '2023-11-03 13:27:46.811543', 'test1', 'test2', '09123456782');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `history`
--
ALTER TABLE `history`
  ADD PRIMARY KEY (`history_id`);

--
-- Indexes for table `rice_stress`
--
ALTER TABLE `rice_stress`
  ADD PRIMARY KEY (`stress_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `history`
--
ALTER TABLE `history`
  MODIFY `history_id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `rice_stress`
--
ALTER TABLE `rice_stress`
  MODIFY `stress_id` smallint(6) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
