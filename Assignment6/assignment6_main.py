from assignment6_psTools import *

def main(file_path, method):
    print(f'Loading data for {method}')

    pstool = PSTool()  # Instanciate object
    spk = pstool.pyspark_session('local[16]')  # start session
    # load data
    #     path = '/data/dataprocessing/interproscan/all_bacilli.tsv'
    schema = StructType([
        StructField("Protein_accession", StringType(), True),
        StructField("Sequence_MD5_digest", StringType(), True),
        StructField("Sequence_length", IntegerType(), True),
        StructField("Analysis", StringType(), True),
        StructField("Signature_accession", StringType(), True),
        StructField("Signature_description", StringType(), True),
        StructField("Start_location", IntegerType(), True),
        StructField("Stop_location", IntegerType(), True),
        StructField("Score", FloatType(), True),
        StructField("Status", StringType(), True),
        StructField("Date", StringType(), True),
        StructField("InterPro_annotations_accession", StringType(), True),
        StructField("InterPro_annotations_description", StringType(), True),
        StructField("GO_annotations", StringType(), True),
        StructField("Pathways_annotations", StringType(), True)])

    num_cols = ['Sequence_length', 'Start_location', 'Stop_location', 'Score']

    df = pstool.file_loader(file_path, '\t', spk, schema)
    df_munged = pstool.data_munger(df, maxsize=0.9)
    labels = pstool.get_array_from_df(df_munged, 'InterPro_annotations_accession')
    print(len(labels))
    print(labels)
    numeric_cols = pstool.get_array_from_df(df_munged, num_cols)

    sign_desc_array = pstool.words_to_array(df_munged, 'Signature_description')
    print(sign_desc_array)
    IP_annot_desc_array = pstool.words_to_array(df_munged, 'InterPro_annotations_description')
    print(IP_annot_desc_array)
    final_array = np.concatenate([numeric_cols, sign_desc_array, IP_annot_desc_array], axis=1)
    print(final_array)
    print(final_array.shape)
    print('Closing spark session')
    spk.sparkContext.stop()


if __name__ == "__main__":
    file_path = 'all_bacilli_subset.tsv'
    main(file_path, 'Random_forest')