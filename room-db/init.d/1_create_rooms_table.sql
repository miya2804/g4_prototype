CREATE DATABASE rooms;
USE rooms;

CREATE TABLE rooms (
       id int auto_increment not null,
       password varchar(30) not null,
       primary key (id)
);
