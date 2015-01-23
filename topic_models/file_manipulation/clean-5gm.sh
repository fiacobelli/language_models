#remove 5 grams that appear less than 10 times. replace \t with CTRL+V TAB
for i in `ls *.txt`;do echo "file:"$i; sed s/\t[0-9]$/d $i >tmp; mv tmp $i; echo "Done"; done;
#remove the frequency counts, we'll just go by occurrences in the text
for i in `ls *.txt`;do echo "file:"$i; sed s/\t[0-9]*$// $i >tmp; mv tmp $i; echo "Done"; done;
#finally, remove any lines containing non alphanumeric nor numeric characters.
for i in `ls *.txt`;do echo "file:"$i; sed /[^A-Za-z0-9[:space:]]/d $i >tmp; mv tmp $i; echo "Done"; done;