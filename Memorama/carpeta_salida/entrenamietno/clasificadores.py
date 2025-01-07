import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

df = pd.read_csv("dataset.csv")
X = df.drop(["nombre_archivo", "clase"], axis=1)
y = df["clase"]

clf = RandomForestClassifier(n_estimators=100, criterion='gini', random_state=42)
clf.fit(X, y)
joblib.dump(clf, "model.pkl")
