import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.feature_selection import RFE
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
import pickle

# Load and preprocess data
data = pd.read_csv('D:\MINI PROJECT\Cardio Vascular Diseases\Prediction\heart (3).csv')
data['Sex'] = data['Sex'].map({'M': 1, 'F': 0})
data['ChestPainType'] = data['ChestPainType'].map({'ASY': 3, 'ATA': 2, 'NAP': 1, 'TA': 0})
data['RestingECG'] = data['RestingECG'].map({'LVH': 2, 'Normal': 1, 'ST': 0})
data['ExerciseAngina'] = data['ExerciseAngina'].map({'Y': 1, 'N': 0})
data['ST_Slope'] = data['ST_Slope'].map({'Down': 2, 'Flat': 1, 'Up': 0})

X = data.drop('HeartDisease', axis=1)
y = data['HeartDisease']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model setup
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rfe = RFE(estimator=rf, n_features_to_select=8)
rfe.fit(X_train, y_train)

X_train_rfe = rfe.transform(X_train)
X_test_rfe = rfe.transform(X_test)

# Train multiple models
knn = KNeighborsClassifier(n_neighbors=5)
svm = SVC(probability=True, random_state=42)
lr = LogisticRegression(random_state=42)
xgb = XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42)

# Voting Classifier
voting_clf = VotingClassifier(estimators=[
    ('rf', rf),
    ('knn', knn),
    ('svm', svm),
    ('lr', lr),
    ('xgb', xgb)
], voting='soft')

voting_clf.fit(X_train_rfe, y_train)


def predict_heart_disease(user_input):
    user_input_rfe = rfe.transform(user_input)
    prediction = voting_clf.predict(user_input_rfe)
    return prediction[0]
