/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

package googlese;
import java.io.FileInputStream;
import java.io.IOException;
import java.util.HashMap;
import java.util.logging.Level;
import java.util.logging.Logger;
import org.apache.lucene.wordnet.SynonymMap;
/**
 *
 * @author Marcelo Almeida
 */
public class GoogleSE {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        HashMap<String, String[]> map = null;
        String query = "how to use a screwdriver";
        String result = queryExpansion(query);
        System.out.println("Original query: " + query);
        System.out.println("Expanded query: " + result);
    }
    
    public static String queryExpansion(String query){
        String path = "src/googlese/";
        String result = query;
        String[] newQuery = query.split("\\s+");
        SynonymMap synMap = null;
        try {
            synMap = new SynonymMap(new FileInputStream(path + "wn_s.pl"));
        } catch (IOException ex) {
            Logger.getLogger(GoogleSE.class.getName()).log(Level.SEVERE, null, ex);
        }
        for (int i = 0; i < newQuery.length; i++) {
            String[] synonyms = synMap.getSynonyms(newQuery[i]);
            for (int j = 0; j < synonyms.length; j++){
                result += " " + synonyms[j];
            }
        }
        return result;
    }
}
