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
from math import ceil

from threading import Thread

def update_progress_target(conn, table, initial_count, *, insert_list=None, count=None,
					_s=it.cycle(('/','--','\\','|','/','|','\\')), sleep=time.sleep):
# 	print('update_progress_target called:',conn,table)
	if insert_list is not None:
		if count is not None:
			raise ValueError('provide either `insert_list` or `count`, not both')
		count = len(insert_list)
	if count is None:
		raise ValueError('provide one of `insert_list` or `count`')
	
	time.sleep(2)
	
	target = initial_count + count
	
	print()
	s=''
	with conn.cursor() as cur:
		try:
			while True:
				cur.execute(f"SELECT COUNT(*) FROM {table};")
				c = next(cur)[0]
				t = f'    {next(_s)} {c} entries in table `{table}`'
				if c==target:
					break
				else:
					print((f'\033[A\r{t}').ljust(len(s)))
					s = t
					sleep(.3)
			print()
		except Exception as e:
			pass

def update_progress(*a, **kw):
	try:
		Thread(target=update_progress_target, args=a, kwargs=kw).start()
	except Exception as e:
		printc('r',f'update progress error: {repr(e)}')

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

# act
def populate_act(conn):
	print('populate: `act`...', end=' ', flush=True)
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
def populate_actor(conn, *, count = 500):
	print('populate: `actor`...', end=' ', flush=True)
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
			printc('g', f'successfully inserted {count} actors')
		except Exception as e:
			print('populate actor: insert actors: exception occurred:',repr(e))
			conn.rollback()

# director
def populate_director(conn, *, count = 500):
	print('populate: `director`...', end=' ', flush=True)
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
			printc('g', f'successfully inserted {count} directors')
		except Exception as e:
			print('populate director: insert directors: exception occurred:',repr(e))
			conn.rollback()

# history
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
	print('\x1b[2K\r',flush=True,end='')
	print(f'generating user choice for user {user}',flush=True,end='')
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
	return ((*c, f) for c,f in zip(choice, is_finished))

def populate_history(conn):
	print('populate: `history`...', end=' ', flush=True)
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
	
	history_insert_list = list(it.chain.from_iterable(
		(_populate_history_user_choice(user, movies_dates, m, n,
		 	history_insert_list, today) for user in users)
		))
	
	print('\x1b[2K\r',flush=True,end='')
	print('\n')
	
	print(f'history_insert_list: {len(history_insert_list)} entries to insert')
	
	with conn.cursor() as cur:
		try:
			cur.execute("SELECT COUNT(*) FROM history;")
			update_progress(conn, 'history', next(cur)[0], insert_list=history_insert_list)
			
			execute_batch(cur,
			"""
			INSERT INTO history
				(user_id, movie_id, watch_date, is_finished)
			VALUES (%s, %s, %s, %s);
			""",
			history_insert_list,
			page_size = 100000
			)
			conn.commit()
			printc('g',f'successfully inserted {len(history_insert_list)} history events')
		except Exception as e:
			print('populate history: insert history: exception:',repr(e))
			conn.rollback()

# movie
def populate_movie(conn):
	print('populate: `movie`...', end=' ', flush=True)
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
			printc('g',f'successfully inserted {num_movies} movies')
		except Exception as e:
			print('populate_movie: movie insertion: exception:',repr(e))
			conn.rollback()
			return

# plan
def populate_plan(conn):
	print('populate: `plan`...', end=' ', flush=True)
	plans = ('basic','plus','premium')
	months = (f'{m} months' for m in (3,6,12))
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
			printc('g',f'successfully inserted 3 plans')
		except Exception as e:
			print('populate plan: insert plans: exception:',repr(e))
			conn.rollback()

# review
def populate_review(conn):
	print('populate: `review`...', end=' ', flush=True)
	with conn.cursor() as cur:
		try:
			# user cannot review a movie before the first watch event
			cur.execute(
			"""
			SELECT user_id, movie_id, MIN(watch_date) FROM history
			GROUP BY user_id,movie_id;
			"""
			)
			# simplifying assumption: a user reviews a movie
			# the first time he watches it
			users_movies_dates = tuple(cur)
# 			print(users_movies_dates[:4])
			conn.commit()
		except Exception as e:
			print('populate review & movie ratings: select user ids: exception:',repr(e))
			conn.rollback()
			return
	
	# randomly choose half of available combinations
	c = np.random.choice(
		np.arange(len(users_movies_dates)),
		size = len(users_movies_dates)//2,
		replace=False
	)
	users, movies, dates = zip(*(users_movies_dates[i] for i in c))
	
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
	print(f'inserting {len(review_insert_list)} entries', flush=True)
	with conn.cursor() as cur:
		try:
			cur.execute("SELECT COUNT(*) FROM review;")
			update_progress(conn, 'review', next(cur)[0], insert_list=review_insert_list)
			execute_batch(cur,
				"""
				INSERT INTO review
					(user_id, movie_id, review_date, rating, content)
				VALUES
					(%s, %s, %s, %s, %s);
				""",
				review_insert_list,
				page_size = 100000
			)
			printc('g',f'successfully inserted {len(review_insert_list)} reviews')
			
			conn.commit()
			
		except Exception as e:
			print('populate review: insertion: exception:',repr(e))
			conn.rollback()
			return

# studio
def populate_studio(conn):
	print('populate: `studio`...', end=' ', flush=True)
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
			printc('g','successfully inserted 10 studios')
		except Exception as e:
			print('populate studio: insert studios: exception occurred:',repr(e))
			conn.rollback()

# subscription
def _gen_user_subscription_hist(i,u,d,t, today, day, plans_lengths, nplans):
	print(f'\x1b[2K\rbuilding subscriptions for user {i}/{t}', end='',flush=True)
	start_date = d
	dif = (dt.date.today() - start_date).days
	plan,length = plans_lengths[np.random.randint(nplans)]
# 	print('dif,length:',dif,length)
	count = ceil(dif / length)
	gen = (
		(u, plan, d+(length*i)*day, d+(length*i)*day - dt.timedelta(int(np.random.randint(1,11))))
		for i in range(count)
	)
	return gen

def populate_subscription(conn):
	print('populate: `subscription`...')
	with conn.cursor() as cur:
		try:
			cur.execute("""
			SELECT user_id, MIN(watch_date) FROM history
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
			cur.execute("""
			SELECT
				name,
				365 * EXTRACT(year from month_length)
					+ 30*EXTRACT(month from month_length)
			FROM plan;""")
			plans_lengths = tuple(cur)
			nplans = len(plans_lengths)
			conn.commit()
		except Exception as e:
			print('populate subscription: select plans: exception:',repr(e))
			conn.rollback()
			return
	
	# generate random history of subscriptions
	# for each user, his history starts from the first date he watched a movie
	# purchase date for any subscription is set to some
	# random time between 1 and 10 days before its start date
	# very simplistic: for ease of calculating within given time frame,
	# assume each user selects a particular plan over and over again
	today = dt.date.today()
	day = dt.timedelta(1)
	t = len(users)
	
	subscription_insert_list = list(it.chain.from_iterable(
		_gen_user_subscription_hist(i,u,d,t, today, day, plans_lengths, nplans)
		for i,(u,d) in enumerate(zip(users,min_dates))
	))
	
# 	print('subscription_insert_list:',subscription_insert_list[:4])
	
	print('\x1b[2K\r',end='',flush=True)
	print('\n')
	
	print(f'inserting {len(subscription_insert_list)} entries')
	with conn.cursor() as cur:
		try:
			cur.execute("SELECT COUNT(*) FROM subscription;")
			update_progress(conn, 'subscription', next(cur)[0], insert_list=subscription_insert_list)
			execute_batch(cur,
			"""
			INSERT INTO subscription
				(user_id, plan_name, start_date, purchased_date)
			VALUES (%s, %s, %s, %s);
			""",
			subscription_insert_list,
			page_size = 100000
			)
			printc('g',f'successfully inserted {len(subscription_insert_list)} subscriptions')
			conn.commit()
		except Exception as e:
			print('populate subscription: insert subscriptions: exception:',repr(e))
			conn.rollback()

# users
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
			cur.execute("SELECT COUNT(*) FROM users;")
			update_progress(conn, 'users', next(cur)[0], insert_list = user_insert_list)
			execute_batch(cur,
			"""
			INSERT INTO users
				(first_name, last_name, email, phone_number, password)
			VALUES (%s, %s, %s, %s, %s);
			""",
			user_insert_list,
			page_size = 10000
			)
			printc('g',f'successfully inserted {count} users')
			conn.commit()
		except Exception as e:
			print('populate users: insert users: exception:',repr(e))
			conn.rollback()

# all tables

"""
TABLE			DEPENDENCIES (other tables that must exist first)

actor			<none>
director		<none>
plan			<none>
studio			<none>
users			<none>

movie			studio, director
act				actor, movie
history			movie, users
review			history
subscription	history
"""

# for some reason this did not work when ran
# def empty_tables(conn):
# 	tables = ('actor','director','plan','studio','users','movie','act','history','subscription')
# 	for table in tables:
# 		with conn.cursor() as cur:
# 			try:
# 				cur.execute(f"DELETE FROM {table};")
# 				conn.commit()
# 				printc('g',f'emptied table {table}')
# 			except Exception as e:
# 				printc('r',f'unable to delete from `{table}`')
# 				conn.rollback()

if __name__ == '__main__':
	user = input("Enter database user: ")
	
	t0 = time.time()
	
	conn = psycopg2.connect(host="localhost", port=5432, \
		dbname="skynetflix_large2", user=user)
	
# 	empty_tables(conn)
	
	statements = (
		"SELECT setval('users_id_seq',(SELECT COALESCE(MAX(id),0)+1 FROM users),false);",
		"SELECT setval('movie_id_seq',(SELECT COALESCE(MAX(id),0)+1 FROM movie),false);",
		"SELECT setval('actor_id_seq',(SELECT COALESCE(MAX(id),0)+1 FROM actor),false);",
		"SELECT setval('director_id_seq',(SELECT COALESCE(MAX(id),0)+1 FROM director),false);"
	)
	with conn.cursor() as cur:
		try:
			for s in statements:
				cur.execute(s)
			conn.commit()
		except Exception as e:
			print('setval statements: exception:',repr(e))
			conn.rollback()
			print('setval statements failed to execute, exiting program')
			conn.close()
			sys.exit()
	
	populate_actor(conn)
	populate_director(conn)
	populate_plan(conn)
	populate_studio(conn)
	populate_users(conn)
	
	populate_movie(conn)
	populate_act(conn)
	populate_history(conn)
	populate_review(conn)
	populate_subscription(conn)
	
	tf = time.time()
	
	print('time elapsed (seconds):', tf-t0)
	
	print('all tables filled; exiting')
	conn.close()