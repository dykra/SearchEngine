import os
import math
import utils
import numpy as np
from scipy.sparse import csc_matrix
from scipy.sparse.linalg import svds, eigs


class IndexBuilder:
    def __init__(self, directory_path=".././tmpfiles", stop_words_file=".././stopWordsFile.txt", normalisation=False):
        self.normalisation = normalisation
        self.file_names = os.listdir(directory_path)
        self.directory_path = directory_path
        self.files_content = {}
        self.all_words_dict = {}
        self.all_words_list = []
        self.matrix_with_back_of_words = []
        self.stop_words_file = stop_words_file
        self.get_file_content()
        self.process_all_files()
        self.inverse_document_frequency()
        if self.normalisation:
            self.normalise_matrix()

    def normalise_matrix(self):
        for index in range(len(self.matrix_with_back_of_words)):
            max_elem = max(self.matrix_with_back_of_words[index])
            self.matrix_with_back_of_words[index] = [x/max_elem for x in self.matrix_with_back_of_words[index]]

    def inverse_document_frequency(self):
        N = len(self.matrix_with_back_of_words)
        for word in range(0, len(self.all_words_list)):
            n_w = 0
            for file in self.matrix_with_back_of_words:
                if file[word] != 0:
                    n_w += 1
            for file in range(0, len(self.file_names)):
                try:
                    factor = math.log(N, n_w)
                except Exception:
                    factor = 0
                self.matrix_with_back_of_words[file][word] *= factor

    def get_file_content(self):
        for file_name in self.file_names:
            f = open(self.directory_path + "/" + file_name, 'r').read().lower()
            self.files_content[file_name] = utils.format_text(f, self.stop_words_file)

    def process_all_files(self):

        for file_name, content in self.files_content.items():
            for word in content:
                self.all_words_dict[word] = ""
        self.all_words_list = list(self.all_words_dict)

        for file_name, content in self.files_content.items():
            file_words_dict = {}
            for word in content:
                if word in file_words_dict.keys():
                    file_words_dict[word] += 1
                else:
                    file_words_dict[word] = 1

            single_file_element = [0] * len(self.all_words_list)
            for index, element in enumerate(self.all_words_list):
                try:
                    value = file_words_dict[element]
                except KeyError:
                    value = 0

                single_file_element[index] = value
            self.matrix_with_back_of_words.append(single_file_element)

    def svd(self, k=23):
        matrix_csc = csc_matrix(self.matrix_with_back_of_words)
        u, s, v = svds(matrix_csc, k=k)
        S = np.diag(s)
        A = np.dot(u, np.dot(S, v))
        self.matrix_with_back_of_words = A
