/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package clusteringapp;

/**
 *
 * @author Joelian Samuel
 */
import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.MalformedURLException;
import java.net.URL;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Map;
import java.util.Set;
import java.util.TreeMap;
import java.util.logging.Level;
import java.util.logging.Logger;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import opennlp.tools.postag.POSModel;
import opennlp.tools.postag.POSTaggerME;
import opennlp.tools.tokenize.TokenizerME;
import opennlp.tools.tokenize.TokenizerModel;
import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TopScoreDocCollector;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.FSDirectory;
import org.apache.lucene.util.Version;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;
import weka.attributeSelection.ASEvaluation;
import weka.classifiers.Evaluation;
import weka.classifiers.lazy.IBk;
import weka.classifiers.meta.FilteredClassifier;
import weka.clusterers.Clusterer;
import weka.clusterers.FilteredClusterer;
import weka.clusterers.SimpleKMeans;
import weka.clusterers.ClusterEvaluation;
import weka.core.Attribute;
import weka.core.Capabilities;
import weka.core.FastVector;
import weka.core.Instance;
import weka.core.Instances;
import weka.core.SelectedTag;
import weka.core.Tag;
import weka.core.converters.ConverterUtils;
import weka.core.converters.ConverterUtils.DataSource;
import weka.core.tokenizers.AlphabeticTokenizer;
import weka.core.tokenizers.Tokenizer;
import weka.filters.Filter;
import weka.filters.MultiFilter;
import weka.filters.supervised.attribute.AttributeSelection;
import weka.filters.unsupervised.attribute.ClassAssigner;
import weka.filters.unsupervised.attribute.StringToNominal;
import weka.filters.unsupervised.attribute.StringToWordVector;

public class ClusteringApp {

    /**
     * @param args the command line arguments
     */
    private Map<String,String> listTag ;
    private String[] googleAPIKey;
    private String[] userProfile;
    private int[] counterTag;
    private static String indexPath = "indexUser";
    private static String modelPath = "FINAL_MODEL_RANDOM_TREE.model";
    
    public ClusteringApp()
    {
        userProfile = new String[5];
        googleAPIKey = new String[5];
        googleAPIKey[0] = "AIzaSyDZFITATgwsWzuw4JpaXbWK0BV6Yd292mg";
        googleAPIKey[1] = "AIzaSyBS5eCOxTHbB7AK4ypduCpqiW-RyQIaG3Y";
        googleAPIKey[2] = "AIzaSyB24XShYV2CK7K5auqUEWcOYLi6nr_Au8A";
        googleAPIKey[3] = "AIzaSyBF3kid2dye5d0wy54r7rLFeCjeNzNfJqk";
        googleAPIKey[4] = "AIzaSyA6_A7f_G3dqZyLoXmydVvGo51AgRhH-fw";
        listTag = new TreeMap<String, String>();
        listTag.put("amazing", "3");
        listTag.put("business", "4");
        listTag.put("car", "5");
        listTag.put("cars", "6");
        listTag.put("community", "7");
        listTag.put("company", "8");
        listTag.put("enthusiast", "9");
        listTag.put("experience", "10");
        listTag.put("geek", "11");
        listTag.put("marketing", "12");
        listTag.put("online", "13");
        listTag.put("sales", "14");
        listTag.put("staff", "15");
        listTag.put("tech", "16");
        listTag.put("time", "17");
        listTag.put("vehicles", "18");
        listTag.put("web", "19");
        listTag.put("world", "20");
        listTag.put("apple", "21");
        listTag.put("articles", "22");
        listTag.put("blog", "23");
        listTag.put("blogger", "24");
        listTag.put("church", "25");
        listTag.put("circle", "26");
        listTag.put("circles", "27");
        listTag.put("college", "28");
        listTag.put("computer", "29");
        listTag.put("degree", "30");
        listTag.put("developer", "31");
        listTag.put("development", "32");
        listTag.put("engineer", "33");
        listTag.put("expert", "34");
        listTag.put("food", "35");
        listTag.put("founder", "36");
        listTag.put("games", "37");
        listTag.put("google", "38");
        listTag.put("guy", "39");
        listTag.put("information", "40");
        listTag.put("interests", "41");
        listTag.put("internet", "42");
        listTag.put("law", "43");
        listTag.put("life", "44");
        listTag.put("love", "45");
        listTag.put("lover", "46");
        listTag.put("loves", "47");
        listTag.put("man", "48");
        listTag.put("manager", "49");
        listTag.put("media", "50");
        listTag.put("news", "51");
        listTag.put("owner", "52");
        listTag.put("passion", "53");
        listTag.put("photography", "54");
        listTag.put("politics", "55");
        listTag.put("school", "56");
        listTag.put("science", "57");
        listTag.put("seo", "58");
        listTag.put("services", "59");
        listTag.put("software", "60");
        listTag.put("solutions", "61");
        listTag.put("student", "62");
        listTag.put("team", "63");
        listTag.put("technology", "64");
        listTag.put("university", "65");
        listTag.put("website", "66");
        listTag.put("work", "67");
        listTag.put("writer", "68");
        listTag.put("apache", "69");
        listTag.put("consultant", "70");
        listTag.put("designer", "71");
        listTag.put("family", "72");
        listTag.put("fashion", "73");
        listTag.put("mom", "74");
        listTag.put("rugby", "75");
        listTag.put("valley", "76");
        listTag.put("wife", "77");
        listTag.put("analyst", "78");
        listTag.put("specialist", "79");
        
        counterTag = new int[77];
        for (int i =0 ; i < 77 ; i++)
        {
            counterTag[i] = 0;
        }
    }
    
    public boolean getUserProfile(String googleID) throws MalformedURLException, IOException, ParseException
    {
        boolean notfound = true;
        int i=0;
        JSONParser jP = new JSONParser();
        while(notfound)
        {
            if (i>4)
            {
                notfound = false;      
            }
            URL url = new URL("https://www.googleapis.com/plus/v1/people/"+googleID+"?key="+googleAPIKey[i]);
            InputStream is = url.openConnection().getInputStream();
            if (is != null)
            {
                BufferedReader reader = new BufferedReader(new InputStreamReader(is));
                String jsonString = "";
                String line = null;
                while((line = reader.readLine()) != null)
                {
                    //System.out.println(line);
                    jsonString = jsonString + line;
                }
                Object jB = jP.parse(jsonString);
                JSONObject jO = (JSONObject) jB;
                notfound = false;
                userProfile[0] = (String)jO.get("id");
                userProfile[1] = (String)jO.get("displayName");
                userProfile[2] = (String)jO.get("gender");
                userProfile[3] = (String)jO.get("relationshipstatus");
                String tagline = (String)jO.get("aboutMe");
                
                tagline = tagline.replaceAll("\"", "");
                tagline = tagline.replaceAll("\'", "");
                String tagline1 = "";
                String[] listtagline;
                listtagline = tagline.split(" ");
                String urlPattern = "(http:|https:)?(//)?[a-zA-Z]+[.]{1}[a-zA-Z]+";
                Pattern p = Pattern.compile(urlPattern,Pattern.CASE_INSENSITIVE);
                //Matcher m = p.matcher(aboutme1);
                int k=0;
                while (k< listtagline.length) {
                    //System.out.println(m);
                    //System.out.println("-----------------------");
                    Matcher m = p.matcher(listtagline[k]);
                    if(m.find())
                    {
                        //System.out.println(listabout[i]);
                        //System.out.println(listtagline[i]);
                    }
                    else
                    {
                        tagline1 = tagline1 + " " + listtagline[k];                                        
                    }
                    k++;
                }
                userProfile[4] = tagline1;
            }
            i++;
        }
        if (notfound)
        {
            return false;
        }
        else
        {
            return true;
        }
    }
    public void setcounterTag(String[] tagline)
    {
        int length = tagline.length;
        for (int i = 0 ; i < length; i++)
        {
            if(listTag.containsKey(tagline[i]))
            {
                int idx = Integer.parseInt(listTag.get(tagline[i]));
                counterTag[idx-3] = counterTag[idx-3] + 1;
               System.out.println(tagline[i]+": "+counterTag[idx-3]);
            }
        }
    }
    public String filteredCluster(String model,String genderstr, String relationstr, String tagline, String affrfile) throws Exception{
      
        String[] listtag = tagline.split(" ");
        setcounterTag(listtag);
       
        FastVector classVal = new FastVector(15);
        classVal.addElement("cluster0");
        classVal.addElement("cluster1");
        classVal.addElement("cluster2");
        classVal.addElement("cluster3");
        classVal.addElement("cluster4");
        classVal.addElement("cluster5");
        classVal.addElement("cluster6");
        classVal.addElement("cluster7");
        classVal.addElement("cluster8");
        classVal.addElement("cluster9");
        classVal.addElement("cluster10");
        classVal.addElement("cluster11");
        classVal.addElement("cluster12");
        classVal.addElement("cluster13");
        classVal.addElement("cluster14");
        
        FastVector genderVal = new FastVector(4);
        genderVal.addElement("male");
        genderVal.addElement("female");
        genderVal.addElement("other");
        genderVal.addElement("");
        
        FastVector relVal = new FastVector(10);
        relVal.addElement("");
        relVal.addElement("single");
        relVal.addElement("in_a_relationship");
        relVal.addElement("married");
        relVal.addElement("engaged");
        relVal.addElement("its_complicated");
        relVal.addElement("open_relationship");
        relVal.addElement("widowed");
        relVal.addElement("in_domestic_partnership");
        relVal.addElement("in_civil_union");
        
        Attribute ClassAttribute = new Attribute("Cluster",classVal);
        
        //attribute other feature
        Attribute gender = new Attribute("gender", genderVal);
        Attribute relationshipstatus = new Attribute("relationshipstatus",relVal);
        Attribute instance = new Attribute("Instance_number",(FastVector) null);
        Attribute id = new Attribute("id",(FastVector) null);
        Attribute name = new Attribute("name",(FastVector) null);
        Attribute placeslived = new Attribute("placeslived",(FastVector) null);
        Attribute organizations = new Attribute("@@organizations@@",(FastVector) null);
        
        //attribute tagline
        Attribute amazing = new Attribute("amazing", (FastVector) null);
        Attribute analyst = new Attribute("analyst", (FastVector) null);
        Attribute apache = new Attribute("apache", (FastVector) null);
        Attribute apple = new Attribute("apple", (FastVector) null);
        Attribute articles = new Attribute("articles", (FastVector) null);
        Attribute blog = new Attribute("blog", (FastVector) null);
        Attribute blogger = new Attribute("blogger", (FastVector) null);
        Attribute business = new Attribute("business", (FastVector) null);
        Attribute car = new Attribute("car", (FastVector) null);
        Attribute cars = new Attribute("cars", (FastVector) null);
        Attribute church = new Attribute("church", (FastVector) null);
        Attribute circle = new Attribute("circle", (FastVector) null);
        Attribute circles = new Attribute("circles", (FastVector) null);
        Attribute college = new Attribute("college", (FastVector) null);
        Attribute community = new Attribute("community", (FastVector) null);
        Attribute company = new Attribute("company", (FastVector) null);
        Attribute computer = new Attribute("computer", (FastVector) null);
        Attribute consultant = new Attribute("consultant", (FastVector) null);
        Attribute degree = new Attribute("degree", (FastVector) null);
        Attribute designer = new Attribute("designer", (FastVector) null);
        Attribute developer = new Attribute("developer", (FastVector) null);
        Attribute development = new Attribute("development", (FastVector) null);
        Attribute engineer = new Attribute("engineer", (FastVector) null);
        Attribute enthusiast = new Attribute("enthusiast", (FastVector) null);
        Attribute experience = new Attribute("experience", (FastVector) null);
        Attribute expert = new Attribute("expert", (FastVector) null);
        Attribute family = new Attribute("family", (FastVector) null);
        Attribute fashion = new Attribute("fashion", (FastVector) null);
        Attribute food = new Attribute("food", (FastVector) null);
        Attribute founder = new Attribute("founder", (FastVector) null);
        Attribute games = new Attribute("games", (FastVector) null);
        Attribute geek = new Attribute("geek", (FastVector) null);
        Attribute google = new Attribute("google", (FastVector) null);
        Attribute guy = new Attribute("guy", (FastVector) null);
        Attribute information = new Attribute("information", (FastVector) null);
        Attribute interests = new Attribute("interests", (FastVector) null);
        Attribute internet = new Attribute("internet", (FastVector) null);
        Attribute law = new Attribute("law", (FastVector) null);
        Attribute life = new Attribute("life", (FastVector) null);
        Attribute love = new Attribute("love", (FastVector) null);
        Attribute lover = new Attribute("lover", (FastVector) null);
        Attribute loves = new Attribute("loves", (FastVector) null);
        Attribute man = new Attribute("man", (FastVector) null);
        Attribute manager = new Attribute("manager", (FastVector) null);
        Attribute marketing = new Attribute("marketing", (FastVector) null);
        Attribute media = new Attribute("media", (FastVector) null);
        Attribute mom = new Attribute("mom", (FastVector) null);
        Attribute news = new Attribute("news", (FastVector) null);
        Attribute online = new Attribute("online", (FastVector) null);
        Attribute owner = new Attribute("owner", (FastVector) null);
        Attribute passion = new Attribute("passion", (FastVector) null);
        Attribute photography = new Attribute("photography", (FastVector) null);
        Attribute politics = new Attribute("politics", (FastVector) null);
        Attribute rugby = new Attribute("rugby", (FastVector) null);
        Attribute sales = new Attribute("sales", (FastVector) null);
        Attribute school = new Attribute("school", (FastVector) null);
        Attribute science = new Attribute("science", (FastVector) null);
        Attribute seo = new Attribute("seo", (FastVector) null);
        Attribute services = new Attribute("services", (FastVector) null);
        Attribute software = new Attribute("software", (FastVector) null);
        Attribute solutions = new Attribute("solutions", (FastVector) null);
        Attribute specialist = new Attribute("specialist", (FastVector) null);
        Attribute staff = new Attribute("staff", (FastVector) null);
        Attribute student = new Attribute("student", (FastVector) null);
        Attribute team = new Attribute("team", (FastVector) null);
        Attribute tech = new Attribute("tech", (FastVector) null);
        Attribute technology = new Attribute("technology", (FastVector) null);
        Attribute time = new Attribute("time", (FastVector) null);
        Attribute university = new Attribute("university", (FastVector) null);
        Attribute valley = new Attribute("valley", (FastVector) null);
        Attribute vehicles = new Attribute("vehicles", (FastVector) null);
        Attribute web = new Attribute("web", (FastVector) null);
        Attribute website = new Attribute("website", (FastVector) null);
        Attribute wife = new Attribute("wife", (FastVector) null);
        Attribute work = new Attribute("work", (FastVector) null);
        Attribute world = new Attribute("world", (FastVector) null);
        Attribute writer = new Attribute("writer", (FastVector) null);

        
		
        //Declare the feature vector
        FastVector FvAttributes = new FastVector(85);
        FvAttributes.addElement(instance);
        FvAttributes.addElement(id);
        FvAttributes.addElement(name);
        FvAttributes.addElement(gender);
        FvAttributes.addElement(relationshipstatus);
        FvAttributes.addElement(placeslived);
        FvAttributes.addElement(organizations);
        FvAttributes.addElement(amazing);
        FvAttributes.addElement(business);
        FvAttributes.addElement(car);
        FvAttributes.addElement(cars);
        FvAttributes.addElement(community);
        FvAttributes.addElement(company);
        FvAttributes.addElement(enthusiast);
        FvAttributes.addElement(experience);
        FvAttributes.addElement(geek);
        FvAttributes.addElement(marketing);
        FvAttributes.addElement(online);
        FvAttributes.addElement(sales);
        FvAttributes.addElement(staff);
        FvAttributes.addElement(tech);
        FvAttributes.addElement(time);
        FvAttributes.addElement(vehicles);
        FvAttributes.addElement(web);
        FvAttributes.addElement(world);
        FvAttributes.addElement(apple);
        FvAttributes.addElement(articles);
        FvAttributes.addElement(blog);
        FvAttributes.addElement(blogger);
        FvAttributes.addElement(church);
        FvAttributes.addElement(circle);
        FvAttributes.addElement(circles);
        FvAttributes.addElement(college);
        FvAttributes.addElement(computer);
        FvAttributes.addElement(degree);
        FvAttributes.addElement(developer);
        FvAttributes.addElement(development);
        FvAttributes.addElement(engineer);
        FvAttributes.addElement(expert);
        FvAttributes.addElement(food);
        FvAttributes.addElement(founder);
        FvAttributes.addElement(games);
        FvAttributes.addElement(google);
        FvAttributes.addElement(guy);
        FvAttributes.addElement(information);
        FvAttributes.addElement(interests);
        FvAttributes.addElement(internet);
        FvAttributes.addElement(law);
        FvAttributes.addElement(life);
        FvAttributes.addElement(love);
        FvAttributes.addElement(lover);
        FvAttributes.addElement(loves);
        FvAttributes.addElement(man);
        FvAttributes.addElement(manager);
        FvAttributes.addElement(media);
        FvAttributes.addElement(news);
        FvAttributes.addElement(owner);
        FvAttributes.addElement(passion);
        FvAttributes.addElement(photography);
        FvAttributes.addElement(politics);
        FvAttributes.addElement(school);
        FvAttributes.addElement(science);
        FvAttributes.addElement(seo);
        FvAttributes.addElement(services);
        FvAttributes.addElement(software);
        FvAttributes.addElement(solutions);
        FvAttributes.addElement(student);
        FvAttributes.addElement(team);
        FvAttributes.addElement(technology);
        FvAttributes.addElement(university);
        FvAttributes.addElement(website);
        FvAttributes.addElement(work);
        FvAttributes.addElement(writer);
        FvAttributes.addElement(apache);
        FvAttributes.addElement(consultant);
        FvAttributes.addElement(designer);
        FvAttributes.addElement(family);
        FvAttributes.addElement(fashion);
        FvAttributes.addElement(mom);
        FvAttributes.addElement(rugby);
        FvAttributes.addElement(valley);
        FvAttributes.addElement(wife);
        FvAttributes.addElement(analyst);
        FvAttributes.addElement(specialist);

        FvAttributes.addElement(ClassAttribute);

        //Create an empty set
        Instances inputinstances = new Instances("relation",FvAttributes,1);
        //Set Class Index
        inputinstances.setClassIndex(84);

        //Create and add instance
        Instance newinstance = new Instance(inputinstances.numAttributes());
        System.out.println(genderstr);
        System.out.println(relationstr);
        newinstance.setValue(instance,"0");
        newinstance.setValue(id,"0");
        newinstance.setValue(name,"xxx");
        newinstance.setValue(gender,genderstr);
        newinstance.setValue(relationshipstatus,relationstr);
        newinstance.setValue(placeslived,"xxx");
        newinstance.setValue(organizations,"xxx");
        newinstance.setValue(amazing, counterTag[0]);
        newinstance.setValue(business, counterTag[1]);
        newinstance.setValue(car, counterTag[2]);
        newinstance.setValue(cars, counterTag[3]);
        newinstance.setValue(community, counterTag[4]);
        newinstance.setValue(company, counterTag[5]);
        newinstance.setValue(enthusiast, counterTag[6]);
        newinstance.setValue(experience, counterTag[7]);
        newinstance.setValue(geek, counterTag[8]);
        newinstance.setValue(marketing, counterTag[9]);
        newinstance.setValue(online, counterTag[10]);
        newinstance.setValue(sales, counterTag[11]);
        newinstance.setValue(staff, counterTag[12]);
        newinstance.setValue(tech, counterTag[13]);
        newinstance.setValue(time, counterTag[14]);
        newinstance.setValue(vehicles, counterTag[15]);
        newinstance.setValue(web, counterTag[16]);
        newinstance.setValue(world, counterTag[17]);
        newinstance.setValue(apple, counterTag[18]);
        newinstance.setValue(articles, counterTag[19]);
        newinstance.setValue(blog, counterTag[20]);
        newinstance.setValue(blogger, counterTag[21]);
        newinstance.setValue(church, counterTag[22]);
        newinstance.setValue(circle, counterTag[23]);
        newinstance.setValue(circles, counterTag[24]);
        newinstance.setValue(college, counterTag[25]);
        newinstance.setValue(computer, counterTag[26]);
        newinstance.setValue(degree, counterTag[27]);
        newinstance.setValue(developer, counterTag[28]);
        newinstance.setValue(development, counterTag[29]);
        newinstance.setValue(engineer, counterTag[30]);
        newinstance.setValue(expert, counterTag[31]);
        newinstance.setValue(food, counterTag[32]);
        newinstance.setValue(founder, counterTag[33]);
        newinstance.setValue(games, counterTag[34]);
        newinstance.setValue(google, counterTag[35]);
        newinstance.setValue(guy, counterTag[36]);
        newinstance.setValue(information, counterTag[37]);
        newinstance.setValue(interests, counterTag[38]);
        newinstance.setValue(internet, counterTag[39]);
        newinstance.setValue(law, counterTag[40]);
        newinstance.setValue(life, counterTag[41]);
        newinstance.setValue(love, counterTag[42]);
        newinstance.setValue(lover, counterTag[43]);
        newinstance.setValue(loves, counterTag[44]);
        newinstance.setValue(man, counterTag[45]);
        newinstance.setValue(manager, counterTag[46]);
        newinstance.setValue(media, counterTag[47]);
        newinstance.setValue(news, counterTag[48]);
        newinstance.setValue(owner, counterTag[49]);
        newinstance.setValue(passion, counterTag[50]);
        newinstance.setValue(photography, counterTag[51]);
        newinstance.setValue(politics, counterTag[52]);
        newinstance.setValue(school, counterTag[53]);
        newinstance.setValue(science, counterTag[54]);
        newinstance.setValue(seo, counterTag[55]);
        newinstance.setValue(services, counterTag[56]);
        newinstance.setValue(software, counterTag[57]);
        newinstance.setValue(solutions, counterTag[58]);
        newinstance.setValue(student, counterTag[59]);
        newinstance.setValue(team, counterTag[60]);
        newinstance.setValue(technology, counterTag[61]);
        newinstance.setValue(university, counterTag[62]);
        newinstance.setValue(website, counterTag[63]);
        newinstance.setValue(work, counterTag[64]);
        newinstance.setValue(writer, counterTag[65]);
        newinstance.setValue(apache, counterTag[66]);
        newinstance.setValue(consultant, counterTag[67]);
        newinstance.setValue(designer, counterTag[68]);
        newinstance.setValue(family, counterTag[69]);
        newinstance.setValue(fashion, counterTag[70]);
        newinstance.setValue(mom, counterTag[71]);
        newinstance.setValue(rugby, counterTag[72]);
        newinstance.setValue(valley, counterTag[73]);
        newinstance.setValue(wife, counterTag[74]);
        newinstance.setValue(analyst, counterTag[75]);
        newinstance.setValue(specialist, counterTag[76]);


        
        //String line = "";
        //Path newfile = Paths.get("example.arff");
        
        //inputinstances.add(newinstance);
        
        //System.out.println(inputinstances.toString());
        //Instance last = inputinstances.lastInstance();

        //System.out.println(newinstance.toString());
        // Load model;
        FilteredClassifier classifier = (FilteredClassifier) weka.core.SerializationHelper.read(model);
        
        //Instance t = newdata.firstInstance();
        newinstance.setDataset(inputinstances);
        double result = classifier.classifyInstance(newinstance);
        
        System.out.println("Cluster:"+inputinstances.classAttribute().value((int) result));
                
        //ClusterEvaluation eval = new ClusterEvaluation();
        //Instance t = newdata.firstInstance();
        
        //Evaluate new data set
        //eval.setClusterer(c); //Test data from cluster kmeans              
        //eval.evaluateClusterer(newdata); //Cluster the new set
       
        //double[] result = eval.getClusterAssignments();
        //System.out.println(result[0]);
        //System.out.println("cluster:"+result);
        //return inputinstances.classAttribute().value((int) result);     
        
        return inputinstances.classAttribute().value((int) result);
        
            //Declare Attributes
               
    }
    
    public String[] getTokenTagline(String tagline)
    {
        InputStream modelIn = null;
        TokenizerModel model = null;
        try
        {
            modelIn = new FileInputStream("en-token.bin");
            model = new TokenizerModel(modelIn);
        }
        catch (IOException e){}
        finally
        {
            if(modelIn != null)
            {
                try 
                {
                    modelIn.close();
                }
                catch(IOException e){}
            }
        }
        tagline = tagline.toLowerCase();
        TokenizerME tokenizer = new TokenizerME(model);
        String[] tokens = tokenizer.tokenize(tagline);
        return tokens;
    }
    public String getNounTagline(String tagline)
    {
        String[] token = getTokenTagline(tagline);
        String cleanTag = "";
        InputStream modelIn = null;
        POSModel model = null;
        try 
        {
            modelIn = new FileInputStream("en-pos-maxent.bin");
            model = new POSModel(modelIn);
        }
        catch(IOException e)
        {
        }
        finally
        {
            if(modelIn != null)
            {
                try 
                {
                    modelIn.close();
                }
                catch(IOException e){}
            }
                
        }
        POSTaggerME tagger = new POSTaggerME(model);
        String[] tag = tagger.tag(token);
        for (int i=0;i<tag.length;i++)
        {
            //System.out.print("Token : "+token[i]+", Tag : "+tag[i]+"\n");
            if (tag[i].equals("NN") || tag[i].equals("NNP") || tag[i].equals("NNS"))
            {
                //System.out.println("masuk : " + token[i]);
                cleanTag = token[i] +" "+cleanTag;
            }
        }
        return cleanTag;
    }
    public void searchSimiliarPerson(String cluster) throws IOException, org.apache.lucene.queryparser.classic.ParseException
    {
        int hitsPerPage = 100;
        Directory index = FSDirectory.open(new File(indexPath));
        try (IndexReader reader = DirectoryReader.open(index)) {
            IndexSearcher searcher = new IndexSearcher(reader);
            TopScoreDocCollector collector = TopScoreDocCollector.create(hitsPerPage, true);
            
            Analyzer analyzer = new StandardAnalyzer(Version.LUCENE_40);
            Query q = new QueryParser(Version.LUCENE_40, "Cluster", analyzer).parse(cluster);
            searcher.search(q, collector);
            ScoreDoc[] hits = collector.topDocs().scoreDocs;

            //display results
            System.out.println("Found " + hits.length + " hits.");
           
            for(int i=0;i<hits.length;++i) {
              int docId = hits[i].doc;
              Document d = searcher.doc(docId);
              System.out.println((i + 1) + ". " + d.get("id") + ", " + d.get("displayName"));
            }
            Document d = searcher.doc(hits[0].doc);
            System.out.println("Get Detail for first person in list!");
            getDetailPerson(d.get("id"));
        }
    }
    
    public void getDetailPerson(String id) throws IOException, org.apache.lucene.queryparser.classic.ParseException
    {
        int hitsPerPage = 100;
        Directory index = FSDirectory.open(new File(indexPath));
        try (IndexReader reader = DirectoryReader.open(index)) {
            IndexSearcher searcher = new IndexSearcher(reader);
            TopScoreDocCollector collector = TopScoreDocCollector.create(hitsPerPage, true);
            
            Analyzer analyzer = new StandardAnalyzer(Version.LUCENE_40);
            Query q = new QueryParser(Version.LUCENE_40, "id", analyzer).parse(id);
            searcher.search(q, collector);
            ScoreDoc[] hits = collector.topDocs().scoreDocs;

            //display results
            System.out.println("Found " + hits.length + " hits.");
            
            for(int i=0;i<hits.length;++i) {
              int docId = hits[i].doc;
              Document d = searcher.doc(docId);
              System.out.println("Google+ ID:" + d.get("id") + "\nDisplay Name : " + d.get("displayName") +  "\nGender : " + d.get("gender") + "\nRelationship Status: " + d.get("relationshipStatus") +  "\nClean Tagline : " + d.get("tagline") + "\nCluster : " + d.get("Cluster"));
            }
        }
    }
    
    public void clusterPerson(String id)
    {        
        try {
            boolean getResult = getUserProfile(id);
            if (getResult)
            {   
                String name = "";
                String relstat = "";
                String strtag = "";
                String cleanTag = "";
                if( userProfile[2] != null )
                {
                    name = userProfile[2];
                }
                if( userProfile[3] != null )
                {
                    relstat = userProfile[3];
                }
                if( userProfile[4] != null )
                {
                    strtag = userProfile[4];                
                    cleanTag = getNounTagline(strtag);
                }
                System.out.println(cleanTag);
                String clusterSelected = filteredCluster(modelPath, name ,relstat,cleanTag, "2TEMP_output_users_wo_aboutme_training_clean_tag.arff");
                searchSimiliarPerson(clusterSelected);
            }
            
        } catch (Exception ex) {
            Logger.getLogger(ClusteringApp.class.getName()).log(Level.SEVERE, null, ex);
        }
        
    }
    public static void main(String[] args) {
        // TODO code application logic here
        ClusteringApp classifier= new ClusteringApp();
        classifier.clusterPerson("100629083497037686479");
    }
}
