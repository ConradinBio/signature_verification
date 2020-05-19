import pickle
import csv
gt_file = open("./dataset/gt.txt", 'r')
gt_reader = csv.reader(gt_file, delimiter=' ')
gt = [row for row in gt_reader]
#### reloading the dictionarys and normalize and sort the distances to get the DTW result list
#reloading the data from the distance_dict_pickled file
dictionary_file = open('distance_dict_pickled_cudi.bin', 'rb')  # reading mode
distance_dict = pickle.load(dictionary_file)
dictionary_file.close()

dictionary_file = open('variance_dict_pickled_cudi.bin', 'rb')  # reading mode
variance_dict = pickle.load(dictionary_file)
dictionary_file.close()

# normalize the distances so that they can be ranked by distance

def normalize_distances(distance_dictionary, variance_dictionary):
    to_be_sorted_lst = []
    for i in range(1,31):
        for j in range(45):
            print(variance_dictionary[i])
            to_be_sorted_lst.append(distance_dictionary[i][j]/variance_dictionary[i][0])
            
    return to_be_sorted_lst

def create_ranked_lst(lst):
    for i in range(len(to_be_sorted_lst)):
        to_be_sorted_lst[i] = (to_be_sorted_lst[i],gt[i])
    return (sorted(to_be_sorted_lst))
       
to_be_sorted_lst=normalize_distances(distance_dict, variance_dict)
ranked_lst=create_ranked_lst(to_be_sorted_lst)

#pickles the results for evaluation
with open('DTW_results_cudi.bin', 'wb') as fp:
    pickle.dump(ranked_lst, fp)

# to read i back use the following code
with open ('DTW_results_cudi.bin', 'rb') as fp:
    ranked_lst = pickle.load(fp)




