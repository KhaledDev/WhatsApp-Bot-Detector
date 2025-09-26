from transformers import pipeline
import time
import torch
import random
import numpy as np


class Inference:
    def __init__(self, model_path: str, device: int, spam_threshold: float = 0.75):
        # Set seeds for more consistent results
        torch.manual_seed(42)
        random.seed(42)
        np.random.seed(42)

        self.spam_threshold = spam_threshold
        self.classifier = pipeline(
            "text-classification",
            model=model_path,
            tokenizer="distilbert-base-uncased",
            device=device,  # -1 = CPU, 0 = GPU (if available)
        )

    def predict(self, text: str) -> int:
        result = self.classifier(text, truncation=True, max_length=128)[0]

        # Only classify as spam if confidence is above threshold
        if result["label"] == "LABEL_1" and result["score"] >= self.spam_threshold:
            return 1  # spam
        else:
            return 0  # not spam (default to safe side)

    def predict_with_confidence(self, text: str) -> dict:
        """Returns prediction with confidence score for debugging"""
        result = self.classifier(text, truncation=True, max_length=128)[0]

        prediction = (
            1
            if (result["label"] == "LABEL_1" and result["score"] >= self.spam_threshold)
            else 0
        )

        return {
            "prediction": prediction,
            "confidence": result["score"],
            "raw_label": result["label"],
            "is_spam": prediction == 1,
        }

    def predict_averaged(self, text: str, num_runs: int = 3) -> int:
        """Run multiple predictions and use majority vote for more consistency"""
        predictions = []
        for _ in range(num_runs):
            result = self.classifier(text, truncation=True, max_length=128)[0]
            if result["label"] == "LABEL_1" and result["score"] >= self.spam_threshold:
                predictions.append(1)
            else:
                predictions.append(0)

        # Use majority vote
        return 1 if sum(predictions) >= (num_runs // 2 + 1) else 0


if __name__ == "__main__":
    # Initialize the improved inference class with confidence threshold
    spam_detector = Inference(
        model_path="source/Server/ai/Models/Luna-1",
        device=-1,  # -1 = CPU, 0 = GPU (if available)
        spam_threshold=0.75,  # Only classify as spam if 75% confident or higher
    )

    texts = [
        "Congratulations! You've won a free iPhone. Click here to claim your prize!",
        "Hey, are we still meeting for lunch tomorrow?",
        "URGENT: Your account has been compromised. Reset your password now.",
        "Man you suck!",
        "كيف حالك خالد بدي اسألك ماخذين شي واجبات بالprobability ؟",
        "also AI is like mostly done just need to finalize the dataset and then fine-tune the model one last time, and then connect the javascript stuff to the ai and then I'll deploy it to the three groups I have admin in to just test it out",
        "🎁You're 1 click away from winning amazing freebies! Grab now before they're gone! 🕙🕙🕙 Accept my invitation and win free gifts on SHEIN https://onelink.shein.com/14/4uo3gu734kkr",
        "Win $1000 cash instantly! Text WINNER to 12345 now!!!",
        "مرحبا صديقي، شو رأيك نروح نتمشى اليوم؟",
        "Can you help me with the math homework tonight?",
        "🔥🔥LAST CHANCE🔥🔥 Claim your FREE crypto bonus before midnight!",
        "أخي محمد، بدي أسأل عن موعد الامتحان النهائي، هل تعرف؟",
        "Your package delivery failed. Update your address here: bit.ly/fake-link",
        "Thanks for yesterday, really had a great time catching up!",
        "مبروك! فزت بجائزة 10000 دولار! اضغط هنا للحصول على الجائزة",
        "Let's grab coffee this weekend if you're free",
        "شو أخبار المشروع؟ خلصت الجزء اللي عليك؟",
        "نقدم جميع الخدمات الطلابية : Quizzes Mid Exam  Final Exam Assigment Project Homework 🪀https://wa.me/+967733534371 𝐆𝐮𝐚𝐫𝐚𝐧𝐭𝐞𝐞𝐝 𝐠𝐫𝐚𝐝𝐞 99.9%👌",
        "surely she will work this time 😭",
        "😭😭😭",
        "😂😂😂",
        "NAHH 😂😂",
    ]

    # Run predictions with detailed output for debugging
    for text in texts:
        start_time = time.time()

        # Get detailed prediction info
        detailed_result = spam_detector.predict_with_confidence(text)

        # Also get averaged prediction for comparison
        averaged_prediction = spam_detector.predict_averaged(text, num_runs=3)

        inference_time = time.time() - start_time

        print(f"Text: {text}")
        print(
            f"Prediction: {'SPAM' if detailed_result['prediction'] == 1 else 'NOT SPAM'}"
        )
        print(f"Confidence: {detailed_result['confidence']:.3f}")
        print(f"Raw Label: {detailed_result['raw_label']}")
        print(
            f"Averaged (3 runs): {'SPAM' if averaged_prediction == 1 else 'NOT SPAM'}"
        )
        print(f"Inference Time: {inference_time:.4f} seconds")
        print("-" * 80)

    print("\nTesting Consistency (Run same text multiple times)\n")
    test_text = "Hey, are we still meeting for lunch tomorrow?"
    print(f"Testing consistency with: '{test_text}'")

    for i in range(5):
        result = spam_detector.predict_with_confidence(test_text)
        print(
            f"Run {i+1}: {'SPAM' if result['prediction'] == 1 else 'NOT SPAM'} (confidence: {result['confidence']:.3f})"
        )
