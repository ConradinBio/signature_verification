import numpy as np
from sklearn.preprocessing import RobustScaler


def make_list_out_of_all_signatures_in_dict(dict_signature_data):

    list_all_signatures_in_dict = []

    # concatenate all signature features in dict to make a super array of this dict
    for user in dict_signature_data:
        for signature in dict_signature_data[user]:
            list_all_signatures_in_dict.append(signature)

    return list_all_signatures_in_dict


def normalize(dict_enrollment_data, dict_verification_data):

    # Collect all feature data into a single array
    list_enrollment_data = make_list_out_of_all_signatures_in_dict(dict_enrollment_data)
    list_verification_data = make_list_out_of_all_signatures_in_dict(dict_verification_data)
    list_all_data = list_enrollment_data + list_verification_data

    # Fit scaler to our data so it can perform the transformation correctly
    """I chose RobustScaler as it is robust to outliers. If it is absolutely necessary that the feature values are 
        contained in the interval [0-1], we can use this function instead:
        scaler = MinMaxScaler().fit(np.vstack(list_all_data))"""
    scaler = RobustScaler().fit(np.vstack(list_all_data))  # vstack appends all values into one large list


    # print(dict_enrollment_data["001"][0][0])  # to check how the rescaling works, more info in notes

    """ transform data into a normalized dictionary """
    dict_enrollment_data_normalized = {}

    for user in dict_enrollment_data:
        list_signatures_normalized = []
        for signature in dict_enrollment_data[user]:
            list_signatures_normalized.append(scaler.transform(signature))
        dict_enrollment_data_normalized[user] = list_signatures_normalized

    # print(dict_enrollment_data_normalized["001"][0][0])  # to check how the rescaling works, more info in notes

    """ transform data into a normalized dictionary """
    dict_verification_data_normalized = {}

    for user in dict_verification_data:
        list_signatures_normalized = []
        for signature in dict_verification_data[user]:
            list_signatures_normalized.append(scaler.transform(signature))
        dict_verification_data_normalized[user] = list_signatures_normalized

    return dict_enrollment_data_normalized, dict_verification_data_normalized
