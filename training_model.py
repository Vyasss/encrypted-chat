from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib

# Synthetic dataset with sample phishing and safe messages
messages = [
    "Please click this link to reset your password immediately.",
    "You have won a prize. Click here to claim it.",
    "Let’s catch up for lunch tomorrow.",
    "Your account has been compromised. Provide your login details here.",
    "The meeting is scheduled for 3 PM today.",
    "We detected unusual activity on your account. Verify here."
]
labels = [1, 1, 0, 1, 0, 1]  # 1: phishing, 0: safe

# Train a simple phishing detection model
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(messages)
model = LogisticRegression()
model.fit(X, labels)

# Save the model and vectorizer
joblib.dump(model, 'phishing_model.pkl')
joblib.dump(vectorizer, 'vectorizer.pkl')
