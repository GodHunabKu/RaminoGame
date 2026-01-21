-- ============================================================================
-- HUNTER SYSTEM - DETAILED STATISTICS MIGRATION
-- ============================================================================
-- Adds detailed grade-specific and type-specific statistics tracking
-- to the Hunter Quest Ranking system.
--
-- This migration adds columns for:
-- - Chests opened by grade (E, D, C, B, A, S, N)
-- - Boss kills by difficulty tier
-- - Metin kills by type
-- - Defense win/loss tracking
-- - Elite mob kills
-- ============================================================================

USE `srv1_hunabku`;

-- Add detailed chest statistics (by grade)
ALTER TABLE `hunter_quest_ranking`
ADD COLUMN `chests_e` INT UNSIGNED NOT NULL DEFAULT 0 COMMENT 'E-Rank chests opened' AFTER `total_chests`,
ADD COLUMN `chests_d` INT UNSIGNED NOT NULL DEFAULT 0 COMMENT 'D-Rank chests opened' AFTER `chests_e`,
ADD COLUMN `chests_c` INT UNSIGNED NOT NULL DEFAULT 0 COMMENT 'C-Rank chests opened' AFTER `chests_d`,
ADD COLUMN `chests_b` INT UNSIGNED NOT NULL DEFAULT 0 COMMENT 'B-Rank chests opened' AFTER `chests_c`,
ADD COLUMN `chests_a` INT UNSIGNED NOT NULL DEFAULT 0 COMMENT 'A-Rank chests opened' AFTER `chests_b`,
ADD COLUMN `chests_s` INT UNSIGNED NOT NULL DEFAULT 0 COMMENT 'S-Rank chests opened' AFTER `chests_a`,
ADD COLUMN `chests_n` INT UNSIGNED NOT NULL DEFAULT 0 COMMENT 'N-Rank chests opened' AFTER `chests_s`;

-- Add detailed boss kill statistics (by difficulty)
ALTER TABLE `hunter_quest_ranking`
ADD COLUMN `boss_kills_easy` INT UNSIGNED NOT NULL DEFAULT 0 COMMENT 'Easy boss kills' AFTER `chests_n`,
ADD COLUMN `boss_kills_medium` INT UNSIGNED NOT NULL DEFAULT 0 COMMENT 'Medium boss kills' AFTER `boss_kills_easy`,
ADD COLUMN `boss_kills_hard` INT UNSIGNED NOT NULL DEFAULT 0 COMMENT 'Hard boss kills' AFTER `boss_kills_medium`,
ADD COLUMN `boss_kills_elite` INT UNSIGNED NOT NULL DEFAULT 0 COMMENT 'Elite/Epic boss kills' AFTER `boss_kills_hard`;

-- Add detailed metin statistics
ALTER TABLE `hunter_quest_ranking`
ADD COLUMN `metin_kills_normal` INT UNSIGNED NOT NULL DEFAULT 0 COMMENT 'Normal metin kills' AFTER `boss_kills_elite`,
ADD COLUMN `metin_kills_special` INT UNSIGNED NOT NULL DEFAULT 0 COMMENT 'Special/Event metin kills' AFTER `metin_kills_normal`;

-- Add fracture defense statistics
ALTER TABLE `hunter_quest_ranking`
ADD COLUMN `defense_wins` INT UNSIGNED NOT NULL DEFAULT 0 COMMENT 'Fracture defenses won' AFTER `metin_kills_special`,
ADD COLUMN `defense_losses` INT UNSIGNED NOT NULL DEFAULT 0 COMMENT 'Fracture defenses lost' AFTER `defense_wins`;

-- Add elite mob kills
ALTER TABLE `hunter_quest_ranking`
ADD COLUMN `elite_kills` INT UNSIGNED NOT NULL DEFAULT 0 COMMENT 'Elite mob kills' AFTER `defense_losses`;

-- Create indexes for frequently queried detailed stats (simple columns only)
CREATE INDEX `idx_elite_kills` ON `hunter_quest_ranking`(`elite_kills` DESC) COMMENT 'Index for elite kills leaderboard';

CREATE INDEX `idx_defense_wins` ON `hunter_quest_ranking`(`defense_wins` DESC) COMMENT 'Index for defense wins leaderboard';

-- ============================================================================
-- VERIFICATION QUERIES
-- ============================================================================

-- Verify new columns were added
SELECT
    COLUMN_NAME,
    COLUMN_TYPE,
    COLUMN_DEFAULT,
    COLUMN_COMMENT
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'srv1_hunabku'
    AND TABLE_NAME = 'hunter_quest_ranking'
    AND COLUMN_NAME IN (
        'chests_e', 'chests_d', 'chests_c', 'chests_b', 'chests_a', 'chests_s', 'chests_n',
        'boss_kills_easy', 'boss_kills_medium', 'boss_kills_hard', 'boss_kills_elite',
        'metin_kills_normal', 'metin_kills_special',
        'defense_wins', 'defense_losses',
        'elite_kills'
    )
ORDER BY ORDINAL_POSITION;

-- Sample query to show detailed stats (example)
-- SELECT
--     player_name,
--     hunter_rank,
--     -- Chest breakdown
--     chests_e AS 'E-Chests',
--     chests_d AS 'D-Chests',
--     chests_c AS 'C-Chests',
--     chests_b AS 'B-Chests',
--     chests_a AS 'A-Chests',
--     chests_s AS 'S-Chests',
--     chests_n AS 'N-Chests',
--     -- Boss breakdown
--     boss_kills_easy AS 'Easy',
--     boss_kills_medium AS 'Medium',
--     boss_kills_hard AS 'Hard',
--     boss_kills_elite AS 'Elite',
--     -- Defense stats
--     defense_wins AS 'Wins',
--     defense_losses AS 'Losses',
--     ROUND(defense_wins * 100.0 / NULLIF(defense_wins + defense_losses, 0), 1) AS 'Win%'
-- FROM hunter_quest_ranking
-- WHERE player_id = ?;
