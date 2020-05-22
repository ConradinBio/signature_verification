import pickle
from pyts.metrics import dtw
import matplotlib.pyplot as plt


def main():
    ########## load the stored data ###########
    with open('list_scores_sorted', 'rb') as dist_file:  # reading mode
        distances = pickle.load(dist_file)

    with open('list_labels_sorted','rb') as label_file:
        labels=pickle.load((label_file))

    #initial values:
    FN=labels.count('g') #start with all as FN, then add one by one
    TP=0
    FP=0

    precisions=[]
    recalls=[]

    for i in range(len(distances)):
        if labels[i]=='g':
            FN-=1
            TP+=1
        else:
            FP+=1

        precision,recall=precision_recall_calc(TP,FP, FN)
        if precision==1:
            max_precision_index=i
        precisions.append(precision)
        recalls.append(recall)
        if recall==1:
            break

    print("In total, there are", len(distances), "distances (signatures)")
    print("max precision is achieved until the", max_precision_index + 1,"smallest distances ,i.e. until a distance of", distances[max_precision_index], "standard deviations")
    print("max recall is achieved using the", recalls.index(max(recalls)) + 1,"smallest distances, i.e. until a distance of", distances[recalls.index(max(recalls))], "standard deviations")

    # now I sometimes have more than 1 precision for the same recall value; I only want to keep the first one
    final_precision_list = []
    final_recall_list = []
    index = -1
    for i in recalls:
        index += 1
        if i not in final_recall_list:
            final_recall_list.append(i)
            final_precision_list.append(precisions[index])

    max_precision_index=final_precision_list.index(max(final_precision_list))
    final_precision_list2=final_precision_list[max_precision_index:]
    final_recall_list2=final_recall_list[max_precision_index:]

    plt.plot(final_recall_list2, final_precision_list2, marker='o', markersize=3, color="red")
    plt.xlabel("recall")
    plt.ylabel("precision")
    plt.title("Recall-Precision curve/AP " )
    plt.savefig("output_AP ")
    plt.show()


def precision_recall_calc(TP, FP, FN):
    precision = TP / (TP + FP)
    recall = TP / (TP + FN)
    return (precision, recall)

main()
