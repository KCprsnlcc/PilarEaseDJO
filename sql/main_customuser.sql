-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 01, 2025 at 05:36 AM
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
-- Table structure for table `main_customuser`
--

--
-- Dumping data for table `main_customuser`
--

INSERT INTO `main_customuser` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`, `student_id`, `full_name`, `academic_year_level`, `contact_number`, `is_counselor`, `block_duration`, `block_reason`, `is_verified`, `verification_status`, `is_itrc_staff`) VALUES
(5, 'pbkdf2_sha256$720000$zpbMyMPXXT4DBSDDEPLDIg$1B2W+KGytZzv7VbBF54xIVnFUl5vA4EGy9belRZ7bF4=', '2024-11-19 17:58:24.731889', 0, 'KCprsnlcc', '', '', 's', 0, 1, '2024-06-28 13:16:02.592036', 'C210077', 'Sulaiman, Khadaffe A.', 'Fourth Year', '+639949953785', 0, NULL, NULL, 1, 'verified', 0),
(6, 'pbkdf2_sha256$720000$iWiUw10UsuzF0XTbOu6HRN$tLh9lesGv2/k462w0eMhDErpTu3tXjLt0fsAXVoOPZ8=', '2024-10-11 15:02:31.915811', 0, 'Dammang', '', '', 'ashraffdammang14@gmail.com', 0, 1, '2024-06-30 14:33:17.563938', 'C246783', 'Ashraff Dammang', 'Fourth Year', '+639425786145', 0, NULL, NULL, 1, 'verified', 0),
(10, 'pbkdf2_sha256$720000$P7pgmLjdkvz0CuKMdkhRfi$3E033PKV63sX7XgGmM8W1E8I3ESXmorZBYeFiD1V3Gw=', '2024-11-16 06:33:05.464240', 0, 'Mark', '', '', 'mahghg@gmail.com', 0, 1, '2024-06-30 16:08:43.524518', 'C2467832', 'mark d. guanzon', 'Fourth Year', '+639587645921', 0, NULL, NULL, 1, 'verified', 0),
(11, 'pbkdf2_sha256$720000$asfzi7efP0rraBqNnn2hHm$N82HrsFVgksvRuWFxpJAvBcssT4vlK0SCFpTbuUQAhk=', '2024-11-19 12:51:06.217754', 0, 'AppleMae', '', '', 'kcpersonalacc@gmail.com', 0, 1, '2024-06-30 18:16:51.981618', 'C654347', 'Apple Dinawanao', 'Fourth Year', '+639949953785', 0, NULL, NULL, 0, 'pending', 0),
(12, 'pbkdf2_sha256$720000$QVSwfuwXWuGm9hB96Fxlw3$sLT8dyrYvRvAktt9/ouL1pLLeKjO+MUythtd20LCzOA=', '2024-08-07 22:37:23.211246', 0, 'YourIdol', '', '', 'youridol12@gmail.com', 0, 1, '2024-06-30 19:30:18.295446', 'C464698', 'Mark Hamill Salahuddin', 'Fourth Year', '+639949953785', 0, NULL, NULL, 1, 'verified', 0),
(13, 'pbkdf2_sha256$720000$APh5yOIqou1UVeT69iK8TI$ulSBpSpYvrrDRgZ4K0eHioC/HQdm7oI2a2rgGfSboxs=', '2024-10-20 10:42:44.675304', 0, 'Radzkhan', '', '', 'alradzkhan13@gmail.com', 0, 0, '2024-06-30 19:35:34.825660', 'C665736', 'Alradzkhan Hayuddini', 'Fourth Year', '+639949956543', 0, NULL, NULL, 0, 'deactivated', 0),
(14, 'pbkdf2_sha256$720000$inmGtKqU6fQdl6I8cy1sYr$VKzrIU5j2o97+NVQIVRdiw1Ev9qcH5A1/7Am6RqyeMs=', '2024-10-11 15:00:41.951360', 0, 'Midorin', '', '', 'midorin2@gmail.com', 0, 0, '2024-06-30 19:39:03.800440', 'C564123', 'Eduard Rolad Donor', 'Fourth Year', '+63923132153', 0, NULL, NULL, 0, 'deactivated', 0),
(15, 'pbkdf2_sha256$720000$ncnhTbf8MYawLtOX0UVNeI$zm5HNked5nyy0XnhVVtwKzxrocgcFJwKcItlYJHW+uI=', '2024-11-19 16:53:10.940434', 0, 'bheng', '', '', '', 0, 1, '2024-08-03 23:16:17.085772', '', 'bheng manalo', '', '', 1, NULL, NULL, 1, 'pending', 0),
(24, 'pbkdf2_sha256$720000$gQNAwXrDm5BvQkv8wQnPi0$GXPaU6/e0MlRBvMATxUu4YfRTwKy8BDkpjliB+703VQ=', '2024-11-19 04:06:22.945548', 1, 'james', '', '', 'james@gmail.com', 0, 1, '2024-10-13 12:16:58.339571', 'NULL', 'James ITRC', 'NULL', NULL, 0, NULL, NULL, 0, 'rejected', 1),
(67, 'pbkdf2_sha256$720000$9AedgSbqRo5iNy2qXCfFqs$uBqt73RGHYg+6TalTq/d5KxxJbRL+1ttxbOHubGIYjk=', '2024-11-16 07:14:22.582590', 0, 'Jerrick', '', '', 'bucarj@pilar.edu.ph', 0, 1, '2024-11-16 07:00:14.768042', 'n/a', '121312', 'n/a', 'n/a', 1, NULL, NULL, 0, 'pending', 1),
(68, 'pbkdf2_sha256$720000$xasFEWB2teEoim4pPn78qK$B9LiiZrTLWmBar6cK0WBBI5i6iNPdshH2z4VEN+KwPU=', NULL, 0, 'Sherri', '', '', NULL, 0, 1, '2024-11-17 06:21:19.020168', 'C211077', 'Sherri Gibson', '3rd Year', '+631827912798', 0, NULL, NULL, 1, 'verified', 0),
(69, 'pbkdf2_sha256$720000$lECl9FHVs7JMpVTCbmhY84$QJocRM18RBZo33N0p5TZdcNM+kKSQQO9yaEcGsXgUAM=', '2024-11-18 03:37:01.412484', 0, 'shayne', '', '', 'shayne@gmail.com', 0, 1, '2024-11-18 03:34:00.039500', 'C230688', 'Shayne Bulat', '2nd Year', NULL, 0, NULL, NULL, 1, 'verified', 0),
(70, 'pbkdf2_sha256$720000$uzFDUJjzgGQOBiaSk9miYY$p6jM0n7vK++TDbgy4DcV8vc0EoVdJC1KW9vVJ9mwcpY=', '2024-11-18 03:39:30.211888', 0, 'Via', '', '', 'via@gmail.com', 0, 1, '2024-11-18 03:34:55.798318', 'C230165', 'Via Nicole Enriquez', '2nd Year', NULL, 0, NULL, NULL, 1, 'verified', 0),
(71, 'pbkdf2_sha256$720000$wiEc6edFS18SZzwAnujllr$sP+SOi8LgA7Ene/rGcCeUJqSdihhrt46fjSbszmpNu4=', '2024-11-18 04:03:07.490961', 0, 'Johnver', '', '', 'johnver@gmail.com', 0, 1, '2024-11-18 03:48:44.849292', 'C230367', 'Johnver Linejan', '2nd Year', 'n/a', 0, NULL, NULL, 1, 'verified', 0),
(72, 'pbkdf2_sha256$720000$ULRRHNlGECbsZrr6fjjIvx$06u1isF3nQuCYob2y/GDltipp20XzJiitRwlcKnmqqc=', '2024-11-18 03:57:59.903194', 0, 'Al-Haider', '', '', 'haider@gmail.com', 0, 1, '2024-11-18 03:54:16.310775', 'C220195', 'haider@gmail.com', '2nd Year', 'n/a', 0, NULL, NULL, 1, 'verified', 0),
(73, 'pbkdf2_sha256$720000$C0xkDGQ6JhQuQzUrpoxcVp$zCSFmIIzsgV3zsVmIvgrPUbB21S8LGyp7MO9va1Hfm4=', '2024-11-18 04:01:09.973717', 0, 'Shafee', '', '', 'shafee@gmail.com', 0, 1, '2024-11-18 04:00:35.237554', 'C230233', 'Shafee Jamih', '2nd Year', NULL, 0, NULL, NULL, 1, 'verified', 0),
(74, 'pbkdf2_sha256$720000$mZjMOZRooIUPNY63OJeWvd$QYKNYPK/iNx+1ZJtB5c51eYt5yrU1MowvAtCT77PJPo=', NULL, 0, 'Rex', '', '', 'rex@gmail.com', 0, 1, '2024-11-18 04:20:30.380783', 'C22199', 'Rex', 'Third Year', NULL, 0, NULL, NULL, 1, 'verified', 0),
(75, 'pbkdf2_sha256$720000$qi2mM1otbjxbtuS7anyEap$JvfKWlyDXynvOO4Z/i8V7tN2txx9PGnl+oBixnFF2Lc=', NULL, 0, 'Aburadzmi', '', '', 'adbu@gmail.com', 0, 1, '2024-11-18 04:21:39.146405', 'C77777', 'Aburadzmi Amdal', 'Third Year', '0999999', 0, NULL, NULL, 1, 'verified', 0),
(76, 'pbkdf2_sha256$720000$e8SCEjnuAsuaaGkC6DAUOx$1pLg3ZD5bJiH4ghwWQ5ycRGcD9KaNWPGWVl1+NAxciY=', NULL, 0, 'C88676', '', '', 'earl@gmail.com', 0, 1, '2024-11-18 04:22:41.946532', 'Earl', 'Earl', 'Third Year', 'n/a', 0, NULL, NULL, 1, 'verified', 0),
(77, 'pbkdf2_sha256$720000$nAGsaoJ0SPVCCM4maWxaUu$GQc2gKroDpMG5hS/cnUrS1mVCvQWzUGopmKioLnqCUQ=', NULL, 0, 'Vincent', '', '', 'vin@gmail.com', 0, 1, '2024-11-18 04:23:24.661500', 'C2299', 'Vincent San Buenaventura', 'Fourth Year', '0990099999', 0, NULL, NULL, 1, 'verified', 0),
(78, 'pbkdf2_sha256$720000$eAmcN6FrUjOJvF0eAwrnQ1$YX2yopzMLxqyxQu1misXv8Fd4gZDHVF4xA/6M9xPFmE=', NULL, 0, 'Sangkula', '', '', 'sangkula@gmail.com', 0, 1, '2024-11-18 04:24:13.894447', 'C7777788', 'Sangkula A', 'Third Year', 'n/a', 0, NULL, NULL, 1, 'verified', 0),
(79, 'pbkdf2_sha256$720000$14pBhGiJgF3jNuTzGUKGZa$sT/CEePWUjq1DSeDwcnVD42byuf5HSof2/vLH+zhtds=', NULL, 0, 'Jandrix', '', '', 'jandrix@gmail.com', 0, 1, '2024-11-18 04:25:42.425286', 'C888', 'Jandrix Despalo', 'Fourth Year', 'n/a', 0, NULL, NULL, 1, 'verified', 0),
(80, 'pbkdf2_sha256$720000$sQi3eHfjzLfqK7hiCOrH8o$L6NMfXV+98CinxNTz2hFnhDVCESPhj/+iZAP9pFWHXk=', '2024-11-18 06:37:47.036290', 0, 'Cassandra', '', '', 'cass@gmail.com', 0, 1, '2024-11-18 06:32:25.528343', 'C88687', 'Cassandra Abalos', 'Third Year', '998876767', 0, NULL, NULL, 1, 'verified', 0),
(81, 'pbkdf2_sha256$720000$gsWHPxP81wIIbdeJx6iGh0$OWB44NkpRfo/mCfvmm1ud+b1L/B6EIHjSDgdwNBkeTU=', '2024-11-18 07:55:33.203607', 0, 'peter123pogi', '', '', 'peterjustin05@gmail.com', 0, 1, '2024-11-18 07:52:27.559277', 'C220394', 'Peter Justin S. Delos Reyes', 'Fourth Year', '9383098055', 0, NULL, NULL, 1, 'verified', 0),
(88, 'pbkdf2_sha256$720000$OvQGiJX1Bj9n24uQsqGgGF$em9A4smopLHLib8tCuXF2oSdwOh/tkt91zCSmV78Wdg=', NULL, 0, 'newacc', '', '', 'new@gmail.com', 0, 0, '2024-11-19 03:03:03.799994', 'c213i12312', 'n/a', 'n/a', '564654654656532', 0, NULL, NULL, 0, 'pending', 1),
(89, '', '2024-11-19 03:34:44.088312', 0, 'editedjames', '', '', 'editedjames@gmail.com', 0, 0, '2024-11-19 03:03:49.261874', 'sadkjaslkd', 'Test', '0945654sd65as4d654sa', 'asadas456d65a4s', 0, NULL, NULL, 0, 'deactivated', 1);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `main_customuser`
--
ALTER TABLE `main_customuser`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `student_id` (`student_id`),
  ADD UNIQUE KEY `main_customuser_email_aad55d69_uniq` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `main_customuser`
--
ALTER TABLE `main_customuser`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=90;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
