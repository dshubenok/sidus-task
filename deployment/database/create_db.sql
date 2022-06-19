CREATE USER admin_user WITH PASSWORD 'userPass123';
CREATE DATABASE sidus_db OWNER admin_user;

CREATE USER test_user WITH PASSWORD 'userPass123';
CREATE DATABASE test_db OWNER test_user;