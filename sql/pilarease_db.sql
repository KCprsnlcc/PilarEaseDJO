-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Sep 03, 2024 at 12:05 PM
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
(44, 'Can view notification', 11, 'view_notification'),
(45, 'Can add referral', 12, 'add_referral'),
(46, 'Can change referral', 12, 'change_referral'),
(47, 'Can delete referral', 12, 'delete_referral'),
(48, 'Can view referral', 12, 'view_referral'),
(49, 'Can add chat message', 13, 'add_chatmessage'),
(50, 'Can change chat message', 13, 'change_chatmessage'),
(51, 'Can delete chat message', 13, 'delete_chatmessage'),
(52, 'Can view chat message', 13, 'view_chatmessage'),
(53, 'Can add questionnaire', 14, 'add_questionnaire'),
(54, 'Can change questionnaire', 14, 'change_questionnaire'),
(55, 'Can delete questionnaire', 14, 'delete_questionnaire'),
(56, 'Can view questionnaire', 14, 'view_questionnaire'),
(57, 'Can add chat session', 15, 'add_chatsession'),
(58, 'Can change chat session', 15, 'change_chatsession'),
(59, 'Can delete chat session', 15, 'delete_chatsession'),
(60, 'Can view chat session', 15, 'view_chatsession');

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
(13, 'main', 'chatmessage'),
(15, 'main', 'chatsession'),
(10, 'main', 'contactus'),
(6, 'main', 'customuser'),
(11, 'main', 'notification'),
(14, 'main', 'questionnaire'),
(12, 'main', 'referral'),
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
(40, 'main', '0020_customuser_block_duration_customuser_block_reason', '2024-08-07 17:23:11.106304'),
(41, 'main', '0021_referral', '2024-08-18 04:50:03.999042'),
(42, 'main', '0022_referral_other_reason_referral_referral_reason', '2024-08-18 15:19:50.187673'),
(43, 'main', '0023_chatmessage', '2024-08-24 07:25:42.947177'),
(45, 'main', '0024_questionnaire', '2024-08-24 12:57:36.929823'),
(46, 'main', '0025_alter_questionnaire_answer_and_more', '2024-08-24 13:08:56.984758'),
(47, 'main', '0026_alter_questionnaire_answer_and_more', '2024-08-24 13:17:09.673520'),
(48, 'main', '0027_alter_questionnaire_answer_and_more', '2024-08-24 13:22:46.255719'),
(49, 'main', '0025_alter_questionnaire_question', '2024-08-24 13:40:52.499720'),
(50, 'main', '0026_chatsession', '2024-08-24 13:52:44.588068'),
(56, 'main', '0027_alter_chatsession_session_data', '2024-08-25 02:34:24.569773'),
(57, 'main', '0028_alter_chatsession_user', '2024-08-25 02:34:24.887947'),
(58, 'main', '0029_alter_chatsession_user', '2024-08-25 02:34:25.010261'),
(59, 'main', '0030_delete_chatsession', '2024-08-25 02:34:25.025678'),
(60, 'main', '0031_chatsession', '2024-08-25 02:34:25.087616'),
(61, 'main', '0032_rename_timestamp_chatsession_created_at_and_more', '2024-08-25 02:34:25.283813'),
(62, 'main', '0033_delete_chatmessage', '2024-08-25 03:15:24.787056'),
(63, 'main', '0034_alter_chatsession_user', '2024-08-30 11:34:53.617197');

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
('086fci8yndp46xxek2hhpguam6qq7voy', 'eyJsYXN0X3Bhc3N3b3JkX3Jlc2V0X2VtYWlsIjoiMjAyNC0wOC0zMSAxMjo1MjoyMC4yNzcxOTQrMDA6MDAifQ:1skNbt:n6sY9T9TW_-e-qp_fBri26qP_MHzvcxNxDIfsHK6Jho', '2024-08-31 13:23:45.942175'),
('0fyued14rqewd6ksyv7tha5fs271gkvu', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1si5Wr:_jz8VHKJtG7_q_RwbeR4F1KrrIW4CEBBIYmNNNXjGao', '2024-08-25 05:41:05.173129'),
('0h3ey4z8r24wbhxy9n0ygbpoc2yrxxpw', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1si75P:-xQjT6ErkG4DlqYvRlNTrw54BIgbf27f98jbW3G-ga0', '2024-08-25 07:20:51.832150'),
('0mh7fjkq5zgr6bc3x1d0l8c8p304h6qz', '.eJxVjMsOwiAQRf-FtSG8BZfu-w1kZgCpGkhKuzL-uzbpQrf3nHNfLMK21riNvMQ5sQuz7PS7IdAjtx2kO7Rb59TbuszId4UfdPCpp_y8Hu7fQYVRv7Uu2Skvk4CizpoIwIIK1pL1aLM2UjsMohAp8L4YJEomeFBOCic8Int_APIPOCg:1skiRI:4-UkG8kGOyKgFP8h2avfMzGsUPSItOM3nmar0SU3FGk', '2024-09-01 11:38:12.731847'),
('0s3azr9j67sag6en95gxfoktn56uj1zw', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sjzHU:PnjvFTAdGu0hjedN_4hAqL616VLRM8wfEiGfBx0Fj_A', '2024-08-30 11:25:04.087055'),
('0w4qkczz4ilgn91rwjtinh4o7c3vcjrw', '.eJxVjEEOgjAQRe_StWkozLQzLt1zBtLOVIsaSCisjHdXEha6_e-9_zJD3NYybDUvw6jmbByZ0--YojzytBO9x-k2W5mndRmT3RV70Gr7WfPzcrh_ByXW8q0BgcVp5zwyBgxZWRIoZmpCk4Qzx44SiAKJtp4IW_QAnq6BGZnM-wPyYTco:1si2s7:VthBUjvGUQ-Ii5OeEHcpe3VvO8qpnqlXhRBSjCa-_fo', '2024-08-25 02:50:51.020450'),
('1mbx68numea66wz4lgk1r4tl3ywu3krm', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1siDDz:nm6azr6lx5A6bh1uL1l6CRSyn2yWZuxuvea75SBU5X8', '2024-08-25 13:54:07.484082'),
('1vxj5fbmh8x5qv6jx9ze1bg6op617cz7', 'eyJsYXN0X3Bhc3N3b3JkX3Jlc2V0X2VtYWlsX2tjcGVyc29uYWxhY2NAZ21haWwuY29tIjoiMjAyNC0wOS0wMSAwNDowNDowMC45ODk2NzkrMDA6MDAifQ:1skbos:Oj-xJq_HI3ytXOnizga_LEmtann13omaBZnV1iRUOaQ', '2024-09-01 04:34:06.135880'),
('24jinufs86zywn89nskdvgdg1jw1s7iw', 'eyJsYXN0X3Bhc3N3b3JkX3Jlc2V0X2VtYWlsX2tjcGVyc29uYWxhY2NAZ21haWwuY29tIjoiMjAyNC0wOS0wMSAwOTozMToyNi4zNjg0NjUrMDA6MDAifQ:1skgyc:SGy190L2Yx3-LlXt1z32eXKZXgt2auL1lzouS0P8u-A', '2024-09-01 10:04:30.971605'),
('24wicntsidgddqwcjxszdzfiov6prs30', 'eyJsYXN0X3Bhc3N3b3JkX3Jlc2V0X2VtYWlsX2tjcGVyc29uYWxhY2NAZ21haWwuY29tIjoiMjAyNC0wOS0wMSAwMTo1ODowNC45NjI2NjArMDA6MDAifQ:1skZr0:OUZ3_OcaEeY4V63A7WOWDMWAJ63C9vBPmxgwQ1dhohQ', '2024-09-01 02:28:10.501571'),
('278oa4ksqzzg7r866bg86suc2e2pz6m4', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1si5dZ:vLOJciwQlltuxYdKQPj5ow8kpVmRNVAo5VF_35ivamk', '2024-08-25 05:48:01.795707'),
('2lz003i5qtp94rwb96ivc1huf8zw6tq2', 'eyJsYXN0X3Bhc3N3b3JkX3Jlc2V0X2VtYWlsX2tjcGVyc29uYWxhY2NAZ21haWwuY29tIjoiMjAyNC0wOS0wMSAwNDo1OTo1Ni43ODM2MjUrMDA6MDAifQ:1skckW:z1BJiVg7RWVq1Q57VSlGSxq_eMtvcjNlgW1RFDIr5tM', '2024-09-01 05:33:40.556186'),
('2totlb7cywg9123il0qv6qdg0or0337a', 'eyJsYXN0X3Bhc3N3b3JkX3Jlc2V0X2VtYWlsX2tjcGVyc29uYWxhY2NAZ21haWwuY29tIjoiMjAyNC0wOS0wMSAwMzo1Mzo0OC41ODEzNTMrMDA6MDAifQ:1skbey:iWdFSZQ5gNKRXxxlCBdaFdGNw3_jm4S6deeYLSWVMRk', '2024-09-01 04:23:52.589394'),
('3rixg5jc764uy5cfi073fo8adyq6dmzp', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1siCUk:rETROt3w4Z3XO949G1SA8gnbj2zbtoC_4MNWuNOVi9A', '2024-08-25 13:07:22.208599'),
('3rxuvih5ek2bdn6vz8xqx7o3kqibfcjs', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1si6r5:nFrEmObujGB3NJMNXvnhtWP6lS4A91M0xs8623uJ48Q', '2024-08-25 07:06:03.748017'),
('448becopw1mu93ntpni2u974pimuj95y', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sk01d:zzhpm7gBGohvbc-8SE39g_PlyrfYTPsDWB1cpcfcAiE', '2024-08-30 12:12:45.954326'),
('4v79pqlj9nwifhvsipa8m2lwax2jyupi', 'eyJsYXN0X3Bhc3N3b3JkX3Jlc2V0X2VtYWlsX2tjcGVyc29uYWxhY2NAZ21haWwuY29tIjoiMjAyNC0wOS0wMSAwOToyNDozOC40NzYyMzUrMDA6MDAifQ:1skgp9:yW_uoRc726MKWkiMk-2rS4BtD17rGP96FbDf141fc4c', '2024-09-01 09:54:43.740723'),
('4ykdt9t4ovw2pv3oqklggtqytmht5ckf', 'eyJsYXN0X3Bhc3N3b3JkX3Jlc2V0X2VtYWlsIjoiMjAyNC0wOC0zMSAxMjo1MDozMS45MjQyNDkrMDA6MDAifQ:1skNaE:bmHZOHnFLtx7ls9Kp_S5nlYkJzmAgyldLLTMVU8rUZk', '2024-08-31 13:22:02.145802'),
('4z6x70lrw5n6228hysye3bx7nnlznwuo', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sjzdy:Aa2MNFkAz6kXOVNR0sUwMULD5AuC5QhCyGNAS5qplqc', '2024-08-30 11:48:18.753334'),
('551uvsajzh1m1etyt0eb09c5yghmrj7w', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sjzVm:MuHr8_1mfAZnR7jcE344dwXrjC6y9lSVVYaG64Aqsb8', '2024-08-30 11:39:50.282699'),
('5dg22osrnwtsvhwowo7l4g5a0jkkw6qe', 'eyJsYXN0X3Bhc3N3b3JkX3Jlc2V0X2VtYWlsIjoiMjAyNC0wOC0zMSAxMjo0MDoxMi42MjU3MTMrMDA6MDAifQ:1skNPy:XE-4a7-fuDlodpps3DGtTRlnaLdfjpfF7ZJyT70btXY', '2024-08-31 13:11:26.334713'),
('5i1vk81exaydekycfas5suo30ltivndz', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1si3aF:K2hmUegp-19M6mptsMnwSHPAI1lMv78sLXCINTcB8HE', '2024-08-25 03:36:27.700234'),
('66a468k7v7l3le41rfknj8muaa0c4mgb', 'eyJsYXN0X3Bhc3N3b3JkX3Jlc2V0X2VtYWlsX2tjcGVyc29uYWxhY2NAZ21haWwuY29tIjoiMjAyNC0wOC0zMSAxNToxMjo1NS4xNDU0NjcrMDA6MDAifQ:1skPme:Z1l-scwAvA3ynaOyvW9GL8Z_-V1sFO7z_E9VxzeMyDY', '2024-08-31 15:43:00.056599'),
('699aku3nbnxqnjy522dmxxn3bswotr96', 'eyJsYXN0X3Bhc3N3b3JkX3Jlc2V0X2VtYWlsX2tjcGVyc29uYWxhY2NAZ21haWwuY29tIjoiMjAyNC0wOS0wMSAwODozMTo0MS42NzQ2OTIrMDA6MDAifQ:1skfzu:U5NZWe7QGDDNtu9Fn5yN-pv8BQWBt8a52KcSCgexB4k', '2024-09-01 09:01:46.783023'),
('6hz9ipb57oryby1uyf26ztsw76c2wfrw', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sjzKj:pU16V1CyCNPkJJmpQ4PDf9LK7OfS_tki6pQfu7UvmNQ', '2024-08-30 11:28:25.729883'),
('6jn0fcnsjm40g8czu9rr72j39730ulju', 'eyJsYXN0X3Bhc3N3b3JkX3Jlc2V0X2VtYWlsX2tjcGVyc29uYWxhY2NAZ21haWwuY29tIjoiMjAyNC0wOC0zMSAxMzo1NjoyMy4zNDgwMTErMDA6MDAifQ:1skOaa:t_EX5RDb8N2m57DkH9ZkVVxht8efjrm7vMPLHh6C2sc', '2024-08-31 14:26:28.208796'),
('6shiwldtqlduai426xcp13469po8xld4', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1si6v6:0j7mN2xtloS0eA4QIbkMO_DQxXLe1eVL_Afo4UB_pcU', '2024-08-25 07:10:12.544170'),
('7fqt2be3ioczybrfu0qd4pg30ukyj8ub', '.eJxVjMsOwiAQRf-FtSGdlsfg0r3fQBhgpGogKe3K-O_apAvd3nPOfQkftrX4refFz0mchRan341CfOS6g3QP9dZkbHVdZpK7Ig_a5bWl_Lwc7t9BCb18a7BgrAI0iAysjYnkBssTAJIFRRMgDo5GJtYujplsdnGi4DSjwmDF-wOzjDc3:1skjNW:O6EMnWywlBCL7R-yUSdahm81T_pXF6Aqq3A0S4gnaYc', '2024-09-01 12:38:22.014636'),
('7grte44loq2jkz59z8g6mv7hpce6ne34', 'eyJsYXN0X3Bhc3N3b3JkX3Jlc2V0X2VtYWlsIjoiMjAyNC0wOC0zMSAxMzowMjowNy44MzU2ODIrMDA6MDAifQ:1skNlM:ugk-C9UcRlWvXyc5GcOck-Q2taDbM5WptV2fRWcl_hQ', '2024-08-31 13:33:32.130313'),
('7m84dzwf38xmzf282ndzd5ybmu55vvls', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1siCco:asqZeWVV8o294ADpYZcWLH1oiHx7IgZDG5fmKt6WVRA', '2024-08-25 13:15:42.251350'),
('7wyfx1z8dod9xfd1cmiuc2w458ey5d3o', 'eyJsYXN0X3Bhc3N3b3JkX3Jlc2V0X2VtYWlsX2tjcGVyc29uYWxhY2NAZ21haWwuY29tIjoiMjAyNC0wOS0wMSAwMzo1NjozOC4xODIwOTkrMDA6MDAifQ:1skbhl:a4bY3Jd0g0XFMK_pqPWiXSAeERMzYPgMT2RlSyvRlRU', '2024-09-01 04:26:45.716866'),
('902mcs8unljbwg28muimw7nut90op5yf', 'eyJsYXN0X3Bhc3N3b3JkX3Jlc2V0X2VtYWlsX2tjcGVyc29uYWxhY2NAZ21haWwuY29tIjoiMjAyNC0wOS0wMSAwMTo0NDowNC4xOTYzNzMrMDA6MDAifQ:1skZdR:t6qOGfCNZ-YsmbI8xsJi4d6d1ixpH_cQOVIjww1Gcu8', '2024-09-01 02:14:09.243395'),
('9lcdw7j6ho46ubepovtrgd7m2x7i4du2', '.eJxVjMsOwiAQRf-FtSGdlsfg0r3fQBhgpGogKe3K-O_apAvd3nPOfQkftrX4refFz0mchRan341CfOS6g3QP9dZkbHVdZpK7Ig_a5bWl_Lwc7t9BCb18a7BgrAI0iAysjYnkBssTAJIFRRMgDo5GJtYujplsdnGi4DSjwmDF-wOzjDc3:1sl4F5:PX5973sXrgqmO1T0ZJGIgTFyZKFnzCv6dxdEC1tW_2A', '2024-09-02 10:55:03.037423'),
('9nj9b513osu8u2k522xdpa2h9hnlucmj', '.eJx9zD0OwjAMQOGroKzQyM5PBZl6k8hKXahImiouYkDcHZCYO743fC-VSba4ksiztjE2Ft4iF5pzvKeVm9SFMqU0XH9Pp1pUUAaM6-DcWTygDQYDgDYX7D0eAb6hTnvsjUaaJpZHprnQgm7PNsFZ3Xvr0f_t9weAozhm:1skO3z:C_LApEKVSLzgqrPCZf6hkIRLDbMvZ-vFHo3JZxWp1ys', '2024-08-31 13:52:47.553635'),
('9q0gr3cvieab5s0bhw34dsgjikah2xnx', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1si69f:5VTXl-Hn3xYFvdoYoCVhkyC3x8mg2APMV4zhQwhJhTc', '2024-08-25 06:21:11.261614'),
('a2l5zh6n1ahhwre4450ebh9o93btchqs', 'eyJsYXN0X3Bhc3N3b3JkX3Jlc2V0X2VtYWlsX2tjcGVyc29uYWxhY2NAZ21haWwuY29tIjoiMjAyNC0wOS0wMSAwMzozMTo0OC43MTM1MjErMDA6MDAifQ:1skbJi:MWXugRVfa4NVpS-HDLOp5XgCa9RLHPojXkr1dxhOIPM', '2024-09-01 04:01:54.157802'),
('a57xfol2zed9joc2wz268p3jnrcc8ifi', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1si3MO:iFl85zYDDEGhvAnoyZRY7-_q3_Wm_v5z1vspnvoLyhI', '2024-08-25 03:22:08.644248'),
('a824roxb9113nh2p28sgezrocd64ypkp', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sjzVx:NEvVTE_UTbjCXcPKCNOTjkSXWKGdN7sT7stUVf1iK0I', '2024-08-30 11:40:01.504883'),
('a8kgp3x3hbe0tujc0a1tsqpszabz504f', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1siDht:8d1CqEOYwgnswvO2X2rxq1UAPgs-GZHbpe9I0ApQm6U', '2024-08-25 14:25:01.469157'),
('blz3wjqf4az1qv32qy0yzchol5lqun0x', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1si6Ji:6zPYRhn8havCKDAMvNvfsSB-wYpS0I4R8GQWEeUZACk', '2024-08-25 06:31:34.074372'),
('bmf47awww9o8e69140r2t4wsoreau5bz', 'eyJsYXN0X3Bhc3N3b3JkX3Jlc2V0X2VtYWlsX2tjcGVyc29uYWxhY2NAZ21haWwuY29tIjoiMjAyNC0wOS0wMSAwMjo1OTo0Ny44MzI2NzgrMDA6MDAifQ:1skaoj:jkEQd_iWahvXfcBpqllNNBTtVCeCMvgEIL4COGYcarc', '2024-09-01 03:29:53.187267'),
('c94o6bamu58h5iraecn9g7bmfmng7fsg', 'eyJsYXN0X3Bhc3N3b3JkX3Jlc2V0X2VtYWlsX2tjcGVyc29uYWxhY2NAZ21haWwuY29tIjoiMjAyNC0wOS0wMSAwMzowNjoxNy4yOTg0NTMrMDA6MDAifQ:1skawE:vv9ZZlXeuHdxoknVI3LncUpAEmGan_xYslNy4QqkJbw', '2024-09-01 03:37:38.888083'),
('cd38dkw4o66se7o71ukgaueco0l3d43o', 'eyJsYXN0X3Bhc3N3b3JkX3Jlc2V0X2VtYWlsIjoiMjAyNC0wOC0zMSAxMjo0NjoxNC4yNTgwMzgrMDA6MDAifQ:1skNUy:n0YdOejaIDCpQr-r6l3GDt79-M6Loo9UmhYcvxX7eQ4', '2024-08-31 13:16:36.553927'),
('cdnq7bs0f6uwo89baor6grpq74x4isbb', 'eyJsYXN0X3Bhc3N3b3JkX3Jlc2V0X2VtYWlsX2tjcGVyc29uYWxhY2NAZ21haWwuY29tIjoiMjAyNC0wOS0wMSAwMjowMDo0NS44NDY2MDYrMDA6MDAifQ:1skZtb:dgTRdHZqe1sqe1okuodmt0H9_FgoK77lCnBNdX8tUYQ', '2024-09-01 02:30:51.094823'),
('cmiynfsj0269unuvhbvsis0gn5hv5oiz', '.eJxVjEEOgjAQRe_StWkozLQzLt1zBtLOVIsaSCisjHdXEha6_e-9_zJD3NYybDUvw6jmbByZ0--YojzytBO9x-k2W5mndRmT3RV70Gr7WfPzcrh_ByXW8q0BgcVp5zwyBgxZWRIoZmpCk4Qzx44SiAKJtp4IW_QAnq6BGZnM-wPyYTco:1si5bv:7nD3WIChfnDCSJt0i7tQ7M9LtkhXytyNAhe_XOiXB5U', '2024-08-25 05:46:19.389701'),
('cumr18p2tegu63k7jaigj1fhzgbf23o3', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1siXl7:6xiaYMIBJn9P_zU_VHuKIeW7icAxIHggJACkCpw6vNY', '2024-08-26 11:49:41.296140'),
('d51ynox6gh1dgjyiww3g7m6h313jyt4u', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1si7EI:eoMfHFSOvchGAlUGTE46wJ_ZEq-C2zOATlJsk-eTF5M', '2024-08-25 07:30:02.243371'),
('e34g2nh4fsa2wpl2np9eooqq4a810m11', 'eyJsYXN0X3Bhc3N3b3JkX3Jlc2V0X2VtYWlsX2tjcGVyc29uYWxhY2NAZ21haWwuY29tIjoiMjAyNC0wOS0wMSAwMzoyMzozMi40NDU1NTkrMDA6MDAifQ:1skbBh:8r47rkgSTM8uC_sUVeqO_xi6Xcjqamm3pxEIwxQ-yYo', '2024-09-01 03:53:37.145973'),
('f0g5gxx3q161dkcmwd9lc4pke8wwqqmu', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1si6gg:NtIbGNXg8zEVUgj0iSCskyzQfd3G0_Tp6QdVCOPAdZ4', '2024-08-25 06:55:18.186951'),
('f476hqd6wqc8nwyra5rblsmolkzn0g6b', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sjz4x:PdfX3NLkVi16Mhr4x7qf8hGxv1OT7Pz6RBXe_gSVxYE', '2024-08-30 11:12:07.904515'),
('f4ds79qlki2nu0z0ldhoceehhe9q7bbf', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1si522:OW6K4zXI2NikulXldlHdOgdBr3MdtiRSzr8zj0LUaFs', '2024-08-25 05:09:14.441765'),
('fsl07vnypb6nzailayqal9q6g5tz235a', 'eyJsYXN0X3Bhc3N3b3JkX3Jlc2V0X2VtYWlsX2tjcGVyc29uYWxhY2NAZ21haWwuY29tIjoiMjAyNC0wOS0wMSAwMjowNDo1MS4yNTA1MTQrMDA6MDAifQ:1skZxX:9ARXuzYAaf4sQIzKjk4IboR9eosOH2TMYbIUfCV0IS0', '2024-09-01 02:34:55.115353'),
('g6om1wdnuvlh0de16utm4lxyc011l9rm', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sjzTq:guW-OuzuNA_SyECUSpiZplO6wPNsNv1UOhhi4L-DgnM', '2024-08-30 11:37:50.585324'),
('i4gys5jdjdpz4m0jpb36xaayvrker2f9', 'eyJsYXN0X3Bhc3N3b3JkX3Jlc2V0X2VtYWlsX2tjcGVyc29uYWxhY2NAZ21haWwuY29tIjoiMjAyNC0wOS0wMSAwMzoyOTo1My43NjMzNjMrMDA6MDAifQ:1skbHr:94c6Uthw1MDogEu4C7fRm5To_zmS5RVOlgoZQOZpDzs', '2024-09-01 03:59:59.787974'),
('ic8szf9hm4j28ldte03q1yen9wxpr5i7', 'eyJsYXN0X3Bhc3N3b3JkX3Jlc2V0X2VtYWlsX2tjcGVyc29uYWxhY2NAZ21haWwuY29tIjoiMjAyNC0wOS0wMSAwOTowODo1Mi4wMDczNDErMDA6MDAifQ:1skgZs:_-icCsetCFW2ldx8zVIbtvrH2gc6YYOegk4V_iwP1Bg', '2024-09-01 09:38:56.222903'),
('iznfytp9cbnfb5qtxyyg8rmsyez97ct4', '.eJxVjMsOwiAQRf-FtSGdlsfg0r3fQBhgpGogKe3K-O_apAvd3nPOfQkftrX4refFz0mchRan341CfOS6g3QP9dZkbHVdZpK7Ig_a5bWl_Lwc7t9BCb18a7BgrAI0iAysjYnkBssTAJIFRRMgDo5GJtYujplsdnGi4DSjwmDF-wOzjDc3:1sl4DK:Zo_TcWdj5D_vkqZjh_RPF2mEPHMIvac91hQAwxvdX-Y', '2024-09-02 10:53:14.150765'),
('j0o646swrpztrl6gqxrj36wslck07lb1', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1siCVV:gin0fGbb92wUiHpAhCItuNVVfWwt-jJYjBL6VFSDEg8', '2024-08-25 13:08:09.237229'),
('j8r36tvnoima20xgzg6uachlsjvf5h42', 'eyJsYXN0X3Bhc3N3b3JkX3Jlc2V0X2VtYWlsX2tjcGVyc29uYWxhY2NAZ21haWwuY29tIjoiMjAyNC0wOC0zMSAxMzo1MjoxNi4xOTEzMzQrMDA6MDAifQ:1skOWb:gPvBJCAFPoJVFDFfq9m47EWt-H7Eblsy36RI97Qx-pw', '2024-08-31 14:22:21.256777'),
('jfu88iz9icpphsj0pnhd879jgd3jku7m', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1siDTP:jaeSLlePfVwVoxKpKimoBcxDkNw2_DyrV5ZwEmyotj8', '2024-08-25 14:10:03.286693'),
('jm2t866ryj9fmbfchz93xp37m377s2lx', 'eyJsYXN0X3Bhc3N3b3JkX3Jlc2V0X2VtYWlsX2tjcGVyc29uYWxhY2NAZ21haWwuY29tIjoiMjAyNC0wOC0zMSAxNTo1OTozNy43NzczODArMDA6MDAifQ:1skQVr:fooaFf4uXlMUFa_ZxmJPWiGcMnsg2pDsMmY7nwSGeMc', '2024-08-31 16:29:43.045651'),
('k45vljunpyfu8e3e03miskke3qz87ko9', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1si5pZ:q_fo6QYkbqYGh8nIY0998kjw4KHJNCYn-7rNYfPk48E', '2024-08-25 06:00:25.379485'),
('kizqtw4i06vicft2w9tvdd9fvo0wrvm6', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sjzvE:JAaeLSZ6FmJB1-5JUPvydOVyVaegZKH3bIsnxUissBo', '2024-08-30 12:06:08.810492'),
('luneonl66a5i3fhf86iixqmd8t5ful4z', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sjzAw:vWH3ytMCP6Dr5WK-r3ctJIo5lqI6yRwS812f6YyDxVQ', '2024-08-30 11:18:18.809134'),
('m0dd09wwr16si03tu6t2mprh7sti2evr', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1si5BO:cs1HyEw0Uy6ak26qUu4mIWtFqZfq1PlamZ2lC-A1QC0', '2024-08-25 05:18:54.795466'),
('m8w0illy8af2oqekptsbpfke13x7j5o3', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sk00r:tYA9IrH79lqcbzNo2wV_zf4ZpL5HiOYPxVzTX3p8EgM', '2024-08-30 12:11:57.020955'),
('mg9sj9y7qmdo8nbn64uvsr7zgugecv1i', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sk0KP:zbcyLobElrUw15D3rv9AYeWuYe2XxanOGe3RX3W-shU', '2024-08-30 12:32:09.330493'),
('n2hmib18hfh3pbytl93p49uoh2kcntje', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1si5JQ:hfJlEe59UikGH7jNA3O6i34vACwFy03T_s5rgS34IEA', '2024-08-25 05:27:12.460168'),
('n72kevf0so5msqcffd1ho6u7e5bjqjov', 'eyJsYXN0X3Bhc3N3b3JkX3Jlc2V0X2VtYWlsX2tjcGVyc29uYWxhY2NAZ21haWwuY29tIjoiMjAyNC0wOS0wMSAxMDo1MTo1NC4yMjc2NTArMDA6MDAifQ:1skiBc:rsuE-vSl-XEfa9c29eD7TsrqdILcKosBPkUoeIz1hg4', '2024-09-01 11:22:00.022278'),
('nay8xebljwyqc1ymdatugzsuohz8hiaz', 'eyJsYXN0X3Bhc3N3b3JkX3Jlc2V0X2VtYWlsX2tjcGVyc29uYWxhY2NAZ21haWwuY29tIjoiMjAyNC0wOS0wMSAxMDoyOTo1Mi4wNjE0MzQrMDA6MDAifQ:1skhqH:WQd6eNu71yJcCCEqWfbgeOudbUVlE1JHMQjAEjZF5aM', '2024-09-01 10:59:57.534566'),
('ng9qs29rrfssf0d706ge0gvuzttwzvv6', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sjzVm:MuHr8_1mfAZnR7jcE344dwXrjC6y9lSVVYaG64Aqsb8', '2024-08-30 11:39:50.574651'),
('nkixj2ok7o3qdntdv8hu4ugh4vtrqcep', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1si4uQ:emG_7Hhp4AUiHzxAnbwUGrZ-jagjgVwxcFwo_eM2dhU', '2024-08-25 05:01:22.730019'),
('nxp1yba7sojtth901lze3sssqfh5262p', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1siDIx:l04VWuJ5qfqzrXxWirzlX7Zji8ssmniCjpHFrqqMRw8', '2024-08-25 13:59:15.224899'),
('nzmfo32bvevql14ar8pfwpml9efrseoq', 'eyJsYXN0X3Bhc3N3b3JkX3Jlc2V0X2VtYWlsX2tjcGVyc29uYWxhY2NAZ21haWwuY29tIjoiMjAyNC0wOS0wMSAwMzozNTozMy4wMTE5MzkrMDA6MDAifQ:1skbNK:vf9pdN4rCGwPYVtBeTJkQa2AEsvGiybl4v68IZTuou8', '2024-09-01 04:05:38.140087'),
('olruig02ij87kxjytd21l8lphw7svvoo', 'eyJsYXN0X3Bhc3N3b3JkX3Jlc2V0X2VtYWlsX2tjcGVyc29uYWxhY2NAZ21haWwuY29tIjoiMjAyNC0wOC0zMSAxNjozNToxOC45MjEzODErMDA6MDAifQ:1skR4T:IvszAP3sclCRcSZx-jigcg53f2wr7KVndJV5_7pj0Z8', '2024-08-31 17:05:29.852124'),
('otc50f2ul0pjbdl92um0oe1r4ic115xu', 'eyJsYXN0X3Bhc3N3b3JkX3Jlc2V0X2VtYWlsX2tjcGVyc29uYWxhY2NAZ21haWwuY29tIjoiMjAyNC0wOS0wMSAxMDowOTo1OS4wODE5MzErMDA6MDAifQ:1skhX3:NOW85GngZSIaNGs7-juM1wK0bD2j0fBVn2RVJP25Mc4', '2024-09-01 10:40:05.288241'),
('oxpzmz36df8bfa7wwkvvnb7wvvpshmj9', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sjzG6:IpVyC1IuM_iXM0mJO26KWV8yHtR0uROjvqwHTNcAYrg', '2024-08-30 11:23:38.192806'),
('p6433igq6nn0cpo38ck2a6kyokzjxkjq', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1siCiG:wgVXNlgsM3a9maoRp_-LCX1ZUwe9SS0UvMkM1T1rEwQ', '2024-08-25 13:21:20.007558'),
('pefzwmabpl01frlkx86xtcw9c29gdsyi', 'eyJsYXN0X3Bhc3N3b3JkX3Jlc2V0X2VtYWlsX2tjcGVyc29uYWxhY2NAZ21haWwuY29tIjoiMjAyNC0wOS0wMSAwMzo0NToxMi45NTMxMTgrMDA6MDAifQ:1skbWg:3twdQySR8vw6AgmEunbyCDtqrJAtxk5zFmYX3Hf7A64', '2024-09-01 04:15:18.375900'),
('ppes4c8y1vdqvnun235dy438f5qht2ck', 'eyJsYXN0X3Bhc3N3b3JkX3Jlc2V0X2VtYWlsX2tjcGVyc29uYWxhY2NAZ21haWwuY29tIjoiMjAyNC0wOS0wMSAwMjo0Mjo1My44MDY2OTIrMDA6MDAifQ:1skaYN:DmzgCnPZCAO6l6FphHduDOFJKcGKm1whA91iNKZG4TE', '2024-09-01 03:12:59.127452'),
('pqnhxo4pn0bo1vfyjc3zvnvrh0671o5z', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1si7T3:U43PcejVkzCIuM6xvbVA1i6-12gsNH21VZjf_Z8LVM0', '2024-08-25 07:45:17.898226'),
('pu7yekr77y586p7w1pmefprm7rhob875', '.eJxVjMsOwiAQRf-FtSGdlsfg0r3fQBhgpGogKe3K-O_apAvd3nPOfQkftrX4refFz0mchRan341CfOS6g3QP9dZkbHVdZpK7Ig_a5bWl_Lwc7t9BCb18a7BgrAI0iAysjYnkBssTAJIFRRMgDo5GJtYujplsdnGi4DSjwmDF-wOzjDc3:1skmWK:TuKQwJqHXhrJ8xvSWSc-sS10jJvKMdTK9JFcIm0tVOI', '2024-09-01 15:59:40.979879'),
('pxytntsmdrwl6xjgs2b2x3v48b1k56fo', 'eyJsYXN0X3Bhc3N3b3JkX3Jlc2V0X2VtYWlsX2tjcGVyc29uYWxhY2NAZ21haWwuY29tIjoiMjAyNC0wOS0wMSAwNDozMzoyMC4yMTQ5OTYrMDA6MDAifQ:1skcHF:-Pm7CfRz8S3Z8WXhR48SIBEoTby_czk4IimnHv5Ujl4', '2024-09-01 05:03:25.233370'),
('q6q0alvr8h1aciltkgx6qic2dfj09us1', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1siD7m:EmknFSV5Mu344Igt1TFSKwSYwcOMrbdI9ysydpDm9H0', '2024-08-25 13:47:42.702491'),
('qiqvci57yp6r6x2wp6n5lyjb0i6pe6v7', '.eJx9zLEOwiAQANBfMaxacvRKpUz-CbnQqzZCabgaB-O_q4lz1ze8l0okW1hJ5FnqGCoLb4EzzSnc48pVykKJYrxcf6ZjycqrFtqugaEBcwDjEb3ttYOzRXME8ADqtNfeaKRpYnkkmjMtptu73bfT6LC38L_fH4QBOGo:1skZXY:8oGqNXwCXlMGp0_lSg1EX9uDrBKL2T45i590F-cSM9U', '2024-09-01 02:08:04.815742'),
('qweoli23g3mdw70cn0ykev18qf4ol1bn', 'eyJsYXN0X3Bhc3N3b3JkX3Jlc2V0X2VtYWlsX2tjcGVyc29uYWxhY2NAZ21haWwuY29tIjoiMjAyNC0wOS0wMSAwODo0ODowNy4zNTUxOTkrMDA6MDAifQ:1skgH8:Cn8mugZjVuHwgNKT7xzuc1oesnc8gXIa9TjDCrfLLrs', '2024-09-01 09:19:34.293827'),
('qy03wgzo740rrwxxo8frh3vgohrnkvs5', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1si57y:YHbf1TRy-0ys1ptzFX_pUTnR7oKhKPM8RyMX2zy73VY', '2024-08-25 05:15:22.079040'),
('rjakddguiogw0b8pcsadply2yi4gcc77', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sk0PT:1iATYr_X0rJdGg26r_m4IiPfcz6zAXO4sBNgow36J30', '2024-08-30 12:37:23.763827'),
('s8brscvpqloaknb2xtrwv8ee9wq9tvxq', 'eyJsYXN0X3Bhc3N3b3JkX3Jlc2V0X2VtYWlsIjoiMjAyNC0wOC0zMSAxMzoxMTo0NS40MDE4NDkrMDA6MDAifQ:1skNvx:n5e9jsRqgzo0hqVoq7VSncL9j6hP80f_dqw9G_5GG64', '2024-08-31 13:44:29.321502'),
('suacn9czlvodo0vxaqy2cq4pb673h85d', '.eJxVjMEOwiAQBf-FsyEgZQGP3vsNBNhFqgaS0p6M_64kPej1zcx7MR_2rfi90-oXZBcmHTv9jjGkB9VB8B7qrfHU6rYukQ-FH7TzuSE9r4f7d1BCL6O2DrRDkyQpIcEQogWjXLTgzolcNiAmUAYw60moTFEGlb-alpqEluz9AfjeN58:1si3FU:089kaxUWbyrAv3IKZbbiPDqPQn4giKdXLWg35Cq-s50', '2024-08-25 03:15:00.499552'),
('ti8223xc6tbekx0hv5okggl3pk8zjvme', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sjzbH:N-2vL0neL5pETkpoCAeAKW0XOqPdT-isgVYoPC-Y8q0', '2024-08-30 11:45:31.660923'),
('tzg5hjtwgnvdmdz7wgfzn3w78497k16x', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1si5FS:FAwzjtlhmkDQnW8pilYurkquZxQi1Y0iRwYDPxD-XB0', '2024-08-25 05:23:06.665116'),
('usu4oth1osw3zwwqteug9b25bbu5piaj', 'eyJsYXN0X3Bhc3N3b3JkX3Jlc2V0X2VtYWlsX2tjcGVyc29uYWxhY2NAZ21haWwuY29tIjoiMjAyNC0wOS0wMSAwOToxOTozMS42MDI4MDYrMDA6MDAifQ:1skgkC:XscXi98yiEGxwRYsUy7X-o-AyD4675ON6FD9xvEkP1M', '2024-09-01 09:49:36.649130'),
('uw3wu2zeulaaf49567vh69qnh8ckmy3d', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1siD4O:6zPR20-3h2byRUdZOTZOhdUh-w9FxyoZ8xrnmNeTgZs', '2024-08-25 13:44:12.844433'),
('v1s0wprqyj4f6icr984ekrbf92x6ebyr', '.eJx9zEEKwjAQQNGrSLbaMJOOkmTVm4QhTbWYNCVTcSHeXQXXhb_78F4qs2xhZZFnbWNoSdIWUuE5h_uNR56mJI_Mc-EFabj-ho61KK8MGOrAdj0e8Oy_EWhnnXF4BPAA6rRnxzU1qQtnjnGHNRffk0ZAsPRn3x-Kmzh4:1skPzq:jeOhXPmFjGY7OMHXVbPSjv3E9HVAkknxWB_GdQkI_hw', '2024-08-31 15:56:38.091052'),
('v36h49qpssy91ffdf63eek4uwj1kjb50', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1si3tZ:wqQcxxiPymYxLCSJzr91Hlk_fV55lSLLlJjoQ0l1lx4', '2024-08-25 03:56:25.093655'),
('v5p88ts3w6cyvuitit9c0qs526nhax1x', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1si4ff:Tk_ZnZ7g_fXjAEGTgVeAonoeSCyHxmL-VC9KjhkUBP0', '2024-08-25 04:46:07.863616'),
('vpwz6u8nn68kwoedyht760b2niayjni0', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1sjzpL:FfnO3qGNkn5a_ehkObYeUJJVQlChS2tEs6C_Z4x-dAE', '2024-08-30 12:00:03.275046'),
('vxxj6buc31u44436hii3mr6dbzsnglqa', 'eyJsYXN0X3Bhc3N3b3JkX3Jlc2V0X2VtYWlsX2tjcGVyc29uYWxhY2NAZ21haWwuY29tIjoiMjAyNC0wOS0wMSAxMTozMDoyMC40ODYxODUrMDA6MDAifQ:1skipd:Ak_3wDt_O1Kf1VuIpbnzxne1Iim6Sa9H_KM-O-2G4p8', '2024-09-01 12:03:21.717758'),
('vywfpd9vkxeghfruxq458fz7vnrtbifw', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1si7aM:rjBRWZHKTNdVdShm60If1Wkl2TeYcX0mTJctCJwanHk', '2024-08-25 07:52:50.892572'),
('w0tmc3vfkp9kf70fcnxjbjia6i7vynzv', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1si3n4:J3Oy4ZYVDSt3DgID0ceEHM1nB648Cj2jxcNmNTSxVVA', '2024-08-25 03:49:42.751346'),
('wbk9i66q4kahbts316it0hdkgmi9349x', 'eyJsYXN0X3Bhc3N3b3JkX3Jlc2V0X2VtYWlsX2tjcGVyc29uYWxhY2NAZ21haWwuY29tIjoiMjAyNC0wOS0wMSAwMzoxMzo0NS4xMzg3MjcrMDA6MDAifQ:1skb2E:4hsUvfBUQs47CuTFSwbJa4f52R8tvh6z2_OwF_Z-wik', '2024-09-01 03:43:50.068386'),
('wvnnve9ato12ovlxlv9id50bopfnnwki', 'eyJsYXN0X3Bhc3N3b3JkX3Jlc2V0X2VtYWlsX2tjcGVyc29uYWxhY2NAZ21haWwuY29tIjoiMjAyNC0wOC0zMSAxNTozNjoyMi4yMjM4MjMrMDA6MDAifQ:1skQ9L:U79aPshwmyO-VljN5oHFyWIjdU7BeGEtQ1bpbiG7bRM', '2024-08-31 16:06:27.586021'),
('xiu70374vurk040cpr28527twy90hspi', 'eyJsYXN0X3Bhc3N3b3JkX3Jlc2V0X2VtYWlsX2tjcGVyc29uYWxhY2NAZ21haWwuY29tIjoiMjAyNC0wOS0wMSAwMjo0OToxMS4yMDg1NjArMDA6MDAifQ:1skaeS:4LU8MxVhG0z5O9j2TNdRdAfBdw-CjLoQCZT9R_w-Lk0', '2024-09-01 03:19:16.220952'),
('xqtnyqg68uo7u7914qyabbbizfp1kwr6', 'eyJsYXN0X3Bhc3N3b3JkX3Jlc2V0X2VtYWlsX2tjcGVyc29uYWxhY2NAZ21haWwuY29tIjoiMjAyNC0wOS0wMSAxMDozNjowMC43NjAzOTMrMDA6MDAifQ:1skhyf:y6rfcmN4w8cu4p6qgif_nzCB4Kh24b4zUVXw1oVyTpU', '2024-09-01 11:08:37.632309'),
('xrhhwpff14xpsnzhdbhasmk7bh6ddklq', 'eyJsYXN0X3Bhc3N3b3JkX3Jlc2V0X2VtYWlsX2tjcGVyc29uYWxhY2NAZ21haWwuY29tIjoiMjAyNC0wOS0wMSAwMjoxNTozNi40ODEyOTMrMDA6MDAifQ:1ska7x:20kY4iypSTimO0z77Ww91Y831gbmqaq1VmaWttk1tek', '2024-09-01 02:45:41.218761'),
('y53py22irhbn40j4nxhj5x4vsmlptd2g', 'eyJsYXN0X3Bhc3N3b3JkX3Jlc2V0X2VtYWlsX2tjcGVyc29uYWxhY2NAZ21haWwuY29tIjoiMjAyNC0wOS0wMSAwODoyMDozNC40MDU5MzcrMDA6MDAifQ:1skfp8:sEpCjF0tLQV1uaHiHFzBc4DA00muAJBZg_-qLi_ZzrI', '2024-09-01 08:50:38.327774'),
('yq8r46w1qftqmtjmj53keu5m2ut8u4tc', '.eJxVjEEOwiAQRe_C2hBKGWBcuvcMhOmAVA0kpV0Z765NutDtf-_9lwhxW0vYelrCzOIsQJx-N4rTI9Ud8D3WW5NTq-syk9wVedAur43T83K4fwcl9vKtjR9hQJcnD5iRlRsNK4NoOSUNFrQHo5UmGCwQqmgMZOuzJSQdXWLx_gCv1zbZ:1si5go:aMmh3Mt4WhXf5Qlv-RUL8NvndyrI_bsDZL4cjf_vVXM', '2024-08-25 05:51:22.164921'),
('ywzgzy304r76k9qji4scduby6qtsickp', 'eyJsYXN0X3Bhc3N3b3JkX3Jlc2V0X2VtYWlsX2tjcGVyc29uYWxhY2NAZ21haWwuY29tIjoiMjAyNC0wOS0wMSAxMToyMzo1NS43MDMwMDcrMDA6MDAifQ:1skiga:mFXan4mmg7pxnWm7npijiUQezocAfnKpgNcKXQUq1hc', '2024-09-01 11:54:00.735464'),
('z1ildtku1rxq1tf5srsv23zal9jgz2px', '.eJxVjMsOwiAQRf-FtSGdlsfg0r3fQBhgpGogKe3K-O_apAvd3nPOfQkftrX4refFz0mchRan341CfOS6g3QP9dZkbHVdZpK7Ig_a5bWl_Lwc7t9BCb18a7BgrAI0iAysjYnkBssTAJIFRRMgDo5GJtYujplsdnGi4DSjwmDF-wOzjDc3:1skmZr:3Qlsu_S-LqxiHPJJ1gp6bHeUMffjI5nIj5M4rHBdE6c', '2024-09-01 16:03:19.673738');

-- --------------------------------------------------------

--
-- Table structure for table `main_chatsession`
--

CREATE TABLE `main_chatsession` (
  `id` bigint(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `user_id` bigint(20) NOT NULL,
  `session_data` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`session_data`)),
  `updated_at` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `main_chatsession`
--

INSERT INTO `main_chatsession` (`id`, `created_at`, `user_id`, `session_data`, `updated_at`) VALUES
(76, '2024-08-30 12:04:21.829540', 5, '[{\"text\": \"12:04 PM\", \"sender\": \"timestamp\"}, {\"text\": \"Hello! Welcome to Piracle, your emotional support companion. How can I assist you today? Should we start?\", \"sender\": \"bot\", \"timestamp\": \"2024-08-30T12:04:21.797Z\"}, {\"text\": \"Hello! Welcome to Piracle, your emotional support companion. How can I assist you today? Should we start?\", \"sender\": \"bot\", \"timestamp\": \"2024-08-30T12:04:21.798Z\", \"questionIndex\": -1}, {\"text\": \"Start\", \"sender\": \"user\", \"timestamp\": \"2024-08-30T12:04:23.097Z\"}, {\"text\": \"Start\", \"sender\": \"user\", \"timestamp\": \"2024-08-30T12:04:23.097Z\", \"questionIndex\": -1}, {\"text\": \"What aspects of your academic life cause you the most stress?\", \"sender\": \"bot\", \"timestamp\": \"2024-08-30T12:04:27.102Z\"}, {\"text\": \"What aspects of your academic life cause you the most stress?\", \"sender\": \"bot\", \"timestamp\": \"2024-08-30T12:04:27.103Z\", \"questionIndex\": 0}, {\"text\": \"Understanding difficult subjects or topics.\", \"sender\": \"user\", \"timestamp\": \"2024-08-30T12:04:51.466Z\"}, {\"text\": \"Struggling with difficult subjects can cause stress and anxiety. Seeking help or using different study methods can reduce these feelings and improve your mental health.\", \"sender\": \"bot\", \"timestamp\": \"2024-08-30T12:04:53.971Z\"}, {\"text\": \"Hello! Welcome to Piracle, your emotional support companion. How can I assist you today? Should we start?\", \"sender\": \"bot\", \"timestamp\": \"2024-08-30T12:07:22.912Z\"}, {\"text\": \"Hello! Welcome to Piracle, your emotional support companion. How can I assist you today? Should we start?\", \"sender\": \"bot\", \"timestamp\": \"2024-08-30T12:07:22.915Z\"}, {\"text\": \"Start\", \"sender\": \"user\", \"timestamp\": \"2024-08-30T12:07:22.917Z\"}, {\"text\": \"Start\", \"sender\": \"user\", \"timestamp\": \"2024-08-30T12:07:22.919Z\"}, {\"text\": \"What aspects of your academic life cause you the most stress?\", \"sender\": \"bot\", \"timestamp\": \"2024-08-30T12:07:22.921Z\"}, {\"text\": \"What aspects of your academic life cause you the most stress?\", \"sender\": \"bot\", \"timestamp\": \"2024-08-30T12:07:22.924Z\"}, {\"text\": \"Understanding difficult subjects or topics.\", \"sender\": \"user\", \"timestamp\": \"2024-08-30T12:07:22.926Z\"}, {\"text\": \"Struggling with difficult subjects can cause stress and anxiety. Seeking help or using different study methods can reduce these feelings and improve your mental health.\", \"sender\": \"bot\", \"timestamp\": \"2024-08-30T12:07:22.928Z\"}, {\"text\": \"Hello! Welcome to Piracle, your emotional support companion. How can I assist you today? Should we start?\", \"sender\": \"bot\", \"timestamp\": \"2024-09-01T12:08:16.044Z\"}, {\"text\": \"Hello! Welcome to Piracle, your emotional support companion. How can I assist you today? Should we start?\", \"sender\": \"bot\", \"timestamp\": \"2024-09-01T12:08:16.046Z\"}, {\"text\": \"Start\", \"sender\": \"user\", \"timestamp\": \"2024-09-01T12:08:16.047Z\"}, {\"text\": \"Start\", \"sender\": \"user\", \"timestamp\": \"2024-09-01T12:08:16.049Z\"}, {\"text\": \"What aspects of your academic life cause you the most stress?\", \"sender\": \"bot\", \"timestamp\": \"2024-09-01T12:08:16.051Z\"}, {\"text\": \"What aspects of your academic life cause you the most stress?\", \"sender\": \"bot\", \"timestamp\": \"2024-09-01T12:08:16.053Z\"}, {\"text\": \"Understanding difficult subjects or topics.\", \"sender\": \"user\", \"timestamp\": \"2024-09-01T12:08:16.054Z\"}, {\"text\": \"Struggling with difficult subjects can cause stress and anxiety. Seeking help or using different study methods can reduce these feelings and improve your mental health.\", \"sender\": \"bot\", \"timestamp\": \"2024-09-01T12:08:16.056Z\"}, {\"text\": \"Hello! Welcome to Piracle, your emotional support companion. How can I assist you today? Should we start?\", \"sender\": \"bot\", \"timestamp\": \"2024-09-01T12:08:16.058Z\"}, {\"text\": \"Hello! Welcome to Piracle, your emotional support companion. How can I assist you today? Should we start?\", \"sender\": \"bot\", \"timestamp\": \"2024-09-01T12:08:16.060Z\"}, {\"text\": \"Start\", \"sender\": \"user\", \"timestamp\": \"2024-09-01T12:08:16.063Z\"}, {\"text\": \"Start\", \"sender\": \"user\", \"timestamp\": \"2024-09-01T12:08:16.065Z\"}, {\"text\": \"What aspects of your academic life cause you the most stress?\", \"sender\": \"bot\", \"timestamp\": \"2024-09-01T12:08:16.067Z\"}, {\"text\": \"What aspects of your academic life cause you the most stress?\", \"sender\": \"bot\", \"timestamp\": \"2024-09-01T12:08:16.068Z\"}, {\"text\": \"Understanding difficult subjects or topics.\", \"sender\": \"user\", \"timestamp\": \"2024-09-01T12:08:16.070Z\"}, {\"text\": \"Struggling with difficult subjects can cause stress and anxiety. Seeking help or using different study methods can reduce these feelings and improve your mental health.\", \"sender\": \"bot\", \"timestamp\": \"2024-09-01T12:08:16.072Z\"}, {\"text\": \"Hello! Welcome to Piracle, your emotional support companion. How can I assist you today? Should we start?\", \"sender\": \"bot\", \"timestamp\": \"2024-09-01T12:08:20.229Z\"}, {\"text\": \"Hello! Welcome to Piracle, your emotional support companion. How can I assist you today? Should we start?\", \"sender\": \"bot\", \"timestamp\": \"2024-09-01T12:08:20.230Z\"}, {\"text\": \"Start\", \"sender\": \"user\", \"timestamp\": \"2024-09-01T12:08:20.232Z\"}, {\"text\": \"Start\", \"sender\": \"user\", \"timestamp\": \"2024-09-01T12:08:20.235Z\"}, {\"text\": \"What aspects of your academic life cause you the most stress?\", \"sender\": \"bot\", \"timestamp\": \"2024-09-01T12:08:20.237Z\"}, {\"text\": \"What aspects of your academic life cause you the most stress?\", \"sender\": \"bot\", \"timestamp\": \"2024-09-01T12:08:20.238Z\"}, {\"text\": \"Understanding difficult subjects or topics.\", \"sender\": \"user\", \"timestamp\": \"2024-09-01T12:08:20.239Z\"}, {\"text\": \"Struggling with difficult subjects can cause stress and anxiety. Seeking help or using different study methods can reduce these feelings and improve your mental health.\", \"sender\": \"bot\", \"timestamp\": \"2024-09-01T12:08:20.241Z\"}, {\"text\": \"Hello! Welcome to Piracle, your emotional support companion. How can I assist you today? Should we start?\", \"sender\": \"bot\", \"timestamp\": \"2024-09-01T12:08:20.244Z\"}, {\"text\": \"Hello! Welcome to Piracle, your emotional support companion. How can I assist you today? Should we start?\", \"sender\": \"bot\", \"timestamp\": \"2024-09-01T12:08:20.246Z\"}, {\"text\": \"Start\", \"sender\": \"user\", \"timestamp\": \"2024-09-01T12:08:20.248Z\"}, {\"text\": \"Start\", \"sender\": \"user\", \"timestamp\": \"2024-09-01T12:08:20.250Z\"}, {\"text\": \"What aspects of your academic life cause you the most stress?\", \"sender\": \"bot\", \"timestamp\": \"2024-09-01T12:08:20.252Z\"}, {\"text\": \"What aspects of your academic life cause you the most stress?\", \"sender\": \"bot\", \"timestamp\": \"2024-09-01T12:08:20.254Z\"}, {\"text\": \"Understanding difficult subjects or topics.\", \"sender\": \"user\", \"timestamp\": \"2024-09-01T12:08:20.256Z\"}, {\"text\": \"Struggling with difficult subjects can cause stress and anxiety. Seeking help or using different study methods can reduce these feelings and improve your mental health.\", \"sender\": \"bot\", \"timestamp\": \"2024-09-01T12:08:20.258Z\"}, {\"text\": \"Hello! Welcome to Piracle, your emotional support companion. How can I assist you today? Should we start?\", \"sender\": \"bot\", \"timestamp\": \"2024-09-01T12:08:20.260Z\"}, {\"text\": \"Hello! Welcome to Piracle, your emotional support companion. How can I assist you today? Should we start?\", \"sender\": \"bot\", \"timestamp\": \"2024-09-01T12:08:20.262Z\"}, {\"text\": \"Start\", \"sender\": \"user\", \"timestamp\": \"2024-09-01T12:08:20.264Z\"}, {\"text\": \"Start\", \"sender\": \"user\", \"timestamp\": \"2024-09-01T12:08:20.266Z\"}, {\"text\": \"What aspects of your academic life cause you the most stress?\", \"sender\": \"bot\", \"timestamp\": \"2024-09-01T12:08:20.267Z\"}, {\"text\": \"What aspects of your academic life cause you the most stress?\", \"sender\": \"bot\", \"timestamp\": \"2024-09-01T12:08:20.269Z\"}, {\"text\": \"Understanding difficult subjects or topics.\", \"sender\": \"user\", \"timestamp\": \"2024-09-01T12:08:20.270Z\"}, {\"text\": \"Struggling with difficult subjects can cause stress and anxiety. Seeking help or using different study methods can reduce these feelings and improve your mental health.\", \"sender\": \"bot\", \"timestamp\": \"2024-09-01T12:08:20.272Z\"}, {\"text\": \"Hello! Welcome to Piracle, your emotional support companion. How can I assist you today? Should we start?\", \"sender\": \"bot\", \"timestamp\": \"2024-09-01T12:08:20.275Z\"}, {\"text\": \"Hello! Welcome to Piracle, your emotional support companion. How can I assist you today? Should we start?\", \"sender\": \"bot\", \"timestamp\": \"2024-09-01T12:08:20.277Z\"}, {\"text\": \"Start\", \"sender\": \"user\", \"timestamp\": \"2024-09-01T12:08:20.279Z\"}, {\"text\": \"Start\", \"sender\": \"user\", \"timestamp\": \"2024-09-01T12:08:20.281Z\"}, {\"text\": \"What aspects of your academic life cause you the most stress?\", \"sender\": \"bot\", \"timestamp\": \"2024-09-01T12:08:20.283Z\"}, {\"text\": \"What aspects of your academic life cause you the most stress?\", \"sender\": \"bot\", \"timestamp\": \"2024-09-01T12:08:20.286Z\"}, {\"text\": \"Understanding difficult subjects or topics.\", \"sender\": \"user\", \"timestamp\": \"2024-09-01T12:08:20.288Z\"}, {\"text\": \"Struggling with difficult subjects can cause stress and anxiety. Seeking help or using different study methods can reduce these feelings and improve your mental health.\", \"sender\": \"bot\", \"timestamp\": \"2024-09-01T12:08:20.290Z\"}]', '2024-09-01 12:08:21.637379');

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
(5, 'pbkdf2_sha256$720000$zpbMyMPXXT4DBSDDEPLDIg$1B2W+KGytZzv7VbBF54xIVnFUl5vA4EGy9belRZ7bF4=', '2024-09-02 12:31:07.903632', 0, 'KCprsnlcc', '', '', 'kcpersonalacc@gmail.com', 1, 1, '2024-06-28 13:16:02.592036', 'C210077', 'Sulaiman, Khadaffe A.', 'Fourth Year', '+639949953785', 0, NULL, NULL),
(6, 'pbkdf2_sha256$720000$iWiUw10UsuzF0XTbOu6HRN$tLh9lesGv2/k462w0eMhDErpTu3tXjLt0fsAXVoOPZ8=', '2024-08-04 05:25:48.752590', 0, 'Dammang', '', '', 'ashraffdammang14@gmail.com', 0, 1, '2024-06-30 14:33:17.563938', 'C246783', 'Ashraff Dammang', 'Fourth Year', '+639425786145', 0, NULL, NULL),
(10, 'pbkdf2_sha256$720000$FezOJflJ2ZM5D3ee7fiDHt$wfn5SFsd5A3Ru3oLQehipwuP4KxRmLRpRFwicc6WNCo=', '2024-08-07 22:34:14.000999', 0, 'MikeElton', '', '', 'mikemangan23@gmail.com', 0, 1, '2024-06-30 16:08:43.524518', 'C2467832', 'Mike Elton John Mangan', 'Fourth Year', '+639587645921', 0, NULL, NULL),
(11, 'pbkdf2_sha256$720000$HV5k8mValMoQsJVBMoPQ01$dEmHt4rAHvkO5DywXvV45MnqPSUuZvnaSqa42/8kvWA=', '2024-08-04 05:31:23.427378', 0, 'AppleMae', '', '', 'appledinawanao12@gmail.com', 0, 1, '2024-06-30 18:16:51.981618', 'C654347', 'Apple Dinawanao', 'Fourth Year', '+639949953785', 0, NULL, NULL),
(12, 'pbkdf2_sha256$720000$QVSwfuwXWuGm9hB96Fxlw3$sLT8dyrYvRvAktt9/ouL1pLLeKjO+MUythtd20LCzOA=', '2024-08-07 22:37:23.211246', 0, 'YourIdol', '', '', 'youridol12@gmail.com', 0, 1, '2024-06-30 19:30:18.295446', 'C464698', 'Mark Hamill Salahuddin', 'Fourth Year', '+639949953785', 0, NULL, NULL),
(13, 'pbkdf2_sha256$720000$APh5yOIqou1UVeT69iK8TI$ulSBpSpYvrrDRgZ4K0eHioC/HQdm7oI2a2rgGfSboxs=', '2024-08-07 22:36:52.271227', 0, 'Radzkhan', '', '', 'alradzkhan13@gmail.com', 0, 1, '2024-06-30 19:35:34.825660', 'C665736', 'Alradzkhan Hayuddini', 'Fourth Year', '+639949956543', 0, NULL, NULL),
(14, 'pbkdf2_sha256$720000$inmGtKqU6fQdl6I8cy1sYr$VKzrIU5j2o97+NVQIVRdiw1Ev9qcH5A1/7Am6RqyeMs=', '2024-08-17 15:04:20.509436', 0, 'Midorin', '', '', 'midorin2@gmail.com', 0, 1, '2024-06-30 19:39:03.800440', 'C564123', 'Eduard Rolad Donor', 'Fourth Year', '+63923132153', 0, NULL, NULL),
(15, 'pbkdf2_sha256$720000$ncnhTbf8MYawLtOX0UVNeI$zm5HNked5nyy0XnhVVtwKzxrocgcFJwKcItlYJHW+uI=', '2024-08-23 14:59:53.884900', 0, 'bheng', '', '', '', 1, 1, '2024-08-03 23:16:17.085772', '', 'bheng manalo', '', '', 1, NULL, NULL),
(18, 'pbkdf2_sha256$720000$LB9GeqcCcTiz1vAKPVZskN$3OwJX8G1mwe0Ic8T+qPG6LYlccFbIlRFYADUC6Aq5qw=', '2024-08-31 07:05:11.955679', 0, 'TEST', '', '', 'khadaffesulaiman14@gmail.com', 1, 1, '2024-08-19 10:10:34.595022', 'TEST', 'TEST', 'TEST', 'TEST', 1, NULL, NULL),
(19, 'pbkdf2_sha256$720000$oaq7aGJqbao5flnldFsmTl$8Jdy4mEOknO7/NNMd5UhhmZEVSH4nlD52hXDzbtWw8Y=', '2024-08-25 02:40:45.181722', 0, 'ChatTEST', '', '', 'ChatTEST@gmail.com', 0, 1, '2024-08-25 02:40:35.078671', 'ChatTEST', 'ChatTEST', 'ChatTEST', 'ChatTEST', 0, NULL, NULL);

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
-- Table structure for table `main_questionnaire`
--

CREATE TABLE `main_questionnaire` (
  `id` bigint(20) NOT NULL,
  `question` longtext DEFAULT NULL,
  `answer` longtext DEFAULT NULL,
  `response` longtext DEFAULT NULL,
  `timestamp` datetime(6) NOT NULL,
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `main_questionnaire`
--

INSERT INTO `main_questionnaire` (`id`, `question`, `answer`, `response`, `timestamp`, `user_id`) VALUES
(66, 'What aspects of your academic life cause you the most stress?', 'Managing multiple assignments and deadlines.', 'Managing multiple assignments can lead to significant stress, which can impact your mental health. It\'s important to develop strategies to manage this workload to protect your well-being.', '2024-08-25 03:18:28.216677', 5),
(67, 'How would you describe your overall emotional state in the past month?', 'Generally positive, with only occasional low moods.', 'It\'s great to hear that you\'ve been feeling generally positive. Maintaining a positive emotional state is important for good mental health, so keep focusing on what keeps you feeling well.', '2024-08-25 03:18:54.329047', 5);

-- --------------------------------------------------------

--
-- Table structure for table `main_referral`
--

CREATE TABLE `main_referral` (
  `id` bigint(20) NOT NULL,
  `highlighted_title` longtext NOT NULL,
  `highlighted_description` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `referred_by_id` bigint(20) NOT NULL,
  `status_id` bigint(20) NOT NULL,
  `other_reason` longtext DEFAULT NULL,
  `referral_reason` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `main_referral`
--

INSERT INTO `main_referral` (`id`, `highlighted_title`, `highlighted_description`, `created_at`, `referred_by_id`, `status_id`, `other_reason`, `referral_reason`) VALUES
(2, 'Anxiety Over Uncertainty', 'Feeling anxious uncertainty of upcoming projects and personal commitments.', '2024-08-18 15:32:37.703264', 5, 152, '', 'Self-Harm or Suicidal Ideation'),
(3, 'Dealing with Anger', 'Felt a surge of anger today due to a miscommunication at work.', '2024-08-18 15:33:33.069131', 5, 151, 'He is trying to kill someone.', 'Other Concerns'),
(30, '', 'disheartening', '2024-08-23 09:10:14.184834', 5, 150, '45', 'Other Concerns'),
(31, '', 'recent  trying  moving', '2024-08-24 10:55:54.847828', 5, 155, 'Test', 'Other Concerns'),
(32, '', 'overwhelming  hopeful  committed  to our goals.', '2024-09-01 11:08:09.846148', 5, 148, '', 'Inappropriate Language'),
(33, '', 'stay  a', '2024-09-02 11:14:35.733223', 5, 155, '', 'Self-Harm or Suicidal Ideation');

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
(26, 'It\'s tough dealing with anger, especially after a miscommunication at work. It\'s great that you\'re focusing on managing your emotions constructively. Take a moment to breathe and find a positive way to address the issue.', '2024-08-07 22:30:58.710601', 151, 14),
(27, 'Dealing with unpleasant tasks is never easy, but it\'s great that you got through it. Sometimes, these challenges test our resilience and make us stronger. Well done for pushing through!', '2024-08-07 22:31:20.649407', 149, 14),
(29, 'It\'s fantastic to hear about the positive momentum in your translation process! The steady progress and the team\'s dedication are truly inspiring. Keep up the great work!', '2024-08-07 22:31:58.831063', 142, 14),
(30, 'I\'m glad to hear that today was filled with joyful moments for you, both at work and at home. Cherishing these happy times is important and can motivate us to keep pushing forward.', '2024-08-07 22:33:03.208216', 154, 13),
(32, 'I\'m really sorry to hear about the disheartening news regarding your close friend. It\'s challenging to stay motivated when personal life throws such curveballs. Remember to take care of yourself during this tough time, and don\'t hesitate to reach out for support if you need it.', '2024-08-07 22:33:53.844002', 150, 13),
(33, 'I\'m sorry to hear you\'re feeling this way. It\'s okay to struggle with sadness, especially after personal events. Remember to be kind to yourself and take things one step at a time. Stay strong, and reach out for support if you need it.', '2024-08-07 22:34:35.482708', 155, 10),
(34, 'It\'s wonderful to hear that your day was filled with joyful moments both at work and at home. Cherishing these happy times is so important and can really help us keep pushing forward.', '2024-08-07 22:35:03.968824', 154, 10),
(35, 'Despite the numerous challenges, it\'s encouraging to see the steady progress we\'re making. The team\'s determination and resilience are truly commendable. Let\'s keep pushing forward together.', '2024-08-07 22:36:02.913451', 147, 10),
(36, 'It\'s great to see that we\'re making steady progress despite the challenges. The team\'s determination and resilience are truly admirable. Let\'s continue to push forward with the same spirit.', '2024-08-07 22:36:36.054822', 147, 5),
(37, 'Amidst all the challenges, it\'s uplifting to see our steady progress. The determination and resilience of the team are truly commendable. Let\'s keep pushing forward together.', '2024-08-07 22:37:09.691447', 147, 13),
(38, 'Even with the many challenges we face, our progress remains steady. The team\'s resilience and determination are inspiring. Let\'s keep moving forward and overcoming obstacles together.', '2024-08-07 22:37:42.700485', 147, 12),
(39, 'Hi\r\n', '2024-08-19 13:20:30.122581', 150, 5),
(40, 'Are you okay?', '2024-08-19 13:20:39.967234', 150, 5);

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
(145, 'Surprise', 'Unexpected Breakthrough', '<div bis_skin_checked=\"1\">We experienced an unexpected breakthrough in our translation process, significantly improving efficiency. This development has boosted team morale and accelerated our timeline.</div>', 'We experienced an unexpected breakthrough in our translation process, significantly improving efficiency. This development has boosted team morale and accelerated our timeline.', '2024-08-04 05:30:29.026318', 5, 0.008794465102255344, 0.0035787622909992933, 0.00664545688778162, 0.6093906760215759, 0.0038843981456011534, 0.12407993525266647, 0.24362628161907196, 0, 0, 0, 60, 24, 0, 12),
(147, 'Happiness', 'Progress Amidst Challenges', '<div bis_skin_checked=\"1\">Despite the numerous challenges, we are making steady progress. The team\'s determination and resilience are commendable. We will continue to push forward.</div><div bis_skin_checked=\"1\"><br></div>', 'Despite the numerous challenges, we are making steady progress. The team\'s determination and resilience are commendable. We will continue to push forward.', '2024-08-04 05:31:39.672243', 11, 0.009493770077824593, 0.005666713695973158, 0.008420553989708424, 0.460519015789032, 0.006693973671644926, 0.009713422507047653, 0.4994925558567047, 0, 0, 0, 46, 49, 0, 0),
(148, 'Fear', 'Overwhelmed but Hopeful', '<div bis_skin_checked=\"1\">The complexity of the translation process has been overwhelming at times, but we remain hopeful and committed to our goals. The team\'s resilience is commendable.</div>', 'The complexity of the translation process has been overwhelming at times, but we remain hopeful and committed to our goals. The team\'s resilience is commendable.', '2024-08-04 05:32:02.172720', 11, 0.004258217290043831, 0.004370026756078005, 0.018206728622317314, 0.6743161082267761, 0.004406822379678488, 0.014697698876261711, 0.27974432706832886, 0, 0, 1, 67, 27, 0, 1),
(149, 'Disgust', 'Overcoming Disgust', '<div bis_skin_checked=\"1\">Had to deal with a particularly unpleasant task today. It was revolting, but necessary. Sometimes, life throws these challenges at us to test our resilience.</div>', 'Had to deal with a particularly unpleasant task today. It was revolting, but necessary. Sometimes, life throws these challenges at us to test our resilience.', '2024-08-04 05:33:02.647728', 10, 0.03187451511621475, 0.4441128969192505, 0.3892916142940521, 0.004690230358392, 0.0819910317659378, 0.004854700993746519, 0.043185003101825714, 3, 44, 38, 0, 4, 8, 0),
(150, 'Sadness', 'Disheartening News', 'Received some disheartening news about a close friend. It\'s hard to stay motivated when personal life throws such curveballs.', 'Received some disheartening news about a close friend. It\'s hard to stay motivated when personal life throws such curveballs.', '2024-08-04 05:34:09.778661', 12, 0.005729991476982832, 0.03910326585173607, 0.0029186869505792856, 0.0019326204201206565, 0.9378151893615723, 0.005862448830157518, 0.006637743208557367, 0, 3, 0, 0, 0, 93, 0),
(151, 'Anger', 'Dealing with Anger', '<div bis_skin_checked=\"1\">Felt a surge of anger today due to a miscommunication at work. It\'s important to manage these emotions constructively, even when it\'s tough.</div>', 'Felt a surge of anger today due to a miscommunication at work. It\'s important to manage these emotions constructively, even when it\'s tough.', '2024-08-04 05:34:30.785649', 12, 0.9573907256126404, 0.014166107401251793, 0.004705321975052357, 0.0007844159263186157, 0.005818953271955252, 0.0009728842414915562, 0.016161533072590828, 95, 1, 0, 0, 1, 0, 0),
(152, 'Fear', 'Anxiety Over Uncertainty', '<div bis_skin_checked=\"1\">Feeling anxious about the uncertainty of upcoming projects and personal commitments. The fear of the unknown is a constant challenge.</div>', 'Feeling anxious about the uncertainty of upcoming projects and personal commitments. The fear of the unknown is a constant challenge.', '2024-08-04 05:36:10.989464', 13, 0.001026142854243517, 0.0008091017953120172, 0.9905966520309448, 0.0013121414231136441, 0.0020971756894141436, 0.0012878328561782837, 0.002870921976864338, 0, 0, 99, 0, 0, 0, 0),
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
(17, '', 15),
(20, 'avatars/avatar_NZsiVzE.png', 18),
(21, '', 19);

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
-- Indexes for table `main_chatsession`
--
ALTER TABLE `main_chatsession`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `main_chatsession_user_id_0269915b_uniq` (`user_id`);

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
-- Indexes for table `main_questionnaire`
--
ALTER TABLE `main_questionnaire`
  ADD PRIMARY KEY (`id`),
  ADD KEY `main_questionnaire_user_id_e1ba18de_fk_main_customuser_id` (`user_id`);

--
-- Indexes for table `main_referral`
--
ALTER TABLE `main_referral`
  ADD PRIMARY KEY (`id`),
  ADD KEY `main_referral_referred_by_id_5b21704f_fk_main_customuser_id` (`referred_by_id`),
  ADD KEY `main_referral_status_id_04bc8b41_fk_main_status_id` (`status_id`);

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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=61;

--
-- AUTO_INCREMENT for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=64;

--
-- AUTO_INCREMENT for table `main_chatsession`
--
ALTER TABLE `main_chatsession`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=79;

--
-- AUTO_INCREMENT for table `main_contactus`
--
ALTER TABLE `main_contactus`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `main_customuser`
--
ALTER TABLE `main_customuser`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

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
-- AUTO_INCREMENT for table `main_questionnaire`
--
ALTER TABLE `main_questionnaire`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=68;

--
-- AUTO_INCREMENT for table `main_referral`
--
ALTER TABLE `main_referral`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=34;

--
-- AUTO_INCREMENT for table `main_reply`
--
ALTER TABLE `main_reply`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=41;

--
-- AUTO_INCREMENT for table `main_status`
--
ALTER TABLE `main_status`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=196;

--
-- AUTO_INCREMENT for table `main_userprofile`
--
ALTER TABLE `main_userprofile`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

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
-- Constraints for table `main_chatsession`
--
ALTER TABLE `main_chatsession`
  ADD CONSTRAINT `main_chatsession_user_id_0269915b_fk_main_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `main_customuser` (`id`);

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
-- Constraints for table `main_questionnaire`
--
ALTER TABLE `main_questionnaire`
  ADD CONSTRAINT `main_questionnaire_user_id_e1ba18de_fk_main_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `main_customuser` (`id`);

--
-- Constraints for table `main_referral`
--
ALTER TABLE `main_referral`
  ADD CONSTRAINT `main_referral_referred_by_id_5b21704f_fk_main_customuser_id` FOREIGN KEY (`referred_by_id`) REFERENCES `main_customuser` (`id`),
  ADD CONSTRAINT `main_referral_status_id_04bc8b41_fk_main_status_id` FOREIGN KEY (`status_id`) REFERENCES `main_status` (`id`);

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
