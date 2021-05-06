import java.sql.*;


public class Task {
	  Utilities utility = new Utilities();  // for print in color
	
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
	  
	  //add_movie
	  // Generate a list of all students and their advisors.
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
 
}
