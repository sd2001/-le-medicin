from flask import Flask,render_template,request

app=Flask(__name__)

@app.route("/",methods=['GET','POST'])
def home():
    if request.method=='POST':
        val1=request.form.get('gender')
        val2=request.form.get('gender2')
        val3=int(val1)+int(val2)
        return str(val3)
    return render_template('htmlform.html')

@app.route("/chatbot")
def chatbot_test():
    

if __name__=="__main__":
    app.run(debug=True)
    