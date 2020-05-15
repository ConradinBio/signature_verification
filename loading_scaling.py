import glob #get files with pattern matching
import os
import csv
import pickle
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import RobustScaler
from sklearn.preprocessing import Normalizer
import matplotlib.pyplot as plt


#########################################
##    Helper functions                ###
#########################################


def file_list_to_feature_matrix(file_list):
##  This function takes a list of files and returns a list of matrices,
##  only containing the features we're intrested in

    return_matrices = []
    for i, file in enumerate(file_list):
        #basename = os.path.basename(enrollment_file)
        #basename = os.path.splitext(basename)[0]
        #processed_file_name = "./dataset/enrollment_processed/"+basename+".dat"
        file = open(file, 'r')
        file_reader = csv.reader(file, delimiter=' ')
        file_mat = np.array([row for row in file_reader])

        # Input matrix:
        # [:,0] =  time
        # [:,1] =  x
        # [:,2] =  y
        # [:,3] =  pressure
        # [:,4] =  penup
        # [:,5] =  azimuth
        # [:,6] =  inclination

        # The final output matrix
        # [:,0] =  normalized(x)
        # [:,1] =  normalized(y)
        # [:,2] =  normalized(v(x))
        # [:,3] =  normalized(v(y))
        # [:,4] =  pressure

        #velocity = delta(dist) / delta(time)
        #as the sampling rate is the same for all saples, we omit dividing by the time
        #calculating the difference between two adjacent positions can be done with 
        # np.gradient which aproximates mat[x] = mat[x+1]-mat[x]

        nb_timesteps = np.shape(file_mat)[0]
        processed_mat = np.empty(shape=[nb_timesteps,5])
        
        file_mat = file_mat.astype(float)
        processed_mat[:,0] = file_mat[:,1]
        processed_mat[:,1] = file_mat[:,2]
        processed_mat[:,2] = np.gradient(file_mat[:,1])
        processed_mat[:,3] = np.gradient(file_mat[:,2])
        processed_mat[:,4] = file_mat[:,3]
        return_matrices.append(processed_mat)
    return return_matrices

def normalize_signatures(transformer, signatures):
    ## This function takes a transformer (a fitted normalizer) and applies
    ## it to a list of matrices, returns a list of normalized matrices
    res = []
    for signature in signatures:
        res.append(transformer.transform(signature))
    return res    




#########################################
##    Main routine starts here        ###
#########################################

#open the files
enrollment_files = glob.glob("./dataset/enrollment/*.txt")
verification_files = glob.glob("./dataset/verification/*.txt")
cutouts = glob.glob("./ground-truth/locations/*.svg")
user_file = open("./dataset/users.txt", 'r')
gt_file = open("./dataset/gt.txt", 'r')
enrollment_files.sort()
verification_files.sort()

#process the single files
#open the readers
user_reader = csv.reader(user_file)
gt_reader = csv.reader(gt_file, delimiter=' ')

#store the data
users = [row for row in user_reader]
gt = [row for row in gt_reader]

#process the file lists
signatures_training = file_list_to_feature_matrix(enrollment_files)
signatures_test = file_list_to_feature_matrix(verification_files)

##train the scaler on the training data
# I chose RobustScaler as it is robust to outliers
# If it is absolutely necessary that the feature values are contained
# in the interval [0-1], we can use this function instead:
# scaler = MinMaxScaler().fit(np.vstack(signatures_training))

scaler = RobustScaler().fit(np.vstack(signatures_training)) #np.vstack appends all values into one large list



#apply the trained scaler to the data
signatures_training_normalized = normalize_signatures(scaler, signatures_training)
signatures_test_normalized = normalize_signatures(scaler, signatures_test)


#################################
##    HOW TO USE THE DATA      ##
#################################

#### SOME EXAMPLES ###
## Access the first signature in the training dataset:
signature_1 = signatures_training_normalized[0]

## get the feature "pressure" for the first signature:
pressure_feature_signature_1 = signature_1[:,4]

## get all features at time 0 for the fist signature:
all_features_at_time_0 = signature_1[0,:]

## iterate over all signatures in the test dataset:
## check the function normalize_signatures() and change the function inside