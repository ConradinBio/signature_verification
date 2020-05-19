def find_nTP_and_nFP_1SD(dict_dissimilarities, dict_1sd_intervals, dict_gt_labels):

    # Something i tried, more for testing and demonstration, if you look into the output folder you will see that
    # this is absolutely not an appropriate classifier

    # find true positives and true negatives: 2 conditions
    #  1. verification signatures that have all 5 dissimilarity scores in an interval that fits inside 1 SD
    #  2. they have a ground truth (gt.txt) label of "g" for TP's and "t" for FP's

    acceptance_threshold = 5  # this means all 5 dissimilarity scores need to be inside 1 standard deviation

    dict_TPs_FPs = {}

    for user in dict_dissimilarities:  # could be any dict really, same keys for all

        counter_TP = 0
        counter_FP = 0

        for index_verification_image, list_verification_image_scores in enumerate(dict_dissimilarities[user]):

            counter_values_inside_1SD = 0

            for dissimilarity_score in list_verification_image_scores:
                if dict_1sd_intervals[user][0] <= dissimilarity_score <= dict_1sd_intervals[user][1]:
                    counter_values_inside_1SD += 1

            if counter_values_inside_1SD >= acceptance_threshold:
                if dict_gt_labels[user][index_verification_image] == 'g':
                    counter_TP += 1
                elif dict_gt_labels[user][index_verification_image] == 'f':
                    counter_FP += 1

        dict_TPs_FPs[user] = [counter_TP, counter_FP]

    return dict_TPs_FPs
