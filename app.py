from flask import Flask,render_template,request,flash,redirect,url_for
import random
import torch
import json
from model import NeuralNet
from basics import bag_of_words, tokenize, stem
from nearby import hospital_search,pharmacy_search

app=Flask(__name__)
app.secret_key = 'hellouserapi'

@app.route("/")
def login():    
    return render_template('login.html')

@app.route("/register")
def reg():
    return render_template('register.html')



@app.route("/d",methods=['POST'])
def doctor():
    email_d=request.form.get('doctor_email')
    pass_d=request.form.get('doctor_pass')
    return redirect(url_for('doctor_home'))


@app.route("/p",methods=['POST'])
def patient():
    email_p=request.form.get('patient_email')
    pass_p=request.form.get('patient_pass')
    return redirect(url_for('test'))


@app.route("/doctor_home")
def doctor_home():
    return render_template('doctor_home.html')

@app.route("/doctor_vc")
def doc_vc():
    return render_template('doctor_vc.html')
    

@app.route("/tests")
def test():
    return render_template('patient_home.html')

@app.route("/tests/chatbot")
def chat():
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
        return render_template('self-assessment2.html')
    return render_template('self-assessment2.html')

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
        if score>=50 and score<100:
            mssg="Great, make your days even better"
        elif score>=100:
            mssg="Awesome, thats the motivation we need"
        elif score<50 and score>0:
            mssg="Try to stay motivated always. We would recommend you to consult a doctor"            
        elif score<=0:
            mssg="Its highly important for you to consult a doctor, before something big happens."
        
        flash(mssg)
        return render_template('inkblot.html')
    return render_template('inkblot.html')

@app.route("/doctor_list")
def doctor_list():
    return render_template('doctor_info.html')


@app.route("/video_patient/<string:name>")
def v_p(name):
    return render_template('video_chat.html',name=name)


@app.route("/shop",methods=['GET','POST'])
def shop_search():
    items=["A Tabs","B Tabs","C Tabs"]
    qnty=[10,18,5]
    price=[10,15,18]
    res=False
    if request.method=='POST':       
        search=request.form.get('search')
        for i in range(0,len(items)):
            if search.lower()==items[i].lower():
                res=True
                q=qnty[i]
                p=price[i]
                return render_template('shop2.html',res=res,q=q,p=p,item=search)
        
        return render_template('shop2.html',res=res)
    
    return render_template('shop.html')

@app.route("/shop/confirmation")
def confirm():
    return render_template('payment_ack.html')      

@app.route("/logout")
def logoute():
    return render_template('register.html')  

@app.route("/nearby",methods=['GET','POST'])
def neerby():
    res=False
    if request.method=='POST':
        choice=request.form.get('choice')
        locality=request.form.get('locality')
        
        if choice=='Hospital':
            names=hospital_search(locality)
            res=True
            
        else:
            names=pharmacy_search(locality)
            res=True
            
        return render_template('hospital.html',res=res,names=names)        
        
    return render_template('hospital.html',res=res)
        
    
if __name__=="__main__":
    app.run(debug=True)
    