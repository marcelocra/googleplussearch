/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package jsonconverter;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;
/**
 *
 * @author Chris
 */
public class JSONConverter {

    /**
     * @param args the command line arguments
     */
    static FileWriter newarff;
    static char doublequote = 34; //char "
    static char singlequote = 39; //char '
   public static void makearff(String inputfile,String outputfile) throws IOException, ParseException{
   /* Build .arff files from JSON */
       
       	  try{
            //Initiates variables
            BufferedReader reader = new BufferedReader(new FileReader(inputfile));
            String line = null;
            String name = null;
            long replyCount = 0;
            String postID = null;
            String userID = null;
            String content = null;
            JSONParser parser = new JSONParser();
            FileWriter arff = new FileWriter(outputfile);
            
            //Write arff file header
            arff.append("@relation output\n");
            arff.append("@attribute username string\n");
            arff.append("@attribute replycount string\n");
            arff.append("@attribute postID string\n");
            arff.append("@attribute userID string\n");
            arff.append("@attribute comment string\n");
            arff.append("@data\n"); 
                        while ((line = reader.readLine()) != null) {
                                //Read from JSON
                                Object obj = parser.parse(line);
                                JSONObject jsonObject = (JSONObject) obj;
                                name = (String) jsonObject.get("userName");
//                                replyCount = (long) jsonObject.get("replyCount");
                                postID = (String) jsonObject.get("postID");
                                userID = (String) jsonObject.get("userID");
                                content = (String) jsonObject.get("content"); 
                                
                                //Write ARFF files
                                 arff.append(doublequote + name + doublequote + ",");
                                 arff.append(String.valueOf(replyCount) + ",");
                                 arff.append(postID + ",");
                                 arff.append(userID + ",");
                                 arff.append(doublequote + content + doublequote + "\n");
                        }
            // Close file
            arff.flush();
            arff.close();

	} catch (FileNotFoundException e) {
        }
   
   }
      public static void insertdata(String inputfile,String classname) throws IOException, ParseException{
   /* Build .arff files from JSON */
       
       	  try{
            //Initiates variables
            BufferedReader reader = new BufferedReader(new FileReader(inputfile));
            String line = null;
            String content = null;
            JSONParser parser = new JSONParser();
  
            //Write arff file header
            
                        while ((line = reader.readLine()) != null) {
                                //Read from JSON
                               // System.out.println(line);
                                Object obj = parser.parse(line);
                                JSONObject jsonObject = (JSONObject) obj;
                                content = (String) jsonObject.get("cleanContent"); 
                                String cleancontent = content.replace(doublequote,singlequote); 
                                //Write ARFF files
                                newarff.append(classname + ",");
                                newarff.append(doublequote + cleancontent + doublequote + "\n");
                                
                                
                                 
                        }

	} catch (FileNotFoundException e) {
            System.out.println("Exception at input");
        }
   
   }
      
   public static void Initarff() throws IOException{
       //* Making new arff file ready for data
        // Create newarff for all post
        newarff = new FileWriter("weka/googlepost.arff");
        // Create New Header
        newarff.append("@relation post\n\n");
        newarff.append("@attribute @@class@@ {technology, automotive}\n");
        newarff.append("@attribute comment string\n\n");
        newarff.append("@data\n"); 
    }
   
   public static void Closearff() throws IOException{
        // Close file
        newarff.flush();
        newarff.close();
   }
   
   public static void writearff() throws IOException, ParseException {
           Initarff();
           insertdata("post/training.txt","technology");
           insertdata("post/output_audi_posts.txt","automotive");
           insertdata("post/output_bmw_posts.txt","automotive");
           insertdata("post/output_driving_posts.txt","automotive");
           insertdata("post/output_racing_posts.txt","automotive");
           Closearff();
   }
   public static void main(String[] args) throws FileNotFoundException, IOException, ParseException {
    //makearff("output_audi_posts.txt","output_audi_posts.arff");
       writearff();
    }

    
}

