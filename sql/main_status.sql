-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 01, 2025 at 05:37 AM
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
(155, 'Sadness', 'Emotional Struggles', 'Struggling with sadness due to recent personal events. It\'s been a tough day, but I\'m trying to stay strong and keep moving forward.', 'Struggling with sadness due to recent personal events. It\'s been a tough day, but I\'m trying to stay strong and keep moving forward.', '2024-08-04 05:38:42.748136', 13, 0.001055471831932664, 0.002059370744973421, 0.003661424620077014, 0.00246447348035872, 0.9811586141586304, 0.0013769293436780572, 0.00822375901043415, 0, 0, 0, 0, 0, 98, 0),
(200, 'Sadness', 'Fading Memorie', 'The moments we once cherished together now feel like distant echoes, fading into the abyss of time. It’s as though each passing day takes a piece of our shared joy, leaving behind only a hollow reminder of what once was. The laughter, the warmth now just a painful memory, lost in the emptiness of longing.', 'The moments we once cherished together now feel like distant echoes, fading into the abyss of time. It’s as though each passing day takes a piece of our shared joy, leaving behind only a hollow reminder of what once was. The laughter, the warmth now just a painful memory, lost in the emptiness of longing.', '2024-10-15 08:53:08.102768', 5, 0.0014825446996837854, 0.012032457627356052, 0.003964613191783428, 0.0037531477864831686, 0.927561342716217, 0.0026272947434335947, 0.04857858642935753, 0, 1, 0, 0, 4, 92, 0),
(211, 'Fear', 'sad', 'im confused with my feelings but i chose fear emoji because i am confused which to pick', 'im confused with my feelings but i chose fear emoji because i am confused which to pick', '2024-11-16 06:38:26.377536', 10, 0.0021085883490741253, 0.00021492365340236574, 0.9872860312461853, 0.0010270755738019943, 0.006163183134049177, 0.0027180223260074854, 0.00048222640180028975, 0, 0, 98, 0, 0, 0, 0),
(213, 'Sadness', 'I\'m Angry', 'I\'m Angry because I don\'t have any money to pay the bill.', 'I\'m Angry because I don\'t have any money to pay the bill.', '2024-11-17 05:30:08.707603', 5, 0.9894320964813232, 0.0019208051962777972, 0.0023795831948518753, 0.0004604501591529697, 0.001580744399689138, 0.0016871285624802113, 0.0025391019880771637, 98, 0, 0, 0, 0, 0, 0),
(215, 'Sadness', 'Angry', 'Angry', 'Angry', '2024-11-17 06:27:59.233346', 11, 0.9918437600135803, 0.0024604022037237883, 0.0006542741903103888, 0.0004511014267336577, 0.0016503847436979413, 0.000988196348771453, 0.0019518932094797492, 99, 0, 0, 0, 0, 0, 0),
(218, 'Happiness', 'im happy', 'just happy', 'just happy', '2024-11-18 03:40:03.493741', 69, 0.0050891367718577385, 0.0006566394586116076, 0.0005550216301344335, 0.6822232604026794, 0.042881835252046585, 0.22348004579544067, 0.04511396959424019, 0, 0, 0, 68, 4, 4, 22),
(219, 'Happiness', 'cutie', 'I\'m too cute', 'I\'m too cute', '2024-11-18 03:40:30.813490', 70, 0.007172546349465847, 0.008029765449464321, 0.003907295875251293, 0.6510660648345947, 0.07284460216760635, 0.10966619849205017, 0.14731355011463165, 0, 0, 0, 65, 14, 7, 10),
(220, 'Happiness', 'happy', 'aaaa', 'aaaa', '2024-11-18 04:03:43.917213', 71, 0.1580021232366562, 0.10301444679498672, 0.2699372470378876, 0.030775513499975204, 0.13040192425251007, 0.038538698107004166, 0.26933008432388306, 15, 10, 26, 3, 26, 13, 3),
(221, 'Sadness', 'Sad', 'stress', 'stress', '2024-11-18 06:41:40.219372', 80, 0.11930106580257416, 0.026837484911084175, 0.09072834253311157, 0.005321484990417957, 0.4610694348812103, 0.03821154311299324, 0.2585305869579315, 11, 2, 9, 0, 25, 46, 3),
(222, 'Sadness', 'I\'m sad', 'I lost my 1pesos yesterday', 'I lost my 1pesos yesterday', '2024-11-18 08:02:09.047670', 81, 0.0021625689696520567, 0.0016873294953256845, 0.0024033794179558754, 0.00227983552031219, 0.9595698118209839, 0.013609703630208969, 0.018287312239408493, 0, 0, 0, 0, 1, 95, 1),
(223, 'Happiness', 'reply here', 'replt', 'replt', '2024-11-19 12:48:36.038210', 5, 0.011179379187524319, 0.010824601165950298, 0.005110676400363445, 0.01093321479856968, 0.02827252447605133, 0.05500300973653793, 0.8786766529083252, 1, 1, 0, 1, 87, 2, 5),
(224, 'Happiness', 'asdasd', 'asdasd', 'asdasd', '2024-11-19 13:27:49.196185', 11, 0.008592569269239902, 0.0045346785336732864, 0.00476930383592844, 0.012101100757718086, 0.04793223738670349, 0.11659235507249832, 0.8054777979850769, 0, 0, 0, 1, 80, 4, 11),
(225, 'Sadness', 'sad', 'i\'m very sad i want to die', 'i\'m very sad i want to die', '2024-11-19 13:44:21.545295', 11, 0.0008205142221413553, 0.00033517961855977774, 0.0006839395500719547, 0.00278854975476861, 0.9917407035827637, 0.002529394580051303, 0.0011017464566975832, 0, 0, 0, 0, 0, 99, 0),
(226, 'Sadness', 'test', 'im very sad i want to jump out of the building', 'im very sad i want to jump out of the building', '2024-11-19 13:47:51.755835', 11, 0.0011268354719504714, 0.00028749051853083074, 0.0013716606190428138, 0.004660685546696186, 0.9856387972831726, 0.005826395470649004, 0.0010882363421842456, 0, 0, 0, 0, 0, 98, 0),
(227, 'Happiness', 'test', 'test', 'test', '2024-11-19 15:35:21.573697', 11, 0.09827201068401337, 0.06734087318181992, 0.06715127825737, 0.014987325295805931, 0.019343804568052292, 0.04400065913796425, 0.6889040470123291, 9, 6, 6, 1, 68, 1, 4),
(230, 'Happiness', 'test', '😹', '😹', '2024-11-19 18:26:30.088582', 5, 0.0032288243528455496, 0.0007504774839617312, 0.0005325946840457618, 0.8801724910736084, 0.041294507682323456, 0.0365544855594635, 0.03746666759252548, 0, 0, 0, 88, 3, 4, 3),
(236, 'Happiness', 'test', '🤣', '🤣', '2024-11-19 18:35:06.635429', 5, 0.009180816821753979, 0.020987574011087418, 0.0013114435132592916, 0.5893054604530334, 0.012593313120305538, 0.0322999507188797, 0.3343215584754944, 0, 2, 0, 58, 33, 1, 3);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `main_status`
--
ALTER TABLE `main_status`
  ADD PRIMARY KEY (`id`),
  ADD KEY `main_status_user_id_9e18e9fa_fk_main_customuser_id` (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `main_status`
--
ALTER TABLE `main_status`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=237;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
