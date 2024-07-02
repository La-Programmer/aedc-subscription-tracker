-- Prepares a MySQL server for the project--
CREATE DATABASE IF NOT EXISTS aedc_subscription_tracker;
CREATE USER IF NOT EXISTS 'aedc_test_env_user'@'127.0.0.1' IDENTIFIED BY 'aedc@1**23&4';
GRANT ALL PRIVILEGES ON `aedc_subscription_tracker`.* TO 'aedc_test_env_user'@'127.0.0.1';
GRANT SELECT ON `performance_schema`.* TO 'aedc_test_env_user'@'127.0.0.1';
FLUSH PRIVILEGES;