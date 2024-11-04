from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib

# Improved dataset with a variety of safe and phishing messages
safe_messages = [
    "Let's meet up tomorrow for coffee.",
    "How are you doing?",
    "Just checking in to see if everything is okay.",
    "Meeting is scheduled for 3 PM. Please confirm.",
    "Here's the link to the project files.",
    "Reminder: The deadline for submission is next Friday.",
    "Your package will arrive soon.",
    "Can we have a call later today?",
    "Congratulations on your promotion!",
    "Here's the summary of the project we discussed.",
    "Thank you for your assistance on this matter.",
    "Please see the attached report.",
    "Looking forward to our meeting tomorrow.",
]

phishing_messages = [
    "Please reset your password immediately by clicking this link.",
    "You have won $1000! Click here to claim.",
    "Your account has been compromised. Provide login details now.",
    "Urgent! Verify your account by transferring funds.",
    "Congratulations, you've been selected. Click here to learn more.",
    "Immediate action required: Confirm your account.",
    "We detected suspicious activity in your account. Act now!",
    "You have a limited time to claim your prize. Don't miss out!",
    "Update your billing information to avoid service disruption.",
    "Your bank account is at risk! Log in here to secure it.",
    "Unusual activity detected. Verify your identity here.",
    "Click here to receive your cash reward.",
    "Your order could not be completed. Update your info here.",
]

# Combine safe and phishing messages into a single dataset
messages = safe_messages + phishing_messages
labels = [0] * len(safe_messages) + [1] * len(phishing_messages)  # 0 for safe, 1 for phishing

# Use TfidfVectorizer with n-grams for better context capture
vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words='english')  # Unigrams and bigrams
X = vectorizer.fit_transform(messages)

# Train a Naive Bayes classifier for text classification
model = MultinomialNB()
model.fit(X, labels)

# Save the trained model and vectorizer
joblib.dump(model, 'phishing_model.pkl')
joblib.dump(vectorizer, 'vectorizer.pkl')

print("Model and vectorizer saved successfully!")
