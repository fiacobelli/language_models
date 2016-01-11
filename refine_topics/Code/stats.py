import numpy;


# PUBLIC feed it a 2d or 1d array of number will return a single number	
def getStandardDeviation(arr):
	if (isinstance(arr[0], list)):
		return numpy.std(convert2DArray(arr));
	else:
		return numpy.std(arr);

# PUBLIC feed it a 2d or 1d array of number will return a single number	
def getMean(arr):
	if (isinstance(arr[0], list)):
		return numpy.mean(convert2DArray(arr));
	else:
		return numpy.mean(arr);	

#Will convert a 2d array and return a single array 
def convert2DArray(arr):
	single_arr = [0,0];
	for i,a in enumerate (arr):
		single_arr.extend(a[i+1:]);
	return single_arr;

def display(sd,mean,min,kb):
	print "Standard Deviation: "+ str(sd);
	print "Mean: "+ str(mean);
	print "Min Normal: "+ str(min);
	print "KB Value: "+ str(kb);	

