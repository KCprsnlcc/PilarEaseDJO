-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Aug 18, 2024 at 05:32 AM
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
-- Table structure for table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add content type', 4, 'add_contenttype'),
(14, 'Can change content type', 4, 'change_contenttype'),
(15, 'Can delete content type', 4, 'delete_contenttype'),
(16, 'Can view content type', 4, 'view_contenttype'),
(17, 'Can add session', 5, 'add_session'),
(18, 'Can change session', 5, 'change_session'),
(19, 'Can delete session', 5, 'delete_session'),
(20, 'Can view session', 5, 'view_session'),
(21, 'Can add user', 6, 'add_customuser'),
(22, 'Can change user', 6, 'change_customuser'),
(23, 'Can delete user', 6, 'delete_customuser'),
(24, 'Can view user', 6, 'view_customuser'),
(25, 'Can add user profile', 7, 'add_userprofile'),
(26, 'Can change user profile', 7, 'change_userprofile'),
(27, 'Can delete user profile', 7, 'delete_userprofile'),
(28, 'Can view user profile', 7, 'view_userprofile'),
(29, 'Can add status', 8, 'add_status'),
(30, 'Can change status', 8, 'change_status'),
(31, 'Can delete status', 8, 'delete_status'),
(32, 'Can view status', 8, 'view_status'),
(33, 'Can add reply', 9, 'add_reply'),
(34, 'Can change reply', 9, 'change_reply'),
(35, 'Can delete reply', 9, 'delete_reply'),
(36, 'Can view reply', 9, 'view_reply'),
(37, 'Can add contact us', 10, 'add_contactus'),
(38, 'Can change contact us', 10, 'change_contactus'),
(39, 'Can delete contact us', 10, 'delete_contactus'),
(40, 'Can view contact us', 10, 'view_contactus'),
(41, 'Can add notification', 11, 'add_notification'),
(42, 'Can change notification', 11, 'change_notification'),
(43, 'Can delete notification', 11, 'delete_notification'),
(44, 'Can view notification', 11, 'view_notification');

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'contenttypes', 'contenttype'),
(10, 'main', 'contactus'),
(6, 'main', 'customuser'),
(11, 'main', 'notification'),
(9, 'main', 'reply'),
(8, 'main', 'status'),
(7, 'main', 'userprofile'),
(5, 'sessions', 'session');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2024-06-28 01:40:46.584721'),
(2, 'contenttypes', '0002_remove_content_type_name', '2024-06-28 01:40:46.647332'),
(3, 'auth', '0001_initial', '2024-06-28 01:40:46.832120'),
(4, 'auth', '0002_alter_permission_name_max_length', '2024-06-28 01:40:46.876689'),
(5, 'auth', '0003_alter_user_email_max_length', '2024-06-28 01:40:46.882629'),
(6, 'auth', '0004_alter_user_username_opts', '2024-06-28 01:40:46.888493'),
(7, 'auth', '0005_alter_user_last_login_null', '2024-06-28 01:40:46.894362'),
(8, 'auth', '0006_require_contenttypes_0002', '2024-06-28 01:40:46.896315'),
(9, 'auth', '0007_alter_validators_add_error_messages', '2024-06-28 01:40:46.902185'),
(10, 'auth', '0008_alter_user_username_max_length', '2024-06-28 01:40:46.909027'),
(11, 'auth', '0009_alter_user_last_name_max_length', '2024-06-28 01:40:46.913914'),
(12, 'auth', '0010_alter_group_name_max_length', '2024-06-28 01:40:46.928580'),
(13, 'auth', '0011_update_proxy_permissions', '2024-06-28 01:40:46.935427'),
(14, 'auth', '0012_alter_user_first_name_max_length', '2024-06-28 01:40:46.941293'),
(15, 'main', '0001_initial', '2024-06-28 01:40:47.234609'),
(16, 'admin', '0001_initial', '2024-06-28 01:40:47.341177'),
(17, 'admin', '0002_logentry_remove_auto_add', '2024-06-28 01:40:47.349027'),
(18, 'admin', '0003_logentry_add_action_flag_choices', '2024-06-28 01:40:47.360761'),
(19, 'sessions', '0001_initial', '2024-06-28 01:40:47.392047'),
(20, 'main', '0002_remove_userprofile_avatar_url', '2024-06-28 05:14:35.834165'),
(21, 'main', '0003_status', '2024-06-29 16:52:51.687414'),
(22, 'main', '0004_alter_status_emotion_alter_status_title', '2024-06-29 17:55:19.218085'),
(23, 'main', '0005_status_plain_description', '2024-06-30 03:21:20.887309'),
(24, 'main', '0006_reply', '2024-07-01 02:51:36.691937'),
(25, 'main', '0007_contactus', '2024-07-01 11:34:56.729002'),
(26, 'main', '0008_notification', '2024-07-01 16:19:57.298344'),
(27, 'main', '0009_rename_read_notification_is_read_and_more', '2024-07-01 17:01:23.693088'),
(28, 'admin_tools', '0001_initial', '2024-08-03 23:12:27.652409'),
(29, 'admin_tools', '0002_delete_adminuser', '2024-08-03 23:12:27.667109'),
(30, 'main', '0010_delete_notification', '2024-08-03 23:12:27.677865'),
(31, 'main', '0011_customuser_is_counselor', '2024-08-03 23:12:27.959085'),
(32, 'main', '0012_status_confidence_scores', '2024-08-03 23:12:27.988463'),
(33, 'main', '0013_remove_status_confidence_scores', '2024-08-03 23:12:28.010952'),
(34, 'main', '0014_status_anger_status_disgust_status_fear_and_more', '2024-08-03 23:12:28.141691'),
(35, 'main', '0015_alter_status_plain_description_alter_status_title', '2024-08-03 23:12:29.117951'),
(36, 'main', '0016_status_neutral', '2024-08-03 23:12:29.514997'),
(37, 'main', '0017_remove_status_neutral', '2024-08-03 23:12:29.535527'),
(38, 'main', '0018_status_neutral', '2024-08-03 23:12:29.567791'),
(39, 'main', '0019_status_anger_percentage_status_disgust_percentage_and_more', '2024-08-04 04:07:27.961571'),
(40, 'main', '0020_customuser_block_duration_customuser_block_reason', '2024-08-07 17:23:11.106304');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('051cewqwxw3v74myuy9x0qona27oh9dm', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sViiE:FSUf52HaW5IDv9dIr2I_unrGzeD6iY-4Xvg5bFj8P_A', '2024-07-22 02:53:42.726467'),
('0assopddxr3ehhq55fozt1qqzn2e3byr', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNVVB:Oxw9swH_1WRds6vxEyJ2sZ4pYsRAXezCricYr8aN2lM', '2024-06-29 11:10:17.609778'),
('0dg0855fspg1a54z12v69krtdy08b0db', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNSQE:pXrlMo620MoSPGhDI0HyoDcRF83yrJLvutQ6uegliCU', '2024-06-29 07:52:58.084637'),
('0kxanxoqw8yjw5tzlu1v4uvy6hgi7d1q', '.eJxVjDEOwjAMRe-SGUXFcQJhZO8ZKie2SQGlUtNOiLtDpQ6w_vfef5mB1qUMa5N5GNlczNEcfrdE-SF1A3yneptsnuoyj8luit1ps_3E8rzu7t9BoVa-dYgRMYCe1GmGgLkDiOCFWFL2SC4oagqJmbyeGVOn5FzGED2ogJj3B-pkOJo:1sN1HA:9yOrQe8T1vGnGkMDhz1rla24SoAgCYdUiR_FgRXP-rY', '2024-06-28 02:53:48.624487'),
('0ulyqv0ibw9uar0kbraqmiwo0g8ji8rz', '.eJxVjDEOwjAMRe-SGUXFcQJhZO8ZKie2SQGlUtNOiLtDpQ6w_vfef5mB1qUMa5N5GNlczNEcfrdE-SF1A3yneptsnuoyj8luit1ps_3E8rzu7t9BoVa-dYgRMYCe1GmGgLkDiOCFWFL2SC4oagqJmbyeGVOn5FzGED2ogJj3B-pkOJo:1sN1El:YMqsAkp8qDUeONzSper6gBsa8AzigkHKYYjLVndUG3c', '2024-06-28 02:51:19.290093'),
('0zxw4pmtpbnmqjqti1e5tpe5qiv2rznr', '.eJxVjDEOwjAMRe-SGUXFcQJhZO8ZKie2SQGlUtNOiLtDpQ6w_vfef5mB1qUMa5N5GNlczNEcfrdE-SF1A3yneptsnuoyj8luit1ps_3E8rzu7t9BoVa-dYgRMYCe1GmGgLkDiOCFWFL2SC4oagqJmbyeGVOn5FzGED2ogJj3B-pkOJo:1sN0d8:vgDQZD5hnYtjuK6mIOjZkPXPhzNkkI68hsssWNyV45A', '2024-06-28 02:12:26.548707'),
('139qa806o7tosq08phy1jm7l7rpewxft', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNrLD:FMORn-Zy9dWGAhBLUQwuTXNhws5FV3dL9ecH88w_nqU', '2024-06-30 10:29:27.951749'),
('14gboze43l0nuq4p5rd1byxrm5810lrn', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNkzd:e5Gg_qPG5VEQSL6SrT0c-Fh1jSG1jR9Ix4OZs0etj3E', '2024-06-30 03:42:45.323051'),
('1imu06vniieyxqymliwjk92m70mdkusc', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNBZX:zmCCMGCIraM3UExg-tgmn7IjmiiTXbatJ5dBolut_Z8', '2024-06-28 13:53:27.933044'),
('1stlemegvmaftrr1psmaz9ctxapysd2q', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sazLj:P3J3TIg2bEkFDsz9vT0WySeVqJRI_KCr9h0p0A7FUps', '2024-08-05 15:40:15.922284'),
('25c1lo755k6osh6bpqnnuv7zt7epkn25', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNVe5:USKLCeAJeuLkKfTXYYViQpuJIJF6py8kB0D1tX_I1oE', '2024-06-29 11:19:29.239347'),
('2b5l5cfalsy4d57j1jgpq2kqec2ag1yw', '.eJxVjEEOgjAQRe_StWnaTjuAS_eegQwzg6CmTSisjHdXEha6_e-9_zI9bevUb1WXfhZzNh7M6XcciB-adyJ3yrdiueR1mQe7K_ag1V6L6PNyuH8HE9XpW6uyoKeIkTmoNA7BATmIwadIPkoaPTaqrkuKioHBjQhButi23cjevD8D8zed:1sQli7:H-HyyUcY2LJRlDuPAuIbsa6QVFJBBXz0i16WK_8HaQI', '2024-07-08 11:05:07.801255'),
('2bvh561efsqymahicbxul4l37e4dm0gc', '.eJxVjDkOwjAUBe_iGlle9BObkp4zWH-xcQA5UpxUiLtDpBTQvpl5L5VwW2vael7SJOqsrDr9boT8yG0Hcsd2mzXPbV0m0ruiD9r1dZb8vBzu30HFXr91QDCOsBT04h1GEyXEAmSARy_RSiESKyNQyIzODZAZBmD0zokJXr0_A104hQ:1sN5Yz:3_NY19iLFa3VQWTrEuCk9ZXbjLx36gSUSdwLbb454zA', '2024-06-28 07:28:29.415730'),
('2c2ken192sb77pvu55qd0f3idx7vx5l9', '.eJxVjMsOwiAQRf-FtSEDhXZw6d5vaIZhkKqBpI-V8d-1SRe6veec-1IjbWsZt0XmcUrqrIxXp98xEj-k7iTdqd6a5lbXeYp6V_RBF31tSZ6Xw_07KLSUb51xAO58IEOewCJ7IAcOmLPxPgVEC0HQ9nagvsvRYUgIwUlmiVlQvT_v3zfk:1saZrA:keiJmfSGjVqWxSMa-0p85MwfSuNotS9kuEEp2G5e4LI', '2024-08-04 12:27:00.436902'),
('2hntgmmb4ldhdn5n4jdeuumadsu7wm9l', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sOx4L:tC-nS8WfbBm9t526AzO89SELcXfHMZ68I1Z4K8o8a0I', '2024-07-03 10:48:33.988710'),
('2kp573w7skamrcq3ll74z1xctwqnhijj', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNVfW:J9wxVVkRPNxiY4OiDsPvsChAZ6ylJrgvzdagiHEmPWQ', '2024-06-29 11:20:58.786453'),
('2rp83xlzsxuday8r5dp519pqrert9tud', '.eJxVjEEOgjAQRe_StWnaTjuAS_eegQwzg6CmTSisjHdXEha6_e-9_zI9bevUb1WXfhZzNh7M6XcciB-adyJ3yrdiueR1mQe7K_ag1V6L6PNyuH8HE9XpW6uyoKeIkTmoNA7BATmIwadIPkoaPTaqrkuKioHBjQhButi23cjevD8D8zed:1sOvnG:ka2TjbEsiCd5F7ZKtatPIRl6azp1fgnVE86XstrzyZk', '2024-07-03 09:26:50.916430'),
('2sulivfgod47vxfd8qdf9bdbp3pg1svm', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sQlmq:BMUCpJrJ7CPDpcvoMsNCTl6LAMPO3Vu14Qd5FQwmhCg', '2024-07-08 11:10:00.422267'),
('397wp3pi43h6v7stwgxcw8n5e18z968y', '.eJxVjDEOwjAMRe-SGUXFcQJhZO8ZKie2SQGlUtNOiLtDpQ6w_vfef5mB1qUMa5N5GNlczNEcfrdE-SF1A3yneptsnuoyj8luit1ps_3E8rzu7t9BoVa-dYgRMYCe1GmGgLkDiOCFWFL2SC4oagqJmbyeGVOn5FzGED2ogJj3B-pkOJo:1sN3h5:upRa1MY8f3NO0QWRoFSQj6hn4QJSzEJZPZjY_RxoATU', '2024-06-28 05:28:43.924374'),
('3bghnumnk6byg2sph8umshyc65hst3a5', '.eJxVjDEOwjAMRe-SGUXFcQJhZO8ZKie2SQGlUtNOiLtDpQ6w_vfef5mB1qUMa5N5GNlczNEcfrdE-SF1A3yneptsnuoyj8luit1ps_3E8rzu7t9BoVa-dYgRMYCe1GmGgLkDiOCFWFL2SC4oagqJmbyeGVOn5FzGED2ogJj3B-pkOJo:1sN2y7:rAHEdxfLP3u_lHOT-OVnBz4uZuBg22Xee3wHwI9gnBw', '2024-06-28 04:42:15.932224'),
('3e4cvqx62qe6xedlwg0x6wkn7ok6lyus', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNYQA:vyjM-7lmJnUCZRtOB5vpljk_12aM7cO46d4G7vUDW6w', '2024-06-29 14:17:18.807528'),
('3ewx790qjqv2i7sduhbf4z4ucfnsgvuo', '.eJxVjDEOwjAMRe-SGUXFcQJhZO8ZKie2SQGlUtNOiLtDpQ6w_vfef5mB1qUMa5N5GNlczNEcfrdE-SF1A3yneptsnuoyj8luit1ps_3E8rzu7t9BoVa-dYgRMYCe1GmGgLkDiOCFWFL2SC4oagqJmbyeGVOn5FzGED2ogJj3B-pkOJo:1sN0mT:g3FwCHVEuJXoQ2QTBGcyVn7pik81uB9q9Sm7gCbcrFI', '2024-06-28 02:22:05.218762'),
('3fnnhbo6519mrnrs5nasp0qn9cd5z7jt', '.eJxVjDkOwjAUBe_iGlle9BObkp4zWH-xcQA5UpxUiLtDpBTQvpl5L5VwW2vael7SJOqsrDr9boT8yG0Hcsd2mzXPbV0m0ruiD9r1dZb8vBzu30HFXr91QDCOsBT04h1GEyXEAmSARy_RSiESKyNQyIzODZAZBmD0zokJXr0_A104hQ:1sN4ni:VLJ4jxKpGPfDRh0e2SnL3QoojLC9rfnTzNUg4XMSwoU', '2024-06-28 06:39:38.388676'),
('3lr0sz5ecmkoa7j9n27ghsy9jnzpavoc', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNfuv:uz95EznGTy3hW02Cbxf3aIFJOZJ9rUhLlm8wQgv4XpA', '2024-06-29 22:17:33.128254'),
('3p21y8ossqneh34btfxb8l1fg6l1xr5e', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNoY5:ASs-91vzHDxutnNRNI_kzL2lOM96fYsoRaw2GbZk1gQ', '2024-06-30 07:30:33.797608'),
('3rwcsmech5z7fz3lh7bql5xq15r1yzn6', '.eJxVjEEOgjAQRe_StWnaTjuAS_eegQwzg6CmTSisjHdXEha6_e-9_zI9bevUb1WXfhZzNh7M6XcciB-adyJ3yrdiueR1mQe7K_ag1V6L6PNyuH8HE9XpW6uyoKeIkTmoNA7BATmIwadIPkoaPTaqrkuKioHBjQhButi23cjevD8D8zed:1sQfz1:cdSOA22b7yTWh06dzkm5-SpVdRnxj7gJ8A1GG1w4MfI', '2024-07-08 04:58:11.197656'),
('3srlnhlid5y2feytc1di30p5jkn21ti1', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sb0L9:6jS0HI2prwxxxbZMa4Dp0UNwmq4uQHjcHm4dY3uD6tc', '2024-08-05 16:43:43.664962'),
('3xq1pkdmcjm34zyz5lzwip8yqjcc3p7f', '.eJxVjDsOwjAQBe_iGllee_2jpM8ZLH8WHEC2FCcV4u4QKQW0b2bei4W4rTVsg5YwF3ZmAOz0O6aYH9R2Uu6x3TrPva3LnPiu8IMOPvVCz8vh_h3UOOq3tgrRYAKTtbcuZkcSBWhnkYyxxicPQjtzzeStkAmkA1UISRQlbNGavT_K2DaY:1sNzRi:MF51mjL2W_rRqIPERSth7FEsXnmA8JBeH0XY1Y-sEms', '2024-06-30 19:08:42.397047'),
('44vtrksbiei8rv29stq2kyzmcv8jcu0e', '.eJxVjDEOwjAMRe-SGUXFcQJhZO8ZKie2SQGlUtNOiLtDpQ6w_vfef5mB1qUMa5N5GNlczNEcfrdE-SF1A3yneptsnuoyj8luit1ps_3E8rzu7t9BoVa-dYgRMYCe1GmGgLkDiOCFWFL2SC4oagqJmbyeGVOn5FzGED2ogJj3B-pkOJo:1sN4CA:W4-M88WZ2kj5IvYI9N8UW2d0REjp0MiBXobjGAclIpc', '2024-06-28 06:00:50.595922'),
('46q494oziiqcod5ipw67w3n0oic181xi', '.eJxVjEEOwiAQRe_C2hCgDExduvcMZIBBqoYmpV0Z765NutDtf-_9lwi0rTVsnZcwZXEWXpx-t0jpwW0H-U7tNss0t3WZotwVedAur3Pm5-Vw_w4q9fqtUVlnC0JBcspFixE0QaJYRq_BERHbQYPC7B2DMglzGU3hIaJnzka8P9tZOBQ:1sNyew:gIICgiHM4iyzLWUAwgZ3VhTb31n3vHop2rZlqqSnUQ4', '2024-06-30 18:18:18.817056'),
('4cj3wxatiuk2gcc11zkwiag0krdo0s9w', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNVfV:eC_M1ttZlezf_9uNYA1IITwc_IS7vd5Ys-vwpaTJdFg', '2024-06-29 11:20:57.777988'),
('4ktdjmoi7bui073k2ca9kwe4ngewm4hm', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNVfW:J9wxVVkRPNxiY4OiDsPvsChAZ6ylJrgvzdagiHEmPWQ', '2024-06-29 11:20:58.077825'),
('4ovrbotwwbpnb2q5bq1zkfmstcgy9dwv', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNeec:gU_XHRot5rOd4SPxpL22xbgmW4XnzEuh10c4fdk66WQ', '2024-06-29 20:56:38.432791'),
('57hu0yx3azm4vy4jtocckg4g9o5fs081', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNX4r:7WPfW8oQfRuV_HpznahXwQY3ZGnZpAvQPX-tGR4N2-4', '2024-06-29 12:51:13.952327'),
('5j0t7sg1en8k0ayuyeralpygo1hc0h20', '.eJxVjDkOwjAUBe_iGlle9BObkp4zWH-xcQA5UpxUiLtDpBTQvpl5L5VwW2vael7SJOqsrDr9boT8yG0Hcsd2mzXPbV0m0ruiD9r1dZb8vBzu30HFXr91QDCOsBT04h1GEyXEAmSARy_RSiESKyNQyIzODZAZBmD0zokJXr0_A104hQ:1sN8Yh:H-Tw6v7r_utzh55QuEveydH2t6R_8qz0yzZo0asxZ40', '2024-06-28 10:40:23.059206'),
('5x9dnnt6s2eps8jpmi84v6apm6jb16ct', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNpMH:7pir_LpRYOiLebSEFnfOioSvKcPoTWHI1PKcXocy3vE', '2024-06-30 08:22:25.171235'),
('6a7acud8ldper33drpwbcxr7tn50pb2t', '.eJxVjEEOgjAQRe_StWnaTjuAS_eegQwzg6CmTSisjHdXEha6_e-9_zI9bevUb1WXfhZzNh7M6XcciB-adyJ3yrdiueR1mQe7K_ag1V6L6PNyuH8HE9XpW6uyoKeIkTmoNA7BATmIwadIPkoaPTaqrkuKioHBjQhButi23cjevD8D8zed:1sOSPr:kzF5QmUdG0ziIBYrwPxypwsMOfs_kAXfGOXHBcPBgu4', '2024-07-02 02:04:43.830837'),
('6qo1v29vlf7ifhq0mfew4r7flxovc480', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNEo3:WJzJpmED9_UBqP6C4G50e9uZhF0UUSBzt7dS68DL3EU', '2024-06-28 17:20:39.585807'),
('6uj59ajp1z968pt0gjn4zzmoe9mpoabl', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNgPZ:4wh6aqnD7HJtMDnCycb-O4qV7UQme2Yysrlvy2aKA34', '2024-06-29 22:49:13.494661'),
('6ven4rb0lp67w9epy93zli09juokcvzf', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNW4S:4t-14Pq9aqBqpm2x2nZVzUUGl8N2YIH_aY1Z43H4uBY', '2024-06-29 11:46:44.622750'),
('6zbqdfxfzhjddkwiyv9yv0dynb0a1myb', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sPCS7:yMEddV3mNRLwQPJMbAG-rAlE_ifX2Lwxjg5h4MxjEKY', '2024-07-04 03:14:07.853813'),
('71yh2xkx4sad4mohv5rs1v255sgm70mm', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNmcr:ar7-XOOb3-yLbvOrvxCBuhm-ecLzNlGad2ZX9uF6hPU', '2024-06-30 05:27:21.733974'),
('7bhppn1gmnv62b5jyta0rrrrb3im1g0e', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNaLO:UWDq4ZfYPqEnJur8CEB3u5feOspM2n6mWuCmtDHjJuc', '2024-06-29 16:20:30.074482'),
('7cdcif9btbmf70b305kn9041jzwvv5sb', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNmdH:2fdobM18osSurc5jzwFdglTAr28rGQ8gN3j8QF2binU', '2024-06-30 05:27:47.305282'),
('7jka7474n9i7bldfm7p4a0zdu1u7nte6', '.eJxVjEEOgjAQRe_StWnaTjuAS_eegQwzg6CmTSisjHdXEha6_e-9_zI9bevUb1WXfhZzNh7M6XcciB-adyJ3yrdiueR1mQe7K_ag1V6L6PNyuH8HE9XpW6uyoKeIkTmoNA7BATmIwadIPkoaPTaqrkuKioHBjQhButi23cjevD8D8zed:1sOok2:QfOjsIgIYsO_5TYGPhnKBc88ugD3KPmGEaXDOOmqLoY', '2024-07-03 01:55:02.820811'),
('7k8e30mzpzbw8u06k5mla81rvufn21kl', '.eJxVjEEOgjAQRe_StWnaTjuAS_eegQwzg6CmTSisjHdXEha6_e-9_zI9bevUb1WXfhZzNh7M6XcciB-adyJ3yrdiueR1mQe7K_ag1V6L6PNyuH8HE9XpW6uyoKeIkTmoNA7BATmIwadIPkoaPTaqrkuKioHBjQhButi23cjevD8D8zed:1sOfdL:JToyNhRHd9W0CfFOhcU63sTZstDe5mCVIbNGtgM8upk', '2024-07-02 16:11:31.482835'),
('7nfw7nm4pl8eci4vaeyhfd1ni4rgccl7', '.eJxVjMsOwiAQRf-FtSEDhXZw6d5vaIZhkKqBpI-V8d-1SRe6veec-1IjbWsZt0XmcUrqrIxXp98xEj-k7iTdqd6a5lbXeYp6V_RBF31tSZ6Xw_07KLSUb51xAO58IEOewCJ7IAcOmLPxPgVEC0HQ9nagvsvRYUgIwUlmiVlQvT_v3zfk:1sbfns:tjGyC4zP9LQWVZRcpfeaX0WWtasnGTzSpgt9Xvsoxk8', '2024-08-07 13:00:08.386806'),
('7uddvyam2zskeqoxd5oflbo3tdfy3hxz', '.eJxVjEEOgjAQRe_StWnaTjuAS_eegQwzg6CmTSisjHdXEha6_e-9_zI9bevUb1WXfhZzNh7M6XcciB-adyJ3yrdiueR1mQe7K_ag1V6L6PNyuH8HE9XpW6uyoKeIkTmoNA7BATmIwadIPkoaPTaqrkuKioHBjQhButi23cjevD8D8zed:1sOsCA:VmkZG4i1SpFXNa3yseMntVCDqKxvgAksZXR0S_IFk2s', '2024-07-03 05:36:18.349842'),
('8768p1b0bfydiaom83zkd5agm7jkmohk', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNmct:xpnoEU4j2CY_1QMSMbk0VflPXBR688YgfQIM7JRcUqs', '2024-06-30 05:27:23.430957'),
('8c2f3ymghkvnywkkkucctigq8rk3q39l', '.eJxVjMsOwiAQRf-FtSEDhXZw6d5vaIZhkKqBpI-V8d-1SRe6veec-1IjbWsZt0XmcUrqrIxXp98xEj-k7iTdqd6a5lbXeYp6V_RBF31tSZ6Xw_07KLSUb51xAO58IEOewCJ7IAcOmLPxPgVEC0HQ9nagvsvRYUgIwUlmiVlQvT_v3zfk:1sbpTR:LLG4e7Qy9oyIdh7RvhSbYHS2ZDnQn33TeHD6qnZ6BOk', '2024-08-07 23:19:41.342427'),
('8jlu1kpx4w6d0wozllu0e5z679awz7d5', '.eJxVjDEOwjAMRe-SGUXFcQJhZO8ZKie2SQGlUtNOiLtDpQ6w_vfef5mB1qUMa5N5GNlczNEcfrdE-SF1A3yneptsnuoyj8luit1ps_3E8rzu7t9BoVa-dYgRMYCe1GmGgLkDiOCFWFL2SC4oagqJmbyeGVOn5FzGED2ogJj3B-pkOJo:1sN3b6:N50qKMcVleAorLZg7fmWpG4xda6SxXyuoRg5wRF9ek4', '2024-06-28 05:22:32.687084'),
('93wtdz7yk940tmukpdtceuwa4jep40y0', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1saz10:VUq2MoTbLXStH4QibtBhAEjyulBlAvodEgBR6QRY29A', '2024-08-05 15:18:50.788755'),
('9ewl9mbvz14d1u41fq21s5wr4k8h96y6', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sazQt:x0Jq-F9Y17QAcBMLPWClxNTDVTaNt12PNoshmrGj5kU', '2024-08-05 15:45:35.729659'),
('9jwusi0br9rbrwpjo8glczkzhdoi0sav', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sazGk:f_QN-mjNxP8Whb5JqN_99vUYOIWw3HnCMRaDEahS0o0', '2024-08-05 15:35:06.584570'),
('9yjc1vneiwn40qgcktg1pib7ua70g2a5', '.eJxVjEEOgjAQRe_StWnaTjuAS_eegQwzg6CmTSisjHdXEha6_e-9_zI9bevUb1WXfhZzNh7M6XcciB-adyJ3yrdiueR1mQe7K_ag1V6L6PNyuH8HE9XpW6uyoKeIkTmoNA7BATmIwadIPkoaPTaqrkuKioHBjQhButi23cjevD8D8zed:1sPD4c:QMI2dmtANNzfTAUm14pKKIPV6gcXR8TJjjXNyGfLXl0', '2024-07-04 03:53:54.148685'),
('a12fpsnite4n6z4cypyft1w7o3inl8wj', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNmcv:Shn6ngNDQuDZi5zS5P2hSEvO3UbJoIFOy1IRTENV6KU', '2024-06-30 05:27:25.182929'),
('aqg9gwj7fgvla48rxw8mkkpiaq85xlp0', '.eJxVjDkOwjAUBe_iGlle9BObkp4zWH-xcQA5UpxUiLtDpBTQvpl5L5VwW2vael7SJOqsrDr9boT8yG0Hcsd2mzXPbV0m0ruiD9r1dZb8vBzu30HFXr91QDCOsBT04h1GEyXEAmSARy_RSiESKyNQyIzODZAZBmD0zokJXr0_A104hQ:1sN4QJ:yB2ORuChooa7o6R5KYLU9wNFwYVvKXWxa6JAbHUrqkw', '2024-06-28 06:15:27.759345'),
('b8qwd83zz85w06w6t0lflk34fzb2ml9p', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNbAz:GvK2rVr8GfV5ce-_AJZ40DpUatD74GF5bpJ6IV47odg', '2024-06-29 17:13:49.538537'),
('bfy3i0ilqum7pyx41vo9g6okpvkyupyo', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNEsf:HZK30FoXi-FK9OMG5idqrq0hMwtjOhxqnL0ix8rD6Wk', '2024-06-28 17:25:25.047719'),
('bulqn9vqb23mdo8iabtv9k1ffyes0cff', '.eJxVjDkOwjAUBe_iGlle9BObkp4zWH-xcQA5UpxUiLtDpBTQvpl5L5VwW2vael7SJOqsrDr9boT8yG0Hcsd2mzXPbV0m0ruiD9r1dZb8vBzu30HFXr91QDCOsBT04h1GEyXEAmSARy_RSiESKyNQyIzODZAZBmD0zokJXr0_A104hQ:1sN6cT:JqICrG_WSauTIKqiF7azCaoVGpYWcNP0EN9vH4sZCyc', '2024-06-28 08:36:09.806313'),
('ccu3bm3p7kgh9q5r5syc1okw1porvush', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sOFNL:0Hhr0rN7B1l-_-Tas9VlXuRw0ShGXsjJbqhQfg4lPB4', '2024-07-01 12:09:15.582398'),
('cji2f0wrrfz68bj50pzxu7ascr07h14a', '.eJxVjDEOwjAMRe-SGUXFcQJhZO8ZKie2SQGlUtNOiLtDpQ6w_vfef5mB1qUMa5N5GNlczNEcfrdE-SF1A3yneptsnuoyj8luit1ps_3E8rzu7t9BoVa-dYgRMYCe1GmGgLkDiOCFWFL2SC4oagqJmbyeGVOn5FzGED2ogJj3B-pkOJo:1sN1NF:Blr3C2S9tn5ViFK9E9wEWNSXub3GaOjMegOoiQ0IRSQ', '2024-06-28 03:00:05.785876'),
('ck6eloxprwo77of6jahdr6n5nm4kdrmg', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNl9F:IIpsEYhVhk144aSlXk5BAVJDBa-pHLBoVUT7TWIT9oE', '2024-06-30 03:52:41.164313'),
('d682fxlze34cibcolnw72ikys0qc6xnl', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNrnv:13Ybdz1m9ziZPknMi5NpjgLJX-bpaXiJyTntO-YRSJ4', '2024-06-30 10:59:07.585732'),
('dfoi9dfkw198j4gyj7uzx2jlt3jmuyic', '.eJxVjEEOgjAQRe_StWnaTjuAS_eegQwzg6CmTSisjHdXEha6_e-9_zI9bevUb1WXfhZzNh7M6XcciB-adyJ3yrdiueR1mQe7K_ag1V6L6PNyuH8HE9XpW6uyoKeIkTmoNA7BATmIwadIPkoaPTaqrkuKioHBjQhButi23cjevD8D8zed:1sQln7:D6hDMOxBCMe-ub02c2AHVAxV9CXQb5x5sz6iFBn0xKk', '2024-07-08 11:10:17.536484'),
('dg3qdgr6k0lzttxfci8aq65xrrhxjakl', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sOx6B:KNrw1F1W5PCVO1HC_KS5FZdihp34ESQ0qpdHqOUaq6E', '2024-07-03 10:50:27.157840'),
('dijsafetmrzlo52de8qy3lhaliphs0u2', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNd0v:XNvglq9DWCVXeLoHadCc6TpJJ-8qQqGCDzRxtihxrQY', '2024-06-29 19:11:33.252321'),
('dj41iq4cnfccumuuj4lsq03ezbth68f0', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sPKLr:RmUZN1YytdrpNhGKqrcyR07sUi1yDPkOZroY_H3_2rg', '2024-07-04 11:40:11.025864'),
('do6ad7zlwfpnta59f8oc0aem8g1519rv', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNVfV:eC_M1ttZlezf_9uNYA1IITwc_IS7vd5Ys-vwpaTJdFg', '2024-06-29 11:20:57.566247'),
('dpx2dayket6apodq1meax3vg04enn5fu', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNpj1:qYAEGJGmDeXoE00V7fboqXKK-0Ca-XOkGkE71cFemUU', '2024-06-30 08:45:55.929616'),
('ds5sewb7jijv31w778oawzwzio9sqxf7', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNZ5h:LDF0GoRIixKA9xr4PKC_-C5HdnG8Ey2PuJQ3q6iy35E', '2024-06-29 15:00:13.506868'),
('dsc3q3q26x6glhszc1v5kf0re1weyhub', '.eJxVjMsOwiAQRf-FtSEDhXZw6d5vaIZhkKqBpI-V8d-1SRe6veec-1IjbWsZt0XmcUrqrIxXp98xEj-k7iTdqd6a5lbXeYp6V_RBF31tSZ6Xw_07KLSUb51xAO58IEOewCJ7IAcOmLPxPgVEC0HQ9nagvsvRYUgIwUlmiVlQvT_v3zfk:1sbg6D:q3vzPkyk3fd-DtzhKi8gai5y2FNazX4qW_AwfPovjug', '2024-08-07 13:19:05.270764'),
('dv1s6ho4eebleey41n6wntjs4t9zx1sz', '.eJxVjMsOwiAQRf-FtSEOb1y67zeQAQapGkhKuzL-uzbpQrf3nHNfLOC21rANWsKc2YWBYqffMWJ6UNtJvmO7dZ56W5c58l3hBx186pme18P9O6g46rcuDoqR1htHxpUIBSQqctolyDELLL6A0DaBQvImGym9NkqhILB49pq9PwjFN78:1sOKcV:pnh83IMJGcpmlbaCTh9ky8pF5ZJYxIhKHo_L9HlmOT0', '2024-07-01 17:45:15.140497'),
('dv6kg51d3znx1rac6r7cvgcmvv6999ed', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sOeN5:h2cJQfNHSzura_d6IIGkJxtz0J1W0QEGZ4I9n8u212Y', '2024-07-02 14:50:39.744475'),
('eapnd8e3liiqkvrwtt4nmcjyow0p54qp', '.eJxVjDkOwjAUBe_iGlle9BObkp4zWH-xcQA5UpxUiLtDpBTQvpl5L5VwW2vael7SJOqsrDr9boT8yG0Hcsd2mzXPbV0m0ruiD9r1dZb8vBzu30HFXr91QDCOsBT04h1GEyXEAmSARy_RSiESKyNQyIzODZAZBmD0zokJXr0_A104hQ:1sN4ky:boEvgJnW4P6vtPPQ3nmoPU01entNq0_3Sw1wKiHq15Y', '2024-06-28 06:36:48.528819'),
('ecf46mrmku6csgw55ojwj5ay6ev89uxc', '.eJxVjEEOgjAQRe_StWnaTjuAS_eegQwzg6CmTSisjHdXEha6_e-9_zI9bevUb1WXfhZzNh7M6XcciB-adyJ3yrdiueR1mQe7K_ag1V6L6PNyuH8HE9XpW6uyoKeIkTmoNA7BATmIwadIPkoaPTaqrkuKioHBjQhButi23cjevD8D8zed:1sViHB:4KYDmvlh1736v3AudySdMC7b1ZxFwwZH5EZDRxZ_Qtg', '2024-07-22 02:25:45.448000'),
('f3z23k7luk9h8q0ys3mmsm4agak0hzdm', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNVaK:KE2HfWW8G4_ihVto5mZ6nZt3XeAKBRlUO-SQc7_7OaI', '2024-06-29 11:15:36.354718'),
('f67pbefse5ju9t5n1t5hcw9h7g6pttna', '.eJxVjEEOgjAQRe_StWnaTjuAS_eegQwzg6CmTSisjHdXEha6_e-9_zI9bevUb1WXfhZzNh7M6XcciB-adyJ3yrdiueR1mQe7K_ag1V6L6PNyuH8HE9XpW6uyoKeIkTmoNA7BATmIwadIPkoaPTaqrkuKioHBjQhButi23cjevD8D8zed:1sOAKq:oOebVxMenCOUfrDGtHggEplIa6xCxUYoJM8D2XcTr_E', '2024-07-01 06:46:20.849910'),
('fbyb1bzua7xigql4e0kgg1dvdnohmj0z', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sOBNn:ArtCDM_jZnS_NmRDWlTp5BX1owvV5WVOXEK98OzuKSs', '2024-07-01 07:53:27.286147'),
('fd7lbqrpbpomp58gnkn6f2n47gfhtdpc', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNbBD:-PZp99cTdnuqMcEaynOP353NYNE8_aqFrwHUnB-uHLE', '2024-06-29 17:14:03.898141'),
('fdenyf0246mntcog8cmewsi9qv6l7t0s', '.eJxVjEEOwiAQRe_C2pCCCDMu3XsGMsCMVA1NSrsy3l2bdKHb_977LxVpXWpcO89xLOqsnDr8bonyg9sGyp3abdJ5ass8Jr0peqddX6fCz8vu_h1U6vVbiwV2BggsDAXTKSBgdig0CAehIgjFJosWk_fHHII4kuCRDVswwav3B-hdN98:1sNBQE:0X1zlP_pI6SCEyr9Ny11zk4RRACEN4APUjluZNK9NHs', '2024-06-28 13:43:50.455525'),
('fi7qu3zxnkpxl9gk9txypvk4a45c8i33', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNfGn:-qwM200Uz92q7SIaZNzzzf2GoE_nwdAVdpBV2fv_Rt8', '2024-06-29 21:36:05.551157'),
('fmocokuqwfmsmn1ag8nefyvm0s53f9bx', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNdh5:kTwO3-zgs1AsKEt6mXMBIG8vbE3diIJ9N_IVBeesuyQ', '2024-06-29 19:55:07.285711'),
('fon3yq8ujno5gencfo30tfis5rtnax6q', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNaTC:lCpr8Syw5GZGJSbCUGReXViA_whiJ6LSI0oeERkm600', '2024-06-29 16:28:34.049399'),
('fyhwa1v307r75cev0xgw8f9836466om5', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNVO1:olZBsW-iKksU8YylkgVoXbmBfMxgVlmAUcJbKV31PLE', '2024-06-29 11:02:53.730712'),
('g8x0zbet1mk9zvc4uq37puit5segikwm', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNDpq:Cb0nGkzKg5bQtCC5aMde4DEFI2Hjvm25Fr15o1Sm7EE', '2024-06-28 16:18:26.364149'),
('ggieje45y1f3ea4sa0h8d9y4fekvlt1z', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sazC4:TG8lDDuInldak46NkvHCwDmmlXWqtEygpWI-ag_OAT4', '2024-08-05 15:30:16.477566'),
('ggtsd7kp8hdxh3ij7mjz3bni9lsbp4yp', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNto4:165jTrgmiPlJPYwl_8VvQP2NDOsxd0pecPh594Pr5KI', '2024-06-30 13:07:24.403169'),
('gous33ulgkql2ogsgw2r4pbeoceg92wb', '.eJxVjDkOwjAUBe_iGlle9BObkp4zWH-xcQA5UpxUiLtDpBTQvpl5L5VwW2vael7SJOqsrDr9boT8yG0Hcsd2mzXPbV0m0ruiD9r1dZb8vBzu30HFXr91QDCOsBT04h1GEyXEAmSARy_RSiESKyNQyIzODZAZBmD0zokJXr0_A104hQ:1sN8ax:4rJLNXLbw703qE70MJNNE-mI_yhVcIl-Nocy1ThE6Kc', '2024-06-28 10:42:43.838238'),
('h6x7trwe8u5sqmiwo3r8tn3lfq5sgd98', '.eJxVjDkOwjAUBe_iGlle9BObkp4zWH-xcQA5UpxUiLtDpBTQvpl5L5VwW2vael7SJOqsrDr9boT8yG0Hcsd2mzXPbV0m0ruiD9r1dZb8vBzu30HFXr91QDCOsBT04h1GEyXEAmSARy_RSiESKyNQyIzODZAZBmD0zokJXr0_A104hQ:1sN7hY:3LfmyOalSK_kGOeBWMmJpz6dV--x4lAWUzQYAlvAucU', '2024-06-28 09:45:28.863854'),
('h92licjrym4cnjbds5yfzhx4yzv5oi0a', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNmcv:Shn6ngNDQuDZi5zS5P2hSEvO3UbJoIFOy1IRTENV6KU', '2024-06-30 05:27:25.429986'),
('hcdvvucblaxutzkh59wf1ik7ev3z5icq', '.eJxVjDEOwjAMRe-SGUXFcQJhZO8ZKie2SQGlUtNOiLtDpQ6w_vfef5mB1qUMa5N5GNlczNEcfrdE-SF1A3yneptsnuoyj8luit1ps_3E8rzu7t9BoVa-dYgRMYCe1GmGgLkDiOCFWFL2SC4oagqJmbyeGVOn5FzGED2ogJj3B-pkOJo:1sN3KX:LErO5TTDb4JHdQcXTMmS4nY2GwimbVhCP3j87WzzFxM', '2024-06-28 05:05:25.706632'),
('hg76r486f1qpgi35gptql8fsu3xohvcc', '.eJxVjDkOwjAUBe_iGlle9BObkp4zWH-xcQA5UpxUiLtDpBTQvpl5L5VwW2vael7SJOqsrDr9boT8yG0Hcsd2mzXPbV0m0ruiD9r1dZb8vBzu30HFXr91QDCOsBT04h1GEyXEAmSARy_RSiESKyNQyIzODZAZBmD0zokJXr0_A104hQ:1sN63Z:H-KzzGwRF9lxLc7Htv--nt9F9BQl2775GFQODv0wrJQ', '2024-06-28 08:00:05.588694'),
('hgyffnli81q1qp5bat03e8iffpjpdqny', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNaCH:zlirWhJPNCuYVKj6-1jZXqAMaOSQ1x89mdQ1cPQunik', '2024-06-29 16:11:05.509084'),
('hihv12oia6cf7trez7tk5leh3urigue3', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNVVd:DevlHBZPFQlRdaUGP2dDpZOI6GtMDahM39zV5BWegt4', '2024-06-29 11:10:45.678228'),
('hjsomnxx6ul7i31ww89enuy2wlt7czl5', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNZRG:NghO1AF-quHpG8kUIgCvR31L9MCCaxA54rFM1mpFdAU', '2024-06-29 15:22:30.697730'),
('hldygxac7wen4jfyojdf2jd5mpm11d35', '.eJxVjDkOwjAUBe_iGlle9BObkp4zWH-xcQA5UpxUiLtDpBTQvpl5L5VwW2vael7SJOqsrDr9boT8yG0Hcsd2mzXPbV0m0ruiD9r1dZb8vBzu30HFXr91QDCOsBT04h1GEyXEAmSARy_RSiESKyNQyIzODZAZBmD0zokJXr0_A104hQ:1sN588:MynCSIZ0jv1o9IbqfV2FYqj2nEYDQ6GYjrBW9suJFTE', '2024-06-28 07:00:44.882988'),
('hnzis9iw3y0rhs4k7kzk5nt184nn1oqy', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNqZs:-8Mn2_zb9xg3-p2vCbixgVPAQVDWmoEcBKwg9Ta7rhE', '2024-06-30 09:40:32.922311'),
('hrqbwp6s6mth8i9imavcbppx96g37drb', '.eJxVjEEOgjAQRe_StWnaTjuAS_eegQwzg6CmTSisjHdXEha6_e-9_zI9bevUb1WXfhZzNh7M6XcciB-adyJ3yrdiueR1mQe7K_ag1V6L6PNyuH8HE9XpW6uyoKeIkTmoNA7BATmIwadIPkoaPTaqrkuKioHBjQhButi23cjevD8D8zed:1sO9lR:SaPXDtNayyhYrw_ZuSbESrBpsbOn04t6kROFQR8evXo', '2024-07-01 06:09:45.238351'),
('hubbog661zwbk8vz0mlo2bq7udiap7v2', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNVfW:J9wxVVkRPNxiY4OiDsPvsChAZ6ylJrgvzdagiHEmPWQ', '2024-06-29 11:20:58.734637'),
('hvv109n7gp5wbfhay1i2x6d05v0ggnos', '.eJxVjDkOwjAUBe_iGlle9BObkp4zWH-xcQA5UpxUiLtDpBTQvpl5L5VwW2vael7SJOqsrDr9boT8yG0Hcsd2mzXPbV0m0ruiD9r1dZb8vBzu30HFXr91QDCOsBT04h1GEyXEAmSARy_RSiESKyNQyIzODZAZBmD0zokJXr0_A104hQ:1sN6sx:7yyR-tsmhsSK-IEXhiepTeOUCB5f6eFLv-OteqWQ3OM', '2024-06-28 08:53:11.473530'),
('hxg0vksexz0f9jjd2o7mtwm15q07wxgp', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNqOh:1EkPSAWvA2DXfRHTM5J0Yd5SLdp1vtNfhq_XjgNJQRI', '2024-06-30 09:28:59.624336'),
('hznyj4w0eizxx4y4x8zb64om5k3bskpn', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNmcv:Shn6ngNDQuDZi5zS5P2hSEvO3UbJoIFOy1IRTENV6KU', '2024-06-30 05:27:25.171195'),
('idzs7ekbwdwo8b4wr27os82vsuopilmq', '.eJxVjMsOwiAQRf-FtSEDhXZw6d5vaIZhkKqBpI-V8d-1SRe6veec-1IjbWsZt0XmcUrqrIxXp98xEj-k7iTdqd6a5lbXeYp6V_RBF31tSZ6Xw_07KLSUb51xAO58IEOewCJ7IAcOmLPxPgVEC0HQ9nagvsvRYUgIwUlmiVlQvT_v3zfk:1sbjqO:A818RZiPhflct6uedDbYjoPjzSDHLT0ReEWyE_vi-oo', '2024-08-07 17:19:00.405716'),
('ilg5bzkniu9blzzrivb5ehzxyfka3w0b', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNmcs:jIKnBtCg7ouLpIdQ05ZpcemueWy8KZyIW_Y8Ua44w1Y', '2024-06-30 05:27:22.600010'),
('inrqspm020x1k4d2heoq66nbkz2ejkdh', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNmcu:twsjtM13RDNO2Op8isZKVxLR7i5V4s-fZAIyiZddVs4', '2024-06-30 05:27:24.566674'),
('iyyx6os056dsjw8gdge80l4nxobkcxyu', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNZPR:cixFPxErTjIwVgUjduIBFvwk7YOGSrKw9SHybWg0jUw', '2024-06-29 15:20:37.990481'),
('j0g0xxnkwxvq5dnfkxylf8pr1o5spm5n', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNlOH:px0DQZ_rQVTY5sDNgAEjhyyeiK5asG6vfERk0oCHjh4', '2024-06-30 04:08:13.487376'),
('j9eqws3p96lheosp2cungdgjdl8s4062', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNnd2:9dAM0pUDrpgLr_RsNCVOdl8x4NZeoAjMAY-W9cITJmo', '2024-06-30 06:31:36.137322'),
('jcfi8zhzb3sod2kft87lxku0h7m98jv6', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNXL7:64Dtm4d21HFDBd395ESMsoIZFhHbbjxDRQXEAVy8q00', '2024-06-29 13:08:01.799609'),
('jehtf1hhlpee4fu3p883fznlqui4unie', '.eJxVjDEOwjAMRe-SGUXFcQJhZO8ZKie2SQGlUtNOiLtDpQ6w_vfef5mB1qUMa5N5GNlczNEcfrdE-SF1A3yneptsnuoyj8luit1ps_3E8rzu7t9BoVa-dYgRMYCe1GmGgLkDiOCFWFL2SC4oagqJmbyeGVOn5FzGED2ogJj3B-pkOJo:1sN2gH:Mdl1hFl2x1otva85v8_0wJ6UNzTKTD37E3iEcn8M8BU', '2024-06-28 04:23:49.238620'),
('jm2qzpq31kxfg6kn3856nt6qioju3iz7', '.eJxVjDEOwjAMRe-SGUXFcQJhZO8ZKie2SQGlUtNOiLtDpQ6w_vfef5mB1qUMa5N5GNlczNEcfrdE-SF1A3yneptsnuoyj8luit1ps_3E8rzu7t9BoVa-dYgRMYCe1GmGgLkDiOCFWFL2SC4oagqJmbyeGVOn5FzGED2ogJj3B-pkOJo:1sN3mr:nRIZeFNG1vJF5M3lx8_ndBJJW8ORdbjMzJHhDlmjvsc', '2024-06-28 05:34:41.480311'),
('jm4hfxzo0p867867wxsk8f9sf36b6a1v', '.eJxVjDEOwjAMRe-SGUXFcQJhZO8ZKie2SQGlUtNOiLtDpQ6w_vfef5mB1qUMa5N5GNlczNEcfrdE-SF1A3yneptsnuoyj8luit1ps_3E8rzu7t9BoVa-dYgRMYCe1GmGgLkDiOCFWFL2SC4oagqJmbyeGVOn5FzGED2ogJj3B-pkOJo:1sN3aL:T0qMW0JGGTU7UHN2OFrQP21PM3TAH1IBdx1HnVDwf0Q', '2024-06-28 05:21:45.851362'),
('jpbagznbb2ivl3e0kolpdcxb4zat1aol', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sQluM:wow3QdfvuJSjfxmmJ6KG3z27Rfwy2JE9i5R9O-ECOdg', '2024-07-08 11:17:46.780581'),
('jt38flkc8no8m2gnjd9hn82eo6lh8y22', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1saZzX:9pfWQMcqyfCtXCVOZ_QDxKnvVPUd17_vL0TukJk5IQs', '2024-08-04 12:35:39.400436'),
('k070s243o5qxe4aymtjq90z6ivaa0toa', '.eJxVjEEOwiAQRe_C2hCgDExduvcMZIBBqoYmpV0Z765NutDtf-_9lwi0rTVsnZcwZXEWXpx-t0jpwW0H-U7tNss0t3WZotwVedAur3Pm5-Vw_w4q9fqtUVlnC0JBcspFixE0QaJYRq_BERHbQYPC7B2DMglzGU3hIaJnzka8P9tZOBQ:1sNweO:dWBNgGi-KLsBwsvDfIVi345_1mt_0e9o5AupyozpeW4', '2024-06-30 16:09:36.127784'),
('k9cyneontub908e3j28ouaphoav80gui', '.eJxVjMsOwiAQRf-FtSEOb1y67zeQAQapGkhKuzL-uzbpQrf3nHNfLOC21rANWsKc2YWBYqffMWJ6UNtJvmO7dZ56W5c58l3hBx186pme18P9O6g46rcuDoqR1htHxpUIBSQqctolyDELLL6A0DaBQvImGym9NkqhILB49pq9PwjFN78:1sPCO1:0CLI4uAILHhc19f3o8iYPHGE9fC6xDlkBuEjeC0i7Js', '2024-07-04 03:09:53.862404'),
('kp4iu3668jwto3fxhf6fj2stlskm8e3l', '.eJxVjDEOwjAMRe-SGUXFcQJhZO8ZKie2SQGlUtNOiLtDpQ6w_vfef5mB1qUMa5N5GNlczNEcfrdE-SF1A3yneptsnuoyj8luit1ps_3E8rzu7t9BoVa-dYgRMYCe1GmGgLkDiOCFWFL2SC4oagqJmbyeGVOn5FzGED2ogJj3B-pkOJo:1sN2qy:oL4XutUCAKUyCXwfpWauL0cpTf1L4FU3z1-AInlXquQ', '2024-06-28 04:34:52.611770'),
('kswtr3ezhqij2gxtmo7qtl44pjs99arj', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNtCk:XhSVozZBqP-CiWQ5zdV2MxOTMZUVeUPvg3nC8W9GOA8', '2024-06-30 12:28:50.108620'),
('kyuavtl79sy6jq2obc5kyvnpgefz6emw', '.eJxVjDsOwjAQBe_iGll2En-Wkp4zWOvdBQeQI8VJhbg7iZQC2pl5760SrktJa5M5jazOqlOnX5aRnlJ3wQ-s90nTVJd5zHpP9GGbvk4sr8vR_h0UbGVbhxtnN8Ag0kcPaMG6PiBZzoE3CEGiAQFkizkgZjYUyYA33nfOG1KfL_ZwOD8:1sNAcC:bd_0EV7_WEE5kACztwPpkrC0lI9bHkYuve90av5_nZ8', '2024-06-28 12:52:08.476059'),
('lp0z2i0g5fovfj28sq36dke1k9hoi6gx', '.eJxVjEEOgjAQRe_StWnaTjuAS_eegQwzg6CmTSisjHdXEha6_e-9_zI9bevUb1WXfhZzNh7M6XcciB-adyJ3yrdiueR1mQe7K_ag1V6L6PNyuH8HE9XpW6uyoKeIkTmoNA7BATmIwadIPkoaPTaqrkuKioHBjQhButi23cjevD8D8zed:1sOV6o:M04RbFTDo7lwp6G2LR934jkkmo8WcvhzD2rJ-oVXv9k', '2024-07-02 04:57:14.597379'),
('lt8b45v5spb717ayct8xggrd17varfp6', '.eJxVjDkOwjAUBe_iGlmWF2JT0nMG6y_-OIAcKU6qiLtDpBTQvpl5m8qwLjWvvcx5ZHVRTp1-NwR6lrYDfkC7T5qmtswj6l3RB-36NnF5XQ_376BCr99aKHCCYAaS4iEFMZI8k7dntCFJtChcohtS8E4CWrYxGSsenAFCLOr9AQGFOKE:1sNBHm:b-IZAep_j_1l8qyt76UjnPUGkFVzZaSGBUEqlieubLo', '2024-06-28 13:35:06.583273'),
('m00ctqe4hqaxyufuvlc5vlc9pmo9zmyy', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNfns:9RXJeuve_38w3SF2Am-YZfMeIacnmkTq_2MXM0TA-sc', '2024-06-29 22:10:16.520279'),
('m2l1dcb6hvi16afeusiat3ad29zdtohb', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNoVM:tfnWhjmSEpmqFF5aPms-Oycf8VnHpMoDSzdJIfoZ41I', '2024-06-30 07:27:44.359954'),
('m6vv7gyhqtub8rnathihfnu5jtirepei', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNunj:rQaSa_ISDPAJZue0oHhqfp77QS91nm5Qst23sa2jUUk', '2024-06-30 14:11:07.459929'),
('ma2uw3hfh9c4qleio1rrue80zhacndw8', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNmQS:Bv-TV8jSuQ78JDi46kGLvk3P49WfbL58Mjleg3YcBdc', '2024-06-30 05:14:32.501330'),
('mklly4xg6dtcis9wouxz9zi9chgxzf20', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sfKyw:6zyT7uCLC_rR7b0V8aw2twlWoobfY9o4RN-orgpaXbQ', '2024-08-17 15:34:42.054159'),
('mtfkdrpxoztztst2setxx4nfgo652hs9', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNdBC:qzxdfpLTCCJQ7MVX7n1fc-NEcKuBsAHVFerYiMofpxc', '2024-06-29 19:22:10.970804'),
('mv504zbvzu3dw0p9xz6xnf8xh4dt86zu', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNfoK:vGpzsfmpc3t4lY_GK9IfJ7ySLQwuDOMfg9MoQ0xtpG4', '2024-06-29 22:10:44.639468'),
('nch7tudm5s2ivkptekah5ywdarfhlwnw', '.eJxVjDkOwjAUBe_iGlle9BObkp4zWH-xcQA5UpxUiLtDpBTQvpl5L5VwW2vael7SJOqsrDr9boT8yG0Hcsd2mzXPbV0m0ruiD9r1dZb8vBzu30HFXr91QDCOsBT04h1GEyXEAmSARy_RSiESKyNQyIzODZAZBmD0zokJXr0_A104hQ:1sN4oO:ZyJ2i2r-rP8hZkWLAKtyKe5u4eTwurzQDp1KLYHuc_s', '2024-06-28 06:40:20.066328'),
('nhid8p16fvqz93u4rqvytu32989m4abm', '.eJxVjDEOwjAMRe-SGUXFcQJhZO8ZKie2SQGlUtNOiLtDpQ6w_vfef5mB1qUMa5N5GNlczNEcfrdE-SF1A3yneptsnuoyj8luit1ps_3E8rzu7t9BoVa-dYgRMYCe1GmGgLkDiOCFWFL2SC4oagqJmbyeGVOn5FzGED2ogJj3B-pkOJo:1sN1cF:LwY8hwwYWiV48oYqx66OdSiC0PLo8oYJX3OKGVQme2U', '2024-06-28 03:15:35.450402'),
('ny770l56h8l5f83rij2h4jsudxs2xp6k', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNYrM:j40veLrBCUryFV1xJlgt-JSLI4meHMWbS08-wh6rsIA', '2024-06-29 14:45:24.440452'),
('oazco3clm2fr7bzbfoywpo596tv80buc', '.eJxVjDEOwjAMRe-SGUXFcQJhZO8ZKie2SQGlUtNOiLtDpQ6w_vfef5mB1qUMa5N5GNlczNEcfrdE-SF1A3yneptsnuoyj8luit1ps_3E8rzu7t9BoVa-dYgRMYCe1GmGgLkDiOCFWFL2SC4oagqJmbyeGVOn5FzGED2ogJj3B-pkOJo:1sN19y:jcKEvbqTGGZOe3k2-1FZocfGwpZqAneVDZJjX-hmtWE', '2024-06-28 02:46:22.710566'),
('oegfr0erttc06i8m88jmd6vc48q7crkz', '.eJxVjEEOgjAQRe_StWnaTjuAS_eegQwzg6CmTSisjHdXEha6_e-9_zI9bevUb1WXfhZzNh7M6XcciB-adyJ3yrdiueR1mQe7K_ag1V6L6PNyuH8HE9XpW6uyoKeIkTmoNA7BATmIwadIPkoaPTaqrkuKioHBjQhButi23cjevD8D8zed:1sO7Fm:HVvfn_cCAAF3CEG4qFCmC8rnWUywbGDxrUv9-mO7Y6E', '2024-07-01 03:28:54.739192'),
('oekdxmanyq71hx30mpsjncf2przmeaew', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNa4n:JPSYcoZ0b5dJzQ_WngjlW7uccQEyQL93FOw_DWycmuc', '2024-06-29 16:03:21.719884'),
('oijaexd00hn5yph9rxqs2twmxzprl3zo', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNyvK:fN8AATdoTeuJoknExguIbsekalFdYDR7pFLH8Y5We-k', '2024-06-30 18:35:14.984516'),
('onzqh68iogx94vqk8pic3sfsr85xbw64', '.eJxVjMsOwiAQRf-FtSEDhXZw6d5vaIZhkKqBpI-V8d-1SRe6veec-1IjbWsZt0XmcUrqrIxXp98xEj-k7iTdqd6a5lbXeYp6V_RBF31tSZ6Xw_07KLSUb51xAO58IEOewCJ7IAcOmLPxPgVEC0HQ9nagvsvRYUgIwUlmiVlQvT_v3zfk:1sbhCm:t-YDkeqIgejG1BHhHfNhhfyOvPPSjreEO52MSdANvoU', '2024-08-07 14:29:56.378053'),
('p1qoewkc6h0dshwp2dwsmi1c185bee9v', '.eJxVjDEOwjAMRe-SGUXFcQJhZO8ZKie2SQGlUtNOiLtDpQ6w_vfef5mB1qUMa5N5GNlczNEcfrdE-SF1A3yneptsnuoyj8luit1ps_3E8rzu7t9BoVa-dYgRMYCe1GmGgLkDiOCFWFL2SC4oagqJmbyeGVOn5FzGED2ogJj3B-pkOJo:1sN1sT:S9qVuPd_g1iwu2ScBarFI4AQd37SvmGBTTlrRwDvcZ4', '2024-06-28 03:32:21.435529'),
('p30qdt5z3s3iz3bxgr3z90nrhl3zamzm', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNV9B:rIpqqQ_UuLPbZ0v3YycPktMldQTHtLztWhMLVHN27yY', '2024-06-29 10:47:33.071384'),
('p40qf3mdn7w7chg9zirweh7n1hemlctt', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNdJD:4XA74EC1txilXtTX96hL4Onj36Jm7eb_Yx3cOvvccIw', '2024-06-29 19:30:27.126793'),
('pahkxgfiwtd2kde4nvyuo3zalj2b9k7f', '.eJxVjEEOgjAQRe_StWnaTjuAS_eegQwzg6CmTSisjHdXEha6_e-9_zI9bevUb1WXfhZzNh7M6XcciB-adyJ3yrdiueR1mQe7K_ag1V6L6PNyuH8HE9XpW6uyoKeIkTmoNA7BATmIwadIPkoaPTaqrkuKioHBjQhButi23cjevD8D8zed:1sOsBx:VYOCSeBKarL3PW_6yxq-w2-lluimAc4lrlKmwCoOjNM', '2024-07-03 05:36:05.056750'),
('pc8zwga9j7b6s02192b5ku0k472jnj7f', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNBUd:foWiIpA84XFYVb9JLAzTmGI31-LmihIDW6VFu7NiVAA', '2024-06-28 13:48:23.590317'),
('pf9bceogdv35h9ipqcrsv5272xvks8oo', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sbhEx:gyZtGfqy5fNm8AnHuiG-f0but30XkS2jwvB1J53a-qM', '2024-08-07 14:32:11.130958'),
('pp4lh8yd3t4ocm3iecn6y9y7ppyy4b3f', '.eJxVjMsOwiAQRf-FtSEDhXZw6d5vaIZhkKqBpI-V8d-1SRe6veec-1IjbWsZt0XmcUrqrIxXp98xEj-k7iTdqd6a5lbXeYp6V_RBF31tSZ6Xw_07KLSUb51xAO58IEOewCJ7IAcOmLPxPgVEC0HQ9nagvsvRYUgIwUlmiVlQvT_v3zfk:1sbidG:LJOJcghqFNE8xZ6ESVx8VRIwjn_bZC_Aovig_MNiyDw', '2024-08-07 16:01:22.302471'),
('promsvc7hyk7tbyokn4ma6c7hx9npc0o', '.eJxVjEEOgjAQRe_StWnaTjuAS_eegQwzg6CmTSisjHdXEha6_e-9_zI9bevUb1WXfhZzNh7M6XcciB-adyJ3yrdiueR1mQe7K_ag1V6L6PNyuH8HE9XpW6uyoKeIkTmoNA7BATmIwadIPkoaPTaqrkuKioHBjQhButi23cjevD8D8zed:1sOf6u:MGtr4s7dXV9MuExyNJRrhLUrtZvcZ-wEROxYZB0wm4g', '2024-07-02 15:38:00.543666'),
('psh5p9tmuaiofmb0bzuimo0uirdoisfe', '.eJxVjMsOwiAQRf-FtSEDhXZw6d5vaIZhkKqBpI-V8d-1SRe6veec-1IjbWsZt0XmcUrqrIxXp98xEj-k7iTdqd6a5lbXeYp6V_RBF31tSZ6Xw_07KLSUb51xAO58IEOewCJ7IAcOmLPxPgVEC0HQ9nagvsvRYUgIwUlmiVlQvT_v3zfk:1saPj9:aEpieuc0TBFelt7-y-SCzMYWtfenu5j6zZ0h9Dv9t3U', '2024-08-04 01:38:03.851799'),
('pwapqo21fct27c5w2l9lbqx1n9np7gnq', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNgY1:R72tdv6kM23F1kT4DyByFBtP680JPdxfcADhmOvlWGk', '2024-06-29 22:57:57.316265'),
('pywpc7ttwi57ns05bc50sau7n1f6n5xg', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNV8l:3dFkSrtOvisyQhJ9oM72hDAybBoIo1A5-bLN-ZL8x-A', '2024-06-29 10:47:07.152669'),
('q0hagwvq2ygrcj4pxde1ej64kfm83nxx', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNbKV:EMz-E-jma2yctEbvUp0m0f1bB50oIrCemR3B6XNOTN8', '2024-06-29 17:23:39.581274'),
('q1d8oif1m4m6cq4wja09uo74pss9b11o', '.eJxVjEEOgjAQRe_StWnaTjuAS_eegQwzg6CmTSisjHdXEha6_e-9_zI9bevUb1WXfhZzNh7M6XcciB-adyJ3yrdiueR1mQe7K_ag1V6L6PNyuH8HE9XpW6uyoKeIkTmoNA7BATmIwadIPkoaPTaqrkuKioHBjQhButi23cjevD8D8zed:1sOvco:805UbdiUsfhYftNmjGRKBsKn4VYr3f0k4JdEK6zieJk', '2024-07-03 09:16:02.697694'),
('qggz1fqufs72hrrz7hwa9kfhxuxlxc5a', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNVfV:eC_M1ttZlezf_9uNYA1IITwc_IS7vd5Ys-vwpaTJdFg', '2024-06-29 11:20:57.621975'),
('qi0oo6r0y55niyhkves8aknnfqwuxfhr', '.eJxVjEEOwiAQRe_C2hCGgoBL9z0DGWZAqoYmpV0Z765NutDtf-_9l4i4rTVuPS9xYnERXpx-t4T0yG0HfMd2myXNbV2mJHdFHrTLceb8vB7u30HFXr91ML44AmAiU5S2BRwgGtROWQspnS0MVhvFweVExifKoEHpAVwAzizeH9VSN1o:1sNwvq:JVptyELU_GCyU3kEp-jPBY8nHWKz7uzYpnQgB75kGEA', '2024-06-30 16:27:38.971165'),
('qxpbnlqcen89zdecpuw064jdn8zjgrs0', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNWZ8:9lg13_EKM6DWHeahJWkWOq6fvseoqIPltXdxQTf_be4', '2024-06-29 12:18:26.143444'),
('r1drxonmd6yxqxvk63xui1vj0a62thhs', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sbe7I:IS6Kt_M5iW8H8ufvDLWDWn2e85y1tjOXo3ZjMucBgyw', '2024-08-07 11:12:04.122658'),
('rbh6b3wogoq8lfahyxdl9b36tzmbil19', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNa1R:y38V7NRgF0ba1UvL5VRwE_6UTjbdYnboLvmgP5RbSnE', '2024-06-29 15:59:53.601303'),
('rdfjp0dkmgi5krr5y8jges3nmdrxo4et', '.eJxVjMsOwiAQRf-FtSEDhXZw6d5vaIZhkKqBpI-V8d-1SRe6veec-1IjbWsZt0XmcUrqrIxXp98xEj-k7iTdqd6a5lbXeYp6V_RBF31tSZ6Xw_07KLSUb51xAO58IEOewCJ7IAcOmLPxPgVEC0HQ9nagvsvRYUgIwUlmiVlQvT_v3zfk:1saUDV:-n3qugpmFQl5CXAys3bcjaE5-D-IrASDjRsHE5a3qmE', '2024-08-04 06:25:41.338038'),
('rejrxbckrblm0oayale5wz68wqd5172t', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sOFac:3F0ZvFDbKm260Mvk6rbqIMV_1Mtl-zYVdmNlp9FyAxY', '2024-07-01 12:22:58.479178'),
('rhw4p2ztj09gneo8wqjtlu1wujqnkbyy', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNa5G:Fc1MCv76Q8YdvBM9BM3SsjwD_9BeZykkyNSS2qlz59c', '2024-06-29 16:03:50.321750'),
('rhws16o3tm6pybhdtx2wjyogujj9xp4k', '.eJxVjEEOgjAQRe_StWnaTjuAS_eegQwzg6CmTSisjHdXEha6_e-9_zI9bevUb1WXfhZzNh7M6XcciB-adyJ3yrdiueR1mQe7K_ag1V6L6PNyuH8HE9XpW6uyoKeIkTmoNA7BATmIwadIPkoaPTaqrkuKioHBjQhButi23cjevD8D8zed:1sPCyU:Mk6pDkb_I4RsgHowuNKpO9KFYBiAF_2KcSOY9DV4o08', '2024-07-04 03:47:34.162488'),
('rjys9ieu0yafq5m9om69etdlqjiax1vo', '.eJxVjMsOwiAQRf-FtSEDhXZw6d5vaIZhkKqBpI-V8d-1SRe6veec-1IjbWsZt0XmcUrqrIxXp98xEj-k7iTdqd6a5lbXeYp6V_RBF31tSZ6Xw_07KLSUb51xAO58IEOewCJ7IAcOmLPxPgVEC0HQ9nagvsvRYUgIwUlmiVlQvT_v3zfk:1saZCU:rKtzdmjUDZkply-pTH7AsoCbtW3plFfzgOuiByC52Gk', '2024-08-04 11:44:58.831743'),
('s80vmq8jx6pueiktqwk01ivivoyyf61z', '.eJxVjDEOwjAMRe-SGUXFcQJhZO8ZKie2SQGlUtNOiLtDpQ6w_vfef5mB1qUMa5N5GNlczNEcfrdE-SF1A3yneptsnuoyj8luit1ps_3E8rzu7t9BoVa-dYgRMYCe1GmGgLkDiOCFWFL2SC4oagqJmbyeGVOn5FzGED2ogJj3B-pkOJo:1sN2TC:PvSnPzLwdo09zsGQ51C8qCXOsQg5KKIeR1KThxumXSU', '2024-06-28 04:10:18.499712'),
('scvd3nd48bpxc6tnwhs9080lf3hjl3n0', '.eJxVjDsOwjAQBe_iGllee_2jpM8ZLH8WHEC2FCcV4u4QKQW0b2bei4W4rTVsg5YwF3ZmAOz0O6aYH9R2Uu6x3TrPva3LnPiu8IMOPvVCz8vh_h3UOOq3tgrRYAKTtbcuZkcSBWhnkYyxxicPQjtzzeStkAmkA1UISRQlbNGavT_K2DaY:1sNzxW:K7lhX_wHIYBysKuzHCy83i1Z2K_lpWsQbvKVqu62xvg', '2024-06-30 19:41:34.252018'),
('sw5zbnntznxtyz4o5w3fy2zka2g9gpza', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNbNl:uPAVA-YlTHBVQPmEVfnwYnN36lxlaJB5Bl-QNutNG_8', '2024-06-29 17:27:01.681443'),
('syjcl8cfaym7vgp1kin7icikp2119bgn', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sPvhn:DBt5P87GZCOhbFBR2ySRqfUxbKyZnEhZRNnCK_C5m9k', '2024-07-06 03:33:19.708295'),
('t1ef8albwygvyfdo506jmamav51dchtk', '.eJxVjMsOwiAQRf-FtSEDhXZw6d5vaIZhkKqBpI-V8d-1SRe6veec-1IjbWsZt0XmcUrqrIxXp98xEj-k7iTdqd6a5lbXeYp6V_RBF31tSZ6Xw_07KLSUb51xAO58IEOewCJ7IAcOmLPxPgVEC0HQ9nagvsvRYUgIwUlmiVlQvT_v3zfk:1saO7F:q8JniF9xcM1oCGHdLLWBoBDWU8qV67RxmCyLNQCQ5Qk', '2024-08-03 23:54:49.499192'),
('t7yt87rp6p75m8ff2yave085jx85izgi', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNF7d:NWt4rAdm8--vdJ3M050miUJrsVy1gPSaHP6aToXBjrg', '2024-06-28 17:40:53.667302'),
('tkx9378blawxxusz7n6bzzo6zcq4oktw', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sb04X:kscEJtTZZNTV-rS1N8Nv17pUrjo1tt2pqBX93t4HrI4', '2024-08-05 16:26:33.368319');
INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('ucfpnzsrrcrbvlybavn3vgz2de7grr9f', '.eJxVjEEOgjAQRe_StWnaTjuAS_eegQwzg6CmTSisjHdXEha6_e-9_zI9bevUb1WXfhZzNh7M6XcciB-adyJ3yrdiueR1mQe7K_ag1V6L6PNyuH8HE9XpW6uyoKeIkTmoNA7BATmIwadIPkoaPTaqrkuKioHBjQhButi23cjevD8D8zed:1sOVLC:T81pNLkNCXzwUe8xSIV399qr12BYaPAgUqCZsZWRcDY', '2024-07-02 05:12:06.017170'),
('ude72zzwe0qet9ey3ahsu0kt297paavu', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNE12:Z2PFMKHjiMzOciyvTLipv-Lf_6KcaZoDx69BBNYOt1c', '2024-06-28 16:30:00.255585'),
('uls9pj592vct8ptm969luh7s6svzxqao', '.eJxVjDEOwjAMRe-SGUXFcQJhZO8ZKie2SQGlUtNOiLtDpQ6w_vfef5mB1qUMa5N5GNlczNEcfrdE-SF1A3yneptsnuoyj8luit1ps_3E8rzu7t9BoVa-dYgRMYCe1GmGgLkDiOCFWFL2SC4oagqJmbyeGVOn5FzGED2ogJj3B-pkOJo:1sN3yg:4Uh2SkBTKH7fTQjrXGWi75P-6eLNm803EcOZSBIMtrk', '2024-06-28 05:46:54.776967'),
('un50ysr1kg27p39fyxec79eehe40bz67', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNeAl:nHQxKwn4KD05DCU8lmThlVNNPLeXrC6RzLDBriWBniI', '2024-06-29 20:25:47.447316'),
('unuk4p6ggchpt3rsz5ff17p6b4fov5hq', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sbdjz:q2-F-7vdA2C7o2fSgHcUkbyDgcL87dIQjvr8bkbKLv8', '2024-08-07 10:47:59.210808'),
('uoa37w8kfqkntqibf4svsie2d5uxeon9', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNfai:nPRrPmq65ziBC7o05gDca_pS4LWGhjo8CNGEQJmXXJM', '2024-06-29 21:56:40.270698'),
('uoesjfl18i6pbsnj4ljscqilqg4f44he', '.eJxVjMsOwiAQRf-FtSEDhXZw6d5vaIZhkKqBpI-V8d-1SRe6veec-1IjbWsZt0XmcUrqrIxXp98xEj-k7iTdqd6a5lbXeYp6V_RBF31tSZ6Xw_07KLSUb51xAO58IEOewCJ7IAcOmLPxPgVEC0HQ9nagvsvRYUgIwUlmiVlQvT_v3zfk:1sbjOX:nZPYC0Iij2LcQrkTO39R9iZd77j9ND7fWhgkLWenz68', '2024-08-07 16:50:13.572784'),
('uq7jpabraktl9jidilr26oax7t0ybs8z', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sPKLp:osY3_UeTVImcQ7eTS_vnZcCZ3_piXWImmTXuSfRzb7s', '2024-07-04 11:40:09.141899'),
('us6gy0j248cuhsmkax0mlmwaucn9rcq6', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNX7V:7kNQWbXMhOqRNemwTXhhI5r0K8Pi-mpcF_0IN9-GjXE', '2024-06-29 12:53:57.380458'),
('ux0s5utkck60w6a6rxcm6lx537x4dxle', '.eJxVjDEOwjAMRe-SGUXFcQJhZO8ZKie2SQGlUtNOiLtDpQ6w_vfef5mB1qUMa5N5GNlczNEcfrdE-SF1A3yneptsnuoyj8luit1ps_3E8rzu7t9BoVa-dYgRMYCe1GmGgLkDiOCFWFL2SC4oagqJmbyeGVOn5FzGED2ogJj3B-pkOJo:1sN1QY:mz-PpZeIL0n1l3uVNbxRu6jLKFGRBa7I0MOBp9QknzU', '2024-06-28 03:03:30.094055'),
('v3khpfmptywb0f4qlkn1xdaxzyp0b3vz', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNFDG:kRo78WmAL_iVsrGF6wCOnC7njslKjiI4-rgBA0beQCo', '2024-06-28 17:46:42.555261'),
('v9e0w2voqns2q3s86y4sr0dm2kv2knj5', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNrKt:RBoyVLmBi7xwLSJRao5vONW6nQYpPfzZFhyC3EhgMV4', '2024-06-30 10:29:07.198674'),
('vohpzfgwqymegc7563rro14gxhqfllbo', '.eJxVjDkOwjAUBe_iGlle9BObkp4zWH-xcQA5UpxUiLtDpBTQvpl5L5VwW2vael7SJOqsrDr9boT8yG0Hcsd2mzXPbV0m0ruiD9r1dZb8vBzu30HFXr91QDCOsBT04h1GEyXEAmSARy_RSiESKyNQyIzODZAZBmD0zokJXr0_A104hQ:1sN7nM:toX2kTGEQU7ki2iaExPnQ3aMJJ-zJF4_gB_w6hX_Okc', '2024-06-28 09:51:28.976984'),
('vph27anrva85sjixh0cm8d0qlueirgwa', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNmct:xpnoEU4j2CY_1QMSMbk0VflPXBR688YgfQIM7JRcUqs', '2024-06-30 05:27:23.193758'),
('vuxwwtgc2pe3d6cn32hdy05hacrpjdf3', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNftB:ETiLUj1RH1pxSQopmfii4e8EciuTD33PtV3PTD4_JnU', '2024-06-29 22:15:45.363019'),
('w7ijee4r7acrxd0e9gr3nacg2sof1hh5', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNW4k:y8ap1ctSOBaA9mHmsX96McGckWT-CrYTJMCV8lXvgUg', '2024-06-29 11:47:02.022431'),
('wafpiktfmx2iuhk3ax3zzr0lp6nx532v', '.eJxVjDEOwjAMRe-SGUXFcQJhZO8ZKie2SQGlUtNOiLtDpQ6w_vfef5mB1qUMa5N5GNlczNEcfrdE-SF1A3yneptsnuoyj8luit1ps_3E8rzu7t9BoVa-dYgRMYCe1GmGgLkDiOCFWFL2SC4oagqJmbyeGVOn5FzGED2ogJj3B-pkOJo:1sN3CF:aZSa5JTyiUdxf4gGZi2qeVXOF6Mx0ktN7h-NQ7amjFA', '2024-06-28 04:56:51.710419'),
('wg4m79zt2c2bz03r09u8oktfycfz0t3j', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNCf6:mz1ZnALY3cplQnh7DQ1geUgS9JaCLUHZro_EIDd0yCg', '2024-06-28 15:03:16.849664'),
('x1ymprgug7rv318vfuge8tecr19nye1b', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNVfW:J9wxVVkRPNxiY4OiDsPvsChAZ6ylJrgvzdagiHEmPWQ', '2024-06-29 11:20:58.248924'),
('x2rfbbf9d9ztnzcurk8x0vacbnqvoqa2', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNkHi:PQJLV9LTIkOrfViz3pbRA3sYh7v19Mwstzu9nq4Z4zs', '2024-06-30 02:57:22.725668'),
('x9xh5cm4uzt0xf2zy0zcsi3dr22tyigw', '.eJxVjDEOwjAMRe-SGUXFcQJhZO8ZKie2SQGlUtNOiLtDpQ6w_vfef5mB1qUMa5N5GNlczNEcfrdE-SF1A3yneptsnuoyj8luit1ps_3E8rzu7t9BoVa-dYgRMYCe1GmGgLkDiOCFWFL2SC4oagqJmbyeGVOn5FzGED2ogJj3B-pkOJo:1sN1KM:7hMm--Q_INpmpaGS9CsdK3WG5iQkMBKqo9FLMhYkwa8', '2024-06-28 02:57:06.954718'),
('xgxfs0xwk100f8adwdge7cini9dej1z2', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNby8:CF0i8XGIwYJfL28wk3S5WRTtP_4bKc_baL8ETvkX-FU', '2024-06-29 18:04:36.709783'),
('xhaa8j9or4cv4srrshwcoyruetc1hohi', '.eJxVjDkOwjAUBe_iGlle9BObkp4zWH-xcQA5UpxUiLtDpBTQvpl5L5VwW2vael7SJOqsrDr9boT8yG0Hcsd2mzXPbV0m0ruiD9r1dZb8vBzu30HFXr91QDCOsBT04h1GEyXEAmSARy_RSiESKyNQyIzODZAZBmD0zokJXr0_A104hQ:1sN8YN:ny_zeu55Zpw6Nq8hHXEFUPVUPAa6wKTU_TAIl4tYsGA', '2024-06-28 10:40:03.175322'),
('xjakf00ndzd8b3kfdrvke39qvbqhu91d', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNDNm:tojtI7IXMqXMuSxQ3WixAeN9bOCwroZcvA-2lstgnCw', '2024-06-28 15:49:26.782170'),
('xtqmdxtyusio9nlx2ujadiohv5cx9vk4', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sOKQM:6Ql6wJvQPBnh1wVgfZaA8R5gP7Ac71D-ORNOPxivtrs', '2024-07-01 17:32:42.265792'),
('xuo8ullw2zf1qd73jw5lprwlefh9tulv', '.eJxVjEEOgjAQRe_StWnaTjuAS_eegQwzg6CmTSisjHdXEha6_e-9_zI9bevUb1WXfhZzNh7M6XcciB-adyJ3yrdiueR1mQe7K_ag1V6L6PNyuH8HE9XpW6uyoKeIkTmoNA7BATmIwadIPkoaPTaqrkuKioHBjQhButi23cjevD8D8zed:1sODaZ:bWWc_ikEEfphPny2A94-aY3A9QLoN4M6cawrlIfibQ0', '2024-07-01 10:14:47.311103'),
('ye4lm8dxy0ibeqpxmm03wr4envq5idpc', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sb0Bm:nUw3XFKLCU3wksqris8bSQjexwgwl4AWCt-msZ4nODA', '2024-08-05 16:34:02.512077'),
('yihzetrgsegy8tqhluby2otch55487jr', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNvEA:9vmQGIZRP_YvlXqFbKWVsgoFVAbULa1tjN6hLA1YTmo', '2024-06-30 14:38:26.592657'),
('yp8hwv3y2ihpp1v2ayo7bv3oig21j63p', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNe8W:m4Av56fMzJYQwpK6HYksre7ITfM_So4LXaf5-SL2J1M', '2024-06-29 20:23:28.121571'),
('yu8gkkhy83ng5ijuw75tdho0dqzxppoy', '.eJxVjEEOgjAQRe_StWnaTjuAS_eegQwzg6CmTSisjHdXEha6_e-9_zI9bevUb1WXfhZzNh7M6XcciB-adyJ3yrdiueR1mQe7K_ag1V6L6PNyuH8HE9XpW6uyoKeIkTmoNA7BATmIwadIPkoaPTaqrkuKioHBjQhButi23cjevD8D8zed:1sOAXF:M5ZWAemzloAdYJeT5uC1s-PkNxB8V64lhsquo4-znSg', '2024-07-01 06:59:09.762946'),
('yxrfxr7atell9velcgr08bf18evcms7h', '.eJxVjMsOwiAQRf-FtSEDhXZw6d5vaIZhkKqBpI-V8d-1SRe6veec-1IjbWsZt0XmcUrqrIxXp98xEj-k7iTdqd6a5lbXeYp6V_RBF31tSZ6Xw_07KLSUb51xAO58IEOewCJ7IAcOmLPxPgVEC0HQ9nagvsvRYUgIwUlmiVlQvT_v3zfk:1sbkdm:fiirk_HT42Flf_VKjzsgx1h2s0okPIhO9QaZnOj5SsQ', '2024-08-07 18:10:02.110005'),
('z5ptrjgrlsn6pe3ne2974h0301v0ul2c', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNeso:yCDK7aNqoj03wCjo9Mnlb3J4Wxp3k2KcB8uY-5jiZcs', '2024-06-29 21:11:18.451518'),
('z6r5hdl9j6ta2bykd60auy2zuy25ozw9', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNgeA:o6GEWu2tXIW3cPBMXxi1W86BPAro3kAfgTQGGdzzkdA', '2024-06-29 23:04:18.858454'),
('z6tf5t2vj6e18t1vq1k84j1v1f188egi', '.eJxVjMsOwiAQRf-FtSEDhXZw6d5vaIZhkKqBpI-V8d-1SRe6veec-1IjbWsZt0XmcUrqrIxXp98xEj-k7iTdqd6a5lbXeYp6V_RBF31tSZ6Xw_07KLSUb51xAO58IEOewCJ7IAcOmLPxPgVEC0HQ9nagvsvRYUgIwUlmiVlQvT_v3zfk:1sfWPj:UF3zQT55FCGgo1_itgOK4ksLiNuMIAU37kHI3VJySK0', '2024-08-18 03:47:07.628798'),
('zbfl32kh8un5pkcj6gbfdcd0rmmfxnhu', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sbi5l:lVlP0R667_r4gkytD78N_FZiTPGJtH95JtUCAbx-rBw', '2024-08-07 15:26:45.354818'),
('zk0e60xf6mp1abhpv1m0fxz0p4vx8v11', '.eJxVjDEOwjAMRe-SGUXFcQJhZO8ZKie2SQGlUtNOiLtDpQ6w_vfef5mB1qUMa5N5GNlczNEcfrdE-SF1A3yneptsnuoyj8luit1ps_3E8rzu7t9BoVa-dYgRMYCe1GmGgLkDiOCFWFL2SC4oagqJmbyeGVOn5FzGED2ogJj3B-pkOJo:1sN1e7:czlnq0ud2qLSBO3sdNjcMbXy8EIAD5-ntRZHxl-88jg', '2024-06-28 03:17:31.739850'),
('zkxak3q7ah9qu93pnqx6o3kb2q3550cq', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNgx3:LTx2kfDCDQIB9XE1P9js8CT4ONPoeBMAOoeYQpOpvTQ', '2024-06-29 23:23:49.355157'),
('zowww6iimwsddgofbcwsk1mdz2cyqh9q', '.eJxVjDEOwjAMRe-SGUXFcQJhZO8ZKie2SQGlUtNOiLtDpQ6w_vfef5mB1qUMa5N5GNlczNEcfrdE-SF1A3yneptsnuoyj8luit1ps_3E8rzu7t9BoVa-dYgRMYCe1GmGgLkDiOCFWFL2SC4oagqJmbyeGVOn5FzGED2ogJj3B-pkOJo:1sN1WC:cpz5VS16VfirFdpRVOoxOIjrvvvwhXtuBWDS14I3Rsk', '2024-06-28 03:09:20.045237'),
('zvhbjqfsoew5kvauwoggsg6zr6z94sy5', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sNYO1:gejDDbIoqf5Y1LuD_O_8z81UwEl1lmGZ0q4_3NNBZWU', '2024-06-29 14:15:05.552386');

-- --------------------------------------------------------

--
-- Table structure for table `main_contactus`
--

CREATE TABLE `main_contactus` (
  `id` bigint(20) NOT NULL,
  `name` varchar(100) NOT NULL,
  `email` varchar(254) NOT NULL,
  `subject` varchar(200) NOT NULL,
  `message` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `main_contactus`
--

INSERT INTO `main_contactus` (`id`, `name`, `email`, `subject`, `message`, `created_at`) VALUES
(3, 'Maria Santos', 'maria.santos1@gmail.com', 'Inquiry about College Courses and Enrollment', 'Dear Pilar Colleges of Zamboanga City, Inc.,\n\nI hope this message finds you well. My name is Maria Santos, a recent graduate of senior high school, and I am very interested in continuing my education at your esteemed institution.\n\nI would like to inquire about the college courses you offer, particularly those related to business administration and information technology. Could you please provide detailed information on the programs available, including the curriculum, faculty, and any specializations within these fields?\n\nAdditionally, I would like to know more about the enrollment process for new students. What are the requirements and steps I need to follow to apply for admission? Are there any important dates or deadlines I should be aware of for the upcoming academic year?\n\nThank you very much for your assistance. I look forward to your response.\n\nBest regards,\nMaria Santos\n', '2024-08-04 11:50:55.530124');

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
  `contact_number` varchar(15) NOT NULL,
  `is_counselor` tinyint(1) NOT NULL,
  `block_duration` int(11) DEFAULT NULL,
  `block_reason` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `main_customuser`
--

INSERT INTO `main_customuser` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`, `student_id`, `full_name`, `academic_year_level`, `contact_number`, `is_counselor`, `block_duration`, `block_reason`) VALUES
(5, 'pbkdf2_sha256$720000$DBXkBFEfvNIs82zUz9pMul$63TACCT2pyLY2qemKX6wCCrzsg/pPqfcKQImBEjIEUE=', '2024-08-17 15:03:51.645155', 0, 'KCprsnlcc', '', '', 'kcpersonalacc@gmail.com', 1, 1, '2024-06-28 13:16:02.592036', 'C210077', 'Sulaiman, Khadaffe A.', 'Fourth Year', '+639949953785', 0, NULL, NULL),
(6, 'pbkdf2_sha256$720000$iWiUw10UsuzF0XTbOu6HRN$tLh9lesGv2/k462w0eMhDErpTu3tXjLt0fsAXVoOPZ8=', '2024-08-04 05:25:48.752590', 0, 'Dammang', '', '', 'ashraffdammang14@gmail.com', 0, 1, '2024-06-30 14:33:17.563938', 'C246783', 'Ashraff Dammang', 'Fourth Year', '+639425786145', 0, NULL, NULL),
(10, 'pbkdf2_sha256$720000$FezOJflJ2ZM5D3ee7fiDHt$wfn5SFsd5A3Ru3oLQehipwuP4KxRmLRpRFwicc6WNCo=', '2024-08-07 22:34:14.000999', 0, 'MikeElton', '', '', 'mikemangan23@gmail.com', 0, 1, '2024-06-30 16:08:43.524518', 'C2467832', 'Mike Elton John Mangan', 'Fourth Year', '+639587645921', 0, NULL, NULL),
(11, 'pbkdf2_sha256$720000$HV5k8mValMoQsJVBMoPQ01$dEmHt4rAHvkO5DywXvV45MnqPSUuZvnaSqa42/8kvWA=', '2024-08-04 05:31:23.427378', 0, 'AppleMae', '', '', 'appledinawanao12@gmail.com', 0, 1, '2024-06-30 18:16:51.981618', 'C654347', 'Apple Dinawanao', 'Fourth Year', '+639949953785', 0, NULL, NULL),
(12, 'pbkdf2_sha256$720000$QVSwfuwXWuGm9hB96Fxlw3$sLT8dyrYvRvAktt9/ouL1pLLeKjO+MUythtd20LCzOA=', '2024-08-07 22:37:23.211246', 0, 'YourIdol', '', '', 'youridol12@gmail.com', 0, 1, '2024-06-30 19:30:18.295446', 'C464698', 'Mark Hamill Salahuddin', 'Fourth Year', '+639949953785', 0, NULL, NULL),
(13, 'pbkdf2_sha256$720000$APh5yOIqou1UVeT69iK8TI$ulSBpSpYvrrDRgZ4K0eHioC/HQdm7oI2a2rgGfSboxs=', '2024-08-07 22:36:52.271227', 0, 'Radzkhan', '', '', 'alradzkhan13@gmail.com', 0, 1, '2024-06-30 19:35:34.825660', 'C665736', 'Alradzkhan Hayuddini', 'Fourth Year', '+639949956543', 0, NULL, NULL),
(14, 'pbkdf2_sha256$720000$inmGtKqU6fQdl6I8cy1sYr$VKzrIU5j2o97+NVQIVRdiw1Ev9qcH5A1/7Am6RqyeMs=', '2024-08-17 15:04:20.509436', 0, 'Midorin', '', '', 'midorin2@gmail.com', 0, 1, '2024-06-30 19:39:03.800440', 'C564123', 'Eduard Rolad Donor', 'Fourth Year', '+63923132153', 0, NULL, NULL),
(15, 'pbkdf2_sha256$720000$ncnhTbf8MYawLtOX0UVNeI$zm5HNked5nyy0XnhVVtwKzxrocgcFJwKcItlYJHW+uI=', '2024-08-18 03:14:47.189696', 0, 'bheng', '', '', '', 1, 1, '2024-08-03 23:16:17.085772', '', 'bheng manalo', '', '', 1, NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `main_customuser_groups`
--

CREATE TABLE `main_customuser_groups` (
  `id` bigint(20) NOT NULL,
  `customuser_id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `main_customuser_user_permissions`
--

CREATE TABLE `main_customuser_user_permissions` (
  `id` bigint(20) NOT NULL,
  `customuser_id` bigint(20) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `main_reply`
--

CREATE TABLE `main_reply` (
  `id` bigint(20) NOT NULL,
  `text` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `status_id` bigint(20) NOT NULL,
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `main_reply`
--

INSERT INTO `main_reply` (`id`, `text`, `created_at`, `status_id`, `user_id`) VALUES
(23, 'I\'m sorry to hear you\'re having a tough day. It\'s okay to feel sad, especially after personal events. Remember to be kind to yourself and take things one step at a time. Reach out to someone you trust if you need support.', '2024-08-07 22:29:34.442710', 155, 5),
(24, 'I\'m sorry you\'re feeling this way. It\'s okay to struggle and feel sad. Take care of yourself and don\'t hesitate to reach out to friends or loved ones for support.', '2024-08-07 22:30:12.981934', 155, 14),
(25, 'I\'m glad to hear you got through that unpleasant task. It\'s always a relief to have such things behind you. Great job pushing through!', '2024-08-07 22:30:33.702845', 153, 14),
(26, 'It\'s tough dealing with anger, especially after a miscommunication at work. It\'s great that you\'re focusing on managing your emotions constructively. Take a moment to breathe and find a positive way to address the issue.', '2024-08-07 22:30:58.710601', 151, 14),
(27, 'Dealing with unpleasant tasks is never easy, but it\'s great that you got through it. Sometimes, these challenges test our resilience and make us stronger. Well done for pushing through!', '2024-08-07 22:31:20.649407', 149, 14),
(29, 'It\'s fantastic to hear about the positive momentum in your translation process! The steady progress and the team\'s dedication are truly inspiring. Keep up the great work!', '2024-08-07 22:31:58.831063', 142, 14),
(30, 'I\'m glad to hear that today was filled with joyful moments for you, both at work and at home. Cherishing these happy times is important and can motivate us to keep pushing forward.', '2024-08-07 22:33:03.208216', 154, 13),
(31, 'It\'s great that you managed to get through that unpleasant task. It\'s always a relief to have such things behind you. Well done for handling it!', '2024-08-07 22:33:26.671193', 153, 13),
(32, 'I\'m really sorry to hear about the disheartening news regarding your close friend. It\'s challenging to stay motivated when personal life throws such curveballs. Remember to take care of yourself during this tough time, and don\'t hesitate to reach out for support if you need it.', '2024-08-07 22:33:53.844002', 150, 13),
(33, 'I\'m sorry to hear you\'re feeling this way. It\'s okay to struggle with sadness, especially after personal events. Remember to be kind to yourself and take things one step at a time. Stay strong, and reach out for support if you need it.', '2024-08-07 22:34:35.482708', 155, 10),
(34, 'It\'s wonderful to hear that your day was filled with joyful moments both at work and at home. Cherishing these happy times is so important and can really help us keep pushing forward.', '2024-08-07 22:35:03.968824', 154, 10),
(35, 'Despite the numerous challenges, it\'s encouraging to see the steady progress we\'re making. The team\'s determination and resilience are truly commendable. Let\'s keep pushing forward together.', '2024-08-07 22:36:02.913451', 147, 10),
(36, 'It\'s great to see that we\'re making steady progress despite the challenges. The team\'s determination and resilience are truly admirable. Let\'s continue to push forward with the same spirit.', '2024-08-07 22:36:36.054822', 147, 5),
(37, 'Amidst all the challenges, it\'s uplifting to see our steady progress. The determination and resilience of the team are truly commendable. Let\'s keep pushing forward together.', '2024-08-07 22:37:09.691447', 147, 13),
(38, 'Even with the many challenges we face, our progress remains steady. The team\'s resilience and determination are inspiring. Let\'s keep moving forward and overcoming obstacles together.', '2024-08-07 22:37:42.700485', 147, 12);

-- --------------------------------------------------------

--
-- Table structure for table `main_status`
--

CREATE TABLE `main_status` (
  `id` bigint(20) NOT NULL,
  `emotion` varchar(50) NOT NULL,
  `title` varchar(255) NOT NULL,
  `description` longtext NOT NULL,
  `plain_description` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `user_id` bigint(20) NOT NULL,
  `anger` double NOT NULL,
  `disgust` double NOT NULL,
  `fear` double NOT NULL,
  `happiness` double NOT NULL,
  `sadness` double NOT NULL,
  `surprise` double NOT NULL,
  `neutral` double NOT NULL,
  `anger_percentage` int(11) NOT NULL,
  `disgust_percentage` int(11) NOT NULL,
  `fear_percentage` int(11) NOT NULL,
  `happiness_percentage` int(11) NOT NULL,
  `neutral_percentage` int(11) NOT NULL,
  `sadness_percentage` int(11) NOT NULL,
  `surprise_percentage` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `main_status`
--

INSERT INTO `main_status` (`id`, `emotion`, `title`, `description`, `plain_description`, `created_at`, `user_id`, `anger`, `disgust`, `fear`, `happiness`, `sadness`, `surprise`, `neutral`, `anger_percentage`, `disgust_percentage`, `fear_percentage`, `happiness_percentage`, `neutral_percentage`, `sadness_percentage`, `surprise_percentage`) VALUES
(139, 'Happiness', 'Translation Phase Completed', 'I\'m thrilled to announce that we have completed the translation of our dataset into Tagalog. This achievement brings us one step closer to fine-tuning our emotion model and enhancing our emotional expression portal. The journey has been challenging but rewarding.', 'I\'m thrilled to announce that we have completed the translation of our dataset into Tagalog. This achievement brings us one step closer to fine-tuning our emotion model and enhancing our emotional expression portal. The journey has been challenging but rewarding.', '2024-08-04 05:24:29.684063', 5, 0.0019292188808321953, 0.0006972739938646555, 0.0013668902684003115, 0.9750613570213318, 0.0012870833743363619, 0.014756225049495697, 0.004901868756860495, 0, 0, 0, 97, 0, 0, 1),
(140, 'Sadness', 'Unexpected Setback', 'We encountered a critical bug in our translation script, causing significant delays. The team is working tirelessly to resolve the issue, but the setback has been disheartening. We\'re determined to overcome this hurdle and continue progressing.', 'We encountered a critical bug in our translation script, causing significant delays. The team is working tirelessly to resolve the issue, but the setback has been disheartening. We\'re determined to overcome this hurdle and continue progressing.', '2024-08-04 05:25:02.262612', 5, 0.0016891434788703918, 0.007039517629891634, 0.006298134569078684, 0.002301199361681938, 0.9638738036155701, 0.005434457212686539, 0.013363741338253021, 0, 0, 0, 0, 1, 96, 0),
(141, 'Happiness', 'Milestone Celebration', 'Today, we celebrate a major milestone—the successful translation of our entire dataset into Tagalog! This accomplishment is a testament to our hard work and dedication. Exciting times lie ahead as we prepare to fine-tune our model.', 'Today, we celebrate a major milestone—the successful translation of our entire dataset into Tagalog! This accomplishment is a testament to our hard work and dedication. Exciting times lie ahead as we prepare to fine-tune our model.', '2024-08-04 05:26:12.428166', 6, 0.004170689731836319, 0.0010625054128468037, 0.0019863450434058905, 0.9526568055152893, 0.0012127094669267535, 0.02076517604291439, 0.018145672976970673, 0, 0, 0, 95, 1, 0, 2),
(142, 'Happiness', 'Positive Momentum', 'We\'ve gained positive momentum in our translation process, making steady progress. The team\'s dedication and hard work are truly inspiring.', 'We\'ve gained positive momentum in our translation process, making steady progress. The team\'s dedication and hard work are truly inspiring.', '2024-08-04 05:27:17.361349', 10, 0.004638023674488068, 0.005188953131437302, 0.003127913922071457, 0.6474635004997253, 0.0036034737713634968, 0.03618434816598892, 0.29979386925697327, 0, 0, 0, 64, 29, 0, 3),
(143, 'Fear', 'Facing Uncertainty', 'The translation process has been more complex than anticipated, leading to uncertainty about our project timeline. The team is working hard to navigate these challenges and find effective solutions.', 'The translation process has been more complex than anticipated, leading to uncertainty about our project timeline. The team is working hard to navigate these challenges and find effective solutions.', '2024-08-04 05:29:10.629298', 11, 0.012217064388096333, 0.005202437750995159, 0.3442191183567047, 0.01092352345585823, 0.018597155809402466, 0.008367986418306828, 0.6004727482795715, 1, 0, 34, 1, 60, 1, 0),
(144, 'Anger', 'Frustration Peaks', '<div bis_skin_checked=\"1\">Another round of technical issues has brought our progress to a halt. The team\'s frustration is palpable, but we are committed to finding a resolution and pushing through.</div>', 'Another round of technical issues has brought our progress to a halt. The team\'s frustration is palpable, but we are committed to finding a resolution and pushing through.', '2024-08-04 05:30:09.687666', 5, 0.9408396482467651, 0.00850855652242899, 0.0011707379017025232, 0.002628578105941415, 0.019658472388982773, 0.0010118219070136547, 0.026182224974036217, 94, 0, 0, 0, 2, 1, 0),
(145, 'Surprise', 'Unexpected Breakthrough', '<div bis_skin_checked=\"1\">We experienced an unexpected breakthrough in our translation process, significantly improving efficiency. This development has boosted team morale and accelerated our timeline.</div>', 'We experienced an unexpected breakthrough in our translation process, significantly improving efficiency. This development has boosted team morale and accelerated our timeline.', '2024-08-04 05:30:29.026318', 5, 0.008794465102255344, 0.0035787622909992933, 0.00664545688778162, 0.6093906760215759, 0.0038843981456011534, 0.12407993525266647, 0.24362628161907196, 0, 0, 0, 60, 24, 0, 12),
(147, 'Happiness', 'Progress Amidst Challenges', '<div bis_skin_checked=\"1\">Despite the numerous challenges, we are making steady progress. The team\'s determination and resilience are commendable. We will continue to push forward.</div><div bis_skin_checked=\"1\"><br></div>', 'Despite the numerous challenges, we are making steady progress. The team\'s determination and resilience are commendable. We will continue to push forward.', '2024-08-04 05:31:39.672243', 11, 0.009493770077824593, 0.005666713695973158, 0.008420553989708424, 0.460519015789032, 0.006693973671644926, 0.009713422507047653, 0.4994925558567047, 0, 0, 0, 46, 49, 0, 0),
(148, 'Fear', 'Overwhelmed but Hopeful', '<div bis_skin_checked=\"1\">The complexity of the translation process has been overwhelming at times, but we remain hopeful and committed to our goals. The team\'s resilience is commendable.</div>', 'The complexity of the translation process has been overwhelming at times, but we remain hopeful and committed to our goals. The team\'s resilience is commendable.', '2024-08-04 05:32:02.172720', 11, 0.004258217290043831, 0.004370026756078005, 0.018206728622317314, 0.6743161082267761, 0.004406822379678488, 0.014697698876261711, 0.27974432706832886, 0, 0, 1, 67, 27, 0, 1),
(149, 'Disgust', 'Overcoming Disgust', '<div bis_skin_checked=\"1\">Had to deal with a particularly unpleasant task today. It was revolting, but necessary. Sometimes, life throws these challenges at us to test our resilience.</div>', 'Had to deal with a particularly unpleasant task today. It was revolting, but necessary. Sometimes, life throws these challenges at us to test our resilience.', '2024-08-04 05:33:02.647728', 10, 0.03187451511621475, 0.4441128969192505, 0.3892916142940521, 0.004690230358392, 0.0819910317659378, 0.004854700993746519, 0.043185003101825714, 3, 44, 38, 0, 4, 8, 0),
(150, 'Sadness', 'Disheartening News', 'Received some disheartening news about a close friend. It\'s hard to stay motivated when personal life throws such curveballs.', 'Received some disheartening news about a close friend. It\'s hard to stay motivated when personal life throws such curveballs.', '2024-08-04 05:34:09.778661', 12, 0.005729991476982832, 0.03910326585173607, 0.0029186869505792856, 0.0019326204201206565, 0.9378151893615723, 0.005862448830157518, 0.006637743208557367, 0, 3, 0, 0, 0, 93, 0),
(151, 'Anger', 'Dealing with Anger', '<div bis_skin_checked=\"1\">Felt a surge of anger today due to a miscommunication at work. It\'s important to manage these emotions constructively, even when it\'s tough.</div>', 'Felt a surge of anger today due to a miscommunication at work. It\'s important to manage these emotions constructively, even when it\'s tough.', '2024-08-04 05:34:30.785649', 12, 0.9573907256126404, 0.014166107401251793, 0.004705321975052357, 0.0007844159263186157, 0.005818953271955252, 0.0009728842414915562, 0.016161533072590828, 95, 1, 0, 0, 1, 0, 0),
(152, 'Fear', 'Anxiety Over Uncertainty', '<div bis_skin_checked=\"1\">Feeling anxious about the uncertainty of upcoming projects and personal commitments. The fear of the unknown is a constant challenge.</div>', 'Feeling anxious about the uncertainty of upcoming projects and personal commitments. The fear of the unknown is a constant challenge.', '2024-08-04 05:36:10.989464', 13, 0.001026142854243517, 0.0008091017953120172, 0.9905966520309448, 0.0013121414231136441, 0.0020971756894141436, 0.0012878328561782837, 0.002870921976864338, 0, 0, 99, 0, 0, 0, 0),
(153, 'Disgust', 'Disgusting Task Overcome', '<div bis_skin_checked=\"1\">Faced a particularly disgusting task today. It was unpleasant, but I\'m glad it\'s over and done with.</div>', 'Faced a particularly disgusting task today. It was unpleasant, but I\'m glad it\'s over and done with.', '2024-08-04 05:36:46.095900', 5, 0.0028061599005013704, 0.9770159125328064, 0.003053655382245779, 0.004919661674648523, 0.0063085127621889114, 0.00040556976455263793, 0.005490371026098728, 0, 97, 0, 0, 0, 0, 0),
(154, 'Happiness', 'Joyful Day', 'Today was filled with joyful moments, both at work and at home. It\'s important to cherish these happy times and keep pushing forward.', 'Today was filled with joyful moments, both at work and at home. It\'s important to cherish these happy times and keep pushing forward.', '2024-08-04 05:37:37.501670', 14, 0.0010308093624189496, 0.0007249161135405302, 0.00026489587617106736, 0.9848569631576538, 0.003817293792963028, 0.002651297952979803, 0.006653815973550081, 0, 0, 0, 98, 0, 0, 0),
(155, 'Sadness', 'Emotional Struggles', 'Struggling with sadness due to recent personal events. It\'s been a tough day, but I\'m trying to stay strong and keep moving forward.', 'Struggling with sadness due to recent personal events. It\'s been a tough day, but I\'m trying to stay strong and keep moving forward.', '2024-08-04 05:38:42.748136', 13, 0.001055471831932664, 0.002059370744973421, 0.003661424620077014, 0.00246447348035872, 0.9811586141586304, 0.0013769293436780572, 0.00822375901043415, 0, 0, 0, 0, 0, 98, 0);

-- --------------------------------------------------------

--
-- Table structure for table `main_userprofile`
--

CREATE TABLE `main_userprofile` (
  `id` bigint(20) NOT NULL,
  `avatar` varchar(100) DEFAULT NULL,
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `main_userprofile`
--

INSERT INTO `main_userprofile` (`id`, `avatar`, `user_id`) VALUES
(7, 'avatars/avatar_tRPd5g1.png', 5),
(8, 'avatars/avatar_IVRgcCK.png', 6),
(12, 'avatars/avatar_w7KIwiD.png', 10),
(13, 'avatars/avatar_PzDVDWv.png', 11),
(14, 'avatars/avatar_ZXKCcrX.png', 12),
(15, 'avatars/avatar_Ohb3id4.png', 13),
(16, 'avatars/avatar_Kw3Ac7r.png', 14),
(17, '', 15);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indexes for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_main_customuser_id` (`user_id`);

--
-- Indexes for table `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indexes for table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Indexes for table `main_contactus`
--
ALTER TABLE `main_contactus`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `main_customuser`
--
ALTER TABLE `main_customuser`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `student_id` (`student_id`);

--
-- Indexes for table `main_customuser_groups`
--
ALTER TABLE `main_customuser_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `main_customuser_groups_customuser_id_group_id_8a5023dd_uniq` (`customuser_id`,`group_id`),
  ADD KEY `main_customuser_groups_group_id_8149f607_fk_auth_group_id` (`group_id`);

--
-- Indexes for table `main_customuser_user_permissions`
--
ALTER TABLE `main_customuser_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `main_customuser_user_per_customuser_id_permission_06a652d8_uniq` (`customuser_id`,`permission_id`),
  ADD KEY `main_customuser_user_permission_id_38e6f657_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `main_reply`
--
ALTER TABLE `main_reply`
  ADD PRIMARY KEY (`id`),
  ADD KEY `main_reply_status_id_2c3fdd18_fk_main_status_id` (`status_id`),
  ADD KEY `main_reply_user_id_c04a947d_fk_main_customuser_id` (`user_id`);

--
-- Indexes for table `main_status`
--
ALTER TABLE `main_status`
  ADD PRIMARY KEY (`id`),
  ADD KEY `main_status_user_id_9e18e9fa_fk_main_customuser_id` (`user_id`);

--
-- Indexes for table `main_userprofile`
--
ALTER TABLE `main_userprofile`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=45;

--
-- AUTO_INCREMENT for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=41;

--
-- AUTO_INCREMENT for table `main_contactus`
--
ALTER TABLE `main_contactus`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `main_customuser`
--
ALTER TABLE `main_customuser`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT for table `main_customuser_groups`
--
ALTER TABLE `main_customuser_groups`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `main_customuser_user_permissions`
--
ALTER TABLE `main_customuser_user_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `main_reply`
--
ALTER TABLE `main_reply`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=39;

--
-- AUTO_INCREMENT for table `main_status`
--
ALTER TABLE `main_status`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=171;

--
-- AUTO_INCREMENT for table `main_userprofile`
--
ALTER TABLE `main_userprofile`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_main_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `main_customuser` (`id`);

--
-- Constraints for table `main_customuser_groups`
--
ALTER TABLE `main_customuser_groups`
  ADD CONSTRAINT `main_customuser_grou_customuser_id_13869e25_fk_main_cust` FOREIGN KEY (`customuser_id`) REFERENCES `main_customuser` (`id`),
  ADD CONSTRAINT `main_customuser_groups_group_id_8149f607_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `main_customuser_user_permissions`
--
ALTER TABLE `main_customuser_user_permissions`
  ADD CONSTRAINT `main_customuser_user_customuser_id_34d37f86_fk_main_cust` FOREIGN KEY (`customuser_id`) REFERENCES `main_customuser` (`id`),
  ADD CONSTRAINT `main_customuser_user_permission_id_38e6f657_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`);

--
-- Constraints for table `main_reply`
--
ALTER TABLE `main_reply`
  ADD CONSTRAINT `main_reply_status_id_2c3fdd18_fk_main_status_id` FOREIGN KEY (`status_id`) REFERENCES `main_status` (`id`),
  ADD CONSTRAINT `main_reply_user_id_c04a947d_fk_main_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `main_customuser` (`id`);

--
-- Constraints for table `main_status`
--
ALTER TABLE `main_status`
  ADD CONSTRAINT `main_status_user_id_9e18e9fa_fk_main_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `main_customuser` (`id`);

--
-- Constraints for table `main_userprofile`
--
ALTER TABLE `main_userprofile`
  ADD CONSTRAINT `main_userprofile_user_id_15c416f4_fk_main_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `main_customuser` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
