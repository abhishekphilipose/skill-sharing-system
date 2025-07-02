from flask import *
from database import *
import uuid
pro=Blueprint('pro',__name__)

@pro.route('/prohome')
def prohome():
	return render_template('prohome.html')



@pro.route('/pro_upload',methods=['post','get'])
def pro_upload():
	data={}
	if 'submit' in request.form:
		upload=request.files['upload']
		path="static/"+str(uuid.uuid4())+upload.filename
		upload.save(path)

		q="insert into upload values(null,'%s','%s',curdate())"%(session['pid'],path)
		insert(q)

	q="select * from upload"
	data['view']=select(q)


	if 'action' in request.args:
		action=request.args['action']
		uid=request.args['uid']
	else:
		action=None


	if action=='delete':
		q="delete from upload where upload_id='%s'"%(uid)
		delete(q)
		return redirect(url_for('pro.pro_upload'))
	return render_template('pro_upload.html',data=data)