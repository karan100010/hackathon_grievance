from flask import Flask, request, jsonify
import torch
from transformers import AlbertForSequenceClassification, AlbertTokenizer
from datasets import ClassLabel
from flask import Flask, request, jsonify
from datetime import datetime
import nemo.collections.asr as nemo_asr
import requests
import tempfile
import os
import json
import wave
import json
import nemo.collections.nlp as nemo_nlp
import torchaudio
from speechbrain.pretrained import EncoderClassifier, SpeakerRecognition
from speechbrain.utils.checkpoints import Checkpointer
import os
from flask import Flask, request, jsonify
import random
import base64
# from classifier import EncoderClassifier

# model = EncoderClassifier.from_hparams(source="speechbrain/lang-id-voxlingua107-ecapa", savedir="pretrained_models/lang-id-voxlingua107-ecapa")

def convert_file(file):
    # Decode and combine u-law fragments into a single bytearray
    # Remove the unused line of code
    # combined_pcm_data = bytearray()

    # ulaw_data = bytes(file['data']['data'])

    # Decode the u-law data to 16-bit linear PCM
    # pcm_data = audioop.ulaw2lin(file, 2)

    # Save the combined PCM data to a WAV file
    file_name = "output{}.wav".format(random.randint(0, 1000))
    with wave.open(file_name, 'wb') as wf:
        wf.setnchannels(1)  # Adjust based on the number of channels in your audio
        wf.setsampwidth(2)  # 2 bytes for 16-bit audio
        wf.setframerate(8000)  # Adjust based on the sample rate of your u-law audio
        wf.writeframes(file)
    return file_name
        

# Load the saved model
nmt_model = nemo_nlp.models.machine_translation.MTEncDecModel.from_pretrained(model_name="nmt_hi_en_transformer12x2")
asr_model_hi = nemo_asr.models.EncDecCTCModelBPE.from_pretrained(model_name="stt_hi_conformer_ctc_medium")
model_path = "./model_2"
model_bin = AlbertForSequenceClassification.from_pretrained(model_path)
model_id = EncoderClassifier.from_hparams(source='model/epaca/1988/save/CKPT+2024-02-15+14-26-50+00')
asr_model_en = nemo_asr.models.EncDecCTCModelBPE.from_pretrained(model_name="stt_en_conformer_ctc_medium")


# Load the tokenizer
tokenizer = AlbertTokenizer.from_pretrained("albert-base-v2")
label_classes = []
with open("labels.txt", "r") as f:
    for line in f:
        label_classes.append(line.replace("\n", ""))

c2l = ClassLabel(num_classes=1155, names=label_classes)


app = Flask(__name__)


@app.route('/predict', methods=['POST'])
def predict():
    try:
        ulaw_fragments  = request.get_data()
        print(ulaw_fragments)
        #convert ulaw_fragment variable to a array

        print(type(ulaw_fragments))
        #writ ulaw_fragments to a json file
        file=convert_file(ulaw_fragments)
        prediction = model_id.classify_file(file)
        if prediction[3]=="en":
            text=asr_model_en.transcribe([file])
            try:
                # Tokenize and convert to tensor
                inputs = tokenizer(text[0], return_tensors="pt")

                # Make inference
                with torch.no_grad():
                    outputs = model_bin(**inputs)

                # Get the predicted class
                logits = outputs.logits

                predicted_class = torch.argmax(logits, dim=1).item()
            except Exception as e:
                print(e)
                return jsonify({"error": str(e)})

        else:
            text=asr_model_hi.transcribe([file])
            translated_text = nmt_model.translate([text[0]])
            try:
                # Tokenize and convert to tensor
                inputs = tokenizer(translated_text[0], return_tensors="pt")

                # Make inference
                with torch.no_grad():
                    outputs = model_bin(**inputs)

                # Get the predicted class
                logits = outputs.logits

                predicted_class = torch.argmax(logits, dim=1).item()
            except Exception as e:
                print(e)
                return jsonify({"error": str(e)})
       # base64_data = base64.b64encode(ulaw_fragments).decode('utf-8')
        final_dict={
  #  "audio": base64_data,
    "transcript": text[0],
    "subjectContentText": "",
    "code": 1,
    "categoryName": c2l.int2str(predicted_class),
    "label": "",
    "status": "",
    "comments": []

  }     
       # resp=requests.post("http://localhost:8080/grievance/post",json=final_dict)
       # print(resp.content)
        return jsonify(final_dict)
            

    except Exception as e:
        print(e)
        return jsonify({"error": str(e)})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
