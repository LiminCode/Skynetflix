import java.util.*;
import java.sql.Connection;
public class Skynetflix {
	 public static void main(String[] args){
		 System.out.println("+".repeat(10));
		 
		 
		 
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
		 String user = scan.next();
		 DatabaseConnection dbConn = new DatabaseConnection();
		 Connection conn = dbConn.Connect(user);
		 boolean quit = false;
		 while (!quit){
		        System.out.println("\033[32;4m" + "=".repeat(50) + "\033[0m"+
		        						"\nWhat would you like to do?\n" +
		  			                   "\t(a) Generate advisor list\n" +
		  			                   "\t(i) Hire an instructor\n" +
		      			               "\t(t) Generate a student transcript\n" +
		  			                   "\t(c) Generate a list of courses for a given semester/year\n" +
		  			                   "\t(r) register a student for a course\n\n" +
		  			                   "Enter a single letter corresponding to one of the above here, " +
		  			                   "or enter 'q' to exit: ");

		        String call = scan.next();

		        switch(call.toLowerCase().charAt(0)){
		        	case 'a':
		        		Task.advisor_list(conn);
		        		break;
		        	case 'i':
		        		Task.hire_instructor(conn);
		        		break;
		        	case 't':
		        		Task.transcript(conn);
		        		break;
		            case 'c':
		                Task.course_list(conn);
		                break;
		            case 'r':
		            	Task.register_student(conn);
		                break;
			        case 'q':
			        	quit = true;
			        	break;
			        default:
			          System.out.println("Not a valid action.");
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
