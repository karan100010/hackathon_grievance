import pandas as pd
from sklearn.model_selection import train_test_split
from transformers import AlbertForSequenceClassification, AlbertTokenizer
import torch
from datasets import ClassLabel
from torch.utils.data import TensorDataset, DataLoader
import torch.optim as optim


# Define hyperparameters
batch_size = 32
num_epochs = 1
learning_rate = 2e-5
num_classes = 1155

# Load the extended dataset
dataset_path = "data\cleaned\cleaned_and_preprocessed.csv"
df = pd.read_csv(dataset_path)

# Split the dataset into train, validation, and test sets
train_df, temp_df = train_test_split(df, test_size=0.2, random_state=42)
val_df, test_df = train_test_split(temp_df, test_size=0.5, random_state=42)

# Initialize the ALBERT tokenizer
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")
model_name = "albert-base-v2"
tokenizer = AlbertTokenizer.from_pretrained(model_name)
model = AlbertForSequenceClassification.from_pretrained(
    model_name, num_labels=num_classes).to(device)


# Tokenize the datasets
def tokenize_dataset(df):
    return tokenizer(df['subject_content_text'].tolist(), padding=True, truncation=True, return_tensors="pt")


train_inputs = tokenize_dataset(train_df)
val_inputs = tokenize_dataset(val_df)
test_inputs = tokenize_dataset(test_df)


train_labels = train_df['label'].tolist()
val_labels = val_df['label'].tolist()
test_labels = test_df['label'].tolist()
label_classes = []

with open("E:\hackathon\data\cleaned\labels.txt", "r") as f:
    for line in f:
        label_classes.append(line.replace("\n", ""))


c2l = ClassLabel(num_classes=num_classes, names=label_classes)


train_label_encodings = [c2l.str2int(label) for label in train_labels]
val_label_encodings = [c2l.str2int(label) for label in val_labels]
test_label_encodings = [c2l.str2int(label) for label in test_labels]


print("Train Labels: ", train_label_encodings)
print("Val Labels: ", val_label_encodings)
print("Test Labels: ", test_label_encodings)
# # Convert labels to tensors
train_labels = torch.tensor(train_label_encodings)
val_labels = torch.tensor(val_label_encodings)
test_labels = torch.tensor(test_label_encodings)


train_dataset = TensorDataset(
    train_inputs['input_ids'], train_inputs['attention_mask'], train_labels)
val_dataset = TensorDataset(
    val_inputs['input_ids'], val_inputs['attention_mask'], val_labels)
test_dataset = TensorDataset(
    test_inputs['input_ids'], test_inputs['attention_mask'], test_labels)


train_dataloader = DataLoader(
    train_dataset, batch_size=batch_size, shuffle=True)
val_dataloader = DataLoader(val_dataset, batch_size=batch_size)
test_dataloader = DataLoader(test_dataset, batch_size=batch_size)


# Define optimizer and scheduler
optimizer = optim.AdamW(model.parameters(), lr=learning_rate)

print("Training Started...")

# Training loop
for epoch in range(num_epochs):
    model.train()
    total_loss = 0

    for batch_idx, batch in enumerate(train_dataloader):
        inputs = {
            "input_ids": batch[0].to(device),
            "attention_mask": batch[1].to(device),
            "labels": batch[2].to(device)
        }

        # Forward pass
        outputs = model(**inputs)
        loss = outputs.loss

        # Backward pass and optimization
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()

        total_loss += loss.item()

        if (batch_idx + 1) % 10 == 0:  # Print every 10 batches
            print(
                f"Epoch {epoch + 1}/{num_epochs} - Batch {batch_idx + 1}/{len(train_dataloader)} - Loss: {loss.item():.4f}")

    # Calculate average training loss for the epoch
    avg_train_loss = total_loss / len(train_dataloader)
    print(
        f"Epoch {epoch + 1}/{num_epochs} - Avg Train Loss: {avg_train_loss:.4f}")

    # Validation loop
    model.eval()
    val_loss = 0
    num_correct = 0

    with torch.no_grad():
        for batch_idx, batch in enumerate(val_dataloader):
            inputs = {
                "input_ids": batch[0].to(device),
                "attention_mask": batch[1].to(device),
                "labels": batch[2].to(device)
            }

            # Forward pass
            outputs = model(**inputs)
            loss = outputs.loss
            val_loss += loss.item()

            # Evaluate correctness
            logits = outputs.logits
            predictions = torch.argmax(logits, dim=1)
            num_correct += (predictions == batch[2].to(device)).sum().item()

    # Calculate average validation loss and accuracy for the epoch
    avg_val_loss = val_loss / len(val_dataloader)
    accuracy = num_correct / len(val_dataloader.dataset)
    print(
        f"Epoch {epoch + 1}/{num_epochs} - Avg Val Loss: {avg_val_loss:.4f}, Accuracy: {accuracy:.4f}")

# Save the fine-tuned model
model.save_pretrained("./model")
