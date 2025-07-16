import email
from collections import Counter
from math import log, exp
import os

"""
A minimal system for spam filtering made by processing the raw training data, 
estimating the conditional probability distributions of the words in the vocabulary 
determined by each document class, then using a naive Bayes model to make predictions on the test set.
"""

def load_tokens(email_path):
    """Extract tokens (words) from an email file"""
    with open(email_path, "r") as f:
        message = email.message_from_file(f)
        tokens = []
        for line in email.iterators.body_line_iterator(message):
            tokens += line.split() # Splits the words by whitespace
    return tokens
        
def log_probs(email_paths, smoothing):
    """Calculate log probabilities of tokens from a list of emails with smoothing"""
    tokens = []
    for path in email_paths:
        tokens += load_tokens(path)

    vocab = set(tokens) # Ensures unique words
    word_counts = Counter(tokens)
    total_words = len(tokens)
    denom = total_words + smoothing * (len(vocab) + 1) # Denominator for smoothing

    # Computes the log probabilities with smoothing
    probs = {word: log((count + smoothing) / denom) for word, count in word_counts.items()}
    probs["<UNK>"] = log(smoothing / denom)
    return probs

class SpamFilter(object):

    def __init__(self, spam_dir, ham_dir, smoothing):
        """
        Train the spam filter using directories of spam and ham emails
        Builds word probability dictionaries and computes prior class probabilities
        """

        self.smoothing = smoothing

        # Get full paths to spam and ham email files
        spam_paths = [os.path.join(spam_dir, f) for f in os.listdir(spam_dir)]
        ham_paths = [os.path.join(ham_dir, f) for f in os.listdir(ham_dir)]

        # Calculate token log-probabilities for both spam and ham
        self.spam_p_dict = log_probs(spam_paths, smoothing)
        self.ham_p_dict = log_probs(ham_paths, smoothing)

        # Compute class priors based on number of training examples
        total = len(spam_paths) + len(ham_paths)
        self.spam_prob = len(spam_paths) / total
        self.ham_prob = len(ham_paths) / total
    
    def is_spam(self, email_path):
        """
        Classify an email as spam or ham based on learned probabilities
        Uses Naive Bayes to compute log-likelihoods and compares them
        """
        tokens = load_tokens(email_path)
        token_counts = Counter(tokens)

        # Start with the log prior probabilities
        spam_score = log(self.spam_prob)
        ham_score = log(self.ham_prob)

        # Add log-probability of each word in the message
        for word, count in token_counts.items():
            spam_score += self.spam_p_dict.get(word, self.spam_p_dict["<UNK>"]) * count
            ham_score += self.ham_p_dict.get(word, self.ham_p_dict["<UNK>"]) * count

        # If the spam score is higher, classify as spam
        return spam_score > ham_score

    def most_indicative_spam(self, n):
        """
        Return the n words most indicative of spam
        Computes indication using log(P(w|spam) / P(w))
        """
         
        indicative = {}
        for word in self.spam_p_dict:
            if word in self.ham_p_dict:
                # P(w) = P(w|spam) * P(spam) + P(w|ham) * P(ham)
                pw = (exp(self.spam_p_dict[word]) * self.spam_prob +
                      exp(self.ham_p_dict[word]) * self.ham_prob)
                indicative[word] = log(exp(self.spam_p_dict[word]) / pw)
        return sorted(indicative, key=indicative.get, reverse=True)[:n]

    def most_indicative_ham(self, n):
        """
        Return the n words most indicative of ham
        Computes indication using log(P(w|ham) / P(w))
        """
        indicative = {}
        for word in self.ham_p_dict:
            if word in self.spam_p_dict:
                # P(w) = P(w|spam) * P(spam) + P(w|ham) * P(ham)
                pw = (exp(self.spam_p_dict[word]) * self.spam_prob +
                      exp(self.ham_p_dict[word]) * self.ham_prob)
                indicative[word] = log(exp(self.ham_p_dict[word]) / pw)
        return sorted(indicative, key=indicative.get, reverse=True)[:n]