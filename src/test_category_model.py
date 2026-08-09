import joblib
from preprocessing import clean_text

model = joblib.load("models/category_model.pkl")
tfidf = joblib.load("models/tfidf.pkl")

while True:
    issue = input("\nEnter an issue (type 'exit' to quit): ")

    if issue.lower() == "exit":
        break

    cleaned = clean_text(issue)

    vector = tfidf.transform([cleaned])

    prediction = model.predict(vector)

    print("Predicted Category:", prediction[0])