##Topic Models
####Extract Topic Models
    input: raw topic in wtcf format generated through LDA
    File Format:    
                    Word_1 topic:count .... topic:count
                    Word_2 topic:count ................
                    :       :    :    :  :  :   :  : :
                    Word_3 topic:count...... topic:count
    Output: A csv containing a probability matrix of the words in topics.
    File Format:
                            Topic_1 ............ Topic_5
                    Word_1  probability ................
                    :       :    :    :  :  :   :  : :
                    Word_9  .................probability
    Calculating Probability Choices: 
        1.Topic-Wise: The probability of the word occuring in that topic from all given topics. 
            **Each word sums upto 1.0 in probability
        2.Word-Wise: The probability of the word occuring in that topic from all given words of that topic
            **Each topic sums upto 1.0 in probability
        3.Document-Wise: The probability of the word occuring that topic from all given words in the document
        **The whole document together sums upto 1.0 probability
    Example:
        | Word          |  Topic:Count   |
        | ------------- |:-------------: |
        | java           | 3:19 4:25 1:1 | 
        | car            | 2:13          | 
        | computers      | 4:9  3:2  4:1 |  
        
    Probability of Java in Topic 2 is ...
    
    Choice 1: 19/45
    Choice 2: 19/21
    Choice 3: 19/70
    
####Refine Topic Models
####Evaluate Topic Models
    
