/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package googleplusindexer;

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
	
	
	public String classifypost(String post,String modelname) throws Exception{
            //Declare Attributes
            Attribute comment = new Attribute("comment",(FastVector) null);
		
            //Declare the class attribute along with its value
            FastVector classVal = new FastVector(2);
            classVal.addElement("automotive");
            classVal.addElement("entertainment");
            classVal.addElement("technology");
            Attribute ClassAttribute = new Attribute("@class@",classVal);
		
            //Declare the feature vector
            FastVector FvAttributes = new FastVector(2);
            FvAttributes.addElement(comment);
            FvAttributes.addElement(ClassAttribute);
		
            //Create an empty set
            Instances inputinstances = new Instances("relation",FvAttributes,1);
            //Set Class Index
            inputinstances.setClassIndex(1);
		
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
	
    public static void main(String[] args) throws Exception {
        // TODO code application logic here
        String post = "This is a good phone";
        Postclassifier classifier= new Postclassifier();
        
        System.out.println(classifier.classifypost(post,"model/postNaiveBayes.model"));
        System.out.println(classifier.classifypost(post,"model/postIBk.model"));
        System.out.println(classifier.classifypost(post,"model/postSMO.model"));
        
    }
}


