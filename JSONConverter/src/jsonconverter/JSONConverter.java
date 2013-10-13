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
   public static void main(String[] args) throws FileNotFoundException, IOException, ParseException {
    
	  try{
            BufferedReader reader = new BufferedReader(new FileReader("output.txt"));
            String line = null;
            String name = null;
            long replyCount = 0;
            String postID = null;
            String userID = null;
            String content = null;
            char doublequote = 34; //char "
			JSONParser parser = new JSONParser();
			FileWriter writer = new FileWriter("output.csv");
			
            //Write CSV file header
            writer.append("UserName,replyCount,postID,userID,content\n");
            FileWriter arff = new FileWriter("output.arff");
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
                            replyCount = (long) jsonObject.get("replyCount");
                            postID = (String) jsonObject.get("postID");
                            userID = (String) jsonObject.get("userID");
                            content = (String) jsonObject.get("content");
                            
                            //Write to CSV
                            writer.append(name);
                            writer.append(",");
                            writer.append(String.valueOf(replyCount));
                            writer.append(",");
                            writer.append(postID);
                            writer.append(",");
                            writer.append(userID);
                            writer.append(",");
                            writer.append(content);
                            writer.append("\n");
                                                        
                            //Write ARFF files
                            arff.append(doublequote);
                            arff.append(name);
                            arff.append(doublequote);
                            arff.append(",");
                            arff.append(String.valueOf(replyCount));
                            arff.append(",");
                            arff.append(postID);
                            arff.append(",");
                            arff.append(userID);
                            arff.append(",");
                            arff.append(doublequote);
                            arff.append(content);
                            arff.append(doublequote);
                            arff.append("\n");
                        }
						
            writer.flush();
            writer.close();
            arff.flush();
            arff.close();

	} catch (FileNotFoundException e) {
        }
}
    
}
