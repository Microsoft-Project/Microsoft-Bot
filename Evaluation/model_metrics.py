import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC


def accuaracy_comp(features, labels):
    models = [
        RandomForestClassifier(n_estimators=200, max_depth=3, random_state=0),
        LinearSVC(),
        MultinomialNB(),
        LogisticRegression(random_state=0),
    ]

    CV = 5
    cv_df = pd.DataFrame(index=range(CV * len(models)))
    entries = []
    print("Models are created! Time to calculates the accuracies")
    count = 0
    for model in models:
        print("INSIDE FOR LOOP")
        model_name = str(count)
        count = count + 1
        accuracies = cross_val_score(model, features, labels, scoring='accuracy', cv=CV)
        print("Doing this for each model")

        for fold_idx, accuracy in enumerate(accuracies):
            entries.append((model_name, fold_idx, accuracy))
    cv_df = pd.DataFrame(entries, columns=['model_name', 'fold_idx', 'accuracy'])
    sns.boxplot(x='model_name', y='accuracy', data=cv_df)
    sns.stripplot(x='model_name', y='accuracy', data=cv_df,
                  size=8, jitter=True, edgecolor="gray", linewidth=2)
    plt.show()
    print(cv_df.groupby('model_name').accuracy.mean())


def confu_gen(model_name, features, labels, testSize, df):
    category_id_df = df[['labels', 'category_id']].drop_duplicates().sort_values('category_id')

    if model_name is "lgr":
        model = LogisticRegression()
    elif model_name is "lsvc":
        model = LinearSVC()
    elif model_name is "forest":
        model = RandomForestClassifier()
    else:
        model = MultinomialNB()

    # X_train, X_test, y_train, y_test = train_test_split(df['body_title'], df['labels'], random_state=1)

    X_train, X_test, y_train, y_test, indices_train, indices_test = train_test_split(features, labels, df.index,
                                                                                     test_size=testSize, random_state=1)

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    conf_mat = confusion_matrix(y_test, y_pred)
    fig, ax = plt.subplots(figsize=(10, 10))
    sns.heatmap(conf_mat, annot=True, fmt='d',
                xticklabels=category_id_df.labels.values, yticklabels=category_id_df.labels.values)
    plt.ylabel('Actual')
    plt.xlabel('Predicted')
    plt.show()
