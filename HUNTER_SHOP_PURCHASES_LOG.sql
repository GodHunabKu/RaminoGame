-- ============================================================
-- HUNTER SHOP PURCHASES LOG TABLE
-- Track all shop transactions for auditing and anti-exploit
-- ============================================================

CREATE TABLE IF NOT EXISTS `srv1_hunabku`.`hunter_shop_purchases` (
  `purchase_id` BIGINT NOT NULL AUTO_INCREMENT,
  `player_id` INT NOT NULL,
  `player_name` VARCHAR(50) NOT NULL,
  `item_id` INT NOT NULL COMMENT 'ID from hunter_quest_shop',
  `item_vnum` INT NOT NULL COMMENT 'Actual item vnum purchased',
  `item_count` INT NOT NULL DEFAULT 1,
  `price_paid` INT NOT NULL COMMENT 'Glory points spent',
  `purchased_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`purchase_id`),
  INDEX `idx_player_id` (`player_id`),
  INDEX `idx_purchased_at` (`purchased_at`),
  INDEX `idx_item_id` (`item_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Shop purchase audit log';

-- ============================================================
-- QUERY UTILI PER MONITORAGGIO
-- ============================================================

-- Vedi tutti gli acquisti di un player
-- SELECT * FROM srv1_hunabku.hunter_shop_purchases WHERE player_id = PLAYER_ID ORDER BY purchased_at DESC;

-- Vedi gli acquisti più recenti (ultime 24 ore)
-- SELECT * FROM srv1_hunabku.hunter_shop_purchases WHERE purchased_at >= DATE_SUB(NOW(), INTERVAL 24 HOUR) ORDER BY purchased_at DESC;

-- Trova acquisti sospetti (stesso player, stesso item, in breve tempo)
-- SELECT player_id, player_name, item_id, COUNT(*) as count,
--        MIN(purchased_at) as first_purchase, MAX(purchased_at) as last_purchase,
--        TIMESTAMPDIFF(SECOND, MIN(purchased_at), MAX(purchased_at)) as seconds_diff
-- FROM srv1_hunabku.hunter_shop_purchases
-- WHERE purchased_at >= DATE_SUB(NOW(), INTERVAL 1 HOUR)
-- GROUP BY player_id, item_id
-- HAVING count > 3 AND seconds_diff < 60;

-- Totale gloria spesa per player (tutte)
-- SELECT player_id, player_name, SUM(price_paid) as total_spent, COUNT(*) as total_purchases
-- FROM srv1_hunabku.hunter_shop_purchases
-- GROUP BY player_id, player_name
-- ORDER BY total_spent DESC
-- LIMIT 50;

-- Item più acquistati
-- SELECT item_id, item_vnum, COUNT(*) as purchase_count, SUM(price_paid) as total_glory_spent
-- FROM srv1_hunabku.hunter_shop_purchases
-- GROUP BY item_id, item_vnum
-- ORDER BY purchase_count DESC
-- LIMIT 20;
