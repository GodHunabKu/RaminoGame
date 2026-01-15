/*
 Navicat Premium Data Transfer

 Source Server         : Metin2Hunter2025
 Source Server Type    : MySQL
 Source Server Version : 101111 (10.11.11-MariaDB)
 Source Host           : 81.180.203.146:3306
 Source Schema         : srv1_hunabku

 Target Server Type    : MySQL
 Target Server Version : 101111 (10.11.11-MariaDB)
 File Encoding         : 65001

 Date: 06/01/2026 15:20:20
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for hunter_achievements_claimed
-- ----------------------------
DROP TABLE IF EXISTS `hunter_achievements_claimed`;
CREATE TABLE `hunter_achievements_claimed`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `player_id` int NOT NULL,
  `achievement_id` int NOT NULL,
  `claimed_at` datetime NOT NULL DEFAULT current_timestamp,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `idx_player_achievement`(`player_id` ASC, `achievement_id` ASC) USING BTREE,
  INDEX `idx_player`(`player_id` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of hunter_achievements_claimed
-- ----------------------------

-- ----------------------------
-- Table structure for hunter_chest_loot
-- ----------------------------
DROP TABLE IF EXISTS `hunter_chest_loot`;
CREATE TABLE `hunter_chest_loot`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `chest_vnum` int NOT NULL COMMENT 'VNUM baule (63000-63007) o 0=tutti',
  `min_rank_tier` int NOT NULL DEFAULT 1 COMMENT 'Rank minimo baule (1=E, 7=N)',
  `loot_type` enum('GLORY','ITEM') CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL DEFAULT 'ITEM',
  `item_vnum` int NULL DEFAULT 0 COMMENT 'VNUM item (se ITEM)',
  `item_quantity` int NULL DEFAULT 1,
  `glory_min` int NULL DEFAULT 0 COMMENT 'Gloria minima (se GLORY)',
  `glory_max` int NULL DEFAULT 0 COMMENT 'Gloria massima (se GLORY)',
  `drop_chance` int NOT NULL DEFAULT 5 COMMENT '% probabilita (1-100)',
  `name` varchar(50) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT 'Jackpot',
  `is_jackpot` tinyint(1) NULL DEFAULT 1 COMMENT '1=mostra effetto jackpot',
  `enabled` tinyint(1) NULL DEFAULT 1,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_chest_vnum`(`chest_vnum` ASC) USING BTREE,
  INDEX `idx_rank_tier`(`min_rank_tier` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 17 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of hunter_chest_loot
-- ----------------------------
INSERT INTO `hunter_chest_loot` VALUES (1, 0, 1, 'GLORY', 0, 0, 50, 150, 15, 'Jackpot Gloria Minore', 1, 1);
INSERT INTO `hunter_chest_loot` VALUES (2, 0, 3, 'GLORY', 0, 0, 100, 300, 10, 'Jackpot Gloria', 1, 1);
INSERT INTO `hunter_chest_loot` VALUES (3, 0, 5, 'GLORY', 0, 0, 200, 500, 8, 'Jackpot Gloria Maggiore', 1, 1);
INSERT INTO `hunter_chest_loot` VALUES (4, 0, 7, 'GLORY', 0, 0, 400, 1000, 5, 'MEGA JACKPOT GLORIA', 1, 1);
INSERT INTO `hunter_chest_loot` VALUES (5, 0, 2, 'ITEM', 50160, 1, 0, 0, 8, 'Scanner di Fratture', 1, 1);
INSERT INTO `hunter_chest_loot` VALUES (6, 0, 3, 'ITEM', 50162, 1, 0, 0, 6, 'Focus del Cacciatore', 1, 1);
INSERT INTO `hunter_chest_loot` VALUES (7, 0, 4, 'ITEM', 50163, 1, 0, 0, 4, 'Chiave Dimensionale', 1, 1);
INSERT INTO `hunter_chest_loot` VALUES (8, 0, 4, 'ITEM', 50167, 1, 0, 0, 5, 'Calibratore', 1, 1);
INSERT INTO `hunter_chest_loot` VALUES (9, 0, 5, 'ITEM', 50161, 1, 0, 0, 3, 'Stabilizzatore di Rango', 1, 1);
INSERT INTO `hunter_chest_loot` VALUES (10, 0, 5, 'ITEM', 50165, 1, 0, 0, 4, 'Segnale Emergenza', 1, 1);
INSERT INTO `hunter_chest_loot` VALUES (11, 0, 6, 'ITEM', 50164, 1, 0, 0, 2, 'Sigillo di Conquista', 1, 1);
INSERT INTO `hunter_chest_loot` VALUES (12, 0, 6, 'ITEM', 50166, 1, 0, 0, 2, 'Risonatore di Gruppo', 1, 1);
INSERT INTO `hunter_chest_loot` VALUES (13, 63006, 7, 'ITEM', 50168, 1, 0, 0, 1, 'Frammento di Monarca', 1, 1);
INSERT INTO `hunter_chest_loot` VALUES (14, 0, 1, 'ITEM', 80030, 2, 0, 0, 20, 'Buono 100 Gloria x2', 0, 1);
INSERT INTO `hunter_chest_loot` VALUES (15, 0, 3, 'ITEM', 80031, 1, 0, 0, 12, 'Buono 500 Gloria', 0, 1);
INSERT INTO `hunter_chest_loot` VALUES (16, 0, 5, 'ITEM', 80032, 1, 0, 0, 8, 'Buono 1000 Gloria', 1, 1);

-- ----------------------------
-- Table structure for hunter_chest_rewards
-- ----------------------------
DROP TABLE IF EXISTS `hunter_chest_rewards`;
CREATE TABLE `hunter_chest_rewards`  (
  `vnum` int NOT NULL COMMENT 'VNUM del baule (63000-63007)',
  `name` varchar(50) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL DEFAULT 'Baule',
  `rank_tier` int NOT NULL DEFAULT 1 COMMENT '1=E, 2=D, 3=C, 4=B, 5=A, 6=S, 7=N',
  `glory_min` int NOT NULL DEFAULT 20 COMMENT 'Gloria minima',
  `glory_max` int NOT NULL DEFAULT 50 COMMENT 'Gloria massima',
  `item_vnum` int NULL DEFAULT 0 COMMENT 'Item bonus (0=nessuno)',
  `item_quantity` int NULL DEFAULT 1,
  `item_chance` int NULL DEFAULT 0 COMMENT '% probabilita item (0-100)',
  `color_code` varchar(16) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT 'GREEN',
  `enabled` tinyint(1) NULL DEFAULT 1,
  PRIMARY KEY (`vnum`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of hunter_chest_rewards
-- ----------------------------
INSERT INTO `hunter_chest_rewards` VALUES (63000, 'Cassa E-Rank', 1, 30, 60, 80030, 1, 30, 'GREEN', 1);
INSERT INTO `hunter_chest_rewards` VALUES (63001, 'Cassa D-Rank', 2, 50, 100, 80030, 2, 25, 'BLUE', 1);
INSERT INTO `hunter_chest_rewards` VALUES (63002, 'Cassa C-Rank', 3, 80, 150, 80031, 1, 20, 'ORANGE', 1);
INSERT INTO `hunter_chest_rewards` VALUES (63003, 'Cassa B-Rank', 4, 120, 220, 80031, 2, 15, 'RED', 1);
INSERT INTO `hunter_chest_rewards` VALUES (63004, 'Cassa A-Rank', 5, 170, 300, 80032, 1, 12, 'PURPLE', 1);
INSERT INTO `hunter_chest_rewards` VALUES (63005, 'Cassa S-Rank', 6, 240, 420, 80032, 2, 10, 'GOLD', 1);
INSERT INTO `hunter_chest_rewards` VALUES (63006, 'Cassa N-Rank', 7, 350, 600, 80040, 1, 8, 'BLACKWHITE', 1);
INSERT INTO `hunter_chest_rewards` VALUES (63007, 'Cassa ???-Rank', 1, 200, 800, 80040, 1, 50, 'PURPLE', 1);

-- ----------------------------
-- Table structure for hunter_event_participants
-- ----------------------------
DROP TABLE IF EXISTS `hunter_event_participants`;
CREATE TABLE `hunter_event_participants`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `event_id` int NOT NULL,
  `player_id` int NOT NULL,
  `player_name` varchar(50) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `joined_at` datetime NOT NULL DEFAULT current_timestamp,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_event_player`(`event_id` ASC, `player_id` ASC) USING BTREE,
  INDEX `idx_joined_at`(`joined_at` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of hunter_event_participants
-- ----------------------------
INSERT INTO `hunter_event_participants` VALUES (1, 12, 4, '[GF]HunabKu', '2026-01-04 15:07:24');
INSERT INTO `hunter_event_participants` VALUES (2, 13, 1684, 'Pacifista', '2026-01-04 15:48:11');
INSERT INTO `hunter_event_participants` VALUES (3, 27, 4, '[GF]HunabKu', '2026-01-04 18:10:51');

-- ----------------------------
-- Table structure for hunter_event_winners
-- ----------------------------
DROP TABLE IF EXISTS `hunter_event_winners`;
CREATE TABLE `hunter_event_winners`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `event_id` int NOT NULL,
  `player_id` int NOT NULL,
  `player_name` varchar(50) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `winner_type` varchar(20) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `winner_data` text CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL,
  `won_at` datetime NOT NULL DEFAULT current_timestamp,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_event_won`(`event_id` ASC, `won_at` ASC) USING BTREE,
  INDEX `idx_player`(`player_id` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of hunter_event_winners
-- ----------------------------
INSERT INTO `hunter_event_winners` VALUES (1, 12, 4, '[GF]HunabKu', 'first_rift', '900', '2026-01-04 15:07:24');
INSERT INTO `hunter_event_winners` VALUES (2, 27, 4, '[GF]HunabKu', 'first_rift', '2500', '2026-01-04 18:10:51');

-- ----------------------------
-- Table structure for hunter_fracture_defense_config
-- ----------------------------
DROP TABLE IF EXISTS `hunter_fracture_defense_config`;
CREATE TABLE `hunter_fracture_defense_config`  (
  `config_key` varchar(64) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `config_value` int NOT NULL,
  `description` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL,
  PRIMARY KEY (`config_key`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of hunter_fracture_defense_config
-- ----------------------------
INSERT INTO `hunter_fracture_defense_config` VALUES ('check_distance', 20, 'Distanza massima dalla frattura (metri)');
INSERT INTO `hunter_fracture_defense_config` VALUES ('check_interval', 2, 'Ogni quanti secondi controllare la posizione');
INSERT INTO `hunter_fracture_defense_config` VALUES ('defense_duration', 60, 'Durata difesa in secondi (fallback generico)');
INSERT INTO `hunter_fracture_defense_config` VALUES ('defense_duration_A', 120, 'Durata difesa A-Rank (2 min)');
INSERT INTO `hunter_fracture_defense_config` VALUES ('defense_duration_B', 90, 'Durata difesa B-Rank (1.5 min)');
INSERT INTO `hunter_fracture_defense_config` VALUES ('defense_duration_C', 60, 'Durata difesa C-Rank (1 min)');
INSERT INTO `hunter_fracture_defense_config` VALUES ('defense_duration_D', 60, 'Durata difesa D-Rank (1 min)');
INSERT INTO `hunter_fracture_defense_config` VALUES ('defense_duration_E', 60, 'Durata difesa E-Rank (1 min)');
INSERT INTO `hunter_fracture_defense_config` VALUES ('defense_duration_N', 180, 'Durata difesa N-Rank (3 min)');
INSERT INTO `hunter_fracture_defense_config` VALUES ('defense_duration_S', 150, 'Durata difesa S-Rank (2.5 min)');
INSERT INTO `hunter_fracture_defense_config` VALUES ('party_all_required', 1, 'Se 1, tutti i membri party devono stare vicini');
INSERT INTO `hunter_fracture_defense_config` VALUES ('spawn_start_delay', 5, 'Secondi prima della prima ondata');

-- ----------------------------
-- Table structure for hunter_fracture_defense_waves
-- ----------------------------
DROP TABLE IF EXISTS `hunter_fracture_defense_waves`;
CREATE TABLE `hunter_fracture_defense_waves`  (
  `wave_id` int NOT NULL AUTO_INCREMENT,
  `rank_grade` varchar(2) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL COMMENT 'E,D,C,B,A,S,N',
  `wave_number` int NOT NULL DEFAULT 1,
  `spawn_time` int NOT NULL DEFAULT 10,
  `mob_vnum` int NOT NULL,
  `mob_count` int NOT NULL DEFAULT 5,
  `spawn_radius` int NOT NULL DEFAULT 7,
  `enabled` tinyint(1) NOT NULL DEFAULT 1,
  PRIMARY KEY (`wave_id`) USING BTREE,
  INDEX `idx_rank_wave`(`rank_grade` ASC, `wave_number` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 56 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of hunter_fracture_defense_waves
-- ----------------------------
INSERT INTO `hunter_fracture_defense_waves` VALUES (1, 'E', 1, 5, 7125, 2, 6, 1);
INSERT INTO `hunter_fracture_defense_waves` VALUES (2, 'E', 2, 25, 7129, 2, 6, 1);
INSERT INTO `hunter_fracture_defense_waves` VALUES (3, 'E', 3, 45, 7133, 2, 6, 1);
INSERT INTO `hunter_fracture_defense_waves` VALUES (4, 'D', 1, 5, 7127, 2, 7, 1);
INSERT INTO `hunter_fracture_defense_waves` VALUES (5, 'D', 2, 20, 7131, 2, 7, 1);
INSERT INTO `hunter_fracture_defense_waves` VALUES (6, 'D', 3, 35, 7135, 2, 7, 1);
INSERT INTO `hunter_fracture_defense_waves` VALUES (7, 'D', 4, 45, 7137, 2, 7, 1);
INSERT INTO `hunter_fracture_defense_waves` VALUES (8, 'C', 1, 5, 7126, 2, 7, 1);
INSERT INTO `hunter_fracture_defense_waves` VALUES (9, 'C', 2, 18, 7130, 2, 7, 1);
INSERT INTO `hunter_fracture_defense_waves` VALUES (10, 'C', 3, 30, 7134, 2, 7, 1);
INSERT INTO `hunter_fracture_defense_waves` VALUES (11, 'C', 4, 45, 7140, 2, 7, 1);
INSERT INTO `hunter_fracture_defense_waves` VALUES (12, 'B', 1, 5, 7128, 2, 8, 1);
INSERT INTO `hunter_fracture_defense_waves` VALUES (13, 'B', 2, 18, 7132, 2, 8, 1);
INSERT INTO `hunter_fracture_defense_waves` VALUES (14, 'B', 3, 32, 7136, 2, 8, 1);
INSERT INTO `hunter_fracture_defense_waves` VALUES (15, 'B', 4, 46, 7138, 2, 8, 1);
INSERT INTO `hunter_fracture_defense_waves` VALUES (16, 'B', 5, 60, 7128, 2, 8, 1);
INSERT INTO `hunter_fracture_defense_waves` VALUES (17, 'B', 6, 75, 7136, 2, 8, 1);
INSERT INTO `hunter_fracture_defense_waves` VALUES (18, 'A', 1, 5, 7126, 2, 8, 1);
INSERT INTO `hunter_fracture_defense_waves` VALUES (19, 'A', 2, 17, 7128, 2, 8, 1);
INSERT INTO `hunter_fracture_defense_waves` VALUES (20, 'A', 3, 30, 7130, 2, 8, 1);
INSERT INTO `hunter_fracture_defense_waves` VALUES (21, 'A', 4, 43, 7132, 2, 8, 1);
INSERT INTO `hunter_fracture_defense_waves` VALUES (22, 'A', 5, 56, 7134, 2, 8, 1);
INSERT INTO `hunter_fracture_defense_waves` VALUES (23, 'A', 6, 69, 7136, 2, 8, 1);
INSERT INTO `hunter_fracture_defense_waves` VALUES (24, 'A', 7, 82, 7140, 2, 8, 1);
INSERT INTO `hunter_fracture_defense_waves` VALUES (25, 'A', 8, 95, 7140, 2, 8, 1);
INSERT INTO `hunter_fracture_defense_waves` VALUES (26, 'A', 9, 105, 7141, 2, 8, 1);
INSERT INTO `hunter_fracture_defense_waves` VALUES (27, 'S', 1, 5, 7141, 2, 8, 1);
INSERT INTO `hunter_fracture_defense_waves` VALUES (28, 'S', 2, 17, 7126, 2, 8, 1);
INSERT INTO `hunter_fracture_defense_waves` VALUES (29, 'S', 3, 29, 7142, 2, 8, 1);
INSERT INTO `hunter_fracture_defense_waves` VALUES (30, 'S', 4, 41, 7130, 2, 8, 1);
INSERT INTO `hunter_fracture_defense_waves` VALUES (31, 'S', 5, 53, 7143, 2, 8, 1);
INSERT INTO `hunter_fracture_defense_waves` VALUES (32, 'S', 6, 65, 7134, 2, 8, 1);
INSERT INTO `hunter_fracture_defense_waves` VALUES (33, 'S', 7, 77, 7144, 2, 8, 1);
INSERT INTO `hunter_fracture_defense_waves` VALUES (34, 'S', 8, 89, 7141, 2, 8, 1);
INSERT INTO `hunter_fracture_defense_waves` VALUES (35, 'S', 9, 101, 7142, 2, 8, 1);
INSERT INTO `hunter_fracture_defense_waves` VALUES (36, 'S', 10, 113, 7143, 2, 8, 1);
INSERT INTO `hunter_fracture_defense_waves` VALUES (37, 'S', 11, 125, 7144, 2, 8, 1);
INSERT INTO `hunter_fracture_defense_waves` VALUES (38, 'S', 12, 135, 7141, 2, 8, 1);
INSERT INTO `hunter_fracture_defense_waves` VALUES (39, 'N', 1, 5, 7141, 2, 8, 1);
INSERT INTO `hunter_fracture_defense_waves` VALUES (40, 'N', 2, 17, 7142, 2, 8, 1);
INSERT INTO `hunter_fracture_defense_waves` VALUES (41, 'N', 3, 29, 7143, 2, 8, 1);
INSERT INTO `hunter_fracture_defense_waves` VALUES (42, 'N', 4, 41, 7144, 2, 8, 1);
INSERT INTO `hunter_fracture_defense_waves` VALUES (43, 'N', 5, 53, 7141, 2, 8, 1);
INSERT INTO `hunter_fracture_defense_waves` VALUES (44, 'N', 6, 65, 7142, 2, 8, 1);
INSERT INTO `hunter_fracture_defense_waves` VALUES (45, 'N', 7, 77, 7143, 2, 8, 1);
INSERT INTO `hunter_fracture_defense_waves` VALUES (46, 'N', 8, 89, 7144, 2, 8, 1);
INSERT INTO `hunter_fracture_defense_waves` VALUES (47, 'N', 9, 101, 7141, 2, 8, 1);
INSERT INTO `hunter_fracture_defense_waves` VALUES (48, 'N', 10, 113, 7142, 2, 8, 1);
INSERT INTO `hunter_fracture_defense_waves` VALUES (49, 'N', 11, 125, 7143, 2, 8, 1);
INSERT INTO `hunter_fracture_defense_waves` VALUES (50, 'N', 12, 137, 7144, 2, 8, 1);
INSERT INTO `hunter_fracture_defense_waves` VALUES (51, 'N', 13, 149, 7141, 2, 8, 1);
INSERT INTO `hunter_fracture_defense_waves` VALUES (52, 'N', 14, 161, 7142, 2, 8, 1);
INSERT INTO `hunter_fracture_defense_waves` VALUES (53, 'N', 15, 165, 7143, 2, 8, 1);

-- ----------------------------
-- Table structure for hunter_gate_access
-- ----------------------------
DROP TABLE IF EXISTS `hunter_gate_access`;
CREATE TABLE `hunter_gate_access`  (
  `access_id` int NOT NULL AUTO_INCREMENT,
  `player_id` int NOT NULL,
  `player_name` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `gate_id` int NOT NULL,
  `granted_at` timestamp NULL DEFAULT current_timestamp,
  `expires_at` timestamp NOT NULL COMMENT 'Quando scade il permesso (2 ore)',
  `status` enum('pending','entered','completed','failed','expired') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT 'pending',
  `entered_at` timestamp NULL DEFAULT NULL,
  `completed_at` timestamp NULL DEFAULT NULL,
  `gloria_earned` int NULL DEFAULT 0,
  PRIMARY KEY (`access_id`) USING BTREE,
  INDEX `gate_id`(`gate_id` ASC) USING BTREE,
  INDEX `idx_player_status`(`player_id` ASC, `status` ASC) USING BTREE,
  INDEX `idx_expires`(`expires_at` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 15 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of hunter_gate_access
-- ----------------------------
INSERT INTO `hunter_gate_access` VALUES (13, 4, '[GF]HunabKu', 1, '2025-12-29 21:49:27', '2025-12-29 23:49:27', 'pending', NULL, NULL, 0);
INSERT INTO `hunter_gate_access` VALUES (14, 4, '[GF]HunabKu', 1, '2025-12-31 19:12:37', '2025-12-31 21:12:37', 'pending', NULL, NULL, 0);

-- ----------------------------
-- Table structure for hunter_gate_config
-- ----------------------------
DROP TABLE IF EXISTS `hunter_gate_config`;
CREATE TABLE `hunter_gate_config`  (
  `gate_id` int NOT NULL AUTO_INCREMENT,
  `gate_name` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `gate_grade` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'E,D,C,B,A,S,N',
  `min_rank` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'E',
  `min_level` int NOT NULL DEFAULT 1,
  `dungeon_index` int NOT NULL COMMENT 'Index del dungeon Metin2',
  `boss_vnum` int NOT NULL DEFAULT 0 COMMENT 'VNUM del boss da uccidere (0 = nessun boss specifico)',
  `duration_minutes` int NOT NULL DEFAULT 30 COMMENT 'Tempo per completare',
  `cooldown_hours` int NOT NULL DEFAULT 24 COMMENT 'Cooldown personale',
  `gloria_reward` int NOT NULL DEFAULT 500,
  `gloria_penalty` int NOT NULL DEFAULT 250 COMMENT 'Se fallisci o scade timer',
  `max_daily_entries` int NOT NULL DEFAULT 1,
  `color_code` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'BLUE',
  `enabled` tinyint(1) NOT NULL DEFAULT 1,
  `created_at` timestamp NULL DEFAULT current_timestamp,
  PRIMARY KEY (`gate_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 8 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of hunter_gate_config
-- ----------------------------
INSERT INTO `hunter_gate_config` VALUES (1, 'Gate Primordiale', 'E', 'E', 30, 1, 4035, 30, 24, 300, 150, 1, 'GREEN', 1, '2025-12-27 02:42:41');
INSERT INTO `hunter_gate_config` VALUES (2, 'Gate Astrale', 'D', 'D', 50, 2, 6790, 25, 24, 500, 250, 1, 'BLUE', 1, '2025-12-27 02:42:41');
INSERT INTO `hunter_gate_config` VALUES (3, 'Gate Abissale', 'C', 'C', 70, 3, 6831, 25, 24, 800, 400, 1, 'ORANGE', 1, '2025-12-27 02:42:41');
INSERT INTO `hunter_gate_config` VALUES (4, 'Gate Cremisi', 'B', 'B', 85, 4, 986, 20, 24, 1200, 600, 1, 'RED', 1, '2025-12-27 02:42:41');
INSERT INTO `hunter_gate_config` VALUES (5, 'Gate Aureo', 'A', 'A', 100, 5, 989, 20, 24, 2000, 1000, 1, 'GOLD', 1, '2025-12-27 02:42:41');
INSERT INTO `hunter_gate_config` VALUES (6, 'Gate Infausto', 'S', 'S', 115, 6, 4385, 15, 24, 3500, 1750, 1, 'PURPLE', 1, '2025-12-27 02:42:41');
INSERT INTO `hunter_gate_config` VALUES (7, 'Gate del Giudizio', 'N', 'N', 130, 7, 4011, 15, 24, 5000, 2500, 1, 'BLACKWHITE', 1, '2025-12-27 02:42:41');

-- ----------------------------
-- Table structure for hunter_gate_history
-- ----------------------------
DROP TABLE IF EXISTS `hunter_gate_history`;
CREATE TABLE `hunter_gate_history`  (
  `history_id` int NOT NULL AUTO_INCREMENT,
  `player_id` int NOT NULL,
  `player_name` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `gate_id` int NOT NULL,
  `gate_name` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `result` enum('completed','failed','expired','death') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `gloria_change` int NOT NULL COMMENT 'Positivo o negativo',
  `duration_seconds` int NULL DEFAULT 0,
  `completed_at` timestamp NULL DEFAULT current_timestamp,
  PRIMARY KEY (`history_id`) USING BTREE,
  INDEX `idx_player`(`player_id` ASC) USING BTREE,
  INDEX `idx_date`(`completed_at` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 53 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of hunter_gate_history
-- ----------------------------
INSERT INTO `hunter_gate_history` VALUES (43, 4, '[GF]HunabKu', 1, 'Gate', 'failed', -250, 300, '2025-12-29 21:48:46');
INSERT INTO `hunter_gate_history` VALUES (44, 4, '[GF]HunabKu', 0, '', '', -250, 0, '2025-12-29 21:49:11');
INSERT INTO `hunter_gate_history` VALUES (45, 4, '[GF]HunabKu', 1, 'Gate', 'failed', -250, 300, '2025-12-29 23:19:07');
INSERT INTO `hunter_gate_history` VALUES (46, 4, '[GF]HunabKu', 1, 'Gate', 'completed', 1125, 300, '2025-12-29 23:19:16');
INSERT INTO `hunter_gate_history` VALUES (47, 4, '[GF]HunabKu', 1, 'Gate', 'failed', -250, 300, '2025-12-29 23:21:29');
INSERT INTO `hunter_gate_history` VALUES (48, 4, '[GF]HunabKu', 0, '', '', -250, 0, '2025-12-30 14:29:51');
INSERT INTO `hunter_gate_history` VALUES (49, 4, '[GF]HunabKu', 0, '', '', -250, 0, '2025-12-31 19:11:08');
INSERT INTO `hunter_gate_history` VALUES (50, 4, '[GF]HunabKu', 0, '', '', -250, 0, '2025-12-31 22:41:32');
INSERT INTO `hunter_gate_history` VALUES (51, 4, '[GF]HunabKu', 0, '', '', -250, 0, '2025-12-31 22:41:44');
INSERT INTO `hunter_gate_history` VALUES (52, 4, '[GF]HunabKu', 0, '', '', -250, 0, '2025-12-31 23:14:26');

-- ----------------------------
-- Table structure for hunter_gate_selection_config
-- ----------------------------
DROP TABLE IF EXISTS `hunter_gate_selection_config`;
CREATE TABLE `hunter_gate_selection_config`  (
  `config_id` int NOT NULL AUTO_INCREMENT,
  `selection_interval_hours` int NOT NULL DEFAULT 4 COMMENT 'Ogni quante ore seleziona',
  `players_per_selection` int NOT NULL DEFAULT 5 COMMENT 'Quanti giocatori per volta',
  `access_duration_hours` int NOT NULL DEFAULT 2 COMMENT 'Ore di validità accesso',
  `min_rank` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'E',
  `min_level` int NOT NULL DEFAULT 30,
  `min_total_points` int NOT NULL DEFAULT 1000,
  `last_selection_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`config_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of hunter_gate_selection_config
-- ----------------------------
INSERT INTO `hunter_gate_selection_config` VALUES (1, 4, 5, 2, 'E', 30, 1000, '2025-12-28 02:42:42');

-- ----------------------------
-- Table structure for hunter_item_names
-- ----------------------------
DROP TABLE IF EXISTS `hunter_item_names`;
CREATE TABLE `hunter_item_names`  (
  `vnum` int NOT NULL,
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`vnum`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of hunter_item_names
-- ----------------------------
INSERT INTO `hunter_item_names` VALUES (50160, 'Scanner di Fratture');
INSERT INTO `hunter_item_names` VALUES (50161, 'Stabilizzatore di Rango');
INSERT INTO `hunter_item_names` VALUES (50162, 'Focus del Cacciatore');
INSERT INTO `hunter_item_names` VALUES (50163, 'Chiave Dimensionale');
INSERT INTO `hunter_item_names` VALUES (50164, 'Sigillo di Conquista');
INSERT INTO `hunter_item_names` VALUES (50165, 'Segnale di Emergenza');
INSERT INTO `hunter_item_names` VALUES (50166, 'Risonatore di Gruppo');
INSERT INTO `hunter_item_names` VALUES (50167, 'Calibratore Fratture');
INSERT INTO `hunter_item_names` VALUES (50168, 'Frammento di Monarca');
INSERT INTO `hunter_item_names` VALUES (63000, 'Baule Rango E');
INSERT INTO `hunter_item_names` VALUES (63001, 'Baule Rango D');
INSERT INTO `hunter_item_names` VALUES (63002, 'Baule Rango C');
INSERT INTO `hunter_item_names` VALUES (63003, 'Baule Rango B');
INSERT INTO `hunter_item_names` VALUES (63004, 'Baule Rango A');
INSERT INTO `hunter_item_names` VALUES (63005, 'Baule Rango S');
INSERT INTO `hunter_item_names` VALUES (63006, 'Baule Rango ???');
INSERT INTO `hunter_item_names` VALUES (63007, 'Baule Speciale');
INSERT INTO `hunter_item_names` VALUES (80030, 'Buono 100 Gloria');
INSERT INTO `hunter_item_names` VALUES (80031, 'Buono 500 Gloria');
INSERT INTO `hunter_item_names` VALUES (80032, 'Buono 1000 Gloria');

-- ----------------------------
-- Table structure for hunter_login_messages
-- ----------------------------
DROP TABLE IF EXISTS `hunter_login_messages`;
CREATE TABLE `hunter_login_messages`  (
  `day_number` int NOT NULL,
  `message_text` varchar(300) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  PRIMARY KEY (`day_number`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of hunter_login_messages
-- ----------------------------
INSERT INTO `hunter_login_messages` VALUES (1, 'Primo_giorno_di_caccia._Il_viaggio_inizia_ora.');
INSERT INTO `hunter_login_messages` VALUES (2, 'Secondo_giorno._Stai_costruendo_un_abitudine.');
INSERT INTO `hunter_login_messages` VALUES (3, '[BONUS_ATTIVATO]_3_giorni_consecutivi!_+5%_Gloria.');
INSERT INTO `hunter_login_messages` VALUES (4, 'La_costanza_e_la_chiave._Continua_cosi.');
INSERT INTO `hunter_login_messages` VALUES (5, '5_giorni._Gli_altri_Cacciatori_ti_stanno_notando.');
INSERT INTO `hunter_login_messages` VALUES (6, 'Quasi_una_settimana._Il_Sistema_e_impressionato.');
INSERT INTO `hunter_login_messages` VALUES (7, '[BONUS_POTENZIATO]_7_giorni!_+10%_Gloria._Sei_determinato.');
INSERT INTO `hunter_login_messages` VALUES (14, '2_settimane._Pochi_hanno_la_tua_dedizione.');
INSERT INTO `hunter_login_messages` VALUES (21, '3_settimane._Stai_diventando_una_leggenda.');
INSERT INTO `hunter_login_messages` VALUES (30, '[BONUS_MASSIMO]_30_giorni!_+20%_Gloria._Il_Sistema_ti_onora.');
INSERT INTO `hunter_login_messages` VALUES (60, '60_giorni._Sei_un_esempio_per_tutti_i_Cacciatori.');
INSERT INTO `hunter_login_messages` VALUES (90, '90_giorni._Il_tuo_nome_risuona_nelle_cronache.');
INSERT INTO `hunter_login_messages` VALUES (100, '[CENTENARIO]_100_giorni!_Sei_entrato_nella_storia.');
INSERT INTO `hunter_login_messages` VALUES (180, '180_giorni._Mezzo_anno_di_caccia_ininterrotta.');
INSERT INTO `hunter_login_messages` VALUES (365, '[IMMORTALE]_Un_anno_intero!_Sei_diventato_immortale.');

-- ----------------------------
-- Table structure for hunter_mission_definitions
-- ----------------------------
DROP TABLE IF EXISTS `hunter_mission_definitions`;
CREATE TABLE `hunter_mission_definitions`  (
  `mission_id` int NOT NULL AUTO_INCREMENT,
  `mission_name` varchar(100) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `mission_type` varchar(20) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `target_vnum` int NULL DEFAULT 0,
  `target_count` int NOT NULL DEFAULT 10,
  `min_rank` varchar(2) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT 'E',
  `gloria_reward` int NOT NULL DEFAULT 100,
  `gloria_penalty` int NOT NULL DEFAULT 25,
  `time_limit_minutes` int NULL DEFAULT 1440,
  `enabled` tinyint(1) NULL DEFAULT 1,
  `created_at` timestamp NULL DEFAULT current_timestamp,
  PRIMARY KEY (`mission_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 50 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of hunter_mission_definitions
-- ----------------------------
INSERT INTO `hunter_mission_definitions` VALUES (1, 'Caccia ai Lupi', 'kill_mob', 101, 10, 'E', 50, 10, 1440, 1, '2025-12-24 05:34:27');
INSERT INTO `hunter_mission_definitions` VALUES (2, 'Stermina gli Orchi', 'kill_mob', 631, 15, 'E', 75, 15, 1440, 1, '2025-12-24 05:34:27');
INSERT INTO `hunter_mission_definitions` VALUES (3, 'Elimina i Cinghiali', 'kill_mob', 102, 20, 'E', 60, 12, 1440, 1, '2025-12-24 05:34:27');
INSERT INTO `hunter_mission_definitions` VALUES (4, 'Caccia agli Orsi', 'kill_mob', 1901, 8, 'E', 80, 16, 1440, 1, '2025-12-24 05:34:27');
INSERT INTO `hunter_mission_definitions` VALUES (5, 'Pulizia Ragni', 'kill_mob', 491, 12, 'E', 55, 11, 1440, 1, '2025-12-24 05:34:27');
INSERT INTO `hunter_mission_definitions` VALUES (6, 'Uccidi i Banditi', 'kill_mob', 5001, 10, 'E', 70, 14, 1440, 1, '2025-12-24 05:34:27');
INSERT INTO `hunter_mission_definitions` VALUES (7, 'Caccia Generale', 'kill_mob', 0, 25, 'E', 65, 13, 1440, 1, '2025-12-24 05:34:27');
INSERT INTO `hunter_mission_definitions` VALUES (8, 'Caccia ai Guerrieri Orco', 'kill_mob', 632, 15, 'D', 100, 20, 1440, 1, '2025-12-24 05:34:27');
INSERT INTO `hunter_mission_definitions` VALUES (9, 'Stermina gli Scheletri', 'kill_mob', 691, 20, 'D', 110, 22, 1440, 1, '2025-12-24 05:34:27');
INSERT INTO `hunter_mission_definitions` VALUES (10, 'Elimina i Demoni Minori', 'kill_mob', 1091, 12, 'D', 120, 24, 1440, 1, '2025-12-24 05:34:27');
INSERT INTO `hunter_mission_definitions` VALUES (11, 'Distruggi 2 Metin', 'kill_metin', 0, 2, 'D', 150, 30, 1440, 1, '2025-12-24 05:34:27');
INSERT INTO `hunter_mission_definitions` VALUES (12, 'Caccia agli Zombie', 'kill_mob', 791, 18, 'D', 95, 19, 1440, 1, '2025-12-24 05:34:27');
INSERT INTO `hunter_mission_definitions` VALUES (13, 'Uccidi i Ninja Nemici', 'kill_mob', 5101, 10, 'D', 130, 26, 1440, 1, '2025-12-24 05:34:27');
INSERT INTO `hunter_mission_definitions` VALUES (14, 'Pulizia Dungeon', 'kill_mob', 0, 30, 'D', 105, 21, 1440, 1, '2025-12-24 05:34:27');
INSERT INTO `hunter_mission_definitions` VALUES (15, 'Caccia al Boss Ragno', 'kill_boss', 492, 1, 'C', 200, 40, 1440, 1, '2025-12-24 05:34:27');
INSERT INTO `hunter_mission_definitions` VALUES (16, 'Stermina i Guerrieri Elite', 'kill_mob', 634, 15, 'C', 180, 36, 1440, 1, '2025-12-24 05:34:27');
INSERT INTO `hunter_mission_definitions` VALUES (17, 'Distruggi 3 Metin', 'kill_metin', 0, 3, 'C', 250, 50, 1440, 1, '2025-12-24 05:34:27');
INSERT INTO `hunter_mission_definitions` VALUES (18, 'Caccia ai Demoni', 'kill_mob', 1092, 12, 'C', 190, 38, 1440, 1, '2025-12-24 05:34:27');
INSERT INTO `hunter_mission_definitions` VALUES (19, 'Uccidi Boss Orco', 'kill_boss', 691, 1, 'C', 220, 44, 1440, 1, '2025-12-24 05:34:27');
INSERT INTO `hunter_mission_definitions` VALUES (20, 'Pulizia Avanzata', 'kill_mob', 0, 40, 'C', 170, 34, 1440, 1, '2025-12-24 05:34:27');
INSERT INTO `hunter_mission_definitions` VALUES (21, 'Caccia ai Non-Morti', 'kill_mob', 792, 20, 'C', 185, 37, 1440, 1, '2025-12-24 05:34:27');
INSERT INTO `hunter_mission_definitions` VALUES (22, 'Uccidi il Generale Orco', 'kill_boss', 693, 1, 'B', 350, 70, 1440, 1, '2025-12-24 05:34:27');
INSERT INTO `hunter_mission_definitions` VALUES (23, 'Distruggi 5 Metin', 'kill_metin', 0, 5, 'B', 400, 80, 1440, 1, '2025-12-24 05:34:27');
INSERT INTO `hunter_mission_definitions` VALUES (24, 'Sigilla una Frattura', 'seal_fracture', 0, 1, 'B', 500, 100, 1440, 1, '2025-12-24 05:34:27');
INSERT INTO `hunter_mission_definitions` VALUES (25, 'Caccia ai Demoni Maggiori', 'kill_mob', 1093, 15, 'B', 300, 60, 1440, 1, '2025-12-24 05:34:27');
INSERT INTO `hunter_mission_definitions` VALUES (26, 'Stermina i Capitani', 'kill_boss', 0, 2, 'B', 380, 76, 1440, 1, '2025-12-24 05:34:27');
INSERT INTO `hunter_mission_definitions` VALUES (27, 'Pulizia Massiva', 'kill_mob', 0, 60, 'B', 280, 56, 1440, 1, '2025-12-24 05:34:27');
INSERT INTO `hunter_mission_definitions` VALUES (28, 'Caccia Notturna', 'kill_mob', 793, 25, 'B', 320, 64, 1440, 1, '2025-12-24 05:34:27');
INSERT INTO `hunter_mission_definitions` VALUES (29, 'Uccidi il Re degli Orchi', 'kill_boss', 694, 1, 'A', 600, 120, 1440, 1, '2025-12-24 05:34:27');
INSERT INTO `hunter_mission_definitions` VALUES (30, 'Distruggi 8 Metin', 'kill_metin', 0, 8, 'A', 700, 140, 1440, 1, '2025-12-24 05:34:27');
INSERT INTO `hunter_mission_definitions` VALUES (31, 'Sigilla 2 Fratture', 'seal_fracture', 0, 2, 'A', 900, 180, 1440, 1, '2025-12-24 05:34:27');
INSERT INTO `hunter_mission_definitions` VALUES (32, 'Caccia ai Boss Demoniaci', 'kill_boss', 1094, 2, 'A', 650, 130, 1440, 1, '2025-12-24 05:34:27');
INSERT INTO `hunter_mission_definitions` VALUES (33, 'Sterminio Totale', 'kill_mob', 0, 100, 'A', 550, 110, 1440, 1, '2025-12-24 05:34:27');
INSERT INTO `hunter_mission_definitions` VALUES (34, 'Caccia ai Generali', 'kill_boss', 0, 3, 'A', 720, 144, 1440, 1, '2025-12-24 05:34:27');
INSERT INTO `hunter_mission_definitions` VALUES (35, 'Elite Hunter', 'kill_mob', 0, 80, 'A', 580, 116, 1440, 1, '2025-12-24 05:34:27');
INSERT INTO `hunter_mission_definitions` VALUES (36, 'Uccidi il Signore dei Demoni', 'kill_boss', 1095, 1, 'S', 1000, 200, 1440, 1, '2025-12-24 05:34:27');
INSERT INTO `hunter_mission_definitions` VALUES (37, 'Distruggi 12 Metin', 'kill_metin', 0, 12, 'S', 1100, 220, 1440, 1, '2025-12-24 05:34:27');
INSERT INTO `hunter_mission_definitions` VALUES (38, 'Sigilla 3 Fratture', 'seal_fracture', 0, 3, 'S', 1500, 300, 1440, 1, '2025-12-24 05:34:27');
INSERT INTO `hunter_mission_definitions` VALUES (39, 'Caccia Leggendaria', 'kill_boss', 0, 5, 'S', 1200, 240, 1440, 1, '2025-12-24 05:34:27');
INSERT INTO `hunter_mission_definitions` VALUES (40, 'Massacro', 'kill_mob', 0, 150, 'S', 900, 180, 1440, 1, '2025-12-24 05:34:27');
INSERT INTO `hunter_mission_definitions` VALUES (41, 'Dominio Assoluto', 'kill_boss', 0, 4, 'S', 1300, 260, 1440, 1, '2025-12-24 05:34:27');
INSERT INTO `hunter_mission_definitions` VALUES (42, 'Campione del Server', 'kill_mob', 0, 120, 'S', 950, 190, 1440, 1, '2025-12-24 05:34:27');
INSERT INTO `hunter_mission_definitions` VALUES (43, 'Uccidi il Boss Finale', 'kill_boss', 0, 3, 'N', 2000, 400, 1440, 1, '2025-12-24 05:34:27');
INSERT INTO `hunter_mission_definitions` VALUES (44, 'Distruggi 20 Metin', 'kill_metin', 0, 20, 'N', 2500, 500, 1440, 1, '2025-12-24 05:34:27');
INSERT INTO `hunter_mission_definitions` VALUES (45, 'Sigilla 5 Fratture', 'seal_fracture', 0, 5, 'N', 3000, 600, 1440, 1, '2025-12-24 05:34:27');
INSERT INTO `hunter_mission_definitions` VALUES (46, 'Leggenda Nazionale', 'kill_boss', 0, 8, 'N', 2200, 440, 1440, 1, '2025-12-24 05:34:27');
INSERT INTO `hunter_mission_definitions` VALUES (47, 'Annientamento', 'kill_mob', 0, 250, 'N', 1800, 360, 1440, 1, '2025-12-24 05:34:27');
INSERT INTO `hunter_mission_definitions` VALUES (48, 'Imperatore Hunter', 'kill_boss', 0, 6, 'N', 2400, 480, 1440, 1, '2025-12-24 05:34:27');
INSERT INTO `hunter_mission_definitions` VALUES (49, 'Gloria Eterna', 'kill_mob', 0, 200, 'N', 1900, 380, 1440, 1, '2025-12-24 05:34:27');

-- ----------------------------
-- Table structure for hunter_player_missions
-- ----------------------------
DROP TABLE IF EXISTS `hunter_player_missions`;
CREATE TABLE `hunter_player_missions`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `player_id` int NOT NULL,
  `mission_slot` int NOT NULL DEFAULT 1,
  `mission_def_id` int NOT NULL,
  `assigned_date` date NOT NULL,
  `current_progress` int NULL DEFAULT 0,
  `target_count` int NOT NULL,
  `status` enum('active','completed','failed') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT 'active',
  `reward_glory` int NOT NULL DEFAULT 100,
  `penalty_glory` int NOT NULL DEFAULT 25,
  `completed_at` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `unique_player_slot_day`(`player_id` ASC, `mission_slot` ASC, `assigned_date` ASC) USING BTREE,
  INDEX `idx_player_date`(`player_id` ASC, `assigned_date` ASC) USING BTREE,
  INDEX `idx_status`(`status` ASC) USING BTREE,
  INDEX `mission_def_id`(`mission_def_id` ASC) USING BTREE,
  INDEX `idx_missions_player_date`(`player_id` ASC, `assigned_date` ASC) USING BTREE,
  CONSTRAINT `hunter_player_missions_ibfk_1` FOREIGN KEY (`mission_def_id`) REFERENCES `hunter_mission_definitions` (`mission_id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 82 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of hunter_player_missions
-- ----------------------------
INSERT INTO `hunter_player_missions` VALUES (28, 4, 1, 18, '2025-12-27', 12, 12, 'completed', 190, 38, '2025-12-27 02:10:07');
INSERT INTO `hunter_player_missions` VALUES (29, 4, 2, 7, '2025-12-27', 25, 25, 'completed', 65, 13, '2025-12-27 01:59:25');
INSERT INTO `hunter_player_missions` VALUES (30, 4, 3, 9, '2025-12-27', 6, 20, 'failed', 110, 22, NULL);
INSERT INTO `hunter_player_missions` VALUES (31, 3900, 1, 7, '2025-12-27', 0, 25, 'failed', 65, 13, NULL);
INSERT INTO `hunter_player_missions` VALUES (32, 3900, 2, 2, '2025-12-27', 0, 15, 'failed', 75, 15, NULL);
INSERT INTO `hunter_player_missions` VALUES (33, 3900, 3, 6, '2025-12-27', 0, 10, 'failed', 70, 14, NULL);
INSERT INTO `hunter_player_missions` VALUES (34, 2, 1, 5, '2025-12-27', 0, 12, 'failed', 55, 11, NULL);
INSERT INTO `hunter_player_missions` VALUES (35, 2, 2, 18, '2025-12-27', 0, 12, 'failed', 190, 38, NULL);
INSERT INTO `hunter_player_missions` VALUES (36, 2, 3, 17, '2025-12-27', 0, 3, 'failed', 250, 50, NULL);
INSERT INTO `hunter_player_missions` VALUES (37, 2, 1, 9, '2025-12-28', 0, 20, 'active', 110, 22, NULL);
INSERT INTO `hunter_player_missions` VALUES (38, 2, 2, 12, '2025-12-28', 0, 18, 'active', 95, 19, NULL);
INSERT INTO `hunter_player_missions` VALUES (39, 2, 3, 15, '2025-12-28', 0, 1, 'active', 200, 40, NULL);
INSERT INTO `hunter_player_missions` VALUES (40, 4, 1, 27, '2025-12-28', 60, 60, 'completed', 280, 56, '2025-12-28 02:09:55');
INSERT INTO `hunter_player_missions` VALUES (41, 4, 2, 14, '2025-12-28', 30, 30, 'completed', 105, 21, '2025-12-28 01:49:03');
INSERT INTO `hunter_player_missions` VALUES (42, 4, 3, 16, '2025-12-28', 0, 15, 'active', 180, 36, NULL);
INSERT INTO `hunter_player_missions` VALUES (43, 4, 1, 2, '2025-12-29', 1, 15, 'active', 75, 15, NULL);
INSERT INTO `hunter_player_missions` VALUES (44, 4, 2, 4, '2025-12-29', 0, 8, 'active', 80, 16, NULL);
INSERT INTO `hunter_player_missions` VALUES (45, 4, 3, 21, '2025-12-29', 0, 20, 'active', 185, 37, NULL);
INSERT INTO `hunter_player_missions` VALUES (46, 4, 1, 47, '2025-12-30', 250, 250, 'completed', 1800, 360, '2025-12-30 02:15:34');
INSERT INTO `hunter_player_missions` VALUES (47, 4, 2, 21, '2025-12-30', 0, 20, 'active', 185, 37, NULL);
INSERT INTO `hunter_player_missions` VALUES (48, 4, 3, 49, '2025-12-30', 200, 200, 'completed', 1900, 380, '2025-12-30 02:15:06');
INSERT INTO `hunter_player_missions` VALUES (49, 994, 1, 3, '2025-12-30', 0, 20, 'active', 60, 12, NULL);
INSERT INTO `hunter_player_missions` VALUES (50, 994, 2, 2, '2025-12-30', 0, 15, 'active', 75, 15, NULL);
INSERT INTO `hunter_player_missions` VALUES (51, 994, 3, 4, '2025-12-30', 0, 8, 'active', 80, 16, NULL);
INSERT INTO `hunter_player_missions` VALUES (52, 2, 1, 16, '2025-12-30', 0, 15, 'active', 180, 36, NULL);
INSERT INTO `hunter_player_missions` VALUES (53, 2, 2, 21, '2025-12-30', 0, 20, 'active', 185, 37, NULL);
INSERT INTO `hunter_player_missions` VALUES (54, 2, 3, 2, '2025-12-30', 0, 15, 'active', 75, 15, NULL);
INSERT INTO `hunter_player_missions` VALUES (55, 4, 1, 23, '2025-12-31', 5, 5, 'completed', 400, 80, '2025-12-31 04:27:02');
INSERT INTO `hunter_player_missions` VALUES (56, 4, 2, 26, '2025-12-31', 2, 2, 'completed', 380, 76, '2025-12-31 04:26:58');
INSERT INTO `hunter_player_missions` VALUES (57, 4, 3, 32, '2025-12-31', 0, 2, 'active', 650, 130, NULL);
INSERT INTO `hunter_player_missions` VALUES (58, 4, 1, 46, '2026-01-01', 0, 8, 'active', 2200, 440, NULL);
INSERT INTO `hunter_player_missions` VALUES (59, 4, 2, 37, '2026-01-01', 0, 12, 'active', 1100, 220, NULL);
INSERT INTO `hunter_player_missions` VALUES (60, 4, 3, 7, '2026-01-01', 0, 25, 'active', 65, 13, NULL);
INSERT INTO `hunter_player_missions` VALUES (61, 4, 1, 26, '2026-01-04', 1, 2, 'active', 380, 76, NULL);
INSERT INTO `hunter_player_missions` VALUES (62, 4, 2, 6, '2026-01-04', 0, 10, 'active', 70, 14, NULL);
INSERT INTO `hunter_player_missions` VALUES (63, 4, 3, 39, '2026-01-04', 1, 5, 'active', 1200, 240, NULL);
INSERT INTO `hunter_player_missions` VALUES (64, 1684, 1, 5, '2026-01-04', 0, 12, 'active', 55, 11, NULL);
INSERT INTO `hunter_player_missions` VALUES (65, 1684, 2, 3, '2026-01-04', 0, 20, 'active', 60, 12, NULL);
INSERT INTO `hunter_player_missions` VALUES (66, 1684, 3, 7, '2026-01-04', 25, 25, 'completed', 65, 13, '2026-01-04 15:20:35');
INSERT INTO `hunter_player_missions` VALUES (67, 4, 1, 42, '2026-01-05', 0, 120, 'active', 950, 190, NULL);
INSERT INTO `hunter_player_missions` VALUES (68, 4, 2, 30, '2026-01-05', 0, 8, 'active', 700, 140, NULL);
INSERT INTO `hunter_player_missions` VALUES (69, 4, 3, 20, '2026-01-05', 0, 40, 'active', 170, 34, NULL);
INSERT INTO `hunter_player_missions` VALUES (70, 2, 1, 9, '2026-01-06', 0, 20, 'active', 110, 22, NULL);
INSERT INTO `hunter_player_missions` VALUES (71, 2, 2, 17, '2026-01-06', 0, 3, 'active', 250, 50, NULL);
INSERT INTO `hunter_player_missions` VALUES (72, 2, 3, 20, '2026-01-06', 0, 40, 'active', 170, 34, NULL);
INSERT INTO `hunter_player_missions` VALUES (73, 3901, 1, 6, '2026-01-06', 0, 10, 'active', 70, 14, NULL);
INSERT INTO `hunter_player_missions` VALUES (74, 3901, 2, 7, '2026-01-06', 25, 25, 'completed', 65, 13, '2026-01-06 12:00:32');
INSERT INTO `hunter_player_missions` VALUES (75, 3901, 3, 5, '2026-01-06', 0, 12, 'active', 55, 11, NULL);
INSERT INTO `hunter_player_missions` VALUES (76, 4, 1, 5, '2026-01-06', 0, 12, 'active', 55, 11, NULL);
INSERT INTO `hunter_player_missions` VALUES (77, 4, 2, 22, '2026-01-06', 0, 1, 'active', 350, 70, NULL);
INSERT INTO `hunter_player_missions` VALUES (78, 4, 3, 25, '2026-01-06', 0, 15, 'active', 300, 60, NULL);
INSERT INTO `hunter_player_missions` VALUES (79, 1684, 1, 3, '2026-01-06', 0, 20, 'active', 60, 12, NULL);
INSERT INTO `hunter_player_missions` VALUES (80, 1684, 2, 1, '2026-01-06', 0, 10, 'active', 50, 10, NULL);
INSERT INTO `hunter_player_missions` VALUES (81, 1684, 3, 7, '2026-01-06', 0, 25, 'active', 65, 13, NULL);

-- ----------------------------
-- Table structure for hunter_player_stats_snapshot
-- ----------------------------
DROP TABLE IF EXISTS `hunter_player_stats_snapshot`;
CREATE TABLE `hunter_player_stats_snapshot`  (
  `snapshot_id` bigint NOT NULL AUTO_INCREMENT,
  `player_id` int NOT NULL,
  `player_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `snapshot_type` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'HOURLY, DAILY, SESSION',
  `kills_count` int NOT NULL DEFAULT 0,
  `glory_earned` int NOT NULL DEFAULT 0,
  `chests_opened` int NOT NULL DEFAULT 0,
  `fractures_completed` int NOT NULL DEFAULT 0,
  `defenses_won` int NOT NULL DEFAULT 0,
  `defenses_lost` int NOT NULL DEFAULT 0,
  `avg_kill_interval_ms` int NULL DEFAULT NULL COMMENT 'Intervallo medio tra kill in ms',
  `min_kill_interval_ms` int NULL DEFAULT NULL COMMENT 'Intervallo minimo (sospetto se troppo basso)',
  `session_duration_sec` int NULL DEFAULT NULL,
  `anomaly_score` int NOT NULL DEFAULT 0 COMMENT '0-100, alto = sospetto',
  `created_at` datetime NOT NULL DEFAULT current_timestamp,
  PRIMARY KEY (`snapshot_id`) USING BTREE,
  INDEX `idx_player_type`(`player_id` ASC, `snapshot_type` ASC, `created_at` ASC) USING BTREE,
  INDEX `idx_anomaly`(`anomaly_score` ASC, `created_at` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of hunter_player_stats_snapshot
-- ----------------------------

-- ----------------------------
-- Table structure for hunter_player_trials
-- ----------------------------
DROP TABLE IF EXISTS `hunter_player_trials`;
CREATE TABLE `hunter_player_trials`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `player_id` int NOT NULL,
  `trial_id` int NOT NULL,
  `status` enum('locked','available','in_progress','completed','failed') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT 'locked',
  `boss_kills` int NOT NULL DEFAULT 0,
  `metin_kills` int NOT NULL DEFAULT 0,
  `fracture_seals` int NOT NULL DEFAULT 0,
  `chest_opens` int NOT NULL DEFAULT 0,
  `daily_missions` int NOT NULL DEFAULT 0,
  `started_at` timestamp NULL DEFAULT NULL,
  `completed_at` timestamp NULL DEFAULT NULL,
  `expires_at` timestamp NULL DEFAULT NULL COMMENT 'Se ha time limit',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `unique_player_trial`(`player_id` ASC, `trial_id` ASC) USING BTREE,
  INDEX `trial_id`(`trial_id` ASC) USING BTREE,
  INDEX `idx_player_status`(`player_id` ASC, `status` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 20 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of hunter_player_trials
-- ----------------------------
INSERT INTO `hunter_player_trials` VALUES (18, 4, 1, 'completed', 3, 6, 0, 0, 0, '2025-12-30 11:41:12', '2025-12-30 11:46:42', NULL);
INSERT INTO `hunter_player_trials` VALUES (19, 4, 2, 'in_progress', 4, 0, 5, 2, 0, '2025-12-31 19:51:00', NULL, NULL);

-- ----------------------------
-- Table structure for hunter_quest_achievements_config
-- ----------------------------
DROP TABLE IF EXISTS `hunter_quest_achievements_config`;
CREATE TABLE `hunter_quest_achievements_config`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL,
  `type` int NULL DEFAULT 1,
  `requirement` int NULL DEFAULT 0,
  `reward_vnum` int NULL DEFAULT 0,
  `reward_count` int NULL DEFAULT 0,
  `enabled` tinyint(1) NULL DEFAULT 1,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 13 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of hunter_quest_achievements_config
-- ----------------------------
INSERT INTO `hunter_quest_achievements_config` VALUES (1, 'Novizio (Kill)', 1, 10, 80030, 1, 1);
INSERT INTO `hunter_quest_achievements_config` VALUES (2, 'Principiante (Kill)', 1, 50, 80030, 5, 1);
INSERT INTO `hunter_quest_achievements_config` VALUES (3, 'Cacciatore D (Kill)', 1, 100, 80031, 1, 1);
INSERT INTO `hunter_quest_achievements_config` VALUES (4, 'Cacciatore C (Kill)', 1, 250, 80031, 2, 1);
INSERT INTO `hunter_quest_achievements_config` VALUES (5, 'Cacciatore B (Kill)', 1, 500, 80032, 1, 1);
INSERT INTO `hunter_quest_achievements_config` VALUES (6, 'Cacciatore A (Kill)', 1, 1000, 80032, 2, 1);
INSERT INTO `hunter_quest_achievements_config` VALUES (7, 'Elite S (Kill)', 1, 2500, 80032, 5, 1);
INSERT INTO `hunter_quest_achievements_config` VALUES (8, 'Fama Nascente (Punti)', 2, 5000, 80030, 10, 1);
INSERT INTO `hunter_quest_achievements_config` VALUES (9, 'Fama Media (Punti)', 2, 20000, 80031, 5, 1);
INSERT INTO `hunter_quest_achievements_config` VALUES (10, 'Fama Alta (Punti)', 2, 50000, 80032, 5, 1);
INSERT INTO `hunter_quest_achievements_config` VALUES (11, 'Leggenda (Punti)', 2, 100000, 80040, 1, 1);
INSERT INTO `hunter_quest_achievements_config` VALUES (12, 'MONARCA (Punti)', 2, 500000, 80039, 1, 1);

-- ----------------------------
-- Table structure for hunter_quest_config
-- ----------------------------
DROP TABLE IF EXISTS `hunter_quest_config`;
CREATE TABLE `hunter_quest_config`  (
  `config_key` varchar(50) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `config_value` int NULL DEFAULT 0,
  PRIMARY KEY (`config_key`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of hunter_quest_config
-- ----------------------------
INSERT INTO `hunter_quest_config` VALUES ('bonus_all_missions_complete', 50);
INSERT INTO `hunter_quest_config` VALUES ('bonus_speed_kill_multiplier', 2);
INSERT INTO `hunter_quest_config` VALUES ('challenge_time_seconds', 60);
INSERT INTO `hunter_quest_config` VALUES ('conversion_gloria_to_credits', 10);
INSERT INTO `hunter_quest_config` VALUES ('daily_reset_hour', 0);
INSERT INTO `hunter_quest_config` VALUES ('emergency_chance_percent', 40);
INSERT INTO `hunter_quest_config` VALUES ('rank_threshold_A', 150000);
INSERT INTO `hunter_quest_config` VALUES ('rank_threshold_B', 50000);
INSERT INTO `hunter_quest_config` VALUES ('rank_threshold_C', 10000);
INSERT INTO `hunter_quest_config` VALUES ('rank_threshold_D', 2000);
INSERT INTO `hunter_quest_config` VALUES ('rank_threshold_E', 0);
INSERT INTO `hunter_quest_config` VALUES ('rank_threshold_N', 1500000);
INSERT INTO `hunter_quest_config` VALUES ('rank_threshold_S', 500000);
INSERT INTO `hunter_quest_config` VALUES ('rival_range_chests', 50);
INSERT INTO `hunter_quest_config` VALUES ('rival_range_daily', 500);
INSERT INTO `hunter_quest_config` VALUES ('rival_range_fractures', 20);
INSERT INTO `hunter_quest_config` VALUES ('rival_range_metins', 50);
INSERT INTO `hunter_quest_config` VALUES ('rival_range_total', 50000);
INSERT INTO `hunter_quest_config` VALUES ('rival_range_weekly', 2000);
INSERT INTO `hunter_quest_config` VALUES ('seal_fracture_bonus', 200);
INSERT INTO `hunter_quest_config` VALUES ('spawn_threshold_normal', 500);
INSERT INTO `hunter_quest_config` VALUES ('speedkill_boss_seconds', 60);
INSERT INTO `hunter_quest_config` VALUES ('speedkill_metin_seconds', 300);
INSERT INTO `hunter_quest_config` VALUES ('streak_days_tier1', 3);
INSERT INTO `hunter_quest_config` VALUES ('streak_days_tier2', 7);
INSERT INTO `hunter_quest_config` VALUES ('streak_days_tier3', 30);
INSERT INTO `hunter_quest_config` VALUES ('timer_reset_check', 60);
INSERT INTO `hunter_quest_config` VALUES ('timer_tips_random', 90);
INSERT INTO `hunter_quest_config` VALUES ('timer_update_stats', 60);
INSERT INTO `hunter_quest_config` VALUES ('welcome_offline_seconds', 120);
INSERT INTO `hunter_quest_config` VALUES ('whatif_chance_percent', 10);
INSERT INTO `hunter_quest_config` VALUES ('speedkill_boss_bonus_pts', 200);
INSERT INTO `hunter_quest_config` VALUES ('speedkill_metin_bonus_pts', 80);
INSERT INTO `hunter_quest_config` VALUES ('streak_bonus_3days', 3);
INSERT INTO `hunter_quest_config` VALUES ('streak_bonus_7days', 7);
INSERT INTO `hunter_quest_config` VALUES ('streak_bonus_30days', 12);

-- ----------------------------
-- Table structure for hunter_quest_emergencies
-- ----------------------------
DROP TABLE IF EXISTS `hunter_quest_emergencies`;
CREATE TABLE `hunter_quest_emergencies`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `description` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL,
  `duration_seconds` int NULL DEFAULT 60,
  `target_vnum` int NULL DEFAULT 0,
  `target_count` int NULL DEFAULT 10,
  `reward_points` int NULL DEFAULT 100,
  `reward_item_vnum` int NULL DEFAULT 0,
  `reward_item_count` int NULL DEFAULT 0,
  `enabled` int NULL DEFAULT 1,
  `min_level` int NULL DEFAULT 1,
  `max_level` int NULL DEFAULT 120,
  `difficulty` varchar(50) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT 'NORMAL',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 9 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of hunter_quest_emergencies
-- ----------------------------
INSERT INTO `hunter_quest_emergencies` VALUES (1, 'Sopravvivi all\'Orda', 'Uccidi 60 mostri in 60 secondi. Fai del tuo meglio!', 60, 0, 60, 300, 0, 0, 1, 5, 120, 'HARD');
INSERT INTO `hunter_quest_emergencies` VALUES (2, 'Distruttore di Metin', 'Distruggi 5 Metin in 3 minuti. Preparati a correre!', 180, 0, 5, 500, 0, 0, 1, 15, 120, 'HARD');
INSERT INTO `hunter_quest_emergencies` VALUES (3, 'Difesa Disperata', 'Elimina 120 nemici in 90 secondi. (1.3 kill al secondo)', 90, 0, 120, 600, 0, 0, 1, 30, 120, 'EXTREME');
INSERT INTO `hunter_quest_emergencies` VALUES (4, 'Cacciatore di Boss', 'Uccidi 3 Boss in 180 secondi. (Puoi cambiare CH)', 180, 0, 3, 1000, 0, 0, 1, 40, 120, 'EXTREME');
INSERT INTO `hunter_quest_emergencies` VALUES (5, 'Il Massacro', 'Uccidi 250 creature in 180 secondi. Serve AOE potente!', 180, 0, 250, 1200, 0, 0, 1, 50, 120, 'GOD_MODE');
INSERT INTO `hunter_quest_emergencies` VALUES (6, 'Prova del Novizio', 'Uccidi 30 mostri in 60 secondi. Missione introduttiva!', 60, 0, 30, 150, 0, 0, 1, 1, 50, 'EASY');
INSERT INTO `hunter_quest_emergencies` VALUES (7, 'Caccia Rapida', 'Uccidi 2 Boss in 120 secondi.', 120, 0, 2, 400, 0, 0, 1, 20, 80, 'NORMAL');
INSERT INTO `hunter_quest_emergencies` VALUES (8, 'Metin Sprint', 'Distruggi 3 Metin in 150 secondi.', 150, 0, 3, 350, 0, 0, 1, 15, 90, 'NORMAL');

-- ----------------------------
-- Table structure for hunter_quest_fractures
-- ----------------------------
DROP TABLE IF EXISTS `hunter_quest_fractures`;
CREATE TABLE `hunter_quest_fractures`  (
  `vnum` int NOT NULL,
  `name` varchar(50) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL,
  `rank_label` varchar(20) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL,
  `color_code` varchar(16) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL DEFAULT 'PURPLE',
  `spawn_chance` int NULL DEFAULT 10,
  `req_points` int NULL DEFAULT 0,
  `enabled` tinyint(1) NULL DEFAULT 1,
  `force_power_rank` int NOT NULL DEFAULT 0,
  PRIMARY KEY (`vnum`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of hunter_quest_fractures
-- ----------------------------
INSERT INTO `hunter_quest_fractures` VALUES (16060, 'Frattura Primordiale', 'E-Rank', 'GREEN', 44, 0, 1, 0);
INSERT INTO `hunter_quest_fractures` VALUES (16061, 'Frattura Astrale', 'D-Rank', 'BLUE', 30, 2000, 1, 0);
INSERT INTO `hunter_quest_fractures` VALUES (16062, 'Frattura Abissale', 'C-Rank', 'ORANGE', 15, 10000, 1, 0);
INSERT INTO `hunter_quest_fractures` VALUES (16063, 'Frattura Cremisi', 'B-Rank', 'RED', 5, 0, 1, 100);
INSERT INTO `hunter_quest_fractures` VALUES (16064, 'Frattura Aurea', 'A-Rank', 'GOLD', 3, 0, 1, 200);
INSERT INTO `hunter_quest_fractures` VALUES (16065, 'Frattura Infausta', 'S-Rank', 'PURPLE', 2, 0, 1, 350);
INSERT INTO `hunter_quest_fractures` VALUES (16066, 'Frattura Instabile', 'N-Rank', 'BLACKWHITE', 1, 0, 1, 500);
INSERT INTO `hunter_quest_fractures` VALUES (16067, 'Frattura del Tesoro', 'A-Rank', 'GOLD', 0, 150000, 0, 0);
INSERT INTO `hunter_quest_fractures` VALUES (16068, 'Frattura Maledetta', 'S-Rank', 'PURPLE', 0, 500000, 0, 0);

-- ----------------------------
-- Table structure for hunter_quest_jackpot_rewards
-- ----------------------------
DROP TABLE IF EXISTS `hunter_quest_jackpot_rewards`;
CREATE TABLE `hunter_quest_jackpot_rewards`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `type_name` varchar(20) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL,
  `item_vnum` int NOT NULL,
  `item_quantity` int NULL DEFAULT 1,
  `bonus_points` int NULL DEFAULT 0,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of hunter_quest_jackpot_rewards
-- ----------------------------
INSERT INTO `hunter_quest_jackpot_rewards` VALUES (1, 'JACKPOT', 80031, 1, 500);
INSERT INTO `hunter_quest_jackpot_rewards` VALUES (2, 'JACKPOT', 80032, 1, 1000);
INSERT INTO `hunter_quest_jackpot_rewards` VALUES (3, 'JACKPOT', 80040, 1, 0);
INSERT INTO `hunter_quest_jackpot_rewards` VALUES (4, 'BAULE', 80030, 1, 10);
INSERT INTO `hunter_quest_jackpot_rewards` VALUES (5, 'BAULE', 80031, 1, 50);

-- ----------------------------
-- Table structure for hunter_quest_ranking
-- ----------------------------
DROP TABLE IF EXISTS `hunter_quest_ranking`;
CREATE TABLE `hunter_quest_ranking`  (
  `player_id` int NOT NULL,
  `player_name` varchar(24) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `hunter_rank` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT 'E',
  `total_points` int NULL DEFAULT 0,
  `spendable_points` int NULL DEFAULT 0,
  `daily_points` int NULL DEFAULT 0,
  `weekly_points` int NULL DEFAULT 0,
  `total_kills` int NULL DEFAULT 0,
  `daily_kills` int NULL DEFAULT 0,
  `weekly_kills` int NULL DEFAULT 0,
  `login_streak` int NULL DEFAULT 0,
  `last_login` int NULL DEFAULT 0,
  `penalty_strikes` int NULL DEFAULT 0,
  `rival_pid` int NULL DEFAULT 0,
  `pending_daily_reward` int NULL DEFAULT 0,
  `pending_weekly_reward` int NULL DEFAULT 0,
  `total_fractures` int NULL DEFAULT 0,
  `total_chests` int NULL DEFAULT 0,
  `total_metins` int NULL DEFAULT 0,
  `current_rank` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT 'E',
  `last_activity` datetime NULL DEFAULT current_timestamp,
  `penalty_active` tinyint(1) UNSIGNED NOT NULL DEFAULT 0,
  `penalty_expires` int UNSIGNED NOT NULL DEFAULT 0,
  `failed_missions` int UNSIGNED NOT NULL DEFAULT 0,
  `overtaken_by` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `overtaken_diff` int NULL DEFAULT 0,
  `overtaken_label` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`player_id`) USING BTREE,
  INDEX `idx_daily_points`(`daily_points` DESC) USING BTREE,
  INDEX `idx_weekly_points`(`weekly_points` DESC) USING BTREE,
  INDEX `idx_total_points`(`total_points` DESC) USING BTREE,
  INDEX `idx_ranking_pid`(`player_id` ASC) USING BTREE,
  INDEX `idx_ranking_daily`(`daily_points` DESC) USING BTREE,
  INDEX `idx_ranking_weekly`(`weekly_points` DESC) USING BTREE
) ENGINE = InnoDB CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of hunter_quest_ranking
-- ----------------------------
INSERT INTO `hunter_quest_ranking` VALUES (2, '[GF]Aelarion', 'C', 33901, 24000, 0, 17000, 300, 0, 100, 0, 0, 0, 0, 0, 0, 48, 0, 0, 'C', '2025-12-21 17:41:26', 0, 0, 0, NULL, 0, NULL);
INSERT INTO `hunter_quest_ranking` VALUES (4, '[GF]HunabKu', 'D', 1505467, 89628, 5040, 5040, 28, 28, 28, 0, 0, 0, 0, 0, 0, 24, 2, 18, 'D', '2025-12-30 11:39:29', 0, 0, 0, NULL, 0, NULL);
INSERT INTO `hunter_quest_ranking` VALUES (994, 'Spikelino', 'E', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 'E', '2025-12-30 12:08:31', 0, 0, 0, NULL, 0, NULL);
INSERT INTO `hunter_quest_ranking` VALUES (1684, 'Pacifista', 'E', 393, 393, 243, 243, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 'E', '2026-01-04 14:59:49', 0, 0, 0, NULL, 0, NULL);
INSERT INTO `hunter_quest_ranking` VALUES (3893, 'Potenza', 'E', 95, 95, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 1, 0, 0, 'E', '2025-12-23 18:06:07', 0, 0, 0, '[GF]HunabKu', 1, 'ESPLORATORI');
INSERT INTO `hunter_quest_ranking` VALUES (3895, '123123123', 'E', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'E', '2025-12-25 12:02:22', 0, 0, 0, 'Pacifista', 1, 'ESPLORATORI');
INSERT INTO `hunter_quest_ranking` VALUES (3900, 'asdasdasd2', 'E', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'E', '2025-12-27 05:24:00', 0, 0, 0, 'Pacifista', 1, 'METIN');
INSERT INTO `hunter_quest_ranking` VALUES (3901, 'Spapum', 'E', 2915, 2915, 65, 65, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'E', '2026-01-06 12:00:19', 0, 0, 0, NULL, 0, NULL);

-- ----------------------------
-- Table structure for hunter_quest_rewards
-- ----------------------------
DROP TABLE IF EXISTS `hunter_quest_rewards`;
CREATE TABLE `hunter_quest_rewards`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `reward_type` varchar(10) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT 'daily',
  `rank_position` int NULL DEFAULT 1,
  `item_vnum` int NOT NULL,
  `item_quantity` int NULL DEFAULT 1,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of hunter_quest_rewards
-- ----------------------------
INSERT INTO `hunter_quest_rewards` VALUES (1, 'daily', 1, 80032, 2);
INSERT INTO `hunter_quest_rewards` VALUES (2, 'daily', 2, 80031, 2);
INSERT INTO `hunter_quest_rewards` VALUES (3, 'daily', 3, 80030, 2);
INSERT INTO `hunter_quest_rewards` VALUES (4, 'weekly', 1, 80039, 1);
INSERT INTO `hunter_quest_rewards` VALUES (5, 'weekly', 2, 80040, 1);
INSERT INTO `hunter_quest_rewards` VALUES (6, 'weekly', 3, 80032, 5);

-- ----------------------------
-- Table structure for hunter_quest_shop
-- ----------------------------
DROP TABLE IF EXISTS `hunter_quest_shop`;
CREATE TABLE `hunter_quest_shop`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `item_vnum` int NOT NULL,
  `item_count` int NULL DEFAULT 1,
  `price_points` int NULL DEFAULT 1000,
  `description` varchar(100) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT 'Item',
  `display_order` int NULL DEFAULT 0,
  `enabled` tinyint(1) NULL DEFAULT 1,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 15 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of hunter_quest_shop
-- ----------------------------
INSERT INTO `hunter_quest_shop` VALUES (1, 80030, 1, 500, 'Buono 100 Punti', 1, 1);
INSERT INTO `hunter_quest_shop` VALUES (2, 80031, 1, 2500, 'Buono 500 Punti', 2, 1);
INSERT INTO `hunter_quest_shop` VALUES (3, 80032, 1, 5000, 'Buono 1000 Punti', 3, 1);
INSERT INTO `hunter_quest_shop` VALUES (4, 50163, 1, 25000, 'Chiave Dimensionale (Forza Baule)', 80, 1);
INSERT INTO `hunter_quest_shop` VALUES (5, 50168, 1, 50000, 'Frammento di Monarca (S-Rank + Focus)', 90, 1);
INSERT INTO `hunter_quest_shop` VALUES (6, 50160, 1, 1000, 'Scanner di Fratture (Evoca Subito)', 10, 1);
INSERT INTO `hunter_quest_shop` VALUES (7, 50162, 1, 2500, 'Focus del Cacciatore (+20% Gloria)', 20, 1);
INSERT INTO `hunter_quest_shop` VALUES (8, 50167, 1, 4000, 'Calibratore (Garantisce Rango C+)', 30, 1);
INSERT INTO `hunter_quest_shop` VALUES (9, 50161, 1, 7500, 'Stabilizzatore di Rango (Scegli Rank)', 40, 1);
INSERT INTO `hunter_quest_shop` VALUES (10, 50165, 1, 10000, 'Segnale d\'Emergenza (Forza Speed Kill)', 50, 1);
INSERT INTO `hunter_quest_shop` VALUES (11, 50164, 1, 12500, 'Sigillo di Conquista (Salta Difesa)', 60, 1);
INSERT INTO `hunter_quest_shop` VALUES (12, 50166, 1, 15000, 'Risonatore di Gruppo (Buff Party)', 70, 1);

-- ----------------------------
-- Table structure for hunter_quest_spawn_types
-- ----------------------------
DROP TABLE IF EXISTS `hunter_quest_spawn_types`;
CREATE TABLE `hunter_quest_spawn_types`  (
  `type_name` varchar(20) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `probability` int NULL DEFAULT 0,
  `is_jackpot` tinyint(1) NULL DEFAULT 0,
  `enabled` tinyint(1) NULL DEFAULT 1,
  PRIMARY KEY (`type_name`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of hunter_quest_spawn_types
-- ----------------------------
INSERT INTO `hunter_quest_spawn_types` VALUES ('BAULE', 150, 0, 1);
INSERT INTO `hunter_quest_spawn_types` VALUES ('BOSS', 650, 0, 1);
INSERT INTO `hunter_quest_spawn_types` VALUES ('JACKPOT', 25, 1, 1);
INSERT INTO `hunter_quest_spawn_types` VALUES ('SUPER_METIN', 300, 0, 1);

-- ----------------------------
-- Table structure for hunter_quest_spawns
-- ----------------------------
DROP TABLE IF EXISTS `hunter_quest_spawns`;
CREATE TABLE `hunter_quest_spawns`  (
  `spawn_id` int NOT NULL AUTO_INCREMENT,
  `vnum` int NOT NULL,
  `name` varchar(50) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL,
  `type_name` varchar(20) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL,
  `min_level` int NULL DEFAULT 1,
  `max_level` int NULL DEFAULT 250,
  `base_points` int NULL DEFAULT 100,
  `rank_color` varchar(16) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL DEFAULT 'PURPLE',
  `rank_tier` int NOT NULL DEFAULT 1 COMMENT '1=E, 2=D, 3=C, 4=B, 5=A, 6=S, 7=N',
  `enabled` tinyint(1) NULL DEFAULT 1,
  PRIMARY KEY (`spawn_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 30 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of hunter_quest_spawns
-- ----------------------------
INSERT INTO `hunter_quest_spawns` VALUES (1, 63010, 'Metin Lv.45', 'SUPER_METIN', 35, 55, 25, 'GREEN', 1, 1);
INSERT INTO `hunter_quest_spawns` VALUES (2, 63011, 'Metin Lv.60', 'SUPER_METIN', 50, 70, 35, 'GREEN', 2, 1);
INSERT INTO `hunter_quest_spawns` VALUES (3, 63012, 'Metin Lv.75', 'SUPER_METIN', 65, 85, 50, 'BLUE', 2, 1);
INSERT INTO `hunter_quest_spawns` VALUES (4, 63013, 'Metin Lv.90', 'SUPER_METIN', 80, 100, 65, 'BLUE', 3, 1);
INSERT INTO `hunter_quest_spawns` VALUES (5, 63014, 'Metin Lv.95', 'SUPER_METIN', 85, 105, 80, 'ORANGE', 3, 1);
INSERT INTO `hunter_quest_spawns` VALUES (6, 63015, 'Metin Lv.115', 'SUPER_METIN', 105, 125, 100, 'ORANGE', 4, 1);
INSERT INTO `hunter_quest_spawns` VALUES (7, 63016, 'Metin Lv.135', 'SUPER_METIN', 125, 150, 125, 'RED', 4, 1);
INSERT INTO `hunter_quest_spawns` VALUES (8, 63017, 'Metin Lv.165', 'SUPER_METIN', 150, 180, 155, 'GOLD', 5, 1);
INSERT INTO `hunter_quest_spawns` VALUES (9, 63018, 'Metin Lv.200', 'SUPER_METIN', 180, 250, 190, 'PURPLE', 6, 1);
INSERT INTO `hunter_quest_spawns` VALUES (10, 4035, 'Funglash', 'BOSS', 65, 85, 10, 'GREEN', 1, 1);
INSERT INTO `hunter_quest_spawns` VALUES (11, 719, 'Thaloren', 'BOSS', 85, 105, 12, 'BLUE', 2, 1);
INSERT INTO `hunter_quest_spawns` VALUES (12, 2771, 'Yinlee', 'BOSS', 90, 110, 15, 'BLUE', 3, 1);
INSERT INTO `hunter_quest_spawns` VALUES (13, 768, 'Slubina', 'BOSS', 105, 125, 18, 'ORANGE', 3, 1);
INSERT INTO `hunter_quest_spawns` VALUES (14, 6790, 'Alastor', 'BOSS', 115, 135, 22, 'ORANGE', 4, 1);
INSERT INTO `hunter_quest_spawns` VALUES (15, 6831, 'Grimlor', 'BOSS', 125, 145, 28, 'RED', 4, 1);
INSERT INTO `hunter_quest_spawns` VALUES (16, 986, 'Branzhul', 'BOSS', 140, 160, 35, 'RED', 5, 1);
INSERT INTO `hunter_quest_spawns` VALUES (17, 989, 'Torgal', 'BOSS', 155, 175, 42, 'GOLD', 5, 1);
INSERT INTO `hunter_quest_spawns` VALUES (18, 4011, 'Nerzakar', 'BOSS', 175, 195, 50, 'GOLD', 6, 1);
INSERT INTO `hunter_quest_spawns` VALUES (19, 6830, 'Nozzera', 'BOSS', 190, 210, 60, 'PURPLE', 6, 1);
INSERT INTO `hunter_quest_spawns` VALUES (20, 4385, 'Velzahar', 'BOSS', 200, 250, 80, 'BLACKWHITE', 7, 1);
INSERT INTO `hunter_quest_spawns` VALUES (21, 63000, 'Cassa E-Rank', 'BAULE', 1, 250, 8, 'GREEN', 1, 1);
INSERT INTO `hunter_quest_spawns` VALUES (22, 63001, 'Cassa D-Rank', 'BAULE', 1, 250, 12, 'BLUE', 2, 1);
INSERT INTO `hunter_quest_spawns` VALUES (23, 63002, 'Cassa C-Rank', 'BAULE', 1, 250, 18, 'ORANGE', 3, 1);
INSERT INTO `hunter_quest_spawns` VALUES (24, 63003, 'Cassa B-Rank', 'BAULE', 1, 250, 25, 'RED', 4, 1);
INSERT INTO `hunter_quest_spawns` VALUES (25, 63004, 'Cassa A-Rank', 'BAULE', 1, 250, 35, 'PURPLE', 5, 1);
INSERT INTO `hunter_quest_spawns` VALUES (26, 63005, 'Cassa S-Rank', 'BAULE', 1, 250, 50, 'GOLD', 6, 1);
INSERT INTO `hunter_quest_spawns` VALUES (27, 63006, 'Cassa N-Rank', 'BAULE', 1, 250, 70, 'BLACKWHITE', 7, 1);
INSERT INTO `hunter_quest_spawns` VALUES (28, 63007, 'Cassa ???-Rank', 'BAULE', 1, 250, 90, 'PURPLE', 7, 1);
INSERT INTO `hunter_quest_spawns` VALUES (29, 63019, 'Metin Lv.???', 'SUPER_METIN', 180, 250, 300, 'BLACKWHITE', 7, 1);

-- ----------------------------
-- Table structure for hunter_quest_tips
-- ----------------------------
DROP TABLE IF EXISTS `hunter_quest_tips`;
CREATE TABLE `hunter_quest_tips`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `tip_text` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 31 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of hunter_quest_tips
-- ----------------------------
INSERT INTO `hunter_quest_tips` VALUES (1, 'Attenzione: Quando apri una Frattura, le tue coordinate vengono svelate a tutto il server!');
INSERT INTO `hunter_quest_tips` VALUES (2, 'Non esiste onore nella caccia: rubare il Boss a un altro giocatore e una strategia valida.');
INSERT INTO `hunter_quest_tips` VALUES (3, 'Chi infligge il maggior danno al Boss si aggiudica il bottino e i Punti Gloria.');
INSERT INTO `hunter_quest_tips` VALUES (4, 'Se vedi un avviso di spawn vicino a te, corri! Potresti rubare un Super Metin.');
INSERT INTO `hunter_quest_tips` VALUES (5, 'La Top 3 della Classifica Settimanale riceve Monete Drago (DR). Dacci dentro!');
INSERT INTO `hunter_quest_tips` VALUES (6, 'SPEED KILL: Uccidi il Boss entro 60 secondi per RADDOPPIARE i punti ottenuti!');
INSERT INTO `hunter_quest_tips` VALUES (7, 'Per i Super Metin hai 5 minuti di tempo per ottenere il bonus Speed Kill (x2 Punti).');
INSERT INTO `hunter_quest_tips` VALUES (8, 'Consiglio: Attiva i buff e le rugiade PRIMA di cliccare sulla Frattura.');
INSERT INTO `hunter_quest_tips` VALUES (9, 'Non spezzare la catena! Logga ogni giorno per un bonus punti passivo fino al +20%.');
INSERT INTO `hunter_quest_tips` VALUES (10, 'Hai perso la streak di login? Dovrai ricominciare da zero per riavere il bonus.');
INSERT INTO `hunter_quest_tips` VALUES (11, 'I Punti Gloria sono una valuta preziosa. Spendili con saggezza nel menu (N).');
INSERT INTO `hunter_quest_tips` VALUES (12, 'Il Mercante Hunter in Capitale vende oggetti esclusivi non presenti nel menu rapido.');
INSERT INTO `hunter_quest_tips` VALUES (13, 'I prezzi del Mercante potrebbero cambiare o apparire offerte speciali. Controllalo spesso.');
INSERT INTO `hunter_quest_tips` VALUES (14, 'Puoi convertire i tuoi punti in Item, ma ricorda: scalare la classifica da prestigio.');
INSERT INTO `hunter_quest_tips` VALUES (15, 'I Buoni Punti trovati nei bauli sono commerciabili? Scoprilo provando a scambiarli!');
INSERT INTO `hunter_quest_tips` VALUES (16, 'Controlla spesso il menu Traguardi (tasto N): ci sono premi che aspettano solo di essere riscossi.');
INSERT INTO `hunter_quest_tips` VALUES (17, 'Esistono due vie per i traguardi: la Via del Sangue (Kill) e la Via della Gloria (Punti).');
INSERT INTO `hunter_quest_tips` VALUES (18, 'Sbloccare il titolo Monarca nei traguardi garantisce una ricompensa leggendaria.');
INSERT INTO `hunter_quest_tips` VALUES (19, 'Anche aprire le Fratture conta per le statistiche del tuo Profilo Cacciatore.');
INSERT INTO `hunter_quest_tips` VALUES (20, 'Le Fratture Rosse (Red Gates) sono molto rare ma hanno un drop rate aumentato.');
INSERT INTO `hunter_quest_tips` VALUES (21, 'Un Red Gate puo spawnare Boss molto piu forti del normale. Non sottovalutarli.');
INSERT INTO `hunter_quest_tips` VALUES (22, 'Se una Frattura evoca un Baule del Tesoro, considerati fortunato: e un Jackpot!');
INSERT INTO `hunter_quest_tips` VALUES (23, 'I Bauli Dimensionali possono contenere Buoni DR (Monete Drago).');
INSERT INTO `hunter_quest_tips` VALUES (24, 'Piu mostri uccidi nel mondo, piu alta e la probabilita che appaia una Frattura.');
INSERT INTO `hunter_quest_tips` VALUES (25, 'Solo i veri Cacciatori sopravvivono ai Dungeon Break.');
INSERT INTO `hunter_quest_tips` VALUES (26, 'Il sistema Hunter premia la costanza, non solo la forza bruta.');
INSERT INTO `hunter_quest_tips` VALUES (27, 'Si narra che alcuni Boss Elite nascondano segreti antichi...');
INSERT INTO `hunter_quest_tips` VALUES (28, 'Il reset Giornaliero avviene ogni notte. Assicurati di aver massimizzato il punteggio.');
INSERT INTO `hunter_quest_tips` VALUES (29, 'Guardati le spalle mentre combatti un Boss... un nemico potrebbe essere in agguato.');
INSERT INTO `hunter_quest_tips` VALUES (30, 'Vuoi vedere il tuo nome in cima a tutti? Premi N e scala la Sala delle Leggende.');

-- ----------------------------
-- Table structure for hunter_rank_trials
-- ----------------------------
DROP TABLE IF EXISTS `hunter_rank_trials`;
CREATE TABLE `hunter_rank_trials`  (
  `trial_id` int NOT NULL AUTO_INCREMENT,
  `from_rank` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'Rank attuale',
  `to_rank` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'Rank obiettivo',
  `trial_name` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `trial_description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL,
  `required_gloria` int NOT NULL DEFAULT 0,
  `required_level` int NOT NULL DEFAULT 1,
  `required_boss_kills` int NOT NULL DEFAULT 0,
  `boss_vnum_list` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'Lista VNUM separati da virgola, NULL=qualsiasi boss',
  `required_metin_kills` int NOT NULL DEFAULT 0,
  `metin_vnum_list` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'Lista VNUM, NULL=qualsiasi metin',
  `required_fracture_seals` int NOT NULL DEFAULT 0,
  `fracture_color_list` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'Colori fratture, NULL=qualsiasi',
  `required_chest_opens` int NOT NULL DEFAULT 0,
  `chest_vnum_list` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'VNUM bauli, NULL=qualsiasi',
  `required_daily_missions` int NOT NULL DEFAULT 0,
  `required_daily_streaks` int NOT NULL DEFAULT 0,
  `time_limit_hours` int NULL DEFAULT NULL COMMENT 'NULL = nessun limite',
  `gloria_reward` int NOT NULL DEFAULT 0,
  `title_reward` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `item_reward_vnum` int NULL DEFAULT NULL,
  `item_reward_count` int NULL DEFAULT 1,
  `color_code` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'BLUE',
  `enabled` tinyint(1) NOT NULL DEFAULT 1,
  PRIMARY KEY (`trial_id`) USING BTREE,
  UNIQUE INDEX `unique_rank_transition`(`from_rank` ASC, `to_rank` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of hunter_rank_trials
-- ----------------------------
INSERT INTO `hunter_rank_trials` VALUES (1, 'E', 'D', 'Prova del Risvegliato', 'Dimostra di essere degno del rango D. Uccidi boss di basso livello e sigilla fratture primordiali.', 2000, 35, 3, '4035', 6, '4700,4701', 0, 'GREEN', 0, '63000', 0, 0, NULL, 500, NULL, NULL, 1, 'GREEN', 1);
INSERT INTO `hunter_rank_trials` VALUES (2, 'D', 'C', 'Prova del Cacciatore', 'Caccia boss più potenti e affronta fratture astrali. Solo i veri cacciatori sopravvivono.', 10000, 55, 5, '4035,719,2771', 10, '4701,4702,4703', 5, 'GREEN,BLUE', 5, NULL, 0, 0, NULL, 1000, NULL, NULL, 1, 'BLUE', 1);
INSERT INTO `hunter_rank_trials` VALUES (3, 'C', 'B', 'Prova del Veterano', 'Affronta le creature più pericolose. Solo i veterani possono aspirare al rango B.', 50000, 75, 10, '719,2771,768,6790', 20, '4702,4703,4704', 10, 'BLUE,ORANGE', 0, NULL, 15, 0, NULL, 2000, NULL, NULL, 1, 'ORANGE', 1);
INSERT INTO `hunter_rank_trials` VALUES (4, 'B', 'A', 'Risveglio Interiore', 'Il tuo potere interiore deve risvegliarsi. Affronta boss leggendari e fratture cremisi.', 150000, 95, 15, '6831,986,989', 30, '4704,4705,4706', 15, 'ORANGE,RED', 0, NULL, 0, 7, 168, 5000, NULL, NULL, 1, 'RED', 1);
INSERT INTO `hunter_rank_trials` VALUES (5, 'A', 'S', 'Ascensione Leggendaria', 'Solo i più potenti possono diventare leggende. Questa prova è brutale.', 500000, 115, 25, '989,4011,6830', 50, '4706,4707,4708', 25, 'RED,GOLD', 0, NULL, 0, 14, 336, 15000, 'Leggenda Vivente', NULL, 1, 'GOLD', 1);
INSERT INTO `hunter_rank_trials` VALUES (6, 'S', 'N', 'Il Giudizio Finale', 'La prova definitiva. Solo coloro che trascendono i limiti mortali possono diventare NATIONAL.', 1500000, 140, 50, '4011,6830,4385', 100, '4707,4708', 50, 'GOLD,PURPLE,BLACKWHITE', 20, '63003', 0, 30, 720, 50000, 'Monarca Nazionale', NULL, 1, 'BLACKWHITE', 1);

-- ----------------------------
-- Table structure for hunter_ranks
-- ----------------------------
DROP TABLE IF EXISTS `hunter_ranks`;
CREATE TABLE `hunter_ranks`  (
  `rank_id` int NOT NULL AUTO_INCREMENT,
  `rank_code` varchar(5) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `rank_name` varchar(30) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `rank_title` varchar(50) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `min_points` int NULL DEFAULT 0,
  `max_points` int NULL DEFAULT 999999999,
  `color_hex` varchar(10) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT 'FF808080',
  `bonus_gloria` int NULL DEFAULT 0,
  `bonus_drop` int NULL DEFAULT 0,
  `rank_order` int NULL DEFAULT 0,
  PRIMARY KEY (`rank_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 9 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of hunter_ranks
-- ----------------------------
INSERT INTO `hunter_ranks` VALUES (1, 'E', 'E-Rank', 'Risvegliato', 0, 2000, 'FF808080', 0, 0, 1);
INSERT INTO `hunter_ranks` VALUES (2, 'D', 'D-Rank', 'Apprendista', 2000, 10000, 'FF00AA00', 2, 0, 2);
INSERT INTO `hunter_ranks` VALUES (3, 'C', 'C-Rank', 'Cacciatore', 10000, 50000, 'FF00CCFF', 4, 0, 3);
INSERT INTO `hunter_ranks` VALUES (4, 'B', 'B-Rank', 'Veterano', 50000, 150000, 'FF0066FF', 6, 0, 4);
INSERT INTO `hunter_ranks` VALUES (5, 'A', 'A-Rank', 'Maestro', 150000, 500000, 'FFAA00FF', 9, 0, 5);
INSERT INTO `hunter_ranks` VALUES (6, 'S', 'S-Rank', 'Leggenda', 500000, 1500000, 'FFFF6600', 13, 0, 6);
INSERT INTO `hunter_ranks` VALUES (7, 'N', 'NATIONAL', 'Monarca Nazionale', 1500000, 5000000, 'FFFF0000', 18, 0, 7);
INSERT INTO `hunter_ranks` VALUES (8, '?', '???', 'Trascendente', 5000000, 999999999, 'FFFFFFFF', 35, 0, 8);

-- ----------------------------
-- Table structure for hunter_scheduled_events
-- ----------------------------
DROP TABLE IF EXISTS `hunter_scheduled_events`;
CREATE TABLE `hunter_scheduled_events`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `event_name` varchar(100) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `event_type` varchar(50) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `event_desc` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL,
  `start_hour` tinyint NOT NULL DEFAULT 0,
  `start_minute` tinyint NOT NULL DEFAULT 0,
  `duration_minutes` smallint NOT NULL DEFAULT 30,
  `days_active` varchar(20) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL DEFAULT '1,2,3,4,5,6,7',
  `min_rank` char(1) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL DEFAULT 'E',
  `reward_glory_base` int NOT NULL DEFAULT 50,
  `reward_glory_winner` int NOT NULL DEFAULT 200,
  `color_scheme` varchar(20) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT 'GOLD',
  `priority` tinyint NULL DEFAULT 5,
  `enabled` tinyint(1) NULL DEFAULT 1,
  `created_at` timestamp NULL DEFAULT current_timestamp,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_enabled`(`enabled` ASC) USING BTREE,
  INDEX `idx_start_hour`(`start_hour` ASC) USING BTREE,
  INDEX `idx_days_active`(`days_active` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 30 CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of hunter_scheduled_events
-- ----------------------------
INSERT INTO `hunter_scheduled_events` VALUES (1, 'Alba del Cacciatore', 'glory_rush', 'Gloria x2 per ogni uccisione! Svegliati e guadagna!', 5, 0, 60, '1,2,3,4,5,6,7', 'E', 20, 100, 'GOLD', 5, 1, '2025-12-24 16:44:17');
INSERT INTO `hunter_scheduled_events` VALUES (2, 'Prima Frattura', 'first_rift', 'Chi trova PER PRIMO la Frattura dellAlba vince!', 6, 0, 30, '1,2,3,4,5,6,7', 'E', 50, 300, 'PURPLE', 6, 1, '2025-12-24 16:44:17');
INSERT INTO `hunter_scheduled_events` VALUES (3, 'Risveglio dei Boss', 'first_boss', 'Boss Mattutino spawna! Chi lo uccide PER PRIMO?', 7, 0, 30, '1,2,3,4,5,6,7', 'D', 60, 350, 'RED', 6, 1, '2025-12-24 16:44:17');
INSERT INTO `hunter_scheduled_events` VALUES (4, 'Caccia alle Fratture', 'fracture_hunter', 'Chi sigilla PIU fratture in 20 minuti vince!', 8, 0, 20, '1,2,3,4,5,6,7', 'E', 40, 250, 'PURPLE', 5, 1, '2025-12-26 12:00:00');
INSERT INTO `hunter_scheduled_events` VALUES (5, 'Caccia ai Bauli', 'chest_hunter', 'Chi apre PIU bauli in 20 minuti vince!', 9, 0, 20, '1,2,3,4,5,6,7', 'E', 35, 200, 'GOLD', 5, 1, '2025-12-26 12:00:00');
INSERT INTO `hunter_scheduled_events` VALUES (6, 'Caccia ai Boss', 'boss_hunter', 'Chi uccide PIU boss in 20 minuti vince!', 10, 0, 20, '1,2,3,4,5,6,7', 'D', 70, 400, 'RED', 6, 1, '2025-12-26 12:00:00');
INSERT INTO `hunter_scheduled_events` VALUES (7, 'Gloria Rush Mezzogiorno', 'glory_rush', 'GLORIA x2 per TUTTO! Farming intensivo!', 11, 30, 30, '1,2,3,4,5,6,7', 'E', 25, 120, 'GOLD', 6, 1, '2025-12-24 16:44:17');
INSERT INTO `hunter_scheduled_events` VALUES (8, 'Frattura del Mezzogiorno', 'first_rift', 'Frattura Dorata! Il PRIMO che la trova vince GROSSO!', 12, 0, 25, '1,2,3,4,5,6,7', 'C', 100, 600, 'GOLD', 8, 1, '2025-12-24 16:44:17');
INSERT INTO `hunter_scheduled_events` VALUES (9, 'Caccia al Boss Leggendario', 'first_boss', 'Boss Leggendario spawna! Chi lo abbatte PER PRIMO?', 12, 30, 30, '1,2,3,4,5,6,7', 'C', 120, 700, 'RED', 9, 1, '2025-12-24 16:44:17');
INSERT INTO `hunter_scheduled_events` VALUES (10, 'Caccia ai Metin', 'metin_hunter', 'Chi distrugge PIU metin in 20 minuti vince!', 13, 0, 20, '1,2,3,4,5,6,7', 'E', 30, 180, 'ORANGE', 5, 1, '2025-12-26 12:00:00');
INSERT INTO `hunter_scheduled_events` VALUES (11, 'Gloria Rush Pomeriggio', 'glory_rush', 'GLORIA x2 per TUTTO! Continua a farmare!', 14, 30, 30, '1,2,3,4,5,6,7', 'E', 25, 120, 'GOLD', 6, 1, '2025-12-26 12:00:00');
INSERT INTO `hunter_scheduled_events` VALUES (12, 'Frattura Pomeridiana', 'first_rift', 'Frattura Epica! Trovala PRIMA degli altri!', 15, 0, 30, '1,2,3,4,5,6,7', 'B', 150, 900, 'PURPLE', 8, 1, '2025-12-26 12:00:00');
INSERT INTO `hunter_scheduled_events` VALUES (13, 'Boss Elite Hunt', 'first_boss', 'Boss Elite spawna! Chi lo uccide PER PRIMO?', 15, 30, 30, '1,2,3,4,5,6,7', 'B', 180, 1000, 'RED', 9, 1, '2025-12-26 12:00:00');
INSERT INTO `hunter_scheduled_events` VALUES (14, 'Gloria Rush Sera', 'glory_rush', 'GLORIA x3 per 45 minuti! FARMING MASSIMO!', 18, 30, 45, '1,2,3,4,5,6,7', 'D', 50, 200, 'GOLD', 8, 1, '2025-12-24 16:44:17');
INSERT INTO `hunter_scheduled_events` VALUES (15, 'Frattura della Sera', 'first_rift', 'Frattura della Sera! Trovala per prima!', 19, 0, 30, '1,2,3,4,5,6,7', 'A', 200, 1200, 'GOLD', 10, 1, '2025-12-26 12:00:00');
INSERT INTO `hunter_scheduled_events` VALUES (16, 'MEGA Boss Hunt', 'first_boss', 'MEGA BOSS spawna! Chi lo uccide PRIMO?', 19, 30, 30, '1,2,3,4,5,6,7', 'A', 250, 1500, 'RED', 10, 1, '2025-12-24 16:44:17');
INSERT INTO `hunter_scheduled_events` VALUES (17, 'Frattura Notturna', 'first_rift', 'Frattura dellOmbra appare SOLO di notte! Trovala!', 22, 0, 30, '1,2,3,4,5,6,7', 'A', 180, 1100, 'PURPLE', 10, 1, '2025-12-24 16:44:17');
INSERT INTO `hunter_scheduled_events` VALUES (18, 'Boss Notturno Leggendario', 'first_boss', 'BOSS NOTTURNO! Appare solo a mezzanotte!', 22, 30, 30, '1,2,3,4,5,6,7', 'S', 300, 1800, 'RED', 10, 1, '2025-12-24 16:44:17');
INSERT INTO `hunter_scheduled_events` VALUES (19, 'Gloria Notturna x4', 'glory_rush', 'GLORIA x4! Solo per chi resta sveglio!', 1, 30, 60, '1,2,3,4,5,6,7', 'C', 40, 250, 'GOLD', 8, 1, '2025-12-24 16:44:17');
INSERT INTO `hunter_scheduled_events` VALUES (20, 'Frattura del Giudizio', 'first_rift', 'Frattura FINALE della notte! Premio MASSIMO!', 1, 0, 30, '1,2,3,4,5,6,7', 'A', 200, 1300, 'PURPLE', 10, 1, '2025-12-24 16:44:17');
INSERT INTO `hunter_scheduled_events` VALUES (21, 'Boss Prima dellAlba', 'first_boss', 'Ultimo Boss prima dellalba! Chi lo uccide?', 4, 15, 30, '1,2,3,4,5,6,7', 'C', 70, 450, 'RED', 7, 1, '2025-12-24 16:44:17');
INSERT INTO `hunter_scheduled_events` VALUES (22, 'Sabato Gloria x3', 'glory_rush', 'WEEKEND! Gloria TRIPLA tutto il giorno!', 10, 0, 120, '6', 'E', 30, 150, 'GOLD', 8, 1, '2025-12-24 16:44:17');
INSERT INTO `hunter_scheduled_events` VALUES (23, 'Sabato Frattura Dorata', 'first_rift', 'Frattura DORATA del weekend! Premio x2!', 11, 0, 30, '6', 'C', 150, 900, 'GOLD', 9, 1, '2025-12-24 16:44:17');
INSERT INTO `hunter_scheduled_events` VALUES (24, 'WORLD BOSS Sabato', 'first_boss', 'WORLD BOSS SETTIMANALE! Chi lo uccide?', 20, 0, 60, '6', 'S', 400, 3000, 'RED', 10, 1, '2025-12-24 16:44:17');
INSERT INTO `hunter_scheduled_events` VALUES (25, 'Notte Sabato - Tutto x4', 'glory_rush', 'GLORIA x4 tutta la notte di sabato!', 22, 0, 120, '6', 'D', 50, 300, 'GOLD', 9, 1, '2025-12-24 16:44:17');
INSERT INTO `hunter_scheduled_events` VALUES (26, 'Domenica Relax Gloria x2', 'glory_rush', 'Domenica tranquilla con Gloria x2!', 9, 0, 180, '7', 'E', 25, 120, 'GOLD', 7, 1, '2025-12-24 16:44:17');
INSERT INTO `hunter_scheduled_events` VALUES (27, 'Frattura Domenicale', 'first_rift', 'Frattura della Domenica! Trovala!', 18, 0, 30, '7', 'S', 350, 2500, 'PURPLE', 10, 1, '2025-12-24 16:44:17');
INSERT INTO `hunter_scheduled_events` VALUES (28, 'BOSS FINALE SETTIMANALE', 'first_boss', 'IL BOSS PIU FORTE! Chi lo abbatte?', 20, 0, 60, '7', 'S', 500, 4000, 'RED', 10, 1, '2025-12-24 16:44:17');
INSERT INTO `hunter_scheduled_events` VALUES (29, 'Countdown Settimana', 'glory_rush', 'Ultime ore! Gloria x5!', 22, 0, 120, '7', 'E', 60, 350, 'GOLD', 10, 1, '2025-12-24 16:44:17');

-- ----------------------------
-- Table structure for hunter_security_logs
-- ----------------------------
DROP TABLE IF EXISTS `hunter_security_logs`;
CREATE TABLE `hunter_security_logs`  (
  `log_id` bigint NOT NULL AUTO_INCREMENT,
  `player_id` int NOT NULL,
  `player_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `log_type` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'SPAWN, DEFENSE, REWARD, KILL, FRACTURE, CHEST, GLORY, SUSPICIOUS',
  `severity` enum('INFO','WARNING','ALERT','CRITICAL') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'INFO',
  `action` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'Azione eseguita',
  `details` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT 'Dettagli JSON',
  `map_index` int NULL DEFAULT 0,
  `position_x` int NULL DEFAULT 0,
  `position_y` int NULL DEFAULT 0,
  `ip_address` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp,
  PRIMARY KEY (`log_id`) USING BTREE,
  INDEX `idx_player`(`player_id` ASC, `created_at` ASC) USING BTREE,
  INDEX `idx_type_severity`(`log_type` ASC, `severity` ASC, `created_at` ASC) USING BTREE,
  INDEX `idx_created`(`created_at` ASC) USING BTREE,
  INDEX `idx_severity`(`severity` ASC, `created_at` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of hunter_security_logs
-- ----------------------------

-- ----------------------------
-- Table structure for hunter_suspicious_players
-- ----------------------------
DROP TABLE IF EXISTS `hunter_suspicious_players`;
CREATE TABLE `hunter_suspicious_players`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `player_id` int NOT NULL,
  `player_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `reason` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `alert_count` int NOT NULL DEFAULT 1,
  `first_alert_at` datetime NOT NULL DEFAULT current_timestamp,
  `last_alert_at` datetime NOT NULL DEFAULT current_timestamp,
  `status` enum('MONITORING','WARNED','BANNED') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'MONITORING',
  `notes` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `idx_player`(`player_id` ASC) USING BTREE,
  INDEX `idx_status`(`status` ASC, `alert_count` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of hunter_suspicious_players
-- ----------------------------

-- ----------------------------
-- Table structure for hunter_system_status
-- ----------------------------
DROP TABLE IF EXISTS `hunter_system_status`;
CREATE TABLE `hunter_system_status`  (
  `status_key` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_update` int NOT NULL DEFAULT 0,
  PRIMARY KEY (`status_key`) USING BTREE,
  UNIQUE INDEX `status_key`(`status_key` ASC) USING BTREE
) ENGINE = InnoDB CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of hunter_system_status
-- ----------------------------
INSERT INTO `hunter_system_status` VALUES ('daily_reset', 0);
INSERT INTO `hunter_system_status` VALUES ('weekly_reset', 0);

-- ----------------------------
-- Table structure for hunter_texts
-- ----------------------------
DROP TABLE IF EXISTS `hunter_texts`;
CREATE TABLE `hunter_texts`  (
  `text_key` varchar(64) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `text_value` varchar(500) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `category` varchar(32) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT 'general',
  `color_code` varchar(16) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL DEFAULT NULL,
  `enabled` tinyint(1) NULL DEFAULT 1,
  PRIMARY KEY (`text_key`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = latin1 COLLATE = latin1_swedish_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of hunter_texts
-- ----------------------------
INSERT INTO `hunter_texts` VALUES ('achievements_unlocked', 'TRAGUARDI SBLOCCATI: {COUNT}', 'combat', NULL, 1);
INSERT INTO `hunter_texts` VALUES ('ach_already_claimed', '[!] RICOMPENSA GIA\' RISCOSSA', 'achievement', 'FF0000', 1);
INSERT INTO `hunter_texts` VALUES ('ach_locked', '[!] BLOCCATO - Impegnati di piu\'', 'achievement', '888888', 1);
INSERT INTO `hunter_texts` VALUES ('ach_requirement', 'Requisito: {REQ} {TYPE}', 'achievement', NULL, 1);
INSERT INTO `hunter_texts` VALUES ('ach_reward', 'Ricompensa: x{COUNT} {ITEM}', 'achievement', NULL, 1);
INSERT INTO `hunter_texts` VALUES ('all_missions_bonus', 'BONUS COMPLETAMENTO x1.5!', 'general', NULL, 1);
INSERT INTO `hunter_texts` VALUES ('all_missions_complete', '=== TUTTE LE MISSIONI COMPLETE ===', 'general', NULL, 1);
INSERT INTO `hunter_texts` VALUES ('awaken1_line1', '========================================', 'awaken', '00FFFF', 1);
INSERT INTO `hunter_texts` VALUES ('awaken1_line2', '        ...ANALISI IN CORSO...', 'awaken', 'FFFFFF', 1);
INSERT INTO `hunter_texts` VALUES ('awaken1_line3', '========================================', 'awaken', '00FFFF', 1);
INSERT INTO `hunter_texts` VALUES ('awaken1_speak', '[SYSTEM] SCANSIONE BIOLOGICA IN CORSO...', 'awaken', NULL, 1);
INSERT INTO `hunter_texts` VALUES ('awaken2_line1', '   >> COMPATIBILITA: 100% <<', 'awaken', '00FF00', 1);
INSERT INTO `hunter_texts` VALUES ('awaken2_line2', '   >> REQUISITI: SODDISFATTI <<', 'awaken', '00FF00', 1);
INSERT INTO `hunter_texts` VALUES ('awaken2_speak', '[SYSTEM] COMPATIBILITA CONFERMATA.', 'awaken', NULL, 1);
INSERT INTO `hunter_texts` VALUES ('awaken3_line1', '   NOME: {NAME}', 'awaken', 'FFD700', 1);
INSERT INTO `hunter_texts` VALUES ('awaken3_line2', '   RANGO INIZIALE: [E-RANK]', 'awaken', '808080', 1);
INSERT INTO `hunter_texts` VALUES ('awaken3_speak', '[SYSTEM] NUOVO CACCIATORE REGISTRATO.', 'awaken', NULL, 1);
INSERT INTO `hunter_texts` VALUES ('awaken4_line1', '========================================', 'awaken', 'FF0000', 1);
INSERT INTO `hunter_texts` VALUES ('awaken4_line2', '   !! RISVEGLIO COMPLETATO !!', 'awaken', 'FF6600', 1);
INSERT INTO `hunter_texts` VALUES ('awaken4_line3', '========================================', 'awaken', 'FF0000', 1);
INSERT INTO `hunter_texts` VALUES ('awaken4_speak', 'RISVEGLIO COMPLETATO. BENVENUTO, {NAME}.', 'awaken', NULL, 1);
INSERT INTO `hunter_texts` VALUES ('awaken5_line1', '====================================================', 'awaken', 'FFD700', 1);
INSERT INTO `hunter_texts` VALUES ('awaken5_line10', '   [Y] - Apri Hunter Terminal', 'awaken', '00FF00', 1);
INSERT INTO `hunter_texts` VALUES ('awaken5_line2', '        *** HUNTER SYSTEM v36.0 ATTIVATO ***', 'awaken', '00FFFF', 1);
INSERT INTO `hunter_texts` VALUES ('awaken5_line3', '====================================================', 'awaken', 'FFD700', 1);
INSERT INTO `hunter_texts` VALUES ('awaken5_line4', '   Il Sistema ti ha scelto. Da questo momento:', 'awaken', 'FFFFFF', 1);
INSERT INTO `hunter_texts` VALUES ('awaken5_line5', '   >> Ogni nemico cadra sotto la tua lama', 'awaken', '00FF00', 1);
INSERT INTO `hunter_texts` VALUES ('awaken5_line6', '   >> Ogni vittoria sara registrata', 'awaken', '00FF00', 1);
INSERT INTO `hunter_texts` VALUES ('awaken5_line7', '   >> Ogni rank sara conquistato', 'awaken', '00FF00', 1);
INSERT INTO `hunter_texts` VALUES ('awaken5_line8', '   \'Inizia con un solo passo...\'', 'awaken', 'FFAA00', 1);
INSERT INTO `hunter_texts` VALUES ('awaken5_line9', '   \'Finisci come una Leggenda.\'', 'awaken', 'FFAA00', 1);
INSERT INTO `hunter_texts` VALUES ('boss_appeared', 'PERICOLO: {NAME} E APPARSO!', 'spawn', NULL, 1);
INSERT INTO `hunter_texts` VALUES ('chest_bonus', 'Incredibile! Il baule conteneva anche {POINTS} Gloria!', 'combat', 'FFD700', 1);
INSERT INTO `hunter_texts` VALUES ('chest_detected', 'BAULE DEL TESORO RILEVATO!', 'spawn', 'GOLD', 1);
INSERT INTO `hunter_texts` VALUES ('chest_opened', 'BAULE APERTO: OTTENUTO {ITEM}', 'combat', NULL, 1);
INSERT INTO `hunter_texts` VALUES ('classic_gate_ask', 'Vuoi spezzare il sigillo ed entrare?', 'classic', NULL, 1);
INSERT INTO `hunter_texts` VALUES ('classic_gate_come_back', 'Torna quando sarai piu\' forte o con un Party da 4.', 'classic', NULL, 1);
INSERT INTO `hunter_texts` VALUES ('classic_gate_intro', 'Questo portale emana un\'energia instabile.', 'classic', NULL, 1);
INSERT INTO `hunter_texts` VALUES ('classic_gate_not_worthy', 'Non possiedi abbastanza Gloria per questo Gate.', 'classic', NULL, 1);
INSERT INTO `hunter_texts` VALUES ('classic_gate_party', 'Tuttavia, il tuo Party (4+) puo forzarlo!', 'classic', NULL, 1);
INSERT INTO `hunter_texts` VALUES ('classic_gate_party_can_force', 'Tuttavia, il tuo Party (4+) puo\' forzarlo!', 'classic', NULL, 1);
INSERT INTO `hunter_texts` VALUES ('classic_gate_req', 'Gloria Richiesta: {REQ}', 'classic', 'FF0000', 1);
INSERT INTO `hunter_texts` VALUES ('classic_gate_required', 'Gloria Richiesta: |cffFF0000%d|r', 'classic', NULL, 1);
INSERT INTO `hunter_texts` VALUES ('classic_gate_unworthy', 'Non possiedi abbastanza Gloria per questo Gate.', 'classic', NULL, 1);
INSERT INTO `hunter_texts` VALUES ('classic_gate_weak', 'Torna quando sarai piu forte o con un Party da 4.', 'classic', NULL, 1);
INSERT INTO `hunter_texts` VALUES ('classic_gate_worthy', 'Il tuo Rango Hunter e sufficiente.', 'classic', NULL, 1);
INSERT INTO `hunter_texts` VALUES ('classic_opt_close', 'Chiudi', 'classic', NULL, 1);
INSERT INTO `hunter_texts` VALUES ('classic_opt_force', 'Forza Gate (Raid)', 'classic', NULL, 1);
INSERT INTO `hunter_texts` VALUES ('classic_opt_open', 'Apri Gate', 'classic', NULL, 1);
INSERT INTO `hunter_texts` VALUES ('classic_raid_announce', '|cffFF0000[RAID]|r Il Party di {PLAYER} ha forzato un Gate {RANK}!', 'classic', NULL, 1);
INSERT INTO `hunter_texts` VALUES ('emergency_bonus_item', 'BONUS: {ITEM} x{COUNT}', 'emergency', NULL, 1);
INSERT INTO `hunter_texts` VALUES ('emergency_complete', 'MISSIONE COMPLETATA! +{POINTS} GLORIA', 'emergency', NULL, 1);
INSERT INTO `hunter_texts` VALUES ('emergency_failed', 'MISSIONE FALLITA.', 'emergency', NULL, 1);
INSERT INTO `hunter_texts` VALUES ('event_ended', 'EVENTO TERMINATO: {NAME}', 'event', 'AAAAAA', 1);
INSERT INTO `hunter_texts` VALUES ('event_joined', 'Hai partecipato a {NAME}! +{GLORY} Gloria base', 'event', '00FFFF', 1);
INSERT INTO `hunter_texts` VALUES ('event_started', 'EVENTO INIZIATO: {NAME}! Partecipa ora!', 'event', '00FF00', 1);
INSERT INTO `hunter_texts` VALUES ('event_starting_soon', 'EVENTO IN ARRIVO: {NAME} tra {MINUTES} minuti!', 'event', 'FFD700', 1);
INSERT INTO `hunter_texts` VALUES ('event_winner', 'VINCITORE EVENTO: {NAME} con {POINTS} punti!', 'event', 'FFD700', 1);
INSERT INTO `hunter_texts` VALUES ('fracture_detected', 'ATTENZIONE: FRATTURA {RANK} RILEVATA.', 'fracture', NULL, 1);
INSERT INTO `hunter_texts` VALUES ('fracture_retreat', 'TI ALLONTANI DALLA FRATTURA.', 'fracture', NULL, 1);
INSERT INTO `hunter_texts` VALUES ('fracture_sealed', 'FRATTURA SIGILLATA. +{POINTS} GLORIA', 'fracture', NULL, 1);
INSERT INTO `hunter_texts` VALUES ('fracture_voice_no_BLACKWHITE', 'Non sei pronto per essere giudicato.', 'fracture_voice', 'BLACKWHITE', 1);
INSERT INTO `hunter_texts` VALUES ('fracture_voice_no_BLUE', 'Il cosmo ti rifiuta.', 'fracture_voice', 'BLUE', 1);
INSERT INTO `hunter_texts` VALUES ('fracture_voice_no_GOLD', 'L\'oro non brilla per i deboli.', 'fracture_voice', 'GOLD', 1);
INSERT INTO `hunter_texts` VALUES ('fracture_voice_no_GREEN', 'Non sei ancora degno della natura.', 'fracture_voice', 'GREEN', 1);
INSERT INTO `hunter_texts` VALUES ('fracture_voice_no_ORANGE', 'L\'oscurita ti divorerebbe.', 'fracture_voice', 'ORANGE', 1);
INSERT INTO `hunter_texts` VALUES ('fracture_voice_no_PURPLE', 'Il fato ti ha gia condannato.', 'fracture_voice', 'PURPLE', 1);
INSERT INTO `hunter_texts` VALUES ('fracture_voice_no_RED', 'Troppo debole. Saresti solo cibo.', 'fracture_voice', 'RED', 1);
INSERT INTO `hunter_texts` VALUES ('fracture_voice_ok_BLACKWHITE', 'Il Giudizio Finale ti attende.', 'fracture_voice', 'BLACKWHITE', 1);
INSERT INTO `hunter_texts` VALUES ('fracture_voice_ok_BLUE', 'Le stelle hanno scelto te.', 'fracture_voice', 'BLUE', 1);
INSERT INTO `hunter_texts` VALUES ('fracture_voice_ok_GOLD', 'La gloria attende chi osa.', 'fracture_voice', 'GOLD', 1);
INSERT INTO `hunter_texts` VALUES ('fracture_voice_ok_GREEN', 'L\'energia primordiale ti chiama...', 'fracture_voice', 'GREEN', 1);
INSERT INTO `hunter_texts` VALUES ('fracture_voice_ok_ORANGE', 'L\'abisso ti fissa... e tu fissi l\'abisso.', 'fracture_voice', 'ORANGE', 1);
INSERT INTO `hunter_texts` VALUES ('fracture_voice_ok_PURPLE', 'Il destino e scritto. Cambialo.', 'fracture_voice', 'PURPLE', 1);
INSERT INTO `hunter_texts` VALUES ('fracture_voice_ok_RED', 'Il sangue chiama sangue.', 'fracture_voice', 'RED', 1);
INSERT INTO `hunter_texts` VALUES ('gate_open', 'IL SIGILLO SI SPEZZA. PREPARATI.', 'fracture', NULL, 1);
INSERT INTO `hunter_texts` VALUES ('gate_party_error', 'ERRORE: SERVONO 4 MEMBRI VICINI.', 'fracture', NULL, 1);
INSERT INTO `hunter_texts` VALUES ('gate_party_force', 'IL PARTY FORZA IL SIGILLO!', 'fracture', NULL, 1);
INSERT INTO `hunter_texts` VALUES ('gate_raid_global', '[RAID] Il Party di {NAME} ha forzato un Gate {RANK}!', 'fracture', 'FF0000', 1);
INSERT INTO `hunter_texts` VALUES ('item_received', 'OGGETTO RICEVUTO: {ITEM}', 'shop', NULL, 1);
INSERT INTO `hunter_texts` VALUES ('lv30_line1a', '========================================', 'lv30', '0099FF', 1);
INSERT INTO `hunter_texts` VALUES ('lv30_line1b', '       [ S Y S T E M ]', 'lv30', '0099FF', 1);
INSERT INTO `hunter_texts` VALUES ('lv30_line1c', '========================================', 'lv30', '0099FF', 1);
INSERT INTO `hunter_texts` VALUES ('lv30_line2a', '   HUNTER SYSTEM ATTIVATO', 'lv30', 'FFD700', 1);
INSERT INTO `hunter_texts` VALUES ('lv30_line2b', '   Benvenuto, {NAME}', 'lv30', 'FFFFFF', 1);
INSERT INTO `hunter_texts` VALUES ('lv30_line3a', '   >> Da oggi lotterai per la Gloria!', 'lv30', '00FF00', 1);
INSERT INTO `hunter_texts` VALUES ('lv30_line3b', '   >> Fratture, Classifiche, Tesori...', 'lv30', '00FF00', 1);
INSERT INTO `hunter_texts` VALUES ('lv30_line3c', '   >> Ti attendono.', 'lv30', '00FF00', 1);
INSERT INTO `hunter_texts` VALUES ('lv30_line4a', '   A R I S E', 'lv30', 'FF6600', 1);
INSERT INTO `hunter_texts` VALUES ('lv30_line4b', '   Il tuo viaggio come Hunter inizia ORA.', 'lv30', 'FFFFFF', 1);
INSERT INTO `hunter_texts` VALUES ('lv30_line4c', '   [Y] - Apri Hunter Terminal', 'lv30', '00FFFF', 1);
INSERT INTO `hunter_texts` VALUES ('lv5_line1a', '========================================', 'lv5', 'FF0000', 1);
INSERT INTO `hunter_texts` VALUES ('lv5_line1b', '   ! ! ! ANOMALIA RILEVATA ! ! !', 'lv5', 'FF0000', 1);
INSERT INTO `hunter_texts` VALUES ('lv5_line1c', '========================================', 'lv5', 'FF0000', 1);
INSERT INTO `hunter_texts` VALUES ('lv5_line2a', '   Il Sistema ti ha notato...', 'lv5', '888888', 1);
INSERT INTO `hunter_texts` VALUES ('lv5_line2b', '   Qualcosa si sta risvegliando.', 'lv5', '888888', 1);
INSERT INTO `hunter_texts` VALUES ('lv5_line3a', '   Raggiungi il livello 30...', 'lv5', 'FFD700', 1);
INSERT INTO `hunter_texts` VALUES ('lv5_line3b', '   ...e scoprirai la verita.', 'lv5', 'FFD700', 1);
INSERT INTO `hunter_texts` VALUES ('mission_all_complete', 'TUTTE LE MISSIONI COMPLETE! BONUS x1.5!', 'mission', 'FFD700', 1);
INSERT INTO `hunter_texts` VALUES ('mission_assigned', '< NUOVE MISSIONI ASSEGNATE >', 'mission', '00FFFF', 1);
INSERT INTO `hunter_texts` VALUES ('mission_complete', '< MISSIONE COMPLETATA >', 'mission', '00FF00', 1);
INSERT INTO `hunter_texts` VALUES ('mission_daily_reset', 'Missioni giornaliere resettate!', 'mission', '00FFFF', 1);
INSERT INTO `hunter_texts` VALUES ('mission_failed', '< MISSIONE FALLITA >', 'mission', 'FF0000', 1);
INSERT INTO `hunter_texts` VALUES ('mission_penalty', 'Penalita: -%d Gloria', 'general', NULL, 1);
INSERT INTO `hunter_texts` VALUES ('mission_penalty_applied', 'PENALITA: -{PENALTY} Gloria per missioni non completate', 'mission', 'FF4444', 1);
INSERT INTO `hunter_texts` VALUES ('mission_progress', 'Progresso Missione: %d / %d', 'mission', 'FFFFFF', 1);
INSERT INTO `hunter_texts` VALUES ('mission_reward', 'Ricompensa: +%d Gloria', 'general', NULL, 1);
INSERT INTO `hunter_texts` VALUES ('mission_time_warning', 'ATTENZIONE: {MINUTES} minuti rimasti!', 'mission', 'FFA500', 1);
INSERT INTO `hunter_texts` VALUES ('mission_type_kill_boss', 'Sconfiggi Boss', 'general', NULL, 1);
INSERT INTO `hunter_texts` VALUES ('mission_type_kill_metin', 'Distruggi Metin', 'general', NULL, 1);
INSERT INTO `hunter_texts` VALUES ('mission_type_kill_mob', 'Elimina Mostri', 'general', NULL, 1);
INSERT INTO `hunter_texts` VALUES ('mission_type_seal_fracture', 'Sigilla Fratture', 'general', NULL, 1);
INSERT INTO `hunter_texts` VALUES ('mission_type_speedkill', 'Uccisione Veloce', 'general', NULL, 1);
INSERT INTO `hunter_texts` VALUES ('overtake_congrats', 'CONGRATULAZIONI! SEI NELLA TOP 10 {CATEGORY}!', 'overtake', NULL, 1);
INSERT INTO `hunter_texts` VALUES ('overtake_new_king', '[NUOVO RE] {NAME} ha preso il comando della Classifica {CATEGORY}!', 'overtake', 'FFD700', 1);
INSERT INTO `hunter_texts` VALUES ('overtake_record', '[RECORD] Nuovo Punteggio: {POINTS}!', 'overtake', '00FF00', 1);
INSERT INTO `hunter_texts` VALUES ('overtake_top10', '[TOP 10] {NAME} e entrato nella Top 10 {CATEGORY}!', 'overtake', '00FFFF', 1);
INSERT INTO `hunter_texts` VALUES ('pending_daily_pos', '[DAILY RANK] Posizione: {POS}', 'pending', '00FFFF', 1);
INSERT INTO `hunter_texts` VALUES ('pending_none', 'Nessun premio in attesa al momento.', 'pending', NULL, 1);
INSERT INTO `hunter_texts` VALUES ('pending_rewards', 'RICOMPENSE IN ATTESA. CONTROLLA IL TERMINALE.', 'pending', 'FFD700', 1);
INSERT INTO `hunter_texts` VALUES ('pending_scala', 'Scala la classifica per ottenere gloria!', 'pending', NULL, 1);
INSERT INTO `hunter_texts` VALUES ('pending_weekly_pos', '[WEEKLY RANK] Posizione: {POS}', 'pending', 'FFD700', 1);
INSERT INTO `hunter_texts` VALUES ('rank_refreshed', '[HUNTER] Rank aggiornato: {RANK} ({POINTS} Gloria)', 'system', NULL, 1);
INSERT INTO `hunter_texts` VALUES ('rank_up_global', '[RANK UP] {NAME} e salito al rango [{RANK}-RANK]!', 'rank', 'FFD700', 1);
INSERT INTO `hunter_texts` VALUES ('rank_up_msg', 'RANK UP! Sei ora un {RANK}-RANK Hunter!', 'rank', NULL, 1);
INSERT INTO `hunter_texts` VALUES ('reset_daily', '|cffFFD700[HUNTER SYSTEM]|r Classifica Giornaliera Resettata! La corsa al potere ricomincia.', 'reset', 'FFD700', 1);
INSERT INTO `hunter_texts` VALUES ('reset_weekly', '|cffFF6600[HUNTER SYSTEM]|r Classifica Settimanale Resettata! I premi sono stati distribuiti.', 'reset', 'FF6600', 1);
INSERT INTO `hunter_texts` VALUES ('reward_claimed', '|cffFFD700[HUNTER]|r {PLAYER} ha riscosso il premio Top Classifica {TYPE}!', 'reward', NULL, 1);
INSERT INTO `hunter_texts` VALUES ('reward_claimed_daily', '{NAME} ha riscosso il premio Top Classifica Giornaliera!', 'reward', 'FFD700', 1);
INSERT INTO `hunter_texts` VALUES ('reward_claimed_weekly', '{NAME} ha riscosso il premio Top Classifica Settimanale!', 'reward', 'FFD700', 1);
INSERT INTO `hunter_texts` VALUES ('reward_type_daily', 'Giornaliera', 'reward', NULL, 1);
INSERT INTO `hunter_texts` VALUES ('reward_type_weekly', 'Settimanale', 'reward', NULL, 1);
INSERT INTO `hunter_texts` VALUES ('shop_ask', 'Vuoi acquistare questo oggetto?', 'shop', NULL, 1);
INSERT INTO `hunter_texts` VALUES ('shop_error', 'ERRORE: CREDITI INSUFFICIENTI.', 'shop', NULL, 1);
INSERT INTO `hunter_texts` VALUES ('shop_error_funds', 'ERRORE: CREDITI INSUFFICIENTI.', 'shop', NULL, 1);
INSERT INTO `hunter_texts` VALUES ('shop_opt_cancel', 'Annulla', 'shop', NULL, 1);
INSERT INTO `hunter_texts` VALUES ('shop_opt_confirm', 'Conferma Acquisto', 'shop', NULL, 1);
INSERT INTO `hunter_texts` VALUES ('shop_success', 'TRANSAZIONE COMPLETATA. -{POINTS} CREDITI', 'shop', NULL, 1);
INSERT INTO `hunter_texts` VALUES ('shop_title', 'MERCANTE HUNTER', 'shop', NULL, 1);
INSERT INTO `hunter_texts` VALUES ('spawn_alert_line1', '[HUNTER ALERT] Il Cacciatore {NAME} ha spezzato il sigillo!', 'spawn', 'FF4444', 1);
INSERT INTO `hunter_texts` VALUES ('spawn_alert_line2', 'Un {MOBNAME} ({RANK}) e apparso a ({X}, {Y})!', 'spawn', 'FF0000', 1);
INSERT INTO `hunter_texts` VALUES ('spawn_alert_location', 'Un |cffFF0000{NAME}|r ({RANK}) e\' apparso a ({X}, {Y})!', 'spawn', NULL, 1);
INSERT INTO `hunter_texts` VALUES ('spawn_alert_seal_broken', '|cffFF4444[HUNTER ALERT]|r Il Cacciatore |cffFFD700{PLAYER}|r ha spezzato il sigillo!', 'spawn', NULL, 1);
INSERT INTO `hunter_texts` VALUES ('spawn_boss_appeared', 'PERICOLO: {NAME} E\' APPARSO!', 'spawn', NULL, 1);
INSERT INTO `hunter_texts` VALUES ('spawn_chest_detected', 'BAULE DEL TESORO RILEVATO!', 'spawn', 'GOLD', 1);
INSERT INTO `hunter_texts` VALUES ('target_eliminated', 'BERSAGLIO ELIMINATO: {NAME} | +{POINTS} GLORIA', 'combat', NULL, 1);
INSERT INTO `hunter_texts` VALUES ('welcome_A_border', '====================================================', 'welcome', 'AA00FF', 1);
INSERT INTO `hunter_texts` VALUES ('welcome_A_line1', '   !! ALLERTA !! Maestro A-Rank online !!', 'welcome', 'CC66FF', 1);
INSERT INTO `hunter_texts` VALUES ('welcome_A_line2', '   Il Sistema si inchina al tuo potere.', 'welcome', 'CC66FF', 1);
INSERT INTO `hunter_texts` VALUES ('welcome_A_line3', '   Sei tra i piu forti di questo mondo.', 'welcome', 'CC66FF', 1);
INSERT INTO `hunter_texts` VALUES ('welcome_A_quote', '   \'Quando un Maestro cammina, il mondo trema.\'', 'welcome', 'AA00FF', 1);
INSERT INTO `hunter_texts` VALUES ('welcome_A_stats', '   >> Status: MAESTRO | Autorizzazione: MASSIMA <<', 'welcome', 'AA00FF', 1);
INSERT INTO `hunter_texts` VALUES ('welcome_A_title', '         *** [A-RANK] MAESTRO ***', 'welcome', 'AA00FF', 1);
INSERT INTO `hunter_texts` VALUES ('welcome_B_border', '====================================================', 'welcome', '0066FF', 1);
INSERT INTO `hunter_texts` VALUES ('welcome_B_line1', '   ATTENZIONE: Veterano B-Rank rilevato.', 'welcome', '4488FF', 1);
INSERT INTO `hunter_texts` VALUES ('welcome_B_line2', '   Pochi raggiungono questo livello.', 'welcome', '4488FF', 1);
INSERT INTO `hunter_texts` VALUES ('welcome_B_line3', '   Il Sistema onora il tuo cammino.', 'welcome', '4488FF', 1);
INSERT INTO `hunter_texts` VALUES ('welcome_B_quote', '   \'I deboli temono il buio. I forti lo dominano.\'', 'welcome', '0066FF', 1);
INSERT INTO `hunter_texts` VALUES ('welcome_B_stats', '   >> Status: ELITE | Autorizzazione: ALTA <<', 'welcome', '0066FF', 1);
INSERT INTO `hunter_texts` VALUES ('welcome_B_title', '          ** [B-RANK] VETERANO **', 'welcome', '0066FF', 1);
INSERT INTO `hunter_texts` VALUES ('welcome_C_border', '====================================================', 'welcome', '00FFFF', 1);
INSERT INTO `hunter_texts` VALUES ('welcome_C_line1', '   Benvenuto, Cacciatore Esperto.', 'welcome', '44FFFF', 1);
INSERT INTO `hunter_texts` VALUES ('welcome_C_line2', '   Le tue gesta risuonano nei registri.', 'welcome', '44FFFF', 1);
INSERT INTO `hunter_texts` VALUES ('welcome_C_line3', '   Il Sistema ti riconosce come guerriero.', 'welcome', '44FFFF', 1);
INSERT INTO `hunter_texts` VALUES ('welcome_C_quote', '   \'La forza non e tutto. La volonta lo e.\'', 'welcome', '00FFFF', 1);
INSERT INTO `hunter_texts` VALUES ('welcome_C_stats', '   >> Status: ESPERTO | Missioni: DISPONIBILI <<', 'welcome', '00FFFF', 1);
INSERT INTO `hunter_texts` VALUES ('welcome_C_title', '           * [C-RANK] CACCIATORE *', 'welcome', '00FFFF', 1);
INSERT INTO `hunter_texts` VALUES ('welcome_D_border', '====================================================', 'welcome', '00FF00', 1);
INSERT INTO `hunter_texts` VALUES ('welcome_D_line1', '   Il Sistema rileva la tua crescita.', 'welcome', '44FF44', 1);
INSERT INTO `hunter_texts` VALUES ('welcome_D_line2', '   Non sei piu un semplice risvegliato.', 'welcome', '44FF44', 1);
INSERT INTO `hunter_texts` VALUES ('welcome_D_line3', '   Continua cosi, Cacciatore.', 'welcome', '44FF44', 1);
INSERT INTO `hunter_texts` VALUES ('welcome_D_quote', '   \'Solo chi persevera raggiunge la vetta.\'', 'welcome', '00FF00', 1);
INSERT INTO `hunter_texts` VALUES ('welcome_D_stats', '   >> Status: CRESCITA | Potenziale: ELEVATO <<', 'welcome', '00FF00', 1);
INSERT INTO `hunter_texts` VALUES ('welcome_D_title', '              [D-RANK] APPRENDISTA', 'welcome', '00FF00', 1);
INSERT INTO `hunter_texts` VALUES ('welcome_E_border', '====================================================', 'welcome', '808080', 1);
INSERT INTO `hunter_texts` VALUES ('welcome_E_line1', '   Bentornato nel Sistema, Cacciatore.', 'welcome', 'AAAAAA', 1);
INSERT INTO `hunter_texts` VALUES ('welcome_E_line2', '   La strada e lunga, ma ogni viaggio', 'welcome', 'AAAAAA', 1);
INSERT INTO `hunter_texts` VALUES ('welcome_E_line3', '   inizia con un singolo passo.', 'welcome', 'AAAAAA', 1);
INSERT INTO `hunter_texts` VALUES ('welcome_E_quote', '   \'Il debole di oggi... il forte di domani.\'', 'welcome', '808080', 1);
INSERT INTO `hunter_texts` VALUES ('welcome_E_stats', '   >> Status: ATTIVO | Minacce: IN ATTESA <<', 'welcome', '808080', 1);
INSERT INTO `hunter_texts` VALUES ('welcome_E_title', '              [E-RANK] RISVEGLIATO', 'welcome', '808080', 1);
INSERT INTO `hunter_texts` VALUES ('welcome_N_border', '====================================================', 'welcome', 'FF0000', 1);
INSERT INTO `hunter_texts` VALUES ('welcome_N_line1', '   !!! ALLARME MASSIMO !!! MONARCA ONLINE !!!', 'welcome', 'FF4444', 1);
INSERT INTO `hunter_texts` VALUES ('welcome_N_line2', '   Il Sistema stesso si piega davanti a te.', 'welcome', 'FF4444', 1);
INSERT INTO `hunter_texts` VALUES ('welcome_N_line3', '   Tu sei oltre ogni classificazione.', 'welcome', 'FF4444', 1);
INSERT INTO `hunter_texts` VALUES ('welcome_N_quote', '   \'Io sono il Sistema. Il Sistema sono io.\'', 'welcome', 'FF0000', 1);
INSERT INTO `hunter_texts` VALUES ('welcome_N_stats', '   >> Status: MONARCA | Potere: ASSOLUTO <<', 'welcome', 'FF0000', 1);
INSERT INTO `hunter_texts` VALUES ('welcome_N_title', '     ***** [NATIONAL] MONARCA *****', 'welcome', 'FF0000', 1);
INSERT INTO `hunter_texts` VALUES ('welcome_S_border', '====================================================', 'welcome', 'FF6600', 1);
INSERT INTO `hunter_texts` VALUES ('welcome_S_line1', '   !! EMERGENZA !! S-RANK RILEVATO !!', 'welcome', 'FFAA00', 1);
INSERT INTO `hunter_texts` VALUES ('welcome_S_line2', '   Il Sistema trema davanti a te.', 'welcome', 'FFAA00', 1);
INSERT INTO `hunter_texts` VALUES ('welcome_S_line3', '   Una Leggenda cammina tra i mortali.', 'welcome', 'FFAA00', 1);
INSERT INTO `hunter_texts` VALUES ('welcome_S_quote', '   \'Le leggende non muoiono. Diventano eterne.\'', 'welcome', 'FF6600', 1);
INSERT INTO `hunter_texts` VALUES ('welcome_S_stats', '   >> Status: LEGGENDA | Potere: INCOMMENSURABILE <<', 'welcome', 'FF6600', 1);
INSERT INTO `hunter_texts` VALUES ('welcome_S_title', '        **** [S-RANK] LEGGENDA ****', 'welcome', 'FF6600', 1);
INSERT INTO `hunter_texts` VALUES ('whatif_need_party', 'ERRORE: SERVONO 4 MEMBRI VICINI.', 'whatif', NULL, 1);
INSERT INTO `hunter_texts` VALUES ('whatif_opt1_force', '>> FORZA [Party 4+]', 'whatif', NULL, 1);
INSERT INTO `hunter_texts` VALUES ('whatif_opt1_ok', '>> ATTRAVERSA IL PORTALE', 'whatif', NULL, 1);
INSERT INTO `hunter_texts` VALUES ('whatif_opt2_seal', '|| SIGILLA [+{POINTS} Gloria]', 'whatif', NULL, 1);
INSERT INTO `hunter_texts` VALUES ('whatif_opt3_retreat', '<< INDIETREGGIA', 'whatif', NULL, 1);
INSERT INTO `hunter_texts` VALUES ('whatif_party_force', 'IL PARTY FORZA IL SIGILLO!', 'whatif', NULL, 1);
INSERT INTO `hunter_texts` VALUES ('whatif_retreat', 'TI ALLONTANI DALLA FRATTURA.', 'whatif', NULL, 1);
INSERT INTO `hunter_texts` VALUES ('whatif_sealed', 'FRATTURA SIGILLATA. +{POINTS} GLORIA', 'whatif', NULL, 1);
INSERT INTO `hunter_texts` VALUES ('whatif_seal_break', 'IL SIGILLO SI SPEZZA. PREPARATI.', 'whatif', NULL, 1);
INSERT INTO `hunter_texts` VALUES ('winners_daily_header', '[HUNTER SYSTEM] * VINCITORI CLASSIFICA GIORNALIERA *', 'winners', '00FFFF', 1);
INSERT INTO `hunter_texts` VALUES ('winners_medal_1', '[1]', 'winners', 'FFD700', 1);
INSERT INTO `hunter_texts` VALUES ('winners_medal_2', '[2]', 'winners', 'C0C0C0', 1);
INSERT INTO `hunter_texts` VALUES ('winners_medal_3', '[3]', 'winners', 'CD7F32', 1);
INSERT INTO `hunter_texts` VALUES ('winners_score', '{NAME} - {POINTS} Gloria', 'winners', 'FFFFFF', 1);
INSERT INTO `hunter_texts` VALUES ('winners_separator', '======================================', 'winners', 'FFD700', 1);
INSERT INTO `hunter_texts` VALUES ('winners_separator_weekly', '======================================', 'winners', 'FF6600', 1);
INSERT INTO `hunter_texts` VALUES ('winners_sep_daily', '|cffFFD700======================================|r', 'winners', NULL, 1);
INSERT INTO `hunter_texts` VALUES ('winners_sep_weekly', '|cffFF6600======================================|r', 'winners', NULL, 1);
INSERT INTO `hunter_texts` VALUES ('winners_title_daily', '|cffFFD700[HUNTER SYSTEM]|r |cff00FFFF* VINCITORI CLASSIFICA GIORNALIERA *|r', 'winners', NULL, 1);
INSERT INTO `hunter_texts` VALUES ('winners_title_weekly', '|cffFF6600[HUNTER SYSTEM]|r |cffFFD700** VINCITORI CLASSIFICA SETTIMANALE **|r', 'winners', NULL, 1);
INSERT INTO `hunter_texts` VALUES ('winners_weekly_header', '[HUNTER SYSTEM] ** VINCITORI CLASSIFICA SETTIMANALE **', 'winners', 'FFD700', 1);

-- ----------------------------
-- View structure for v_hunter_daily_summary
-- ----------------------------
DROP VIEW IF EXISTS `v_hunter_daily_summary`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `v_hunter_daily_summary` AS select `hunter_security_logs`.`player_id` AS `player_id`,`hunter_security_logs`.`player_name` AS `player_name`,cast(`hunter_security_logs`.`created_at` as date) AS `log_date`,count(0) AS `total_logs`,sum(case when `hunter_security_logs`.`severity` = 'INFO' then 1 else 0 end) AS `info_count`,sum(case when `hunter_security_logs`.`severity` = 'WARNING' then 1 else 0 end) AS `warning_count`,sum(case when `hunter_security_logs`.`severity` = 'ALERT' then 1 else 0 end) AS `alert_count`,sum(case when `hunter_security_logs`.`severity` = 'CRITICAL' then 1 else 0 end) AS `critical_count`,sum(case when `hunter_security_logs`.`log_type` = 'SPAWN' then 1 else 0 end) AS `spawn_logs`,sum(case when `hunter_security_logs`.`log_type` = 'DEFENSE' then 1 else 0 end) AS `defense_logs`,sum(case when `hunter_security_logs`.`log_type` = 'REWARD' then 1 else 0 end) AS `reward_logs`,sum(case when `hunter_security_logs`.`log_type` = 'GLORY' then 1 else 0 end) AS `glory_logs` from `hunter_security_logs` group by `hunter_security_logs`.`player_id`,`hunter_security_logs`.`player_name`,cast(`hunter_security_logs`.`created_at` as date);

-- ----------------------------
-- View structure for v_hunter_suspicious_activity
-- ----------------------------
DROP VIEW IF EXISTS `v_hunter_suspicious_activity`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `v_hunter_suspicious_activity` AS select `l`.`log_id` AS `log_id`,`l`.`player_id` AS `player_id`,`l`.`player_name` AS `player_name`,`l`.`log_type` AS `log_type`,`l`.`severity` AS `severity`,`l`.`action` AS `action`,`l`.`details` AS `details`,`l`.`map_index` AS `map_index`,`l`.`position_x` AS `position_x`,`l`.`position_y` AS `position_y`,`l`.`created_at` AS `created_at`,`s`.`alert_count` AS `alert_count`,`s`.`status` AS `player_status` from (`hunter_security_logs` `l` left join `hunter_suspicious_players` `s` on(`l`.`player_id` = `s`.`player_id`)) where `l`.`severity` in ('WARNING','ALERT','CRITICAL') order by `l`.`created_at` desc;

-- ----------------------------
-- View structure for v_missions_by_rank
-- ----------------------------
DROP VIEW IF EXISTS `v_missions_by_rank`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `v_missions_by_rank` AS select `hunter_mission_definitions`.`mission_id` AS `id`,`hunter_mission_definitions`.`mission_name` AS `mission_name`,`hunter_mission_definitions`.`mission_name` AS `mission_desc`,`hunter_mission_definitions`.`mission_type` AS `mission_type`,`hunter_mission_definitions`.`min_rank` AS `min_rank`,`hunter_mission_definitions`.`target_vnum` AS `target_vnum`,`hunter_mission_definitions`.`target_count` AS `target_count`,`hunter_mission_definitions`.`time_limit_minutes` * 60 AS `time_limit_sec`,`hunter_mission_definitions`.`gloria_reward` AS `reward_glory`,`hunter_mission_definitions`.`gloria_penalty` AS `penalty_glory`,'NORMAL' AS `difficulty`,1 AS `weight` from `hunter_mission_definitions` where `hunter_mission_definitions`.`enabled` = 1 order by `hunter_mission_definitions`.`min_rank`,`hunter_mission_definitions`.`mission_id`;

-- ----------------------------
-- View structure for v_today_events
-- ----------------------------
DROP VIEW IF EXISTS `v_today_events`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `v_today_events` AS select `hunter_scheduled_events`.`id` AS `id`,`hunter_scheduled_events`.`event_name` AS `event_name`,`hunter_scheduled_events`.`event_type` AS `event_type`,`hunter_scheduled_events`.`event_desc` AS `event_desc`,`hunter_scheduled_events`.`start_hour` AS `start_hour`,`hunter_scheduled_events`.`start_minute` AS `start_minute`,`hunter_scheduled_events`.`duration_minutes` AS `duration_minutes`,`hunter_scheduled_events`.`min_rank` AS `min_rank`,`hunter_scheduled_events`.`reward_glory_base` AS `reward_glory_base`,`hunter_scheduled_events`.`reward_glory_winner` AS `reward_glory_winner`,`hunter_scheduled_events`.`color_scheme` AS `color_scheme`,`hunter_scheduled_events`.`priority` AS `priority`,concat(lpad(`hunter_scheduled_events`.`start_hour`,2,'0'),':',lpad(`hunter_scheduled_events`.`start_minute`,2,'0')) AS `start_time` from `hunter_scheduled_events` where `hunter_scheduled_events`.`enabled` = 1 and find_in_set(dayofweek(curdate()),`hunter_scheduled_events`.`days_active`) > 0 order by `hunter_scheduled_events`.`start_hour`,`hunter_scheduled_events`.`start_minute`;

-- ----------------------------
-- Function structure for fn_rank_to_num
-- ----------------------------
DROP FUNCTION IF EXISTS `fn_rank_to_num`;
delimiter ;;
CREATE FUNCTION `fn_rank_to_num`(p_rank VARCHAR(2))
 RETURNS int(11)
  DETERMINISTIC
BEGIN
    CASE p_rank
        WHEN 'E' THEN RETURN 0;
        WHEN 'D' THEN RETURN 1;
        WHEN 'C' THEN RETURN 2;
        WHEN 'B' THEN RETURN 3;
        WHEN 'A' THEN RETURN 4;
        WHEN 'S' THEN RETURN 5;
        WHEN 'N' THEN RETURN 6;
        ELSE RETURN 0;
    END CASE;
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for sp_apply_daily_penalties
-- ----------------------------
DROP PROCEDURE IF EXISTS `sp_apply_daily_penalties`;
delimiter ;;
CREATE PROCEDURE `sp_apply_daily_penalties`()
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE v_player_id INT;
    DECLARE v_total_penalty INT;
    
    DECLARE cur CURSOR FOR 
        SELECT player_id, SUM(penalty_glory) as total_penalty
        FROM hunter_player_missions
        WHERE assigned_date = DATE_SUB(CURDATE(), INTERVAL 1 DAY)
          AND status = 'active'
        GROUP BY player_id;
    
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
    
    OPEN cur;
    read_loop: LOOP
        FETCH cur INTO v_player_id, v_total_penalty;
        IF done THEN LEAVE read_loop; END IF;
        
        UPDATE hunter_quest_ranking 
        SET total_points = GREATEST(0, total_points - v_total_penalty)
        WHERE player_id = v_player_id;
        
        UPDATE hunter_player_missions 
        SET status = 'failed'
        WHERE player_id = v_player_id 
          AND assigned_date = DATE_SUB(CURDATE(), INTERVAL 1 DAY)
          AND status = 'active';
    END LOOP;
    CLOSE cur;
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for sp_assign_daily_missions
-- ----------------------------
DROP PROCEDURE IF EXISTS `sp_assign_daily_missions`;
delimiter ;;
CREATE PROCEDURE `sp_assign_daily_missions`(IN p_player_id INT, IN p_rank VARCHAR(2), IN p_player_name VARCHAR(64))
BEGIN
    DECLARE v_today DATE;
    DECLARE v_existing INT DEFAULT 0;
    DECLARE v_player_rank_num INT;
    DECLARE v_mission1_id INT DEFAULT NULL;
    DECLARE v_mission2_id INT DEFAULT NULL;
    DECLARE v_mission3_id INT DEFAULT NULL;
    DECLARE v_mission1_target INT;
    DECLARE v_mission2_target INT;
    DECLARE v_mission3_target INT;
    DECLARE v_mission1_reward INT;
    DECLARE v_mission2_reward INT;
    DECLARE v_mission3_reward INT;
    DECLARE v_mission1_penalty INT;
    DECLARE v_mission2_penalty INT;
    DECLARE v_mission3_penalty INT;
    
    SET v_today = CURDATE();
    SET v_player_rank_num = fn_rank_to_num(p_rank);
    
    -- Controlla missioni esistenti oggi
    SELECT COUNT(*) INTO v_existing FROM hunter_player_missions WHERE player_id = p_player_id AND assigned_date = v_today;
    
    -- Se ne ha meno di 3 (o 0), rigenera
    IF v_existing < 3 THEN
        DELETE FROM hunter_player_missions WHERE player_id = p_player_id AND assigned_date = v_today;
        
        -- Slot 1
        SELECT mission_id, target_count, gloria_reward, gloria_penalty 
        INTO v_mission1_id, v_mission1_target, v_mission1_reward, v_mission1_penalty
        FROM hunter_mission_definitions WHERE enabled = 1 AND fn_rank_to_num(min_rank) <= v_player_rank_num
        ORDER BY RAND() LIMIT 1;
        
        -- Slot 2
        SELECT mission_id, target_count, gloria_reward, gloria_penalty 
        INTO v_mission2_id, v_mission2_target, v_mission2_reward, v_mission2_penalty
        FROM hunter_mission_definitions WHERE enabled = 1 AND fn_rank_to_num(min_rank) <= v_player_rank_num AND mission_id != IFNULL(v_mission1_id, -1)
        ORDER BY RAND() LIMIT 1;
        
        -- Slot 3
        SELECT mission_id, target_count, gloria_reward, gloria_penalty 
        INTO v_mission3_id, v_mission3_target, v_mission3_reward, v_mission3_penalty
        FROM hunter_mission_definitions WHERE enabled = 1 AND fn_rank_to_num(min_rank) <= v_player_rank_num AND mission_id != IFNULL(v_mission1_id, -1) AND mission_id != IFNULL(v_mission2_id, -1)
        ORDER BY RAND() LIMIT 1;
        
        IF v_mission1_id IS NOT NULL THEN
            INSERT INTO hunter_player_missions (player_id, mission_slot, mission_def_id, assigned_date, current_progress, target_count, status, reward_glory, penalty_glory)
            VALUES (p_player_id, 1, v_mission1_id, v_today, 0, v_mission1_target, 'active', v_mission1_reward, v_mission1_penalty);
        END IF;
        IF v_mission2_id IS NOT NULL THEN
            INSERT INTO hunter_player_missions (player_id, mission_slot, mission_def_id, assigned_date, current_progress, target_count, status, reward_glory, penalty_glory)
            VALUES (p_player_id, 2, v_mission2_id, v_today, 0, v_mission2_target, 'active', v_mission2_reward, v_mission2_penalty);
        END IF;
        IF v_mission3_id IS NOT NULL THEN
            INSERT INTO hunter_player_missions (player_id, mission_slot, mission_def_id, assigned_date, current_progress, target_count, status, reward_glory, penalty_glory)
            VALUES (p_player_id, 3, v_mission3_id, v_today, 0, v_mission3_target, 'active', v_mission3_reward, v_mission3_penalty);
        END IF;
    END IF;
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for sp_check_gate_access
-- ----------------------------
DROP PROCEDURE IF EXISTS `sp_check_gate_access`;
delimiter ;;
CREATE PROCEDURE `sp_check_gate_access`(IN p_player_id INT,
    OUT p_has_access TINYINT,
    OUT p_gate_id INT,
    OUT p_gate_name VARCHAR(64),
    OUT p_remaining_seconds INT,
    OUT p_color_code VARCHAR(16))
BEGIN
    SELECT 
        1,
        ga.gate_id,
        gc.gate_name,
        GREATEST(0, TIMESTAMPDIFF(SECOND, NOW(), ga.expires_at)),
        gc.color_code
    INTO p_has_access, p_gate_id, p_gate_name, p_remaining_seconds, p_color_code
    FROM hunter_gate_access ga
    JOIN hunter_gate_config gc ON ga.gate_id = gc.gate_id
    WHERE ga.player_id = p_player_id
      AND ga.status = 'pending'
      AND ga.expires_at > NOW()
    LIMIT 1;
    
    IF p_has_access IS NULL THEN
        SET p_has_access = 0;
        SET p_gate_id = 0;
        SET p_gate_name = '';
        SET p_remaining_seconds = 0;
        SET p_color_code = '';
    END IF;
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for sp_check_trial_complete
-- ----------------------------
DROP PROCEDURE IF EXISTS `sp_check_trial_complete`;
delimiter ;;
CREATE PROCEDURE `sp_check_trial_complete`(IN p_player_id INT,
    OUT p_completed TINYINT,
    OUT p_new_rank VARCHAR(2),
    OUT p_gloria_reward INT,
    OUT p_title_reward VARCHAR(64))
BEGIN
    DECLARE v_trial_id INT;
    DECLARE v_boss_kills INT;
    DECLARE v_metin_kills INT;
    DECLARE v_fracture_seals INT;
    DECLARE v_chest_opens INT;
    DECLARE v_daily_missions INT;
    DECLARE v_req_boss INT;
    DECLARE v_req_metin INT;
    DECLARE v_req_fracture INT;
    DECLARE v_req_chest INT;
    DECLARE v_req_daily INT;
    
    SET p_completed = 0;
    
    SELECT pt.trial_id, pt.boss_kills, pt.metin_kills, pt.fracture_seals, pt.chest_opens, pt.daily_missions,
           rt.required_boss_kills, rt.required_metin_kills, rt.required_fracture_seals, rt.required_chest_opens, rt.required_daily_missions,
           rt.to_rank, rt.gloria_reward, rt.title_reward
    INTO v_trial_id, v_boss_kills, v_metin_kills, v_fracture_seals, v_chest_opens, v_daily_missions,
         v_req_boss, v_req_metin, v_req_fracture, v_req_chest, v_req_daily,
         p_new_rank, p_gloria_reward, p_title_reward
    FROM hunter_player_trials pt
    JOIN hunter_rank_trials rt ON pt.trial_id = rt.trial_id
    WHERE pt.player_id = p_player_id AND pt.status = 'in_progress'
    LIMIT 1;
    
    IF v_trial_id IS NOT NULL THEN
        IF v_boss_kills >= v_req_boss 
           AND v_metin_kills >= v_req_metin 
           AND v_fracture_seals >= v_req_fracture 
           AND v_chest_opens >= v_req_chest 
           AND v_daily_missions >= v_req_daily THEN
            
            -- Completa la prova
            UPDATE hunter_player_trials SET status = 'completed', completed_at = NOW() WHERE player_id = p_player_id AND trial_id = v_trial_id;
            
            -- Aggiorna rank e gloria
            UPDATE hunter_quest_ranking 
            SET hunter_rank = p_new_rank, 
                current_rank = p_new_rank,
                total_points = total_points + p_gloria_reward
            WHERE player_id = p_player_id;
            
            SET p_completed = 1;
        END IF;
    END IF;
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for sp_complete_gate
-- ----------------------------
DROP PROCEDURE IF EXISTS `sp_complete_gate`;
delimiter ;;
CREATE PROCEDURE `sp_complete_gate`(IN p_player_id INT,
    IN p_result VARCHAR(16),
    OUT p_gloria_change INT)
BEGIN
    DECLARE v_access_id INT;
    DECLARE v_gate_id INT;
    DECLARE v_gate_name VARCHAR(64);
    DECLARE v_entered_at TIMESTAMP;
    DECLARE v_gloria_reward INT;
    DECLARE v_gloria_penalty INT;
    DECLARE v_duration INT;
    
    -- Trova l'accesso attivo
    SELECT ga.access_id, ga.gate_id, gc.gate_name, ga.entered_at, gc.gloria_reward, gc.gloria_penalty
    INTO v_access_id, v_gate_id, v_gate_name, v_entered_at, v_gloria_reward, v_gloria_penalty
    FROM hunter_gate_access ga
    JOIN hunter_gate_config gc ON ga.gate_id = gc.gate_id
    WHERE ga.player_id = p_player_id AND ga.status = 'entered'
    LIMIT 1;
    
    IF v_access_id IS NOT NULL THEN
        SET v_duration = TIMESTAMPDIFF(SECOND, v_entered_at, NOW());
        
        IF p_result = 'completed' THEN
            SET p_gloria_change = v_gloria_reward;
            UPDATE hunter_gate_access SET status = 'completed', completed_at = NOW(), gloria_earned = v_gloria_reward WHERE access_id = v_access_id;
        ELSE
            SET p_gloria_change = -v_gloria_penalty;
            UPDATE hunter_gate_access SET status = 'failed', completed_at = NOW(), gloria_earned = -v_gloria_penalty WHERE access_id = v_access_id;
        END IF;
        
        -- Aggiorna Gloria del giocatore
        UPDATE hunter_quest_ranking 
        SET total_points = GREATEST(0, total_points + p_gloria_change),
            daily_points = daily_points + GREATEST(0, p_gloria_change)
        WHERE player_id = p_player_id;
        
        -- Inserisci in history
        INSERT INTO hunter_gate_history (player_id, player_name, gate_id, gate_name, result, gloria_change, duration_seconds)
        SELECT p_player_id, player_name, v_gate_id, v_gate_name, p_result, p_gloria_change, v_duration
        FROM hunter_quest_ranking WHERE player_id = p_player_id;
    ELSE
        SET p_gloria_change = 0;
    END IF;
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for sp_distribute_party_glory
-- ----------------------------
DROP PROCEDURE IF EXISTS `sp_distribute_party_glory`;
delimiter ;;
CREATE PROCEDURE `sp_distribute_party_glory`(IN p_opener_id INT,
    IN p_opener_name VARCHAR(50),
    IN p_base_glory INT,
    IN p_source_type VARCHAR(50),
    IN p_source_name VARCHAR(100))
BEGIN
    DECLARE v_party_id INT DEFAULT 0;
    DECLARE v_member_count INT DEFAULT 0;
    DECLARE v_share_per_member INT DEFAULT 0;
    
    -- Trova il party_id del giocatore che ha aperto
    SELECT pid INTO v_party_id 
    FROM player.player 
    WHERE id = p_opener_id;
    
    -- Se non ha party (pid=0), assegna tutto a lui
    IF v_party_id IS NULL OR v_party_id = 0 THEN
        -- Assegna direttamente all'opener
        UPDATE srv1_hunabku.hunter_quest_ranking 
        SET total_points = total_points + p_base_glory,
            spendable_points = spendable_points + p_base_glory
        WHERE player_id = p_opener_id;
    ELSE
        -- Conta i membri del party
        SELECT COUNT(*) INTO v_member_count 
        FROM player.player 
        WHERE pid = v_party_id;
        
        IF v_member_count < 1 THEN SET v_member_count = 1; END IF;
        
        -- Calcola la quota per membro (divisione equa semplice)
        SET v_share_per_member = FLOOR(p_base_glory / v_member_count);
        IF v_share_per_member < 1 THEN SET v_share_per_member = 1; END IF;
        
        -- Inserisci ricompense pendenti per TUTTI i membri del party
        INSERT INTO srv1_hunabku.hunter_pending_rewards 
            (player_id, player_name, glory_amount, source_type, source_name, opener_id, opener_name)
        SELECT 
            p.id,
            p.name,
            v_share_per_member,
            p_source_type,
            p_source_name,
            p_opener_id,
            p_opener_name
        FROM player.player p
        WHERE p.pid = v_party_id;
        
        -- Assegna subito la gloria a tutti i membri del party
        UPDATE srv1_hunabku.hunter_quest_ranking r
        INNER JOIN player.player p ON r.player_id = p.id
        SET r.total_points = r.total_points + v_share_per_member,
            r.spendable_points = r.spendable_points + v_share_per_member
        WHERE p.pid = v_party_id;
        
        -- Marca le ricompense come consegnate
        UPDATE srv1_hunabku.hunter_pending_rewards
        SET claimed = 1, claimed_at = NOW()
        WHERE opener_id = p_opener_id 
        AND source_name = p_source_name
        AND claimed = 0;
    END IF;
    
    -- Ritorna il numero di membri che hanno ricevuto
    SELECT v_member_count AS members_rewarded, v_share_per_member AS glory_each;
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for sp_distribute_party_glory_merit
-- ----------------------------
DROP PROCEDURE IF EXISTS `sp_distribute_party_glory_merit`;
delimiter ;;
CREATE PROCEDURE `sp_distribute_party_glory_merit`(IN p_opener_id INT,
    IN p_opener_name VARCHAR(50),
    IN p_base_glory INT,
    IN p_source_type VARCHAR(50),
    IN p_source_name VARCHAR(100))
BEGIN
    DECLARE v_party_id INT DEFAULT 0;
    DECLARE v_total_power INT DEFAULT 0;
    DECLARE done INT DEFAULT FALSE;
    DECLARE v_pid INT;
    DECLARE v_pname VARCHAR(50);
    DECLARE v_points INT;
    DECLARE v_grade VARCHAR(5);
    DECLARE v_power INT;
    DECLARE v_share INT;
    DECLARE v_member_count INT DEFAULT 0;
    
    -- Cursore per iterare sui membri del party
    DECLARE member_cursor CURSOR FOR
        SELECT p.id, p.name, COALESCE(r.total_points, 0) as points
        FROM player.player p
        LEFT JOIN srv1_hunabku.hunter_quest_ranking r ON p.id = r.player_id
        WHERE p.pid = v_party_id;
    
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
    
    -- Trova il party_id
    SELECT pid INTO v_party_id 
    FROM player.player 
    WHERE id = p_opener_id;
    
    -- Se non ha party, assegna tutto a lui
    IF v_party_id IS NULL OR v_party_id = 0 THEN
        UPDATE srv1_hunabku.hunter_quest_ranking 
        SET total_points = total_points + p_base_glory,
            spendable_points = spendable_points + p_base_glory
        WHERE player_id = p_opener_id;
        
        SELECT 1 AS members_rewarded, p_base_glory AS glory_each;
    ELSE
        -- Calcola il power totale del party
        SELECT SUM(
            CASE 
                WHEN COALESCE(r.total_points, 0) >= 100000 THEN 250  -- N
                WHEN COALESCE(r.total_points, 0) >= 50000 THEN 150   -- S
                WHEN COALESCE(r.total_points, 0) >= 20000 THEN 80    -- A
                WHEN COALESCE(r.total_points, 0) >= 8000 THEN 40     -- B
                WHEN COALESCE(r.total_points, 0) >= 3000 THEN 15     -- C
                WHEN COALESCE(r.total_points, 0) >= 500 THEN 5       -- D
                ELSE 1                                               -- E
            END
        ) INTO v_total_power
        FROM player.player p
        LEFT JOIN srv1_hunabku.hunter_quest_ranking r ON p.id = r.player_id
        WHERE p.pid = v_party_id;
        
        IF v_total_power < 1 THEN SET v_total_power = 1; END IF;
        
        -- Itera sui membri e distribuisci per meritocrazia
        OPEN member_cursor;
        
        read_loop: LOOP
            FETCH member_cursor INTO v_pid, v_pname, v_points;
            IF done THEN
                LEAVE read_loop;
            END IF;
            
            -- Calcola il power rank di questo membro
            SET v_power = CASE 
                WHEN v_points >= 100000 THEN 250
                WHEN v_points >= 50000 THEN 150
                WHEN v_points >= 20000 THEN 80
                WHEN v_points >= 8000 THEN 40
                WHEN v_points >= 3000 THEN 15
                WHEN v_points >= 500 THEN 5
                ELSE 1
            END;
            
            -- Calcola la quota basata sul power rank
            SET v_share = FLOOR((v_power * p_base_glory) / v_total_power);
            IF v_share < 1 THEN SET v_share = 1; END IF;
            
            -- Assegna la gloria
            UPDATE srv1_hunabku.hunter_quest_ranking 
            SET total_points = total_points + v_share,
                spendable_points = spendable_points + v_share
            WHERE player_id = v_pid;
            
            -- Se non esiste il record, crealo
            IF ROW_COUNT() = 0 THEN
                INSERT INTO srv1_hunabku.hunter_quest_ranking 
                    (player_id, player_name, total_points, spendable_points)
                VALUES (v_pid, v_pname, v_share, v_share)
                ON DUPLICATE KEY UPDATE
                    total_points = total_points + v_share,
                    spendable_points = spendable_points + v_share;
            END IF;
            
            -- Log nella tabella pending (per storico)
            INSERT INTO srv1_hunabku.hunter_pending_rewards 
                (player_id, player_name, glory_amount, source_type, source_name, opener_id, opener_name, claimed, claimed_at)
            VALUES (v_pid, v_pname, v_share, p_source_type, p_source_name, p_opener_id, p_opener_name, 1, NOW());
            
            SET v_member_count = v_member_count + 1;
        END LOOP;
        
        CLOSE member_cursor;
        
        SELECT v_member_count AS members_rewarded, p_base_glory AS total_glory;
    END IF;
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for sp_enter_gate
-- ----------------------------
DROP PROCEDURE IF EXISTS `sp_enter_gate`;
delimiter ;;
CREATE PROCEDURE `sp_enter_gate`(IN p_player_id INT,
    IN p_access_id INT,
    OUT p_success TINYINT,
    OUT p_dungeon_index INT,
    OUT p_duration_minutes INT)
BEGIN
    DECLARE v_gate_id INT;
    
    SELECT ga.gate_id, gc.dungeon_index, gc.duration_minutes
    INTO v_gate_id, p_dungeon_index, p_duration_minutes
    FROM hunter_gate_access ga
    JOIN hunter_gate_config gc ON ga.gate_id = gc.gate_id
    WHERE ga.access_id = p_access_id
      AND ga.player_id = p_player_id
      AND ga.status = 'pending'
      AND ga.expires_at > NOW();
    
    IF v_gate_id IS NOT NULL THEN
        UPDATE hunter_gate_access 
        SET status = 'entered', entered_at = NOW()
        WHERE access_id = p_access_id;
        SET p_success = 1;
    ELSE
        SET p_success = 0;
        SET p_dungeon_index = 0;
        SET p_duration_minutes = 0;
    END IF;
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for sp_get_party_notifications
-- ----------------------------
DROP PROCEDURE IF EXISTS `sp_get_party_notifications`;
delimiter ;;
CREATE PROCEDURE `sp_get_party_notifications`(IN p_player_id INT)
BEGIN
    -- Seleziona tutte le notifiche non ancora mostrate (max 5 alla volta)
    SELECT id, notification_type, source_name, glory_received, glory_total,
           actor_name, actor_rank, color_code, extra_data, created_at
    FROM srv1_hunabku.hunter_party_notifications
    WHERE player_id = p_player_id AND shown = 0
    ORDER BY created_at ASC
    LIMIT 5;
    
    -- Marca come mostrate
    UPDATE srv1_hunabku.hunter_party_notifications
    SET shown = 1, shown_at = NOW()
    WHERE player_id = p_player_id AND shown = 0
    LIMIT 5;
    
    -- Pulizia vecchie notifiche (oltre 1 ora)
    DELETE FROM srv1_hunabku.hunter_party_notifications
    WHERE created_at < DATE_SUB(NOW(), INTERVAL 1 HOUR);
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for sp_hunter_activity
-- ----------------------------
DROP PROCEDURE IF EXISTS `sp_hunter_activity`;
delimiter ;;
CREATE PROCEDURE `sp_hunter_activity`(IN p_player_id INT,
    IN p_player_name VARCHAR(24),
    IN p_activity_type VARCHAR(30),
    IN p_vnum INT,
    IN p_amount INT,
    IN p_metadata JSON)
BEGIN
    DECLARE v_base_points INT DEFAULT 0;
    DECLARE v_vnum_type VARCHAR(20) DEFAULT 'mob';
    DECLARE v_current_rank CHAR(1) DEFAULT 'E';
    DECLARE v_streak_bonus DECIMAL(5,2) DEFAULT 0;
    DECLARE v_event_mult DECIMAL(3,2) DEFAULT 1.00;
    DECLARE v_final_glory INT DEFAULT 0;
    DECLARE v_is_boss TINYINT DEFAULT 0;
    DECLARE v_is_metin TINYINT DEFAULT 0;
    DECLARE v_speed_kill_bonus TINYINT DEFAULT 0;
    
    INSERT INTO hunter_players (player_id, player_name, created_at)
    VALUES (p_player_id, p_player_name, NOW())
    ON DUPLICATE KEY UPDATE player_name = p_player_name;
    
    SELECT current_rank,
           CASE 
               WHEN login_streak >= 30 THEN 0.20
               WHEN login_streak >= 14 THEN 0.15
               WHEN login_streak >= 7 THEN 0.10
               WHEN login_streak >= 3 THEN 0.05
               ELSE 0
           END
    INTO v_current_rank, v_streak_bonus
    FROM hunter_players WHERE player_id = p_player_id;
    
    IF p_activity_type IN ('kill_mob', 'kill_boss', 'kill_metin') THEN
        SELECT COALESCE(base_points, 1), 
               COALESCE(vnum_type, 'mob'),
               COALESCE(event_multiplier, 1.00),
               COALESCE(speed_kill_bonus, 0)
        INTO v_base_points, v_vnum_type, v_event_mult, v_speed_kill_bonus
        FROM hunter_vnum_registry WHERE vnum = p_vnum;
        
        IF v_base_points = 0 THEN SET v_base_points = 1; END IF;
        SET v_is_boss = IF(v_vnum_type IN ('boss', 'super_boss'), 1, 0);
        SET v_is_metin = IF(v_vnum_type IN ('metin', 'super_metin'), 1, 0);
        SET v_final_glory = FLOOR(v_base_points * v_event_mult * (1 + v_streak_bonus));
        
        IF p_amount = 1 AND v_speed_kill_bonus = 1 THEN
            SET v_final_glory = v_final_glory * 2;
        END IF;
        
        UPDATE hunter_players SET
            pending_glory = pending_glory + v_final_glory,
            pending_kills = pending_kills + 1,
            total_bosses = total_bosses + v_is_boss,
            total_metins = total_metins + v_is_metin,
            trial_boss_kills = trial_boss_kills + IF(trial_id > 0, v_is_boss, 0),
            trial_metin_kills = trial_metin_kills + IF(trial_id > 0, v_is_metin, 0)
        WHERE player_id = p_player_id;
        
    ELSEIF p_activity_type = 'open_chest' THEN
        SELECT COALESCE(base_points, 50) INTO v_final_glory FROM hunter_vnum_registry WHERE vnum = p_vnum;
        IF v_final_glory = 0 THEN SET v_final_glory = 50; END IF;
        UPDATE hunter_players SET
            pending_glory = pending_glory + v_final_glory,
            total_chests = total_chests + 1,
            trial_chest_opens = trial_chest_opens + IF(trial_id > 0, 1, 0)
        WHERE player_id = p_player_id;
        
    ELSEIF p_activity_type = 'seal_fracture' THEN
        SET v_final_glory = p_amount;
        UPDATE hunter_players SET
            pending_glory = pending_glory + v_final_glory,
            total_fractures = total_fractures + 1,
            trial_fracture_seals = trial_fracture_seals + IF(trial_id > 0, 1, 0)
        WHERE player_id = p_player_id;
        
    ELSEIF p_activity_type = 'complete_mission' THEN
        SET v_final_glory = p_amount;
        UPDATE hunter_players SET
            pending_glory = pending_glory + v_final_glory,
            trial_daily_missions = trial_daily_missions + IF(trial_id > 0, 1, 0)
        WHERE player_id = p_player_id;
        
    ELSEIF p_activity_type = 'complete_trial' THEN
        SET v_final_glory = p_amount;
        UPDATE hunter_players SET
            pending_glory = pending_glory + v_final_glory,
            trial_id = 0, trial_boss_kills = 0, trial_metin_kills = 0,
            trial_fracture_seals = 0, trial_chest_opens = 0, trial_daily_missions = 0,
            trial_started_at = NULL, trial_expires_at = NULL
        WHERE player_id = p_player_id;
        
    ELSEIF p_activity_type = 'enter_gate' THEN
        UPDATE hunter_players SET
            gate_id = p_vnum,
            gate_entered_at = NOW(),
            gate_expires_at = DATE_ADD(NOW(), INTERVAL p_amount MINUTE)
        WHERE player_id = p_player_id;
        
    ELSEIF p_activity_type = 'complete_gate' THEN
        SET v_final_glory = p_amount;
        UPDATE hunter_players SET
            pending_glory = pending_glory + v_final_glory,
            gate_id = 0, gate_entered_at = NULL, gate_expires_at = NULL
        WHERE player_id = p_player_id;
        
    ELSEIF p_activity_type = 'fail_gate' THEN
        SET v_final_glory = -p_amount;
        UPDATE hunter_players SET
            total_glory = GREATEST(0, total_glory - p_amount),
            gate_id = 0, gate_entered_at = NULL, gate_expires_at = NULL
        WHERE player_id = p_player_id;
        
    ELSEIF p_activity_type = 'login_bonus' THEN
        UPDATE hunter_players SET
            login_streak = IF(last_login = DATE_SUB(CURDATE(), INTERVAL 1 DAY), login_streak + 1, 1),
            last_login = CURDATE()
        WHERE player_id = p_player_id;
        
    ELSEIF p_activity_type = 'convert_credits' THEN
        UPDATE hunter_players SET
            spendable_credits = spendable_credits + p_amount,
            total_glory = GREATEST(0, total_glory - (p_amount * 10))
        WHERE player_id = p_player_id;
        
    ELSEIF p_activity_type = 'shop_purchase' THEN
        UPDATE hunter_players SET
            spendable_credits = GREATEST(0, spendable_credits - p_amount)
        WHERE player_id = p_player_id;
    END IF;
    
    IF v_final_glory != 0 OR p_activity_type IN ('enter_gate', 'login_bonus', 'shop_purchase') THEN
        INSERT INTO hunter_activity_log (player_id, activity_type, vnum, glory_change, metadata)
        VALUES (p_player_id, p_activity_type, p_vnum, v_final_glory, p_metadata);
    END IF;
    
    SELECT v_final_glory AS glory_earned, v_vnum_type AS vnum_type, v_is_boss AS is_boss, v_is_metin AS is_metin;
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for sp_hunter_assign_missions
-- ----------------------------
DROP PROCEDURE IF EXISTS `sp_hunter_assign_missions`;
delimiter ;;
CREATE PROCEDURE `sp_hunter_assign_missions`(IN p_player_id INT)
BEGIN
    DECLARE v_rank CHAR(1);
    DECLARE v_today DATE;
    DECLARE v_count INT;
    
    SET v_today = CURDATE();
    SELECT COUNT(*) INTO v_count FROM hunter_player_missions WHERE player_id = p_player_id AND assigned_at = v_today;
    
    IF v_count > 0 THEN
        SELECT pm.slot, pm.mission_id, pm.current_progress, pm.status, m.mission_name, m.mission_type, 
               m.target_vnum, m.target_count, m.glory_reward, m.glory_penalty
        FROM hunter_player_missions pm JOIN hunter_missions m ON pm.mission_id = m.mission_id
        WHERE pm.player_id = p_player_id AND pm.assigned_at = v_today ORDER BY pm.slot;
    ELSE
        SELECT current_rank INTO v_rank FROM hunter_players WHERE player_id = p_player_id;
        
        INSERT INTO hunter_player_missions (player_id, slot, mission_id, assigned_at)
        SELECT p_player_id, 0, mission_id, v_today FROM hunter_missions
        WHERE is_active = 1 AND min_rank <= v_rank ORDER BY RAND() * weight DESC LIMIT 1;
        
        INSERT INTO hunter_player_missions (player_id, slot, mission_id, assigned_at)
        SELECT p_player_id, 1, mission_id, v_today FROM hunter_missions
        WHERE is_active = 1 AND min_rank <= v_rank AND mission_id NOT IN 
            (SELECT mission_id FROM hunter_player_missions WHERE player_id = p_player_id AND assigned_at = v_today)
        ORDER BY RAND() * weight DESC LIMIT 1;
        
        INSERT INTO hunter_player_missions (player_id, slot, mission_id, assigned_at)
        SELECT p_player_id, 2, mission_id, v_today FROM hunter_missions
        WHERE is_active = 1 AND min_rank <= v_rank AND mission_id NOT IN 
            (SELECT mission_id FROM hunter_player_missions WHERE player_id = p_player_id AND assigned_at = v_today)
        ORDER BY RAND() * weight DESC LIMIT 1;
        
        SELECT pm.slot, pm.mission_id, pm.current_progress, pm.status, m.mission_name, m.mission_type,
               m.target_vnum, m.target_count, m.glory_reward, m.glory_penalty
        FROM hunter_player_missions pm JOIN hunter_missions m ON pm.mission_id = m.mission_id
        WHERE pm.player_id = p_player_id AND pm.assigned_at = v_today ORDER BY pm.slot;
    END IF;
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for sp_hunter_daily_reset
-- ----------------------------
DROP PROCEDURE IF EXISTS `sp_hunter_daily_reset`;
delimiter ;;
CREATE PROCEDURE `sp_hunter_daily_reset`()
BEGIN
    CALL sp_hunter_flush_pending();
    UPDATE hunter_players SET daily_glory = 0, daily_kills = 0, daily_position = 0;
    UPDATE hunter_player_missions SET status = 'failed' WHERE status = 'active' AND assigned_at < CURDATE();
    SELECT 'DAILY_RESET_COMPLETE' AS status;
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for sp_hunter_flush_pending
-- ----------------------------
DROP PROCEDURE IF EXISTS `sp_hunter_flush_pending`;
delimiter ;;
CREATE PROCEDURE `sp_hunter_flush_pending`()
BEGIN
    UPDATE hunter_players SET
        total_glory = total_glory + pending_glory,
        daily_glory = daily_glory + pending_glory,
        weekly_glory = weekly_glory + pending_glory,
        total_kills = total_kills + pending_kills,
        daily_kills = daily_kills + pending_kills,
        weekly_kills = weekly_kills + pending_kills,
        pending_glory = 0, pending_kills = 0, last_flush = NOW()
    WHERE pending_glory > 0 OR pending_kills > 0;
    
    UPDATE hunter_players SET current_rank = 
        CASE 
            WHEN total_glory >= 1500000 THEN 'N'
            WHEN total_glory >= 500000 THEN 'S'
            WHEN total_glory >= 150000 THEN 'A'
            WHEN total_glory >= 50000 THEN 'B'
            WHEN total_glory >= 10000 THEN 'C'
            WHEN total_glory >= 2000 THEN 'D'
            ELSE 'E'
        END;
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for sp_hunter_get_active_events
-- ----------------------------
DROP PROCEDURE IF EXISTS `sp_hunter_get_active_events`;
delimiter ;;
CREATE PROCEDURE `sp_hunter_get_active_events`()
BEGIN
    DECLARE v_day INT;
    DECLARE v_hour INT;
    
    SET v_day = DAYOFWEEK(NOW());
    SET v_hour = HOUR(NOW());
    
    SELECT event_id, event_name, event_type, glory_multiplier, min_rank, color_code, description
    FROM hunter_events
    WHERE is_active = 1
      AND FIND_IN_SET(v_day, days_active) > 0
      AND v_hour >= start_hour
      AND v_hour < (start_hour + CEIL(duration_minutes / 60));
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for sp_hunter_get_player
-- ----------------------------
DROP PROCEDURE IF EXISTS `sp_hunter_get_player`;
delimiter ;;
CREATE PROCEDURE `sp_hunter_get_player`(IN p_player_id INT)
BEGIN
    SELECT p.*, t.trial_name, t.to_rank, t.boss_kills_req, t.metin_kills_req,
           t.fracture_seals_req, t.chest_opens_req, t.daily_missions_req,
           t.glory_reward AS trial_glory_reward, t.color_code AS trial_color
    FROM hunter_players p
    LEFT JOIN hunter_trials t ON p.trial_id = t.trial_id
    WHERE p.player_id = p_player_id;
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for sp_hunter_get_ranking
-- ----------------------------
DROP PROCEDURE IF EXISTS `sp_hunter_get_ranking`;
delimiter ;;
CREATE PROCEDURE `sp_hunter_get_ranking`(IN p_type VARCHAR(20), IN p_limit INT)
BEGIN
    IF p_type = 'daily' THEN
        SELECT player_name, daily_glory AS glory, daily_kills AS kills, current_rank
        FROM hunter_players WHERE daily_glory > 0 ORDER BY daily_glory DESC LIMIT p_limit;
    ELSEIF p_type = 'weekly' THEN
        SELECT player_name, weekly_glory AS glory, weekly_kills AS kills, current_rank
        FROM hunter_players WHERE weekly_glory > 0 ORDER BY weekly_glory DESC LIMIT p_limit;
    ELSE
        SELECT player_name, total_glory AS glory, total_kills AS kills, current_rank
        FROM hunter_players WHERE total_glory > 0 ORDER BY total_glory DESC LIMIT p_limit;
    END IF;
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for sp_hunter_log
-- ----------------------------
DROP PROCEDURE IF EXISTS `sp_hunter_log`;
delimiter ;;
CREATE PROCEDURE `sp_hunter_log`(IN p_player_id INT,
    IN p_player_name VARCHAR(50),
    IN p_log_type VARCHAR(32),
    IN p_severity VARCHAR(16),
    IN p_action VARCHAR(64),
    IN p_details TEXT,
    IN p_map_index INT,
    IN p_pos_x INT,
    IN p_pos_y INT)
BEGIN
    INSERT INTO hunter_security_logs 
        (player_id, player_name, log_type, severity, action, details, map_index, position_x, position_y)
    VALUES 
        (p_player_id, p_player_name, p_log_type, p_severity, p_action, p_details, p_map_index, p_pos_x, p_pos_y);
    
    -- Se severity alta, aggiorna/inserisci in suspicious_players
    IF p_severity IN ('ALERT', 'CRITICAL') THEN
        INSERT INTO hunter_suspicious_players (player_id, player_name, reason, alert_count, first_alert_at, last_alert_at)
        VALUES (p_player_id, p_player_name, p_action, 1, NOW(), NOW())
        ON DUPLICATE KEY UPDATE 
            alert_count = alert_count + 1,
            last_alert_at = NOW(),
            reason = CONCAT(reason, ' | ', p_action);
    END IF;
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for sp_hunter_log_cleanup
-- ----------------------------
DROP PROCEDURE IF EXISTS `sp_hunter_log_cleanup`;
delimiter ;;
CREATE PROCEDURE `sp_hunter_log_cleanup`()
BEGIN
    -- Elimina log INFO piu vecchi di 7 giorni
    DELETE FROM hunter_security_logs 
    WHERE severity = 'INFO' AND created_at < DATE_SUB(NOW(), INTERVAL 7 DAY);
    
    -- Elimina log WARNING piu vecchi di 30 giorni
    DELETE FROM hunter_security_logs 
    WHERE severity = 'WARNING' AND created_at < DATE_SUB(NOW(), INTERVAL 30 DAY);
    
    -- Mantieni ALERT e CRITICAL per 90 giorni
    DELETE FROM hunter_security_logs 
    WHERE severity IN ('ALERT', 'CRITICAL') AND created_at < DATE_SUB(NOW(), INTERVAL 90 DAY);
    
    -- Elimina snapshot piu vecchi di 30 giorni
    DELETE FROM hunter_player_stats_snapshot
    WHERE created_at < DATE_SUB(NOW(), INTERVAL 30 DAY);
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for sp_hunter_start_trial
-- ----------------------------
DROP PROCEDURE IF EXISTS `sp_hunter_start_trial`;
delimiter ;;
CREATE PROCEDURE `sp_hunter_start_trial`(IN p_player_id INT)
BEGIN
    DECLARE v_rank CHAR(1);
    DECLARE v_trial_id INT;
    DECLARE v_duration INT;
    
    SELECT current_rank INTO v_rank FROM hunter_players WHERE player_id = p_player_id;
    SELECT trial_id, duration_hours INTO v_trial_id, v_duration FROM hunter_trials WHERE from_rank = v_rank LIMIT 1;
    
    IF v_trial_id IS NOT NULL THEN
        UPDATE hunter_players SET
            trial_id = v_trial_id, trial_boss_kills = 0, trial_metin_kills = 0,
            trial_fracture_seals = 0, trial_chest_opens = 0, trial_daily_missions = 0,
            trial_started_at = NOW(), trial_expires_at = DATE_ADD(NOW(), INTERVAL v_duration HOUR)
        WHERE player_id = p_player_id;
        
        SELECT t.*, p.trial_expires_at FROM hunter_trials t
        JOIN hunter_players p ON p.trial_id = t.trial_id
        WHERE t.trial_id = v_trial_id AND p.player_id = p_player_id;
    ELSE
        SELECT 'NO_TRIAL' AS error;
    END IF;
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for sp_hunter_update_mission
-- ----------------------------
DROP PROCEDURE IF EXISTS `sp_hunter_update_mission`;
delimiter ;;
CREATE PROCEDURE `sp_hunter_update_mission`(IN p_player_id INT,
    IN p_mission_type VARCHAR(20),
    IN p_vnum INT,
    IN p_increment INT)
BEGIN
    DECLARE v_today DATE;
    SET v_today = CURDATE();
    
    -- Aggiorna progresso per missioni attive che matchano il tipo
    UPDATE hunter_player_missions pm
    JOIN hunter_missions m ON pm.mission_id = m.mission_id
    SET pm.current_progress = pm.current_progress + p_increment,
        pm.status = CASE 
            WHEN pm.current_progress + p_increment >= m.target_count THEN 'completed'
            ELSE 'active'
        END,
        pm.completed_at = CASE
            WHEN pm.current_progress + p_increment >= m.target_count THEN NOW()
            ELSE NULL
        END
    WHERE pm.player_id = p_player_id
      AND pm.assigned_at = v_today
      AND pm.status = 'active'
      AND (
          m.mission_type = p_mission_type
          OR (m.mission_type = 'kill_any' AND p_mission_type IN ('kill_mob', 'kill_boss', 'kill_metin'))
          OR (m.mission_type = 'kill_vnum' AND m.target_vnum = p_vnum)
      );
    
    -- Ritorna stato missioni aggiornate
    SELECT pm.slot, pm.mission_id, pm.current_progress, pm.status, 
           m.mission_name, m.target_count, m.glory_reward, m.glory_penalty
    FROM hunter_player_missions pm
    JOIN hunter_missions m ON pm.mission_id = m.mission_id
    WHERE pm.player_id = p_player_id AND pm.assigned_at = v_today;
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for sp_hunter_weekly_reset
-- ----------------------------
DROP PROCEDURE IF EXISTS `sp_hunter_weekly_reset`;
delimiter ;;
CREATE PROCEDURE `sp_hunter_weekly_reset`()
BEGIN
    CALL sp_hunter_daily_reset();
    UPDATE hunter_players SET weekly_glory = 0, weekly_kills = 0, weekly_position = 0;
    SELECT 'WEEKLY_RESET_COMPLETE' AS status;
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for sp_notify_party_glory
-- ----------------------------
DROP PROCEDURE IF EXISTS `sp_notify_party_glory`;
delimiter ;;
CREATE PROCEDURE `sp_notify_party_glory`(IN p_actor_id INT,
    IN p_actor_name VARCHAR(50),
    IN p_actor_rank VARCHAR(10),
    IN p_notification_type VARCHAR(30),
    IN p_source_name VARCHAR(100),
    IN p_glory_total INT,
    IN p_color_code VARCHAR(20),
    IN p_extra_data VARCHAR(255))
BEGIN
    DECLARE v_party_id INT DEFAULT 0;
    DECLARE v_total_power INT DEFAULT 0;
    DECLARE done INT DEFAULT FALSE;
    DECLARE v_pid INT;
    DECLARE v_pname VARCHAR(50);
    DECLARE v_points INT;
    DECLARE v_power INT;
    DECLARE v_share INT;
    
    DECLARE member_cursor CURSOR FOR
        SELECT p.id, p.name, COALESCE(r.total_points, 0) as points
        FROM player.player p
        LEFT JOIN srv1_hunabku.hunter_quest_ranking r ON p.id = r.player_id
        WHERE p.pid = v_party_id;
    
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
    
    -- Trova il party_id
    SELECT pid INTO v_party_id 
    FROM player.player 
    WHERE id = p_actor_id;
    
    -- Se non ha party, notifica solo a lui
    IF v_party_id IS NULL OR v_party_id = 0 THEN
        INSERT INTO srv1_hunabku.hunter_party_notifications 
            (player_id, notification_type, source_name, glory_received, glory_total, 
             actor_name, actor_rank, color_code, extra_data)
        VALUES (p_actor_id, p_notification_type, p_source_name, p_glory_total, p_glory_total,
                p_actor_name, p_actor_rank, p_color_code, p_extra_data);
    ELSE
        -- Calcola power totale per meritocrazia
        SELECT SUM(
            CASE 
                WHEN COALESCE(r.total_points, 0) >= 100000 THEN 250
                WHEN COALESCE(r.total_points, 0) >= 50000 THEN 150
                WHEN COALESCE(r.total_points, 0) >= 20000 THEN 80
                WHEN COALESCE(r.total_points, 0) >= 8000 THEN 40
                WHEN COALESCE(r.total_points, 0) >= 3000 THEN 15
                WHEN COALESCE(r.total_points, 0) >= 500 THEN 5
                ELSE 1
            END
        ) INTO v_total_power
        FROM player.player p
        LEFT JOIN srv1_hunabku.hunter_quest_ranking r ON p.id = r.player_id
        WHERE p.pid = v_party_id;
        
        IF v_total_power < 1 THEN SET v_total_power = 1; END IF;
        
        -- Crea notifica per ogni membro del party
        OPEN member_cursor;
        
        notify_loop: LOOP
            FETCH member_cursor INTO v_pid, v_pname, v_points;
            IF done THEN
                LEAVE notify_loop;
            END IF;
            
            -- Calcola la quota di gloria per questo membro
            SET v_power = CASE 
                WHEN v_points >= 100000 THEN 250
                WHEN v_points >= 50000 THEN 150
                WHEN v_points >= 20000 THEN 80
                WHEN v_points >= 8000 THEN 40
                WHEN v_points >= 3000 THEN 15
                WHEN v_points >= 500 THEN 5
                ELSE 1
            END;
            
            SET v_share = FLOOR((v_power * p_glory_total) / v_total_power);
            IF v_share < 1 THEN SET v_share = 1; END IF;
            
            -- Inserisci notifica
            INSERT INTO srv1_hunabku.hunter_party_notifications 
                (player_id, notification_type, source_name, glory_received, glory_total, 
                 actor_name, actor_rank, color_code, extra_data)
            VALUES (v_pid, p_notification_type, p_source_name, v_share, p_glory_total,
                    p_actor_name, p_actor_rank, p_color_code, p_extra_data);
        END LOOP;
        
        CLOSE member_cursor;
    END IF;
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for sp_party_glory_complete
-- ----------------------------
DROP PROCEDURE IF EXISTS `sp_party_glory_complete`;
delimiter ;;
CREATE PROCEDURE `sp_party_glory_complete`(IN p_actor_id INT,
    IN p_actor_name VARCHAR(50),
    IN p_base_glory INT,
    IN p_source_type VARCHAR(30),
    IN p_source_name VARCHAR(100),
    IN p_color_code VARCHAR(20),
    IN p_extra_data VARCHAR(255))
BEGIN
    DECLARE v_party_id INT DEFAULT 0;
    DECLARE v_total_power INT DEFAULT 0;
    DECLARE v_actor_rank VARCHAR(10) DEFAULT 'E';
    DECLARE v_actor_points INT DEFAULT 0;
    DECLARE done INT DEFAULT FALSE;
    DECLARE v_pid INT;
    DECLARE v_pname VARCHAR(50);
    DECLARE v_points INT;
    DECLARE v_power INT;
    DECLARE v_share INT;
    DECLARE v_member_count INT DEFAULT 0;
    
    DECLARE member_cursor CURSOR FOR
        SELECT p.id, p.name, COALESCE(r.total_points, 0) as points
        FROM player.player p
        LEFT JOIN srv1_hunabku.hunter_quest_ranking r ON p.id = r.player_id
        WHERE p.pid = v_party_id;
    
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
    
    -- Ottieni rank dell'attore
    SELECT COALESCE(total_points, 0) INTO v_actor_points
    FROM srv1_hunabku.hunter_quest_ranking
    WHERE player_id = p_actor_id;
    
    SET v_actor_rank = CASE 
        WHEN v_actor_points >= 100000 THEN 'N'
        WHEN v_actor_points >= 50000 THEN 'S'
        WHEN v_actor_points >= 20000 THEN 'A'
        WHEN v_actor_points >= 8000 THEN 'B'
        WHEN v_actor_points >= 3000 THEN 'C'
        WHEN v_actor_points >= 500 THEN 'D'
        ELSE 'E'
    END;
    
    -- Trova il party_id
    SELECT pid INTO v_party_id 
    FROM player.player 
    WHERE id = p_actor_id;
    
    -- === SOLO PLAYER (no party) ===
    IF v_party_id IS NULL OR v_party_id = 0 THEN
        -- Assegna gloria
        UPDATE srv1_hunabku.hunter_quest_ranking 
        SET total_points = total_points + p_base_glory,
            spendable_points = spendable_points + p_base_glory
        WHERE player_id = p_actor_id;
        
        -- Crea notifica
        INSERT INTO srv1_hunabku.hunter_party_notifications 
            (player_id, notification_type, source_name, glory_received, glory_total, 
             actor_name, actor_rank, color_code, extra_data)
        VALUES (p_actor_id, p_source_type, p_source_name, p_base_glory, p_base_glory,
                p_actor_name, v_actor_rank, p_color_code, p_extra_data);
        
        SELECT 1 AS members_rewarded, p_base_glory AS glory_each, v_actor_rank AS actor_rank;
    
    -- === PARTY MODE ===
    ELSE
        -- Calcola power totale
        SELECT SUM(
            CASE 
                WHEN COALESCE(r.total_points, 0) >= 100000 THEN 250
                WHEN COALESCE(r.total_points, 0) >= 50000 THEN 150
                WHEN COALESCE(r.total_points, 0) >= 20000 THEN 80
                WHEN COALESCE(r.total_points, 0) >= 8000 THEN 40
                WHEN COALESCE(r.total_points, 0) >= 3000 THEN 15
                WHEN COALESCE(r.total_points, 0) >= 500 THEN 5
                ELSE 1
            END
        ) INTO v_total_power
        FROM player.player p
        LEFT JOIN srv1_hunabku.hunter_quest_ranking r ON p.id = r.player_id
        WHERE p.pid = v_party_id;
        
        IF v_total_power < 1 THEN SET v_total_power = 1; END IF;
        
        -- Itera e distribuisci + notifica
        OPEN member_cursor;
        
        party_loop: LOOP
            FETCH member_cursor INTO v_pid, v_pname, v_points;
            IF done THEN
                LEAVE party_loop;
            END IF;
            
            -- Power di questo membro
            SET v_power = CASE 
                WHEN v_points >= 100000 THEN 250
                WHEN v_points >= 50000 THEN 150
                WHEN v_points >= 20000 THEN 80
                WHEN v_points >= 8000 THEN 40
                WHEN v_points >= 3000 THEN 15
                WHEN v_points >= 500 THEN 5
                ELSE 1
            END;
            
            -- Quota gloria
            SET v_share = FLOOR((v_power * p_base_glory) / v_total_power);
            IF v_share < 1 THEN SET v_share = 1; END IF;
            
            -- Assegna gloria
            INSERT INTO srv1_hunabku.hunter_quest_ranking 
                (player_id, player_name, total_points, spendable_points)
            VALUES (v_pid, v_pname, v_share, v_share)
            ON DUPLICATE KEY UPDATE
                total_points = total_points + v_share,
                spendable_points = spendable_points + v_share;
            
            -- Crea notifica
            INSERT INTO srv1_hunabku.hunter_party_notifications 
                (player_id, notification_type, source_name, glory_received, glory_total, 
                 actor_name, actor_rank, color_code, extra_data)
            VALUES (v_pid, p_source_type, p_source_name, v_share, p_base_glory,
                    p_actor_name, v_actor_rank, p_color_code, p_extra_data);
            
            -- Log storico
            INSERT INTO srv1_hunabku.hunter_pending_rewards 
                (player_id, player_name, glory_amount, source_type, source_name, 
                 opener_id, opener_name, claimed, claimed_at)
            VALUES (v_pid, v_pname, v_share, p_source_type, p_source_name, 
                    p_actor_id, p_actor_name, 1, NOW());
            
            SET v_member_count = v_member_count + 1;
        END LOOP;
        
        CLOSE member_cursor;
        
        SELECT v_member_count AS members_rewarded, p_base_glory AS total_glory, v_actor_rank AS actor_rank;
    END IF;
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for sp_select_gate_players
-- ----------------------------
DROP PROCEDURE IF EXISTS `sp_select_gate_players`;
delimiter ;;
CREATE PROCEDURE `sp_select_gate_players`()
BEGIN
    DECLARE v_players_count INT;
    DECLARE v_access_hours INT;
    DECLARE v_min_rank VARCHAR(2);
    DECLARE v_min_level INT;
    DECLARE v_min_points INT;
    DECLARE v_gate_id INT;
    
    -- Leggi config
    SELECT players_per_selection, access_duration_hours, min_rank, min_level, min_total_points
    INTO v_players_count, v_access_hours, v_min_rank, v_min_level, v_min_points
    FROM hunter_gate_selection_config LIMIT 1;
    
    -- Seleziona un gate casuale abilitato
    SELECT gate_id INTO v_gate_id 
    FROM hunter_gate_config 
    WHERE enabled = 1 
    ORDER BY RAND() 
    LIMIT 1;
    
    IF v_gate_id IS NOT NULL THEN
        -- Inserisci giocatori selezionati casualmente
        INSERT INTO hunter_gate_access (player_id, player_name, gate_id, expires_at)
        SELECT 
            r.player_id,
            r.player_name,
            v_gate_id,
            DATE_ADD(NOW(), INTERVAL v_access_hours HOUR)
        FROM hunter_quest_ranking r
        WHERE r.total_points >= v_min_points
          AND NOT EXISTS (
              -- Non selezionare chi ha già un accesso pending
              SELECT 1 FROM hunter_gate_access ga 
              WHERE ga.player_id = r.player_id 
              AND ga.status = 'pending' 
              AND ga.expires_at > NOW()
          )
          AND NOT EXISTS (
              -- Non selezionare chi ha completato un gate nelle ultime 24 ore
              SELECT 1 FROM hunter_gate_history gh
              WHERE gh.player_id = r.player_id
              AND gh.completed_at > DATE_SUB(NOW(), INTERVAL 24 HOUR)
          )
        ORDER BY RAND()
        LIMIT v_players_count;
        
        -- Aggiorna timestamp ultima selezione
        UPDATE hunter_gate_selection_config SET last_selection_at = NOW();
    END IF;
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for sp_start_rank_trial
-- ----------------------------
DROP PROCEDURE IF EXISTS `sp_start_rank_trial`;
delimiter ;;
CREATE PROCEDURE `sp_start_rank_trial`(IN p_player_id INT,
    IN p_current_rank VARCHAR(2),
    OUT p_trial_id INT,
    OUT p_trial_name VARCHAR(128),
    OUT p_success TINYINT,
    OUT p_message VARCHAR(255))
BEGIN
    DECLARE v_player_gloria INT;
    DECLARE v_player_level INT;
    DECLARE v_required_gloria INT;
    DECLARE v_required_level INT;
    DECLARE v_time_limit INT;
    DECLARE v_existing_status VARCHAR(20);

    -- Trova la prova disponibile per il rank attuale
    SELECT trial_id, trial_name, required_gloria, required_level, time_limit_hours
    INTO p_trial_id, p_trial_name, v_required_gloria, v_required_level, v_time_limit
    FROM hunter_rank_trials
    WHERE from_rank = p_current_rank AND enabled = 1
    LIMIT 1;
    
    IF p_trial_id IS NULL THEN
        SET p_success = 0;
        SET p_message = 'Nessuna prova disponibile per il tuo rank.';
    ELSE
        -- Controlla se il giocatore ha GIA' una riga per questa prova
        SELECT status INTO v_existing_status
        FROM hunter_player_trials
        WHERE player_id = p_player_id AND trial_id = p_trial_id;
        
        -- Se la prova è già in corso o completata, non fare nulla e esci
        IF v_existing_status = 'in_progress' OR v_existing_status = 'completed' THEN
            SET p_success = 0;
            SET p_message = 'Prova già in corso o completata.';
        ELSE
            -- Controlla i requisiti solo se la prova non è attiva
            SELECT total_points INTO v_player_gloria FROM hunter_quest_ranking WHERE player_id = p_player_id;
            
            -- Ottieni il livello del giocatore (questo richiede un modo per passarlo o assumerlo)
            -- Per ora, omettiamo il controllo del livello qui e lo lasciamo alla quest LUA
            
            IF v_player_gloria < v_required_gloria THEN
                SET p_success = 0;
                SET p_message = CONCAT('Gloria insufficiente. Richiesti: ', v_required_gloria);
            ELSE
                -- INIZIA LA PROVA: Usa INSERT IGNORE per creare la riga solo se non esiste.
                -- Se esiste (ma è 'failed' o altro), l'UPDATE successivo la resetterà.
                
                INSERT INTO hunter_player_trials (player_id, trial_id, status, started_at, expires_at, boss_kills, metin_kills, fracture_seals, chest_opens, daily_missions)
                VALUES (p_player_id, p_trial_id, 'in_progress', NOW(), 
                        IF(v_time_limit IS NOT NULL, DATE_ADD(NOW(), INTERVAL v_time_limit HOUR), NULL),
                        0, 0, 0, 0, 0)
                ON DUPLICATE KEY UPDATE 
                    status = 'in_progress', 
                    started_at = NOW(),
                    expires_at = IF(v_time_limit IS NOT NULL, DATE_ADD(NOW(), INTERVAL v_time_limit HOUR), NULL),
                    boss_kills = 0, 
                    metin_kills = 0, 
                    fracture_seals = 0, 
                    chest_opens = 0, 
                    daily_missions = 0;

                SET p_success = 1;
                SET p_message = CONCAT('Prova iniziata: ', p_trial_name);
            END IF;
        END IF;
    END IF;
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for sp_update_trial_progress
-- ----------------------------
DROP PROCEDURE IF EXISTS `sp_update_trial_progress`;
delimiter ;;
CREATE PROCEDURE `sp_update_trial_progress`(IN p_player_id INT,
    IN p_progress_type VARCHAR(32),
    IN p_vnum INT,
    IN p_amount INT)
BEGIN
    DECLARE v_trial_id INT;
    DECLARE v_boss_list VARCHAR(255);
    DECLARE v_metin_list VARCHAR(255);
    DECLARE v_fracture_list VARCHAR(128);
    DECLARE v_chest_list VARCHAR(255);
    DECLARE v_vnum_str VARCHAR(16);
    
    SET v_vnum_str = CAST(p_vnum AS CHAR);
    
    -- Trova prova in corso
    SELECT pt.trial_id, rt.boss_vnum_list, rt.metin_vnum_list, rt.fracture_color_list, rt.chest_vnum_list
    INTO v_trial_id, v_boss_list, v_metin_list, v_fracture_list, v_chest_list
    FROM hunter_player_trials pt
    JOIN hunter_rank_trials rt ON pt.trial_id = rt.trial_id
    WHERE pt.player_id = p_player_id AND pt.status = 'in_progress'
    AND (pt.expires_at IS NULL OR pt.expires_at > NOW())
    LIMIT 1;
    
    IF v_trial_id IS NOT NULL THEN
        CASE p_progress_type
            WHEN 'boss_kill' THEN
                IF v_boss_list IS NULL OR FIND_IN_SET(v_vnum_str, v_boss_list) > 0 THEN
                    UPDATE hunter_player_trials SET boss_kills = boss_kills + p_amount WHERE player_id = p_player_id AND trial_id = v_trial_id;
                END IF;
            WHEN 'metin_kill' THEN
                IF v_metin_list IS NULL OR FIND_IN_SET(v_vnum_str, v_metin_list) > 0 THEN
                    UPDATE hunter_player_trials SET metin_kills = metin_kills + p_amount WHERE player_id = p_player_id AND trial_id = v_trial_id;
                END IF;
            WHEN 'fracture_seal' THEN
                -- p_vnum qui è il colore come stringa (passato come 0 se non serve)
                UPDATE hunter_player_trials SET fracture_seals = fracture_seals + p_amount WHERE player_id = p_player_id AND trial_id = v_trial_id;
            WHEN 'chest_open' THEN
                IF v_chest_list IS NULL OR FIND_IN_SET(v_vnum_str, v_chest_list) > 0 THEN
                    UPDATE hunter_player_trials SET chest_opens = chest_opens + p_amount WHERE player_id = p_player_id AND trial_id = v_trial_id;
                END IF;
            WHEN 'daily_mission' THEN
                UPDATE hunter_player_trials SET daily_missions = daily_missions + p_amount WHERE player_id = p_player_id AND trial_id = v_trial_id;
        END CASE;
    END IF;
END
;;
delimiter ;

-- ----------------------------
-- Event structure for evt_daily_mission_reset
-- ----------------------------
DROP EVENT IF EXISTS `evt_daily_mission_reset`;
delimiter ;;
CREATE EVENT `evt_daily_mission_reset`
ON SCHEDULE
EVERY '1' DAY STARTS '2025-12-24 00:05:00'
DO BEGIN
    -- Applica penalita per missioni non completate
    CALL sp_apply_daily_penalties();
END
;;
delimiter ;

-- ----------------------------
-- Event structure for evt_expire_trials
-- ----------------------------
DROP EVENT IF EXISTS `evt_expire_trials`;
delimiter ;;
CREATE EVENT `evt_expire_trials`
ON SCHEDULE
EVERY '1' HOUR STARTS '2025-12-29 15:17:44'
DO BEGIN
    UPDATE hunter_player_trials 
    SET status = 'expired' 
    WHERE status = 'in_progress' 
    AND expires_at < NOW();
    
    DELETE FROM hunter_player_missions 
    WHERE assigned_date < CURDATE() - INTERVAL 7 DAY;
END
;;
delimiter ;

-- ----------------------------
-- Event structure for evt_gate_expire_access
-- ----------------------------
DROP EVENT IF EXISTS `evt_gate_expire_access`;
delimiter ;;
CREATE EVENT `evt_gate_expire_access`
ON SCHEDULE
EVERY '1' HOUR STARTS '2025-12-27 02:42:42'
DO UPDATE hunter_gate_access 
    SET status = 'expired'
    WHERE status = 'pending' AND expires_at < NOW()
;;
delimiter ;

-- ----------------------------
-- Event structure for evt_gate_player_selection
-- ----------------------------
DROP EVENT IF EXISTS `evt_gate_player_selection`;
delimiter ;;
CREATE EVENT `evt_gate_player_selection`
ON SCHEDULE
EVERY '4' HOUR STARTS '2025-12-27 02:42:42'
DO CALL sp_select_gate_players()
;;
delimiter ;

-- ----------------------------
-- Event structure for evt_hunter_log_cleanup
-- ----------------------------
DROP EVENT IF EXISTS `evt_hunter_log_cleanup`;
delimiter ;;
CREATE EVENT `evt_hunter_log_cleanup`
ON SCHEDULE
EVERY '1' WEEK STARTS '2026-01-07 04:00:00'
DO CALL sp_hunter_log_cleanup()
;;
delimiter ;

-- ----------------------------
-- Event structure for evt_trial_expire
-- ----------------------------
DROP EVENT IF EXISTS `evt_trial_expire`;
delimiter ;;
CREATE EVENT `evt_trial_expire`
ON SCHEDULE
EVERY '1' HOUR STARTS '2025-12-27 02:42:42'
DO UPDATE hunter_player_trials 
    SET status = 'failed'
    WHERE status = 'in_progress' 
    AND expires_at IS NOT NULL 
    AND expires_at < NOW()
;;
delimiter ;

SET FOREIGN_KEY_CHECKS = 1;
