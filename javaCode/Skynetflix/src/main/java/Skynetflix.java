import java.util.*;
import java.sql.Connection;
public class Skynetflix {
	 public static void main(String[] args){
		 System.out.println("+".repeat(10));
		 Utilities utility = new Utilities();  // for print in color
		 Task task = new Task();
		 
		 // start SSH forwarding if not running on Skynet 
		 SshPortForward forward = new SshPortForward();
		 String os = System.getProperty("os.name"); 
		 System.out.println("Operation System: "+os);
		 if(os.toLowerCase().startsWith("win")){  
			 forward.StartSSH();
		 } 
		
		 // connect database
		 Scanner scan = new Scanner(System.in);
		 System.out.println("\033[32;4m"+"Enter user:"+"\033[0m");
		 //String user = scan.next();
		 String user = "lwang24"; // speed up debug
		 DatabaseConnection dbConn = new DatabaseConnection();
		 Connection conn = dbConn.Connect(user);
		 boolean quit = false;
		 while (!quit){
		        System.out.println("\033[32;4m" + "=".repeat(50) + "\033[0m"+
		        						"\nWhat would you like to do?\n" +
		  			                   "\t(0) Add actors to movie\n" +
		  			                   "\t(1) add movie\n" +
		  			                   "\t(2) add user\n" +
		  			                   "\t(3) delist movie\n" +
		  			                   "\t(4) ending subscriptions\n" +
		  			                   "\t(5) generate subscription counts\n" +
		  			                   "\t(6) get active movies\n" +
		  			                   "\t(7) get actor director pairs\n" +
		  			                   "\t(8) get busiest users\n" +
		  			                   "\t(9) get highest grossing studios\n" +
		  			                   "\t(10) get highest rated actors\n" +
		  			                   "\t(11) get highest rated directors\n" +
		  			                   "\t(12) get highest rated movies\n" +
		  			                   "\t(13) get popular movies\n" +
		  			                   "\t(14) get user current subscription window\n" +
		  			                   "\t(15) get user genres\n" +
		  			                   "\t(16) leave a review\n" +
		  			                   "\t(17) relist movie\n" +
		  			                   "\t(18) remove user\n" +
		  			                   "Enter an integer or enter 'q' to exit: \n");

		        String call = scan.next();
		        // string -> integer
		        int number= -1;
		        try {
		        	number = Integer.parseInt(call);
		        }catch(NumberFormatException e) {
		        	// here means not a integer
		        	quit = true;
		        	System.out.println("Not a integer, quit...");
		        	break;
		        }
		        switch(number){ // TODO --- replace the methods when finish
		        	case 1:
		        		task.get_active_movies(conn);
		        		break;
		        	case 2:
		        		task.add_movie(conn);
		        		break;
		        	case 3:
		        		task.get_active_movies(conn);
		        		break;
		        	case 4:
		        		task.get_active_movies(conn);
		        		break;
		        	case 5:
		        		task.get_active_movies(conn);
		        		break;
		        	case 6:
		        		task.get_active_movies(conn);
		        		break;
		        	case 7:
		        		task.get_active_movies(conn);
		        		break;
		        	case 8:
		        		task.get_active_movies(conn);
		        		break;
		        	case 9:
		        		task.get_active_movies(conn);
		        		break;
		        	case 10:
		        		task.get_active_movies(conn);
		        		break;
		        	case 11:
		        		task.get_active_movies(conn);
		        		break;
		        	case 12:
		        		task.get_active_movies(conn);
		        		break;
		        	case 13:
		        		task.get_active_movies(conn);
		        		break;
		        	case 14:
		        		task.get_active_movies(conn);
		        		break;
		        	case 15:
		        		task.get_active_movies(conn);
		        		break;
		        	case 116:
		        		task.get_active_movies(conn);
		        		break;
		        	case 17:
		        		task.get_active_movies(conn);
		        		break;
		        	case 18:
		        		task.get_active_movies(conn);
		        		break;
			        default:
			          System.out.println(utility.as_bold_color("[!!!]","r")+"Not a valid action: "+number);
		        }
		 }
		 System.out.println("\n-- -- -- -- -- -- -- --\nExiting...");
		 dbConn.CloseConnection();
		 if(os.toLowerCase().startsWith("win")){  
			 forward.CloseSSH();
		 } 
		 
		 System.out.println("Goodbye.");
	 }
}
