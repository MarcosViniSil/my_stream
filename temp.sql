SET NAMES 'utf8mb4';

CREATE TABLE user(
    userId BINARY(16) PRIMARY KEY,
    userName VARCHAR(255) NOT NULL,
    userRole NOT NULL CHECK (role IN ('USER', 'ADMIN')),
    userEmail VARCHAR(255) NOT NULL,
    userPassword VARCHAR(255) NOT NULL,
);