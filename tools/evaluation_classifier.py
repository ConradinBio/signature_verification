

def reduce_to_smallest_normalized_score(dict_dissimilarity_scores, dict_mean, dict_variance):

    # create a dictionary containing only the smallest dissimilarities of each of the 5 computed dissimilarities
    # of each verification image for this user
    dict_only_smallest_scores = {}

    for user in dict_dissimilarity_scores:

        list_smallest_scores_of_verification_images = []

        for verification_signature in dict_dissimilarity_scores[user]:
            list_smallest_scores_of_verification_images.append(min(verification_signature))  # only pick smallest of 5

        dict_only_smallest_scores[user] = list_smallest_scores_of_verification_images

    # normalise scores by dividing through their user's enrollment image mean dissimilarity score
    dict_only_smallest_scores_normalized = {}

    for user in dict_only_smallest_scores:
        list_scores_normalized = [(score - dict_mean[user]) / dict_variance[user]
                                  for score in dict_only_smallest_scores[user]]
        dict_only_smallest_scores_normalized[user] = list_scores_normalized

    return dict_only_smallest_scores_normalized


def build_sorted_list(dict_only_smallest_score_normalized):

    # create a dictionary that saves the index and user-label for each dissimilarity score
    # THIS CAN POTENTIALLY LEAD TO ERRORS SINCE 2 MEASURES COULD HAVE THE EXACT SAME SCORE BUT DIFFERENT INDICES/USERS
    dict_scores_as_keys = {}

    for user in dict_only_smallest_score_normalized:
        for index_verification_signature, signature_score in enumerate(dict_only_smallest_score_normalized[user]):

            dict_scores_as_keys[signature_score] = [user, index_verification_signature]

    assert len(dict_scores_as_keys) == 1350, " data contains 2 equal dissimilarity scores, unable to fetch gt labels"

    # now we need to build a big list with all min(scores) from all users and sort it in ascending fashion
    list_smallest_scores_all_users = []

    for user in dict_only_smallest_score_normalized:
        list_smallest_scores_all_users += dict_only_smallest_score_normalized[user]  # list.append() no good here

    list_scores_sorted = sorted(list_smallest_scores_all_users)

    return list_scores_sorted, dict_scores_as_keys
