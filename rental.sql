CREATE TABLE IF NOT EXISTS users
(
userID INT auto_increment PRIMARY KEY NOT NULL,
userPermission INT NOT NULL,
-- 1 is admin, 2 is staff, 3 is customer
userName VARCHAR(80) NOT NULL,
userPassword VARCHAR NOT NULL,
email VARCHAR(255) NOT NULL,
phoneNumber BIGINT,
userAddress VARCHAR(200)
);

CREATE TABLE IF NOT EXISTS cars
(
carID INT auto_increment PRIMARY KEY NOT NULL,
rego VARCHAR(6) NOT NULL,
brand VARCHAR(50) NOT NULL,
model VARCHAR(50) NOT NULL,
yearBuild INT NOT NULL,
seat INT NOT NULL,
price DECIMAL(10,2)
);