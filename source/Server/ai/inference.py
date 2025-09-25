from transformers import pipeline
import time


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
        model="source/Server/ai/Models/Luna-1",  # Use the saved model path
        tokenizer="distilbert-base-uncased",  # Match the tokenizer used in training
        device=-1,  # -1 = CPU, 0 = GPU (if available)
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
    ]

    # Run predictions
    for text in texts:
        start_time = time.time()
        result = classifier(text, truncation=True, max_length=128)[0]

        if result["label"] == "LABEL_0":
            result["label"] = "not spam"
        else:
            result["label"] = "spam"

        print(
            f"Text: {text}\nPrediction: {result}\n Inference Time: {time.time() - start_time:.4f} seconds\n"
        )
