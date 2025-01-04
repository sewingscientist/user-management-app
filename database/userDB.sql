-- This sql script contains some commands used to create the database beforehand within MySQL workbench
-- The table user_list was created within MySQL workbench using the import feature. user_list.csv was imported into
-- the database */

-- The database can be used to add, update, delete users
CREATE DATABASE usersDB;
USE usersDB;

-- Import CSV file to create table here. Table name = user_list here - change table name
-- accordingly to match DB table name. Reference to table in project to be updated if so.

-- Check the state of the table after your import
DESCRIBE user_list;

-- The following statements alter the table to set column constraints
ALTER TABLE user_list
MODIFY COLUMN id INT AUTO_INCREMENT PRIMARY KEY;

ALTER TABLE user_list MODIFY name text NOT NULL;

ALTER TABLE user_list MODIFY email text NOT NULL;

ALTER TABLE user_list MODIFY status text NOT NULL;

-- This statement can otherwise be used to create table manually
CREATE TABLE IF NOT EXISTS user_list (
                id INT PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                status VARCHAR(50) NOT NULL);

-- Add values to the table like below:
INSERT INTO `user_list` (name, email, status)
VALUES ('Test User', 'test@email.com', 'active');


-- Query to show all data in the database
SELECT * FROM user_list  -- can also just query table name after FROM
ORDER BY id; 


-- Code below can be used to delete entry from table - SQL_SAFE_UPDATES prevents accidental updates of data
SET SQL_SAFE_UPDATES = 0;
DELETE FROM user_list WHERE name='Mia';
SET SQL_SAFE_UPDATES = 1;


-- Query to select entry from database based on name
SELECT * FROM user_list WHERE name = "Mia";

-- Show only the name column from the table - change [name] to appropriate table field
SELECT name FROM user_list;


