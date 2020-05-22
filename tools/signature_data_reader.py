import glob
import numpy as np


def read_data(path_data_folder="./signature_verification/data/"):

    # Get the user numbers from the corresponding file
    file_users = open(path_data_folder + "users.txt", 'r')
    list_users = [user.rstrip() for user in file_users]

    # Get the ground truth (gt) labels from the corresponding file
    dict_gt_labels = {}
    file_gt = open(path_data_folder + "gt.txt", 'r')
    for user in list_users:

        list_user_labels = []

        for gt_label_index, gt_line in enumerate(file_gt):

            label_gt = gt_line.rstrip().split()[1]
            list_user_labels.append(label_gt)

            if gt_label_index == 44:
                break  # this resets enumerate() so it always loads 45 labels for each user

        dict_gt_labels[user] = list_user_labels

    """ Read enrollment data from files and build a dictionary out of it, same thing with verification """

    dict_enrollment_data = {}

    for user_number in list_users:

        iterable_files = glob.glob(path_data_folder + "enrollment/" + user_number + "*.txt")
        dict_enrollment_data[user_number] = []  # creates an empty list in our dict to append np.arrays to

        for file_number, file_path in enumerate(iterable_files, 1):  # start enumerating from 1 instead of 0

            # get shape of data in file to create a numpy array with appropriate dimensions
            file_object = open(file_path, "r")
            nRows = 0
            nColumns = 7
            for line in file_object:  # yes, i iterate though the entire file to find it's nRows please somebody
                nColumns = len(line.split())  # find a better solution this is maximum ugly oh god wtf
                nRows += 1

            # create array with the file's data
            array_file = np.zeros([nRows, nColumns])
            file_object = open(file_path, "r")
            for line_number, line in enumerate(file_object):
                array_file[line_number] = line.rstrip().split()  # adds line data to corresponding row of array

            dict_enrollment_data[user_number].append(array_file)  # adds array to list in the dictionary key

    """ Read verification data from files and build a dictionary out of it, same thing with enrollment """

    dict_verification_data = {}

    for user_number in list_users:

        iterable_files = glob.glob(path_data_folder + "verification/" + user_number + "*.txt")
        dict_verification_data[user_number] = []  # creates an empty list in our dict to append np.arrays to

        for file_number, file_path in enumerate(iterable_files, 1):  # start enumerating from 1 instead of 0

            # get shape of data in file to create a numpy array with appropriate dimensions
            file_object = open(file_path, "r")
            nRows = 0
            nColumns = 7
            for line in file_object:  # yes, i iterate though the entire file to find it's nRows please somebody
                nColumns = len(line.split())  # find a better solution this is maximum ugly oh god wtf
                nRows += 1

            # create array with the file's data
            array_file = np.zeros([nRows, nColumns])
            file_object = open(file_path, "r")
            for line_number, line in enumerate(file_object):
                array_file[line_number] = line.rstrip().split()  # adds line data to corresponding row of array

            dict_verification_data[user_number].append(array_file)  # adds array to list in the dictionary key

    return dict_enrollment_data, dict_verification_data, dict_gt_labels

