from flask import *
from database import *

from pyzbar.pyzbar import decode
from PIL import Image
import hashlib, os



def generate_hash(data: str) -> str:
    return hashlib.sha256(data.encode()).hexdigest()

public=Blueprint('public',__name__)
@public.route('/')
def home():
	return render_template('index.html')
@public.route('/login',methods=['post','get'])
def login():
	if "submit" in request.form:
		u=request.form['un']
		p=request.form['ps']
		s="select * from login where username='%s' and password='%s'" %(u,p)
		res=select(s)
		if res:
			session['login_id']=res[0]['login_id']
			print('my login',session['login_id'])

			if res[0]['usertype']=='admin':
				return redirect(url_for('admin.adminhome'))


			elif res[0]['usertype']=='proffessional':
				q="select * from proffessional where login_id='%s'"%(session['login_id'])
				val=select(q)
				if val:
					session['pid']=val[0]['pid']
					return redirect(url_for('pro.prohome'))
			elif res[0]['usertype']=='staff':
				q="select * from staff where login_id='%s'"%(session['login_id'])
				val=select(q)
				if val:
					session['sid']=val[0]['staff_id']
					return redirect(url_for('staff.staffhome'))
		else:
			flash("username or password is incorrect")

	return render_template('login1.html')


@public.route('/verifycerti', methods=['GET', 'POST'])
def verifycerti():
    result = ""

    if request.method == 'POST':
        cert_id = request.form['certificate_id']
        name = request.form['name']
        course = request.form['course']
        date = request.form['date']
        uploaded_file = request.files['qr']

        # Save uploaded QR temporarily
        if uploaded_file:
            qr_path = os.path.join('static', 'uploaded_qr.png')
            uploaded_file.save(qr_path)

            # Read hash from QR image
            decoded_data = decode(Image.open(qr_path))
            if not decoded_data:
                result = "❌ Could not read QR code."
            else:
                qr_hash = decoded_data[0].data.decode()

                # Reconstruct data to compare
                combined_data = f"{name}|{course}|{date}|{cert_id}"
                print(combined_data)
                recalculated_hash = generate_hash(combined_data)
                print(qr_hash,"---------------------")
                print(recalculated_hash,"---------------------")
                # Compare
                if qr_hash == recalculated_hash:
                    result = "✅ Certificate is VALID and untampered."
                else:
                    result = "❌ Certificate is INVALID or TAMPERED!"

    return render_template("verifycerti.html", result=result)


# @public.route('/staff_register',methods=['post','get'])
# def staff_register():
# 	if 'ds' in request.form:
# 		fname=request.form['fname']
# 		lname=request.form['lname']
# 		pla=request.form['pla']
# 		phn=request.form['phn']
# 		mail=request.form['mail']
# 		uname=request.form['uname']
# 		pwd=request.form['pwd']
# 		q="insert into login values(null,'%s','%s','staff')"%(uname,pwd)
# 		res=insert(q)
# 		q="insert into staff values(null,'%s','%s','%s','%s','%s','%s')"%(res,fname,lname,pla,phn,mail)
# 		insert(q)
# 	return render_template('staff_register.html')

# @public.route('/proffessional_register',methods=['post','get'])
# def proffessional_register():
# 	if 'ds' in request.form:
# 		fname=request.form['fname']
# 		lname=request.form['lname']
# 		pla=request.form['pla']
# 		phn=request.form['phn']
# 		mail=request.form['mail']
# 		uname=request.form['uname']
# 		pwd=request.form['pwd']
# 		q="insert into login values(null,'%s','%s','proffessional')"%(uname,pwd)
# 		res=insert(q)
# 		q="insert into proffessional values(null,'%s','%s','%s','%s','%s','%s')"%(res,fname,lname,pla,phn,mail)
# 		insert(q)
# 	return render_template('proffessional_register.html')