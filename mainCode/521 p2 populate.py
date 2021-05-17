import sys
import itertools as it
import datetime as dt
from collections import deque
import time

import psycopg2
from psycopg2 import ProgrammingError, IntegrityError
from psycopg2.extras import execute_batch

import numpy as np

import platform

from threading import Thread

def update_progress_target(conn, table, *, insert_list=None, count=None,
					_s=it.cycle(('/','--','\\','|','/','|','\\')), sleep=time.sleep):
	if insert_list is not None:
		if count is not None:
			raise ValueError('provide either `insert_list` or `count`, not both')
		count = len(insert_list)
	if count is None:
		raise ValueError('provide one of `insert_list` or `count`')
	
	time.sleep(2)
	
	with conn.cursor() as cur:
		try:
			while True:
				cur.execute(f"SELECT COUNT(*) FROM {table};")
				c = next(cur)[0]
				print('\x1b[2K\r',flush=True,end='')
				print(f'    {next(_s)} {c} entries in table `{table}`',flush=True,end='')
				if c==count:
					break
				sleep(.5)
			print()
		except Exception as e:
			pass

def update_progress(*a, **kw):
	try:
		Thread(target=update_progress_target, args=a, kwargs=k).start()
	except:
		pass

# more portable implementation might use a pypi packaged
# but this suffices for now
COLORS = { # for terminal output
    'r': 91,            # red (bright)
    'dr': 31,            # red (dark)
    'o':'38;5;202',        # orange
    'mac':'38;5;214',    # macaroni
    'y': 33,            # yellow (darker)
    'm': 35,            # magenta
    'g': 32,            # green (medium)
    'dg':'38;5;22',        # green (dark)
    'teal': 36,
    'b':34,             # blue
    'orchid':'38;5;165',
    'p':'38;5;56',        # purple
    'bold': 1,
    'reset': 0
}

def as_color(s, c):
    """Return string surrouded by ANSI codes for outputting colored text.
    The string to be colored is `s`. The color can be specified by name
    or by integer value. If a name is provided that is not defined,
    this function silently returns the original, unmodified string.
    
    See e.g. https://en.wikipedia.org/wiki/ANSI_escape_code
    """
    if (platform.system()=='Linux'):
        if isinstance(c,int):
            return f'\033[{c}m{s}\033[0m'
        try:
            return f'\033[{COLORS[c]}m{s}\033[0m'
        except KeyError:
            return s
    else:
        return s

def as_bold_color(s, c):
    """Similar to `as_color`, but return string encoded to be bold and colored.
    `s` and `c` have the same parameterization as in `as_color`.
    """
    if (platform.system()=='Linux'):
        if isinstance(c,int):
            return f'\033[1m\033[{c}m{s}\033[0m'
        try:
            return f'\033[1m\033[{COLORS[c]}m{s}\033[0m'
        except KeyError:
            return s
    else:
        return s

def printc(color, *args, **kw):
	"""Print text in a given color."""
	print(*(as_color(a,color) for a in args), **kw)

# all relations
"""
"""

# act
"""
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
"""
def populate_act(conn):
	with conn.cursor() as cur:
		try:
			cur.execute("SELECT id FROM actor;")
			actors = np.array([r[0] for r in cur], dtype=int)
			conn.commit()
		except Exception as e:
			print('populate act: retrieve actors: exception:', repr(e))
			conn.rollback()
			return
		try:
			cur.execute("SELECT id FROM movie;")
			movies = tuple(r[0] for r in cur)
			conn.commit()
		except Exception as e:
			print('populate act: retrieve actors: exception:', repr(e))
			conn.rollback()
			return
	
	actor_ids_per_movie = [
		np.random.choice(
			actors,
			size = np.random.randint(5,20),
			replace=False
		).tolist()
		for m in movies
	]
	
	# simplifying assumption: each movie has one main actor
	main = [('T',)+('F',)*(len(a)-1) for a in actor_ids_per_movie]
	role = [tuple(f'role {i}' for i,id in enumerate(a,1)) for a in actor_ids_per_movie]
	act_insert_list = [
		(m,*i)
		for m,a,b,r in zip(movies,actor_ids_per_movie, main, role)
		for i in zip(a,b,r)
	]
	
	print(f'act_insert_list: {len(act_insert_list)} entries to be inserted')
# 	for _ in act_insert_list: print(_)
# 	return
	
	with conn.cursor() as cur:
		try:
			execute_batch(cur,
				"""
				INSERT INTO act (movie_id, actor_id, if_main, role)
				VALUES (%s, %s, %s, %s);
				""",
				act_insert_list
			)
			conn.commit()
			printc('g',f'success: inserted {len(act_insert_list)} into `act`')
		except Exception as e:
			print('populate act: fill act: exception:', repr(e))
			conn.rollback()
			return

# actor
"""
create table actor
(
    id            varchar(10),
    first_name    varchar(30),
    last_name     varchar(30) not null,
    gender        varchar(1),
    age           varchar(3) check (age > 0),

    primary key (id)
);
"""
def populate_actor(conn, *, count = 500):
	actors = range(count)
	
	# keep things simple here
	first_names = (f'actor {i} first' for i in actors)
	last_names = (f'actor {i} last' for i in actors)
# 	infos = (f'some info about actor {i}' for i in actors) # wound up not including this
	genders = np.random.choice(['m','f'], size=count, replace=True).tolist()
	ages = np.random.randint(20, 81, count).tolist()
	
	actor_insert_list = list(zip(first_names, last_names, genders, ages))
	
	del ages,genders
	with conn.cursor() as cur:
		try:
			execute_batch(cur,
			"""
			INSERT INTO actor
				(first_name, last_name, gender, age)
			VALUES (%s, %s, %s, %s);
			""",
			actor_insert_list
			)
			conn.commit()
		except Exception as e:
			print('populate actor: insert actors: exception occurred:',repr(e))
			conn.rollback()

# director
"""
create table director
(
    id            varchar(5),
    first_name    varchar(20),
    last_name     varchar(20) not null,
    age           varchar(3) check (age > 0),
    primary key (id)
);
"""
def populate_director(conn, *, count = 500):
	directors = range(count)
	
	# keep things simple here
	first_names = (f'director {i} first' for i in directors)
	last_names = (f'director {i} last' for i in directors)
	ages = np.random.randint(30, 81, count).tolist()
	director_insert_list = list(zip(first_names, last_names, ages))
	
	del ages
	
	with conn.cursor() as cur:
		try:
			execute_batch(cur,
			"""
			INSERT INTO director
				(first_name, last_name, age)
			VALUES (%s, %s, %s);
			""",
			director_insert_list
			)
			conn.commit()
		except Exception as e:
			print('populate director: insert directors: exception occurred:',repr(e))
			conn.rollback()

# genre (removed from schema)
# """
#                        Table "public.genre"
#  Column |          Type          | Collation | Nullable | Default 
# --------+------------------------+-----------+----------+---------
#  name   | character varying(50)  |           | not null | 
#  info   | character varying(200) |           |          | 
# Indexes:
#     "genre_pkey" PRIMARY KEY, btree (name)
# Referenced by:
#     TABLE "movie" CONSTRAINT "movie_genre_fkey" FOREIGN KEY (genre) REFERENCES genre(name)"""
# def populate_genre(conn):
# 	with conn.cursor() as cur:
# 		try:
# 			for i in range(20):
# 				cur.execute(
# 				"""
# 				INSERT INTO genre (name, info)
# 				VALUES (%s, %s, %s);
# 				""",
# 				(f'genre {i}',f'director {i}', f'some info about genre {i}')
# 				)
# 			conn.commit()
# 		except Exception as e:
# 			print('populate genre: insert genres: exception occurred:',repr(e))
# 			conn.rollback()

# history
"""
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
"""

def _populate_history_user_choice(user, movies_dates, m, n, history_insert_list, today,
								  *, tf=np.array(['T','F'])):
	
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
	choice = {
		# the set comprehension ensures any given movie can be watched
		#     at most once on a given day, as stated above
		(
			user,
			movies_dates[i][0], # movie id
			# user watched this movie some random time
			# between when it was first produced and today
			
			# use if-else here because np.random.randint raises an error
			# with argument 0, which happens if the movie was produced today
			today if movies_dates[i][1]==today
				else
				movies_dates[i][1] + dt.timedelta(
					np.random.randint((today - movies_dates[i][1]).days)
				)
			
		)
		for i in np.random.choice(m,
								  size = np.random.randint(1,n),
								  replace = True)
	}
# 	is_finished = np.random.randint(2, size = len(choice), dtype=bool).tolist()
	is_finished = np.random.choice(tf, size = len(choice), replace=True).tolist()
	history_insert_list.extend((*c, f) for c,f in zip(choice, is_finished))

def populate_history(conn):
	with conn.cursor() as cur:
		try:
			cur.execute(
			"""
			SELECT id, date_released
			FROM movie;"""
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
			users = tuple(r[0] for r in cur)
			conn.commit()
		except Exception as e:
			print('populate history: select users: exception:', repr(e))
			conn.rollback()
			return
	
	today = dt.date.today()
	
	m = np.arange(len(movies_dates))
	n = 100
	
	history_insert_list = []
	
# 	print('populate history:')
# 	print('movies_dates:')
# 	print(movies_dates)
# 	print('users:')
# 	print(users)
	
	deque( # consumes the whole iterable, but much faster than Python for-loop
		(_populate_history_user_choice(user, movies_dates, m, n,
		 	history_insert_list, today) for user in users
		),
		maxlen=0
	)
	
	print(f'history_insert_list: {len(history_insert_list)} entries to insert:')
	
# 	print('history_insert_list: first 3 entries to insert:',history_insert_list[:3])
	with conn.cursor() as cur:
		try:
			execute_batch(cur,
			"""
			INSERT INTO history
				(user_id, movie_id, watch_date, is_finished)
			VALUES (%s, %s, %s, %s);
			""",
			history_insert_list,
			page_size = 1000
			)
			printc('successfully inserted {len(history_insert_list)} history events')
		except Exception as e:
			print('populate history: insert history: exception:',repr(e))

# movie
"""
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
"""

####  THIS HAS TO BE UPDATED

def populate_movie(conn):
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
			directors = tuple(r[0] for r in cur)
			conn.commit()
		except Exception as e:
			print('populate movie: select director ids: exception:',repr(e))
			conn.rollback()
			return
# 
# 	with conn.cursor() as cur:
# 		try:
# 			cur.execute("SELECT name FROM genre;")
# 			genres = tuple(cur)
# 			conn.commit()
# 		except Exception as e:
# 			print('populate movie: select genres: exception:',repr(e))
# 			conn.rollback()
# 			return
	
	num_movies = 10000
	
	# choose randomly from 10 genres
	genres = tuple(f'genre {i}' for i in np.random.randint(1,11,num_movies))
	
	chars = np.array(list(
		'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_'
		), dtype='U1'
	)
	urls = np.array(list(map(''.join, np.random.choice(chars,[num_movies,20]))))
	incomes = np.random.randint(10**8,10**9,num_movies)
	# optimistic
	budgets = incomes - np.random.randint(10**7,5*10**7,num_movies)
	
	insert = "(title, url, genre, date_released, budget, rating, gross_income, summary, studio, director_id)"
	
	i = np.random.choice(
		np.arange(len(studios)),
		size = num_movies,
		replace=True
	)
	studios = tuple(studios[_] for _ in i)
	dates = tuple(dates[_] for _ in i)
	del i
	
	intervals = np.array([((dt.date.today()-d) - dt.timedelta(10)).days for d in dates])
	intervals[intervals==0]=1
	
	dates = tuple(d + dt.timedelta(i) for d,i in zip(dates,np.random.randint(intervals).tolist()))
	del intervals
	
	directors = np.random.choice(
		directors,
		size = num_movies,
		replace = True
	).tolist()
	
	ratings = np.random.choice(['G','PG','PG-13','R'], size=num_movies, replace=True).tolist()
	
	movie_insert_list = [
		(
			f'title of movie {m}',
			url,
			genre,
			date,
			budget,
			rating,
			income,
			f'summary about movie {m}',
			studio,
			director
		)
		for m,url,genre,date,budget,rating,income,studio,director in zip(
			range(num_movies), urls.tolist(), genres, dates, budgets.tolist(),
			ratings, incomes.tolist(), studios, directors
		)
	]
	
	with conn.cursor() as cur:
		try:
			execute_batch(cur,
				f"""
				INSERT INTO movie
					{insert}
				VALUES
					(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
				""",
				movie_insert_list
			)
			conn.commit()
		except Exception as e:
			print('populate_movie: movie insertion: exception:',repr(e))
			conn.rollback()
			return

# plan
"""
create table plan
(
    name            varchar(50),
    month_length    numeric(2,0),
    total_price     numeric(15,2),

    primary key (name)
);
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

# progress (removed from schema)
# """
#                   Table "public.progress"
#      Column     |   Type   | Collation | Nullable | Default 
# ----------------+----------+-----------+----------+---------
#  user_id        | integer  |           | not null | 
#  movie_id       | integer  |           | not null | 
#  last_timestamp | interval |           |          | 
# Indexes:
#     "progress_pkey" PRIMARY KEY, btree (user_id, movie_id)
# Foreign-key constraints:
#     "progress_movie_id_fkey" FOREIGN KEY (movie_id) REFERENCES movie(id)
#     "progress_user_id_fkey" FOREIGN KEY (user_id) REFERENCES users(id)
# """
# def populate_progress(conn):
# 	with conn.cursor() as cur:
# 		try:
# 			cur.execute(
# 			"""
# 			SELECT DISTINCT user_id, movie_id
# 			FROM history;
# 			"""
# 			)
# 			users,movies = zip(*cur)
# 			conn.commit()
# 		except Exception as e:
# 			print('populate progress: select users, movies: exception:',repr(e))
# 			conn.rollback()
# 			return
# 	
# 	progress_insert_list = list(zip(
# 		users,
# 		movies,
# 		(f'{i} seconds' for i in
# 			np.random.randint(30*60, 120*60+1, len(users))
# 		)
# 	))
# 	
# 	with conn.cursor() as cur:
# 		try:
# 			execute_batch(cur,
# 			"""
# 			INSERT INTO progress
# 				(user_id, movie_id, last_timestamp)
# 			VALUES (%s, %s, %s);
# 			"""
# 			)
# 			printc('g',f'`progress` relation successfully populated with {len(progress_insert_list)} entries')
# 			conn.commit()
# 		except Exception as e:
# 			print('populate progress: insert entries: exception:',repr(e))
# 			conn.rollback()

# produce
# """
# """
# def populate_produce():
# 	with conn.cursor() as cur:
# 		try:
# 			cur.execute(
# 			"""
# 			SELECT name FROM studio;
# 			"""
# 			)
# 			studios = tuple(cur)
# 			conn.commit()
# 		except Exception as e:
# 			print('populate_produce: select studio names: exception:',repr(e))
# 			conn.rollback()
# 			return
# 	
# 	with conn.cursor() as cur:
# 		try:
# 			cur.execute(
# 			"""
# 			SELECT id FROM movie;
# 			"""
# 			)
# 			studios = tuple(cur)
# 			conn.commit()
# 		except Exception as e:
# 			print('populate_produce: select movies: exception:',repr(e))
# 			conn.rollback()
# 			return
# 	
# 	studios = np.random.choice(
# 		studios,
# 		size=len(movies),
# 		replace=True
# 	)
# 	
# 	produce_insert_list = list(zip(movies,studios))
# 	n = len(produce_insert_list)
# 	
# 	with conn.cursor() as cur:
# 		try:
# 			execute_batch(cur,
# 			"""
# 			INSERT INTO produce
# 				(studio_name, movie_id)
# 			VALUES (%s, %s);
# 			""",
# 			produce_insert_list
# 			)
# 			printc('g', f'successfully inserted {n} entries into `produce` relation')
# 			conn.commit()
# 		except Exception as e:
# 			print('populate_produce: insert entries: exception:',repr(e))
# 			conn.rollback()

# review
"""
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
"""
def populate_review(conn):
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
	).tolist())
	
	# assume that probabilities of higher ratings are higher
	# there's probably some fellow in the field of sociology who named a law after that
	ratings_probabilites = np.array([1,4,16,64,256], dtype=float)
	ratings_probabilites /= ratings_probabilites.sum()
	
	# TO DO: what are permissible rating values?
	ratings = np.random.choice(
		np.arange(1,6),
		size = len(users),
		p = ratings_probabilites
	).tolist()
	
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
			execute_batch(cur,
				"""
				INSERT INTO review
					(user_id, movie_id, review_date, rating, content)
				VALUES
					(%s, %s, %s, %s, %s);
				""",
				review_insert_list
			)
			printc('g','populate review: inserted reviews')
			
			# for prior version of schema
			
# 			cur.execute(
# 			"""
# 			UPDATE movie
# 			SET
# 				total_rating_count = (
# 					SELECT COUNT(*)
# 					FROM review
# 					WHERE movie.id = review.movie_id
# 				),
# 				total_rating = (
# 					SELECT SUM(rating)
# 					FROM review
# 					WHERE movie.id = review.movie_id
# 				)
# 			"""
# 			)
# 			printc('g','populate review: updated movie ratings')
			
			conn.commit()
			printc('g','populate review: finished')
			
		except Exception as e:
			print('populate movie: movie insertion: exception:',repr(e))
			conn.rollback()
			return

# studio
"""
create table studio
(
    name          varchar(20),
    date_founded  date,
    budget        numeric(12,2) check (budget > 0),

    primary key (name)
);
"""
def populate_studio(conn):
	with conn.cursor() as cur:
		try:
			for i in range(10):
				cur.execute(
				"""
				INSERT INTO studio (name, date_founded, budget)
				VALUES (%s, %s, %s);
				""",
				(f'studio {i}',dt.date.today()-dt.timedelta(3663),
				 int(np.random.randint(3*10**9,10**10+1)))
				)
			conn.commit()
			printc('g','studio table populated')
		except Exception as e:
			print('populate studio: insert studios: exception occurred:',repr(e))
			conn.rollback()

# subscription
"""
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
	# for each user, his history starts from the first date he watched a movie
	# purchase date for any subscription is set to some
	# random time between 1 and 10 days before its start date
	subscription_insert_list = []
	for u,d in zip(users,min_dates):
		start_date = d
		while True:
			plan,length = np.random.choice(plans_lengths)
			end_date = start_date + length
			purchased_date = start_date - int(np.random.randint(1,11))
			subscription_insert_list.append((u,plan,start_date,purchased_date))
			start_date = end_date+1
			if start_date > dt.date.today():
				break
	
	with conn.cursor() as cur:
		try:
			execute_batch(cur,
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
	phone_numbers = np.random.randint(10**9,2*10**9-1,size=len(users)).astype('U10').tolist()
	chars = np.array(list(
		'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_!@#$%^&*'
		), dtype='U1'
	).tolist()
	# if only user passwords were this strong...
	passwords = np.array(list(map(''.join, np.random.choice(chars,[count,30])))).tolist()
	
	user_insert_list = [
		(f'user {u} first',f'user {u} last',email,phone,pwd)
		for u,email,phone,pwd in zip(users,emails,phone_numbers,passwords)
	]
	
	with conn.cursor() as cur:
		try:
			update_progress(conn, 'users', insert_list = user_insert_list)
			execute_batch(cur,
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

# all tables
"""
"""

"""
TABLE			DEPENDENCIES (other tables that must exist first)
actor			<none>
director		<none>
-genre				<none>
plan			<none>
studio			<none>
users			<none>

movie			studio, director, genre
-produce			studio, movie
act				actor, movie
history			movie, users
-progress			history
review			history
subscription	history
"""

if __name__ == '__main__':
	user = input("Enter database user: ")
	
	conn = psycopg2.connect(host="localhost", port=5432, \
		dbname="skynetflix_large", user=user)
	
	statements = (
		"SELECT setval('users_id_seq',(SELECT COALESCE(MAX(id),0)+1 FROM users),false);",
		"SELECT setval('movie_id_seq',(SELECT COALESCE(MAX(id),0)+1 FROM movie),false);",
		"SELECT setval('actor_id_seq',(SELECT COALESCE(MAX(id),0)+1 FROM actor),false);",
		"SELECT setval('director_id_seq',(SELECT COALESCE(MAX(id)+1,0) FROM director),false);"
	)
	with conn.cursor() as cur:
		try:
			for s in statements:
				cur.execute(s)
		except Exception as e:
			print('setval statements: exception:',repr(e))
			conn.rollback()
			print('setval statements failed to execute, exiting program')
			conn.close()
			sys.exit()
	
	populate_actor(conn)
	populate_director(conn)
# 	populate_genre(conn) # (removed)
	populate_plan(conn)
	populate_studio(conn)
	populate_users(conn)
	
	populate_movie(conn)
# 	populate_produce() # (not used)
	populate_act(conn)					## CHECK WHEN 'if_main' type changed
	populate_history(conn)				## CHECK WHEN 'is_finished' type changed
# 	populate_progress(conn) # (removed)
	populate_review(conn)
	populate_subscription(conn)
	
	print('all tables filled; exiting')
	conn.close()