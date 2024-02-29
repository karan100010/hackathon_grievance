from flask import Flask, request, jsonify
import torch
from transformers import AlbertForSequenceClassification, AlbertTokenizer
from datasets import ClassLabel

# Load the saved model
model_path = "./model"
model = AlbertForSequenceClassification.from_pretrained(model_path)

# Load the tokenizer
tokenizer = AlbertTokenizer.from_pretrained("albert-base-v2")
label_classes = []
with open("labels.txt", "r") as f:
    for line in f:
        label_classes.append(line.replace("\n", ""))

c2l = ClassLabel(num_classes=3, names=label_classes)


app = Flask(__name__)


@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    try:
        text = data['text']
    except KeyError:
        return jsonify({"error": "Please provide a text field."})

    try:
        # Tokenize and convert to tensor
        inputs = tokenizer(text, return_tensors="pt")

        # Make inference
        with torch.no_grad():
            outputs = model(**inputs)

        # Get the predicted class
        logits = outputs.logits

        predicted_class = torch.argmax(logits, dim=1).item()

        return jsonify({"predicted_class": c2l.int2str(predicted_class)})
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
