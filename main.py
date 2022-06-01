from flask import *
import sqlite3, hashlib, os
import uuid
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'random string'
UPLOAD_FOLDER = 'statics/uploads'
ALLOWED_EXTENSIONS = set(['jpeg', 'jpg', 'png', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def getLoginDetails():
    with sqlite3.connect('student.db') as conn:
        cur = conn.cursor()
        if 'email' not in session:
            loggedIn = False
            name = ''
            roll = ''
            program = ''
            branch = ''
            batch = ''
            dob = ''
            presentaddress = ''
            mobile = ''
            parentmobile = ''
            bloodgroup = ''
            allergic = ''
            cgpa = ''
            skills = ''
            linkedin = ''
            photo=''
        else:
            loggedIn = True
            cur.execute("SELECT userId, name, roll, program, branch, batch, dob, presentaddress, mobile, parentmobile, bloodgroup, allergic, cgpa, skills, linkedin, photo FROM profile WHERE email = ?", (session['email'], ))
            userId, name, roll, program, branch, batch, dob, presentaddress, mobile, parentmobile, bloodgroup, allergic, cgpa, skills, linkedin, photo = cur.fetchone()
    conn.close()
    return (loggedIn, name, roll, program, branch, batch, dob, presentaddress, mobile, parentmobile, bloodgroup, allergic, cgpa, skills, linkedin, photo)

@app.route("/")
def root():
    loggedIn, name, roll, program, branch, batch, dob, presentaddress, mobile, parentmobile, bloodgroup, allergic, cgpa, skills, linkedin, photo= getLoginDetails()
    return render_template('home.html', loggedIn=loggedIn, name=name, roll=roll, program=program, branch=branch, batch=batch, dob=dob, presentaddress=presentaddress, mobile=mobile, parentmobile=parentmobile, bloodgroup=bloodgroup, allergic=allergic, cgpa=cgpa, skills=skills, linkedin=linkedin, photo=photo)

  
@app.route("/handbook")
def handbook():
    loggedIn, name, roll, program, branch, batch, dob, presentaddress, mobile, parentmobile, bloodgroup, allergic, cgpa, skills, linkedin, photo= getLoginDetails()
    return render_template('handbook.html', loggedIn=loggedIn, name=name, roll=roll, program=program, branch=branch, batch=batch, dob=dob, presentaddress=presentaddress, mobile=mobile, parentmobile=parentmobile, bloodgroup=bloodgroup, allergic=allergic, cgpa=cgpa, skills=skills, linkedin=linkedin, photo=photo)

@app.route("/forms")
def forms():
    loggedIn, name, roll, program, branch, batch, dob, presentaddress, mobile, parentmobile, bloodgroup, allergic, cgpa, skills, linkedin, photo= getLoginDetails()
    return render_template('forms.html', loggedIn=loggedIn, name=name, roll=roll, program=program, branch=branch, batch=batch, dob=dob, presentaddress=presentaddress, mobile=mobile, parentmobile=parentmobile, bloodgroup=bloodgroup, allergic=allergic, cgpa=cgpa, skills=skills, linkedin=linkedin, photo=photo)



@app.route("/edit")
def editProfile():
    if 'email' not in session:
        return redirect(url_for('root'))
    loggedIn, name, roll, program, branch, batch, dob, presentaddress, mobile, parentmobile, bloodgroup, allergic, cgpa, skills, linkedin, photo = getLoginDetails()
    with sqlite3.connect('student.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT userId, name, roll, program, branch, batch, dob, presentaddress, mobile, parentmobile, bloodgroup, allergic, cgpa, skills, linkedin, photo FROM profile WHERE email = ?", (session['email'], ))
        profileData = cur.fetchone()
    conn.close()
    return render_template("editProfile.html", profileData=profileData, loggedIn=loggedIn, name=name, roll=roll, program=program, branch=branch, batch=batch, dob=dob, presentaddress=presentaddress, mobile=mobile, parentmobile=parentmobile, bloodgroup=bloodgroup, allergic=allergic, cgpa=cgpa, skills=skills, linkedin=linkedin, photo=photo)

@app.route("/changePassword", methods=["GET", "POST"])
def changePassword():
    if 'email' not in session:
        return redirect(url_for('loginForm'))
    if request.method == "POST":
        oldPassword = request.form['oldpassword']
        oldPassword = hashlib.md5(oldPassword.encode()).hexdigest()
        newPassword = request.form['password']
        newPassword = hashlib.md5(newPassword.encode()).hexdigest()
        with sqlite3.connect('student.db') as conn:
            cur = conn.cursor()
            cur.execute("SELECT userId, password FROM profile WHERE email = ?", (session['email'], ))
            userId, password = cur.fetchone()
            if (password == oldPassword):
                try:
                    cur.execute("UPDATE profile SET password = ? WHERE userId = ?", (newPassword, userId))
                    conn.commit()
                    msg="Changed successfully"
                except:
                    conn.rollback()
                    msg = "Failed"
                return render_template("changePassword.html", msg=msg)
            else:
                msg = "Wrong password"
        conn.close()
        return render_template("changePassword.html", msg=msg)
    else:
        return render_template("changePassword.html")

@app.route("/updateProfile", methods=["GET", "POST"])
def updateProfile():
    if request.method == 'POST':
        name = request.form['name']
        roll = request.form['roll']
        program = request.form['program']
        branch = request.form['branch']
        batch = request.form['batch']
        dob = request.form['dob']
        presentaddress = request.form['presentaddress']
        mobile = request.form['mobile']
        parentmobile = request.form['parentmobile']
        bloodgroup = request.form['bloodgroup']
        allergic = request.form['allergic']
        cgpa = request.form['cgpa']
        skills = request.form['skills']
        linkedin = request.form['linkedin']
        photo = request.files['photo']
        with sqlite3.connect('student.db') as con:
            try:
                cur = con.cursor()
                cur.execute('UPDATE profile SET name = ?, roll = ?, program = ?, branch = ?, batch = ?, dob = ?, presentaddress = ?, mobile = ?, parentmobile = ?, bloodgroup = ?, allergic = ?, cgpa = ?, skills = ?, linkedin = ? WHERE email = ?', (name, roll, program, branch, batch, dob, presentaddress, mobile, parentmobile, bloodgroup, allergic, cgpa, skills, linkedin, session['email']))

                con.commit()
                msg = "Saved Successfully"
            except:
                con.rollback()
                msg = "Error occured"
        con.close()
        return redirect(url_for('editProfile'))

@app.route("/loginForm")
def loginForm():
    if 'email' in session:
        return redirect(url_for('root'))
    else:
        return render_template('login.html', error='')

@app.route("/login", methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if is_valid(email, password):
            session['email'] = email
            return redirect(url_for('root'))
        else:
            error = 'Invalid UserId / Password'
            return render_template('login.html', error=error)

@app.route("/addToQuery", methods=['POST', 'GET'])
def addToQuery():
    if 'email' not in session:
        return redirect(url_for('loginForm'))
    else:
        if request.method == 'POST':
            qid = uuid.uuid4()
            query = request.form['query']
            date = request.form['date']
            status="pending"
            verify="No"
            email=session['email']
            with sqlite3.connect('student.db') as conn:
                cur = conn.cursor()
                cur.execute("SELECT userId FROM profile WHERE email = ?", (session['email'], ))
                userId = cur.fetchone()[0]
                #try:
                cur.execute("INSERT INTO help (roll, query, date, status, verify, email) VALUES (?, ?, ?, ?, ?, ?)", (userId, query, date, status, verify, session['email']))
                conn.commit()
                #cur.execute("UPDATE help set qid = ?", qid)
                #conn.commit()
                msg = "Added successfully"
                #except:
                conn.rollback()
                msg = "Error occured"
            conn.close()
            return redirect(url_for('query'))

@app.route("/query")
def query():
    if 'email' not in session:
        return redirect(url_for('loginForm'))
    
    loggedIn, name, email, roll, program, branch, batch, dob, presentaddress, mobile, parentmobile, bloodgroup, allergic, cgpa, skills, linkedin= getLoginDetails()
    
    email = session['email']
    with sqlite3.connect('student.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT userId FROM profile WHERE email = ?", (email, ))
        userId = cur.fetchone()[0]
        cur.execute("SELECT roll, query, date, status, verify FROM help WHERE roll = ?", (userId, ))
        helps=cur.fetchall()
    conn.close()
    return render_template("query.html", helps = helps, loggedIn=loggedIn, name=name)

@app.route("/logout")
def logout():
    session.pop('email', None)
    return redirect(url_for('root'))

def is_valid(email, password):
    con = sqlite3.connect('student.db')
    cur = con.cursor()
    cur.execute('SELECT email, password FROM profile')
    data = cur.fetchall()
    for row in data:
        if row[0] == email and row[1] == hashlib.md5(password.encode()).hexdigest():
            return True
    return False

@app.route("/register", methods = ['GET', 'POST'])
def register():
    if request.method == 'POST': 
        password = request.form['password']
        email = request.form['email']
        name = request.form['name']
        roll = request.form['roll']
        program = request.form['program']
        branch = request.form['branch']
        batch = request.form['batch']
        dob = request.form['dob']
        presentaddress = request.form['presentaddress']
        permanentaddress = request.form['permanentaddress']
        mobile = request.form['mobile']
        parentmobile = request.form['parentmobile']
        bloodgroup = request.form['bloodgroup']
        allergic = request.form['allergic']
        cgpa = request.form['cgpa']
        skills = request.form['skills']
        linkedin = request.form['linkedin']
        photo = request.files['photo']
        filename=""
        if photo and allowed_file(photo.filename):
            filename = secure_filename(photo.filename)
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        photoname = filename
      

        with sqlite3.connect('student.db') as con:
            #try:
                cur = con.cursor()
                cur.execute('INSERT INTO profile (password, email, name, roll, program, branch, batch, dob, presentaddress, permanentaddress, mobile, parentmobile, bloodgroup, allergic, cgpa, skills, linkedin, photo) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (hashlib.md5(password.encode()).hexdigest(), email, name, roll, program, branch, batch, dob, presentaddress, permanentaddress, mobile, parentmobile, bloodgroup, allergic, cgpa, skills, linkedin, photoname))

                con.commit()

                msg = "Registered Successfully"
            #except:
                #con.rollback()
                #msg = "Error occured"
        con.close()
        return render_template("login.html", error=msg)

@app.route("/registerationForm")
def registrationForm():
    return render_template("register.html")






def getAdminLoginDetails():
    with sqlite3.connect('student.db') as conn:
        cur = conn.cursor()
        if 'email' not in session:
            loggedIn = False
            name = ''
        else:
            loggedIn = True
            cur.execute("SELECT name, email FROM admin WHERE email = ?", (session['email'], ))
            name, email = cur.fetchone()
    conn.close()
    return (loggedIn, name)

@app.route("/adminloginForm")
def adminloginForm():
    if 'email' in session:
        return redirect(url_for('root'))
    else:
        return render_template('adminlogin.html', error='')

@app.route("/adminlogin", methods = ['POST', 'GET'])
def adminlogin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if is_validadmin(email, password):
            session['email'] = email
            return redirect(url_for('admin'))
        else:
            error = 'Invalid UserId / Password'
            return render_template('adminlogin.html', error=error)

def is_validadmin(email, password):
    con = sqlite3.connect('student.db')
    cur = con.cursor()
    cur.execute('SELECT email, password FROM admin')
    data = cur.fetchall()
    for row in data:
        if row[0] == email and row[1] == hashlib.md5(password.encode()).hexdigest():
            return True
    return False

@app.route("/adminregister", methods = ['GET', 'POST'])
def adminregister():
    if request.method == 'POST':
        #Parse form data    
        password = request.form['password']
        email = request.form['email']
        name = request.form['name']
        with sqlite3.connect('student.db') as con:
            #try:
                cur = con.cursor()
                cur.execute('INSERT INTO admin (password, email, name) VALUES (?, ?, ?)', (hashlib.md5(password.encode()).hexdigest(), email, name))

                con.commit()

                msg = "Registered Successfully"
            #except:
                #con.rollback()
                #msg = "Error occured"
        con.close()
        return render_template("adminlogin.html", error=msg)

@app.route("/adminregisterationForm")
def adminregistrationForm():
    return render_template("adminregister.html")

@app.route("/admin")
def admin():
    if 'email' not in session:
        return redirect(url_for('adminloginForm'))
    loggedIn, name= getAdminLoginDetails()
    with sqlite3.connect('student.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT query, date, status, email, verify FROM help")
        data=cur.fetchall()
    conn.close() 
    return render_template('admin.html', data = data, loggedIn=loggedIn, name=name)

@app.route("/adminUpdateQuery", methods=['POST', 'GET'])
def adminUpdateQuery():
    if request.method == 'POST':
        query = request.form['query']
        date = request.form['date']
        email= request.form['email']
        verify= request.form['verify']
        with sqlite3.connect('student.db') as conn:
            cur = conn.cursor()
            #try:
            cur.execute("UPDATE help SET verify = ? WHERE query = ? AND date = ? AND email = ?", (verify, query, date, email))
            conn.commit()
            #cur.execute("UPDATE help set qid = ?", qid)
            #conn.commit()
            msg = "Saved successfully"
            #except:
            #conn.rollback()
            #msg = "Error occured"
        conn.close()
        return redirect(url_for('admin'))






###Service Provider###
def getserviceLoginDetails():
    with sqlite3.connect('student.db') as conn:
        cur = conn.cursor()
        if 'email' not in session:
            loggedIn = False
            name = ''
        else:
            loggedIn = True
            cur.execute("SELECT name, email FROM service WHERE email = ?", (session['email'], ))
            name, email = cur.fetchone()
    conn.close()
    return (loggedIn, name)

@app.route("/serviceloginForm")
def serviceloginForm():
    if 'email' in session:
        return redirect(url_for('root'))
    else:
        return render_template('servicelogin.html', error='')

@app.route("/servicelogin", methods = ['POST', 'GET'])
def servicelogin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if is_validservice(email, password):
            session['email'] = email
            return redirect(url_for('service'))
        else:
            error = 'Invalid UserId / Password'
            return render_template('servicelogin.html', error=error)

def is_validservice(email, password):
    con = sqlite3.connect('student.db')
    cur = con.cursor()
    cur.execute('SELECT email, password FROM service')
    data = cur.fetchall()
    for row in data:
        if row[0] == email and row[1] == hashlib.md5(password.encode()).hexdigest():
            return True
    return False

@app.route("/serviceregister", methods = ['GET', 'POST'])
def serviceregister():
    if request.method == 'POST':
        #Parse form data    
        password = request.form['password']
        email = request.form['email']
        name = request.form['name']
        with sqlite3.connect('student.db') as con:
            #try:
                cur = con.cursor()
                cur.execute('INSERT INTO service (password, email, name) VALUES (?, ?, ?)', (hashlib.md5(password.encode()).hexdigest(), email, name))

                con.commit()

                msg = "Registered Successfully"
            #except:
                #con.rollback()
                #msg = "Error occured"
        con.close()
        return render_template("servicelogin.html", error=msg)

@app.route("/serviceregisterationForm")
def serviceregistrationForm():
    return render_template("serviceregister.html")

@app.route("/service")
def service():
    if 'email' not in session:
        return redirect(url_for('serviceloginForm'))
    loggedIn, name= getserviceLoginDetails()
    with sqlite3.connect('student.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT query, date, status, email FROM help WHERE query like '%mess%'")
        data=cur.fetchall()
    conn.close() 
    return render_template('service.html', data = data, loggedIn=loggedIn, name=name)

@app.route("/serviceUpdateQuery", methods=['POST', 'GET'])
def serviceUpdateQuery():
    if request.method == 'POST':
        query = request.form['query']
        date = request.form['date']
        email= request.form['email']
        status= request.form['status']
        with sqlite3.connect('student.db') as conn:
            cur = conn.cursor()
            #try:
            cur.execute("UPDATE help SET status = ? WHERE query = ? AND date = ? AND email = ?", (status, query, date, email))
            conn.commit()
            #cur.execute("UPDATE help set qid = ?", qid)
            #conn.commit()
            msg = "Saved successfully"
            #except:
            #conn.rollback()
            #msg = "Error occured"
        conn.close()
        return redirect(url_for('service'))







def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def parse(data):
    ans = []
    i = 0
    while i < len(data):
        curr = []
        for j in range(7):
            if i >= len(data):
                break
            curr.append(data[i])
            i += 1
        ans.append(curr)
    return ans

if __name__ == '__main__':
    app.run(debug=True)
