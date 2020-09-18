from flask import Flask,render_template,request
import random
import torch
import json
from model import NeuralNet
from basics import bag_of_words, tokenize, stem

device=torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('intents.json','r') as f:
    intents=json.load(f)
    
FILE="data.pth"
data=torch.load(FILE)


input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

app = Flask(__name__) 

@app.route("/")
def index():
     return render_template("index.html") #to send context to html

@app.route("/get")
def get_bot_response():
     sentence = request.args.get("msg") #get data from input,we write js  to index.html
     sentence=tokenize(sentence)
     X=bag_of_words(sentence,all_words)
     X=X.reshape(1,X.shape[0])
     X=torch.from_numpy(X)
     output=model(X)
     _,predicted=torch.max(output,dim=1)
     tag=tags[predicted.item()]
     bot="I do not understand..."
     probs = torch.softmax(output, dim=1)
     prob = probs[0][predicted.item()]
     if prob.item() > 0.75:
          for intent in intents['intents']:
               if tag == intent["tag"]:
                    bot=random.choice(intent['responses'])
     else:
          bot="I do not know...try something unique😊"
          
     return bot


if __name__ == "__main__":
     app.run(debug = True)


