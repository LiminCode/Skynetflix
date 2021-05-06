import java.sql.*;
import java.util.Calendar;
import java.util.Date;

public class Task {
	  Utilities utility = new Utilities();  // for print in color
	  DateUtil dateUtil = new DateUtil();
	  /*
	   * Add new actors to an already existing movie
	   * */
	  public void add_actors_to_movie(Connection conn){}

	  /*
	   * add_movie
	   * Add a new movie, requiring that actors be specified in addition to fields in 'movies' table
	  */
	  public void add_movie(Connection conn){
		  System.out.println(utility.as_bold_color("[iii]","g")+" Add New Movie ==>");
		  PreparedStatement stmt=null;
		  ResultSet res=null;
		  String sql = "SELECT title from movie where available=true order by title;";
		try {
			stmt = conn.prepareStatement(sql);
			res = stmt.executeQuery();
			int i = 1;
			
		    while (res.next()){
			      System.out.println(i+": "+res.getString(1));
			      // todo: limit the print rows number
			      i++;
			}
		}catch(SQLException e){
			System.out.println("Query Active Movie failed,SQL error: ");
			e.printStackTrace();
 		}catch(Exception e){
			System.out.println("Query Active Movie failed, class error: ");
			e.printStackTrace();
		}finally{
			 try{
		         if(stmt!=null)
		            stmt.close();
		         if(res!=null)
			        res.close();
		      }catch(SQLException e){
		    	 System.out.println("Query Active Movie failed,SQL error: ");
		    	 e.printStackTrace();
		      }//end finally try
		}
		System.out.println(utility.as_bold_color("[iii]","g")+" Query Active Movie finished.");
	  }
	  
	  //--------OK
	  public void add_user(Connection conn){
		  System.out.println(utility.as_bold_color("[iii]","g")+" Add User ======>");
		  String[] fileds = new String[]{"First Name","Last Name","Email","Phone Number", "Password"};
		  Utilities utility = new Utilities();
		  String[] values = utility.menu_selections(fileds);
		  String sql = "INSERT INTO users  (first_name, last_name, email,phone_number, password) VALUES (?, ?, ?, ?,?)";
			PreparedStatement statement=null;
		    try {
		      statement  = conn.prepareStatement(sql);
		      statement.setString(1, values[0]);
		      statement.setString(2, values[1]);
		      statement.setString(3, values[2]);
		      statement.setString(4, values[3]);
		      statement.setString(5, values[4]);
		      int row_added = statement.executeUpdate();
		      System.out.println(utility.as_color("[SUCCESS]", "g")+"  >>>> Insert successful. row added:" + row_added);
		    }catch (SQLException sqle){
		      System.out.println("Could not insert user into db." + sqle);
		    }catch (Exception  e){
			      System.out.println("Could not insert user into db.");
			      e.printStackTrace();
			}finally{
				try{
			         if(statement!=null)
			        	 statement.close();
			      }catch(SQLException e){
			    	 System.out.println("SQL error: ");
			    	 e.printStackTrace();
			      }//end finally try
			}
	  }
	  //--------OK
	  public void add_director(Connection conn){
		  System.out.println(utility.as_bold_color("[iii]","g")+" Add Director ======>");
		  String[] fileds = new String[]{"First Name","Last Name","age"};
		  Utilities utility = new Utilities();
		  String[] values = utility.menu_selections(fileds);
		  String sql = "INSERT INTO director  (first_name, last_name,age) VALUES (?, ?, ?)";
			PreparedStatement statement=null;
			int age=0;
			try {
				age =Integer.parseInt(values[2]);
			}catch (Exception  e){
			      System.out.println("Not a valid age: "+values[2]);
			      return;
			}
		    
		    try {
		      statement  = conn.prepareStatement(sql);
		      statement.setString(1, values[0]);
		      statement.setString(2, values[1]);
		      statement.setInt(3, age);
		      
		      int row_added = statement.executeUpdate();
		      System.out.println(utility.as_color("[SUCCESS]", "g")+"  >>>> Insert successful. row added:" + row_added);
		    }catch (SQLException sqle){
		      System.out.println("Could not insert director into db." + sqle);
		    }catch (Exception  e){
			      System.out.println("Could not insert director into db.");
			      e.printStackTrace();
			}finally{
				try{
			         if(statement!=null)
			        	 statement.close();
			      }catch(SQLException e){
			    	 System.out.println("SQL error: ");
			    	 e.printStackTrace();
			      }//end finally try
			}
	  }
	  //--------OK
	  public void add_studio(Connection conn){
		  System.out.println(utility.as_bold_color("[iii]","g")+" Add Studio ======>");
		  String[] fileds = new String[]{"Studio Name","Founded date(YYYY-MM-DD)","budget"};
		  Utilities utility = new Utilities();
		  String[] values = utility.menu_selections(fileds);
		  String sql = "INSERT INTO studio  (name, date_founded,budget) VALUES (?, ?, ?)";
			PreparedStatement statement=null;
			double budget=0;
			try {
				budget =Double.parseDouble(values[2]);
			}catch (Exception  e){
			      System.out.println("Not a valid budget: "+values[2]);
			      return;
			}
		    
		    try {
		      statement  = conn.prepareStatement(sql);
		      statement.setString(1, values[0]);
		      statement.setDate(2, dateUtil.strToDate(values[1]));
		      statement.setDouble(3, budget);
		      
		      int row_added = statement.executeUpdate();
		      System.out.println(utility.as_color("[SUCCESS]", "g")+"  >>>> Insert successful. row added:" + row_added);
		    }catch (SQLException sqle){
		      System.out.println("Could not insert studio into db." + sqle);
		    }catch (Exception  e){
			      System.out.println("Could not insert studio into db.");
			      e.printStackTrace();
			}finally{
				try{
			         if(statement!=null)
			        	 statement.close();
			      }catch(SQLException e){
			    	 System.out.println("SQL error: ");
			    	 e.printStackTrace();
			      }//end finally try
			}
	  }
	  /*
	   * "Set a movie's active status to false, meaning it is not actively streaming.
    Keep historical records of the movie being watched.
	   * */
	  public void delist_movie(Connection conn){}
	  
	  /*
	   * Get all users whose subscriptions are ending within a short time frame (week or month) from the current date
	   * Generate a list of users whose subscriptions are ending soon.
    The definition of 'soon' is specified by user input.
	   * */
	  public void ending_subscriptions(Connection conn){}
	  
	  /*
	   *  tell how many users are on currently each of the subscription plans
	   *  Generate counts of how many users are currently subscribed for each plan.
	   * */
	  public void generate_subscription_counts(Connection conn){}
	  // Generate a list of all students and their advisors.
	  public void get_active_movies(Connection conn){
		  System.out.println(utility.as_bold_color("[iii]","g")+" Query Active Movies ==>");
		  PreparedStatement stmt=null;
		  ResultSet res=null;
		  String sql = "SELECT title from movie where available=true order by title;";
		try {
			stmt = conn.prepareStatement(sql);
			res = stmt.executeQuery();
			int i = 1;
			
		    while (res.next()){
			      System.out.println(i+": "+res.getString(1));
			      // todo: limit the print rows number
			      i++;
			}
		}catch(SQLException e){
			System.out.println("Query Active Movie failed,SQL error: ");
			e.printStackTrace();
 		}catch(Exception e){
			System.out.println("Query Active Movie failed, class error: ");
			e.printStackTrace();
		}finally{
			 try{
		         if(stmt!=null)
		            stmt.close();
		         if(res!=null)
			        res.close();
		      }catch(SQLException e){
		    	 System.out.println("Query Active Movie failed,SQL error: ");
		    	 e.printStackTrace();
		      }//end finally try
		}
		System.out.println(utility.as_bold_color("[iii]","g")+" Query Active Movie finished.");
	  }
	  
	  /*
	   * Get the number of movies that each actor, director pair have collaborated
    on, in descending order, with option to limit result count.
	   * */
	  public void get_actor_director_pairs(Connection conn){}
	  /*
	   *  Which users watch the most movies (of a certain genre) in a given time frame?
	   *  Get the most binge-heavy movie watchers in a certain time frame, optionally
    filtering by genre and limiting number of query results returned.
	   * */
	  public void get_busiest_users(Connection conn){}
	  
	  
	  
	  public void get_highest_grossing_studios(Connection conn){}
	  /* Which actors have the highest associated movie ratings?
       * Calculate an actor's rating as the average rating across all the movies he starred in
	   * */
	  public void get_highest_rated_actors(Connection conn){}
	  
	  /*
	   * Which directors have the highest associated movie ratings?
	   * + Calculate a director's rating as the average rating across all the movies he directed
	   * */
	  public void get_highest_rated_directors(Connection conn){}
	  
	  /*
	   *  Get highest-rated movie(s) for a given time frame, genre
	   *  Get the highest-rated movies in a certain time frame, optionally
    filtering by genre and limiting number of query results returned.
	   * */
	  public void get_highest_rated_movies(Connection conn){}
	  
	  /*
	   * Which movies are the most popular in a given time frame?
	   * Get the most popular movies in a certain time frame, optionally
    filtering by genre and limiting number of query results returned.
	   * */
	  public void get_popular_movies(Connection conn){}
	  
	  /*
	   * For a given user id, get the start and end dates of his current subscription.
	   * */
	  public void get_user_current_subscription_window(Connection conn){}
	  
	  /*
	   * Get, for each user, which genre(s) that user is most likely to watch.
	   * */
	  public void get_user_genres(Connection conn){}
	  /*
	   * Leave a review for a particular user on a particular movie.
    If the user has already reviewed this movie, prompt the user
    to confirm that he wants to overwrite his previous review.
	   * */
	  public void leave_a_review(Connection conn){}
	  
	  /*
	   * Set a movie's active status to true, meaning it is actively streaming.
    The movie must already be present in the database.
    Keep historical records of the movie being watched.
	   * */
	  public void relist_movie(Connection conn){}
	  public void remove_user(Connection conn){}
	 
}
