# Naive Bayes Spam Filter

This project provides a Python implementation of a **Naive Bayes classifier** for detecting spam emails based on word probabilities learned from labeled training data.

It includes:
- Tokenization of email content
- Log-probability calculation with Laplace smoothing
- A `SpamFilter` class to classify emails as spam or ham
- Functions to extract the most indicative words for each class

---

### Running the Classifier

1. Place your labeled training emails in the following structure:
data/training_data/spam/ spam1, spam2, spam_n
data/training_data/ham/ ham1, ham2, ham_n

2. Create a folder for test emails:
data/test_emails/ test1, test2, test_n

3. Run the test script:
python test_spam_filter.py

---

## Included Components

```load_tokens(email_path)```
Reads an email and returns a list of all tokens (words) in the body.

```log_probs(email_paths, smoothing)```
Computes smoothed log-probabilities of words from a set of email paths.

```SpamFilter(spam_dir, ham_dir, smoothing)```
Initializes the spam filter by calculating token probabilities and class priors from the provided spam and ham directories.

```is_spam(email_path)```
Classifies a given email as spam or not spam based on the learned model.

```most_indicative_spam(n)```
Returns the top n words most strongly associated with spam.

```most_indicative_ham(n)```
Returns the top n words most strongly associated with ham (non-spam).

---

## Sample Output

```filter = SpamFilter("training_data/spam", "training_data/ham", smoothing=1.0)```
```filter.is_spam("test_emails/test1")```  ➜ True or False

```filter.most_indicative_spam(5)```
➜ ['free', 'winner', 'buy', 'click', 'money']

```filter.most_indicative_ham(5)```
➜ ['meeting', 'project', 'schedule', 'team', 'update']
