from transformers import pipeline

classifier = pipeline(
    "text-classification",
    model="bert-base-uncased",  # BERT-base (110M params)
    tokenizer="bert-base-uncased",
    device=-1,  # -1 = CPU, 0 = GPU (if available)
)

texts = [
    "Congratulations! You've won a free iPhone. Click here to claim your prize!",
    "Hey, are we still meeting for lunch tomorrow?",
    "URGENT: Your account has been compromised. Reset your password now.",
]

if __name__ == "__main__":
    # Run predictions
    for text in texts:
        result = classifier(text, truncation=True, max_length=128)[0]
        print(f"Text: {text}\nPrediction: {result}\n")
