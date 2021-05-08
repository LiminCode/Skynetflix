import java.text.DecimalFormat;
import java.util.*;

public class Utilities {
	Dictionary colors;

	public Utilities() {
		colors = new Hashtable();
		colors.put("r", "31");
		colors.put("dr", "31");
		colors.put("o", "38;5;202'");
		colors.put("mac", "38;5;214");
		colors.put("y", "33");
		colors.put("m", "35");
		colors.put("g", "32");
		colors.put("dg", "38;5;22");
		colors.put("teal", "36");
		colors.put("b", "34");
		colors.put("orchid", "38;5;165");
		colors.put("p", "38;5;56");
		colors.put("bold", "1");
		colors.put("reset", "reset");
	}

	/*
	 * Prompt the user for input for each field in `fields`, asking for confirmation
	 * at the end and allowing for re-entry.
	 */
	public String[] menu_selections(String[] fields) {
		Scanner scan = new Scanner(System.in);
		String[] res = new String[fields.length];
		String confirm = null;
		while (true) {
			for (int i = 0; i < fields.length; i++) {
				System.out.print("Enter " + fields[i] + ": ");
				String get = scan.nextLine();
				res[i] = get; // blank

			}
			System.out.println("YOU ENTERED: ");
			for (int i = 0; i < fields.length; i++) {
				System.out.println("    >>>" + fields[i] + " = " + res[i]);
			}
			System.out.print("IS THIS CORRECT? (type 'y' without quotes to acknowledge): ");
			confirm = scan.nextLine();

			if (!confirm.isBlank() && confirm.toLowerCase().charAt(0) == 'y') {
				break;
			}
		}
		return res;
	}

	public String as_color(String source, String color) {
		String res = "\033[" + this.colors.get(color) + "m" + source + "\033[0m";
		return res;
	}

	public String as_bold_color(String source, String color) {
		String res = "\033[1m\033[" + this.colors.get(color) + "m" + source + "\033[0m";
		return res;
	}

	public String double_to_string(double num) {
		DecimalFormat format = new DecimalFormat("#.00");
		String scaled = format.format(num);
		return scaled;
	}

	public String capitalize(String str) {
		str = str.toLowerCase();
		String s1 = str.substring(0, 1).toUpperCase();
		String apitalized = s1 + str.substring(1);
		return apitalized;
	}

}
