"""
TO DO
	* specific error handling
	* print formatting
"""

import sys
import re
import itertools as it
import datetime as dt
import pydoc
from functools import partial

import psycopg2
from psycopg2 import ProgrammingError, IntegrityError
from psycopg2.extras import execute_batch

#  ssh tunnel enable this program runs on any device
#  remember install sshtunnel first: $pip install sshtunnel
from sshtunnel import SSHTunnelForwarder

MAX_ID_SIZE = 50
MAX_INFO_SIZE = 500

ACTOR_ID_PARSE = re.compile('(\d{1,%i})([*]{,1})' % MAX_ID_SIZE)

# more portable implementation might use a pypi packaged
# but this suffices for now
COLORS = {  # for terminal output
    'r': 91,            # red (bright)
    'dr': 31,            # red (dark)
    'o': '38;5;202',        # orange
    'mac': '38;5;214',    # macaroni
    'y': 33,            # yellow (darker)
    'm': 35,            # magenta
    'g': 32,            # green (medium)
    'dg': '38;5;22',        # green (dark)
    'teal': 36,
    'b': 34,             # blue
    'orchid': '38;5;165',
    'p': '38;5;56',        # purple
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
    if (platform.system() == 'Linux'):
        if isinstance(c, int):
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
    if (platform.system() == 'Linux'):
        if isinstance(c, int):
            return f'\033[1m\033[{c}m{s}\033[0m'
        try:
            return f'\033[1m\033[{COLORS[c]}m{s}\033[0m'
        except KeyError:
            return s
    else:
        return s


def printc(color, *args, **kw):
    """Print text in a given color."""
    print(*(as_color(a, color) for a in args), **kw)


def page_color(text):
    """Send text to the pagerm preserving ANSI color command interpretation."""
    # https://stackoverflow.com/questions/7922973
    # consider writing to a buffer rather than creating a potentially very large string
    pydoc.pipepager(text, cmd='less -R')


def truncate(s, l):
    return s if len(s) < l else s[:l]


def empty_notice(s):
    """Convenience method. '\\0' in a field name is replaced with a message
    telling the user to hit the return key in order to leave the field blank.
    `s` is the field that may or may not contain '\\0', and the function returns
    the new message string (same as original is no '\\0' is present)."""
    return s.replace('\0', ' (press <RETURN> to leave empty)')


def menu_selections(*fields):
    """Input loop. Prompt the user for input for each field in `fields`,
    asking for confirmation at the end and allowing for re-entry.
    """
    while True:
        inputs = tuple(input(f"Enter {empty_notice(f)}: ") for f in fields)
        print('YOU ENTERED:')
        for f, i in zip(fields, inputs):
            print(f"    >>> {f} = '{i}'")

        if input(
                "IS THIS CORRECT? (type 'y' without quotes to acknowledge): "
        ).lower() == 'y':
            return inputs


def simple_select(prompt, options, msg=None):
    """Input loop. Use a collection of values `options` to verify user input.
    Input is considered valid iff it is present in this collection. No constraint
    is imposed on the collection type. Returns the raw user input."""
    print(empty_notice(prompt))
    while True:
        i = input('    >>> ')
        if i not in options:
            if msg is None:
                msg = f'Input "{i}" is invalid: select from {options} (re-enter here):'
            else:
                msg = f'{msg}: re-enter here:'
            printc('r', msg)
        else:
            return i


def custom_select(prompt, matcher, msg=None):
    """Input loop. Use a custom callable `matcher` to verify user input.
    `matcher` is expected to return an object that is true in a boolean context
    if input is valid, and a false object if input is invalid. This function returns
    a 2-tuple: (raw user input, result of calling matcher on raw user input)."""
    print(empty_notice(prompt))
    while True:
        i = input('\n    >>> ')
        try:
            r = matcher(i)
            if not r:
                if msg is None:
                    msg = f'Input "{i}" is invalid: re-enter here:'
                else:
                    msg = f'{msg}: re-enter here:'
                printc('r', msg)
        except Exception as e:
            # 			printc('r', 'custom_select error: '+repr(e))
            raise
        else:
            return i, r


def get_date(date_string,
             matcher=re.compile(
                 '(\d{1,2}\s+)?(\d{1,2}\s+)?(\d{4})'
             ).search,
             allow_empty=True
             ):
    """Accept a date string, which can take forms of
    "[D[D]] [M[M]] YYYY" (enclosure in square brackets indicates optional input).
    If valid input is given, a `datetime.date` object is returned.
    If invalid input is given, the boolean value False is returned.
    If `allow_empty`, the date can be left empty, and '-' will be returned;
    otherwise, it cannot be left empty.
    """
    if not date_string:
        if allow_empty:
            # provide option of empty value
            return '-'
        return False
    r = matcher(date_string)
    try:
        r = list(filter(r.groups()))
        if len(r) == 1:
            return dt.date(r[0], 1, 1)
        if len(r) == 2:
            return dt.date(r[1], r[0], 1)
        return dt.date(r[2], r[1], r[0])
    except (ValueError, AttributeError):
        # AttributeError if date_string is malformed
        # ValueError if date is invalid
        # both yield the same result: not a valid date
        return False


def get_integer(istring, limit=120):
    """Accept.verify an integer string less than `limit` (120 by default)."""
    s = istring.strip()
    if not s.isdigit():
        return False
    if s > limit:
        return False
    return s


def get_future_date(date_string):
    """Get a date that is after today's date (whatever today happens to be)."""
    date = get_date(date_string, allow_empty=False)
    if date < dt.date.today():
        return False
    return date


def filter_date_range():
    """Prompt user for start, end dates to isolate query results
    from a specific time range. Returns two `datetime.date` instances."""
    start_date = custom_select("specify start date\0:", get_date)[1]
    if start_date == '-':  # no start date provided
        start_date = ''
    end_date = custom_select("specify end date\0:", get_date)[1]
    if end_date == '-':  # no end date provided
        end_date = ''
    return start_date, end_date


# NOT USED AT THE MOMENT
"""
def get_cutoff_date(date_cutoff_string):
	if date_cutoff_string[0] not in '<>':
		return False
	date = get_date(date_cutoff_string[1])
	if not date:
		return False
	return date_cutoff_string[0], date
"""


def filter_return_count(f, values):
    """Given mapping `f` of field names to inputted values,
    process the string that corresponds to a limit on the number
    of items to return from a query. The `values` list is updated to hold
    this string after it is verified. Returns the paramtereized SQL clause.
    Raises ValueError if verification fails."""
    # if this raises an error, it will be handled outside this function
    count = f.get('# of results to return\0')
    if count:
        try:
            count = int(count)
        except ValueError:
            raise ValueError(
                f'get highest rated movies: enter a valid count (you entered {count})')
        if count < 1:
            raise ValueError(
                'get highest rated movies: enter a count > 0 (you entered {count})')
        # this will be passed to the parameterized query
        values.append(str(count))
        return f'LIMIT %s'  # SQL for the paratemerized query
    return count


PRIMARY_FIELDS = ('genre\0', '# of results to return\0')
DATE_FIELDS = ('opening date\0', 'closing date\0')


def parse_genre(f, where, values):
    """Given mapping `f` of field names to inputted values, process user input
    corresopnding to a genre of movies. Modify `where` and `values` lists in place
    for the sake of constructing SQL code to filter results based on genre."""
    genre = f.get('genre\0')
    if genre:
        where.append("genre=%s")  # let psycopg2 paratemerize query
        values.append(f['genre\0'])  # corresopnding user input string


def parse_dates(date_name, where, values):
    """Take input for start date, end date from user, validating input.
    Modify the `where` and `values` lists in place for the purpose of
    constructing SQL code to filter based on provided dates. `date_name`
    is the name of the field in the respective table that gives the date.
    Returns nothing."""
    start_date, end_date = filter_date_range()
    # `date_name` is hard-coded, so directly inserting into query is safe
    if start_date:
        where.append(f'{date_name} >= %s')
        values.append(start_date)
    if end_date:
        where.append(f'{date_name} <= %s')
        values.append(end_date)


# # # # # # # # # # # # # # # # Queries # # # # # # # # # # # # # # # #

def list_genres(conn):
    with conn.cursor() as cur:
        try:
            cur.execute("SELECT name, info FROM genre;")
            for genre, info in cur:
                printc('b', f'*** {genre} ***')
                print(info)
                print('-' * 70)
        except Exception as e:
            print('list_genres: error:', repr(e))


def get_active_movies(
        conn, *, fields=PRIMARY_FIELDS + ('keywords',),
        prune_pattern=re.compile('([A-z]|[0-9]|\s)+'),
        parse_pattern=re.compile('\S+{1,20}')
):
    """Get a list of movies that are actively available for streaming,
    with options to filter by release date and genre, as well as keywords."""
    print('obtaining active movie list...')
    printc('b',
           '** Note **: keywords, if provided, are logically joined by AND, not OR.'
           ' May be provided in any order. Enter all keywords on one line,'
           ' space-separated. Keywords longer than 20 characters will be truncated.'
           ' Max 10 keywords will be processed.'
           ' Symbols other than plain letters, spaces, or numbers will be ignored.'
           )
    where = []
    values = []
    f = {f: i for f, i in zip(fields, menu_selections(*fields))}

    parse_genre(f, where, values)
    parse_dates('date_produced', where, values)

    keywords = f.get('keywords')
    if keywords:
        keywords = ''.join(m.group() for m in prune_pattern.finditer(keywords))
        for k in it.islice((m.group() for m in parse_pattern.finditer(keywords)), 10):
            where.append(f"title LIKE %s")  # SQL clause
            values.append(f'%{k}%')  # for paramterizing query

    count = filter_return_count(f, values)

    # filter movies that are available for streaming
    where.append('available=true')

    where = f'WHERE {" AND ".join(where)}' if where else ''

    with conn.cursor() as cur:
        try:
            cur.execute(
                f"""
				SELECT title FROM movie
				{where}
				ORDER BY title
				{count};""",
                values
            )
            print('*** CURSOR RESULTS:', list(cur))  # "<PRINT THE RESULTS>"
        except Exception as e:
            print('get_active_movies: error:', repr(e))

# 	Who are the most popular actors?
# 		+ Which actors star in the most movies in a given time?


def get_busiest_actors(conn, *, fields=PRIMARY_FIELDS):
    """Get the actors featured in the most movies in some time frame, optionally
    filtering by genre and limiting number of query results returned."""
    where = []
    values = []
    f = {f: i for f, i in zip(fields, menu_selections(*fields))}

    parse_genre(f, where, values)
    parse_dates('date_produced', where, values)
    count = filter_return_count(f, values)

    where = f'WHERE {" AND ".join(where)}' if where else ''

    with conn.cursor() as cur:
        try:
            cur.execute(
                f"""
				SELECT
					first_name || ' ' || last_name AS name,
					COUNT(*) num_movies_acted
				FROM actors
					JOIN act
					ON (actors.id = act.actor_id)
				{where}
				GROUP BY name
				ORDER BY COUNT(*) DESC
				{count};""",
                values
            )
            print('*** CURSOR RESULTS:', list(cur))  # "<PRINT THE RESULTS>"
        except Exception as e:
            print('get_busiest_actors: error:', repr(e))

# 	Which actors have the highest associated movie ratings?
# 		* Calculate an actor's rating as the average rating across all the movies he starred in


def get_highest_rated_actors(conn, *, fields=PRIMARY_FIELDS):
    where = []
    values = []
    f = {f: i for f, i in zip(fields, menu_selections(*fields))}

    parse_genre(f, where, values)
    parse_dates('date_produced', where, values)
    count = filter_return_count(f, values)

    where = f'WHERE {" AND ".join(where)}' if where else ''

    with conn.cursor() as cur:
        try:
            cur.execute(
                """
				SELECT
					first_name || ' ' || last_name AS name,
					AVG(average_rating)
				FROM
					actors A
					JOIN act ON (act.actor_id = A.id)
					JOIN movie ON (act.movie_id = movie.id)
				{where}
				GROUP BY name
				{count};
				""",
                values
            )
            print('*** CURSOR RESULTS:', list(cur))  # "<PRINT THE RESULTS>"
        except Exception as e:
            print('get_highest_rated_actors: error:', repr(e))

# 	Which directors have the highest associated movie ratings?
# 		+ Calculate a director's rating as the average rating across all the movies he directed


def get_highest_rated_directors(conn, *, fields=PRIMARY_FIELDS):
    where = []
    values = []
    f = {f: i for f, i in zip(fields, menu_selections(*fields))}

    parse_genre(f, where, values)
    parse_dates('date_produced', where, values)
    count = filter_return_count(f, values)

    where = f'WHERE {" AND ".join(where)}' if where else ''

    with conn.cursor() as cur:
        try:
            cur.execute(
                """
				SELECT
					first_name || ' ' || last_name AS name,
					AVG(average_rating) avg_rating
				FROM
					directors D
					JOIN movie ON (D.id = movie.director_id)
				{where}
				GROUP BY name
				{count};
				""",
                values
            )
            print('*** CURSOR RESULTS:', list(cur))  # "<PRINT THE RESULTS>"
        except Exception as e:
            print('get_highest_rated_directors: error:', repr(e))

# 	Which movies are the most popular in a given time frame?


def get_popular_movies(conn, *, fields=PRIMARY_FIELDS):
    """Get the most popular movies in a certain time frame, optionally
    filtering by genre and limiting number of query results returned."""
    where = []
    values = []
    f = {f: i for f, i in zip(fields, menu_selections(*fields))}

    parse_genre(f, where, values)
    parse_dates('watch_time', where, values)
    count = filter_return_count(f, values)

    where = f'WHERE {" AND ".join(where)}' if where else ''

    with conn.cursor() as cur:
        try:
            cur.execute(
                f"""
				SELECT M.title, COUNT(*) num_watches
				FROM history H
					JOIN movie M
					ON (M.id = H.movie_id)
				{where}
				GROUP BY M.id
				ORDER BY COUNT(*) DESC
				{count};""",
                values
            )
            print('*** CURSOR RESULTS:', list(cur))  # "<PRINT THE RESULTS>"
        except Exception as e:
            print('get_popular_movies: error:', repr(e))

# 	Who directs the most movies in a given time frame?


def get_busiest_directors(conn, *, fields=PRIMARY_FIELDS):
    """Get the most productive directors in a certain time frame, optionally
    filtering by genre and limiting number of query results returned."""
    where = []
    values = []
    f = {f: i for f, i in zip(fields, menu_selections(*fields))}

    parse_genre(f, where, values)
    parse_dates('date_produced', where, values)
    count = filter_return_count(f, values)

    where = f'WHERE {" AND ".join(where)}' if where else ''

    with conn.cursor() as cur:
        try:
            cur.execute(
                f"""
				SELECT
					D.first_name || ' ' || D.last_name AS name,
					COUNT(*) num_movies_directed
				FROM director D
					JOIN movie M
					ON (D.id = M.director_id)
				{where}
				GROUP BY name
				ORDER BY COUNT(*) DESC
				{count};""",
                values
            )
            print('*** CURSOR RESULTS:', list(cur))  # "<PRINT THE RESULTS>"
        except Exception as e:
            print('get_busiest_directors: error:', repr(e))


# 	Which users watch the most movies (of a certain genre) in a given time frame?
def get_busiest_users(conn, *, fields=PRIMARY_FIEDS):
    """Get the most binge-heavy movie watchers in a certain time frame, optionally
    filtering by genre and limiting number of query results returned."""
    where = []
    values = []
    f = {f: i for f, i in zip(fields, menu_selections(*fields))}

    parse_genre(f, where, values)
    parse_dates('watch_time', where, values)
    count = filter_return_count(f, values)

    where = f'WHERE {" AND ".join(where)}' if where else ''

    with conn.cursor() as cur:
        try:
            cur.execute(
                f"""
				SELECT user_id, COUNT(*) num_watches
				FROM history
				{where}
				GROUP BY user_id
				ORDER BY COUNT(*) DESC
				{count};""",
                values
            )
            print('*** CURSOR RESULTS:', list(cur))  # "<PRINT THE RESULTS>"
        except Exception as e:
            print('get_busiest_users: error:', repr(e))

# 	Get highest-rated movie(s) for a given time frame, genre


def get_highest_rated_movies(
        conn, *,
        fields=('genre\0', '# of results to return\0',
                'opening date\0', 'closing date\0')
):
    """Get the highest-rated movies in a certain time frame, optionally
    filtering by genre and limiting number of query results returned."""
    where = []
    values = []
    f = {f: i for f, i in zip(fields, menu_selections(*fields))}

    parse_genre(f, where, values)
    parse_dates('date_produced', where, values)
    count = filter_return_count(f, values)

    where = f'WHERE {" AND ".join(where)}' if where else ''

# 	f"""
# 	SELECT COALESCE(AVG(rating),0) R
# 	FROM <review table>
# 	"""
    with conn.cursor() as cur:
        try:
            cur.execute(
                f"""
				SELECT title, total_rating/total_rating_count AS average_rating
				FROM movie
				{where}
				ORDER BY average_rating DESC
				{count};""",
                values
            )
            print('*** CURSOR RESULTS:', list(cur))  # "<PRINT THE RESULTS>"
        except Exception as e:
            print('get_highest_rated_movies: error:', repr(e))

# 	Get all users whose subscriptions are ending within a short time frame (week or month) from the current date


def ending_subscriptions(conn, *, options=set('dwm'),
                         conv=dict(d=1, w=7, m=30),
                         prompt="enter window here ('d', 'w', or 'm'):"):
    """month = 30 days, week = 7 days"""
    window = conv[simple_select(prompt, options)]
    # get ending times of subscriptions within window
    with conn.cursor() as cur:
        try:
            cur.execute(
                f"""
			SELECT
				user_id,
				start_date + month_length AS end_date
			FROM
				subscription S
				JOIN plan P ON (S.plan_name = P.name)
			WHERE
				end_date - CURRENT_DATE() > INTEGER {window}
			ORDER BY end_date DESC;"""
                # direct input of `window` by formatting is okay here
                # since the inputs are restricted by the `conv` dictionary
            )
            print('*** CURSOR RESULTS:', list(cur))  # "<PRINT THE RESULTS>"
        except Exception as e:
            print('ending_subscriptions: error:', repr(e))

# tell how many users are on currently each of the subscription plans


def generate_subscription_counts(conn):
    with conn.cursor() as cur:
        try:
            cur.execute(
                """
			SELECT name, COUNT(*) count
			FROM subscriptions S JOIN plan P ON (S.plan_name = P.name)
			WHERE
				start_date < CURRENT_DATE()
				AND start_date + month_length > CURRENT_DATE()
			GROUP BY name;
			"""
            )
            # pretty print as table
            for plan, count in cur:
                print(plan, count)
        except Exception as e:
            print('generate_subscription_counts: error:', repr(e))


def subscription_history(conn):
    """Generate history of users signing up for subscriptions
    going back some specified # of months"""

    m = custom_select(
        "enter # of months of history to get (max 120):",
        get_integer
    )
    m = f'{m} MONTH{"" if m==1 else "S"}'

    with conn.get_cursor() as cur:
        try:
            cur.execute(
                f"""
			SELECT 
				DATE_PART('year',start_date) year,
				DATE_PART('month',start_date) month,
				plan_name,
				COUNT(*)
			FROM subscription
			WHERE CURRENT_DATE()-start_date <= INTERVAL '{m}'
			GROUP BY plan_name, year, month
			ORDER BY year DESC, month DESC, plan_name ASC;
			"""
            )
            # TO DO: pretty print in table
            for year, group in it.groupby(cur, lambda tup: tup[0]):
                print(year)
                for _, month, name, count in group:
                    print('   ', month, name, count)
        except Exception as e:
            print('subscription_history: error:', repr(e))


def get_user_current_subscription_window(conn):
    id = menu_selections('user id')

    with conn.cursor() as cur:
        try:
            cur.execute(
                """
			SELECT
				start_date,
				start_date + month_length AS end_date
			FROM
				subscription S JOIN plan P ON (S.plan_name = P.name)
			WHERE
				user_id = %s AND
				start_date <= CURRENT_DATE() AND
				end_date >= CURRENT_DATE();
			""",
                (id,)
            )
            if next(cur, None) is None:
                printc('b', f'No subscription found for user {id}')
        except Exception as e:
            print('get_user_current_subscription_window: error:', repr(e))


# # # # # # # # # # # # # # # # Updates # # # # # # # # # # # # # # # #

def leave_a_review(conn):
    """Leave a review for a particular user on a particular movie.
    If the user has already reviewed this movie, prompt the user
    to confirm that he wants to overwrite his previous review."""

    user_id, movie_id, rating, review = menu_selections(
        'user id', 'movie id', 'rating (integer from 1-5 inclusive)',
        'review content (max 256 chars)'
    )
    date = dt.date.today()

    with conn.cursor() as cur:
        try:
            cur.execute(
                """
			SELECT user_id,movie_id
			FROM review
			WHERE user_id = %s AND movie_id = %s;
			""",
                (user_id, movie_id)
            )
            if next(cur, None) is None:
                cur.execute(
                    """
				INSERT INTO review
					(user_id, movie_id, date, rating, content)
				VALUES (%s, %s, %s, %s, %s);
				""",
                    (user_id, movie_id, date, rating, review)
                )
            else:
                proceed = simple_select(
                    'WARNING: review already exists for '
                    f'user {user_id} on movie {movie_id}; '
                    'do you want to overwrite it (y/n)?',
                    ('y', 'n'),
                    msg="input not understood: please enter 'y' or 'n'"
                )
                if proceed:
                    cur.execute(
                        """
					UDPATE review SET
						(date, rating, content)
						=
						(%s, %s, %s)
					WHERE
						user_id = %s AND movie_id = %s;
					""",
                        (date, rating, review, user_id, movie_id)
                    )
        except Exception as e:
            print('leave_a_review: exception:', repr(e))


def sign_user_up_for_plan_today(conn):
    id, name = menu_selections('user id', 'subscription plan name')
    date = dt.date.today()

    with conn.cursor() as cur:
        try:
            cur.execute(
                """
			SELECT *
			FROM subscription S JOIN plan P ON (S.plan_name = plan.name)
			WHERE
				user_id = %s AND
				start_date <= CURRENT_DATE() AND
				start_date + month_length >= CURRENT_DATE();
			""",
                (id,)
            )
            if next(cur, None) is not None:
                raise ValueError(
                    f'cannot sign up user {id} for new subscription plan starting today; '
                    'that user\'s current subscription has not ended'
                )
        except Exception as e:
            print('sign_user_up_for_plan_today: error:', repr(e))
            return

    with conn.cursor() as cur:
        try:
            cur.execute(
                """
			INSERT INTO subscription
				(user_id, plan_name, start_date)
			VALUES (%s, %s, %s);
			""",
                (id, name, date)
            )
        except Exception as e:
            print('sign_user_up_for_plan_today: error occcured:', repr(e))


def sign_user_up_for_future_plan(conn):
    id, name = menu_selections('user id', 'subscription plan name')
    date = custom_select(
        "Enter a date past the current date", get_future_date)[1]

    with conn.cursor() as cur:
        try:
            cur.execute(
                """
			SELECT *
			FROM subscription S JOIN plan P ON (S.plan_name = plan.name)
			WHERE
				user_id = %s AND
				start_date <= %s AND
				start_date + month_length >= %s;
			""",
                (id, date, date)
            )
            if next(cur, None) is not None:
                raise ValueError(
                    f'cannot sign up user {id} for new subscription plan starting on {date}; '
                    'that user\'s has an overalpping subscription with that date'
                )
        except Exception as e:
            print('sign_user_up_for_plan_today: error:', repr(e))
            return

    with conn.cursor() as cur:
        try:
            cur.execute(
                """
			INSERT INTO subscription
				(user_id, plan_name, start_date)
			VALUES (%s, %s, %s);
			""",
                (id, name, date)
            )
        except Exception as e:
            print('sign_user_up_for_future_plan: error occcured:', repr(e))

# Add a new user


def add_user(conn):
    values = menu_selections(
        'first name', 'last name', 'email', 'phone',
        'pwd', 'any additional info [{info_cap} chars max]\0'
    )

    date = dt.datetime.now()

    with conn.cursor() as cur:
        try:
            cur.execute(
                """
			INSERT INTO users
				(first_name, last_name, email, phone, pwd, info, join_time)
			VALUES (%s, %s, %s, %s, %s, %s, %s)
			RETURNING id;
			""",
                values+(date,)
            )
            printc('g', f'added user {cur.fetchone()[0]}')
        except Exception as e:
            print('add_user: error:', repr(e))

# Remove user


def remove_user(conn):
    id = menu_selections('user id')

    with conn.cursor() as cur:
        try:
            cur.execute(
                """
			DELETE FROM users
			WHERE id=%s;
			""",
                (id,)
            )
            printc('g', f'deleted user {id}')
        except Exception as e:
            print('remove_user: error:', repr(e))

# Delist a movie


def delist_movie(conn):
    """Set a movie's active status to false, meaning it is not actively streaming.
    Keep historical records of the movie being watched."""
    m = menu_selections('movie id')
    with conn.cursor() as cur:
        try:
            cur.execute(
                """UPDATE movies SET available = 'false';"""
            )
            print('operation successful')  # "<PRINT SUCCESS>"
        except Exception as e:
            print('delist_movie: error:', repr(e))

# relist a movie


def relist_movie(conn):
    """Set a movie's active status to true, meaning it is actively streaming.
    The movie must already be present in the database.
    Keep historical records of the movie being watched."""
    m = menu_selections('movie id')
    with conn.cursor() as cur:
        try:
            cur.execute(
                """UPDATE movies SET available = 'true';"""
            )
            print('operation successful')  # "<PRINT SUCCESS>"
        except Exception as e:
            print('relist_movie: error:', repr(e))

# Add a new movie, requiring that actors be specified in addition to fields in 'movies' table


def add_movie(conn, *, id_parse=ACTOR_ID_PARSE, info_cap=MAX_INFO_SIZE):
    print('adding new movie')
    printc('b',
           '** Note ** : if release time is left blank, current date will be assumed. '
           'To enter actors, provide each actor\'s id #, space-separated. Actor ids are '
           'not required, but a director id is. If the actor is a main actor, '
           'enter the actor id with a * at its end (without space), e.g. 12345*.'
           )
    title, url, director_id, actors, info = menu_selections(
        'title', 'url', 'director id', 'actor ids\0',
        f'any additional info [{info_cap} chars max]\0'
    )
    info = truncate(info, info_cap)
    date = custom_select(
        "Enter release date (empty field sets date to today)", get_date)[1]
    if not date:
        date = dt.date.today()

    conn.autocommit = False
    with conn.cursor() as cur:
        # IMPORTANT -- make this a transaction that succeeds only if both parts
        # (adding movie and actors) succeeds
        try:
            cur.execute(
                """
			INSERT INTO movies
				(title, url, director_id, date_produced, info)
			VALUES (%s, %s, %s, %s, %s) RETURNING id;""",
                (title, url, director_id, date, info)
            )
            movie_id = cur.fetchone()[0]
            printc('g', f'movie {title} inserted with id {movie_id}')

            for actor_id in id_parse.finditer(actors):
                actor_id, is_main = actor_id.groups()
                if is_main:
                    cur.execute(
                        """
					INSERT INTO act
						(actor_id, movie_id, if_main)
					VALUES (%s, %s, %s);""",
                        (actor_id, movie_id, 'true')
                    )
                else:
                    cur.execute(
                        """
					INSERT INTO act
						(actor_id, movie_id)
					VALUES (%s, %s);""",
                        (actor_id, movie_id)
                    )

                printc(
                    'g', f'{"main "*is_main}actor {id} inserted on movie {movie_id}')
            conn.commit()
        except Exception as e:
            print('add_movie: error:', repr(e))
            conn.rollback()
            #printc('r', ...)
            # make sure ROLLBACK if failure
            ...
    conn.autocommit = True

# Add a new director


def add_director(conn):
    first, last, info = \
        menu_selections('first name', 'last name', 'any additional info\0')

    with conn.cursor() as cur:
        try:
            cur.execute(
                """
			INSERT INTO director
				(first_name, last_name, info)
			VALUES (%s, %s, %s);
			""",
                (first, last, info)
            )
        except Exception as e:
            print('add_director: error:', repr(e))

# Add new actors to an already existing movie


def add_actors_to_movie(conn, *, id_parse=ACTOR_ID_PARSE):
    printc('b',
           '** Note ** : To enter actors, provide each actor\'s id #, space-separated. '
           'If the actor is a main actor, enter the actor id with a * '
           'at its end (without space), e.g. 12345*.'
           )
    movie_id, actors = menu_selections('movie id', 'actor ids')

    conn.autocommit = False
    with conn.cursor() as cur:
        # IMPORTANT -- make this a transaction that succeeds only if all insertions successful
        try:
            for actor_id in id_parse.finditer(actors):
                actor_id, is_main = actor_id.groups()
                if is_main:
                    cur.execute(
                        """
					INSERT INTO act
						(actor_id, movie_id, if_main)
					VALUES (%s, %s, %s);""",
                        (actor_id, movie_id, 'true')
                    )
                else:
                    cur.execute(
                        """
					INSERT INTO act
						(actor_id, movie_id)
					VALUES (%s, %s);""",
                        (actor_id, movie_id)
                    )
            # COMMIT changes
            conn.commit()
        except Exception as e:
            print('add_actors_to_movie: error:', repr(e))
            conn.rollback()

    conn.autocommit = True

# Add a new actor


def add_actor(conn, *, info_cap=MAX_INFO_SIZE):
    first, last, info = menu_selections(
        'first name', 'last name',
        f'any additional info (truncated at {info_cap} chars)\0'
    )

    info = truncate(info, info_cap)

    with conn.cursor() as cur:
        try:
            cur.execute(
                """
			INSERT INTO actor
				(fisrt_name, last_name, info)
			VALUES (%s, %s, %s);
			""",
                (first, last, info)
            )
        except Exception as e:
            print('add_actor: error:', repr(e))

# record a new event when a user watches a movie


def track_watch_event(conn, *, fields=('user id', 'movie id')):
    u, m = menu_selections(*fields)
    d = custom_select("Enter date watched:",
                      partial(get_date, allow_empty=False),
                      'invalid date')[1]
    with conn.cursor() as cur:
        try:
            cur.execute(
                """
			INSERT INTO history
			(user_id,movie_id, <date>) VALUES (%s, %s, %s);""",
                (u, m, d)
            )
            print('operation successful')  # "<PRINT SUCCESS>"
        except Exception as e:
            print('track_watch_event: error:', repr(e))


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
_func_mapping = {
    '1':	list_genres,
    '2':	get_active_movies,
    '3':	get_busiest_actors,
    '4':	get_highest_rated_actors,
    '5':	get_highest_rated_directors,
    '6':	get_popular_movies,
    '7':	get_busiest_directors,
    '8':	get_busiest_users,
    '9':	get_highest_rated_movies,
    '10':	ending_subscriptions,
    '11':	generate_subscription_counts,
    '12':	subscription_history,
    '13':	get_user_current_subscription_window,
    '14':	leave_a_review,
    '15':	sign_user_up_for_plan_today,
    '16':	sign_user_up_for_future_plan,
    '17':	add_user,
    '18':	remove_user,
    '19':	delist_movie,
    '20':	relist_movie,
    '21':	add_movie,
    '22':	add_director,
    '23':	add_actors_to_movie,
    '24':	add_actor,
    '25':	track_watch_event
}

if __name__ == '__main__':
    user = input("Enter database user: ")

    if (platform.system() == 'Windows'):
        # create ssh tunnel
        tunnel = SSHTunnelForwarder(
            ('rocco.cs.wm.edu', 11536),
            ssh_username='lwang24',
            ssh_password='1rujiwang',
            remote_bind_address=('localhost', 5432)  # database
        )
        tunnel.start()
    print("SSh tunnel connected:",
          "\n\tlocal bind host:", tunnel.local_bind_host,
          "\n\tlocal bind port:", tunnel.local_bind_port, "\n")
    connect_port = tunnel.local_bind_port
    conn = psycopg2.connect(host="localhost", port=5432,
                            dbname="skynetflix_small", user=user)

    conn.autocommit = True  # as recommended by documentation

    # create indices: movie.date_produced, ...

    printc('b', '**** AVAILABLE FUNCTIONS:')
    for i, f in sorted((int(i), f) for i, f in _func_mapping.items()):
        printc('dg', f.__name__.replace('_', ' '))

    while True:
        try:
            f = input('enter an integer to call a function, or \'q\' to exit')
            if f == 'q':
                break
            else:
                _func_mapping[f](conn)

        except Exception as e:
            print('top-level exception:', repr(e))

    conn.close()

    printc('b', '\n-- -- -- -- -- -- -- --\nExiting...')
