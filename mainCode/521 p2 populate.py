import datetime as dt

import psycopg2
from psycopg2 import ProgrammingError, IntegrityError
from psycopg2.extras import execute_batch

import numpy as np

# all relations
"""
 Schema |      Name       |   Type   
--------+-----------------+----------
 public | act             | table    
 public | actor           | table    
 public | actor_id_seq    | sequence 
 public | director        | table    
 public | director_id_seq | sequence 
 public | genre           | table    
 public | history         | table    
 public | movie           | table    
 public | movie_id_seq    | sequence 
 public | plan            | table    
 public | progress        | table    
 public | review          | table    
 public | studio          | table    
 public | subscription    | table    
 public | users           | table    
 public | users_id_seq    | sequence 
"""

# act
"""
                        Table "public.act"
  Column  |         Type          | Collation | Nullable | Default 
----------+-----------------------+-----------+----------+---------
 actor_id | integer               |           | not null | 
 movie_id | integer               |           | not null | 
 if_main  | boolean               |           |          | 
 role     | character varying(50) |           | not null | 
Indexes:
    "act_pkey" PRIMARY KEY, btree (actor_id, movie_id)
Foreign-key constraints:
    "act_actor_id_fkey" FOREIGN KEY (actor_id) REFERENCES actor(id)
    "act_movie_id_fkey" FOREIGN KEY (movie_id) REFERENCES movie(id)
"""
def populate_act():
	with conn.cursor() as cur:
		try:
			cur.execute("SELECT id FROM actor;")
			actors = np.array(tuple(cur), dtype=int)
			conn.commit()
		except Exception as e:
			print('populate act: retrieve actors: exception:', repr(e))
			conn.rollback()
			return
		try:
			cur.execute("SELECT id FROM movie;")
			movies = np.array(tuple(cur), dtype=int)
			conn.commit()
		except Exception as e:
			print('populate act: retrieve actors: exception:', repr(e))
			conn.rollback()
			return
	
	actor_ids_per_movie = [
		tuple(np.random.choice(
			actors,
			size = np.random.randint(3,11),
			replace=False
		))
		for m in movies
	]
	
	main = [(True,)+(False,)*len(a-1) for a in actor_ids_per_movie]
	role = [tuple(f'role {i}' for i,id in enumerate(a,1)) for a in actor_ids_per_movie]
	full_insert_list = [
		(a,m,b,r)
		for m,z in zip(movies,zip(actor_ids_per_movie, main, role))
			for a,b,r in it.chain.from_iterable(zip(_) for _ in z)
	]
	
	print('full_insert_list:')
	for _ in full_insert_list: print(_)
	return
	
	with conn.cursor() as cur:
		try:
			cur.execute_batch(
				"""
				INSERT INTO act (actor_id, movie_id, if_main, role)
				VALUES (%s, %s, %s, %s);
				""",
				full_insert_list
			)
			conn.commit()
		except Exception as e:
			print('populate act: fill act: exception:', repr(e))
			conn.rollback()
			return

# actor
"""
                                      Table "public.actor"
   Column   |          Type          | Collation | Nullable |              Default              
------------+------------------------+-----------+----------+-----------------------------------
 id         | integer                |           | not null | nextval('actor_id_seq'::regclass)
 first_name | character varying(30)  |           | not null | 
 last_name  | character varying(30)  |           | not null | 
 info       | character varying(256) |           |          | 
Indexes:
    "actor_pkey" PRIMARY KEY, btree (id)
Referenced by:
    TABLE "act" CONSTRAINT "act_actor_id_fkey" FOREIGN KEY (actor_id) REFERENCES actor(id)
"""
def populate_actor(conn):
	with conn.cursor() as cur:
		try:
			for i in range(100):
				cur.execute(
				"""
				INSERT INTO actor
					(first_name, last_name, info)
				VALUES (%s, %s, %s);
				""",
				(f'actor {i} first',f'actor {i} last', f'some info about actor {i}')
				)
			conn.commit()
		except Exception as e:
			print('populate actor: insert actors: exception occurred:',repr(e))
			conn.rollback()

# director
"""
                                      Table "public.director"
   Column   |          Type          | Collation | Nullable |               Default                
------------+------------------------+-----------+----------+--------------------------------------
 id         | integer                |           | not null | nextval('director_id_seq'::regclass)
 first_name | character varying(30)  |           | not null | 
 last_name  | character varying(30)  |           | not null | 
 info       | character varying(256) |           |          | 
Indexes:
    "director_pkey" PRIMARY KEY, btree (id)
Referenced by:
    TABLE "movie" CONSTRAINT "movie_director_fkey" FOREIGN KEY (director) REFERENCES director(id)
"""
def populate_director(conn):
	with conn.cursor() as cur:
		try:
			for i in range(100):
				cur.execute(
				"""
				INSERT INTO director
					(first_name, last_name, info)
				VALUES (%s, %s, %s);
				""",
				(f'director {i} first',f'director {i} last', f'some info about director {i}')
				)
			conn.commit()
		except Exception as e:
			print('populate director: insert directors: exception occurred:',repr(e))
			conn.rollback()

# genre
"""
                       Table "public.genre"
 Column |          Type          | Collation | Nullable | Default 
--------+------------------------+-----------+----------+---------
 name   | character varying(50)  |           | not null | 
 info   | character varying(200) |           |          | 
Indexes:
    "genre_pkey" PRIMARY KEY, btree (name)
Referenced by:
    TABLE "movie" CONSTRAINT "movie_genre_fkey" FOREIGN KEY (genre) REFERENCES genre(name)"""
def populate_genre(conn):
	with conn.cursor() as cur:
		try:
			for i in range(20):
				cur.execute(
				"""
				INSERT INTO genre (name, info)
				VALUES (%s, %s, %s);
				""",
				(f'genre {i}',f'director {i}', f'some info about genre {i}')
				)
			conn.commit()
		except Exception as e:
			print('populate genre: insert genres: exception occurred:',repr(e))
			conn.rollback()

# history
"""
                 Table "public.history"
   Column    |  Type   | Collation | Nullable | Default 
-------------+---------+-----------+----------+---------
 user_id     | integer |           | not null | 
 movie_id    | integer |           | not null | 
 watch_time  | date    |           |          | 
 is_finished | boolean |           |          | 
Indexes:
    "history_pkey" PRIMARY KEY, btree (user_id, movie_id)
Foreign-key constraints:
    "history_movie_id_fkey" FOREIGN KEY (movie_id) REFERENCES movie(id)
    "history_user_id_fkey" FOREIGN KEY (user_id) REFERENCES users(id)
"""
def populate_history(conn):
	with conn.cursor() as cur:
		try:
			cur.execute(
			"""
			SELECT movie_id, MIN(date_produced)
			FROM movie
			GROUP BY movie_id;"""
			)
			movies_dates = tuple(cur)
			conn.commit()
		except Exception as e:
			print('populate history: select min produce dates: exception:', repr(e))
			conn.rollback()
			return
	
	with conn.cursor() as cur:
		try:
			cur.execute("""SELECT id FROM users;""")
			users = tuple(cur)
			conn.commit()
		except Exception as e:
			print('populate history: select users: exception:', repr(e))
			conn.rollback()
			return
	
	today = dt.date.today()
	
	m = np.arange(len(movies_dates))
	n = 100
	
	history_insert_list = []
	
	for user in users:
		choice = np.random.choice(
			m
			size = np.random.randint(1,n)
			replace = True
		)
		# this is the complete history of movies for this user
		#
		# simplification: a user watches a given movie only once on any given day
		#
		# also to simplify things, we do not ensure that users are watching movies
		#     during all times when they have a subscription
		#         since the subscription table is randomly populated
		#         based on the history table;
		#     the two-way dependency is unnecessarily complex
		#         for this application
		choice = tuple({
			# notice: the tuple acts on a set comprehension
			# the set comprehension ensures any given movie can be watched
			#     at most once on a given day, as stated above
			(
				user,
				movies_dates[i][0], # movie id
				# user watched this movie some random time
				# between when it was first produced and today
				movies_dates[i][1] + np.random.randint((today - movies_dates[i][1]).days),
				
			)
			for i in choice
		})
		history_insert_list.append(choice)
	
	with conn.cursor() as cur:
		try:
			cur.execute_batch(
			"""
			INSERT INTO history
				(user_id, movie_id, watch_time)
			VALUES (%s, %s, %s);
			""",
			history_insert_list,
			page_size = 1000
			)
		except Exception as e:
			print('populate history: insert history: exception:',repr(e))

# movie
"""
                                        Table "public.movie"
     Column     |          Type          | Collation | Nullable |              Default              
----------------+------------------------+-----------+----------+-----------------------------------
 id             | integer                |           | not null | nextval('movie_id_seq'::regclass)
 title          | character varying(50)  |           | not null | 
 url            | character varying(100) |           |          | 
 genre          | character varying(50)  |           |          | 
 studio         | character varying(50)  |           |          | 
 director       | integer                |           |          | 
 date_produced  | date                   |           |          | 
 average_rating | numeric(3,1)           |           |          | 
 available      | boolean                |           |          | 
 summary        | character varying(256) |           |          | 
Indexes:
    "movie_pkey" PRIMARY KEY, btree (id)
Foreign-key constraints:
    "movie_director_fkey" FOREIGN KEY (director) REFERENCES director(id)
    "movie_genre_fkey" FOREIGN KEY (genre) REFERENCES genre(name)
    "movie_studio_fkey" FOREIGN KEY (studio) REFERENCES studio(name)
Referenced by:
    TABLE "act" CONSTRAINT "act_movie_id_fkey" FOREIGN KEY (movie_id) REFERENCES movie(id)
    TABLE "history" CONSTRAINT "history_movie_id_fkey" FOREIGN KEY (movie_id) REFERENCES movie(id)
    TABLE "progress" CONSTRAINT "progress_movie_id_fkey" FOREIGN KEY (movie_id) REFERENCES movie(id)
    TABLE "review" CONSTRAINT "review_movie_id_fkey" FOREIGN KEY (movie_id) REFERENCES movie(id)
"""
def populate_movie_without_ratings(conn):
	with conn.cursor() as cur:
		try:
			cur.execute("SELECT name,date_founded FROM studio;")
			studios,dates = zip(*cur)
			conn.commit()
		except Exception as e:
			print('populate movie: select studios & dates: exception:',repr(e))
			conn.rollback()
			return
	
	with conn.cursor() as cur:
		try:
			cur.execute("SELECT id FROM director;")
			directors = tuple(cur)
			conn.commit()
		except Exception as e:
			print('populate movie: select director ids: exception:',repr(e))
			conn.rollback()
			return

	with conn.cursor() as cur:
		try:
			cur.execute("SELECT name FROM genre;")
			genres = tuple(cur)
			conn.commit()
		except Exception as e:
			print('populate movie: select genres: exception:',repr(e))
			conn.rollback()
			return
	
	num_movies = 10000
	
	chars = np.array(list(
		'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_'
		), dtype='U1'
	)
	urls = np.array(list(map(''.join, np.random.choice(chars,[num_movies,20]))))
	
	insert = "(title, url, genre, studio, director, date_produced, available, summary)"
	
	i = np.random.choice(
		np.arange(len(studios)),
		size = num_movies,
		replace=True
	)
	studios = tuple(studios[_] for _ in i)
	dates = tuple(dates[_] for _ in i)
	del i
	
	intervals = [((dt.date().today()-d) - dt.timedelta(10)).days for d in dates]
	dates = tuple(d + i for d,i in zip(dates,np.random.randint(intervals)))
	
	available = np.random.randint(0,101,num_movies).astype(bool)
	
	movie_insert_list = [
		(
			f'title of movie {m}',
			url,
			genre,
			studio,
			director,
			date,
			a,
			f'summary about movie {m}'
		)
		for m,url,genre,studio,director,date,a in zip(
			movies, urls, genres, studios, directors, dates, available
		)
	]
	
	with conn.cursor() as cur:
		try:
			cur.execute_batch(
				f"""
				INSERT INTO movie
					{insert}
				VALUES
					(%s, %s, %s, %s, %s, %s, %s, %s);
				""",
				movie_insert_list
			)
			conn.commit()
		except Exception as e:
			print('populate movie: movie insertion: exception:',repr(e))
			conn.rollback()
			return

# plan
"""
                          Table "public.plan"
    Column    |         Type          | Collation | Nullable | Default 
--------------+-----------------------+-----------+----------+---------
 name         | character varying(50) |           | not null | 
 month_length | interval              |           |          | 
 total_price  | numeric(15,3)         |           |          | 
Indexes:
    "plan_pkey" PRIMARY KEY, btree (name)
Referenced by:
    TABLE "subscription" CONSTRAINT "subscription_plan_name_fkey" FOREIGN KEY (plan_name) REFERENCES plan(name)
"""
def populate_plan(conn):
	plans = ('basic','plus','premium')
	months = (3,6,12)
	prices = (100,185,350)
	with conn.cursor() as cur:
		try:
			for plan,length,price in zip(plans,months,prices):
				cur.execute(
				"""
				INSERT INTO plan
					(name, month_length, total_price)
				VALUES (%s, %s, %s);
				""",
				(plan, str(length), str(price))
				)
			conn.commit()
		except Exception as e:
			print('populate plan: insert plans: exception:',repr(e))
			conn.rollback()

# progress
"""
                  Table "public.progress"
     Column     |   Type   | Collation | Nullable | Default 
----------------+----------+-----------+----------+---------
 user_id        | integer  |           | not null | 
 movie_id       | integer  |           | not null | 
 last_timestamp | interval |           |          | 
Indexes:
    "progress_pkey" PRIMARY KEY, btree (user_id, movie_id)
Foreign-key constraints:
    "progress_movie_id_fkey" FOREIGN KEY (movie_id) REFERENCES movie(id)
    "progress_user_id_fkey" FOREIGN KEY (user_id) REFERENCES users(id)
"""
def populate_progress(conn):
	with conn.cursor() as conn:
		try:
			cur.execute(
			"""
			SELECT DISTINCT user_id, movie_id
			FROM history;
			"""
			)
			users,movies = zip(*cur)
			conn.commit()
		except Exception as e:
			print('populate progress: select users, movies: exception:',repr(e))
			conn.rollback()
			return
	
	progress_insert_list = list(zip(
		users,
		movies,
		(f'{i} seconds' for i in
			np.random.randint(30*60, 120*60+1, len(users))
		)
	))
	
	with conn.cursor() as conn:
		try:
			cur.execute_batch(
			"""
			INSERT INTO progress
				(user_id, movie_id, last_timestamp)
			VALUES (%s, %s, %s);
			"""
			)
			printc('g',f'`progress` relation successfully populated with {len(progress_insert_list)} entries')
			conn.commit()
		except Exception as e:
			print('populate progress: insert entries: exception:',repr(e))
			conn.rollback()

# review
"""
                       Table "public.review"
  Column  |          Type          | Collation | Nullable | Default 
----------+------------------------+-----------+----------+---------
 user_id  | integer                |           | not null | 
 movie_id | integer                |           | not null | 
 date     | date                   |           |          | 
 rating   | numeric(3,1)           |           | not null | 
 content  | character varying(256) |           |          | 
Indexes:
    "review_pkey" PRIMARY KEY, btree (user_id, movie_id)
Foreign-key constraints:
    "review_movie_id_fkey" FOREIGN KEY (movie_id) REFERENCES movie(id)
    "review_user_id_fkey" FOREIGN KEY (user_id) REFERENCES users(id)
"""
def populate_review_and_movie_ratings(conn):
	with conn.cursor() as cur:
		try:
			# user cannot review a movie before the first watch event
			cur.execute(
			"""
			SELECT user_id, movie_id, MIN(watch_time) FROM history
			GROUP BY user_id,movie_id;
			"""
			)
			# simplifying assumption: a user reviews a movie
			# the first time he watches it
			users_movies_dates = tuple(cur)
			conn.commit()
		except Exception as e:
			print('populate review & movie ratings: select user ids: exception:',repr(e))
			conn.rollback()
			return
	
	# randomly choose half of available combinations
	users, movies, dates = zip(*np.random.choice(
		users_movies_dates,
		size = len(users_movies_dates)//2,
		replace=False
	))
	
	# assume that probabilities of higher ratings are higher
	# there's probably some fellow in the field of sociology who named a law after that
	ratings_probabilites = np.array([1,4,16,64,256], dtype=float)
	ratings_probabilites /= ratings_probabilites.sum()
	
	# TO DO: what are permissible rating values?
	ratings = np.random.choice(
		np.arange(1,6),
		size = len(users),
		p = ratings_probabilites
	)
	
	review_insert_list = [
		(
			user,
			movie,
			date,
			rating,
			f'<content of review for user {user} on movie {movie}>'
		)
		for user, movie, date, rating in zip(users, movies, dates, ratings)
	]
	
	with conn.cursor() as cur:
		try:
			cur.execute_batch(
				"""
				INSERT INTO review
					(user_id, movie_id, date, rating, content)
				VALUES
					(%s, %s, %s, %s, %s);
				""",
				review_insert_list
			)
			printc('g','populate review: inserted reviews')
			
			cur.execute(
			"""
			UPDATE movie
			SET
				total_rating_count = (
					SELECT COUNT(*)
					FROM review
					WHERE movie.id = review.movie_id
				),
				total_rating = (
					SELECT SUM(rating)
					FROM review
					WHERE movie.id = review.movie_id
				)
			"""
			)
			printc('g','populate review: updated movie ratings')
			
			conn.commit()
			printc('g','populate review: finished')
			
		except Exception as e:
			print('populate movie: movie insertion: exception:',repr(e))
			conn.rollback()
			return

# studio
"""
                         Table "public.studio"
    Column    |         Type          | Collation | Nullable | Default 
--------------+-----------------------+-----------+----------+---------
 name         | character varying(50) |           | not null | 
 date_founded | date                  |           |          | 
Indexes:
    "studio_pkey" PRIMARY KEY, btree (name)
Referenced by:
    TABLE "movie" CONSTRAINT "movie_studio_fkey" FOREIGN KEY (studio) REFERENCES studio(name)
"""
def populate_studio(conn):
	with conn.cursor() as cur:
		try:
			for i in range(10):
				cur.execute(
				"""
				INSERT INTO studio (name, date_founded)
				VALUES (%s, %s);
				""",
				(f'studio {i}',dt.date.today())
				)
			conn.commit()
		except Exception as e:
			print('populate studio: insert studios: exception occurred:',repr(e))
			conn.rollback()

# subscription
"""
                       Table "public.subscription"
     Column     |         Type          | Collation | Nullable | Default 
----------------+-----------------------+-----------+----------+---------
 user_id        | integer               |           | not null | 
 plan_name      | character varying(50) |           | not null | 
 start_date     | date                  |           | not null | 
 purchased_date | date                  |           |          | 
Indexes:
    "subscription_pkey" PRIMARY KEY, btree (user_id, plan_name, start_date)
Foreign-key constraints:
    "subscription_plan_name_fkey" FOREIGN KEY (plan_name) REFERENCES plan(name)
    "subscription_user_id_fkey" FOREIGN KEY (user_id) REFERENCES users(id)
"""
def populate_subscription(conn):
	with conn.cursor() as cur:
		try:
			cur.execute(
			"""
			SELECT user_id, MIN(watch_time) FROM history
			GROUP BY user_id;
			""")
			users,min_dates = zip(*cur)
			conn.commit()
		except Exception as e:
			print('populate subscription: select users & min dates: exception:',repr(e))
			conn.rollback()
			return
	
	with conn.cursor() as cur:
		try:
			cur.execute("SELECT name,30*EXTRACT(month from month_length) FROM plan;")
			plans_lengths = tuple(cur)
			conn.commit()
		except Exception as e:
			print('populate subscription: select plans: exception:',repr(e))
			conn.rollback()
			return
	
	# generate random history of subscriptions
	# for each user, his history stars from the first date he watched a movie
	# purchase date for any subscription is set to some
	# random time between 1 and 10 days before its start date
	subscription_insert_list = []
	for u,d in zip(users,min_dates):
		start_date = d
		while True:
			plan,length = np.random.choice(plans_lengths)
			end_date = start_date + length
			purchased_date = start_date - np.random.randint(1,11)
			subscription_insert_list.append((u,plan,start_date,purchased_date))
			start_date = end_date+1
			if start_date > dt.date.today():
				break
	
	with conn.cursor() as cur:
		try:
			cur.execute_batch(
			"""
			INSERT INTO subscription
				(user_id, plan_name, start_date, purchased_date)
			VALUES (%s, %s, %s, %s);
			""",
			subscription_insert_list,
			page_size = 1000
			)
			printc('g',f'successfully inserted {len(subscription_insert_list)} subscriptions')
			conn.commit()
		except Exception as e:
			print('populate subscription: insert subscriptions: exception:',repr(e))
			conn.rollback()

# users
"""
                                       Table "public.users"
    Column    |          Type          | Collation | Nullable |              Default              
--------------+------------------------+-----------+----------+-----------------------------------
 id           | integer                |           | not null | nextval('users_id_seq'::regclass)
 first_name   | character varying(30)  |           |          | 
 last_name    | character varying(30)  |           |          | 
 email        | character varying(50)  |           | not null | 
 phone_number | character varying(20)  |           |          | 
 password     | character varying(256) |           |          | 
Indexes:
    "users_pkey" PRIMARY KEY, btree (id)
Referenced by:
    TABLE "history" CONSTRAINT "history_user_id_fkey" FOREIGN KEY (user_id) REFERENCES users(id)
    TABLE "review" CONSTRAINT "review_user_id_fkey" FOREIGN KEY (user_id) REFERENCES users(id)
    TABLE "subscription" CONSTRAINT "subscription_user_id_fkey" FOREIGN KEY (user_id) REFERENCES users(id)
"""
def populate_users(conn):
	count = 100000
	users = tuple(range(1,count+1))
	emails = tuple(
		f'u{i}@{d}.com'
		for i,d in enumerate(
			np.random.randint(1,11,size = len(users)),
			1
		)
	)
	phone_numers = np.random.randint(10**9,2*10**9-1,size=len(users)).astype('U10')
	chars = np.array(list(
		'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_!@#$%^&*'
		), dtype='U1'
	)
	# if only user passwords were this strong...
	passwords = np.array(list(map(''.join, np.random.choice(chars,[count,60]))))
	
	user_insert_list = [
		(f'user {u} first',f'user {u} last',email,phone,pwd)
		for u,email,phone,pwd in zip(users,emails,phone_numbers,passwords)
	]
	
	with conn.cursor() as cur:
		try:
			cur.execute_batch(
			"""
			INSERT INTO users
				(first_name, last_name, email, phone_number, password)
			VALUES (%s, %s, %s, %s, %s);
			""",
			user_insert_list,
			page_size = 1000
			)
			printc('g',f'successfully insert {count} users')
			conn.commit()
		except Exception as e:
			print('populate users: insert users: exception:',repr(e))
			conn.rollback()

"""
 Schema |      Name       |   Type   
--------+-----------------+----------
 public | act             | table    
 public | actor           | table    
 public | director        | table    
 public | genre           | table    
 public | history         | table    
 public | movie           | table    
 public | plan            | table    
 public | progress        | table    
 public | review          | table    
 public | studio          | table    
 public | subscription    | table    
 public | users           | table    
"""

"""
act				actor, movie
history			movie, users
movie			
progress		
review			
subscription	

populate_movie_without_ratings
"""

if __name__ == '__main__':
	populate_actor()
	populate_director()
	populate_genre()
	populate_plan()
	populate_studio()
	populate_users()
	
	