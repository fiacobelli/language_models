public class NGram {

	public String[] items;
	private int count;

	public NGram(int size) {
		count = size;
		items = new String[size];
	}

	public void addWord(String word) {
		if(count > 0) {
			items[items.length-count] = word;
			count--;
		}	
	}
	
	public String toString() {
		String output = items.length + "-GRAM\t";
        output += items[0];
		for(int i = 1; i < items.length; i++)
			output += " " + items[i];	
		return output;	
	}
	
	public boolean equals(Object o) {
		String[] strArr = ((NGram)o).items;
		if(strArr.length == items.length) {
			for(int i = 0; i < items.length; i++)
				if(!strArr[i].equals(items[i]))
					return false;
			return true;		
		}
		return false;
	}
	
	public int hashCode() {
		String hashStr = "";
		for(int i = 0; i < items.length; i++)
			hashStr += items[i] + ":";
		int hash = 7;
		for(int i = 0; i < hashStr.length(); i++)
			hash = hash*31+hashStr.charAt(i);
		return hash;
	}
}	
