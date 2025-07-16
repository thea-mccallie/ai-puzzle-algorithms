import os
from spam_filter import SpamFilter

spam_dir = "data/training/spam"
ham_dir = "data/training/ham"

# Initialize the spam filter with a small smoothing value (Laplace smoothing)
filter = SpamFilter(spam_dir, ham_dir, smoothing=1.0)

# Create a list of test email paths
test_dir = "data/testing" 
test_emails = [os.path.join(test_dir, f) for f in os.listdir(test_dir)]

# Classify each test email and print result
print("Test Email Classifications:\n")
for path in test_emails:
    label = "SPAM" if filter.is_spam(path) else "HAM"
    print(f"{os.path.basename(path)} => {label}")

# Bonus: show the most indicative words
print("\nMost Indicative Spam Words:")
print(filter.most_indicative_spam(10))

print("\nMost Indicative Ham Words:")
print(filter.most_indicative_ham(10))