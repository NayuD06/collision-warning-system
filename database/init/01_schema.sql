-- Phải khớp với các model trong BE/app/models/

CREATE TABLE IF NOT EXISTS alerts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    level VARCHAR(20) NOT NULL,
    message VARCHAR(255) NOT NULL,
    vehicle_a_plate VARCHAR(20) NULL,
    vehicle_b_plate VARCHAR(20) NULL,
    ttc_seconds FLOAT NULL,
    is_resolved BOOLEAN NOT NULL DEFAULT FALSE,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX ix_alerts_level (level)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
