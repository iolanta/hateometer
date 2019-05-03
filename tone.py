import json
from sklearn.cluster import KMeans
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
import pickle
from nltk.corpus import stopwords

def text_classifier(vectorizer, transformer, classifier):
    return Pipeline(
            [("vectorizer", vectorizer),
            ("transformer", transformer),
            ("classifier", classifier)],
            )

def KMeansClustering(data):
    vectorizer = CountVectorizer(ngram_range = (1, 2))
    vect = vectorizer.fit_transform(data)
    transformer = TfidfTransformer()
    transform_data = transformer.fit_transform(vect)

    model = KMeans(n_clusters = 2)
    model.fit(transform_data)
    all_predictions = model.predict(transform_data)

    for i in range(0, len(data)):
        print(data[i])
        print(all_predictions[i])

def TestClassifier(all_comments, labels, sw_rus):
    vect = CountVectorizer(ngram_range = (1, 2))

    for clf in [MultinomialNB, LinearSVC, KNeighborsClassifier, LogisticRegression, DecisionTreeClassifier]:
        print(clf.__name__)
        print('precision: %f' % (cross_val_score(text_classifier(vect,
            TfidfTransformer(), clf()), all_comments, labels, scoring = 'precision', cv = 5).mean()))
        print('recall: %f' % (cross_val_score(text_classifier(vect,
            TfidfTransformer(), clf()), all_comments, labels, scoring = 'recall', cv = 5).mean()))

def TestRegression(all_comments, labels):
    vect = CountVectorizer(ngram_range = (1, 2))

    print('r2: %f' % (cross_val_score(text_classifier(vect, TfidfTransformer(), SVR(gamma='scale')), all_comments, labels, scoring = 'r2', cv = 5).mean()))

if __name__ == '__main__':
    pos_comments = []
    neg_comments = []

    with open('pos_comments.json', 'r') as f1, open('neg_comments.json', 'r') as f2:
        pos_comments = json.loads(f1.read())
        neg_comments = json.loads(f2.read())

    count_com = 520
    all_comments = pos_comments[0:count_com] + neg_comments[0:count_com]
    labels = [1] * count_com + [0] * count_com

    sw_rus = stopwords.words('russian')
    #TestClassifier(all_comments, labels, sw_rus)

    model = text_classifier(CountVectorizer(ngram_range = (1, 2)), TfidfTransformer(), LinearSVC())
    model.fit(all_comments, labels)

    #with open('model.bin', 'wb') as f:
    #    pickle.dump(model, f)

    with open('model.bin', 'rb') as f:
        loaded_model = pickle.load(f)
        print(loaded_model.decision_function(["Да этот сморчок уже для женщин не опасен.", "Главное чтобы голова не закружилась от таких стремительных успехов", "Прелесть...", "Хорошо хоть валежник разрешили бесплатно собирать."]))
        print(loaded_model.decision_function(["д'Артаньян? Или Тер-д'Артаньян?", "Женщину Морганом не назовут.", "Ты тоже можешь набрать кредитов и жить в комфорте и достатке.", "Орел вроде как совершенно китайская компания, не?"]))
        print(loaded_model.decision_function(["Получается одна большая корзина с яйцами, рискованно...", "лично я жду появления новых серий Сватов, а не всякую американскую муть.",  "Помолчи мусор с московских свалок.", "Смотри-ка, даже записные путирасты громят Милонова, будто он не член Единой России."]))
