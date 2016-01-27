# Refining Topic Models
The files here are used to read a topc model file from mallet and convert them into this format:

    Topic_1 w_1 w_2 .... w_n
    Topic_2 w_1 .....
      :       :    :    :  :
    Topic_n w_1 w_2 .....w_n
    
With and without garbage topics. Garbage topics are those that are close to a uniform distribution.

## Supporting Materials
The mallet  command to generate the input file is
    /bin/mallet XXXXXXX
    
    
