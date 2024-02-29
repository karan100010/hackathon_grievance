import torch
from transformers import AlbertForSequenceClassification, AlbertTokenizer
from datasets import ClassLabel

# Load the saved model
model_path = "./model"
model = AlbertForSequenceClassification.from_pretrained(model_path)

# Load the tokenizer
tokenizer = AlbertTokenizer.from_pretrained("albert-base-v2")

# Input text for testing
input_text =  "Labour and Employment >> Others (EPFO)    Name and Address of Establishment : Zydus healthcare ltd  UAN No. : X0X4X3X5X2X1  PF Code/ PF Account No. : Not Provided  PPO No. : Not Provided  Scheme Certificate Number : Not Provided  PF Office : Regional Office, Bandra 4  -----------------------  Dear sir /madam still I am not able to submit 10C. It is still showing already claim is settled"
label_classes = []
with open("labels.txt", "r") as f:
    for line in f:
        label_classes.append(line.replace("\n", ""))

# Tokenize and convert to tensor
inputs = tokenizer(input_text, return_tensors="pt")

# Make inference
with torch.no_grad():
    outputs = model(**inputs)

# Get the predicted class
logits = outputs.logits
predicted_class = torch.argmax(logits, dim=1).item()

print(f"Predicted Class: {predicted_class}")

c2l = ClassLabel(num_classes=1155, names=label_classes)


print(c2l.int2str(predicted_class))


