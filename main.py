import tools.signature_data_reader_cuba as reader
import tools.signature_data_normalizer_cuba as normalizer
import tools.signature_data_preprocessing_cuba as preprocessor
import tools.dtw_cuba as dtw
import tools.evaluation_verificator_cuba as verificator


if __name__ == '__main__':

    """ ### this chapter manages loading and processing our data ### """

    # Load Data
    dict_raw_enrollment_data, dict_raw_verification_data, dict_gt_labels = reader.read_data("./data/")

    # Process our 7 feature arrays to 5 feature arrays (with awesome new features)
    dict_enrollment_data = preprocessor.preprocess(dict_raw_enrollment_data)
    dict_verification_data = preprocessor.preprocess(dict_raw_verification_data)

    # Normalize values of our arrays for smoother dtw action
    dict_enrollment_norm, dict_verification_norm = normalizer.normalize(dict_enrollment_data, dict_verification_data)

    """ ### this chapter manages the steps where we actively rely on a dtw algorithm ### """

    # dtw time, get the 1st standard deviation quantiles for the dissimilarities within users!
    print("\n", "Calculating variance and mean within users")
    dict_ignore, dict_also_ignore, dict_1sd_intervals = dtw.calculate_variance_within_users(dict_enrollment_norm)

    # now get the dissimilarity indices between all enrollment signatures and their verification signatures!
    print("\n", "Calculating dissimilarities between datasets")
    dict_dissimilarities = dtw.calculate_dissimilarities_between_datasets(dict_enrollment_norm, dict_verification_norm)

    """ ### this chapter deals with the evaluation of our dtw data ### """

    # WIP todo @evaluation team

    # find true positives and true negatives: 2 conditions
    #  1. verification signatures that have all 5 dissimilarity scores in an interval that fits inside 1 SD
    #  2. they have a ground truth (gt.txt) label of "g" for TP's and "t" for FP's
    dict_TPs_FPs = verificator.find_nTP_and_nFP_1SD(dict_dissimilarities, dict_1sd_intervals, dict_gt_labels)
    print(dict_TPs_FPs)
