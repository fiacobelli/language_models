import java.util.HashMap;
import java.util.regex.Pattern;
import java.util.regex.Matcher;
import java.io.*;
import java.lang.*;
import java.util.*;

public class NGramReader {
  //Regex patterns from http://sentiment.christopherpotts.net/code-data/happyfuntokenizing.py
   public Pattern emoticon = 
   Pattern.compile("(?:[<>] ?[:;=8]? [\\Q-\\Eo\\Q*\\E\\Q'\\E] [\\Q)\\E\\Q]\\E\\Q(\\E\\Q[\\EdDpP/\\Q:\\E\\Q}\\E\\Q{\\E@\\Q|\\E] | [\\Q)\\E\\Q]\\E\\Q(\\E\\Q[\\EdDpP/\\Q:\\E\\Q}\\E\\Q{\\E@\\Q|\\E\\\\] [\\Q-\\Eo\\Q*\\E\\Q'\\E]? [:;=8] ?[<>])");
      // eyes
      // optional nose
      // mouth
      // or
      // mouth 
      // optional nose 
      // eyes
   public Pattern twitterUserName = Pattern.compile("?:@[\\w_]+");
   public Pattern twitterHashtag = Pattern.compile("(?:\\#+[\\w_]+[\\w\\Q'\\E_\\Q-\\E]*[\\w_]+)");
   private void readFile(String file)throws IOException {
      String token = new String();
      int nGramNameLength = 1;
      final int atomic = 1;
      String gram = new String();
      StringBuilder hashGram = new StringBuilder();
      ArrayList<String> stBuild = new ArrayList<String>();
      HashMap<StringBuilder,Integer> hashOne = new HashMap<StringBuilder,Integer>();
      Pattern pattern = Pattern.compile("\\s");
      File f = new File(file);
      Scanner scan = new Scanner(f).useDelimiter(pattern);
      while(scan.hasNext()) {
         token = scan.next();
         if (!token.equals("")){
            stBuild.add("\t" + token);  
         }                                            
      } scan.close();
      
      //stBuild = gram.split("\\t");
      
      for(int j = 1; j < stBuild.size(); j++) {
         hashGram.append("\t"); 
         
         for(int k = j; k < stBuild.size(); k++) {
            int num = k - j + 1;
            nGramNameLength = hashGram.indexOf("\t") + 1;
            hashGram.delete(0, nGramNameLength);
            hashGram.insert(0, num + "Gram\t");
            Matcher matcher = emoticon.matcher(stBuild.get(k));
            Matcher hashMatcher = twitterHashtag.matcher(stBuild.get(k));
            Matcher userMatcher = twitterUserName.matcher(stBuild.get(k));
            if (matcher.matches()){
               hashGram.append("Emoticon ");
               //matcher.group();
                   // matcher.start();
                    //matcher.end();
            }
            if (hashMatcher.matches()){
               hashGram.append("TwitterHashTag ");
               //hashMatcher.group();
              // hashMatcher.start();
               //hashMatcher.end();
            }

            if (userMatcher.matches()){
               hashGram.append("TwitterUserName ");
               //userMatcher.group();
               //userMatcher.start();
               //userMatcher.end();
            }
            hashGram.append(stBuild.get(k) + "\t");
            if (hashOne.containsKey(hashGram)) {
               int t = hashOne.get(hashGram) + 1;
               hashOne.put(hashGram, t);
               System.out.println(k - j + 1);
            }else {
               hashOne.put(hashGram, atomic); 
            }                  
            System.out.println(hashGram.toString());
         }
         hashGram.delete(0, hashGram.length());            
      }System.out.println(hashOne.toString());
   } 
   
   public static void main(String[] args)throws IOException {
      NGramReader a = new NGramReader();
      a.readFile("20120101.txt");
   }
}

         
         
         
         