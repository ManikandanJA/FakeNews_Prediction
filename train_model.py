import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier

df = pd.read_csv("news_dataset.csv")
df['label_num'] = df['label'].apply(lambda x: 1 if str(x).strip().lower() == 'real' else 0)

X = df['text']
y = df['label_num']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

vectorizer = TfidfVectorizer(stop_words='english', max_df=0.7)
tfidf_train = vectorizer.fit_transform(X_train)
tfidf_test  = vectorizer.transform(X_test)

model = PassiveAggressiveClassifier(max_iter=200)
model.fit(tfidf_train, y_train)

accuracy = model.score(tfidf_test, y_test) * 100
print(f"Model trained with accuracy: {accuracy:.2f}%")

model_data = {"model": model, "vectorizer": vectorizer}
with open("model.pkl", "wb") as f:
    pickle.dump(model_data, f)

print("model.pkl saved!")
