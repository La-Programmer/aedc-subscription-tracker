-- Prepares a MySQL server for the project--
CREATE DATABASE IF NOT EXISTS aedc_subscription_tracker;
CREATE USER IF NOT EXISTS 'aedc_user'@'localhost' IDENTIFIED BY 'aedc1234';
GRANT ALL PRIVILEGES ON 'aedc_subscription_tracker'.* TO 'aedc_user'@'localhost';
GRANT SELECT ON 'performance_schema'.* TO 'aedc_user'@'localhost';
FLUSH PRIVILEGES;