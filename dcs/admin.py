from flask import *
from database import *
from datetime import datetime
import os
from werkzeug.utils import secure_filename
import segno
import hashlib
import os

def generate_hash(data: str) -> str:
    return hashlib.sha256(data.encode()).hexdigest()

admin=Blueprint('admin',__name__)

@admin.route('/adminhome')
def adminhome():
    # Get total users count 
    q = "SELECT COUNT(*) as total FROM user"
    result = select(q)
    total_users = result[0]['total'] if result else 0
    
    # Get total feedback count
    q = "SELECT COUNT(*) as total FROM feedback"
    result = select(q)
    total_feedback = result[0]['total'] if result else 0
    
    # Get total requests count
    q = "SELECT COUNT(*) as total FROM request"
    result = select(q)
    total_requests = result[0]['total'] if result else 0
    
    # Get pending complaints with user info
    q = """SELECT complaint.*, user.* 
           FROM complaint 
           INNER JOIN user ON complaint.user_id = user.user_id 
           WHERE complaint.reply = 'pending' 
           ORDER BY complaint.date DESC"""
    pending_complaints = select(q)
    
    # Get all users with their details
    users_query = """
        SELECT user.*, 
               COUNT(DISTINCT request.request_id) as total_requests,
               COUNT(DISTINCT myskills.myskills_id) as total_skills
        FROM user 
        LEFT JOIN request ON request.user_id = user.user_id
        LEFT JOIN myskills ON myskills.user_id = user.user_id
        GROUP BY user.user_id
        ORDER BY user.user_id DESC
    """
    users = select(users_query)
    
    # Get statistics for skills
    stats_query = """
    SELECT 
        s.skills,
        COUNT(DISTINCT ms.user_id) as total_users,
        COUNT(DISTINCT r.request_id) as total_requests,
        SUM(CASE WHEN r.status = 'paid' THEN 1 ELSE 0 END) as completed_requests
    FROM skills s
    LEFT JOIN myskills ms ON s.skills_id = ms.skills_id
    LEFT JOIN request r ON ms.myskills_id = r.myskills_id
    GROUP BY s.skills_id, s.skills
    """
    skill_stats = select(stats_query)
    
    return render_template('indexadmin.html',
                         complaints=pending_complaints,
                         total_users=total_users,
                         total_feedback=total_feedback,
                         total_requests=total_requests,
                         users=users,
                         current_date=datetime.now(),
                         skill_stats=skill_stats)

@admin.route('/admin_addskills',methods=['get','post'])
def admin_addskills():
	data={}
	s="select * from skills"
	data['skillview']=select(s)
	if "sub" in request.form:
		fn=request.form['skill']
		
		qu="insert into skills values(null,'%s')"%(fn)
		insert(qu)
		return redirect(url_for('admin.admin_addskills'))
	if "action" in request.args:
		action=request.args['action']
		sid=request.args['sid']
	else:
		action=None
	if action=='delete':
		de="delete from skills where skills_id='%s'"%(sid)
		delete(de)
		return redirect(url_for('admin.admin_addskills'))
	if action=='update':
		up="select * from skills where skills_id='%s'"%(sid)
		data['skillupdate']=select(up)
		if "sub1" in request.form:
			fn=request.form['skill']
			upd="update skills set skills='%s' where skills_id='%s'"%(fn,sid)
			update(upd)
			return redirect(url_for('admin.admin_addskills'))

	return render_template('admin_addskills.html',data=data)

@admin.route('/admin_managebadge',methods=['get','post'])
def admin_managebadge():
	data={}
	s="select * from badgeorachive"
	data['catview']=select(s)
	if "sub" in request.form:
		fn=request.form['category']
		
		qu="insert into badgeorachive values(null,'%s')"%(fn)
		insert(qu)
		return redirect(url_for('admin.admin_managebadge'))
	if "action" in request.args:
		action=request.args['action']
		cid=request.args['cid']
	else:
		action=None
	if action=='delete':
		de="delete from badgeorachive where badgeorchive_id='%s'"%(cid)
		delete(de)
		return redirect(url_for('admin.admin_managebadge'))
	if action=='update':
		up="select * from badgeorachive where badgeorchive_id='%s'"%(cid)
		data['catupdate']=select(up)
		if "sub1" in request.form:
			fn=request.form['category']
			upd="update badgeorachive set badgeorachive='%s' where badgeorchive_id='%s'"%(fn,cid)
			update(upd)
			return redirect(url_for('admin.admin_managebadge'))

	return render_template('admin_managebadge.html',data=data)


	
@admin.route('/admin_viewusers',methods=['get','post'])
def admin_viewusers():
	data={}
	s="select * from user"
	data['userview']=select(s)
	return render_template('admin_viewusers.html',data=data)
@admin.route('/adminuserskill',methods=['get','post'])
def adminuserskill():
	uid=request.args['uid']
	data={}
	s=" SELECT * FROM myskills INNER JOIN `user` USING(user_id) INNER JOIN `skills` USING(skills_id) where user_id='%s'"%(uid)
	data['myskillview']=select(s)
	return render_template('adminusersskill.html',data=data)

@admin.route('/viewcomplaint',methods=['get','post'])
def viewcomplaint():
    data = {}
    # Get complaints with user info and order by status and date
    q = """
        SELECT complaint.*, user.*,
        CASE 
            WHEN reply = 'pending' THEN 0
            ELSE 1
        END as is_replied
        FROM complaint 
        INNER JOIN user USING(user_id)
        ORDER BY is_replied ASC, date DESC
    """
    res = select(q)
    data['viewcomplaint'] = res
    
    if 'submit' in request.form:
        complaint_id=request.form['complaint_id']
        reply=request.form['reply']
        
        q = """
                    UPDATE complaint 
                    SET reply = '%s', 
        				date = curdate() 
                    WHERE complaint_id = '%s'
                """%(reply,complaint_id)
        update(q)
        flash("Reply sent successfully", "success")
        return redirect(url_for("admin.viewcomplaint"))

    
               

    return render_template("adminview_complaints.html", data=data)


@admin.route('/admin_requests',methods=['get','post'])
def admin_requests():
    data = {}
    q = """
        SELECT request.*, myskills.*, user.*, skills.skills, badgeorachive.badgeorachive 
        FROM request 
        INNER JOIN myskills ON request.myskills_id = myskills.myskills_id 
        INNER JOIN user ON myskills.user_id = user.user_id
        INNER JOIN skills ON myskills.skills_id = skills.skills_id
        INNER JOIN badgeorachive ON myskills.badgeorchive_id = badgeorachive.badgeorchive_id
        ORDER BY request.date DESC
    """
    data['requests'] = select(q)
    
    if 'action' in request.args:
        rid = request.args['rid']
        action = request.args['action']
        if action == 'approve':
            q = "UPDATE request SET status='approved' WHERE request_id='%s'" % rid
            update(q)
            flash("Request approved successfully")
        elif action == 'reject':
            q = "UPDATE request SET status='rejected' WHERE request_id='%s'" % rid
            update(q)
            flash("Request rejected")
        return redirect(url_for('admin.admin_requests'))
    
    return render_template('admin_requests.html', data=data)

@admin.route('/upload_certificate',methods=['POST'])
def upload_certificate():
    if 'certificate' in request.files:
        request_id = request.form['request_id']
        certificate = request.files['certificate']
        name = request.form['name']
        course = request.form['course']
        dates = request.form['date']
        
        # Save file
        path = 'static/certificates'
        if not os.path.exists(path):
            os.makedirs(path)
        filename = secure_filename(certificate.filename)
        certificate.save(os.path.join(path, certificate.filename))
        
        # Insert into certificate table
        date = datetime.now().strftime('%Y-%m-%d')
        q = "INSERT INTO certificate VALUES(NULL,'%s','%s','%s','%s','%s','%s','')" % (
            request_id, name, filename, date,course,dates)
        res=insert(q)
        
        
        # Get last inserted ID
        cert_id = res

        # Combine data and generate hash
        combined = f"{name}|{course}|{dates}|{cert_id}"
        print(combined,"--------------------------")
        hash_val = generate_hash(combined)

        # Generate QR and save
        qr = segno.make_qr(hash_val)
        qr_filename = f"cert_{cert_id}.png"
        qr_path = os.path.join('dcs/static/qrcode/', qr_filename)
        qr.save(qr_path, scale=5)
        u="update certificate set qr='%s' where certificate_id='%s'"%(qr_path,cert_id)
        update(u)
        
        flash("Certificate uploaded successfully")
        return redirect(url_for('admin.admin_requests'))
    
    flash("No file selected")
    return redirect(url_for('admin.admin_requests'))

@admin.route('/view_certificate/<request_id>')
def view_certificate(request_id):
    data = {}
    q = """SELECT certificate.*, request.* 
           FROM certificate 
           INNER JOIN request ON certificate.request_id=request.request_id 
           WHERE certificate.request_id='%s'""" % request_id
    data['cert'] = select(q)
    return render_template('view_certificate.html', data=data)

@admin.route('/delete_certificate/<int:certificate_id>')
def delete_certificate(certificate_id):
    # First get the file name
    q = "SELECT file FROM certificate WHERE certificate_id='%s'" % certificate_id
    res = select(q)
    
    if res:
        # Delete physical file
        file_path = os.path.join('static/certificates', res[0]['file'])
        if os.path.exists(file_path):
            os.remove(file_path)
            
        # Delete database record
        q = "DELETE FROM certificate WHERE certificate_id='%s'" % certificate_id
        delete(q)
        flash("Certificate deleted successfully")
    else:
        flash("Certificate not found")
        
    return redirect(url_for('admin.admin_requests'))

# @admin.route('/send_reply', methods=['POST'])
# def send_reply():
#     if request.method == 'POST':
#         complaint_id = request.form.get('complaint_id')
#         reply = request.form.get('reply')
        
#         if complaint_id and reply:
#             # Update complaint with reply
#             reply_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#             q = """
#                 UPDATE complaint 
#                 SET reply = %s,
#                     reply_date = %s 
#                 WHERE complaint_id = %s
#             """
#             update(q, (reply, reply_date, complaint_id))
            
#             flash("Reply sent successfully", "success")
#         else:
#             flash("Invalid request", "error")
            
#     return redirect(url_for("admin.viewcomplaint"))


