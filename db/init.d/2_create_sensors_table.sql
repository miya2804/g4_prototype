USE ventilation;

CREATE TABLE sensors (
       id int auto_increment not null,
       room_id int not null,
       host varchar(30) not null,
       primary key (id)
);
