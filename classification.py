import json
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer


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

def SplitComments(all_articles, fpos_name, fneg_name, fneut_name):
    pos_comments = []
    neg_comments = []
    neutral_comments = []

    with open(fpos_name, 'r') as fp:
        pos_comments = json.loads(fp.read())
    with open(fneg_name, 'r') as fn:
        neg_comments = json.loads(fn.read())
    with open(fneut_name, 'r') as fn:
        neutral_comments = json.loads(fn.read())

    answer = ""
    artc_to_delete = []
    end_flag = False

    for article in all_articles:

        if (end_flag == True):
            break

        title = article["name"]
        to_delete = []
        for comment in article["comments"]:
            answer = input("Название статьи: " + title + '\n' + "Комментарий: " + comment + '\n')

            # 1 - негативный, 2 - нейтральный, 3 - положительный
            if (answer == "1"):
                neg_comments.append(comment)
            else:
                if (answer == "3"):
                    pos_comments.append(comment)
                else:
                    if (answer == "2"):
                        neutral_comments.append(comment)
                    else:
                        end_flag = True
                        break
            to_delete.append(comment)

        for com in to_delete:
            article["comments"].remove(com)
        if(len(article["comments"]) == 0):
            artc_to_delete.append(article)

    for article in artc_to_delete:
        all_articles.remove(article)

    with open(fpos_name, 'w') as f_pos:
        f_pos.write(json.dumps(pos_comments, indent=2, ensure_ascii=False))
    with open(fneg_name, 'w') as f_neg:
        f_neg.write(json.dumps(neg_comments, indent=2, ensure_ascii=False))
    with open(fneut_name, 'w') as f_neut:
        f_neut.write(json.dumps(neutral_comments, indent=2, ensure_ascii=False))

    return all_articles


all_articles = []
with open('all_comments.json', 'r') as f:
    all_articles = json.loads(f.read())

all_articles = SplitComments(all_articles, "pos_comments.json", "neg_comments.json", "neutral_comments.json")

with open('all_comments.json', 'w') as f:
    f.write(json.dumps(all_articles, indent=2, ensure_ascii=False))
