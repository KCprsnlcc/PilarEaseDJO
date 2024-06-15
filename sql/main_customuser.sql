-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 15, 2024 at 09:24 AM
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
-- Database: `pilarease_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `main_customuser`
--

CREATE TABLE `main_customuser` (
  `id` bigint(20) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `student_id` varchar(10) NOT NULL,
  `full_name` varchar(100) NOT NULL,
  `academic_year_level` varchar(20) NOT NULL,
  `contact_number` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `main_customuser`
--

INSERT INTO `main_customuser` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`, `student_id`, `full_name`, `academic_year_level`, `contact_number`) VALUES
(1, 'pbkdf2_sha256$720000$7EGjo4wLgeu9tpywK07CzS$aVFvOEGcEQe+FKprezVsjZ1U0uAoGa/u+yaaXYNqVhs=', '2024-06-11 15:53:54.760864', 0, 'asdasd', '', '', 'asdasd@gmail.com', 0, 1, '2024-06-11 15:53:54.103013', 'asdasd', 'asdasd', 'asdasd', 'asdasd'),
(2, 'pbkdf2_sha256$720000$DO2lWQ8Uw9NN8TC2TZuQz0$a0oejVoaf26jHirG86EJfW5Na7+UIGEzKooZCvCcl94=', '2024-06-15 06:57:36.214155', 0, 'KCprsnlcc', '', '', 'kcpersonalacc@gmail.com', 0, 1, '2024-06-12 05:45:14.811565', 'C210077', 'Khadaffe Abubakar Sulaiman', 'Fourth Year', '+639949953785'),
(3, 'pbkdf2_sha256$720000$lWS4Np0NVO3dYPjcaiMIvr$TiEduD2Uqn3CB7K+aDfoXKEymlNQOa5RX2tFqOny6EI=', '2024-06-12 07:03:57.939616', 0, 'sadasd', '', '', 'asdasssd@gmail.com', 0, 1, '2024-06-12 07:03:56.773218', 's', 'asdasdasd', 'asdasdas', 'dasdasd'),
(4, 'pbkdf2_sha256$720000$NEaQ6iJ2TqMueVLTM4eVwi$gYN7FsMbR/Ieexy/TQR+DmybLRjB4095arvXL3V3kmE=', '2024-06-12 07:22:59.383723', 0, 'test3', '', '', 'name@gmail.com', 0, 1, '2024-06-12 07:22:58.532310', 'test31313', 'test1323', 'testtttt', '321321321321'),
(5, 'pbkdf2_sha256$720000$CrWwvG2IaJVZn3jaKUEemm$bag3fNmjBZJ34vjLJwhofdLAmIad6yj8Eoig86LJVK0=', '2024-06-12 10:07:08.256425', 0, 'test4', '', '', 's@gmail.com', 0, 1, '2024-06-12 10:07:07.315439', 'test41313', 'test test test test', 'test-4', '6546532123'),
(6, 'pbkdf2_sha256$720000$9rplju7lSFrJiql4oiwx9C$LWEB51r4yDG0moUFYXYbiOZbjkBulhSOWhphEE4WFM8=', '2024-06-12 11:02:39.240542', 0, 'test5success', '', '', 'test5@gmail.com', 0, 1, '2024-06-12 11:02:38.430652', 'test5', 'test52', 'test5555', '56464654564'),
(7, 'pbkdf2_sha256$720000$GfSxVs27bJgavyqjmZDXKz$+tvNfi7ocs9/L77r3s1s2tVZ8aibQI8WLiVLUhKHVnc=', '2024-06-12 11:34:54.996019', 0, 's', '', '', 's@d.com', 0, 1, '2024-06-12 11:34:54.135392', 'sd', 's', 's', 's'),
(8, 'pbkdf2_sha256$720000$cZznX4KhZDIUHA3ODclvZJ$OYAcKPgw38U5g7wVm1MrHz8GIE9dXVVJT1Pb/EVAg4A=', '2024-06-12 11:36:28.126463', 0, 'test6', '', '', 'test6@gmail.com', 0, 1, '2024-06-12 11:36:27.246052', 'test6', 'test user admin', 'test year', '369852147'),
(9, 'pbkdf2_sha256$720000$7NCYVIgvwLgxIYmWcaT5oA$+2FL0M06iUJLWvDCN6MWF0IJ7we+1kvFYyhI8B5DlJQ=', '2024-06-12 13:28:06.601344', 0, 'finaltest', '', '', 'finaltest@gmail.com', 0, 1, '2024-06-12 13:28:05.669755', 'final131', 'final test', 'final 3', '123654789'),
(10, 'pbkdf2_sha256$720000$UXAP63LPdKZTMdnxfpjkFb$j5VlRrGa8Ebe5ftL98m69kv8bImYcscZba+ULRGjHao=', '2024-06-12 13:40:16.046826', 0, 'testfinalfinal', '', '', 'final@gmail.com', 0, 1, '2024-06-12 13:40:15.098497', 'C200774', 'final final test', 'final test 3', '123654789'),
(11, 'pbkdf2_sha256$720000$NGXqOpNCYnM6KHd9MelIa2$HbuUUIG9Z3yd4HpQ4aTfJWezYIzRGy1aYbwRXt3RwNw=', '2024-06-12 13:44:15.075873', 0, 'last_bal', '', '', 'last@gmail.com', 0, 1, '2024-06-12 13:44:14.180963', 'B131315', 'last ball at', 'last-3', '123654789'),
(12, 'pbkdf2_sha256$720000$JON2TkIxlrVi7sOH9OeOa9$TIEIY/8IW39qsmEWsqIylYWS1aDZxq19Jw8IlDXUX24=', '2024-06-12 13:48:58.081994', 0, 'balllast', '', '', 'balllast@gmail.com', 0, 1, '2024-06-12 13:48:57.157316', 'balllast', 'balllast', 'balllast', '123654789'),
(13, 'pbkdf2_sha256$720000$xSkWdhCD7ykNbyXzppR25w$bQlCT5wldFcts9o9EgTmJBvyOsqDnBmVpfcAo8xfQdA=', '2024-06-12 13:58:01.010324', 0, 'register', '', '', 'register@gmail.com', 0, 1, '2024-06-12 13:58:00.089224', 'register', 'register', 'register-3', '123654789'),
(15, 'pbkdf2_sha256$720000$sblBAxrjLUTYvKM4sArnvJ$PPcCogT794dZILYtiGHTSnKJbzXXlaWs/VQZLiqmtJ8=', '2024-06-12 14:00:54.800978', 0, 'lastna', '', '', 'lastna@gmail.com', 0, 1, '2024-06-12 14:00:53.997263', 'lastna', 'lastna', 'lastna-3', '123654789'),
(16, 'pbkdf2_sha256$720000$2LjMNu9uVZW1Y2A4oTx9wX$7sxevIIwmdydHFwTVy8hkXloQjGb6jczAMRgQoYPpNA=', '2024-06-12 14:02:38.876858', 0, 'nalast', '', '', 'nalast@gmail.com', 0, 1, '2024-06-12 14:02:38.230263', 'nalast', 'nalast', 'nalast-3', '123654789'),
(17, 'pbkdf2_sha256$720000$3eMmf3C5XX0LK5wJVyCDZO$mKrIvoKmllXO1z3XI0pySij+kaicY6Qc9pJ8KAvy/l0=', '2024-06-12 14:07:09.115737', 0, 'pota', '', '', 'pota@gmaill.com', 0, 1, '2024-06-12 14:07:08.328379', 'pota', 'pota', 'pota', 'pota'),
(18, 'pbkdf2_sha256$720000$HrYVPk1IyjCMaUyzI0fgVy$iQHAj3FjDkY9Sba9eE++T17K7StKrN5+ps5HGcg8/qE=', '2024-06-12 14:11:52.667977', 0, 'gitupdate', '', '', 'gitupdate@gmail.com', 0, 1, '2024-06-12 14:11:51.953596', 'gitupdate', 'gitupdate', 'gitupdate', '123654789'),
(19, 'pbkdf2_sha256$720000$4iaD0aZ34c0WgADAqkpbkv$UTlUYoRPoxaoEKCTxOUQNHIuN3O9dyESTnwt+COe4N8=', '2024-06-12 14:40:11.751148', 0, 'daffsulaiman', '', '', 'daffsulaiman@gmail.com', 0, 1, '2024-06-12 14:40:10.890228', 'C147852', 'Daff Abubakar Sulaiman', 'Third Year', '123654789'),
(20, 'pbkdf2_sha256$720000$WLnZSp1NawhxXC7o6dMXBS$LLKFwjfx71+Nlm6AC07W/dh6EN6Sx6xrfXIdZGXzA+s=', '2024-06-12 14:47:10.789664', 0, 'KCprsnlcc2', '', '', 'maria.cruz@example.com', 0, 1, '2024-06-12 14:47:10.008255', 'C098677', 'Cruz, Maria L', 'Grade 12', '+639951234567'),
(21, 'pbkdf2_sha256$720000$REWFjO0gSMdygYQey39Sny$hFR3M7zvCtLaitZ8uAL2KSi1iYVwokKhf/p0uwmdeEY=', '2024-06-12 15:24:39.616552', 0, 'Honey_Lou', '', '', 'Honeyloulito@gmail.com', 0, 1, '2024-06-12 15:24:39.039510', 'H12545', 'Honey Lou Rusiana Lito', 'Third Year', '123654789'),
(22, 'pbkdf2_sha256$720000$l23ipO8uycLf8owGy4H6gR$pIe5EIgJUXTHpj10kdtkhV6aDLEAXyLcuBAZn/RFMr0=', '2024-06-12 15:55:21.421023', 0, 'testagain', '', '', 'testagain@gmail.com', 0, 1, '2024-06-12 15:55:20.795439', 'testagain', 'testagain', 'testagain-3', '123654789'),
(23, 'pbkdf2_sha256$720000$IGscr3drzamLc9XDVoTHcZ$0cJ/XTzj0l+cU/njxrYw6v8WICiDwJEtp9jPK6L3P9Y=', '2024-06-12 16:07:25.773937', 0, 'daff', '', '', 'daff@gmail.com', 0, 1, '2024-06-12 16:07:25.133844', 'd', 'd', 'd', 'd'),
(24, 'pbkdf2_sha256$720000$XM2RUfylmWg4WgOVmcV3ue$SrY3/Hd8uxYG3lhvr9P7I5DZ1AEetyziKfGnTEQBpY0=', '2024-06-12 16:14:19.153429', 0, 'newacc', '', '', 'newacc@gmail.com', 0, 1, '2024-06-12 16:14:18.523031', 'newacc', 'newacc', 'newacc-3', '123654789'),
(25, 'pbkdf2_sha256$720000$LMzQQri8082vUdMG9QurID$FGWFd+Jmsfai2UaHF45HVWaJ/xDWDq+WNbPTp8tpPZA=', '2024-06-12 16:29:28.823804', 0, 'Khadaffe', '', '', 'khadaffesulaiman14@gmail.com', 0, 1, '2024-06-12 16:29:28.230507', 'C1478521', 'Khadaffe Abubakar Sulaiman', 'First Year', '123654789'),
(26, 'pbkdf2_sha256$720000$0XTTfyqmvlzWW4pTATkpg6$woyLOIVN2Vvx8BvVcVsVvESqG6U0Brflv9/g7Zd/ggs=', '2024-06-12 16:55:28.240845', 0, 'csrf', '', '', 'csrf@gmail.com', 0, 1, '2024-06-12 16:55:27.521882', 'csrf13', 'csrf', 'csrf', '123654789'),
(27, 'pbkdf2_sha256$720000$v9GKnNtskmTFg09Pxemw6E$AEIigQX0MbgFPE8E9bcqHpBtd5AC8n0IP7oFX6tatw0=', '2024-06-12 18:48:28.036172', 0, 'Student', '', '', 'Student@gmail.com', 0, 1, '2024-06-12 17:06:11.125042', 'Student', 'Student', 'Student-3', '123654789'),
(28, 'pbkdf2_sha256$720000$gBawv6UBUJPeisJTu4JKG8$MOezf03nge1rME5SU/C/K+4h8DTSFncMxJMPYsZBzhk=', '2024-06-12 17:45:15.413856', 0, 'testacc', '', '', 'testacc@gmail.com', 0, 1, '2024-06-12 17:36:24.924354', 'testacc', 'testacc', 'testacc', '123654789'),
(29, 'pbkdf2_sha256$720000$7WROF9AfmG2f9LHISKyMgI$G3TNPJwMS/uvdZEuyJxJd/XUWY91IpwoFt2Ic9m8o4g=', '2024-06-12 17:46:38.739953', 0, 'KCprsnlcc10', '', '', 'paolo.mendoza@example.com', 0, 1, '2024-06-12 17:46:37.868512', 'C667788', 'Mendoza, Paolo D.', 'Fourth Year', '+639954445566'),
(30, 'pbkdf2_sha256$720000$Sv1PTIz0W23gnpNbigrrT5$7W5S9IyCEAI3G6zjk9CKsspT8gxtSI5G4e38jIFWy8A=', '2024-06-12 18:35:06.104418', 0, 'KCprsnlcc9', '', '', 'julia.ramirez@example.com', 0, 1, '2024-06-12 18:31:03.767416', 'C334455', 'Ramirez, Julia H.', 'Third Year', '+639953334455'),
(31, 'pbkdf2_sha256$720000$7vHt98rO0YagrjiqhtcSKe$ksl4CBQAY+kex/Nck1xae9mowkTW1rSAm0ftJkZ17Eo=', '2024-06-13 04:17:36.430026', 0, 'KCprsnlcc8', '', '', 'carlo.bautista@example.com', 0, 1, '2024-06-12 18:36:37.043696', 'C112233', 'Bautista, Carlo V.', 'Second Year', '+639952223344'),
(32, 'pbkdf2_sha256$720000$9lZPturdrM1Av1JgAZtGHs$+2JfQgK7ptJ5IKuwixP1f5sh8jitfSsYteyaxz6rUYk=', '2024-06-13 02:27:28.568606', 0, '44', '', '', '44@gmail.com', 0, 1, '2024-06-13 02:27:27.985861', '4', '4', '4', '4'),
(33, 'pbkdf2_sha256$720000$NcyHNFMy1UmvVjiB7lS17u$HpAcMNfFyRIzIBdhDZjrbzCNypigFYuWxCpG5o3JbJw=', '2024-06-13 04:21:47.026750', 0, 'KCprsnlcc11', '', '', 'kcpersonalacc1@gmail.com', 0, 1, '2024-06-13 04:20:56.180422', 'C2100771', 'c', 'c', '123'),
(34, 'pbkdf2_sha256$720000$Er4dAhjObkoixe6Espnvc1$V2S7OyUIpPidS/6NoHBxD0p0jIDW3aRm7bTCI/ijCcc=', '2024-06-13 05:51:58.348578', 0, 'Khadaffe_14', '', '', 'khadaffesulaiman_14@gmail.com', 0, 1, '2024-06-13 04:31:19.696977', 'C210078', 'Khadaffe Abubakar Sulaiman', 'Third Year', '123654789'),
(37, 'pbkdf2_sha256$720000$GD12wnVKevATu9FlFx4QpH$zsgP5k+3Vepv0U/yvoaoO8KRoV7iBeZKbowG71HpmgI=', '2024-06-13 06:28:08.595792', 0, 'Newly', '', '', 'Newly@gmail.com', 0, 1, '2024-06-13 06:27:55.426746', 'NewAccount', 'NewAccount', 'NewAccount', 'NewAccount'),
(38, 'pbkdf2_sha256$720000$XE8IwpqKO38R9GOCjcGd5I$SwaBijZkDOURuQ6NyZr3Zmp1rjyl+8Eo9BknoDehE4o=', '2024-06-13 07:00:05.512120', 0, 'KCprsnlcc20', '', '', 'kcpersonalacc20@gmail.com', 0, 1, '2024-06-13 06:57:47.909316', 'C210090', 'Khadaffe Abubakar Sulaiman', 'Third Year', '+639949953785'),
(39, 'pbkdf2_sha256$720000$ubhPfHtl8zQQdE4LucLrYE$lS+BCE6rW8caBrKMAAHqLULnSz3G1izrfpltduwCFDI=', '2024-06-13 07:59:17.263537', 0, 'KCprsnlcc99', '', '', 'kcpersonalacc99@gmail.com', 0, 1, '2024-06-13 07:10:15.052173', 'C210099', 'Khadaffe Abubakar Sulaiman', 'Third Year', '+639949953785'),
(40, 'pbkdf2_sha256$720000$oxwVE2lLFY710UNU1KYriY$Bj3vS/VjVmmfCJuUbdD8C4fV45PA9dVxR2Egl0nNwkI=', '2024-06-13 13:23:38.224177', 0, 'testnut', '', '', 'testnewacc@gmail.com', 0, 1, '2024-06-13 13:23:31.729867', 'testnewacc', 'testnewacc', 'testnewacc', 'testnewacc'),
(41, 'pbkdf2_sha256$720000$eOqiqZM4LfZWVzDl6Z7hQ6$x03YQHYlPzAqIib46E/BhnZt1ZYK4FrUvHYUr/vuDUo=', '2024-06-13 16:34:20.388951', 0, 'sex', '', '', 'sex@gmail.com', 0, 1, '2024-06-13 16:34:03.183555', 'sex', 'sex', 'sex', 'sex'),
(42, 'pbkdf2_sha256$720000$EjUxbbtY4nAwUHAlYoXCar$VwuJh6SdQQGxQblq0HV4iwFTwO4k4sPSac9LCAMK9D0=', NULL, 0, 'KCprsnlccnew', '', '', 'KCprsnlcc@gmail.com', 0, 1, '2024-06-14 16:25:53.013844', 'C21007779', 'KCprsnlcc', 'KCprsnlcc', '123654789');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `main_customuser`
--
ALTER TABLE `main_customuser`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `student_id` (`student_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `main_customuser`
--
ALTER TABLE `main_customuser`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=43;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
