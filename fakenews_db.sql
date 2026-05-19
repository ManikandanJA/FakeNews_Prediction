-- =====================================================
--  FAKE NEWS PREDICTION SYSTEM - Database Setup
--  Built by: Manikandan J.A.
--  Import Command: mysql -u root -p < fakenews_db.sql
-- =====================================================

-- Create & use database
CREATE DATABASE IF NOT EXISTS `fakenews_db`
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE `fakenews_db`;

-- ── Users Table ──────────────────────────────────────
CREATE TABLE IF NOT EXISTS `users` (
  `id`         INT          AUTO_INCREMENT PRIMARY KEY,
  `username`   VARCHAR(100) NOT NULL UNIQUE,
  `password`   VARCHAR(255) NOT NULL,
  `created_at` DATETIME     DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ── Predictions Table ─────────────────────────────────
CREATE TABLE IF NOT EXISTS `predictions` (
  `id`          INT           AUTO_INCREMENT PRIMARY KEY,
  `user_id`     INT           NOT NULL,
  `news_text`   TEXT          NOT NULL,
  `verdict`     VARCHAR(50),
  `confidence`  FLOAT,
  `method`      VARCHAR(50),
  `source_name` VARCHAR(200),
  `source_url`  VARCHAR(500),
  `reason`      TEXT,
  `created_at`  DATETIME      DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ── Sample Demo User (optional) ──────────────────────
-- Username: admin | Password: admin123
INSERT IGNORE INTO `users` (username, password)
VALUES ('admin', 'admin123');

-- ── Done ─────────────────────────────────────────────
SELECT 'fakenews_db setup complete!' AS Status;
