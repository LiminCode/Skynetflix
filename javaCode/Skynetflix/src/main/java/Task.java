import java.sql.*;
import java.util.Dictionary;
import java.util.Hashtable;

public class Task {
	  // Generate a list of all students and their advisors.
	  public static void advisor_list(Connection conn){
		  System.out.println("Query advisor list start...");
		  PreparedStatement stmt=null;
		  ResultSet res=null;
		  String sql = ""
				  	+ "SELECT "
				  		+ "S.ID, S.name, I.name "
					+ "FROM "
						+ "student S "
						+ "JOIN "
						+ "advisor A "
							+ "ON (S.ID = A.s_ID) "
						+ "JOIN "
						+ "instructor I "
							+ "ON (A.i_ID = I.ID);";
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

	  /*Insert a new instructor into the database by providing
		his ID, name, department, salary.
		Raise ValueError if ID is alrady taken or if the department
		specified does not exist.*/
	  public static void hire_instructor(Connection conn){
		System.out.println("Hire Instructor"+"*".repeat(40));
		String[] fileds = new String[]{"instructor ID","instructor name","department name","salary"};
		Utilities utility = new Utilities();
		String[] values = utility.menu_selections(fileds);
		double salary_num=0;
		try {
			salary_num =Double.parseDouble(values[3]);
		}catch (Exception  e){
		      System.out.println("Not a valid salary: "+values[3]);
		      return;
		}
	    
		String sql = "INSERT INTO instructor  (ID, name, dept_name, salary) VALUES (?, ?, ?, ?)";
		PreparedStatement statement=null;
	    try {
	      statement  = conn.prepareStatement(sql);
	      statement.setString(1, values[0]);
	      statement.setString(2, values[1]);
	      statement.setString(3, values[2]);
	      statement.setDouble(4, salary_num); 
	      int row_added = statement.executeUpdate();
	      System.out.println(utility.as_color("[SUCCESS]", "g")+"  >>>> Insert successful. row added:" + row_added);
	    }catch (SQLException sqle){
	      System.out.println("Could not insert instructor into db." + sqle);
	    }catch (Exception  e){
		      System.out.println("Could not insert instructor into db.");
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
	  // Generate a transcript for a student given his ID.
	  public static void transcript(Connection conn) {
		  System.out.println("Show Transcript"+"*".repeat(40));
		  String[] fileds = new String[]{"Student ID"};
		  Utilities utility = new Utilities();
		  String[] values = utility.menu_selections(fileds);
		  //verify exists
		  String sql = "SELECT name,dept_name from student where id = ?"; // guaranteed to be 1 or 0 result
		  PreparedStatement statement=null;
		  ResultSet res=null;
		  String name, dept_name;
		  try {
			  statement  = conn.prepareStatement(sql);
		      statement.setString(1, values[0]);
				res = statement.executeQuery();
				if(!res.next()){
				      System.out.println(utility.as_color("[!!!]", "r")+"  >>>> Student id not exist:"+values[0]);
				      return;
				}else {
					name = res.getString(1);
					dept_name = res.getString(2);
					System.out.println(res.getString(1) + " " + res.getString(2) );
				}
				// NULL grades are represented by 'N/A'
				sql = "SELECT "
						+ "course_id, sec_id, title, credits, "
						+ "COALESCE(grade,'N/A'),year,semester "
					+ "FROM "
						+ "takes T JOIN course C USING (course_id) "
					+ "WHERE "
						+ "ID = ? "
					+ "ORDER BY year ASC, semester DESC";
				statement  = conn.prepareStatement(sql);
			    statement.setString(1, values[0]);
			    res = statement.executeQuery();


			    System.out.println("*".repeat(50));
			    System.out.println("TRASNCRIPT FORMAT:");
			    String format = "   "+
			    		utility.as_color("{course ID}-{section}", "r")+ " "+
			    		utility.as_color("{course title}", "y")+" "+"{credits} "+
			    		utility.as_bold_color("{letter grade}", "g") ;
			    System.out.println(format);
			    System.out.println(utility.as_color("    '*' after GPA means N/A grades were ignored","b"));
			    System.out.println();
			    System.out.println(utility.as_color(name,"bold")+"  "+
			    "(ID = "+utility.as_color(values[0],"teal")+
			    " ) department: "+utility.as_color(dept_name,"o"));
			    // calculate
			    if(res.isLast()) {
			    	System.out.println("No course taken record.");
			    	return;
			    }
			    
			    String semester_year = null;
			    
			      
			    double section_grade_sum = 0; // for every semester-year
			    double section_credit_sum = 0;
			    double total_grade_sum = 0;
			    double total_credit_sum = 0;
			    
			    // GPA = sum(grade*credit)/sum(credit)
			    // The semester and year is ordered, so we can use iteration 
			    // N/A graded course not counted to GPA, since it means not finished/graded.
			    while (res.next()){
			    	String course_id = res.getString(1);
			    	String sec_id = res.getString(2);
			    	String title = res.getString(3);
			    	int credits = res.getInt(4);
			    	String grade = res.getString(5);
			    	String year = res.getString(6);
			    	String semester = res.getString(7);
				    String new_semester_year = semester+" "+year;
				    
				    if(new_semester_year.equals(semester_year)){
				    	// still the same semester and year
				    	// print course
						String course_info = utility.as_color(course_id+"-"+sec_id,"r")+ " "+
											 utility.as_color(title,"y")+ " ("+credits+") "+
											 utility.as_bold_color(grade,"g") ;// like "CS-101-1 Intro. to Computer Science(4) C"
						System.out.println(course_info);
						if(!grade.equals("N/A")) {
							grade = (String)utility.grades.get(grade);
							double grade_df = 0;
							try {
								grade_df =Double.parseDouble(grade);
							}catch (Exception  e){
							      System.out.println("Not a valid grade: "+grade);
							      return;
							}
							section_grade_sum += grade_df*credits;
							section_credit_sum+=credits;
							total_grade_sum+= grade_df*credits;
							total_credit_sum+=credits;
						} 
				    }else {// a new semester or year
				    	  
				    	// first, print last semester-year 's GPA
				    	if (semester_year!=null){
				    		// print last semester-year 's GPA
				    		System.out.println("    *  *  *    ");
				    		if (section_credit_sum!=0) {
				    			double gpa = section_grade_sum/section_credit_sum;
					    		System.out.println(utility.as_color("    >"+semester_year+" GPA = "+utility.double_to_string(gpa),"bold"));
				    		}else {
					    		System.out.println(utility.as_color("    >"+semester_year+" GPA = N/A ","bold"));
				    		}
				    		
				    		
				    	}
				    	semester_year = new_semester_year;
				    	section_grade_sum = 0;
				    	section_credit_sum = 0;
				    	System.out.println();
				    	System.out.println(utility.as_color(semester_year,"bold")); // like "Spring 2017"
						
						// print course
						String course_info = utility.as_color(course_id+"-"+sec_id,"r")+ " "+
											 utility.as_color(title,"y")+ " ("+credits+") "+
											 utility.as_bold_color(grade,"g") ;// like "CS-101-1 Intro. to Computer Science(4) C"
						System.out.println(course_info);
						if(!grade.equals("N/A")) {
							grade = (String)utility.grades.get(grade);
							double grade_df = 0;
							try {
								grade_df =Double.parseDouble(grade);
							}catch (Exception  e){
							      System.out.println("Not a valid grade: "+grade);
							      return;
							}
							section_grade_sum += grade_df*credits;
							section_credit_sum+=credits;
							total_grade_sum+= grade_df*credits;
							total_credit_sum+=credits;
						} 
				    }
				}
			    // print last semester's gpa
			   	// first, print last semester-year 's GPA
		    	if (semester_year!=null){
		    		// print last semester-year 's GPA
		    		System.out.println("    *  *  *    ");
		    		if (section_credit_sum!=0) {
		    			double gpa = section_grade_sum/section_credit_sum;
			    		System.out.println(utility.as_color("    >"+semester_year+" GPA = "+utility.double_to_string(gpa),"bold"));
		    		}else {
			    		System.out.println(utility.as_color("    >"+semester_year+" GPA = N/A ","bold"));
		    		}
		    		
		    		
		    	}
			    // finally print the over all gpa
			    
	    		if (total_credit_sum!=0) {
	    			double gpa = total_grade_sum/total_credit_sum;
		    		System.out.println(utility.as_color("Cumulative GPA = "+utility.double_to_string(gpa),"bold"));
	    		}else {
		    		System.out.println(utility.as_color("Cumulative GPA = N/A","bold"));
	    		}
		  }catch (SQLException sqle){
		      System.out.println("Could not query student id in db: " + sqle);
		      return;
		    }catch (Exception  e){
			      System.out.println("Could not query student id in db.");
			      e.printStackTrace();
			      return;
			}finally {
				try{
			         if(statement!=null)
			        	 statement.close();
			         if(res!=null)
				        res.close();
			      }catch(SQLException e){
			    	 System.out.println("Query transcript,SQL error: ");
			    	 e.printStackTrace();
			    	 return;
			      }//end finally try
			}
		  //
		  System.out.println(utility.as_color("[SUCCESS]", "g")+"  >>>> Query transcript finished.");
		  return;
	  }
	  // Generate a list of course sections offered in a given year/semester.
	  public static void course_list(Connection conn){
		  System.out.println("Show Course List"+"*".repeat(40));
		  String[] fileds = new String[]{"semester","year"};
		  Utilities utility = new Utilities();
		  String[] values = utility.menu_selections(fileds);
		  String semester = values[0];
		  if(!semester.equals("Spring")&&!semester.equals("Fall")&&!semester.equals("Summer")) {
			  System.out.println(utility.as_color("[!!!]", "r")+" Invalid semester, try one of Fall, Spring, Summer.");
			  return;
		  }
		  Dictionary slots_dict = get_time_slot_dict(conn);
		  int year = 0;
		  try {
			  year = Integer.parseInt(values[1]);
		  }catch (Exception e){
			  System.out.println("Not a valid year: "+values[1]);
		      return;
		  }
		  
		  PreparedStatement stmt=null;
		  ResultSet res=null;
		  String sql = " WITH enrollments as( "
		  		+ " 			SELECT "
		  		+ " 			sec_id, course_id, semester, year, COALESCE(COUNT(*),0) count "
		  		+ " 			FROM "
		  		+ " 			section NATURAL LEFT JOIN takes "
		  		+ " 			GROUP BY sec_id, course_id, semester, year "
		  		+ " 			) "
		  		+ " "
		  		+ "			SELECT  "
		  		+ "				S.course_id, S.sec_id, C.title, C.credits, S.building, S.room_number, capacity, count, time_slot_id "
		  		+ "			FROM  "
		  		+ "				course C  "
		  		+ "				JOIN  "
		  		+ "				section S  "
		  		+ "					USING (course_id)  "
		  		+ "				JOIN classroom R  "
		  		+ "					ON (R.building=S.building AND R.room_number=S.room_number)  "
		  		+ "				NATURAL JOIN enrollments "
		  		+ "			WHERE semester = ? AND year = ?;";
		try {
			stmt  = conn.prepareStatement(sql);
		    stmt.setString(1, semester);
		    stmt.setInt(2, year);
		    res = stmt.executeQuery();
		    boolean has_course=false;
		    while (res.next()){
		    	has_course=true;
		    	String course_id = res.getString(1); 
		    	String section = res.getString(2); 
		    	String title = res.getString(3); 
		    	String credits = res.getString(4); 
		    	String building = res.getString(5); 
		    	String room = res.getString(6); 
		    	String capacity = res.getString(7); 
		    	String enrollment = res.getString(8); 	
		    	String time_slot = res.getString(9); 
		    	String 	head = "|  Course  |Section|              Title              |Credits|Building|Room|Enrollment|";
		    	System.out.println("_".repeat(head.length()));
		    	System.out.println(head);
		    	// for version 1.4 
		    	System.out.printf("|%10s|%7s|%33s|%7s|%8s|%4s|%6s/%3s|\n", new String[]{course_id,section,title,credits,building,room,enrollment,capacity});
		    	System.out.println("_".repeat(head.length()));
		    	String[] slots = ((String) slots_dict.get(time_slot)).split(",");
		    	System.out.println("| Meeting Time:");
		    	for(int i=0;i<slots.length;i++) {
		    		System.out.println("  >>>>   "+ slots[i] );
		    	}
		    }
		    if (!has_course) {
		    	System.out.println(utility.as_color("[i]", "g")+" There is no course for this time period.");
		    }
		}catch(SQLException e){
			System.out.println("Query course list Failed,SQL error: ");
			e.printStackTrace();
 		}finally {
 			try{
		         if(stmt!=null)
		        	 stmt.close();
		         if(res!=null)
			        res.close();
		      }catch(SQLException e){
		    	 System.out.println("show course list,SQL error: ");
		    	 e.printStackTrace();
		    	 return;
		      }//end finally try
 		}
		
	  }
	  public static void register_student(Connection conn){
		  System.out.println("Register student"+"*".repeat(40));
		  String[] fileds = new String[]{"student ID", "semester", "year", "course ID", "section ID"};
		  Utilities utility = new Utilities();
		  String[] values = utility.menu_selections(fileds);
		  String student_id = values[0];
		  String semester = values[1];
		  //String year= values[2];
		  String course_id= values[3].toUpperCase(); 
		  String sec_id= values[4];
		  int year = 0;
		  try {
			  year = Integer.parseInt(values[2]);
		  }catch (Exception e){
			  System.out.println("Not a valid year: "+values[1]);
		      return;
		  }
		  
		  // check student ID is valid
		  String sql = "SELECT name,dept_name from student where id = ?"; // guaranteed to be 1 or 0 result
		  PreparedStatement statement=null;
		  ResultSet res=null;
 
		  try {
			  statement  = conn.prepareStatement(sql);
		      statement.setString(1, student_id);
		      res = statement.executeQuery();
		      if(!res.next()){
				      System.out.println(utility.as_color("[!!!]", "r")+"  >>>> Student id not exist:"+values[0]);
				      return;
				}
		  }catch (Exception e){
			  System.out.println("Exception when check student id: "+values[0]);
		      return;
		  }
		  //# check that requested course is offered in the specified term(make sure the primary key in section is valid)
		  sql = "select 1 from section where semester = ? and year = ? and course_id = ? and sec_id = ?";
		  try {
			  statement  = conn.prepareStatement(sql);
		      statement.setString(1, semester);
		      statement.setInt(2, year);
		      statement.setString(3, course_id);
		      statement.setString(4, sec_id);
		      res = statement.executeQuery();
		      if(!res.next()){
				      System.out.println(utility.as_color("[!!!]", "r")+"  >>>> Course id not offered in "+semester+" "+ year + " "+ " section "+sec_id );
				      return;
				}
		  }catch (Exception e){
			  System.out.println("Exception when check course is offered or not.");
		      return;
		  }
		  String title;
		  sql = "select title from course where course_id = ?";
		  try {
			  statement  = conn.prepareStatement(sql);
		      statement.setString(1, course_id);
		      res = statement.executeQuery();
		      if(!res.next()){
				      System.out.println(utility.as_color("[!!!]", "r")+"  >>>> Course id not exist."   );
				      return;
				}else {
					title = res.getString(1);
				}
		  }catch (Exception e){
			  System.out.println("Exception when check course is exist.");
		      return;
		  }
		  sql = "(SELECT prereq_id FROM prereq WHERE course_id = ?)"
		  		+ " EXCEPT(SELECT course_id FROM takes WHERE "
		  		+ "id = ? AND grade <'D') ";
		  try {
			  statement  = conn.prepareStatement(sql);
		      statement.setString(1, course_id);
		      statement.setString(2, course_id);
		      res = statement.executeQuery();
		      if(res.next()){
		    	      System.out.println(utility.as_color("[!!!]", "r")+"  >>>> Cannot register student for course "+title+
		    	    		  "("+course_id+"): missing prerequisites." );
				      return;
				} 
		  }catch (Exception e){
			  System.out.println("Exception when check prereq is exist.");
		      return;
		  }
		  //make sure that the student is not already registered the same course
		  sql = "SELECT 1 FROM takes WHERE semester = ? and year = ? and course_id = ? and sec_id = ? and id = ?";
			  try {
				  statement  = conn.prepareStatement(sql);
				  statement.setString(1, semester);
			      statement.setInt(2, year);
			      statement.setString(3, course_id);
			      statement.setString(4, sec_id);
			      statement.setString(5, student_id);
			      res = statement.executeQuery();
			      if(res.next()){
			    	      System.out.println(utility.as_color("[!!!]", "r")+" >>>> Cannot register student for course "+title+
			    	    		  "("+course_id+"): already registered." );
					      return;
					} 
			  }catch (Exception e){
				  System.out.println("Exception when check multiple register is exist.");
			      return;
			  }
			// make sure that the requested section is not already full
			sql =     "	WITH enrollments as( "
					+ " 			SELECT "
					+ " 			sec_id, course_id, semester, year, COALESCE(COUNT(*),0) count "
					+ " 			FROM "
					+ " 			section NATURAL LEFT JOIN takes "
					+ " 			GROUP BY sec_id, course_id, semester, year "
					+ " 			) "
					+ "			SELECT count, capacity  "
					+ "			FROM  "
					+ "			enrollments NATURAL JOIN section S JOIN classroom R  "
					+ "				ON (R.building=S.building AND R.room_number=S.room_number)  "
					+ "			WHERE semester=? AND year=? AND course_id=? AND sec_id=?"; 
			  
			try {
				  statement  = conn.prepareStatement(sql);
				  statement.setString(1, semester);
			      statement.setInt(2, year);
			      statement.setString(3, course_id);
			      statement.setString(4, sec_id);
			      res = statement.executeQuery();
			      
			      res.next();
			      if (res.getString(1).equals(res.getString(2))) {
			    	  System.out.println("Registration not permitted: section "
			    	  		+ sec_id+" of course "+title+" is full.");
			    	  return;
			      }
			      
			  }catch (Exception e){
				  System.out.println("Exception when check capacity.");
				  System.out.println(e);
			      return;
			  }
			
			 //# make sure the student does not have a conflicting registration
			 // since currently different time slot are not conflict, I didn't 
			 // compare their start and end times.
			 // to implement the compare operation highly need features in java version above 1.4
			  sql =   "			(	SELECT time_slot_id "
			  		+ "				FROM section "
			  		+ "				WHERE  semester=? AND year=? AND course_id=? AND sec_id=? "
			  		+ "			) "
			  		+ "			except "
			  		+ "			( "
			  		+ "				SELECT time_slot_id "
			  		+ "				FROM "
			  		+ "					takes NATURAL JOIN section "
			  		+ "				WHERE ID=? AND semester=? AND year=?"
			  		+ "			)";
				  try {
					  statement  = conn.prepareStatement(sql);
					  statement.setString(1, semester);
				      statement.setInt(2, year);
				      statement.setString(3, course_id);
				      statement.setString(4, sec_id);
				      statement.setString(5, student_id);
					  statement.setString(6, semester);
				      statement.setInt(7, year);
				      res = statement.executeQuery();
				      if(!res.next()){
				    	      System.out.println(utility.as_color("[!!!]", "r")+" >>>> Cannot register student for course "+title+
				    	    		  "("+course_id+"): time conflict." );
						      return;
						} 
				  }catch (Exception e){
					  System.out.println("Exception when check time conflict.");
				      return;
				  }
		  //perform registration
			sql = "INSERT INTO takes  (ID, course_id, sec_id,semester,year) VALUES (?, ?, ?, ?,?)";
		    try {
		      statement  = conn.prepareStatement(sql);
		      statement.setString(1, student_id);
		      statement.setString(2, course_id);
		      statement.setString(3, sec_id);
			  statement.setString(4, semester);
		      statement.setInt(5, year);
		      int row_added = statement.executeUpdate();
		      System.out.println(utility.as_color("[SUCCESS]", "g")+" >>>> Register course successful. row added:" + row_added);
		    }catch (SQLException sqle){
		      System.out.println("Could not insert taken into db." + sqle);
		    }catch (Exception  e){
			      System.out.println("Could not insert taken into db.");
			      e.printStackTrace();
			}finally{
				try{
			         if(statement!=null)
			        	 statement.close();
				         if(res!=null)
					        res.close();
			      }catch(SQLException e){
			    	 System.out.println("SQL error: ");
			    	 e.printStackTrace();
			      }//end finally try
			}
		  
	  }
	  public static Dictionary get_time_slot_dict(Connection conn) {
		  Dictionary slots = new Hashtable();
		  PreparedStatement stmt=null;
		  ResultSet res=null;
		  String sql =  "SELECT * from time_slot";
		try {
			stmt = conn.prepareStatement(sql);
			res = stmt.executeQuery();
		    while (res.next()){
		    	String id = res.getString(1); 
		        String day = res.getString(2); 
		        String start_h = res.getString(3); 
		        String start_m = res.getString(4); 
		        String end_h = res.getString(5); 
		        String end_m = res.getString(6); 
		        if (start_h.length()==1) {
		        	start_h = "0"+start_h;
		        }
		        if (end_h.length()==1) {
		        	end_h = "0"+end_h;
		        }
		        if (start_m.length()==1) {
		        	start_m = "0"+start_m;
		        }
		        if (end_m.length()==1) {
		        	end_m = "0"+end_m;
		        }
		        String slot = day+' '+start_h+':'+start_m+'-'+end_h+':'+end_m;
		        if (slots.get(id)==null){
		        	slots.put(id, slot);
		        }else {
		        	String new_slot = slots.get(id)+","+slot; // split later.
		        	slots.put(id, new_slot);
		        }
			}
		}catch(SQLException e){
			System.out.println("Query time slot Failed,SQL error: ");
			e.printStackTrace();
			return slots;
 		}
		try{
	         if(stmt!=null)
	        	 stmt.close();
	         if(res!=null)
		        res.close();
	      }catch(SQLException e){
	    	 System.out.println("Query transcript,SQL error: ");
	    	 e.printStackTrace();
	    	  
	      }//end  try
		return slots;
	  }
}
