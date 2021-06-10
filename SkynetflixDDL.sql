DROP TABLE IF EXISTS plan CASCADE;
create table plan
(
    name            varchar(50),
    month_length    interval,
    total_price     numeric(15,2),
    primary key (name)
);

-- test--
--
DROP TABLE IF EXISTS director CASCADE;
create table director
(
    id            integer GENERATED BY DEFAULT AS IDENTITY,
    first_name    varchar(20),
    last_name     varchar(20) not null,
    age           numeric(3,0) check (age > 0),
    primary key (id)
);
--
DROP TABLE IF EXISTS studio CASCADE;
create table studio
(
    name          varchar(50),
    date_founded  date,
    budget        numeric(12,2) check (budget > 0),
    primary key (name)
);
--
DROP TABLE IF EXISTS actor CASCADE;
create table actor
(
    id            integer GENERATED BY DEFAULT AS IDENTITY,
    first_name    varchar(30),
    last_name     varchar(30) not null,
    gender        varchar(1),
    age           numeric(3,0) check (age > 0),
    primary key (id)
);
--
DROP TABLE IF EXISTS users CASCADE;
create table users
(
    id            integer GENERATED BY DEFAULT AS IDENTITY,
    first_name    varchar(20),
    last_name     varchar(20) not null,
    email         varchar(50) not null,
    phone_number  varchar(10),
    password      varchar(30) not null,
    primary key (id)
);
--
DROP  TABLE IF EXISTS movie CASCADE;
create table movie
(
    id             integer GENERATED BY DEFAULT AS IDENTITY,
    title          varchar(50)  NOT NULL,
    url            varchar(100),
    genre          varchar(30),
    date_released  date,
    rating         varchar(5),
    budget         numeric(12,2) check (budget > 0),
    gross_income   numeric(12,2),
    summary        varchar(255),
    studio         varchar(50),
    director_id    integer,
    primary key (id),
    foreign key (studio) references studio (name) 
	    on delete set null,
    foreign key (director_id) references director (id)
            on delete set null
);
--
DROP TABLE IF EXISTS subscription CASCADE;
create table subscription
(
    user_id         integer,
    plan_name       varchar(50),
    start_date      date not null,
    purchased_date  date,
    primary key (user_id, plan_name, start_date),
    foreign key (user_id) references users (id)
            on delete cascade,
    foreign key (plan_name) references plan (name)
            on delete cascade
);
--
DROP TABLE IF EXISTS history CASCADE;
create table history
(
    user_id         integer,
    movie_id        integer,
    watch_date      date not null,
    is_finished     varchar(1),
    primary key (user_id, movie_id, watch_date),
    foreign key (user_id) references users (id)
            on delete cascade,
    foreign key (movie_id) references movie (id)
            on delete cascade
);
--
DROP TABLE IF EXISTS review CASCADE;
create table review
(
    user_id         integer,
    movie_id        integer,
    review_date     date,
    rating          numeric(4,1) check (rating >= 0 and rating <= 100) not null,
    content         varchar(256),
    primary key (user_id, movie_id),
    foreign key (user_id) references users (id)
            on delete cascade,
    foreign key (movie_id) references movie (id)
            on delete cascade
);
--
DROP TABLE IF EXISTS act CASCADE;
create table act
(
    movie_id        integer,
    actor_id        integer,
    if_main         varchar(1),
    role            varchar(50) not null,
    primary key (movie_id, actor_id),
    foreign key (movie_id) references movie (id)
            on delete cascade,
    foreign key (actor_id) references actor (id)
            on delete cascade
);
