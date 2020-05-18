import numpy as np
from fastdtw import fastdtw
from tqdm import tqdm


def calculate_variance_within_users(dict_enrollment_data):

    dict_variances_within_users = {}
    dict_mean_dissimilarity_within_users = {}
    dict_dissimilarity_intervals_within_users = {}

    for user in tqdm(dict_enrollment_data):  # tqdm() makes the loading bar - super weird and useful behaviour

        nSignatures = len(dict_enrollment_data[user])
        list_dissimilarities_within_user = []  # this list will contain all computed dtw values for this user

        for index_signature in range(0, nSignatures):
            for index_signature_to_compare_to in range(index_signature + 1, nSignatures):
                signature_1 = dict_enrollment_data[user][index_signature]
                signature_2 = dict_enrollment_data[user][index_signature_to_compare_to]

                dissimilarity_score = fastdtw(signature_1, signature_2)[0]  # we only want the score, hence [0]
                list_dissimilarities_within_user.append(dissimilarity_score)  # add score to list of scores

        # Some math to calculate variance. formula here: https://bit.ly/3cSyEGx - is "n" better than "n-1" ?
        mean_dissimilarity_score = sum(list_dissimilarities_within_user) / len(list_dissimilarities_within_user)

        sum_of_squared_differences = np.sum(np.square([dissimilarity - mean_dissimilarity_score
                                                       for dissimilarity in list_dissimilarities_within_user]))

        variance_within_user = np.sqrt(sum_of_squared_differences / (len(list_dissimilarities_within_user) - 1))

        expected_dissimilarity_range_within_user = [mean_dissimilarity_score - variance_within_user,
                                                    mean_dissimilarity_score + variance_within_user]

        # Add calculated values/range to their respective dictionaries
        dict_mean_dissimilarity_within_users[user] = mean_dissimilarity_score
        dict_variances_within_users[user] = variance_within_user
        dict_dissimilarity_intervals_within_users[user] = expected_dissimilarity_range_within_user

    return dict_mean_dissimilarity_within_users, dict_variances_within_users, dict_dissimilarity_intervals_within_users


def calculate_dissimilarities_between_datasets(dict_enrollment, dict_verification):

    dict_all_dissimilarities = {}

    for user in tqdm(dict_enrollment):  # could also be dict_verification, and again tqdm loading bar, magnificent

        # get nRows and nCols for array containing dissimilarity scores between enrollment and verification signatures
        nRows = len(dict_verification[user])  # this means that each row corresponds to a verification signature
        nCols = len(dict_enrollment[user])  # this means that each column corresponds to a enrollment signature

        array_dissimilarities = np.zeros(shape=(nRows, nCols))   # initiate said array

        for index_signature_enroll, signature_enroll in enumerate(dict_enrollment[user]):

            list_dissimilarities = []  # this list will contain all dissimilarities between this user's signatures

            for signature_verification in dict_verification[user]:

                dissimilarity = fastdtw(signature_enroll, signature_verification)[0]  # we still don't want the path
                list_dissimilarities.append(dissimilarity)                                                  # sorry

            array_dissimilarities[:, index_signature_enroll] = list_dissimilarities

        dict_all_dissimilarities[user] = array_dissimilarities

    return dict_all_dissimilarities
