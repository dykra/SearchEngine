from flask import Flask, render_template, request
import os


from indexBuilder import IndexBuilder
from query import QueryMaker
import pickle
import time

app = Flask(__name__)


indexed_file = "./index.pickle"

indexBuilder = ""


directory_path_to_files = "../tmpfiles/"


def check_if_index_builder_is_made(normalisation=True, svd=False):

    if not os.path.isfile(indexed_file):
        global indexBuilder
        time1 = time.time()
        indexBuilder = IndexBuilder(directory_path=directory_path_to_files, stop_words_file=".././stopWordsFile.txt",
                                    normalisation=normalisation)
        if svd:
            indexBuilder.svd()
        time2 = time.time()
        print(time2-time1)
        binary_file = open(indexed_file, mode='wb')
        pickle.dump(indexBuilder, binary_file, protocol=pickle.HIGHEST_PROTOCOL)
        binary_file.close()

    else:
        global indexBuilder
        if indexBuilder == "":
            indexBuilder = pickle.load(open(indexed_file, 'rb'))


@app.route("/")
def main():
    check_if_index_builder_is_made()
    return render_template('index.html')


@app.route('/showResults', methods=['POST', 'GET'])
def showResults():
    time1 = time.time()
    query = request.form['inputQuery']
    query_maker = QueryMaker(query, 6, indexBuilder, normalization=False)
    query_maker.corelation()
    result_after = query_maker.result_files
    time2 = time.time()
    return render_template('results.html', query=query, result_files=result_after, time=time2-time1)


@app.route('/singleFile', methods=['POST'])
def singleFile():
    file_name = request.form['fileName']
    with open(directory_path_to_files + file_name, "r") as f:
        content = f.read()
    return render_template('singleFile.html', content=content, fileName=file_name)


if __name__ == "__main__":
    app.run()
