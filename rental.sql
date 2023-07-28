CREATE TABLE IF NOT EXISTS users
(
userID INT auto_increment PRIMARY KEY NOT NULL,
userPermission INT NOT NULL,
-- 1 is admin, 2 is staff, 3 is customer
userName VARCHAR(80) NOT NULL,
userPassword VARCHAR(80) NOT NULL
);

CREATE TABLE IF NOT EXISTS staffinfo
(
userID INT PRIMARY KEY NOT NULL,
realName VARCHAR(80) NOT NULL,
email VARCHAR(255) NOT NULL,
phoneNumber BIGINT,
userAddress VARCHAR(200),

FOREIGN KEY (userID) REFERENCES users(userID)
ON UPDATE CASCADE
ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS customerinfo
(
userID INT PRIMARY KEY NOT NULL,
realName VARCHAR(80) NOT NULL,
email VARCHAR(255) NOT NULL,
phoneNumber BIGINT,
userAddress VARCHAR(200),

FOREIGN KEY (userID) REFERENCES users(userID)
ON UPDATE CASCADE
ON DELETE CASCADE
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

INSERT INTO cars(rego, brand, model, yearBuild, seat, price) VALUES 
('AAA000', 'Audi', 'A3',2000, 5 ,99.99),
('ADG657', 'Audi', 'A4',2015, 5 ,99.99),
('DXH666', 'Audi', 'A5',2011, 5 ,139.99),
('DGX474', 'Audi', 'A7',2019, 5 ,99.99),
('RST65', 'Audi', 'Q5',2022, 5 ,109.99),
('DFB888', 'BMW', 'M3',2005, 5 ,159.99),
('BD5765', 'BMW', 'M1',2018, 5 ,109.99),
('NHB385', 'BMW', 'M5',2000, 5 ,199.99),
('MNM90', 'BMW', '320i',2021, 5 ,159.99),
('FDS233', 'BMW', '535i',2020, 5 ,209.99),
('FGH567', 'TOYOTA', 'Corolla',2022, 5 ,109.99),
('BNG444', 'TOYOTA', 'Aqua',2014, 5 ,69.99),
('DGSFB3', 'TOYOTA', 'Prius',2011, 5 ,59.99),
('FBB555', 'TOYOTA', 'AE86',1985, 5 ,359.99),
('GFB6', 'TOYOTA', 'Hilux',2000, 7 ,359.99),
('SGF788', 'HONDA', 'Fit',2015, 5 ,49.99),
('HJG241', 'HONDA', 'Civic',2018, 5 ,59.99),
('FGB643', 'HONDA', 'Accord',2020, 5 ,89.99),
('SDF564', 'Mazda', '3',1995, 5 ,39.99),
('JFH675', 'Mazda', '6',1998, 5 ,39.99);

INSERT INTO users VALUES
-- test password: rental-HaochenZhu
(10001, 1, 'adminRental', '$2b$12$gJ3wlX6SdOYOx0k./7zdJ.dLzu9a6fQ5beTQVLf4bwBGHv7.cGY36'),
(10002, 2, 'staffRental1', '$2b$12$gJ3wlX6SdOYOx0k./7zdJ.dLzu9a6fQ5beTQVLf4bwBGHv7.cGY36'),
(10003, 2, 'staffRental2', '$2b$12$gJ3wlX6SdOYOx0k./7zdJ.dLzu9a6fQ5beTQVLf4bwBGHv7.cGY36'),
(10004, 2, 'staffRental3', '$2b$12$gJ3wlX6SdOYOx0k./7zdJ.dLzu9a6fQ5beTQVLf4bwBGHv7.cGY36'),
(10005, 3, 'custRental1', '$2b$12$gJ3wlX6SdOYOx0k./7zdJ.dLzu9a6fQ5beTQVLf4bwBGHv7.cGY36'),
(10006, 3, 'custRental2', '$2b$12$gJ3wlX6SdOYOx0k./7zdJ.dLzu9a6fQ5beTQVLf4bwBGHv7.cGY36'),
(10007, 3, 'custRental3', '$2b$12$gJ3wlX6SdOYOx0k./7zdJ.dLzu9a6fQ5beTQVLf4bwBGHv7.cGY36'),
(10008, 3, 'custRental4', '$2b$12$gJ3wlX6SdOYOx0k./7zdJ.dLzu9a6fQ5beTQVLf4bwBGHv7.cGY36'),
(10009, 3, 'custRental5', '$2b$12$gJ3wlX6SdOYOx0k./7zdJ.dLzu9a6fQ5beTQVLf4bwBGHv7.cGY36');

INSERT INTO staffInfo VALUES

(10001, 'Haochen', 'haochen.sam.zhu@gmail.com', 0220220222, 'Example Address'),
(10002, 'staff1Name', 'staff1@example.com', 0221111111, 'Example Address'),
(10003, 'staff2Name', 'staff2@example.com', 0221555511, 'Example Address'),
(10004, 'staff3Name', 'staff3@example.com', 0221566511, 'Example Address');

INSERT INTO customerInfo VALUES

(10005, 'cust1Name', 'cust1@example.com', 0224545451, 'Example Address'),
(10006, 'cust2Name', 'cust2@example.com', 0224546651, 'Example Address'),
(10007, 'cust3Name', 'cust3@example.com', 0257465451, 'Example Address'),
(10008, 'cust4Name', 'cust4@example.com', 0224567771, 'Example Address'),
(10009, 'cust5Name', 'cust5@example.com', 0243544451, 'Example Address');

