/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package clustering;

import weka.core.Instances;
import weka.clusterers.SimpleKMeans;
import weka.core.converters.ConverterUtils.DataSource;
import weka.clusterers.ClusterEvaluation;

/**
 *
 * @author Chris
 */
public class Clustering {

	//Training set variables
	private static Instances data; //set of training instances
	private static SimpleKMeans kmeans; //instance of clusterer
	private static DataSource source; //training set arff file
	
	//Test set variables
	private static DataSource newsource; // test set arff file
	private static Instances newdata; // set of test instances
	private static ClusterEvaluation eval; // evaluation cluster
	private static double[] InstancesCluster;
        
	public Clustering(){} //Constructor
	
	public static void trainkmeans(String filename) throws Exception{
		source = new DataSource(filename); //Load arff file
		data = source.getDataSet(); // Get instances from file
		kmeans = new SimpleKMeans(); // Make new k means
		
		//Set Parameter
		kmeans.setNumClusters(10); //Get X number of clusters
		kmeans.setSeed(10);
		
		//Build Clusterer
		kmeans.buildClusterer(data);
	}
	
	public static void clusternewset(String filename) throws Exception{
		newsource = new DataSource(filename); // Load arff file
		newdata = newsource.getDataSet(); // Get instances from file
		eval = new ClusterEvaluation();
		
		//Evaluate new data set
		eval.setClusterer(kmeans); //Test data from cluster kmeans
		eval.evaluateClusterer(newdata); //Cluster the new set
	}
        
        public static void printcluster(){
            	// output cluster result
                System.out.println("# of clusters: " + kmeans.getNumClusters());
                System.out.println(kmeans);
        }
        
        /* Print every data/instances that has cluster no N (instances with member of cluster no N) */
        public static void printdatawithclusterN (int N) {
            InstancesCluster = eval.getClusterAssignments(); //Get #cluster from every instances in an array
            for(int i = 0;i < newdata.numInstances();i++){
                if(InstancesCluster[i]==N){
                    System.out.print("Instances #");
                    System.out.print(i);
                    System.out.print(" ");
                    System.out.print(newdata.instance(i));
                    System.out.println();
                }
            }
        }
        
    public static void main(String[] args) throws Exception {
        //Training the cluster with bank.arff trainingset
        trainkmeans("bank.arff");
        //evaluate bank-new with trained cluster
        clusternewset("bank-new.arff");
        
        //Print cluster result
        printcluster();
        printdatawithclusterN(3); //Print Data with cluster no 3
    }
    
}
