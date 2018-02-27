import utils
import numpy as np


class QueryMaker:

    def __init__(self, query_text, amount_of_documents_to_give, index_builder, normalization):
        self.query_text = query_text
        self.indexBuilder = index_builder
        self._prepare_query_test()
        self.query_back_of_words = []
        self.prepare_back_of_words_for_query()
        self.amount_of_documents_to_give = amount_of_documents_to_give
        self.result_files = []
        self.normalization = normalization
        self.normalise_query()

    def normalise_query(self):
        if self.normalization:
            query_max_elem = max(self.query_back_of_words)
            if query_max_elem != 0:
                self.query_back_of_words = [x / query_max_elem for x in self.query_back_of_words]

    def corelation(self):
        transposed_query = []
        for i in self.query_back_of_words:
            transposed_query.append([i])

        if not self.normalization:
            query_norm = np.linalg.norm(self.query_back_of_words)
            A_e_norm = np.linalg.norm(self.indexBuilder.matrix_with_back_of_words[0])

        result = {}
        for j, file_name in enumerate(self.indexBuilder.file_names):
            if not self.normalization:
                result[file_name] = np.dot(self.indexBuilder.matrix_with_back_of_words[j], transposed_query)/(query_norm*A_e_norm) # teraz wezmiemy najwieksze wartosci
            else:
                result[file_name] = np.dot(self.indexBuilder.matrix_with_back_of_words[j], transposed_query)
        sorted_result = sorted(result, key=result.get)[:self.amount_of_documents_to_give]
        self.result_files = sorted_result

    def _prepare_query_test(self):
        self.query_text = self.query_text.lower()
        self.query_text = utils.format_text(self.query_text, self.indexBuilder.stop_words_file)

    def prepare_back_of_words_for_query(self):
        self.query_back_of_words = [0] * len(self.indexBuilder.all_words_list)
        dict_words = {}
        for word in self.query_text:
            if word in dict_words.keys():
                dict_words[word] += 1
            else:
                dict_words[word] = 1
        for index, base_word in enumerate(self.indexBuilder.all_words_list):
            if base_word in dict_words.keys():
                self.query_back_of_words[index] = dict_words[base_word]

