from datasets import (
    load_dataset,
    DatasetDict,
    Dataset,
    IterableDatasetDict,
    IterableDataset,
)
from transformers import (
    AutoTokenizer,
    TrainingArguments,
    Trainer,
    AutoModelForSequenceClassification,
)


def load_spam_dataset(location: str) -> DatasetDict:
    dataset: DatasetDict | Dataset | IterableDatasetDict | IterableDataset = (
        load_dataset("csv", data_files=location)
    )
    return dataset


def main():
    dataset: DatasetDict = load_spam_dataset("source/Server/ai/Data/spam.csv")

    # Split the dataset into train and test (80/20 split)
    train_test_split = dataset["train"].train_test_split(test_size=0.2, seed=42)
    dataset = DatasetDict(
        {"train": train_test_split["train"], "test": train_test_split["test"]}
    )

    tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")

    def preprocess_function(examples):
        # Convert string labels to integers: HAM=0, SPAM=1
        labels = [0 if label == "HAM" else 1 for label in examples["label"]]
        tokenized = tokenizer(
            examples["sms"], padding="max_length", truncation=True, max_length=128
        )
        tokenized["labels"] = labels
        return tokenized

    tokenized_datasets = dataset.map(preprocess_function, batched=True)
    tokenized_datasets.set_format(
        "torch", columns=["input_ids", "attention_mask", "labels"]
    )

    model = AutoModelForSequenceClassification.from_pretrained(
        "distilbert-base-uncased", num_labels=2
    )

    training_args = TrainingArguments(
        output_dir="./results",
        eval_strategy="epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=16,
        per_device_eval_batch_size=16,
        num_train_epochs=20,
        weight_decay=0.01,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_datasets["train"],
        eval_dataset=tokenized_datasets["test"],
    )

    trainer.train()

    return model


if __name__ == "__main__":
    final_model = main()
    print("Training completed successfully!")
    print(f"Model: {final_model}")
    # save the model to a directory
    final_model.save_pretrained("source/Server/ai/Models/spam-detector")
