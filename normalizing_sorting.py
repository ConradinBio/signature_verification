import pickle
import csv
import time
import matplotlib.pyplot as plt
dataset_name = "cudis"

def main():
  t0 = time.time()
  
  #######################################
  ## Get data and create a ranked list ##
  #######################################

  gt_file = open("./data/gt.txt", 'r')
  gt_reader = csv.reader(gt_file, delimiter=' ')
  # should we close the file?:
  # gt_file.close()
  
  gt = [row for row in gt_reader]
  
  distance_dict = 0
  variance_dict = 0
  if dataset_name == "cudis":
    distance_dict = get_bin_data("distance_dict_pickled_cudi.bin")
    variance_dict = get_bin_data("variance_dict_pickled_cudi.bin")
  elif dataset_name == "default":
    distance_dict = get_bin_data("dist_dict_default.bin")
    variance_dict = get_bin_data("var_dict_default.bin")
  elif dataset_name == "euclid":
    distance_dict = get_bin_data("dist_dict_euclid.bin")
    variance_dict = get_bin_data("var_dict_euclid.bin")
  
  to_be_sorted_lst = normalize_distances(distance_dict, variance_dict)
  ranked_lst = create_ranked_lst(to_be_sorted_lst, gt)
  
  ########################################
  ##  Calculate Presicion/Recall curve  ##
  ########################################


  # print("ranked list:")
  # print(ranked_lst[0:20])
  print("the length:", len(ranked_lst))
  
  tot_num_positives = 0
  # count all positives
  for signature in ranked_lst:
    if signature[1][1] == 'g':
      tot_num_positives += 1
  
  precision = []
  recall = []
  TPs = 0
  FPs = 0
  for signature in ranked_lst:
    if (TPs + FPs) < 40:
      print(signature)
    if signature[1][1] == 'g':
      TPs += 1
    else:
      FPs += 1
    precision.append(TPs / (TPs+FPs))
    recall.append(TPs / tot_num_positives)
      
  # print()
  # print("precision:", precision)
  # print("recall:", recall)
  
  
  # plt.plot(recall, precision, marker='o', markersize=3, color="red")
  plt.plot(recall, precision, color="red")
  plt.xlabel("recall")
  plt.ylabel("precision")
  plt.title("Recall-Precision curve/AP " + dataset_name)
  plt.show()
    

  # #pickles the results for evaluation
  # with open('DTW_results_cudi.bin', 'wb') as fp:
  #     pickle.dump(ranked_lst, fp)
  
  # # to read i back use the following code
  # with open ('DTW_results_cudi.bin', 'rb') as fp:
  #     ranked_lst = pickle.load(fp)
  
  
  ########## print time ###########
  tot_time = time.time()-t0
  minutes = int(tot_time/60)
  seconds = int(tot_time - (minutes*60))
  print("time: ", minutes, "min ", seconds, "s", sep="")




def get_bin_data(filename):
  file_object = open(filename, 'rb')  # reading mode
  data = pickle.load(file_object)
  file_object.close()
  return data


def normalize_distances(distance_dictionary, variance_dictionary):
    to_be_sorted_lst = []
    for i in range(1,31):
        for j in range(45):
            # print(variance_dictionary[i])
            to_be_sorted_lst.append(distance_dictionary[i][j]/variance_dictionary[i][0])
            
    return to_be_sorted_lst


def create_ranked_lst(lst, gt):
    for i in range(len(lst)):
        lst[i] = (lst[i],gt[i])
    return (sorted(lst))


if __name__ == "__main__":
  main()

