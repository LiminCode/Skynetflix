
DROP TABLE IF EXISTS plan;
create table plan
(
    name            varchar(50),
    month_length    numeric(2,0),
    total_price     numeric(15,2),
    primary key (name)
);
--
DROP TABLE IF EXISTS director;
create table director
(
    id            varchar(5),
    first_name    varchar(20),
    last_name     varchar(20) not null,
    age           varchar(3) check (age > 0),
    primary key (id)
);
--
DROP TABLE IF EXISTS studio;
create table studio
(
    name          varchar(20),
    date_founded  date,
    budget        numeric(12,2) check (budget > 0),
    primary key (name)
);
--
DROP TABLE IF EXISTS actor;
create table actor
(
    id            varchar(10),
    first_name    varchar(30),
    last_name     varchar(30) not null,
    gender        varchar(1),
    age           varchar(3) check (age > 0),
    primary key (id)
);
--
DROP TABLE IF EXISTS users;
create table users
(
    id            varchar(5),
    first_name    varchar(20),
    last_name     varchar(20) not null,
    email         varchar(50) not null,
    phone_number  varchar(10),
    password      varchar(30) not null,
    primary key (id)
);
--
DROP  TABLE IF EXISTS movie;
create table movie
(
    id             varchar(10),
    title          varchar(50)  NOT NULL,
    url            varchar(100),
    genre          varchar(30),
    date_released  date,
    rating         varchar(5),
    budget         numeric(12,2) check (budget > 0),
    gross_income   numeric(12,2),
    summary        varchar(255),
    studio         varchar(20),
    director_id    varchar(10),
    primary key (id),
    foreign key (studio) references studio (name)
            on delete set null,
    foreign key (director_id) references director (id)
            on delete set null,
);
--
DROP TABLE IF EXISTS subscription;
create table subscription
(
    user_id         varchar(10),
    plan_name       varchar(50),
    start_date      date not null,
    purchased_date  date,
    primary key (user_id, plan_name, start_date)
    foreign key (user_id) references user (id)
            on delete cascade,
    foreign key (plan_name) references plan (name)
            on delete cascade
);
--
DROP TABLE IF EXISTS history;
create table history
(
    user_id         varchar(10),
    movie_id        varchar(10),
    watch_date      date not null,
    is_finished     boolean,
    primary key (user_id, movie_id),
    foreign key (user_id) references user (id)
            on delete cascade,
    foreign key (movie_id) references movie (id),
            on delete cascade
);
--
DROP TABLE IF EXISTS review;
create table review
(
    user_id         varchar(10),
    movie_id        varchar(10),
    review_date     date,
    rating          numeric(3,1) check (rating >= 0 and rating <= 100) not null,
    content         varchar(256),
    primary key (user_id, movie_id),
    foreign key (user_id) references user (id)
            on delete cascade,
    foreign key (movie_id) references movie (id)
            on delete cascade
);
--
DROP TABLE IF EXISTS act;
create table act
(
    movie_id        varchar(10),
    actor_id        varchar(10),
    if_main         boolean,
    role            varchar(50) not null,
    primary key (movie_id, actor_id),
    foreign key (movie_id) references movie (id)
            on delete cascade,
    foreign key (actor_id) references actor (id)
            on delete cascade
);
