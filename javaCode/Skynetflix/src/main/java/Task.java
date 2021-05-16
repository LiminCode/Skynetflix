import java.sql.*;
import java.util.Calendar;
import java.util.Date;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class Task {
	Utilities utility = new Utilities(); // for print in color
	DateUtil dateUtil = new DateUtil();

	/*
	 * Add new actors to an already existing movie
	 */
	public void add_actors_to_movie(Connection conn) {
		System.out.println(utility.as_bold_color("[iii]", "g") + " Add Actors to Movie ==>");
		System.out.println("** Note ** : To enter actors, provide each actor's id #, space-separated."
				+ " If the actor is a main actor, enter the actor id with a * at "
				+ "its end (without space), e.g. 12345*. To enter Roles, separate each actor's role by '#', leave space but also followed a '#' if the role is unknown. ");
		String[] fileds = new String[] { "Movie ID", "Actors", "Roles" };
		Utilities utility = new Utilities();
		String[] values = utility.menu_selections(fileds);
		int movie_id = parseIntwithName(values[0], "Movie ID");
		if (movie_id == -1) {
			return;
		}
		String[] actor_ids = values[1].split("\\s+");
		String[] actor_roles = values[2].split("#");
		System.out.println("actor_ids:" + actor_ids.hashCode());

		String sql = "INSERT INTO act  (actor_id, movie_id, if_main, role ) VALUES (?, ?, ?,?)";
		PreparedStatement statement = null;
		int count = 0;
		try {
			conn.setAutoCommit(false); // close auto commit
			for (int i = 0; i < actor_ids.length; i++) {
				String if_main = "0";
				if (actor_ids[i].contains("*")) {
					if_main = "1";
				}
				int actor_id = parseIntwithName(actor_ids[i].replace("*", ""), "Actor ID");
				if (actor_id == -1) {
					throw new Exception("Actor ID parse fail.");
				}
				statement = conn.prepareStatement(sql);
				statement.clearParameters();
				statement.setInt(1, actor_id); // movie id
				statement.setInt(2, movie_id); // movie id
				statement.setString(3, if_main); // if main
				statement.setString(4, actor_roles[i]); // role
				statement.executeUpdate();
				count++;
			}

			conn.commit(); // commit
			System.out.println(utility.as_color("[SUCCESS]", "g") + "  >>>> Insert successful. row added:" + count);
		} catch (SQLException sqle) {
			System.out.println("Could not insert act info into db." + sqle);
			try {
				conn.rollback();
			} catch (SQLException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		} catch (Exception e) {
			System.out.println("Could not insert act info into db.");
			try {
				conn.rollback();
			} catch (SQLException e1) {
				// TODO Auto-generated catch block
				e1.printStackTrace();
			}
			e.printStackTrace();
		} finally {
			try {
				conn.setAutoCommit(true);
			} catch (SQLException e1) {
				// TODO Auto-generated catch block
				e1.printStackTrace();
			}
			try {
				if (statement != null)
					statement.close();
			} catch (SQLException e) {
				System.out.println("SQL error: ");
				e.printStackTrace();
			} // end finally try
		}
		System.out.println(utility.as_bold_color("[iii]", "g") + "Add new Act-Movie finished.");

	}

	/*
	 * add_movie Add a new movie, requiring that actors be specified in addition to
	 * fields in 'movies' table
	 */
	public void add_movie(Connection conn) {
		System.out.println(utility.as_bold_color("[iii]", "g") + " Add New Movie ==>");
		String[] fileds = new String[] { "Title", "URL", "genre", "Released date (YYYY-MM-DD)", "Rating(R/PG/..)",
				"budget", "Summary", "Studio", "Director ID" };
		Utilities utility = new Utilities();
		String[] values = utility.menu_selections(fileds);
		// check if Director and Studio exists
		int director_id = 0;
		if (values[8].isBlank() == false) {
			director_id = Integer.parseInt(values[8]);
		}

		if (this.check_director_exsist(conn, director_id) == false) {
			System.out.println(
					utility.as_bold_color("[!!!]", "r") + " Director ID doesn't exsit, you might add director first.");
			return;
		}
		if (values[7].isBlank() == false) {

			if (this.check_studio_exsist(conn, values[7]) == false) {
				System.out.println(
						utility.as_bold_color("[!!!]", "r") + " Studio doesn't exsit. you might add director first.");
				return;
			}
		}
		double budget = 0;
		if (values[5].isBlank() == false) {
			try {
				budget = Double.parseDouble(values[5]);
			} catch (Exception e) {
				System.out.println("Not a valid budget: " + values[5]);
				return;
			}
		}
		java.sql.Date movie_date;
		try {
			movie_date = dateUtil.strToDate(values[3]);

		} catch (Exception e) {
			System.out.println(utility.as_bold_color("[!!!]", "r") + "Not a valid date: " + values[3]);
			return;
		}
		String sql = "INSERT INTO movie  (title, url, genre,date_released, rating, budget, summary, studio, director_id) VALUES (?, ?, ?, ?,?,?,?,?,?)";
		PreparedStatement statement = null;
		try {
			statement = conn.prepareStatement(sql);

			statement.setString(1, values[0]); // title
			statement.setString(2, values[1]); // url
			statement.setString(3, values[2]); // genre
			statement.setDate(4, movie_date); // released date
			statement.setString(5, values[4]); // rating
			statement.setDouble(6, budget); // budget
			statement.setString(7, values[6]); // summary
			statement.setString(8, values[7]); // studio
			statement.setInt(9, director_id); // director_id

			int row_added = statement.executeUpdate();
			System.out.println(utility.as_color("[SUCCESS]", "g") + "  >>>> Insert successful. row added:" + row_added);
		} catch (SQLException sqle) {
			System.out.println("Could not insert movie into db." + sqle);
		} catch (Exception e) {
			System.out.println("Could not insert movie into db.");
			e.printStackTrace();
		} finally {
			try {
				if (statement != null)
					statement.close();
			} catch (SQLException e) {
				System.out.println("SQL error: ");
				e.printStackTrace();
			} // end finally try
		}
		System.out.println(utility.as_bold_color("[iii]", "g") + "Add new Movie finished.");
	}

	// --------OK
	public void add_user(Connection conn) {
		System.out.println(utility.as_bold_color("[iii]", "g") + " Add User ======>");
		String[] fileds = new String[] { "First Name", "Last Name", "Email", "Phone Number", "Password" };
		Utilities utility = new Utilities();
		String[] values = utility.menu_selections(fileds);
		String sql = "INSERT INTO users  (first_name, last_name, email,phone_number, password) VALUES (?, ?, ?, ?,?)";
		PreparedStatement statement = null;
		try {
			statement = conn.prepareStatement(sql);
			statement.setString(1, values[0]);
			statement.setString(2, values[1]);
			statement.setString(3, values[2]);
			statement.setString(4, values[3]);
			statement.setString(5, values[4]);
			int row_added = statement.executeUpdate();
			System.out.println(utility.as_color("[SUCCESS]", "g") + "  >>>> Insert successful. row added:" + row_added);
		} catch (SQLException sqle) {
			System.out.println("Could not insert user into db." + sqle);
		} catch (Exception e) {
			System.out.println("Could not insert user into db.");
			e.printStackTrace();
		} finally {
			try {
				if (statement != null)
					statement.close();
			} catch (SQLException e) {
				System.out.println("SQL error: ");
				e.printStackTrace();
			} // end finally try
		}
	}

	// get user by id
	public void get_user(Connection conn) {
		System.out.println(utility.as_bold_color("[iii]", "g") + " Get User info by ID ==>");
		String[] fileds = new String[] { "User ID" };
		Utilities utility = new Utilities();
		String[] values = utility.menu_selections(fileds);
		// check user
		int user_id = parseIntwithName(values[0], "User ID");
		if (user_id == -1) {
			return;
		}
		List<Object> user_info = check_user_exists(conn, user_id);
		if (user_info.isEmpty()) {
			System.out.println(utility.as_color("[!!!]", "r") + ">>> User ID not exsist.");
			return;
		} else {
			System.out.println(utility.as_color("[iii]", "g") + ">>> User Infomation:");
			for (Object s : user_info) {
				System.out.println(s);
			}
			System.out.println("\t\t >>>ID: " + user_info.get(0).toString());
			System.out.println("\t\t >>>First Name: " + user_info.get(1).toString());
			System.out.println("\t\t >>>Last Name: " + user_info.get(2).toString());
			System.out.println("\t\t >>>Email: " + user_info.get(3).toString());
			System.out.println("\t\t >>>Phone Number: " + user_info.get(4).toString());
			System.out.println("\t\t >>>Hashed Password: " + user_info.get(5).toString());
		}
		System.out.println(utility.as_color("[iii]", "g") + ">>> User Infomation finished.");
	}

	public List<Object> check_user_exists(Connection conn, int id) {
		String sql = "Select * from users where id = ?;";
		PreparedStatement statement = null;
		ResultSet res = null;
		List<Object> list = new ArrayList<Object>();
		try {
			statement = conn.prepareStatement(sql);
			statement.setInt(1, id);
			String[] arr;
			res = statement.executeQuery();
			if (res.next()) {
				list.add(res.getInt(1)); // id
				list.add(res.getString(2) == null ? "" : res.getString(2)); // first name
				list.add(res.getString(3)); // last name
				list.add(res.getString(4)); // email
				list.add(res.getString(5) == null ? "" : res.getString(5)); // phone number
				list.add(res.getString(6) == null ? "" : res.getString(6)); // password
				System.out.println(utility.as_color("[iii]", "g") + "  >>>> User " + id + " exsist: " + res.getString(2)
						+ " " + res.getString(3));
			} else {
				System.out.println(utility.as_color("[iii]", "g") + "  >>>> User " + id + " not exsist.");

			}
			return list;
		} catch (SQLException sqle) {
			System.out.println("Could not query user." + sqle);
		} catch (Exception e) {
			System.out.println("Could not query user.");
			e.printStackTrace();
		} finally {
			try {
				if (statement != null)
					statement.close();
			} catch (SQLException e) {
				System.out.println("SQL error: ");
				e.printStackTrace();
			} // end finally try
		}
		System.out.println(utility.as_bold_color("[iii]", "g") + " Check User ======> Finished");
		return list;
	}

	public List<Object> check_movie_exists(Connection conn, int id) {
		String sql = "Select * from movie where id = ?;";
		PreparedStatement statement = null;
		ResultSet res = null;
		List<Object> list = new ArrayList<Object>();
		try {
			statement = conn.prepareStatement(sql);
			statement.setInt(1, id);
			res = statement.executeQuery();
			if (res.next()) {
				list.add(res.getInt(1)); // id
				list.add(res.getString(2)); // title
				list.add(res.getString(3) == null ? "" : res.getString(3)); // url
				list.add(res.getString(4) == null ? "" : res.getString(4)); // genre
				list.add(res.getString(5) == null ? "" : res.getString(5)); // date_released
				list.add(res.getString(6) == null ? "" : res.getString(6)); // rating
				list.add(res.getDouble(7)); // budget
				list.add(res.getDouble(8)); // gross income
				list.add(res.getString(9) == null ? "" : res.getString(9)); // summary
				list.add(res.getString(10)); // studio
				list.add(res.getInt(11)); // director id

				System.out.println(
						utility.as_color("[iii]", "g") + "  >>>> Movie " + id + " exsist: " + res.getString(2));
			} else {
				System.out.println(utility.as_color("[iii]", "g") + "  >>>> Movie " + id + " not exsist.");

			}
			return list;
		} catch (SQLException sqle) {
			System.out.println("Could not query movie." + sqle);
		} catch (Exception e) {
			System.out.println("Could not query movie.");
			e.printStackTrace();
		} finally {
			try {
				if (statement != null)
					statement.close();
			} catch (SQLException e) {
				System.out.println("SQL error: ");
				e.printStackTrace();
			} // end finally try
		}
		System.out.println(utility.as_bold_color("[iii]", "g") + " Check Movie ======> Finished");
		return list;
	}

	public List<Object> check_review_exists(Connection conn, int user_id, int movie_id) {
		String sql = "Select * from review where user_id = ? and movie_id = ?;";
		PreparedStatement statement = null;
		ResultSet res = null;
		List<Object> list = new ArrayList<Object>();
		try {
			statement = conn.prepareStatement(sql);
			statement.setInt(1, user_id);
			statement.setInt(2, movie_id);
			res = statement.executeQuery();
			if (res.next()) {
				list.add(res.getInt(1)); // user_id
				list.add(res.getInt(2)); // movie_id
				list.add(res.getString(3)); // review date
				list.add(res.getDouble(4)); // rating
				list.add(res.getString(5)); // content
				System.out.println(utility.as_color("[iii]", "g") + "  >>>> Review from user " + user_id + "about movie"
						+ movie_id + " exsist: " + res.getString(3));
			} else {
				System.out.println(utility.as_color("[iii]", "g") + "  >>>> Review from user " + user_id + "about movie"
						+ movie_id + "not exsist.");

			}
			return list;
		} catch (SQLException sqle) {
			System.out.println("Could not query review." + sqle);
		} catch (Exception e) {
			System.out.println("Could not query review.");
			e.printStackTrace();
		} finally {
			try {
				if (statement != null)
					statement.close();
			} catch (SQLException e) {
				System.out.println("SQL error: ");
				e.printStackTrace();
			} // end finally try
		}
		System.out.println(utility.as_bold_color("[iii]", "g") + " Check review ======> Finished");
		return list;
	}

	// --------OK
	public void add_director(Connection conn) {
		System.out.println(utility.as_bold_color("[iii]", "g") + " Add Director ======>");
		String[] fileds = new String[] { "First Name", "Last Name", "age" };
		Utilities utility = new Utilities();
		String[] values = utility.menu_selections(fileds);
		String sql = "INSERT INTO director  (first_name, last_name,age) VALUES (?, ?, ?)";
		PreparedStatement statement = null;
		int age = 0;
		try {
			age = Integer.parseInt(values[2]);
		} catch (Exception e) {
			System.out.println("Not a valid age: " + values[2]);
			return;
		}

		try {
			statement = conn.prepareStatement(sql);
			statement.setString(1, values[0]);
			statement.setString(2, values[1]);
			statement.setInt(3, age);

			int row_added = statement.executeUpdate();
			System.out.println(utility.as_color("[SUCCESS]", "g") + "  >>>> Insert successful. row added:" + row_added);
		} catch (SQLException sqle) {
			System.out.println("Could not insert director into db." + sqle);
		} catch (Exception e) {
			System.out.println("Could not insert director into db.");
			e.printStackTrace();
		} finally {
			try {
				if (statement != null)
					statement.close();
			} catch (SQLException e) {
				System.out.println("SQL error: ");
				e.printStackTrace();
			} // end finally try
		}
	}

	// --------OK
	public void add_actor(Connection conn) {
		System.out.println(utility.as_bold_color("[iii]", "g") + " Add actor ======>");
		String[] fileds = new String[] { "First Name", "Last Name", "Gender", "age" };
		Utilities utility = new Utilities();
		String[] values = utility.menu_selections(fileds);
		String sql = "INSERT INTO actor  (first_name, last_name,gender, age) VALUES (?, ?, ?,?)";
		PreparedStatement statement = null;
		int age = parseIntwithName(values[3], "Age");
		if (age < 1) {
			System.out.println("Not a valid age, return.");
		}
		if (values[2].isEmpty() || values[2].equals("M") || values[2].equals("F")) {
		} else {
			System.out.println("Not a valid Gender:" + values[2]);
			return;
		}
		try {
			statement = conn.prepareStatement(sql);
			statement.setString(1, values[0]);
			statement.setString(2, values[1]);
			statement.setString(3, values[2]);
			statement.setInt(4, age);

			int row_added = statement.executeUpdate();
			System.out.println(utility.as_color("[SUCCESS]", "g") + "  >>>> Insert successful. row added:" + row_added);
		} catch (SQLException sqle) {
			System.out.println("Could not insert actor into db." + sqle);
		} catch (Exception e) {
			System.out.println("Could not insert actor into db.");
			e.printStackTrace();
		} finally {
			try {
				if (statement != null)
					statement.close();
			} catch (SQLException e) {
				System.out.println("SQL error: ");
				e.printStackTrace();
			} // end finally try
		}
	}

	public boolean check_director_exsist(Connection conn, int id) {

		String sql = "Select first_name, last_name, age from director where id = ?;";
		PreparedStatement statement = null;
		ResultSet res = null;
		try {
			statement = conn.prepareStatement(sql);
			statement.setInt(1, id);

			res = statement.executeQuery();
			if (res.next() == false) {
				return false;
			}
			// System.out.println(utility.as_color("[SUCCESS]", "g")+" >>>> Insert
			// successful. row added:" + row_added);
		} catch (SQLException sqle) {
			System.out.println("Could not query director." + sqle);
		} catch (Exception e) {
			System.out.println("Could not query director.");
			e.printStackTrace();
		} finally {
			try {
				if (statement != null)
					statement.close();
			} catch (SQLException e) {
				System.out.println("SQL error: ");
				e.printStackTrace();
			} // end finally try
		}
		System.out.println(utility.as_bold_color("[iii]", "g") + " Check Director ======> OK");
		return true;
	}

	public boolean check_studio_exsist(Connection conn, String name) {

		String sql = "Select name from studio where name = ?;";
		PreparedStatement statement = null;
		ResultSet res = null;
		try {
			statement = conn.prepareStatement(sql);
			statement.setString(1, name);

			res = statement.executeQuery();
			if (res.next() == false) {
				return false;
			}
			// System.out.println(utility.as_color("[SUCCESS]", "g")+" >>>> Insert
			// successful. row added:" + row_added);
		} catch (SQLException sqle) {
			System.out.println("Could not query studio." + sqle);
		} catch (Exception e) {
			System.out.println("Could not query studio.");
			e.printStackTrace();
		} finally {
			try {
				if (statement != null)
					statement.close();
			} catch (SQLException e) {
				System.out.println("SQL error: ");
				e.printStackTrace();
			} // end finally try
		}
		System.out.println(utility.as_bold_color("[iii]", "g") + " Check Studio ======> OK");
		return true;
	}

	// --------OK
	public void add_studio(Connection conn) {
		System.out.println(utility.as_bold_color("[iii]", "g") + " Add Studio ======>");
		String[] fileds = new String[] { "Studio Name", "Founded date(YYYY-MM-DD)", "budget" };
		Utilities utility = new Utilities();
		String[] values = utility.menu_selections(fileds);
		String sql = "INSERT INTO studio  (name, date_founded,budget) VALUES (?, ?, ?)";
		PreparedStatement statement = null;
		double budget = 0;
		try {
			budget = Double.parseDouble(values[2]);
		} catch (Exception e) {
			System.out.println("Not a valid budget: " + values[2]);
			return;
		}

		try {
			statement = conn.prepareStatement(sql);
			statement.setString(1, values[0]);
			statement.setDate(2, dateUtil.strToDate(values[1]));
			statement.setDouble(3, budget);

			int row_added = statement.executeUpdate();
			System.out.println(utility.as_color("[SUCCESS]", "g") + "  >>>> Insert successful. row added:" + row_added);
		} catch (SQLException sqle) {
			System.out.println("Could not insert studio into db." + sqle);
		} catch (Exception e) {
			System.out.println("Could not insert studio into db.");
			e.printStackTrace();
		} finally {
			try {
				if (statement != null)
					statement.close();
			} catch (SQLException e) {
				System.out.println("SQL error: ");
				e.printStackTrace();
			} // end finally try
		}
	}

	/*
	 * Get all users whose subscriptions are ending within a short time frame (week
	 * or month) from the current date Generate a list of users whose subscriptions
	 * are ending soon. The definition of 'soon' is specified by user input.
	 */
	public void ending_subscriptions(Connection conn) {
		System.out.println(utility.as_bold_color("[iii]", "g") + " Ending Subscriptions ==>");
		String[] fileds = new String[] { "enter window here ('d'=day, 'w'=week, or 'm'=month):" };

		Utilities utility = new Utilities();
		String[] values = utility.menu_selections(fileds);
		String window = values[0];
		while (!(window.equals("d") || window.equals("w") || window.equals("m"))) {
			System.out.println("Input " + window + " is invalid: select from {'w', 'd', 'm'} ");
			values = utility.menu_selections(fileds);
			window = values[0];
		}
		//

		PreparedStatement stmt = null;
		ResultSet res = null;
		String sql = " SELECT  " + "U.first_name || ' ' || U.last_name AS name,  "
				+ " (start_date + month_length)::date AS end_date " + "FROM  subscription S   "
				+ "JOIN plan P ON (S.plan_name = P.name)   " + "JOIN users U ON (U.id = S.user_id) "
				+ " WHERE  start_date + month_length > CURRENT_DATE "
				+ "AND  start_date + month_length - CURRENT_DATE <= ?  " + " ORDER BY start_date + month_length DESC;";
		if (window == "d") {
			window = "1 days";
			sql = sql.replace("?", "'1 days'");
		} else if (window == "w") {
			window = "7 days";
			sql = sql.replace("?", "'7 days'");
		} else {
			window = "30 days";
			sql = sql.replace("?", "'30 days'");
		}
		PreparedStatement statement = null;
		try {
			statement = conn.prepareStatement(sql);

			res = statement.executeQuery();
			System.out.println("following users have subscriptions ending within " + window);
			int count = 0;
			while (res.next()) {
				String name = res.getString(1);
				String end_date = res.getString(2);
				System.out.println(name + " : " + end_date);
				count++;
			}
			if (count == 0) {
				System.out.println("No users have subscriptions ending within " + window);
			}
		} catch (SQLException e) {
			System.out.println("Query Ending Subscription failed,SQL error: ");
			e.printStackTrace();
		} catch (Exception e) {
			System.out.println("Query Ending Subscription failed, class error: ");
			e.printStackTrace();
		} finally {
			try {
				if (stmt != null)
					stmt.close();
				if (res != null)
					res.close();
			} catch (SQLException e) {
				System.out.println("Query Ending Subscription failed,SQL error: ");
				e.printStackTrace();
			} // end finally try
		}
		System.out.println(utility.as_bold_color("[iii]", "g") + " Query Ending Subscription finished.");
	}

	/*
	 * tell how many users are on currently each of the subscription plans Generate
	 * counts of how many users are currently subscribed for each plan.
	 */
	public void generate_subscription_counts(Connection conn) {
		System.out.println(utility.as_bold_color("[iii]", "g") + " Count Each Subscription ==>");
		PreparedStatement stmt = null;
		ResultSet res = null;
		String sql = "SELECT name, COUNT(*) count " + "FROM subscription S JOIN plan P ON (S.plan_name = P.name)  "
				+ " WHERE start_date < CURRENT_DATE " + "AND start_date + month_length > CURRENT_DATE "
				+ "GROUP BY name;";
		try {
			stmt = conn.prepareStatement(sql);
			res = stmt.executeQuery();
			while (res.next()) {
				System.out.println(res.getString(1) + " : " + res.getInt(2));
			}
		} catch (SQLException e) {
			System.out.println("Query Subscription counts failed,SQL error: ");
			e.printStackTrace();
		} catch (Exception e) {
			System.out.println("Query Subscription counts failed, class error: ");
			e.printStackTrace();
		} finally {
			try {
				if (stmt != null)
					stmt.close();
				if (res != null)
					res.close();
			} catch (SQLException e) {
				System.out.println("Query Subscription counts failed,SQL error: ");
				e.printStackTrace();
			} // end finally try
		}
		System.out.println(utility.as_bold_color("[iii]", "g") + " Query Subscription counts finished.");

	}

	// Generate a list of all students and their advisors.
	public void get_movies(Connection conn) {
		System.out.println(utility.as_bold_color("[iii]", "g") + " Query Movies ==>");
		PreparedStatement stmt = null;
		ResultSet res = null;
		String sql = "SELECT title from movie order by title;";
		try {
			stmt = conn.prepareStatement(sql);
			res = stmt.executeQuery();
			int i = 1;

			while (res.next()) {
				System.out.println(i + ": " + res.getString(1));
				// todo: limit the print rows number
				i++;
			}
		} catch (SQLException e) {
			System.out.println("Query Active Movie failed,SQL error: ");
			e.printStackTrace();
		} catch (Exception e) {
			System.out.println("Query Active Movie failed, class error: ");
			e.printStackTrace();
		} finally {
			try {
				if (stmt != null)
					stmt.close();
				if (res != null)
					res.close();
			} catch (SQLException e) {
				System.out.println("Query Active Movie failed,SQL error: ");
				e.printStackTrace();
			} // end finally try
		}
		System.out.println(utility.as_bold_color("[iii]", "g") + " Query Active Movie finished.");
	}

	/*
	 * Get the number of movies that each actor, director pair have collaborated on,
	 * in descending order, with option to limit result count.
	 */
	public void get_actor_director_pairs(Connection conn) {
		System.out.println(utility.as_bold_color("[iii]", "g") + " Count Actor Director Pairs ==>");
		String[] fileds = new String[] { "Result Limit(leave empty if no)" };
		Utilities utility = new Utilities();
		String[] values = utility.menu_selections(fileds);
		int limit = parseIntwithName(values[0], "Result Limit");

		PreparedStatement stmt = null;
		ResultSet res = null;
		String sql = "SELECT actor_id, director_id, COUNT(*) num_movies "
				+ "FROM  act A JOIN movie M ON (A.movie_id = M.id)  " + "GROUP BY  actor_id, director_id ORDER BY     "
				+ " COUNT(*) DESC, actor_id ASC, director_id ASC";
		if (limit != -1) {
			sql += "   LIMIT ?;";
		}
		try {
			stmt = conn.prepareStatement(sql);

			if (limit != -1) {

				stmt.setInt(1, limit);
			}
			res = stmt.executeQuery();
			System.out.println("Actor ID\t Director ID\t Movies");
			while (res.next()) {
				System.out.println(res.getInt(1) + " \t\t " + res.getInt(2) + " \t\t " + res.getInt(3));
			}
		} catch (SQLException e) {
			System.out.println("Query Actor Director Pairs failed,SQL error: ");
			e.printStackTrace();
		} catch (Exception e) {
			System.out.println("Query Actor Director Pairs failed, class error: ");
			e.printStackTrace();
		} finally {
			try {
				if (stmt != null)
					stmt.close();
				if (res != null)
					res.close();
			} catch (SQLException e) {
				System.out.println("Query Actor Director Pairs failed,SQL error: ");
				e.printStackTrace();
			} // end finally try
		}
		System.out.println(utility.as_bold_color("[iii]", "g") + " Query Actor Director Pairs finished.");

	}

	/*
	 * Which users watch the most movies (of a certain genre) in a given time frame?
	 * Get the most binge-heavy movie watchers in a certain time frame, optionally
	 * filtering by genre and limiting number of query results returned.
	 */
	public void get_busiest_users(Connection conn) {
		String f_name = "Get busiest users.";
		System.out.println(utility.as_bold_color("[iii]", "g") + f_name + "==>");

		String[] fileds = new String[] { "Enter genre (press <RETURN> to leave empty):",
				"Enter # of results to return (press <RETURN> to leave empty)",
				"specify start date(YYYY-MM-DD) (press <RETURN> to leave empty)",
				"specify end date (YYYY-MM-DD)(press <RETURN> to leave empty)" };
		Utilities utility = new Utilities();
		String[] values = utility.menu_selections(fileds);
		String genre = values[0];
		int limit = parseIntwithName(values[1], "Result Limit");
		String start_date = values[2];
		String end_date = values[3];
		String sql = 
				  "                SELECT user_id, count(*) num_watches "
				+ "                FROM history H JOIN movie M ON (H.movie_id = M.id) "
				+ "                where date_released > DATE(?) AND date_released < DATE(?) ### "
				+ "                GROUP BY user_id ORDER BY COUNT(*) DESC ";
		
		// if
		if (!genre.isBlank()) {
			sql = sql.replace("###", "AND genre=?");
		} else {
			sql = sql.replace("###", "");
		}
		if (limit != -1) {
			sql += "   LIMIT ? ";
		}
		PreparedStatement stmt = null;
		ResultSet res = null;
		try {
			stmt = conn.prepareStatement(sql);
			if (start_date.isBlank()) {
				start_date = "0001-1-1";
			}
			if (end_date.isBlank()) {
				end_date = "9999-1-1";
			}
			stmt.setString(1, start_date);
			stmt.setString(2, end_date);
			if (!genre.isBlank()) {
				stmt.setString(3, genre);
			}
			if (limit != -1) {
				if (!genre.isBlank()) {
					stmt.setInt(4, limit);
				} else {
					stmt.setInt(3, limit);
				}
			}
			res = stmt.executeQuery();
			System.out.println("History Results:");
			while (res.next()) {
				System.out.println("User "+ res.getInt(1) + " has watched " +  res.getInt(2)+ " movies." );
			}
		} catch (SQLException e) {
			System.out.println("Query " + f_name + " failed,SQL error: ");
			e.printStackTrace();
		} catch (Exception e) {
			System.out.println("Query " + f_name + " failed, class error: ");
			e.printStackTrace();
		} finally {
			try {
				if (stmt != null)
					stmt.close();
				if (res != null)
					res.close();
			} catch (SQLException e) {
				System.out.println("Query " + f_name + " failed,SQL error: ");
				e.printStackTrace();
			} // end finally try
		}
		System.out.println(utility.as_bold_color("[iii]", "g") + " Query " + f_name + " finished.");
	}

	public void get_highest_grossing_studios(Connection conn) {
		System.out.println(utility.as_bold_color("[iii]", "g") + " Get Highest Grossing Studios ==>");

		Utilities utility = new Utilities();
		PreparedStatement stmt = null;
		ResultSet res = null;
		String sql = "SELECT studio, SUM(gross_income) revenue " + "            FROM movie " + "            GROUP BY "
				+ "                studio " + "            ORDER BY revenue;";

		try {
			stmt = conn.prepareStatement(sql);
			res = stmt.executeQuery();
			System.out.println("Studio\t\t Gross Income");
			while (res.next()) {
				String num = utility.big(res.getDouble(2));
				System.out.println(res.getString(1) + " \t\t " + num);
			}
		} catch (SQLException e) {
			System.out.println("Query Highest Grossing Studios failed,SQL error: ");
			e.printStackTrace();
		} catch (Exception e) {
			System.out.println("Query Highest Grossing Studios  failed, class error: ");
			e.printStackTrace();
		} finally {
			try {
				if (stmt != null)
					stmt.close();
				if (res != null)
					res.close();
			} catch (SQLException e) {
				System.out.println("Query Highest Grossing Studios  failed,SQL error: ");
				e.printStackTrace();
			} // end finally try
		}
		System.out.println(utility.as_bold_color("[iii]", "g") + " Query Highest Grossing Studios  finished.");

	}

	/*
	 * Which directors have the highest associated movie ratings? + Calculate a
	 * director's rating as the average rating across all the movies he directed
	 */
	public void get_highest_rated_directors(Connection conn) {
		String f_name = "Get Highest Rated Directors";
		System.out.println(utility.as_bold_color("[iii]", "g") + f_name + "==>");

		String[] fileds = new String[] { "Enter genre (press <RETURN> to leave empty):",
				"Enter # of results to return (press <RETURN> to leave empty)",
				"specify start date(YYYY-MM-DD) (press <RETURN> to leave empty)",
				"specify end date (YYYY-MM-DD)(press <RETURN> to leave empty)" };
		Utilities utility = new Utilities();
		String[] values = utility.menu_selections(fileds);
		String genre = values[0];
		int limit = parseIntwithName(values[1], "Result Limit");
		String start_date = values[2];
		String end_date = values[3];

		String sql = "WITH average_ratings AS " + "                    (SELECT movie_id, AVG(rating) avg_r "
				+ "                     FROM review " + "                     GROUP BY movie_id "
				+ "                    ) " + "                SELECT "
				+ "                    first_name || ' ' || last_name AS name, "
				+ "                    AVG(AR.avg_r) avg_rating " + "                FROM "
				+ "                    director D " + "                    JOIN movie M ON (D.id = M.director_id) "
				+ "                    JOIN average_ratings AR ON (M.id = AR.movie_id) "
				+ "                where M.date_released > DATE(?) AND M.date_released < DATE(?) ### "
				+ "                GROUP BY name " + "                ORDER BY avg_rating DESC ";
		// if
		if (!genre.isBlank()) {
			sql = sql.replace("###", "AND genre=?");
		} else {
			sql = sql.replace("###", "");
		}
		if (limit != -1) {
			sql += "   LIMIT ? ";
		}
		PreparedStatement stmt = null;
		ResultSet res = null;
		try {
			stmt = conn.prepareStatement(sql);
			if (start_date.isBlank()) {
				start_date = "0001-1-1";
			}
			if (end_date.isBlank()) {
				end_date = "9999-1-1";
			}
			stmt.setString(1, start_date);
			stmt.setString(2, end_date);
			if (!genre.isBlank()) {
				stmt.setString(3, genre);
			}
			if (limit != -1) {
				if (!genre.isBlank()) {
					stmt.setInt(4, limit);
				} else {
					stmt.setInt(3, limit);
				}
			}
			res = stmt.executeQuery();
			System.out.println("Name\t\t Average Rating");
			while (res.next()) {
				System.out.println(res.getString(1) + " \t\t " + utility.big(res.getDouble(2)));
			}
		} catch (SQLException e) {
			System.out.println("Query " + f_name + " failed,SQL error: ");
			e.printStackTrace();
		} catch (Exception e) {
			System.out.println("Query " + f_name + " failed, class error: ");
			e.printStackTrace();
		} finally {
			try {
				if (stmt != null)
					stmt.close();
				if (res != null)
					res.close();
			} catch (SQLException e) {
				System.out.println("Query " + f_name + " failed,SQL error: ");
				e.printStackTrace();
			} // end finally try
		}
		System.out.println(utility.as_bold_color("[iii]", "g") + " Query " + f_name + " finished.");

	}

	/*
	 * Which actors have the highest associated movie ratings? Calculate an actor's
	 * rating as the average rating across all the movies he starred in
	 */
	public void get_highest_rated_actors(Connection conn) {
		System.out.println(utility.as_bold_color("[iii]", "g") + " Get Highest Rated Actors ==>");

		String[] fileds = new String[] { "Enter genre (press <RETURN> to leave empty):",
				"Enter # of results to return (press <RETURN> to leave empty)",
				"specify start date(YYYY-MM-DD) (press <RETURN> to leave empty)",
				"specify end date (YYYY-MM-DD)(press <RETURN> to leave empty)" };
		Utilities utility = new Utilities();
		String[] values = utility.menu_selections(fileds);
		String genre = values[0];
		int limit = parseIntwithName(values[1], "Result Limit");
		String start_date = values[2];
		String end_date = values[3];

		String sql = "WITH average_ratings AS " + "                    (SELECT movie_id, AVG(rating) avg_r "
				+ "                     FROM review " + "                     GROUP BY movie_id "
				+ "                    ) " + "                SELECT "
				+ "                    first_name || ' ' || last_name AS name, "
				+ "                    AVG(AR.avg_r) avg_rating " + "                FROM "
				+ "                    actor A " + "                    JOIN act ON (act.actor_id = A.id) "
				+ "                    JOIN average_ratings AR ON (act.movie_id = AR.movie_id) "
				+ "                    JOIN movie M ON (M.id = AR.movie_id) "
				+ "                where M.date_released > DATE(?) AND M.date_released < DATE(?) ### "
				+ "                GROUP BY name " + "                ORDER BY avg_rating DESC ";
		// if
		if (!genre.isBlank()) {
			sql = sql.replace("###", "AND genre=?");
		} else {
			sql = sql.replace("###", "");
		}
		if (limit != -1) {
			sql += "   LIMIT ? ";
		}
		PreparedStatement stmt = null;
		ResultSet res = null;
		try {
			stmt = conn.prepareStatement(sql);
			if (start_date.isBlank()) {
				start_date = "0001-1-1";
			}
			if (end_date.isBlank()) {
				end_date = "9999-1-1";
			}
			stmt.setString(1, start_date);
			stmt.setString(2, end_date);
			if (!genre.isBlank()) {
				stmt.setString(3, genre);
			}
			if (limit != -1) {
				if (!genre.isBlank()) {
					stmt.setInt(4, limit);
				} else {
					stmt.setInt(3, limit);
				}
			}
			res = stmt.executeQuery();
			System.out.println("Name\t\t Average Rating");
			while (res.next()) {
				System.out.println(res.getString(1) + " \t\t " + utility.big(res.getDouble(2)));
			}
		} catch (SQLException e) {
			System.out.println("Query Highest Rated Actors failed,SQL error: ");
			e.printStackTrace();
		} catch (Exception e) {
			System.out.println("Query Highest Rated Actors failed, class error: ");
			e.printStackTrace();
		} finally {
			try {
				if (stmt != null)
					stmt.close();
				if (res != null)
					res.close();
			} catch (SQLException e) {
				System.out.println("Query Highest Rated Actors failed,SQL error: ");
				e.printStackTrace();
			} // end finally try
		}
		System.out.println(utility.as_bold_color("[iii]", "g") + " Query Highest Rated Actors finished.");

	}

	/*
	 * Get highest-rated movie(s) for a given time frame, genre Get the
	 * highest-rated movies in a certain time frame, optionally filtering by genre
	 * and limiting number of query results returned.
	 */
	public void get_highest_rated_movies(Connection conn) {
		String f_name = "Get Highest Rated Movies";
		System.out.println(utility.as_bold_color("[iii]", "g") + f_name + "==>");

		String[] fileds = new String[] { "Enter genre (press <RETURN> to leave empty):",
				"Enter # of results to return (press <RETURN> to leave empty)",
				"specify start date(YYYY-MM-DD) (press <RETURN> to leave empty)",
				"specify end date (YYYY-MM-DD)(press <RETURN> to leave empty)" };
		Utilities utility = new Utilities();
		String[] values = utility.menu_selections(fileds);
		String genre = values[0];
		int limit = parseIntwithName(values[1], "Result Limit");
		String start_date = values[2];
		String end_date = values[3];

		String sql = "WITH average_ratings AS " 
				+ "                    (SELECT movie_id, AVG(rating) avg_r "
				+ "                     FROM review " 
				+ "                     GROUP BY movie_id "
				+ "                    ) " 
				+ "                SELECT title, AR.avg_r AS average_rating "
				+ "                FROM movie JOIN average_ratings AR "
				+ "                    ON movie.id = AR.movie_id " 
				+ "                where date_released > DATE(?) AND date_released < DATE(?) ### "
				+ "                ORDER BY average_rating DESC ";
		// if
		if (!genre.isBlank()) {
			sql = sql.replace("###", "AND genre=?");
		} else {
			sql = sql.replace("###", "");
		}
		if (limit != -1) {
			sql += "   LIMIT ? ";
		}
		PreparedStatement stmt = null;
		ResultSet res = null;
		try {
			stmt = conn.prepareStatement(sql);
			if (start_date.isBlank()) {
				start_date = "0001-1-1";
			}
			if (end_date.isBlank()) {
				end_date = "9999-1-1";
			}
			stmt.setString(1, start_date);
			stmt.setString(2, end_date);
			if (!genre.isBlank()) {
				stmt.setString(3, genre);
			}
			if (limit != -1) {
				if (!genre.isBlank()) {
					stmt.setInt(4, limit);
				} else {
					stmt.setInt(3, limit);
				}
			}
			res = stmt.executeQuery();
			System.out.println("Name\t\t Average Rating");
			while (res.next()) {
				System.out.println(res.getString(1) + " \t\t " + utility.big(res.getDouble(2)));
			}
		} catch (SQLException e) {
			System.out.println("Query " + f_name + " failed,SQL error: ");
			e.printStackTrace();
		} catch (Exception e) {
			System.out.println("Query " + f_name + " failed, class error: ");
			e.printStackTrace();
		} finally {
			try {
				if (stmt != null)
					stmt.close();
				if (res != null)
					res.close();
			} catch (SQLException e) {
				System.out.println("Query " + f_name + " failed,SQL error: ");
				e.printStackTrace();
			} // end finally try
		}
		System.out.println(utility.as_bold_color("[iii]", "g") + " Query " + f_name + " finished.");
	}

	/*
	 * Which movies are the most popular in a given time frame? Get the most popular
	 * movies in a certain time frame, optionally filtering by genre and limiting
	 * number of query results returned.
	 */
	public void get_popular_movies(Connection conn) {
		
		String f_name = "Get Popular Movies";
		System.out.println(utility.as_bold_color("[iii]", "g") + f_name + "==>");

		String[] fileds = new String[] { "Enter genre (press <RETURN> to leave empty):",
				"Enter # of results to return (press <RETURN> to leave empty)",
				"specify start date(YYYY-MM-DD) (press <RETURN> to leave empty)",
				"specify end date (YYYY-MM-DD)(press <RETURN> to leave empty)" };
		Utilities utility = new Utilities();
		String[] values = utility.menu_selections(fileds);
		String genre = values[0];
		int limit = parseIntwithName(values[1], "Result Limit");
		String start_date = values[2];
		String end_date = values[3];

		String sql =
				  "                SELECT M.title, COUNT(*) num_watches "
				+ "                FROM history H JOIN movie M "
				+ "                    ON  (M.id = H.movie_id) " 
				+ "                where watch_date > DATE(?) AND watch_date < DATE(?) ### "
				+ "                GROUP BY M.id"
				+ "                ORDER BY COUNT(*) DESC ";
		// if
		if (!genre.isBlank()) {
			sql = sql.replace("###", "AND genre=?");
		} else {
			sql = sql.replace("###", "");
		}
		if (limit != -1) {
			sql += "   LIMIT ? ";
		}
		PreparedStatement stmt = null;
		ResultSet res = null;
		try {
			stmt = conn.prepareStatement(sql);
			if (start_date.isBlank()) {
				start_date = "0001-1-1";
			}
			if (end_date.isBlank()) {
				end_date = "9999-1-1";
			}
			stmt.setString(1, start_date);
			stmt.setString(2, end_date);
			if (!genre.isBlank()) {
				stmt.setString(3, genre);
			}
			if (limit != -1) {
				if (!genre.isBlank()) {
					stmt.setInt(4, limit);
				} else {
					stmt.setInt(3, limit);
				}
			}
			res = stmt.executeQuery();
			System.out.println("Name\t\t Number of Watches");
			while (res.next()) {
				System.out.println(res.getString(1) + " \t\t " + utility.big(res.getDouble(2)));
			}
		} catch (SQLException e) {
			System.out.println("Query " + f_name + " failed,SQL error: ");
			e.printStackTrace();
		} catch (Exception e) {
			System.out.println("Query " + f_name + " failed, class error: ");
			e.printStackTrace();
		} finally {
			try {
				if (stmt != null)
					stmt.close();
				if (res != null)
					res.close();
			} catch (SQLException e) {
				System.out.println("Query " + f_name + " failed,SQL error: ");
				e.printStackTrace();
			} // end finally try
		}
		System.out.println(utility.as_bold_color("[iii]", "g") + " Query " + f_name + " finished.");

	}

	/*
	 * For a given user id, get the start and end dates of his current subscription.
	 */
	public void get_user_current_subscription_window(Connection conn) {
		String f_name = "Get User's Subscription";
		System.out.println(utility.as_bold_color("[iii]", "g") + f_name + "==>");

		String[] fileds = new String[] { "User ID" };
		Utilities utility = new Utilities();
		String[] values = utility.menu_selections(fileds);
		int user_id = parseIntwithName(values[0], "User ID");
		if (user_id == -1) {
			return;
		}
		String sql ="  SELECT"
				+ "                start_date,"
				+ "                EXTRACT(MONTH FROM month_length) AS month, "
				+ "                EXTRACT(YEAR FROM month_length) AS year,"
				+ "                (start_date + month_length)::date AS end_date,"
				+ "                name"
				+ "            FROM"
				+ "                subscription S JOIN plan P ON (S.plan_name = P.name)"
				+ "            WHERE"
				+ "                user_id = ? AND"
				+ "                start_date <= CURRENT_DATE AND"
				+ "                start_date + month_length >= CURRENT_DATE";
		 
		PreparedStatement stmt = null;
		ResultSet res = null;
		try {
			stmt = conn.prepareStatement(sql);
			 
			stmt.setInt(1, user_id);
			res = stmt.executeQuery();
			System.out.println("Start Date\t Month \t Year \t End Date \t Name");
			while (res.next()) {
				System.out.println(res.getString(1)+"\t"+res.getString(2)+"\t"+res.getString(3)+"\t"+res.getString(4)+"\t"+res.getString(5));
			}
		} catch (SQLException e) {
			System.out.println("Query " + f_name + " failed,SQL error: ");
			e.printStackTrace();
		} catch (Exception e) {
			System.out.println("Query " + f_name + " failed, class error: ");
			e.printStackTrace();
		} finally {
			try {
				if (stmt != null)
					stmt.close();
				if (res != null)
					res.close();
			} catch (SQLException e) {
				System.out.println("Query " + f_name + " failed,SQL error: ");
				e.printStackTrace();
			} // end finally try
		}
		System.out.println(utility.as_bold_color("[iii]", "g") + " Query " + f_name + " finished.");
		
	}

	/*
	 * Get, for each user, which genre(s) that user is most likely to watch.
	 */
	public void get_user_genres(Connection conn) {
		String f_name = "Get User Genres";
		System.out.println(utility.as_bold_color("[iii]", "g") + f_name + "==>");
		String sql =" WITH "
				+ "                user_genre_counts as "
				+ "                (SELECT user_id, genre, COUNT(*) c "
				+ "                 FROM history H "
				+ "                    JOIN movie M ON H.movie_id = M.id "
				+ "                 GROUP BY "
				+ "                    user_id, genre "
				+ "                ), "
				+ "                user_genre_max as "
				+ "                (SELECT user_id, MAX(c) mc "
				+ "                 FROM user_genre_counts "
				+ "                 GROUP BY user_id "
				+ "                ), "
				+ "                user_genre_res AS "
				+ "                (SELECT user_id, genre, c "
				+ "                 FROM user_genre_counts NATURAL JOIN user_genre_max "
				+ "                 WHERE c = mc\r\n"
				+ "                 ORDER BY user_id)\r\n"
				+ "            SELECT user_id, string_agg(genre, ', '), MIN(c) "
				+ "            FROM user_genre_res "
				+ "            GROUP BY user_id;";
		 
		PreparedStatement stmt = null;
		ResultSet res = null;
		try {
			stmt = conn.prepareStatement(sql);
			 
			res = stmt.executeQuery();
			System.out.println("User ID\t Genre \t Count ");
			while (res.next()) {
				System.out.println(res.getString(1)+"\t"+res.getString(2)+"\t"+res.getString(3));
			}
		} catch (SQLException e) {
			System.out.println("Query " + f_name + " failed,SQL error: ");
			e.printStackTrace();
		} catch (Exception e) {
			System.out.println("Query " + f_name + " failed, class error: ");
			e.printStackTrace();
		} finally {
			try {
				if (stmt != null)
					stmt.close();
				if (res != null)
					res.close();
			} catch (SQLException e) {
				System.out.println("Query " + f_name + " failed,SQL error: ");
				e.printStackTrace();
			} // end finally try
		}
		System.out.println(utility.as_bold_color("[iii]", "g") + " Query " + f_name + " finished.");
		
	}

	/*
	 * Leave a review for a particular user on a particular movie. If the user has
	 * already reviewed this movie, prompt the user to confirm that he wants to
	 * overwrite his previous review.
	 */
	public void leave_a_review(Connection conn) {
		System.out.println(utility.as_bold_color("[iii]", "g") + " Leave a Review ======>");
		String[] fileds = new String[] { "User ID", "Movie ID", "Review Date(YYYY-MM-DD)", "Rating(1-100)", "Content" };
		Utilities utility = new Utilities();
		String[] values = utility.menu_selections(fileds);

		// check user
		int user_id = parseIntwithName(values[0], "User ID");
		if (user_id == -1) {
			return;
		}
		List<Object> user_info = check_user_exists(conn, user_id);
		if (user_info.isEmpty()) {
			System.out.println(utility.as_color("[!!!]", "r") + ">>> User ID not exsist.");
			return;
		}

		// check movie
		int movie_id = parseIntwithName(values[1], "Movie ID");
		if (movie_id == -1) {
			return;
		}
		List<Object> movie_info = check_movie_exists(conn, movie_id);
		if (movie_info.isEmpty()) {
			System.out.println(utility.as_color("[!!!]", "r") + ">>> Movie ID not exsist.");
			return;
		}

		// get date
		java.sql.Date review_date;
		try {
			review_date = dateUtil.strToDate(values[2]);
		} catch (Exception e) {
			System.out.println(utility.as_bold_color("[!!!]", "r") + "Not a valid date: " + values[3]);
			return;
		}

		// parse Rating
		int rating = parseIntwithName(values[3], "Rating");
		if (rating <= 0) {
			return;
		}
		// check exsist
		List<Object> review_info = check_review_exists(conn, user_id, movie_id);
		if (!review_info.isEmpty()) {
			System.out.println(
					utility.as_color("[!!!]", "r") + ">>> Do you want to overwrite the previous review? (Y/N)");
			Scanner scan = new Scanner(System.in);
			String get = scan.nextLine();

			if (get.equals("Y")) {
				System.out.println(utility.as_color("[!!!]", "r") + ">>>Overwrite...");
				// here call overWrite

			} else {
				System.out.println(utility.as_color("[!!!]", "r") + ">>>Not Overwrite, Quit...");
				return;
			}

		}

		String insert_sql = "INSERT INTO review  (user_id,movie_id, review_date, rating,content) VALUES (?, ?, ?,?,?);";
		String update_sql = "UPDATE review SET review_date=?, rating=?, content=? WHERE user_id = ? AND movie_id = ? ;";
		PreparedStatement statement = null;
		try {
			// insert
			if (review_info.isEmpty()) {
				statement = conn.prepareStatement(insert_sql);
				statement.setInt(1, user_id);
				statement.setInt(2, movie_id);
				statement.setDate(3, review_date);
				statement.setInt(4, rating);
				statement.setString(5, values[4]);
				int row_added = statement.executeUpdate();
				System.out.println(
						utility.as_color("[SUCCESS]", "g") + "  >>>> Insert review successful. row added:" + row_added);
			} else { // update
				statement = conn.prepareStatement(update_sql);

				statement.setDate(1, review_date);
				statement.setInt(2, rating);
				statement.setString(3, values[4]);
				statement.setInt(4, user_id);
				statement.setInt(5, movie_id);
				int row_added = statement.executeUpdate();
				System.out.println(
						utility.as_color("[SUCCESS]", "g") + "  >>>> Update review successful. row added:" + row_added);
			}

		} catch (SQLException sqle) {
			System.out.println("Could not insert review into db." + sqle);
		} catch (Exception e) {
			System.out.println("Could not insert review into db.");
			e.printStackTrace();
		} finally {
			try {
				if (statement != null)
					statement.close();
			} catch (SQLException e) {
				System.out.println("SQL error: ");
				e.printStackTrace();
			} // end finally try
		}
	}


	public void remove_user(Connection conn) {
		String f_name = "Remove User";
		System.out.println(utility.as_bold_color("[iii]", "g") + f_name + "==>");

		String[] fileds = new String[] { "User ID" };
		Utilities utility = new Utilities();
		String[] values = utility.menu_selections(fileds);
		int user_id = parseIntwithName(values[0], "User ID");
		if (user_id == -1) {
			return;
		}
		String sql ="DELETE FROM users "
				+ "WHERE id = ?";
		
		PreparedStatement stmt = null;
		int res = 0;
		try {
			stmt = conn.prepareStatement(sql);
			 
			stmt.setInt(1, user_id);
			res = stmt.executeUpdate();
			System.out.println("User deleted, row deleted:"+res);
		} catch (SQLException e) {
			System.out.println("Query " + f_name + " failed,SQL error: ");
			e.printStackTrace();
		} catch (Exception e) {
			System.out.println("Query " + f_name + " failed, class error: ");
			e.printStackTrace();
		} finally {
			try {
				if (stmt != null)
					stmt.close();
			} catch (SQLException e) {
				System.out.println("Query " + f_name + " failed,SQL error: ");
				e.printStackTrace();
			} // end finally try
		}
		System.out.println(utility.as_bold_color("[iii]", "g") + f_name + " finished.");
		
	}

	public int parseIntwithName(String str, String name) {
		int re = 0;
		try {
			re = Integer.parseInt(str);
		} catch (Exception e) {
			System.out.println("Not a valid " + name + ": " + str);
			return -1;
		}
		return re;
	}
}
