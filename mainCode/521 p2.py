import sys
import re
import itertools as it
import datetime as dt
import pydoc
from functools import partial

import psycopg2
from psycopg2 import ProgrammingError, IntegrityError
from psycopg2.extras import execute_batch


import platform

"""
TO DO
    * specific error handling
    * print formatting
"""

MAX_ID_SIZE = 50
MAX_INFO_SIZE = 500

PRIMARY_FIELDS = ('genre\0', '# of results to return\0')
DATE_FIELDS = ('opening date\0', 'closing date\0')
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

_c = as_color

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
                continue
        except Exception as e:
            #             printc('r', 'custom_select error: '+repr(e))
            raise
        else:
            return i, r


def get_date(date_string, allow_empty=True, pattern = re.compile('\d+')):
    """Accept a date string, which can take forms of
    "YYYY [M[M]] [D[D]]" (enclosure in square brackets indicates optional input).
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
    r = [m.group() for m in pattern.finditer(date_string)]
    print('r:',r)
    if (not (0 < len(r) < 4)) or len(r[0])!=4:
    	print('malformed year')
    	return False
    if any(not (0< len(s) < 3) for s in it.islice(r,1,None)):
    	print('malformed other')
    	return False
    try:
        r = [int(s) for s in r]
        if len(r) == 1:
            return dt.date(r[0], 1, 1)
        if len(r) == 2:
            return dt.date(r[0], r[1], 1)
        return dt.date(r[0], r[1], r[2])
    except (ValueError, AttributeError) as e:
        # AttributeError if date_string is malformed
        # ValueError if date is invalid
        # both yield the same result: not a valid date
        print('get date: error:',repr(e))
        return False

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


def get_integer(istring, limit=120):
    """Accept.verify an integer string less than `limit` (120 by default)."""
    s = istring.strip()
    if not s.isdigit():
        return False
    s = int(s)
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
                f'enter a valid count (you entered {count})')
        if count < 1:
            raise ValueError(
                'enter a count > 0 (you entered {count})')
        # this will be passed to the parameterized query
        values.append(str(count))
        return f'LIMIT %s'  # SQL for the paratemerized query
    return ''



def parse_genre(f, where, values):
    """Given mapping `f` of field names to inputted values, process user input
    corresopnding to a genre of movies. Modify `where` and `values` lists in place
    for the sake of constructing SQL code to filter results based on genre."""
    genre = f.get('genre\0','')
    if genre:
        where.append("genre=%s")  # let psycopg2 paratemerize query
        values.append(f['genre\0'])  # corresopnding user input string
    return genre

def pluralize(n, kind):
	return f"{n} {kind}{'s' if n>1 else ''}"

# # # # # # # # # # # # # # # # Queries # # # # # # # # # # # # # # # #


def get_highest_rated_actors(conn, *, fields=PRIMARY_FIELDS):
    where = []
    values = []
    f = {f: i for f, i in zip(fields, menu_selections(*fields))}

    parse_genre(f, where, values)
    parse_dates('M.date_released', where, values)
    count = filter_return_count(f, values)

    where = f'WHERE {" AND ".join(where)}' if where else ''

    with conn.cursor() as cur:
        try:
            cur.execute(
                f"""
                WITH average_ratings AS
                    (SELECT movie_id, AVG(rating) avg_r
                     FROM review
                     GROUP BY movie_id
                    )
                SELECT
                    first_name || ' ' || last_name AS name,
                    AVG(AR.avg_r) avg_rating
                FROM
                    actor A
                    JOIN act ON (act.actor_id = A.id)
                    JOIN average_ratings AR ON (act.movie_id = AR.movie_id)
                    JOIN movie M ON (M.id = AR.movie_id)
                {where}
                GROUP BY name
                ORDER BY avg_rating DESC
                {count};
                """,
                values
            )
            printc('b','actors in order of rating:\n- - - -')
            for name,r in cur:
            	print(f'    {name}: {float(r):.1f}')
            print('- - - -')
        except Exception as e:
            print('get_highest_rated_actors: error:', repr(e))


#     Which directors have the highest associated movie ratings?
#         + Calculate a director's rating as the average rating across all the movies he directed

def get_highest_rated_directors(conn, *, fields=PRIMARY_FIELDS):
    where = []
    values = []
    f = {f: i for f, i in zip(fields, menu_selections(*fields))}

    parse_genre(f, where, values)
    parse_dates('M.date_released', where, values)
    count = filter_return_count(f, values)

    where = f'WHERE {" AND ".join(where)}' if where else ''

    with conn.cursor() as cur:
        try:
            cur.execute(
                f"""
                WITH average_ratings AS
                    (SELECT movie_id, AVG(rating) avg_r
                     FROM review
                     GROUP BY movie_id
                    )
                SELECT
                    first_name || ' ' || last_name AS name,
                    AVG(AR.avg_r) avg_rating
                FROM
                    director D
                    JOIN movie M ON (D.id = M.director_id)
                    JOIN average_ratings AR ON (M.id = AR.movie_id)
                {where}
                GROUP BY name
                ORDER BY avg_rating
                {count};
                """,
                values
            )
            print('*** CURSOR RESULTS:', list(cur))  # "<PRINT THE RESULTS>"
        except Exception as e:
            print('get_highest_rated_directors: error:', repr(e))

#     Which movies are the most popular in a given time frame?


def get_popular_movies(conn, *, fields=PRIMARY_FIELDS):
    """Get the most watched movies in a certain time frame, optionally
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


#     Which users watch the most movies (of a certain genre) in a given time frame?
def get_busiest_users(conn, *, fields=PRIMARY_FIELDS):
    """Get the most busiest users in a certain time frame, optionally
    filtering by genre and limiting number of query results returned."""
    where = []
    values = []
    f = {f: i for f, i in zip(fields, menu_selections(*fields))}

    genre = parse_genre(f, where, values)
    parse_dates('watch_date', where, values)
    count = filter_return_count(f, values)

    where = f'WHERE {" AND ".join(where)}' if where else ''
    
    print('where:',where)
    print('values:',values)
    
    if genre:
        _from = f'history H JOIN movie M ON (H.movie_id = M.id)'
    else:
    	_from = 'history'
    
    with conn.cursor() as cur:
        try:
            cur.execute(
                f"""
                SELECT user_id, COUNT(*) num_watches
                FROM {_from}
                {where}
                GROUP BY user_id
                ORDER BY COUNT(*) DESC
                {count};""",
                values
            )
            print('history results:')
            extra = f" (in genre '{genre}')" if genre else ''
            for u,c in cur:
            	print(f'    user {u} has watched {c} movies{extra}')
        except Exception as e:
            print('get_busiest_users: error:', repr(e))

#     Get highest-rated movie(s) for a given time frame, genre


def get_highest_rated_movies(
        conn, *,
        fields=PRIMARY_FIELDS
):
    """Get the highest-rated movies in a certain time frame, optionally
    filtering by genre and limiting number of query results returned."""
    where = []
    values = []
    f = {f: i for f, i in zip(fields, menu_selections(*fields))}

    parse_genre(f, where, values)
    parse_dates('date_released', where, values)
    count = filter_return_count(f, values)

    where = f'WHERE {" AND ".join(where)}' if where else ''

    with conn.cursor() as cur:
        try:
            cur.execute(
                f"""
                WITH average_ratings AS
                    (SELECT movie_id, AVG(rating) avg_r
                     FROM review
                     GROUP BY movie_id
                    )
                
                SELECT title, AR.avg_r AS average_rating
                FROM movie JOIN average_ratings AR
                    ON movie.id = AR.movie_id
                {where}
                ORDER BY average_rating DESC
                {count};""",
                values
            )
            print('*** CURSOR RESULTS:', list(cur))  # "<PRINT THE RESULTS>"
        except Exception as e:
            print('get_highest_rated_movies: error:', repr(e))


#     Get all users whose subscriptions are ending within a short time frame (week or month) from the current date

def ending_subscriptions(conn, *, options=set('dwm'),
                         conv=dict(d=1, w=7, m=30),
                         prompt="enter window here ('d'=day, 'w'=week, or 'm'=month):"):
    """Generate a list of users whose subscriptions are ending soon.
    The definition of 'soon' is specified by user input."""

    # month = 30 days, week = 7 days
    d = conv[simple_select(prompt, options)]
    window = f'{d} days'
    
    # because postgresql doesn't understand referencing a
    # column alias just created
    end_date = 'start_date + month_length'
    
    with conn.cursor() as cur:
        try:
            cur.execute(
            f"""
            SELECT
                U.first_name || ' ' || U.last_name AS name,
                ({end_date})::date AS end_date
            FROM
                subscription S
                JOIN plan P ON (S.plan_name = P.name)
                JOIN users U ON (U.id = S.user_id)
            WHERE
                {end_date} > CURRENT_DATE AND
                {end_date} - CURRENT_DATE <= '{window}'
            ORDER BY {end_date} DESC;"""
                # direct input of `window` by formatting is okay here
                # since the inputs are restricted by the `conv` dictionary
            )
            r = next(cur,None)
            if r is None:
            	print('no users have subscriptions ending within {pluralize{d, "day"}}')
            else:
            	result = it.chain((r,),cur)
            	print(f'following users have subscriptions ending within {pluralize(d, "day")}')
            	for name,end_date in result:
            		print(f'    {name}:',end_date)
        except Exception as e:
            print('ending_subscriptions: error:', repr(e))

# tell how many users are on currently each of the subscription plans


def generate_subscription_counts(conn):
    """Generate counts of how many users are currently subscribed for each plan."""
    with conn.cursor() as cur:
        try:
            cur.execute(
            """
            SELECT name, COUNT(*) count
            FROM subscription S JOIN plan P ON (S.plan_name = P.name)
            WHERE
                start_date < CURRENT_DATE
                AND start_date + month_length > CURRENT_DATE
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
    )[1]

    with conn.cursor() as cur:
        try:
            cur.execute(
            f"""
            SELECT 
                DATE_PART('year',start_date) AS year,
                DATE_PART('month',start_date) AS month,
                plan_name,
                COUNT(*)
            FROM subscription
            WHERE CURRENT_DATE-start_date <= (30 * %s)
            GROUP BY plan_name, year, month
            ORDER BY year DESC, month DESC, plan_name ASC;
            """,
            (m,)
            )
            # TO DO: pretty print in table
            for year, group in it.groupby(cur, lambda tup: tup[0]):
                print(int(year))
                for _, month, name, count in group:
                    print('   ', 'month:', month, 'name:',name, 'count:',count)
        except Exception as e:
            print('subscription_history: error:', repr(e))


def get_user_current_subscription_window(conn):
    """For a given user id, get the start and end dates of his current subscription."""
    id, = menu_selections('user id')
    
    end_date = 'start_date + month_length'

    with conn.cursor() as cur:
        try:
            cur.execute(
            f"""
            SELECT
                start_date,
                EXTRACT(MONTH FROM month_length) AS month,
                EXTRACT(YEAR FROM month_length) AS year,
                ({end_date})::date AS end_date,
                name
            FROM
                subscription S JOIN plan P ON (S.plan_name = P.name)
            WHERE
                user_id = %s AND
                start_date <= CURRENT_DATE AND
                {end_date} >= CURRENT_DATE;
            """,
                (id,)
            )
            result = next(cur, None)
            if result is None:
                printc('b', f'No subscription found for user {id}')
            else:
            	s,m,y,e,n = result
            	m,y = int(m),int(y)
            	m = pluralize(m, 'month')
            	y = pluralize(y, 'year')
            	t = f'{y}{" "*(bool(y)*bool(m))}{m}'
            	print(f"user {id}'s current subscription is the '{_c(n,'b')}'"
            	      f"plan ({_c(t,'g')}), from {_c(s,'r')} - {_c(e,'r')}")
        except Exception as e:
            print('get_user_current_subscription_window: error:', repr(e))


def get_actor_director_pairs(conn, *, prompt = PRIMARY_FIELDS[1]):
    """Get the number of movies that each actor, director pair have collaborated
    on, in descending order, with option to limit result count."""
	
    count = input(empty_notice(prompt))
    if count.isdigit():
    	count = f'LIMIT {count}'
    else:
    	count = ''

    with conn.cursor() as cur:
        try:
            cur.execute(
            f"""
            SELECT actor_id, director_id, COUNT(*) num_movies
            FROM
                act A JOIN movie M ON (A.movie_id = M.id)
            GROUP BY
                actor_id, director_id
            ORDER BY
                COUNT(*) DESC, actor_id ASC, director_id ASC
            {count};
            """
            )
            print('actor id, director id, # movies\n- - - -')
            for a, d, m in cur: print(f'    a={a}, d={d}, # movies = {m}')
            print('- - - -')
        except Exception as e:
            print('get_actor_director_pairs: exception:', repr(e))


def get_user_genres(conn):
    """Get, for each user, which genre(s) that user is most likely to watch."""

    with conn.cursor() as cur:
        try:
            cur.execute(
            """
            WITH
                user_genre_counts as
                (SELECT user_id, genre, COUNT(*) c
                 FROM history H
                    JOIN movie M ON H.movie_id = M.id
                 GROUP BY
                    user_id, genre
                ),
        
                user_genre_max as
                (SELECT user_id, MAX(c) mc
                 FROM user_genre_counts
                 GROUP BY user_id
                ),
                
                user_genre_res AS
                (SELECT user_id, genre, c
                 FROM user_genre_counts NATURAL JOIN user_genre_max
                 WHERE c = mc
                 ORDER BY user_id)
            
            SELECT user_id, string_agg(genre, ', '), MIN(c)
            FROM user_genre_res
            GROUP BY user_id;
            """
            )
            print('most common genre for each user (with ties included):\n- - - -')
            for u, g, c in cur: print(f'    user {u}: {g} {c}')
            print('- - - -')
        except Exception as e:
            print('get_user_genres: exception:', repr(e))


def get_highest_grossing_studios(conn):
    """Get the total gross amount earned by each studio, in descending order."""

    with conn.cursor() as cur:
        try:
            cur.execute(
            """
            SELECT studio, SUM(gross_income) revenue
            FROM movie
            GROUP BY
                studio
            ORDER BY revenue;
            """
            )
            for s,r in cur:
                print(f'{s}: total income = {r}')
        except Exception as e:
            print('get_highest_grossing_studios: exception:', repr(e))

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
            FROM subscription S JOIN plan P ON (S.plan_name = P.name)
            WHERE
                user_id = %s AND
                start_date <= CURRENT_DATE AND
                start_date + month_length >= CURRENT_DATE;
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
            FROM subscription S JOIN plan P ON (S.plan_name = P.name)
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
                (title, url, director_id, date_released, info)
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
            # printc('r', ...)
            # make sure ROLLBACK if failure
            ...
    conn.autocommit = True


# Add new actors to an already existing movie


def add_actors_to_movie(conn, *, id_parse=ACTOR_ID_PARSE):
    printc('b',
           '** Note ** : To enter actors, provide each actor\'s id #, space-separated. '
           'If the actor is a main actor, enter the actor id with a * '
           'at its end (without space), e.g. 12345*.'
           )
    movie_id, actors = menu_selections('movie id', 'actor ids')
    actors, main_values = zip(*(a.groups() for a in id_parse.finditer(actors)))
    main_values = tuple(map(bool, main_values))
    
    printc('b','provide roles for each actor specified (max 50 chars per role):')
    roles = (input(f'    role for actor {a}:  ') for a in actors)
    
    act_insert_list = [(a, movie_id, r, b) for a,r,b zip(actors, roles, main_values)]
    del actors, main_values, roles
    
    conn.autocommit = False
    with conn.cursor() as cur:
        # IMPORTANT -- make this a transaction that succeeds only if all insertions successful
        try:
			execute_batch(cur,
			"""
			INSERT INTO act
				(actor_id, movie_id, role, if_main)
			VALUES (%s, %s, %s, %s);""",
			act_insert_list
            )
			
            conn.commit()
            printc('g', f'successully added {len(act_insert_list)} actors to movie {movie_id}')
        except Exception as e:
            print('add_actors_to_movie: error:', repr(e))
            conn.rollback()

    conn.autocommit = True


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
    str(i):f for i,f in enumerate(sorted
    ((
#         get_active_movies,
        get_highest_rated_actors,
        get_highest_rated_directors,
        get_popular_movies,
        get_busiest_users,
        get_highest_rated_movies,
        ending_subscriptions,
        generate_subscription_counts,
        subscription_history,
        get_user_current_subscription_window,
        leave_a_review,
        sign_user_up_for_plan_today,
        sign_user_up_for_future_plan,
        add_user,
        remove_user,
        add_movie,
        add_actors_to_movie,
        track_watch_event,
        get_actor_director_pairs,  ## check with new schema
        get_user_genres,  ## check with new schema
        get_highest_grossing_studios  ## check with new schema
    ), key = lambda f: f.__name__))
}

if __name__ == '__main__':
   
    connect_port = "5432"
    if (platform.system()=='Windows'):
        #  ssh tunnel enable this program runs on any device
        #  remember install sshtunnel first: $pip install sshtunnel

        from sshtunnel import SSHTunnelForwarder
        #create ssh tunnel
        tunnel =  SSHTunnelForwarder(
            ('rocco.cs.wm.edu',11536), 
            ssh_username = 'lwang24',
            ssh_password = '1rujiwang',
            remote_bind_address = ('localhost',5432) #database
            ) 
        tunnel.start()
        print ("SSh tunnel connected:",
        "\n\tlocal bind host:",tunnel.local_bind_host,
        "\n\tlocal bind port:",tunnel.local_bind_port,"\n") 
        connect_port = tunnel.local_bind_port 
        
    # create database connection
    user = input("Enter database user: ")
    database = simple_select('Which database? (enter s for small, b for big)', ('s','b'))
    database = 'skynetflix_small' if database=='s' else 'skynetflix_big'
    conn = psycopg2.connect(
        database=database,
        user=user,
        host='localhost',
        port=connect_port
    )
    cur = conn.cursor()
    
    ################
    
    
    
    
    conn.autocommit = True  # as recommended by documentation

    # create indices: movie.date_released, ...

    while True:
        printc('b', '**** AVAILABLE FUNCTIONS:')
        for i, f in sorted((int(i), f) for i, f in _func_mapping.items()):
            printc('dg', f'    {i}', f.__name__.replace('_', ' '))
        
        try:
            f = input('enter an integer to call a function, or \'q\' to exit:\n    >>> ')
            if f == 'q':
                break
            else:
                _f = _func_mapping.get(f)
                if _f is not None:
                	_f(conn)
                else:
                	printc('r',f'input `{f}` is not recognized')

        except Exception as e:
            print('top-level exception:', repr(e))
    
    conn.close()
    if (platform.system()=='Windows'):
        tunnel.stop()
    printc('b', '\n-- -- -- -- -- -- -- --\nExiting...')
