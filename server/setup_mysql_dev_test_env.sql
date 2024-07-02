-- Prepares a MySQL server for the project--
CREATE DATABASE IF NOT EXISTS aedc_subscription_tracker;
GRANT ALL PRIVILEGES ON `aedc_subscription_tracker`.* TO 'sam'@'127.0.0.1';
FLUSH PRIVILEGES;