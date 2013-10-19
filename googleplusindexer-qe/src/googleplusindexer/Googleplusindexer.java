/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package googleplusindexer;
import java.io.File;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.StringField;
import org.apache.lucene.document.TextField;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.queryparser.classic.ParseException;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TopScoreDocCollector;
import org.apache.lucene.store.Directory;
import org.apache.lucene.util.Version;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.index.IndexWriterConfig.OpenMode;
import org.apache.lucene.store.FSDirectory;
import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import org.apache.lucene.document.DoubleField;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;

public class Googleplusindexer {

private static String indexPath = "index";
static char doublequote = 34; //char "
static char singlequote = 39; //char '

  private static void addDoc(IndexWriter w, String postfile) throws IOException, org.json.simple.parser.ParseException, Exception {
      
	try{
        //Initiates variables
        BufferedReader reader = new BufferedReader(new FileReader(postfile));
        String line = null;
        String text = null;
        double number = 0;
        JSONParser parser = new JSONParser();
	int i=0;
        //Add Document
		while ((line = reader.readLine()) != null) {
                    System.out.println("Adding and classifying post #" + i + " ...");
                    //Read from JSON
                    //System.out.println(line);
                    Document doc = new Document();
                    Object obj = parser.parse(line);
                    JSONObject jsonObject = (JSONObject) obj;
                    //Get data from json and add to document
                    text = (String) jsonObject.get("userName"); 
                    doc.add(new TextField("userName", text, Field.Store.YES));
                    text = (String) jsonObject.get("userID"); 
                    doc.add(new StringField("userID", text, Field.Store.YES));
                    number = (double) jsonObject.get("sentiment_score"); 
                    doc.add(new DoubleField("sentiment_score", number, Field.Store.YES));
                    text = (String) jsonObject.get("postID"); 
                    doc.add(new StringField("postID", text, Field.Store.YES));
                    text = (String) jsonObject.get("cleanContent"); 
                    doc.add(new TextField("cleanContent", text, Field.Store.YES));
                    
                    //Classify post and put it on field : NaiveBayes,IBK,SMO
                    String post = text.replace(doublequote,singlequote);
                    Postclassifier classifier= new Postclassifier();
                    text = classifier.classifypost(post,"model/postNaiveBayes.model");
                    doc.add(new StringField("NaiveBayes", text, Field.Store.YES));
                    text = classifier.classifypost(post,"model/postIBk.model");
                    doc.add(new StringField("IBk", text, Field.Store.YES));
                    text = classifier.classifypost(post,"model/postSMO.model");
                    doc.add(new StringField("SMO", text, Field.Store.YES));
                    w.addDocument(doc);
                    i++;
         }
	} catch (FileNotFoundException e) {
		System.out.println("File not found");
	}
  }
  
  public static void createIndex(boolean update,String postfile) throws IOException, org.json.simple.parser.ParseException, Exception
  {
    System.out.println("Building Indexes...." );
    //Create Analyzer
    Analyzer analyzer = new StandardAnalyzer(Version.LUCENE_40);
	
	//create the index
    Directory index = FSDirectory.open(new File(indexPath));
    IndexWriterConfig config = new IndexWriterConfig(Version.LUCENE_40, analyzer);
    
    if (update) {
	// Create new index
    config.setOpenMode(OpenMode.CREATE_OR_APPEND);
    } else {
    // Add new documents to an existing index:
    config.setOpenMode(OpenMode.CREATE);
    }
	
    IndexWriter w = new IndexWriter(index, config);
    addDoc(w,postfile);
    w.close();
    System.out.println("Build/Update Indexes from " + postfile + " is completed with field:");
    System.out.println("userName,userID,sentiment_score,postID,cleanContent,Label1,Label2,Label3");
    
  }
  
  public static void queryparser(String args) {
	/* HANDLE THE QUERY */
  }
  
  public static void searchIndex(Query q) throws IOException,ParseException {
    //search
    int hitsPerPage = 100;
    Directory index = FSDirectory.open(new File(indexPath));
    IndexReader reader = DirectoryReader.open(index);
    IndexSearcher searcher = new IndexSearcher(reader);
    TopScoreDocCollector collector = TopScoreDocCollector.create(hitsPerPage, true);
    searcher.search(q, collector);
    ScoreDoc[] hits = collector.topDocs().scoreDocs;
    
    //display results
    System.out.println("Found " + hits.length + " hits.");
    for(int i=0;i<hits.length;++i) {
      int docId = hits[i].doc;
      Document d = searcher.doc(docId);
      System.out.println((i + 1) + ". " + d.get("userName") + ", " + d.get("cleanContent")+", "+ d.get("SMO")+", "+ d.get("NaiveBayes")+", "+ d.get("IBk"));
    }
    reader.close();
  }
  
  public static void main(String[] args) throws IOException, ParseException, org.json.simple.parser.ParseException, Exception {
    
    //Build Index
    //createIndex(false,"post/output_randomposts.txt");  
    Analyzer analyzer = new StandardAnalyzer(Version.LUCENE_40);
    
    GoogleSE expan = new GoogleSE();
    
    //Testing simple QUERY with user Name
    String querystr = "mobile";
    String expanded = expan.queryExpansion(querystr);
    Query q = new QueryParser(Version.LUCENE_40, "cleanContent", analyzer).parse(querystr);
    System.out.println("Testing Simple Query\nQuery Result:\n");
    //Search Index
    searchIndex(q);

    System.out.println("\n new expanded query: "+expanded);
    // Try new query
    q = new QueryParser(Version.LUCENE_40, "cleanContent", analyzer).parse(expanded);
    searchIndex(q);
    
  }
}
