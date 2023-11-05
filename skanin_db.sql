-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 05, 2023 at 08:04 AM
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

--
-- Dumping data for table `rice_stress`
--

INSERT INTO `rice_stress` (`stress_id`, `stress_name`, `stress_type`, `stress_level`, `description`, `description_src`, `recommendation`, `recommendation_src`) VALUES
(1, 'blast', 'biotic', 0, 'Blast is a fungal disease that causes lesions on leaves, stems, and panicles. It can reduce grain yield by up to 70%.', 'http://www.knowledgebank.irri.org/training/fact-sheets/pest-management/diseases/item/blast-leaf-collar', '1. Plant Resistant Varieties: Use resistant rice varieties; consult local agricultural authorities for updated lists.\r\n2. Crop Management Measures:\r\n*', 'http://www.knowledgebank.irri.org/training/fact-sheets/pest-management/diseases/item/blast-leaf-collar'),
(2, 'bacterial leaf blight', 'biotic', 0, 'Bacterial leaf blight is a bacterial disease that causes brown streaks on leaves. It can reduce grain yield by up to 20%.', 'https://ricetoday.irri.org/a-tool-that-tracks-and-stops-bacterial-blight-outbreaks-in-rice/', '* Use balanced amounts of plant nutrients, especially nitrogen.\r\n* Ensure good drainage of fields (in conventionally flooded crops) and nurseries.\r\n* ', 'http://www.knowledgebank.irri.org/training/fact-sheets/pest-management/diseases/item/bacterial-blight?category_id=326'),
(3, 'tungro', 'biotic', 0, 'Tungro is a viral disease that causes yellowing and stunting of plants. It can reduce grain yield by up to 100%.', 'http://www.knowledgebank.irri.org/training/fact-sheets/pest-management/diseases/item/tungro', '1. No Cure for Infected Plants: Once infected, rice plants cannot be cured from tungro.\r\n\r\n2. Preventive Measures are Key: Preventive measures are mor', 'http://www.knowledgebank.irri.org/training/fact-sheets/pest-management/diseases/item/tungro'),
(4, 'sheath blight', 'biotic', 0, 'Sheath blight is a fungal disease that causes brown lesions on leaf sheaths. It can reduce grain yield by up to 15%.', 'http://www.knowledgebank.irri.org/training/fact-sheets/pest-management/diseases/item/sheath-blight', '* use a reasonable level of fertilizer adapted to the cropping season.\r\n* use reasoned density of crop establishment (direct seeding or transplanting)', 'http://www.knowledgebank.irri.org/training/fact-sheets/pest-management/diseases/item/sheath-blight'),
(5, 'brown plant hopper', 'biotic', 0, 'Brown plant hopper is an insect that sucks sap from plants and transmits tungro virus. It can cause significant yield losses.', 'http://www.knowledgebank.irri.org/training/fact-sheets/pest-management/insects/item/planthopper', '1. Preventing Outbreaks:\r\n\r\n* Weed Control: Remove weeds from the field and surrounding areas to minimize habitat for brown plant hoppers (BPH).\r\n* Av', 'http://www.knowledgebank.irri.org/training/fact-sheets/pest-management/insects/item/planthopper'),
(6, 'green leaf hopper', 'biotic', 0, 'Green leaf hopper is an insect that sucks sap from plants and transmits tungro virus. It can cause significant yield losses.', 'http://www.knowledgebank.irri.org/training/fact-sheets/pest-management/insects/item/green-leafhopper', '* Use GLH-resistant and tungro-resistant varieties. Contact your local agriculture office for an up-to-date list of available varieties.\r\n* Reduce the', 'http://www.knowledgebank.irri.org/training/fact-sheets/pest-management/insects/item/green-leafhopper'),
(7, 'yellow stem borer', 'biotic', 0, 'Yellow stem borer is an insect that bores into stems and destroys them. It can cause significant yield losses.', 'http://www.knowledgebank.irri.org/training/fact-sheets/pest-management/insects/item/stem-borer', '* Use resistant varieties\r\n* At seedbed and transplanting, handpick and destroy egg masses\r\n* Raise level of irrigation water periodically to submerge', 'http://www.knowledgebank.irri.org/training/fact-sheets/pest-management/insects/item/stem-borer'),
(8, 'stem borer', 'biotic', 0, 'Stem borer is an insect that bores into stems and destroys them. It can cause significant yield losses.', 'http://www.knowledgebank.irri.org/training/fact-sheets/pest-management/insects/item/stem-borer', '* Use resistant varieties\r\n* At seedbed and transplanting, handpick and destroy egg masses\r\n* Raise level of irrigation water periodically to submerge', 'http://www.knowledgebank.irri.org/training/fact-sheets/pest-management/insects/item/stem-borer'),
(9, 'false smut', 'biotic', 0, 'False smut is a fungal disease that causes black heads to form on panicles. It can reduce grain yield by up to 10%.', 'http://www.knowledgebank.irri.org/training/fact-sheets/pest-management/diseases/item/false-smut', '* Keep the field clean.\r\n* Remove infected seeds, panicles, and plant debris after harvest.\r\n* Reduce humidity levels through alternate wetting and dr', 'http://www.knowledgebank.irri.org/training/fact-sheets/pest-management/diseases/item/false-smut'),
(10, 'healthy', 'abiotic', 0, 'Healthy rice plants are green and vigorous. They have no signs of disease or pests.', 'https://www.irri.org/crop-manager', 'N/A', 'N/A');

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
  MODIFY `stress_id` smallint(6) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
