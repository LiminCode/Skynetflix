import java.sql.*;


public class Task {
	  // Generate a list of all students and their advisors.
	  public static void add_user(Connection conn){
		  
		  PreparedStatement stmt=null;
		  ResultSet res=null;
		  String sql = "";
		try {
			stmt = conn.prepareStatement(sql);
			res = stmt.executeQuery();
		    while (res.next()){
			      System.out.println(res.getString(1) + " " + res.getString(2) + " " + res.getString(3));
			}
		}catch(SQLException e){
			System.out.println("Query advisor list Failed,SQL error: ");
			e.printStackTrace();
 		}catch(Exception e){
			System.out.println("Query advisor list Failed, class error: ");
			e.printStackTrace();
		}finally{
			 try{
		         if(stmt!=null)
		            stmt.close();
		         if(res!=null)
			        res.close();
		      }catch(SQLException e){
		    	 System.out.println("Query advisor list Failed,SQL error: ");
		    	 e.printStackTrace();
		      }//end finally try
		}
		System.out.println("Query advisor list finished.");
	  }
 
}
