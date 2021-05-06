delete from act;
delete from actor;
delete from director;
delete from genre;
delete from history;
delete from movie;
delete from plan;
delete from progress;
delete from review;
delete from studio;
delete from subscription;
delete from users;



INSERT INTO "director" ("id", "first_name", "last_name", "age") VALUES ('1', 'Frank', 'Darabont', '62');
INSERT INTO "director" ("id", "first_name", "last_name", "age") VALUES ('3', 'Christopher', 'Nolan', '50');
INSERT INTO "director" ("id", "first_name", "last_name", "age") VALUES ('4', 'Sidney', 'Lumet', '87');
INSERT INTO "director" ("id", "first_name", "last_name", "age") VALUES ('5', 'Steven', 'Spielberg', '74');
INSERT INTO "director" ("id", "first_name", "last_name", "age") VALUES ('6', 'Peter', 'Jackson', '59');
INSERT INTO "director" ("id", "first_name", "last_name", "age") VALUES ('2', 'Francis', ' Coppola', '82');

INSERT INTO "studio" ("name", "date_founded", "budget") VALUES ('Warner Bros.', '1923-04-04', '6.00');
INSERT INTO "studio" ("name", "date_founded", "budget") VALUES ('Paramount Pictures', '1912-05-08', '4.00');
INSERT INTO "studio" ("name", "date_founded", "budget") VALUES ('Walt Disney Pictures', '1923-10-16', '201.55');
INSERT INTO "studio" ("name", "date_founded", "budget") VALUES ('20th Century Studios', '1935-05-31', '52.40');
INSERT INTO "studio" ("name", "date_founded", "budget") VALUES ('Columbia Pictures', '1924-01-10', '3.40');
INSERT INTO "studio" ("name", "date_founded", "budget") VALUES ('Universal Pictures', '1912-04-30', '30.00');
INSERT INTO "studio" ("name", "date_founded", "budget") VALUES ('Metro-Goldwyn-Mayer Pictures', '1924-04-17', '4.20');
INSERT INTO "studio" ("name", "date_founded", "budget") VALUES ('New Line Cinema', '1967-01-01', '0.50');

INSERT INTO "movie" ("id", "title", "url", "genre", "date_released", "rating", "budget", "gross_income", "summary", "studio", "director_id") VALUES ('1', 'The Shawshank Redemption', 'https://www.imdb.com/video/vi3877612057?playlistId=tt0111161&ref_=tt_pr_ov_vi', 'Drama', '1994-10-14', 'R', '25000000.00', '28241469.00', 'Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.', 'Warner Bros.', '1');
INSERT INTO "movie" ("id", "title", "url", "genre", "date_released", "rating", "budget", "gross_income", "summary", "studio", "director_id") VALUES ('2', 'The Godfather', 'https://www.imdb.com/video/imdb/vi1348706585?playlistId=tt0068646&ref_=tt_ov_vi', 'Crime', '1972-03-24', 'R', '6000000.00', '134966411.00', 'An organized crime dynastys aging patriarch transfers control of his clandestine empire to his reluctant son.', 'Paramount Pictures', '2');
INSERT INTO "movie" ("id", "title", "url", "genre", "date_released", "rating", "budget", "gross_income", "summary", "studio", "director_id") VALUES ('3', 'The Dark Knight', 'https://www.imdb.com/video/imdb/vi324468761?playlistId=tt0468569&ref_=tt_ov_vi', 'Action', '2008-07-18', 'PG-13', '185000000.00', '533720947.00', 'When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.', 'Warner Bros.', '3');
INSERT INTO "movie" ("id", "title", "url", "genre", "date_released", "rating", "budget", "gross_income", "summary", "studio", "director_id") VALUES ('4', '12 Angry Men', 'https://www.imdb.com/video/imdb/vi3452609817?playlistId=tt0050083&ref_=tt_ov_vi', 'Crime', '1957-04-10', 'PG', '340000.00', '379.00', 'A jury holdout attempts to prevent a miscarriage of justice by forcing his colleagues to reconsider the evidence.', 'Metro-Goldwyn-Mayer Pictures', '4');
INSERT INTO "movie" ("id", "title", "url", "genre", "date_released", "rating", "budget", "gross_income", "summary", "studio", "director_id") VALUES ('5', 'Schindler''s List', 'https://www.imdb.com/video/imdb/vi1158527769?playlistId=tt0108052&ref_=tt_pr_ov_vi', 'Historical', '1994-02-04', 'R', '22000000.00', '96898818.00', 'In German-occupied Poland during World War II, industrialist Oskar Schindler gradually becomes concerned for his Jewish workforce after witnessing their persecution by the Nazis.', 'Universal Pictures', '5');
INSERT INTO "movie" ("id", "title", "url", "genre", "date_released", "rating", "budget", "gross_income", "summary", "studio", "director_id") VALUES ('6', 'The Lord of the Rings: The Return of the King', 'https://www.imdb.com/video/imdb/vi2073101337?playlistId=tt0167260&ref_=tt_pr_ov_vi', 'Fantasy', '2003-12-17', 'PG-13', '94000000.00', '1143000000.00', 'Gandalf and Aragorn lead the World of Men against Saurons army to draw his gaze from Frodo and Sam as they approach Mount Doom with the One Ring.', 'New Line Cinema', '6');
INSERT INTO "movie" ("id", "title", "url", "genre", "date_released", "rating", "budget", "gross_income", "summary", "studio", "director_id") VALUES ('7', 'The Dark Knight Rises', 'https://en.wikipedia.org/wiki/The_Dark_Knight_Rises', 'Action', '2012-07-16', 'PG-13', '300000000.00', '1081000000.00', 'Summary', 'Warner Bros.', '3');

INSERT INTO "actor" ("id", "first_name", "last_name", "gender", "age") VALUES ('1', 'Tim', 'Robbins', 'M', '62');
INSERT INTO "actor" ("id", "first_name", "last_name", "gender", "age") VALUES ('2', 'Morgan', 'Freeman', 'M', '83');
INSERT INTO "actor" ("id", "first_name", "last_name", "gender", "age") VALUES ('3', 'Bob', 'Gunton', 'M', '75');
INSERT INTO "actor" ("id", "first_name", "last_name", "gender", "age") VALUES ('4', 'Marlon', 'Brando', 'M', '80');
INSERT INTO "actor" ("id", "first_name", "last_name", "gender", "age") VALUES ('5', 'Al', 'Pacino', 'M', '81');
INSERT INTO "actor" ("id", "first_name", "last_name", "gender", "age") VALUES ('6', 'Christian', 'Bale', 'M', '47');
INSERT INTO "actor" ("id", "first_name", "last_name", "gender", "age") VALUES ('7', 'Heath', 'Ledger', 'M', '29');
INSERT INTO "actor" ("id", "first_name", "last_name", "gender", "age") VALUES ('8', 'Aaron', 'Eckhart', 'M', '53');
INSERT INTO "actor" ("id", "first_name", "last_name", "gender", "age") VALUES ('9', 'Michael', 'Caine', 'M', '88');
INSERT INTO "actor" ("id", "first_name", "last_name", "gender", "age") VALUES ('10', 'Gary', 'Oldman', 'M', '63');
INSERT INTO "actor" ("id", "first_name", "last_name", "gender", "age") VALUES ('11', 'Martin', 'Balsam', 'M', '76');
INSERT INTO "actor" ("id", "first_name", "last_name", "gender", "age") VALUES ('12', 'John', 'Fiedler', 'M', '80');
INSERT INTO "actor" ("id", "first_name", "last_name", "gender", "age") VALUES ('13', 'Liam', 'Neeson', 'M', '68');
INSERT INTO "actor" ("id", "first_name", "last_name", "gender", "age") VALUES ('14', 'Ben', 'Kingsley', 'M', '77');
INSERT INTO "actor" ("id", "first_name", "last_name", "gender", "age") VALUES ('15', 'Ralph', 'Fiennes', 'M', '58');
INSERT INTO "actor" ("id", "first_name", "last_name", "gender", "age") VALUES ('16', 'Caroline', 'Goodall', 'F', '61');
INSERT INTO "actor" ("id", "first_name", "last_name", "gender", "age") VALUES ('17', 'Jonathan', 'Sagall', 'M', '62');
INSERT INTO "actor" ("id", "first_name", "last_name", "gender", "age") VALUES ('18', 'Noel', 'Appleby', 'M', '70');
INSERT INTO "actor" ("id", "first_name", "last_name", "gender", "age") VALUES ('19', 'Ali', 'Astin', 'F', '24');
INSERT INTO "actor" ("id", "first_name", "last_name", "gender", "age") VALUES ('20', 'Sean', 'Astin', 'M', '50');
INSERT INTO "actor" ("id", "first_name", "last_name", "gender", "age") VALUES ('21', 'David', 'Aston', 'M', '68');
INSERT INTO "actor" ("id", "first_name", "last_name", "gender", "age") VALUES ('22', 'John', 'Bach', 'M', '74');
INSERT INTO "actor" ("id", "first_name", "last_name", "gender", "age") VALUES ('23', 'Sean', 'Bean', 'M', '62');
INSERT INTO "actor" ("id", "first_name", "last_name", "gender", "age") VALUES ('24', 'Cate', 'Blanchett', 'F', '51');
INSERT INTO "actor" ("id", "first_name", "last_name", "gender", "age") VALUES ('25', 'Orlando', 'Bloom', 'M', '47');
INSERT INTO "actor" ("id", "first_name", "last_name", "gender", "age") VALUES ('26', 'Tom', 'Hardy', 'M', '43');

INSERT INTO "plan" ("name", "month_length", "total_price") VALUES ('One Month', '1', '30.00');
INSERT INTO "plan" ("name", "month_length", "total_price") VALUES ('One Year', '12', '300.00');
INSERT INTO "plan" ("name", "month_length", "total_price") VALUES ('Half Year', '6', '160.00');


INSERT INTO "users" ("id", "first_name", "last_name", "email", "phone_number", "password") VALUES ('1', ' James', 'Smith', 'james@email.com', NULL, 'ahfdhsdfgdxcvbfh');
INSERT INTO "users" ("id", "first_name", "last_name", "email", "phone_number", "password") VALUES ('2', 'John', 'Taylor', 'johntaylor@email.com', '7573321111', 'asdfgadsgasdf');
INSERT INTO "users" ("id", "first_name", "last_name", "email", "phone_number", "password") VALUES ('3', 'David', 'Lee', 'dl@email.com', '7573331122', 'dgadfhgsdfh');
INSERT INTO "users" ("id", "first_name", "last_name", "email", "phone_number", "password") VALUES ('4', 'Mary', 'Brown', 'mbrown@email.com', '7473331234', 'dfasgerfheragygafd');
INSERT INTO "users" ("id", "first_name", "last_name", "email", "phone_number", "password") VALUES ('5', 'Lisa', 'Williams', 'lisa@email.com', NULL, '3r5234tr534tdxcvdf');
INSERT INTO "users" ("id", "first_name", "last_name", "email", "phone_number", "password") VALUES ('6', 'Edward', 'Thompson', 'edward@email.com', '5442322145', 'agsr34t4gdfhga');
INSERT INTO "users" ("id", "first_name", "last_name", "email", "phone_number", "password") VALUES ('7', 'Brian', 'White', 'bw@email.com', '3452355667', 'rfgsrh356w4tgefw32t5');
INSERT INTO "users" ("id", "first_name", "last_name", "email", "phone_number", "password") VALUES ('8', 'Donald', 'Martin', 'dmartin@email.com', NULL, 'dasgergyertyerfgsdhgr');
INSERT INTO "users" ("id", "first_name", "last_name", "email", "phone_number", "password") VALUES ('9', 'Susan', 'Miller', 'susan@email.com', '3554441111', 'datewt32453');
INSERT INTO "users" ("id", "first_name", "last_name", "email", "phone_number", "password") VALUES ('10', 'Laura', 'Smith', 'laura@email.com', NULL, 'fat3453fgsfdger');

INSERT INTO "review" ("user_id", "movie_id", "review_date", "rating", "content") VALUES ('1', '1', '2021-05-05', '61.0', 'This movie was ok.');
INSERT INTO "review" ("user_id", "movie_id", "review_date", "rating", "content") VALUES ('1', '2', '2021-05-06', '42.0', 'eh movie');
INSERT INTO "review" ("user_id", "movie_id", "review_date", "rating", "content") VALUES ('1', '3', '2021-05-07', '85.0', 'it made me cry at the end');
INSERT INTO "review" ("user_id", "movie_id", "review_date", "rating", "content") VALUES ('2', '2', '2021-05-06', '34.0', 'I have seen better');
INSERT INTO "review" ("user_id", "movie_id", "review_date", "rating", "content") VALUES ('2', '3', '2021-05-05', '50.0', 'Just your average mediocre movie');
INSERT INTO "review" ("user_id", "movie_id", "review_date", "rating", "content") VALUES ('5', '1', '2021-05-06', '86.0', 'Fantastic!!!');
INSERT INTO "review" ("user_id", "movie_id", "review_date", "rating", "content") VALUES ('6', '1', '2021-05-05', '91.0', 'Such a powerful movie');
INSERT INTO "review" ("user_id", "movie_id", "review_date", "rating", "content") VALUES ('6', '5', '2021-05-06', '14.0', 'made me way too sad');
INSERT INTO "review" ("user_id", "movie_id", "review_date", "rating", "content") VALUES ('7', '6', '2021-05-05', '95.0', 'absolutely extrordinary');
INSERT INTO "review" ("user_id", "movie_id", "review_date", "rating", "content") VALUES ('7', '5', '2021-05-06', '100.0', 'the storytelling was captivting!');
INSERT INTO "review" ("user_id", "movie_id", "review_date", "rating", "content") VALUES ('2', '7', '2021-06-05', '84.0', 'Extradoniary ending to the trilogy');
INSERT INTO "review" ("user_id", "movie_id", "review_date", "rating", "content") VALUES ('5', '7', '2021-06-06', '93.0', 'Loved Bane!');
INSERT INTO "review" ("user_id", "movie_id", "review_date", "rating", "content") VALUES ('6', '7', '2021-06-05', '96.0', 'Bane made the whole movie');



INSERT INTO "act" ("movie_id", "actor_id", "if_main", "role") VALUES ('1', '1', '1', 'Andy Dufresne');
INSERT INTO "act" ("movie_id", "actor_id", "if_main", "role") VALUES ('1', '2', '1', 'Ellis Boyd ''Red'' Redding');
INSERT INTO "act" ("movie_id", "actor_id", "if_main", "role") VALUES ('1', '3', '0', 'Warden Norton');
INSERT INTO "act" ("movie_id", "actor_id", "if_main", "role") VALUES ('2', '4', '1', 'Don Vito Corleone');
INSERT INTO "act" ("movie_id", "actor_id", "if_main", "role") VALUES ('2', '5', '1', 'Michael Corleone');
INSERT INTO "act" ("movie_id", "actor_id", "if_main", "role") VALUES ('3', '6', '1', 'Bruce Wayne');
INSERT INTO "act" ("movie_id", "actor_id", "if_main", "role") VALUES ('3', '7', '1', 'Joker');
INSERT INTO "act" ("movie_id", "actor_id", "if_main", "role") VALUES ('3', '8', '0', 'Harvey Dent');
INSERT INTO "act" ("movie_id", "actor_id", "if_main", "role") VALUES ('3', '9', '0', 'Alfred');
INSERT INTO "act" ("movie_id", "actor_id", "if_main", "role") VALUES ('3', '10', '0', 'Gordon');
INSERT INTO "act" ("movie_id", "actor_id", "if_main", "role") VALUES ('3', '2', '0', 'Lucius Fox');
INSERT INTO "act" ("movie_id", "actor_id", "if_main", "role") VALUES ('4', '11', '0', 'Juror 1');
INSERT INTO "act" ("movie_id", "actor_id", "if_main", "role") VALUES ('4', '12', '0', 'Juror 2');
INSERT INTO "act" ("movie_id", "actor_id", "if_main", "role") VALUES ('5', '13', '1', 'Oskar Schindler');
INSERT INTO "act" ("movie_id", "actor_id", "if_main", "role") VALUES ('5', '14', '0', 'Itzhak Stern');
INSERT INTO "act" ("movie_id", "actor_id", "if_main", "role") VALUES ('5', '15', '0', 'Amon Goeth');
INSERT INTO "act" ("movie_id", "actor_id", "if_main", "role") VALUES ('5', '16', '0', 'Emilie Schindler');
INSERT INTO "act" ("movie_id", "actor_id", "if_main", "role") VALUES ('5', '17', '0', 'Poldek Pfefferberg');
INSERT INTO "act" ("movie_id", "actor_id", "if_main", "role") VALUES ('6', '18', '0', 'Everard Proudfoot');
INSERT INTO "act" ("movie_id", "actor_id", "if_main", "role") VALUES ('6', '19', '0', 'Elanor Gamgee');
INSERT INTO "act" ("movie_id", "actor_id", "if_main", "role") VALUES ('6', '20', '1', 'Sam');
INSERT INTO "act" ("movie_id", "actor_id", "if_main", "role") VALUES ('6', '21', '0', 'Gondorian Soldier 3');
INSERT INTO "act" ("movie_id", "actor_id", "if_main", "role") VALUES ('6', '22', '0', 'Madril');
INSERT INTO "act" ("movie_id", "actor_id", "if_main", "role") VALUES ('6', '23', '0', 'Boromir');
INSERT INTO "act" ("movie_id", "actor_id", "if_main", "role") VALUES ('6', '24', '0', 'Galadriel');
INSERT INTO "act" ("movie_id", "actor_id", "if_main", "role") VALUES ('6', '25', '0', 'Legolas');
INSERT INTO "act" ("movie_id", "actor_id", "if_main", "role") VALUES ('7', '6', '1', 'Bruce Wayne');
INSERT INTO "act" ("movie_id", "actor_id", "if_main", "role") VALUES ('7', '8', '0', 'Harvey Dent');
INSERT INTO "act" ("movie_id", "actor_id", "if_main", "role") VALUES ('7', '9', '0', 'Alfred');
INSERT INTO "act" ("movie_id", "actor_id", "if_main", "role") VALUES ('7', '10', '0', 'Gordon');
INSERT INTO "act" ("movie_id", "actor_id", "if_main", "role") VALUES ('7', '2', '0', 'Lucius Fox');
INSERT INTO "act" ("movie_id", "actor_id", "if_main", "role") VALUES ('7', '26', '0', 'Bane');


INSERT INTO "subscription" ("user_id", "plan_name", "start_date", "purchased_date") VALUES ('1', 'One Month', '2021-05-05', '2021-05-05');
INSERT INTO "subscription" ("user_id", "plan_name", "start_date", "purchased_date") VALUES ('2', 'One Month', '2021-05-05', '2021-05-03');
INSERT INTO "subscription" ("user_id", "plan_name", "start_date", "purchased_date") VALUES ('3', 'One Month', '2021-03-02', '2021-01-25');
INSERT INTO "subscription" ("user_id", "plan_name", "start_date", "purchased_date") VALUES ('4', 'One Year', '2021-05-05', '2021-05-05');
INSERT INTO "subscription" ("user_id", "plan_name", "start_date", "purchased_date") VALUES ('5', 'Half Year', '2021-04-02', '2021-04-02');

INSERT INTO "history" ("user_id", "movie_id", "watch_date", "is_finished") VALUES ('1', '1', '2021-05-05', '1');
INSERT INTO "history" ("user_id", "movie_id", "watch_date", "is_finished") VALUES ('1', '2', '2021-05-06', '1');
INSERT INTO "history" ("user_id", "movie_id", "watch_date", "is_finished") VALUES ('1', '3', '2021-05-07', '0');
INSERT INTO "history" ("user_id", "movie_id", "watch_date", "is_finished") VALUES ('2', '2', '2021-05-06', '1');
INSERT INTO "history" ("user_id", "movie_id", "watch_date", "is_finished") VALUES ('2', '3', '2021-05-05', '0');
INSERT INTO "history" ("user_id", "movie_id", "watch_date", "is_finished") VALUES ('5', '1', '2021-05-06', '1');
INSERT INTO "history" ("user_id", "movie_id", "watch_date", "is_finished") VALUES ('6', '1', '2021-05-05', '1');
INSERT INTO "history" ("user_id", "movie_id", "watch_date", "is_finished") VALUES ('6', '5', '2021-05-06', '1');
INSERT INTO "history" ("user_id", "movie_id", "watch_date", "is_finished") VALUES ('7', '6', '2021-05-05', '1');
INSERT INTO "history" ("user_id", "movie_id", "watch_date", "is_finished") VALUES ('7', '5', '2021-05-06', '1');
INSERT INTO "history" ("user_id", "movie_id", "watch_date", "is_finished") VALUES ('1', '7', '2021-06-07', '0');
INSERT INTO "history" ("user_id", "movie_id", "watch_date", "is_finished") VALUES ('2', '7', '2021-06-06', '1');
INSERT INTO "history" ("user_id", "movie_id", "watch_date", "is_finished") VALUES ('3', '7', '2021-06-05', '0');
INSERT INTO "history" ("user_id", "movie_id", "watch_date", "is_finished") VALUES ('5', '7', '2021-06-06', '1');
INSERT INTO "history" ("user_id", "movie_id", "watch_date", "is_finished") VALUES ('6', '7', '2021-06-05', '1');
 