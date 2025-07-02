from flask import *
from database import *
import uuid
staff=Blueprint('staff',__name__)

@staff.route('/staffhome')
def staffhome():
	return render_template('staffhome.html')



@staff.route('/staff_upload',methods=['post','get'])
def staff_upload():
	data={}
	if 'submit' in request.form:
		upload=request.files['upload']
		path="static/"+str(uuid.uuid4())+upload.filename
		upload.save(path)

		q="insert into notes values(null,'%s','%s',curdate())"%(session['sid'],path)
		insert(q)

	q="select * from notes"
	data['view']=select(q)


	if 'action' in request.args:
		action=request.args['action']
		uid=request.args['uid']
	else:
		action=None


	if action=='delete':
		q="delete from notes where notes_id='%s'"%(uid)
		delete(q)
		return redirect(url_for('staff.staff_upload'))
	return render_template('staff_upload.html',data=data)