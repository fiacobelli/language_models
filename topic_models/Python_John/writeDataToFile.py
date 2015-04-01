def writeToFile(sampleCollection):
   for x in sampleCollection:
      write(x.key + "\t" + x.value + "/n")