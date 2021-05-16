import java.util.*;
import java.sql.Connection;
import java.sql.SQLException;

public class Skynetflix {
	public static void main(String[] args) {
		System.out.println("+".repeat(10));
		Utilities utility = new Utilities(); // for print in color
		Task task = new Task();

		// start SSH forwarding if not running on Skynet
		SshPortForward forward = new SshPortForward();
		String os = System.getProperty("os.name");
		System.out.println("Operation System: " + os);
		if (os.toLowerCase().startsWith("win")) {
			forward.StartSSH();
		}

		// connect database
		Scanner scan = new Scanner(System.in);
		System.out.println("\033[32;4m" + "Enter database user:" + "\033[0m");
		// String user = scan.next();
		String user = "lwang24"; // speed up debug
		System.out.println("\033[32;4m" + "Which Database?(enter s for small, b for big):" + "\033[0m");
		// String database = scan.next();
		String database = "s";
		
		
		DatabaseConnection dbConn = new DatabaseConnection();
		Connection conn = dbConn.Connect(user,database);
		boolean quit = false;
		while (!quit) {
			System.out.println("\033[32;4m" + "=".repeat(50) + "\033[0m" + "\nWhat would you like to do?\n"
					+ "\t( 0) Add Actors To Movie\n" 
					+ "\t( 1) Add Movie\n" 
					+ "\t( 2) Add user\n"
					+ "\t( 3) Ending subscriptions\n" 
					+ "\t( 4) Generate subscription counts\n"
					+ "\t( 5) Get movies\n" 
					+ "\t( 6) Get actor director pairs\n" 
					+ "\t( 7) Busiest users\n"
					+ "\t( 8) Get highest grossing studios\n" 
					+ "\t( 9) Get highest rated actors\n"
					+ "\t(10) Get highest rated directors\n" 
					+ "\t(11) Get highest rated movies\n"
					+ "\t(12) Get popular movies\n" 
					+ "\t(13) Get user current subscription window\n"
					+ "\t(14) Get user genres\n" 
					+ "\t(15) Leave a review\n" 
					+ "\t(16) Remove user\n" 
					+ "\t(17) Add director\n" 
					+ "\t(18) Add studio\n"
					+ "\t(19) Get user info by id\n" 
					+ "\t(20) Add actor\n"
					+ "Enter an integer or enter 'q' to exit: \n");

			String call = scan.nextLine();
			// string -> integer
			int number = -1;
			try {
				number = Integer.parseInt(call);
			} catch (NumberFormatException e) {
				// here means not a integer
				quit = true;
				System.out.println("Not a integer, quit...");
				break;
			}
			switch (number) { // TODO --- replace the methods when finish
			case 0:
				task.add_actors_to_movie(conn);
				break;
			case 1:
				task.add_movie(conn);
				break;
			case 2:
				task.add_user(conn);
				break;
 
			case 3:
				task.ending_subscriptions(conn);
				break;
			case 4:
				task.generate_subscription_counts(conn);
				break;
			case 5:
				task.get_movies(conn);
				break;
			case 6:
				task.get_actor_director_pairs(conn);
				break;
			case 7:
				task.get_busiest_users(conn);
				break;
			case 8:
				task.get_highest_grossing_studios(conn);
				break;
			case 9:
				task.get_highest_rated_actors(conn);
				break;
			case 10:
				task.get_highest_rated_directors(conn);
				break;
			case 11:
				task.get_highest_rated_movies(conn);
				break;
			case 12:
				task.get_popular_movies(conn);
				break;
			case 13:
				task.get_user_current_subscription_window(conn);
				break;
			case 14:
				task.get_user_genres(conn);
				break;
			case 15:
				task.leave_a_review(conn);
				break;
			case 16:
				task.remove_user(conn);
				break;
			case 17:
				task.add_director(conn);
				break;
			case 18:
				task.add_studio(conn);
				break;
			case 19:
				task.get_user(conn);
				break;
			case 20:
				task.add_actor(conn);
				break;
			default:
				System.out.println(utility.as_bold_color("[!!!]", "r") + "Not a valid action: " + number);
			}
			System.out.println("Press Enter to continue ...");
			// press c to continue
			call = scan.nextLine();
		}
		System.out.println("\n-- -- -- -- -- -- -- --\nExiting...");
		dbConn.CloseConnection();
		if (os.toLowerCase().startsWith("win")) {
			forward.CloseSSH();
		}

		System.out.println("Goodbye.");
	}
}
