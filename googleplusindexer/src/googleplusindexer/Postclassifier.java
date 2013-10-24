/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package googleplusindexer;

import java.util.Random;
import weka.classifiers.meta.FilteredClassifier;
import weka.core.Attribute;
import weka.core.FastVector;
import weka.core.Instance;
import weka.core.Instances;

/**
 *
 * @author Chris
 */
public class Postclassifier {

	/* Declare Variables */
	private FastVector classVal;
	private Instances inputinstances;
        Attribute ClassAttribute;
        Attribute comment;
	public void initclassifier() throws Exception{
            //Declare Attributes
            comment = new Attribute("comment",(FastVector) null);
		
            //Declare the class attribute along with its value
            classVal = new FastVector(2);
            classVal.addElement("automotive");
            classVal.addElement("entertainment");
            classVal.addElement("technology");
            ClassAttribute = new Attribute("@class@",classVal);
		
            //Declare the feature vector
            FastVector FvAttributes = new FastVector(2);
            FvAttributes.addElement(comment);
            FvAttributes.addElement(ClassAttribute);
		
            //Create an empty set
            inputinstances = new Instances("relation",FvAttributes,1);
            //Set Class Index
            inputinstances.setClassIndex(1);
	}
    public String classifypost(String post,String modelname) throws Exception{
            //Create and add instance
            Instance newinstance = new Instance(inputinstances.numAttributes());
            newinstance.setValue(comment,post);
            inputinstances.add(newinstance);
            Instance last = inputinstances.lastInstance();
             
            // Load model;
            FilteredClassifier classifier = (FilteredClassifier) weka.core.SerializationHelper.read(modelname);
            double result = classifier.classifyInstance(last);
            return inputinstances.classAttribute().value((int) result);   
    }
    
    public String GetClass(String post) throws Exception {
        String SMO,Naive,IBk;
        String result="Unknown";
        Naive = classifypost(post,"model/postNaiveBayes.model");
        SMO = classifypost(post,"model/postSMO.model");
        IBk = classifypost(post,"model/postIBk.model");
        
        //Ensemble Learning
        
        // IF 2 class result at least same
        if((SMO.equals(Naive)) || (SMO.equals(IBk)) || (Naive.equals(IBk))){
            if((SMO.equals(Naive)) || (SMO.equals(IBk)))  {
                result = SMO;
            }else{
                result = Naive;
            }
        }else{
            Random r = new Random();
            int i = r.nextInt(3);
            if(i==0){
                result = Naive;
            }else if(i==1){
                result = SMO;
            }else {
                result = IBk;
            }
        }
        
        return result;
    }
    public static void main(String[] args) throws Exception {
        // TODO code application logic here
        String post = "Computer Phone";
        Postclassifier classifier= new Postclassifier();
        classifier.initclassifier();
        System.out.println(classifier.classifypost(post,"model/postNaiveBayes.model"));
        System.out.println(classifier.classifypost(post,"model/postIBk.model"));
        System.out.println(classifier.classifypost(post,"model/postSMO.model"));
        System.out.println(classifier.GetClass(post));
    }
}


