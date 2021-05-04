import java.sql.*;
import java.util.*;

public class DatabaseConnection {
 
	Connection conn = null;
	String url = "jdbc:postgresql://localhost:5432/skynetflix_small";
	Properties info; 
 
	public Connection Connect(String userid) {
		System.out.println("Connect to postgreSQL....");
		info = new Properties(); 
	    info.setProperty("user",userid);  
	    info.setProperty("password","");
		try {
			Class.forName("org.postgresql.Driver");
			conn = DriverManager.getConnection(url, info);
			Statement st = conn.createStatement();
			ResultSet rs = st.executeQuery("SELECT version()");
			System.out.println("Connect to postgreSQL success:");
			while (rs.next())
			{
			    System.out.println(rs.getString(1));
			}
			rs.close();
			st.close();
		}catch (Exception e) {
			System.out.println("Connect to postgreSQL failed:");
			System.out.println(e);
			System.out.println("Exit Program Now...");
			
			System.exit(0);
		}
		
		
		return conn;
		 
	}
	public void CloseConnection() {
 
		try {
			conn.close();
		}catch (SQLException e) {
			System.out.println("Close Connection to postgreSQL failed:");
			System.out.println(e);
		}
		System.out.println("Connection to postgreSQL Closed.");
	}
}
