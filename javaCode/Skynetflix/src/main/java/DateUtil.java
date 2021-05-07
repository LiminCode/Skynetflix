import java.sql.Timestamp;
import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Date;
public class DateUtil {
    /**
     * new Timestamp(s)
     * @return s
     */
    public Timestamp newStampTime(){
        long s=System.currentTimeMillis();
        return new Timestamp(s);
    }
    /**
     * timeStamp to String
     * @return
     */
    public String timeStampToString(){
        SimpleDateFormat df = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");//no mill seconds 
        Timestamp now = new Timestamp(System.currentTimeMillis());//get current system time
        String str = df.format(now);
        return str;
    }
    /**
     * String to timestamp
     * @return
     */
    public Timestamp StringTotimeStamp(){
        SimpleDateFormat df = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
        String time = df.format(new Date()); 
        Timestamp ts = Timestamp.valueOf(time);
        return ts;
    }
    public Date myStringTotimeStamp(String dateString){
        int length=dateString.length();
        if(length>10){
            DateFormat df = new SimpleDateFormat("yyyy-MM-dd");
            Date day=new Date();
            try {
                day = df.parse(dateString);
                //String ts=df.format(today);
            } catch (ParseException e) {
                e.printStackTrace();
            }
            return day;
        }else {
            DateFormat df = new SimpleDateFormat("yyyy-MM-dd");
            Date day=new Date();
            try {
                day = df.parse(dateString);
                //String ts=df.format(today);
            } catch (ParseException e) {
                e.printStackTrace();
            }
            return day;
        }
        
    }
    
    /**
     * @param 返回java.sql.Date格式的
     * */
    public  java.sql.Date strToDate(String strDate) {
        String str = strDate;
        SimpleDateFormat format = new SimpleDateFormat("yyyy-MM-dd");
        java.util.Date d = null;
        try {
            d = format.parse(str);
        } catch (Exception e) {
            e.printStackTrace();
        }
        java.sql.Date date = new java.sql.Date(d.getTime());
        return date;
    }
    /**
           * String to timestamp
           * String "2016-5-25" to Timestamp 
           * @return
           */
          public Timestamp StringTotimeStamp(String dateString){
                  SimpleDateFormat df = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
                  StringBuffer ds=new StringBuffer(dateString);
                  if(dateString.length()>10){
                          Timestamp ts = Timestamp.valueOf(dateString);
                          return ts;
                  }else{
                          ds.append(" 00:00:00");
                          Timestamp ts = Timestamp.valueOf(ds.toString());
                          return ts;
                  }
          }
    /**
     * get current time string 
     * eg:2016-10-11 16:57:52
     **/
    public String formateDateString(){
        SimpleDateFormat format = new SimpleDateFormat("yyyy-MM-dd H:m:s");
        String dateString=format.format(new Date());
        return dateString;
    }
    /**
     * compare
     */
    public boolean compareTime(String t1){
        if(t1.length()<=10){
            t1=t1+" 23:59:59";
        }
        Date currentTime = new Date(); 
                SimpleDateFormat formatter = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
                String nowtime = formatter.format(currentTime);
                Calendar now = Calendar.getInstance();
                Calendar c1 = Calendar.getInstance();
                //String t1 = "2016-02-29 00:30:00";
                try {
                now.setTime(formatter.parse(nowtime));
                c1.setTime(formatter.parse(t1));
                } catch (ParseException e) {
                e.printStackTrace();
                }
                int result1 = now.compareTo(c1);   
                System.out.println("result:"+result1);
                if(result1>0){
                    return false;
                }else{
                    return true;
                }           
    }      
    
}
