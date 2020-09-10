from flask import Flask,render_template,request,flash
import random
import torch
import json
from model import NeuralNet
from basics import bag_of_words, tokenize, stem

app=Flask(__name__)
app.secret_key = 'hellouserapi'

@app.route("/",methods=['GET','POST'])
def home():
    if request.method=='POST':
        val1=request.form.get('gender')
        val2=request.form.get('gender2')
        val3=int(val1)+int(val2)
        return str(val3)
    return render_template('htmlform.html')

@app.route("/tests/chatbot")
def index():
     return render_template("Chatbot_temp.html")

@app.route("/tests/chatbot_get")
def chatbot():
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
    sentence = request.args.get("msg") #get data from input,we write js  to index.html
    sentence=tokenize(sentence)
    X=bag_of_words(sentence,all_words)
    X=X.reshape(1,X.shape[0])
    X=torch.from_numpy(X)
    output=model(X)
    _,predicted=torch.max(output,dim=1)
    tag=tags[predicted.item()]
    bot="I do not know...try something different😊"
    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                bot=random.choice(intent['responses'])
    else:
        bot="I do not know...try something different😊"
        
    return bot

    

@app.route("/tests/self_assess",methods=['GET','POST'])
def self_assess():
    if request.method=='POST':
        score=50
        fear=request.form.get('fear')
        eat=request.form.get('eat')
        confidence=request.form.get('confidence')
        future=request.form.get('future')
        relation=request.form.get('relation')
        activity=request.form.get('activity')
        score=score+int(fear)+int(eat)+int(confidence)+int(future)+int(relation)+int(activity)
        mssg=""
        if score>50 and score<100:
            mssg="Great, make your days even better"
        elif score>100:
            mssg="Awesome, thats the motivation we need"
        elif score<50 and score>0:
            mssg="Try to stay motiavted always. We would recommend you to consult Dr A"            
        elif score<0:
            mssg="Its highly important for you to consult Dr A, before something big happens."
        
        flash(mssg)
        return render_template('self-assessment.html')
    return render_template('self-assessment.html')

@app.route("/tests/inkblot",methods=['GET','POST'])
def inkblot():
    if request.method=='POST':
        score=50
        fear=request.form.get('1')
        eat=request.form.get('2')
        confidence=request.form.get('3')
        future=request.form.get('4')
        relation=request.form.get('5')
        
        score=score+int(fear)+int(eat)+int(confidence)+int(future)+int(relation)
        mssg=""
        if score>50 and score<100:
            mssg="Great, make your days even better"
        elif score>100:
            mssg="Awesome, thats the motivation we need"
        elif score<50 and score>0:
            mssg="Try to stay motiavted always. We would recommend you to consult Dr A"            
        elif score<0:
            mssg="Its highly important for you to consult Dr A, before something big happens."
        
        flash(mssg)
        return render_template('inkblot.html')
    return render_template('inkblot.html')
        
    

if __name__=="__main__":
    app.run(debug=True)
    