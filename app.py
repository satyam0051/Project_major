import os
from flask import flash
from flask import Flask,render_template,url_for,redirect,request
from flask import send_from_directory
from flaskext.mysql import MySQL
from flask_mail import Mail,Message


app=Flask(__name__)
app.secret_key="pratima"
mysql=MySQL()
mail=Mail(app)


app.config['MAIL_SERVER'] ='smtp.gmail.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USERNAME']='rs0264755@gmail.com'
app.config['MAIL_PASSWORD']='ramsita22'
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USE_SSL']=True
mail=Mail(app)

app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']='MarstoEarth19'
app.config['MYSQL_DATABASE_DB']='police_station'
app.config['MYSQL_DATABASE_HOST']='localhost'
mysql.init_app(app)



@app.route("/",methods=["POST","GET"])
def home():
    return render_template("index.html")

@app.route("/data")
def registration_data(ls):
    a,b,c,d,e,f,g,h=ls[0],ls[1],ls[2],ls[3],ls[4],ls[5],ls[6],ls[7]

    try:
        conn=mysql.connect()
        cursor=conn.cursor()
        cursor.execute("select govtid from registration")
        dt=cursor.fetchall()
    
        
        inst=("""insert into registration(govtid,email,fname,lname,phoneno,age,password,gender) values(%s,%s,%s,%s,%s,%s,%s,%s)""")
    
        dat=(a,b,c,d,e,f,g,h)
        cursor.execute(inst,dat)
        conn.commit()
        
    except:
       
        return redirect(url_for('login'))
    finally:
        msg=Message('Hi!',sender='rs0264755@gmail.com',recipients=[b])
        msg.body='Hi! user you have successfully registerd on VPS'
        mail.send(msg)
        cursor.close()
        return redirect(url_for('login'))
    
@app.route("/register",methods=["POST","GET"])
def register():
    
    if request.method=="POST":
        fname=request.form.get('fname')
        lname=request.form.get('lname')
        email=request.form.get('email')

        
        phoneno=request.form.get('phoneno')
        govtid=request.form.get('govtid')
        age=request.form.get('age')
        password=request.form.get('password')
        gender=request.form.get('gender')
        ls=[govtid,email,fname,lname,phoneno,age,password,gender]
        registration_data(ls)

        
            
    return render_template("reg.html")

@app.route('/profile')
def profile():
    pass
@app.route('/contact',methods=["GET","POST"])
def contact():
    return render_template("contact.html")
@app.route("/complain",methods=["GET","POST"])
def complaint():
    if request.method=="POST":
        name=str(request.form.get("username"))
        dob=str(request.form.get("dob"))
        phone=str(request.form.get("ID"))
        up_doc=str(request.form.get("upload_doc"))
        father=str(request.form.get("position"))
        area=str(request.form.get("Area"))
        category=str(request.form.get("phone"))
        email=str(request.form.get("email"))
        description=str(request.form.get("kuch"))
        proof_type=str(request.form.get("proof"))
        up_proof=str(request.form.get("upload_proof"))
        gid=str(request.form.get("GID"))
        other=str(request.form.get("other"))
        print(name,dob,phone,up_doc,father,area,category,email)
        print(description,proof_type,up_proof,gid,other)

        try:
            print("bebgin")
            conn=mysql.connect()
            print('first')
            cursor=conn.cursor()
            print('second')
            inst=("""insert into complaints(name,dob,phone,up_doc,father,area,category,email,description,proof_type,up_proof,gid,other) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""")
            print("third")
            dat=(name,dob,phone,up_doc,father,area,category,email,description,proof_type,up_proof,gid,other)
            print("fourth")
            cursor.execute(inst,dat)
            print("five")
            conn.commit()
            print("six")
            cursor.close()
            print("try succes")

        except:
            print("except succes")
            pass
        else:
            msg=Message('Hi!',sender='rs0264755@gmail.com',recipients=[email])
            msg.body='Hello,'+str(name)+'your comlaint have recorded and we will take action as soon as possible'
            mail.send(msg)
            msg1=Message('HI!,Satyam',sender='rs0264755@gmail.com',recipients=['satyam700770@gmail.com'])
            msg1.body="""Hello sir! You have got another complaints from user so please take action on this complaints for craete a better environment"""
            mail.send(msg1)
            print("elase succes")
        finally:
            print("Successfully complaints")


    return render_template("complaint.html")

@app.route("/login",methods=["POST","GET"])
def login():
    if request.method=="POST":
        userid=request.form.get('email')
        passw=request.form.get('password')
        print(userid,passw)
        conn=mysql.connect()
        cursor=conn.cursor()
        query="select email from registration where email=%s"
        cursor.execute(query,(userid,))
        userid1=cursor.fetchone()
        query1="select password from registration where password=%s"
        cursor.execute(query1,(passw,))
        passw1=cursor.fetchone()
        print(userid1,passw1)
        dt="select * from registration where email=%s"
        cursor.execute(dt,(userid,))
        d=cursor.fetchall()
        print(d)
        if userid.lower()==userid1[0].lower() and passw==passw1[0]:
            flash("Loggin successfully")
            return render_template('prof.html',detail=d)
        
        

    return render_template("login.html")

@app.route("/adminlogin",methods=["POST","GET"])
def adminlogin():
    if request.method=="POST":
        email=request.form.get('email')
        password=request.form.get('password')
        conn=mysql.connect()
        cursor=conn.cursor()
        query="select * from complaints"
        cursor.execute(query)
        dta=cursor.fetchall()
        
        print(dta)
        print(email,password)
        if email=='rs0264775@gmail.com' and password=='242322':
            return render_template('aprof.html',data=dta)
    return render_template('adminlogin.html')
@app.route("/map",methods=["POST","GET"])
def map():
    return render_template('mp.html')

if __name__=="__main__":
    app.run(debug=True)

