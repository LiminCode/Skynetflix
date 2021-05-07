import java.sql.*;
import java.util.Calendar;
import java.util.Date;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

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
		  String[] fileds = new String[]{"Title","URL","genre","Released date (YYYY-MM-DD)", "budget", "Summary", "Studio", "Director ID"};
		  Utilities utility = new Utilities();
		  String[] values = utility.menu_selections(fileds);
		  // check if Director and Studio exists
		  int director_id =0;
		  if (values[7].isBlank()==false){
			  director_id = Integer.parseInt(values[7]);
		  }
		  
		  if (this.check_director_exsist(conn, director_id)==false) {
			  System.out.println(utility.as_bold_color("[!!!]","r")+" Director ID doesn't exsit, you might add director first.");
			  return;
		  }
		  if (values[6].isBlank()==false) {

			  if (this.check_studio_exsist(conn, values[6])==false) {
				  System.out.println(utility.as_bold_color("[!!!]","r")+" Studio doesn't exsit. you might add director first.");
				  return;
			  }
		  }
			double budget=0;
			if (values[4].isBlank()==false) {
				try {
					budget =Double.parseDouble(values[4]);
				}catch (Exception  e){
				      System.out.println("Not a valid budget: "+values[4]);
				      return;
				}
			}
			java.sql.Date movie_date;
			try {
				movie_date = dateUtil.strToDate(values[3]);
				
			}catch(Exception  e) {
				System.out.println(utility.as_bold_color("[!!!]","r")+"Not a valid date: "+values[3]);
			      return;
			}
			String sql = "INSERT INTO movie  (title, url, genre,date_released, budget, summary, studio, director_id) VALUES (?, ?, ?, ?,?,?,?,?)";
			PreparedStatement statement=null;
		    try {
		      statement  = conn.prepareStatement(sql);
		      
		      statement.setString(1, values[0]); // title
		      statement.setString(2, values[1]); // url
		      statement.setString(3, values[2]); // genre
		      statement.setDate(4, movie_date); // released date
		      statement.setDouble(5, budget); // budget
		      statement.setString(6, values[5]); // summary
		      statement.setString(7, values[6]); // studio
		      statement.setInt(8, director_id); // director_id
		      
		      int row_added = statement.executeUpdate();
		      System.out.println(utility.as_color("[SUCCESS]", "g")+"  >>>> Insert successful. row added:" + row_added);
		    }catch (SQLException sqle){
		      System.out.println("Could not insert movie into db." + sqle);
		    }catch (Exception  e){
			      System.out.println("Could not insert movie into db.");
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
		System.out.println(utility.as_bold_color("[iii]","g")+"Add new Movie finished.");
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
	  public List<Object> check_user_exists(Connection conn, int id) {
		  String sql = "Select * from users where id = ?;";
			PreparedStatement statement=null;
			ResultSet res=null;
		    List<Object> list = new ArrayList<Object>();
			try {
		      statement  = conn.prepareStatement(sql);
		       statement.setInt(1, id);
		       String[] arr;
		       res = statement.executeQuery();
		       if (res.next()) {
		    	   list.add(res.getInt(1)); //id
		    	   list.add(res.getString(2)); //first name
		    	   list.add(res.getString(3)); //last name
		    	   list.add(res.getString(4)); //email
		    	   list.add(res.getString(5)); //phone number
		    	   list.add(res.getString(6)); //phone number
		    	   System.out.println(utility.as_color("[iii]", "g")+"  >>>> User "+ id+" exsist: " + res.getString(2) +res.getString(3));
		       }else {
		    	   System.out.println(utility.as_color("[iii]", "g")+"  >>>> User "+ id+" not exsist.");
				    
		       }
		       return list;
		      }catch (SQLException sqle){
		      System.out.println("Could not query user." + sqle);
		    }catch (Exception  e){
			      System.out.println("Could not query user.");
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
			  System.out.println(utility.as_bold_color("[iii]","g")+" Check User ======> Finished");
			return list;
	  }
	  
	  public List<Object> check_movie_exists(Connection conn, int id) {
		  String sql = "Select * from movie where id = ?;";
			PreparedStatement statement=null;
			ResultSet res=null;
		    List<Object> list = new ArrayList<Object>();
			try {
		      statement  = conn.prepareStatement(sql);
		       statement.setInt(1, id);
		       res = statement.executeQuery();
		       if (res.next()) {
		    	   list.add(res.getInt(1)); //id
		    	   list.add(res.getString(2)); //title
		    	   list.add(res.getString(3)); //url
		    	   list.add(res.getString(4)); //genre
		    	   list.add(res.getString(5)); //date_released
		    	   list.add(res.getString(6)); //rating
		    	   list.add(res.getDouble(7)); //budget
		    	   list.add(res.getDouble(8)); //gross income
		    	   list.add(res.getString(9)); //summary
		    	   list.add(res.getString(10)); //studio
		    	   list.add(res.getInt(11)); //director id
		    	   
		    	   
		    	   System.out.println(utility.as_color("[iii]", "g")+"  >>>> Movie "+ id+" exsist: " + res.getString(2)  );
		       }else {
		    	   System.out.println(utility.as_color("[iii]", "g")+"  >>>> Movie "+ id+" not exsist.");
				    
		       }
		       return list;
		      }catch (SQLException sqle){
		      System.out.println("Could not query movie." + sqle);
		    }catch (Exception  e){
			      System.out.println("Could not query movie.");
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
			  System.out.println(utility.as_bold_color("[iii]","g")+" Check Movie ======> Finished");
			return list;
	  }
	  public List<Object> check_review_exists(Connection conn, int user_id,int movie_id) {
		  String sql = "Select * from review where user_id = ? and movie_id = ?;";
			PreparedStatement statement=null;
			ResultSet res=null;
		    List<Object> list = new ArrayList<Object>();
			try {
		      statement  = conn.prepareStatement(sql);
		       statement.setInt(1, user_id);
		       statement.setInt(2, movie_id);
		       res = statement.executeQuery();
		       if (res.next()) {
		    	   list.add(res.getInt(1)); //user_id
		    	   list.add(res.getInt(2)); //movie_id
		    	   list.add(res.getString(3)); //review date
		    	   list.add(res.getDouble(4)); //rating
		    	   list.add(res.getString(5)); //content 
		    	   System.out.println(utility.as_color("[iii]", "g")+"  >>>> Review from user "+ user_id+"about movie"+ movie_id+" exsist: " + res.getString(3) );
		       }else {
		    	   System.out.println(utility.as_color("[iii]", "g")+"  >>>> Review from user "+ user_id+"about movie"+ movie_id+"not exsist.");
   				    
		       }
		       return list;
		      }catch (SQLException sqle){
		      System.out.println("Could not query review." + sqle);
		    }catch (Exception  e){
			      System.out.println("Could not query review.");
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
			  System.out.println(utility.as_bold_color("[iii]","g")+" Check review ======> Finished");
			return list;
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
	  public boolean check_director_exsist(Connection conn, int id){

		  String sql = "Select first_name, last_name, age from director where id = ?;";
			PreparedStatement statement=null;
			ResultSet res=null;
		    try {
		      statement  = conn.prepareStatement(sql);
		       statement.setInt(1, id);
		      
		       res = statement.executeQuery();
		       if (res.next()==false) {
		    	   return false;
		       }
		      //System.out.println(utility.as_color("[SUCCESS]", "g")+"  >>>> Insert successful. row added:" + row_added);
		    }catch (SQLException sqle){
		      System.out.println("Could not query director." + sqle);
		    }catch (Exception  e){
			      System.out.println("Could not query director.");
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
			  System.out.println(utility.as_bold_color("[iii]","g")+" Check Director ======> OK");
			return true;
	  }
	  public boolean check_studio_exsist(Connection conn, String name){

		  String sql = "Select name from studio where name = ?;";
			PreparedStatement statement=null;
			ResultSet res=null;
		    try {
		      statement  = conn.prepareStatement(sql);
		       statement.setString(1, name);
		      
		       res = statement.executeQuery();
		       if (res.next()==false) {
		    	   return false;
		       }
		      //System.out.println(utility.as_color("[SUCCESS]", "g")+"  >>>> Insert successful. row added:" + row_added);
		    }catch (SQLException sqle){
		      System.out.println("Could not query studio." + sqle);
		    }catch (Exception  e){
			      System.out.println("Could not query studio.");
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
			  System.out.println(utility.as_bold_color("[iii]","g")+" Check Studio ======> OK");
			return true;
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
	  public void get_movies(Connection conn){
		  System.out.println(utility.as_bold_color("[iii]","g")+" Query Movies ==>");
		  PreparedStatement stmt=null;
		  ResultSet res=null;
		  String sql = "SELECT title from movie order by title;";
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
	  public void leave_a_review(Connection conn){
		  System.out.println(utility.as_bold_color("[iii]","g")+" Leave a Review ======>");
		  String[] fileds = new String[]{"User ID","Movie ID","Review Date(YYYY-MM-DD)","Rating(1-100)","Content"};
		  Utilities utility = new Utilities();
		  String[] values = utility.menu_selections(fileds);
		  
		  // check user
		  int user_id =  parseIntwithName(values[0],"User ID");
		  if (user_id==-1) {return;}
		  List<Object> user_info = check_user_exists(conn, user_id);
		  if (user_info.isEmpty()) {
			  System.out.println(utility.as_color("[!!!]", "r")+">>> User ID not exsist.");
			  return;
		  }
		  
		  // check movie
		  int movie_id =  parseIntwithName(values[1],"Movie ID");
		  if (movie_id==-1) {return;}
		  List<Object> movie_info = check_movie_exists(conn, movie_id);
		  if (movie_info.isEmpty()) {
			  System.out.println(utility.as_color("[!!!]", "r")+">>> Movie ID not exsist.");
			  return;
		  }
		  
		  // get date
			java.sql.Date review_date;
			try {
				review_date = dateUtil.strToDate(values[2]);
			}catch(Exception  e) {
				System.out.println(utility.as_bold_color("[!!!]","r")+"Not a valid date: "+values[3]);
			      return;
			}
		  	  
		  //parse Rating
		  int rating =  parseIntwithName(values[3],"Rating");
		  if (rating <= 0) {return;}
		  // check exsist
		  List<Object> review_info = check_review_exists(conn,user_id, movie_id);
		  if (!review_info.isEmpty()) {
			  System.out.println(utility.as_color("[!!!]", "r")+">>> Do you want to overwrite the previous review? (Y/N)");
			  Scanner scan = new Scanner(System.in);
			  String get = scan.nextLine();
			 
			  if(get.equals("Y")) {
				  System.out.println(utility.as_color("[!!!]", "r")+">>>Overwrite..."); 
				  // here call overWrite
				   
			  }else {
				  System.out.println(utility.as_color("[!!!]", "r")+">>>Not Overwrite, Quit...");
				  return;
			  }

		  }

		  String insert_sql = "INSERT INTO review  (user_id,movie_id, review_date, rating,content) VALUES (?, ?, ?,?,?);";
		  String update_sql = "UPDATE review SET review_date=?, rating=?, content=? WHERE user_id = ? AND movie_id = ? ;";
		   PreparedStatement statement=null;
		    try {
				  //insert
				  if (review_info.isEmpty()) {
					  statement  = conn.prepareStatement(insert_sql);
				      statement.setInt(1, user_id);
				      statement.setInt(2, movie_id);
				      statement.setDate(3, review_date);
				      statement.setInt(4, rating);
				      statement.setString(5, values[4]);
				      int row_added = statement.executeUpdate();
				      System.out.println(utility.as_color("[SUCCESS]", "g")+"  >>>> Insert review successful. row added:" + row_added);
				  }else { //update
					  statement  = conn.prepareStatement(update_sql);

				      statement.setDate(1, review_date);
				      statement.setInt(2, rating);
				      statement.setString(3, values[4]);
				      statement.setInt(4, user_id);
				      statement.setInt(5, movie_id);
				      int row_added = statement.executeUpdate();
				      System.out.println(utility.as_color("[SUCCESS]", "g")+"  >>>> Update review successful. row added:" + row_added);
				  }
		      
		    }catch (SQLException sqle){
		      System.out.println("Could not insert review into db." + sqle);
		    }catch (Exception  e){
			      System.out.println("Could not insert review into db.");
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
	   * Set a movie's active status to true, meaning it is actively streaming.
    The movie must already be present in the database.
    Keep historical records of the movie being watched.
	   * */
	  public void relist_movie(Connection conn){}
	  public void remove_user(Connection conn){}
	  
	  
	  public int parseIntwithName(String str, String name) {
		  int re=0;
			try {
				re =Integer.parseInt(str);
			}catch (Exception  e){
			      System.out.println("Not a valid "+name+ ": "+str);
			      return -1;
			}
			return re;
	  }
}
