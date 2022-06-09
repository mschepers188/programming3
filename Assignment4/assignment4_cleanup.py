import pandas as pd
import shutil

# file = 'output.csv'
# rem_path = '/students/2021-2022/master/Martin_DSLS/output'


def get_best_kmer(file):
    out = pd.read_csv(file, names=['N50', 'Kmer_size'], header=None)
    best_kmer = out.sort_values('N50', ascending=False).iloc[0, 1]
    return best_kmer

def copy_file(src, dst):
    shutil.copyfile(src, dst)

if __name__ == "__main__":
    print('Getting best K_mer from csv')
    print(get_best_kmer('output/output.csv'))
    best_k = get_best_kmer('output/output.csv')
    best_k_path = f'/students/2021-2022/master/Martin_DSLS/output/{best_k}/contigs.fa'
    output_path = 'output/contigs.fa'
    print('Copying the file')
    copy_file(best_k_path, output_path)