from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import joblib

# Expanded synthetic dataset with balanced sample phishing and safe messages
messages = [
    "Please click this link to reset your password immediately.",  # Phishing
    "You have won a prize. Click here to claim it.",               # Phishing
    "Let’s catch up for lunch tomorrow.",                          # Safe
    "Your account has been compromised. Provide your login details here.",  # Phishing
    "The meeting is scheduled for 3 PM today.",                    # Safe
    "We detected unusual activity on your account. Verify here.",  # Phishing
    "Don't forget to submit the project by tomorrow.",             # Safe
    "Congratulations on your new job!",                            # Safe
    "Update your contact information for the upcoming event.",     # Safe
    "Urgent: verify your account to avoid suspension.",            # Phishing
    "Our meeting is at 2 PM in the main office.",                  # Safe
    "Get exclusive access to deals by clicking this link.",        # Phishing
]

# Labels indicating phishing (1) or safe (0)
labels = [1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1]  # Balanced dataset

# Train a simple phishing detection model
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(messages)

# Split data into training and testing to evaluate performance
X_train, X_test, y_train, y_test = train_test_split(X, labels, test_size=0.3, random_state=42)

# Initialize Logistic Regression with higher regularization to prevent overfitting
model = LogisticRegression(C=0.5)  # C < 1 increases regularization
model.fit(X_train, y_train)

# Check model performance
train_accuracy = model.score(X_train, y_train)
test_accuracy = model.score(X_test, y_test)
print(f"Training Accuracy: {train_accuracy * 100:.2f}%")
print(f"Test Accuracy: {test_accuracy * 100:.2f}%")

# Save the model and vectorizer
joblib.dump(model, 'phishing_model.pkl')
joblib.dump(vectorizer, 'vectorizer.pkl')
