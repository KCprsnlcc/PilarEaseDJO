-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 01, 2025 at 05:38 AM
-- Server version: 11.4.2-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `pilarease_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `main_reply`
--

CREATE TABLE `main_reply` (
  `id` bigint(20) NOT NULL,
  `text` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `status_id` bigint(20) NOT NULL,
  `user_id` bigint(20) NOT NULL,
  `parent_reply_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `main_reply`
--

INSERT INTO `main_reply` (`id`, `text`, `created_at`, `status_id`, `user_id`, `parent_reply_id`) VALUES
(23, 'I\'m sorry to hear you\'re having a tough day. It\'s okay to feel sad, especially after personal events. Remember to be kind to yourself and take things one step at a time. Reach out to someone you trust if you need support.', '2024-08-07 22:29:34.442710', 155, 5, NULL),
(24, 'I\'m sorry you\'re feeling this way. It\'s okay to struggle and feel sad. Take care of yourself and don\'t hesitate to reach out to friends or loved ones for support.', '2024-08-07 22:30:12.981934', 155, 14, NULL),
(26, 'It\'s tough dealing with anger, especially after a miscommunication at work. It\'s great that you\'re focusing on managing your emotions constructively. Take a moment to breathe and find a positive way to address the issue.', '2024-08-07 22:30:58.710601', 151, 14, NULL),
(27, 'Dealing with unpleasant tasks is never easy, but it\'s great that you got through it. Sometimes, these challenges test our resilience and make us stronger. Well done for pushing through!', '2024-08-07 22:31:20.649407', 149, 14, NULL),
(29, 'It\'s fantastic to hear about the positive momentum in your translation process! The steady progress and the team\'s dedication are truly inspiring. Keep up the great work!', '2024-08-07 22:31:58.831063', 142, 14, NULL),
(30, 'I\'m glad to hear that today was filled with joyful moments for you, both at work and at home. Cherishing these happy times is important and can motivate us to keep pushing forward.', '2024-08-07 22:33:03.208216', 154, 13, NULL),
(32, 'I\'m really sorry to hear about the disheartening news regarding your close friend. It\'s challenging to stay motivated when personal life throws such curveballs. Remember to take care of yourself during this tough time, and don\'t hesitate to reach out for support if you need it.', '2024-08-07 22:33:53.844002', 150, 13, NULL),
(33, 'I\'m sorry to hear you\'re feeling this way. It\'s okay to struggle with sadness, especially after personal events. Remember to be kind to yourself and take things one step at a time. Stay strong, and reach out for support if you need it.', '2024-08-07 22:34:35.482708', 155, 10, NULL),
(34, 'It\'s wonderful to hear that your day was filled with joyful moments both at work and at home. Cherishing these happy times is so important and can really help us keep pushing forward.', '2024-08-07 22:35:03.968824', 154, 10, NULL),
(35, 'Despite the numerous challenges, it\'s encouraging to see the steady progress we\'re making. The team\'s determination and resilience are truly commendable. Let\'s keep pushing forward together.', '2024-08-07 22:36:02.913451', 147, 10, NULL),
(36, 'It\'s great to see that we\'re making steady progress despite the challenges. The team\'s determination and resilience are truly admirable. Let\'s continue to push forward with the same spirit.', '2024-08-07 22:36:36.054822', 147, 5, NULL),
(37, 'Amidst all the challenges, it\'s uplifting to see our steady progress. The determination and resilience of the team are truly commendable. Let\'s keep pushing forward together.', '2024-08-07 22:37:09.691447', 147, 13, NULL),
(38, 'Even with the many challenges we face, our progress remains steady. The team\'s resilience and determination are inspiring. Let\'s keep moving forward and overcoming obstacles together.', '2024-08-07 22:37:42.700485', 147, 12, NULL);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `main_reply`
--
ALTER TABLE `main_reply`
  ADD PRIMARY KEY (`id`),
  ADD KEY `main_reply_status_id_2c3fdd18_fk_main_status_id` (`status_id`),
  ADD KEY `main_reply_user_id_c04a947d_fk_main_customuser_id` (`user_id`),
  ADD KEY `main_reply_parent_reply_id_07ed2885_fk_main_reply_id` (`parent_reply_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `main_reply`
--
ALTER TABLE `main_reply`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=71;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
