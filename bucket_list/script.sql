CREATE TABLE users(
	user_id BIGINT NOT NULL AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL,
    password VARCHAR(200) NOT NULL
    PRIMARY KEY (user_id));

DELIMITER $$
CREATE DEFINER=root@localhost PROCEDURE sp_createUser(
    IN p_first_name VARCHAR(50),
    IN p_last_name VARCHAR(50),
    IN p_username VARCHAR(50),
    IN p_email VARCHAR(50),
    IN p_password VARCHAR(200)
)
BEGIN
    if ( select exists (select 1 from users where username = p_username) ) THEN
     
        select 'Username Exists !!';
     
    ELSE
     
        insert into users
        (
            first_name,
            last_name,
            username,
            email,
            password
        )
        values
        (
            p_first_name,
            p_last_name,
            p_username,
            p_email,
            p_password
        );
     
    END IF;
END$$
DELIMITER ;

CREATE TABLE bucketlist_tasks(
    task_id BIGINT NOT NULL AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    task_description VARCHAR(200) NOT NULL,
    date_created DATETIME NOT NULL,
    completed BOOLEAN NOT NULL,
    PRIMARY KEY (task_id));

DELIMITER $$
CREATE DEFINER=johnnyyeo@localhost PROCEDURE sp_createTask(
    IN puser_id VARCHAR(50),
    IN ptask_description VARCHAR(50),
    IN pdate_created DATETIME
)
BEGIN

    insert into users
    (
        user_id,
        task_description,
        date_created,
        completed
    )
    values
    (
        puser_id,
        ptask_description,
        pdate_created,
        FALSE
    );

END$$
DELIMITER ;


GRANT ALL PRIVILEGES ON BucketList.* To 'johnnyyeo'@'localhost' IDENTIFIED BY 'abcd1234';