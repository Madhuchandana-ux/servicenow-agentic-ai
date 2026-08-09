import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)

from preprocessing import clean_text
df = pd.read_csv("data/incidents_cleaned.csv")
df = df[["description", "category"]]
df.dropna(inplace=True)
df["clean_description"] = df["description"].apply(clean_text)
print(df.head())
X = df["clean_description"]

y = df["category"]
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)
tfidf = TfidfVectorizer(
    stop_words="english",
    max_features=5000
)

X_train = tfidf.fit_transform(X_train)

X_test = tfidf.transform(X_test)
model = LogisticRegression(max_iter=1000)

model.fit(X_train, y_train)
predictions = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, predictions))

print(classification_report(y_test, predictions))

print(confusion_matrix(y_test, predictions))
joblib.dump(model, "models/category_model.pkl")
joblib.dump(tfidf, "models/tfidf.pkl")

print("Model Saved Successfully")