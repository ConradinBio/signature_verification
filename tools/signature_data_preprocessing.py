import numpy as np


def preprocess(dict_raw_data):

    dict_preprocessed_data = {}

    for user in dict_raw_data:

        list_signatures_preprocessed = []  # this list will contain all preprocessed signatures of the current user

        for signature in dict_raw_data[user]:

            # Get rows & cols for new, improved, Banging, PREPCROCESSED feature array
            signature_nRows = np.shape(signature)[0]
            nCols = 5

            # initiate new, improved, Banging, PREPCROCESSED feature array
            signature_preprocessed = np.zeros(shape=(signature_nRows, nCols))

            # assign values to new, improved, Banging, PREPCROCESSED feature array
            signature_preprocessed[:, 0] = signature[:, 1]
            signature_preprocessed[:, 1] = signature[:, 2]
            signature_preprocessed[:, 2] = np.gradient(signature[:, 1])
            signature_preprocessed[:, 3] = np.gradient(signature[:, 2])
            signature_preprocessed[:, 4] = signature[:, 3]

            list_signatures_preprocessed.append(signature_preprocessed)  # append to list of signatures of user

        dict_preprocessed_data[user] = list_signatures_preprocessed  # add user with list of signatures to dictionary

    return dict_preprocessed_data
