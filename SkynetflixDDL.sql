
--
DROP   TABLE IF EXISTS users CASCADE;
create table users
(
    id SERIAL PRIMARY KEY,
    first_name varchar(30), 
    last_name varchar(30), 
    email varchar(50) NOT NULL, 
    phone_number varchar(20), 
    password varchar(256)
);


--
DROP  TABLE IF EXISTS director CASCADE;
create table director
(
    id SERIAL PRIMARY KEY,
    first_name varchar(30)  NOT NULL, 
    last_name varchar(30)  NOT NULL, 
    info varchar(256)
);
--
DROP  TABLE IF EXISTS genre CASCADE;
create table genre
(
    name varchar(50) PRIMARY KEY,
    info varchar(200)
);
--
DROP  TABLE IF EXISTS studio CASCADE;
create table studio
(
    name varchar(50) PRIMARY KEY,
    date_founded date
);

--
DROP  TABLE IF EXISTS movie CASCADE;
create table movie
(
    id SERIAL PRIMARY KEY,
    title varchar(50)  NOT NULL, 
    url varchar(100), 
    genre varchar(50) references genre(name), 
    studio varchar(50) references studio(name),
    director INTEGER references director(id),
    date_produced date,
    total_rating_count INTEGER,
    total_rating INTEGER,
    available boolean,
    summary varchar(256)
);

--
DROP   TABLE IF EXISTS actor CASCADE;
create table actor
(
    id SERIAL PRIMARY KEY,
    first_name varchar(30)  NOT NULL, 
    last_name varchar(30)  NOT NULL, 
    info varchar(256)
);





--
DROP  TABLE IF EXISTS plan CASCADE;
create table plan
(
    name varchar(50) PRIMARY KEY,
    month_length INTERVAL,
    total_price numeric(15,3)
);

--
DROP  TABLE IF EXISTS subscription CASCADE;
create table subscription
(
    user_id INTEGER references users(id),
    plan_name varchar(50) references plan(name),
    start_date date,
    purchased_date date,
    PRIMARY KEY( user_id, plan_name, start_date)
);

--
DROP TABLE IF EXISTS history;
create table history
(
    user_id INTEGER references users(id),
    movie_id INTEGER references movie(id),
    watch_time date,
    --is_finished boolean,
    PRIMARY KEY( user_id, movie_id)
);

--
DROP TABLE IF EXISTS progress;
create table progress
(
    user_id INTEGER references users(id),
    movie_id INTEGER references movie(id),
    last_timestamp INTERVAL,
    PRIMARY KEY( user_id, movie_id)
);

--
DROP TABLE IF EXISTS review;
create table review
(
    user_id INTEGER references users(id),
    movie_id INTEGER references movie(id),
    date date,
    rating numeric(3,1) NOT NULL,
    content varchar(256),
    PRIMARY KEY( user_id, movie_id)
);

--
DROP TABLE IF EXISTS act;
create table act
(
    actor_id INTEGER references actor(id),
    movie_id INTEGER references movie(id),
    if_main boolean,
    role varchar(50) NOT NULL,
    PRIMARY KEY( actor_id, movie_id)
);