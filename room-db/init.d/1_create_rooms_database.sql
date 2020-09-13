CREATE DATABASE rooms;
USE rooms;

CREATE TABLE rooms (
       id int auto_increment not null,
       password varchar(30) not null,
       created_at datetime not null default current_timestamp,
       updated_at datetime not null default current_timestamp on update current_timestamp,
       primary key (id)
);
