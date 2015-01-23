import java.util.*;
import java.io.*;

public class NGramExtractor {

	public Hashtable<NGram, Integer>[] nGrams;
	//final String START = "@START@";
	//final String END = "@END@";
    final String SEPARATOR = "@SEP@";
    final String config = ".config"; 
    private String sourceDir;
            
    public Hashtable<NGram, Integer>[] generateDictionary() {
        // 
        File dir = new File(sourceDir);
        String sourceText;
        
        // Foreach file in source directory
        for(File file : dir.listFiles()) {
            sourceText = "";
    		try { 
    			Scanner input = new Scanner(file);
    			while(input.hasNextLine()) {
    				sourceText += input.nextLine();
    			}
                System.out.println("Reading file: " + file);
                
                // Extract
                int num = extract(sourceText, 3);
                
                System.out.println("Added " + num + " entries to the dictionary.");
    		}
    		catch(FileNotFoundException e) {
                System.out.println("Skipped file: " + file);
    		}
        }
                
        return nGrams;
	}
	
	public NGramExtractor(String sourceDir) {
	
		this.sourceDir = sourceDir;
	}
    
	public int extract(String source, int n) {
		
        // Init nGrams
		nGrams = new Hashtable[n];
		for(int i = 0; i < n; i++)
            nGrams[i] = new Hashtable<NGram, Integer>();

        int count = 0;
        // Filter source
		source = applyFilters(source);

        // Split source into multiple words
        String[] words = source.split(" ");

        // Loop through words[]
        for(int i = 0; i < words.length; i++) {
        		
			// Create nGrams of size {1, ... n-1, n}
			for(int m = 1; m <= n; m++) { // Loop from 1 to n

                // If we are within bounds
        		if(i+m <= words.length) {
       
                    // Create a new NGram of size m
    				NGram nGram = new NGram(m);

    				// Add words to the nGram
    				for(int w = 0; w <= m-1; w++) // Loop from 0 to m-1
                        nGram.addWord(words[i+w]);
                    
                    // Record NGram
    				if(nGrams[m-1].containsKey(nGram)) // if nGram exists
    					nGrams[m-1].put(nGram, nGrams[m-1].get(nGram)+1); // Increment NGram's count
    				else { // else nGram is new
    					nGrams[m-1].put(nGram, 1); // Add new NGram to NGrams 
                        count++; // Increment count
    				}	
    			}
    		}
    	}
        return count; // Return the number of entries added to the dictionary
    }
        
	public String applyFilters(String str) {
	    
        // Convert to lowercase
		str = str.toLowerCase();
        
        // Strip all line endings
        str = str.replaceAll("[\\n\\r]+", " ");
        
        // Strip unnecessary punctuation
        str = str.replaceAll("[^a-zA-Z0-9\\?\\!\\.\\s]+", "");

        // Collapse unnecessary whitespace
        str = str.replaceAll("[\\s\\t]{2,}", " ");
                
        // strip whitespace between punctuation
        str = str.replaceAll("([\\?\\!\\.])[\\s]+([\\?\\!\\.])", "$1$2");
        
        // Put spaces around punctuation
        str = str.replaceAll("[\\s]*([\\?\\!\\.]+)[\\s]*", " $1 ");
        
        // Put SEPARATOR after terminating punctuation
        str = str.replaceAll("([\\?\\!\\.]+)", "$1 " + SEPARATOR);

        // Put SEPARATOR at beginning and ending of source
        str = SEPARATOR + " " + str.trim() + " " + SEPARATOR;
        
		return str; // Return filtered str
	}
}	
		
	
		