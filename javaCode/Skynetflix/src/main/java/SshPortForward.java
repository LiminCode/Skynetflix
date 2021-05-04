
import com.jcraft.jsch.*;


public class SshPortForward{
	String user="lwang24";
    String host="rocco.cs.wm.edu";
    String password = "1rujiwang";
    Session session;
    public void StartSSH(){

	    try{
	      JSch jsch=new JSch();
	
	      
	      int port = 11536;
	      session=jsch.getSession(user, host, port);
	      session.setPassword(password);
	      session.setConfig("StrictHostKeyChecking", "no");
	 
	
	      session.connect();
	      System.out.println("SSH server connected: "+session.getServerVersion());
	      
	      int assinged_port = session.setPortForwardingL(5432, "localhost", 5432);//port forward
	      
	      System.out.println("SSH Port Forward established:"+assinged_port);
	       
	 
	       
	    }
	    catch(Exception e){
	    	System.out.println("Port forward failed:");
	    	System.out.println(e);
	    	return;
	    }
    }
    public void CloseSSH(){

	    try{
	      session.disconnect();       
	    }
	    catch(Exception e){
	    	System.out.println(e);
	    }
	    System.out.println("Port forward closed.");
    }
}