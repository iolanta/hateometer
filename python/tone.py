import json
from sklearn.cluster import KMeans
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
import pickle
from nltk.corpus import stopwords
import re
import pymorphy2

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

def ModifyComment(comment):
    list_words = re.split("[\\s+|\\,+|\\.+|\\:+|\\?+]",comment)
    list_words = list(filter(lambda x: x != '', list_words))
    morph = pymorphy2.MorphAnalyzer()
    for i in range(0,len(list_words)):
        list_words[i] = morph.parse(list_words[i])[0].normal_form

    comment = ' '.join(list_words)
    return comment

def new_preprocessor(str):
    str = str.lower()
    str = re.sub("(\\s+!+)", "!", str)
    str = re.sub("(\s+\(+)", "(", str)
    str = re.sub("(\s+\)+)", ")", str)
    return str

def PreprocessingNegations(comment):
    comment = comment.lower()
    comment = re.sub(r"([.,!;:\(\)])", r" \1 ", comment)
    list_tokens = re.split("\\s+", comment)
    is_neg = False

    for i in range(0, len(list_tokens)):
        if(list_tokens[i] == "не"):
            if(not is_neg):
                is_neg = True
                list_tokens[i] = ''
            else:
                is_neg = False
        elif(re.search("[.,!?;:()]", list_tokens[i]) != None):
            is_neg = False
        elif(is_neg):
            list_tokens[i] = "не"+list_tokens[i]

    comment = ' '.join(list_tokens)
    return comment


def TestClassifier(all_comments, labels, sw_rus):
    all_comments = list(map(ModifyComment, all_comments))
    all_comments = list(map(PreprocessingNegations, all_comments))
    vect = CountVectorizer(ngram_range = (1, 2), lowercase = False, preprocessor = new_preprocessor,  token_pattern = "[а-яa-z]+[!|\\)|\\(]*", analyzer = "word", stop_words = sw_rus)

    for clf in [MultinomialNB(), LinearSVC(), LogisticRegression(solver='liblinear')]:
        print(type(clf))
        print('precision: %f' % (cross_val_score(text_classifier(vect,
            TfidfTransformer(), clf), all_comments, labels, scoring = 'precision', cv = 5).mean()))
        print('recall: %f' % (cross_val_score(text_classifier(vect,
            TfidfTransformer(), clf), all_comments, labels, scoring = 'recall', cv = 5).mean()))
        print('f1: %f' % (cross_val_score(text_classifier(vect,
            TfidfTransformer(), clf), all_comments, labels, scoring = 'f1', cv = 5).mean()))


def TestPreproc(all_comments, count_pos, count_neg):
    all_comments = list(map(PreprocessingNegations, all_comments))

    vectorizer = CountVectorizer(ngram_range = (1, 3), lowercase = False, preprocessor = new_preprocessor,  token_pattern = "[а-яa-z]+[!|\\)|\\(]*", analyzer = "word")
    X = vectorizer.fit_transform(all_comments[0:count_pos-1])
    print(len(vectorizer.get_feature_names()))

    vectorizer_neg = CountVectorizer(ngram_range = (1, 3), lowercase = False, preprocessor = new_preprocessor,  token_pattern = "[а-яa-z]+[!|\\)|\\(]*", analyzer = "word")
    X = vectorizer_neg.fit_transform(all_comments[count_pos:count_pos+count_neg])
    print(len(vectorizer_neg.get_feature_names()))

def FitModel(all_comments, labels):
    all_comments = list(map(ModifyComment, all_comments))
    all_comments = list(map(PreprocessingNegations, all_comments))
    model = text_classifier(CountVectorizer(ngram_range = (1, 2), lowercase = False, preprocessor = new_preprocessor,  token_pattern = "[а-яa-z]+[!|\\)|\\(]*", analyzer = "word"),
        TfidfTransformer(), LinearSVC())
    model.fit(all_comments, labels)

    with open('model.bin', 'wb') as f:
        pickle.dump(model, f)

if __name__ == '__main__':
    pos_comments = []
    neg_comments = []

    with open('pos_comments.json', 'r') as f1, open('neg_comments.json', 'r') as f2:
        pos_comments = json.loads(f1.read())
        neg_comments = json.loads(f2.read())

    count_pos = 600
    count_neg = 600

    all_comments = pos_comments[0:count_pos] + neg_comments[0:count_neg]
    labels = [1] * count_pos + [0] * count_neg

    sw_rus = stopwords.words('russian')

    #TestClassifier(all_comments, labels, sw_rus)
    #FitModel(all_comments, labels)

    with open('model.bin', 'rb') as f:
        loaded_model = pickle.load(f)
        print(loaded_model.decision_function(["Да этот сморчок уже для женщин не опасен.", "Главное чтобы голова не закружилась от таких стремительных успехов", "Прелесть...", "Хорошо хоть валежник разрешили бесплатно собирать."]))
        print(loaded_model.decision_function(["д'Артаньян? Или Тер-д'Артаньян?", "Женщину Морганом не назовут.", "Ты тоже можешь набрать кредитов и жить в комфорте и достатке.", "Орел вроде как совершенно китайская компания, не?"]))
        print(loaded_model.decision_function(["Получается одна большая корзина с яйцами, рискованно...", "лично я жду появления новых серий Сватов, а не всякую американскую муть.",  "Помолчи мусор с московских свалок.", "Смотри-ка, даже записные путирасты громят Милонова, будто он не член Единой России."]))
