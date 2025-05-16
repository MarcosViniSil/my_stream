SET NAMES 'utf8mb4';

CREATE TABLE tb_user(
    userId BINARY(16) PRIMARY KEY,
    userName VARCHAR(255) NOT NULL,
    userRole VARCHAR(7) NOT NULL CHECK (userRole IN ('USER', 'ADMIN')),
    userEmail VARCHAR(255) NOT NULL,
    userPassword VARCHAR(255) NOT NULL
);

CREATE TABLE tb_userCodeVerification(
    userCodeId BINARY(16) PRIMARY KEY,
    code VARCHAR(255) NOT NULL,
    codeType VARCHAR(255) NOT NULL,
    createdAt DATE NOT NULL,
    expiresAt DATE NOT NULL,
    isCodeUsed BOOLEAN NOT NULL,
    idUser BINARY(16) NOT NULL
);

CREATE TABLE tb_videoHistory(
    historyId BINARY(16) PRIMARY KEY,
    userId BINARY(16) NOT NULL,
    videoId BINARY(16) NOT NULL,
    lastViewAt INT
);

CREATE TABLE tb_video(
    videoId BINARY(16) PRIMARY KEY UNIQUE,
    videoTitle VARCHAR(255) UNIQUE ,
    thumbnailUrl VARCHAR(255) UNIQUE,
    videoUrl VARCHAR(255) UNIQUE,
    videoStatus VARCHAR(10) NOT NULL CHECK (videoStatus IN ('READY', 'PROCESSING','FAIL')),
    videoDuration INT ,
    lastStreaming DATE,
    isVideoAvailable BOOLEAN NOT NULL,
    idAdmin BINARY(16)
);

CREATE TABLE tb_videoReaction(
    videoId BINARY(16) ,
    videoLikes INT,
    videoDislikes INT,
    FOREIGN KEY (videoId) REFERENCES tb_video(videoId)
);

CREATE TABLE tb_userVideoReaction(
    userVideoReactionId BINARY(16) PRIMARY KEY,
    userId BINARY(16),
    videoId BINARY(16) ,
    createdAt DATE NOT NULL,
    reactionType INT NOT NULL
);

ALTER TABLE tb_userCodeVerification ADD FOREIGN KEY (idUser) REFERENCES tb_user(userId);
ALTER TABLE tb_video ADD FOREIGN KEY (idAdmin) REFERENCES tb_user(userId);
ALTER TABLE tb_userVideoReaction ADD FOREIGN KEY (userId) REFERENCES tb_user(userId);
ALTER TABLE tb_userVideoReaction ADD FOREIGN KEY (videoId) REFERENCES tb_video(videoId);

ALTER TABLE tb_videoHistory ADD FOREIGN KEY (videoId) REFERENCES tb_video(videoId);
ALTER TABLE tb_videoHistory ADD FOREIGN KEY (userId) REFERENCES tb_user(userId);

-- UUID_TO_BIN(UUID(), 1) -> INSERT

INSERT INTO tb_user (userId,userName,userRole,userEmail,userPassword) VALUES (UNHEX(REPLACE('3f06af63-a93c-11e4-9797-00505690773f', '-','')),'testUser','ADMIN','testemail@gmail.com','12345678');
