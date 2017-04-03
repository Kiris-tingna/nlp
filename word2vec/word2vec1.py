from gensim.models import Word2Vec, LdaModel


class MyCorpus(object):
    def __init__(self, docs):
        self.docs = docs

    def __iter__(self):
        for line in self.docs:
            yield line.split()


if __name__ == "__main__":
    documents = ["Human machine interface for lab abc computer applications",
                 "A survey of user opinion of computer system response time",
                 "The EPS user interface management system",
                 "System and human system engineering testing of EPS",
                 "Relation of user perceived response time to error measurement",
                 "The generation of random binary unordered trees",
                 "The intersection graph of paths in trees",
                 "Graph minors IV Widths of trees and well quasi ordering", "Graph minors A survey"]

    corpuss = MyCorpus(documents)

    model = Word2Vec(corpuss, size=10, window=2, min_count=0)
    print    (model["Human"])
    print    (model.similarity('Human', 'system'))
    print(model.similarity('Human', 'user'))
