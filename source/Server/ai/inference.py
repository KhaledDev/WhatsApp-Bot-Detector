from transformers import pipeline


class Inference:
    def __init__(self, model_path: str, device: int):
        self.classifier = pipeline(
            "text-classification",
            model=model_path,
            tokenizer="distilbert-base-uncased",
            device=device,  # -1 = CPU, 0 = GPU (if available)
        )

    def predict(self, text: str) -> int:
        result = self.classifier(text, truncation=True, max_length=128)[0]
        if result["label"] == "LABEL_0":
            return 0  # not spam
        else:
            return 1  # spam


if __name__ == "__main__":

    classifier = pipeline(
        "text-classification",
        model="source/Server/ai/Models/spam-detector",  # Use the saved model path
        tokenizer="distilbert-base-uncased",  # Match the tokenizer used in training
        device=-1,  # -1 = CPU, 0 = GPU (if available)
    )

    texts = [
        "Congratulations! You've won a free iPhone. Click here to claim your prize!",
        "Hey, are we still meeting for lunch tomorrow?",
        "URGENT: Your account has been compromised. Reset your password now.",
        "Man you suck!",
    ]

    # Run predictions
    for text in texts:
        result = classifier(text, truncation=True, max_length=128)[0]

        if result["label"] == "LABEL_0":
            result["label"] = "not spam"
        else:
            result["label"] = "spam"

        print(f"Text: {text}\nPrediction: {result}\n")
