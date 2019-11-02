'''
Created on Oct 31, 2019

@author: shivani.chauhan
'''

class Logic:
    
    word_list = []
    word_occ_dict = {}

    def get_word_list(self):
        return self.word_list
 
 
    def get_word_occ_dict(self):
        return self.word_occ_dict
 
 
    def set_word_list(self, value):
        self.word_list = value
 
 
    def set_word_occ_dict(self, value):
        self.word_occ_dict = value


# The function is reading a tsv file.
# input : A tsv file
# output : Generates a dictionary and a list
    with open(r"C:\Users\shivani.chauhan\Downloads\word_search.tsv") as file:
        for line in file:
            word, occ = line.split('\t')
            word_occ_dict[word] = occ.strip()
            word_list.append(word)
        
            
# search_word method takes the input and check for the matching words in the word list and returns the input_matching_list.
#input : query string typed by user
# returns : list of words matching input string
    def search_word(self, input):
        input_matching_list = []
        for word in self.get_word_list():
            if input in word:
                input_matching_list.append(word)
        return input_matching_list
    

#  sorting method performs ranking and returns a list of 25 tuples elements which ranks higher.
# input : input and input matching list of words
# output : returns list of tuple based n ranking
    def sorting(self, input_matching_results, input):
        list_of_tuple = [(result, result.find(input), self.word_occ_dict[result], len(result)) for result in input_matching_results]
        list_of_tuple.sort(key=lambda elem: (elem[3],elem[1]))
        ranked_results = [(result_distance[0],result_distance[2]) for result_distance in list_of_tuple][:25]
        return(ranked_results)


# sorting(search_word('eta'), 'eta')