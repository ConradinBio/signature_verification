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

#####################DTW###################


from fastdtw import fastdtw
from scipy.spatial.distance import euclidean
from tqdm import tqdm

#calculate the variance within one user of his 5 signatures
#create a dictionary where key i user and value are the 5 signatures
def variance_dict(users,signatures_training_normalized):
    variance_dict = {}
    for i in range(1,len(users)+1):
        variance_dict[i]=0
    d = 1
    for user in tqdm(range(1,31)):  
        distance_matrix = np.zeros(shape=(5,5))
        user_sigs = signatures_training_normalized[d-1:d+4]
        for i in range(5):
            for j in range(5):
                distance_matrix[i,j]= fastdtw(user_sigs[j],user_sigs[i],dist=euclidean)[0]
        #print(distance_matrix)
        distance_matrix = np.unique(distance_matrix)[1:] #removes all lower half of the array and the 0
        mean=np.mean(distance_matrix)
        variance = np.sum(np.sqrt(np.abs(mean-distance_matrix)))/10
        variance_dict[user]=[mean,variance]
        d = d+5
        #print(mean,variance)
    return(variance_dict)

def create_distances(signatures_training_normalized,signatures_test_normalized):
    #create dictionary that contains the distances of the enrollment to the verification signatures
    d=1 #just two counters to iterate through the list of the test/training signatures in slices
    e=0 #should have used slicing now that i think about it
    distance_dict = {}
    for user in tqdm(range(1,31)):
        user_sigs = signatures_training_normalized[d-1:d+4]
        d+=5
        verification_sigs = signatures_test_normalized[e:e+45]
        e+=45
        best_lst = []
        
        for i in verification_sigs:
            distances = []
            for j in user_sigs:
                distance = fastdtw(i, j,dist=euclidean)[0]
                distances.append(distance)
            best_lst.append(min(distances))
        #print(len(best_lst))
        distance_dict[user]=best_lst
        
    return distance_dict

#pickling the results as the distance measuring takes time
def pickling(dictionary, filename):
    import pickle
    with open(filename+".bin", "wb") as dictionary_file:
        pickle.dump(dictionary, dictionary_file)

#### run functions to get the two dictionarys that are used for creating the ranked list

var_dict = variance_dict(users, signatures_training_normalized)
distance_dict = create_distances(signatures_training_normalized,signatures_test_normalized)
pickling(distance_dict,"distance_dict_pickled")
pickling(var_dict,"variance_dict_pickled")









