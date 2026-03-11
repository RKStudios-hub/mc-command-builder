from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
import joblib
import os

texts = []
labels = []

with open("training/dataset.txt") as f:
    for line in f:
        text, label = line.strip().split("|")
        texts.append(text)
        labels.append(label)

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(texts)

model = LogisticRegression()
model.fit(X, labels)

os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/intent_model.pkl")
joblib.dump(vectorizer, "models/vectorizer.pkl")

print("Model trained successfully!")
