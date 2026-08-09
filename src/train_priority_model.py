import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)
df = pd.read_csv("data/incidents_cleaned.csv")

print(df.head())
df = df[
    [
        "description",
        "impact",
        "urgency",
        "priority",
    ]
]

df.dropna(inplace=True)
X = df[
    [
        "description",
        "impact",
        "urgency",
    ]
]

y = df["priority"]
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
)
preprocessor = ColumnTransformer(
    transformers=[
        (
            "text",
            TfidfVectorizer(stop_words="english"),
            "description",
        ),
        (
            "cat",
            OneHotEncoder(handle_unknown="ignore"),
            ["impact", "urgency"],
        ),
    ]
)
model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        (
            "classifier",
            RandomForestClassifier(
                n_estimators=200,
                random_state=42,
            ),
        ),
    ]
)
model.fit(X_train, y_train)
predictions = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, predictions))

print(classification_report(y_test, predictions))

print(confusion_matrix(y_test, predictions))
joblib.dump(
    model,
    "models/priority_model.pkl",
)

print("Priority Model Saved")
sample = pd.DataFrame(
    [
        {
            "description": "VPN is not connecting",
            "impact": "High",
            "urgency": "High",
        }
    ]
)

prediction = model.predict(sample)

print("Predicted Priority:", prediction[0])
