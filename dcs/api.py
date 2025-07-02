from flask import *
from database import *
import uuid
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
import os
# from hash import *

# Add configuration
UPLOAD_FOLDER = 'static/videos'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'wmv'} 
MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100MB

api = Blueprint('api', __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@api.route('/logins',methods=['post'])
def login():
    data={}
    
    username = request.form['username']
    password = request.form['password']
    q="SELECT * from login where username='%s' and password='%s'" % (username,password)
    res = select(q)
    print(res)
    if res :
        if res[0]['usertype']=="user":
            return jsonify(status="ok",lid=res[0]["login_id"])
        else:
            return jsonify(status="no")
    else:
        return jsonify(status="no")



@api.route('/user_reg',methods=['post'])
def user_reg():
    fname=request.form['fname']
    lname=request.form['lname']
    place=request.form['place']
    phone=request.form['phone']
    email=request.form['email']
    uname=request.form['uname']
    pwd=request.form['pwd']
    y="insert into login values(null,'%s','%s','user')"%(uname,pwd)
    log=insert(y)
    r="insert into user values(null,'%s','%s','%s','%s','%s','%s')"%(log,fname,lname,place,phone,email)
    res=insert(r)
    if res :
        return jsonify(status="ok",data=res)
    else:
        return jsonify(status="no")
@api.route('/add_skill',methods=['post'])
def add_skill():
    
    login_id=request.form['login_id']
    e="select * from user where login_id='%s'"%(login_id)
    res=select(e)
    if res:
        user_id=res[0]['user_id']
        print("mmmmmmmmmmmm",user_id)
    cid=request.form['cid']
    print("iiiiiiiiiiiii",cid)
    sid=request.form['sid']
    print("iiiiiiiiiiiii",sid)
    r="insert into myskills values(null,'%s','%s','%s')"%(user_id,cid,sid)
    res=insert(r)
    if res :
        return jsonify(status="ok",data=res)
    else:
        return jsonify(status="no")
@api.route('/user_view_other_user',methods=['post'])
def user_view_other_user():
    data={}
    login_id=request.form['login_id']
    print("jjjjjjjjjjjjjjjjjjjjjj",login_id)
    r="select * from user where not login_id='%s'"%(login_id)
    res=select(r)
    if res :
        return jsonify(status="ok",data=res)
    else:
        return jsonify(status="no")



@api.route('/viewcate',methods=['post'])
def viewcate():
    data={}
    
    r="select * from badgeorachive"
    res=select(r)
    if res :
        return jsonify(status="ok",data=res)
    else:
        return jsonify(status="no")



@api.route('/viewskill',methods=['post'])
def viewskill():
    data={}
    
    r="select * from skills"
    res=select(r)
    if res :
        return jsonify(status="ok",data=res)
    else:
        return jsonify(status="no")
@api.route('/viewskillandcate',methods=['post'])
def viewskillandcate():
    data={}
    
    r="select * from myskills"
    res=select(r)
    if res :
        return jsonify(status="ok",data=res)
    else:
        return jsonify(status="no")
@api.route('/user_view_skill_cate',methods=['post'])
def user_view_skill_cate():
    data={}
    userid=request.form['user_id']
    print("jjjjjjjjjjjjjjj",userid)
    
    r="select * from myskills inner join badgeorachive using(badgeorchive_id) inner join skills using(skills_id) where user_id='%s'"%(userid)
    res=select(r)
    if res :
        return jsonify(status="ok",data=res)
    else:
        return jsonify(status="no")
@api.route('/user_sendrequest',methods=['post'])
def user_sendrequest():
    details=request.form['details']
    login_id=request.form['login_id']
    mysk=request.form['mysk']
    y="insert into request values(null,'%s',(select user_id from user where login_id='%s'),'pending','%s',curdate(),'pending')"%(mysk,login_id,details)
    res=insert(y)
    if res :
        return jsonify(status="ok",data=res)
    else:
        return jsonify(status="no")
@api.route('/user_add_project',methods=['post'])
def user_add_project():
    project=request.form['project']
    details=request.form['details']
    amount=request.form['amount']
    login_id=request.form['login_id']
    t="select * from user where login_id='%s'"%(login_id)
    re2=select(t)
    if re2:
        user_id=re2[0]['user_id']

    y="insert into projects values(null,'%s','%s','%s',curdate(),'%s','Available')"%(user_id,project,details,amount)
    res=insert(y)
    if res :
        return jsonify(status="ok",data=res)
    else:
        return jsonify(status="no")

@api.route('/user_view_project',methods=['post'])
def user_view_project():
    data={}
    login_id=request.form['login_id']
    y="select * from user where login_id='%s'"%(login_id)
    re2=select(y)
    if re2:
        user_id=re2[0]['user_id']
    r="select * from projects where user_id='%s'"%(user_id)
    res=select(r)
    if res :
        return jsonify(status="ok",data=res)
    else:
        return jsonify(status="no")
@api.route('/user_view_other_project',methods=['post'])
def user_view_other_project():
    data={}
    login_id=request.form['login_id']
    y="select * from user where login_id='%s'"%(login_id)
    re2=select(y)
    if re2:
        user_id=re2[0]['user_id']
    r="select * from projects where not user_id='%s'"%(user_id)
    res=select(r)
    if res :
        return jsonify(status="ok",data=res)
    else:
        return jsonify(status="no")
@api.route('/user_add_highlights',methods=['post'])
def user_add_highlights():
    highlights=request.form['highlights']
    image=request.files['pic']
    path="static/images/"+str(uuid.uuid4())+image.filename
    image.save(path)
    proid=request.form['proid']
    
    

    y="insert into highlights values(null,'%s','%s','%s')"%(proid,highlights,path)
    res=insert(y)
    if res :
        return jsonify(status="ok",data=res)
    else:
        return jsonify(status="no")
@api.route('/user_view_highlight',methods=['post'])
def user_view_highlight():
    data={} 
    pro_id=request.form['pro_id']
    r="select * from highlights where project_id='%s'"%(pro_id)
    res=select(r)
    if res :
        return jsonify(status="ok",data=res)
    else:
        return jsonify(status="no")
@api.route('/prorequest',methods=['post'])
def prorequest():
    data={}
    
    login_id=request.form['login_id']
    pro_id=request.form['pro_id']
    print("oooooooooooo",login_id)
    r = "INSERT INTO prequest VALUES (NULL, (SELECT user_id FROM user WHERE login_id='%s'), '%s', CURDATE(), 'pending')" % (login_id, pro_id)
    res=insert(r)
    if res :
        return jsonify(status="ok",data=res)
    else:
        return jsonify(status="no")

@api.route('/user_send_comp',methods=['post'])
def user_send_comp():
    data={}
    login_id=request.form['login_id']
    
    comp=request.form['comp']
    t="select * from user where login_id='%s'"%(login_id)
    res3=select(t)
    if res3:
        user_id=res3[0]['user_id']

    r="insert into complaint values(null,'%s','%s','pending',curdate())"%(user_id,comp)
    res=insert(r)
    if res :
        return jsonify(status="ok",data=res)
    else:
        return jsonify(status="no")
@api.route('/user_view_comp',methods=['post'])
def user_view_comp():
    data={} 
    login_id=request.form['login_id']
    user_id=request.form['user_id']
    r="select * from complaint where user_id=(select user_id from user where login_id='%s')"%(login_id)
    res=select(r)
    print(r)
    if res :
        return jsonify(status="ok",data=res)
    else:
        return jsonify(status="no")
@api.route('/View_Requested_Projects',methods=['post'])
def View_Requested_Projects():
    data={} 
    login_id=request.form['login_id']
    user_id=request.form['user_id']
    
    r="select *,prequest.status as stat from prequest inner join projects on projects.project_id=prequest.project_id where prequest.user_id=(SELECT user_id FROM user WHERE login_id='%s')"%(login_id)
    res=select(r)
    if res :
        return jsonify(status="ok",data=res)
    else:
        return jsonify(status="no")

@api.route('/view_other_request',methods=['get'])
def view_other_request():
    data={} 
    login_id=request.args['login']
    # user_id=request.form['user_id']
    
    print(login_id,'///////////////////hguhukhuk///')
    r="""
SELECT 
    request.request_id,
    request.user_id AS requester_user_id,
    request.amount,
    request.details,
    request.date,
    request.status AS stat,

    myskills.myskills_id,
    myskills.skills_id,
    myskills.user_id AS skill_owner_user_id,
    myskills.badgeorchive_id,

    skills.skills AS skill_name,

    skill_owner.ufname AS skill_owner_fname,
    skill_owner.ulname AS skill_owner_lname,
    skill_owner.place AS skill_owner_place,
    skill_owner.phone AS skill_owner_phone,
    skill_owner.email AS skill_owner_email,

    requester.ufname AS requester_fname,
    requester.ulname AS requester_lname,
    requester.phone AS requester_phone,
    requester.email AS requester_email

FROM request
INNER JOIN myskills ON request.myskills_id = myskills.myskills_id
INNER JOIN skills ON myskills.skills_id = skills.skills_id

-- Join to get skill owner details
INNER JOIN USER AS skill_owner ON myskills.user_id = skill_owner.user_id

-- Join to get requester (person who sent request) details
INNER JOIN USER AS requester ON request.user_id = requester.user_id

-- Exclude requests made by logged-in user
WHERE request.user_id != (SELECT user_id FROM USER WHERE login_id = '%s');


    """%(login_id)
    # r="select *,prequest.status as stat from prequest inner join projects on projects.project_id=prequest.project_id where projects.user_id=(SELECT user_id FROM user WHERE login_id='%s')"%(login_id)
    res=select(r)
    if res :
        return jsonify(status="success",data=res)
    else:
        return jsonify(status="no")
@api.route('/user_accept_req',methods=['get'])
def user_accept_req ():
    data={} 
    
    login_id=request.args['login_id']
    req_id=request.args['req_id']
    print('kkkkkkkkkkkkkkk',req_id)
    u="update request set status='accept' where request_id='%s'"%(req_id)
    res=update(u)
    if res :

        return jsonify(status="ok",data=res)
    else:
        return jsonify(status="no")
@api.route('/user_reject_req',methods=['post'])
def user_reject_req ():
    data={} 
    pro_id=request.form['pro_id']
    login_id=request.form['login_id']
    req_id=request.form['req_id']
    
    u="update prequest set status='reject' where project_id='%s' and prequest_id='%s'"%(pro_id,req_id)
    res=update(u)
    if res :

        return jsonify(status="ok",data=res)
    else:
        return jsonify(status="no")

@api.route('/user_view_payment_1',methods=['post'])
def user_view_payment_1():
    data={} 
    login_id=request.form['login_id']
    req_id=request.form['req_id']
    r="select * from payment where request_id='%s'"%(req_id)
    res=select(r)
    if res :
        return jsonify(status="ok",data=res)
    else:
        return jsonify(status="no")
@api.route('/user_add_issue',methods=['post'])
def user_add_issue():
    data={} 
    issue=request.form['issue']
    image=request.files['pic']
    path="static/images/"+str(uuid.uuid4())+image.filename
    image.save(path)
    req_id=request.form['req_id']
    r="insert into issues values(null,'%s','%s','%s')"%(req_id,issue,path)
    res=insert(r)
    if res :
        return jsonify(status="ok",data=res)
    else:
        return jsonify(status="no")

@api.route('/user_view_issue',methods=['post'])
def user_view_issue():
    data={} 
    login_id=request.form['login_id']
    req_id=request.form['req_id']
    r="select * from issues where prequest_id='%s'"%(req_id)
    res=select(r)
    if res :
        return jsonify(status="ok",data=res)
    else:
        return jsonify(status="no")

@api.route('/user_make_payment_1',methods=['post'])
def user_make_payment_1():
    data={} 
    pre_id=request.form['pre_id']
    amount=request.form['amount']
   
    r="insert into payment values(null,'%s','projects','%s',curdate())"%(pre_id,amount)
    res=insert(r)
    if res :
        return jsonify(status="ok",data=res)
    else:
        return jsonify(status="no")
@api.route('/user_search_user',methods=['post'])
def user_search_user():
    data={} 
    login_id=request.form['login_id']
    print("////////////////////",login_id)
    skill_id=request.form['skill_id']
    r="""SELECT * FROM USER INNER JOIN myskills USING(user_id) INNER JOIN badgeorachive USING(badgeorchive_id) INNER JOIN skills USING(skills_id) WHERE NOT login_id='%s' and myskills.skill_id='%s'"""%(login_id,skill_id)
    res=select(r)
    if res :
        return jsonify(status="ok",data=res)
    else:
        return jsonify(status="no")




@api.route('/user_search_sendrequest',methods=['post'])
def user_search_sendrequest():
    details=request.form['details']
    login_id=request.form['login_id']
    mysk=request.form['mysk']
    y="insert into request values(null,'%s',(select user_id from user where login_id='%s'),'pending','%s',curdate(),'pending')"%(mysk,login_id,details)
    res=insert(y)
    if res :
        return jsonify(status="ok",data=res)
    else:
        return jsonify(status="no")
@api.route('/search_skill',methods=['post'])
def search_skill():
    data={} 
    skill_id=request.form['skill_id']
    r="select * from user inner join myskills using(user_id) inner join badgeorachive using(badgeorchive_id) inner join skills using(skills_id) where skills_id='%s'"%(skill_id)
    res=select(r)
    
    if res :
        return jsonify(status="ok",data=res)
    else:
        return jsonify(status="no")
# @api.route('/search_skill',methods=['post'])
# def search_skill():
#     data={} 
#     s=request.form['skillorbadge']
    
#     r="select * from user inner join myskills using(user_id) inner join badgeorachive using(badgeorchive_id) inner join skills using(skills_id) where skills like '%s' or badgeorachive like '%s'"%(s,s)
#     res=select(r)
    
#     if res :
#         return jsonify(status="ok",data=res)
#     else:
#         return jsonify(status="no")
@api.route('/pro_unavailable',methods=['post'])
def pro_unavailable():
    project_id=request.form['project_id']
    y="update projects set status='unavailable' where project_id='%s'"%(project_id)
    res=update(y)
    if res :
        return jsonify(status="ok",data=res)
    else:
        return jsonify(status="no")
@api.route('/pro_available',methods=['post'])
def pro_available():
    project_id=request.form['project_id']
    y="update projects set status='Available' where project_id='%s'"%(project_id)
    res=update(y)
    if res :
        return jsonify(status="ok",data=res)
    else:
        return jsonify(status="no")



@api.route('/user_view_skill_badgeorachive',methods=['post'])
def user_view_skill_badgeorachive():
    data={}
    login_id=request.form['login_id']
    
    r="select * from myskills inner join badgeorachive on myskills.badgeorchive_id=badgeorachive.badgeorchive_id inner join skills using(skills_id) where user_id=(select user_id from user where login_id='%s')"%(login_id)
    res=select(r)
    if res :
        return jsonify(status="ok",data=res)
    else:
        return jsonify(status="no")
@api.route('/deleteskill',methods=['post'])
def deleteskill():
    
    myid=request.form['myid']
    
    r="delete from myskills where myskills_id='%s'"%(myid)
    res=delete(r)
    print("pppppppppppppppp",res)
    if res :
        return jsonify(status="ok",data=res)
    else:
        return jsonify(status="no")
@api.route('/deleteproject',methods=['post'])
def deleteproject():
    
    proid=request.form['pro_id']
    t="delete from highlights where project_id='%s'"%(proid)
    delete(t)
    r="delete from projects where project_id='%s'"%(proid)
    res=delete(r)

    
    if res :
        return jsonify(status="ok",data=res)
    else:
        return jsonify(status="no")




# ++++++++++++++++++++++\


@api.route('/user_view_request',methods=['post'])
def user_view_request():
    data={}
    login_id = request.form['login_id']
    # q="SELECT * FROM `request` INNER JOIN `user` USING(user_id) INNER JOIN `myskills` USING (myskills_id)INNER JOIN `skills` ON `skills`.`skills_id` =`myskills`.`skill_id` where `user`.user_id=(select user_id from user where login_id<>'%s') "%(login_id)
    q="""SELECT r.request_id,r.myskills_id,s.skills,u2.`user_id`,u1.`login_id`,u2.phone,r.amount,r.details,r.date,r.status,u1.ufname,u1.ulname 
FROM request r,USER u1,USER u2,myskills m,skills s 
WHERE r.user_id=u1.user_id AND r.`myskills_id`=m.`myskills_id`AND m.`skills_id`=s.`skills_id` 
AND m.user_id=u2.user_id AND  r.user_id IN (SELECT user_id FROM USER WHERE login_id != '%s')"""  %(login_id)
    print(q)
    res=select(q)
    if res :
        return jsonify(status="ok",data=res)
    else:
        return jsonify(status="no")


@api.route('/user_send_amts',methods=['post'])
def user_send_amts():
    amtss=request.form['amtss']    
    detss=request.form['detss']    
    req_id=request.form['req_id']
    q="update `request` set amount='%s',details='%s',status='amount_sended' where request_id='%s'"%(amtss,detss,req_id)
    res=update(q)
    if res :
        return jsonify(status="ok",data=res)
    else:
        return jsonify(status="no")





@api.route('/user_view_sended_request',methods=['post'])
def user_view_sended_request():
    data={}
    login_id = request.form['login_id']
    # q="SELECT * FROM `request` INNER JOIN `user` USING(user_id) INNER JOIN `myskills` USING (myskills_id)INNER JOIN `skills` ON `skills`.`skills_id` =`myskills`.`skill_id` where `user`.user_id=(select user_id from user where login_id='%s') "%(login_id)
    q="SELECT r.request_id,r.myskills_id,s.skills,u2.`user_id`,u2.`login_id`,u2.phone,r.amount,r.details,r.date,r.status,u2.ufname,u2.ulname FROM request r,USER u1,USER u2,myskills m,skills s WHERE r.user_id=u1.user_id AND r.`myskills_id`=m.`myskills_id` AND m.`skills_id`=s.`skills_id` AND m.user_id=u2.user_id and  r.user_id=(select user_id from user where login_id='%s')"  %(login_id)
    print(q)
    res=select(q)
    if res :
        return jsonify(status="ok",data=res)
    else:
        return jsonify(status="no") 



@api.route('/user_make_payment',methods=['post'])
def user_make_payment():
    amtss=request.form['amts']    
    req_id=request.form['req_id']
    q="update `request` set status='paid' where request_id='%s'"%(req_id)
    print(q)
    update(q)    
    q="insert into `payment` values(null,'%s','skill','%s',curdate())"%(req_id,amtss)
    print(q)
    res=insert(q)
    if res :
        return jsonify(status="ok",data=res)
    else:
        return jsonify(status="no")





@api.route('/user_sended_chat',methods=['post'])
def user_sended_chat():
    sender_id=request.form['sender_id']    
    receiver_id=request.form['receiver_id']
    print("r_sender_id",sender_id)
    print("r_receiver_id",receiver_id)
    chat=request.form['details']
  
    q="insert into `chat` values(null,'%s',(select login_id from user where user_id='%s'),'%s',curdate())"%(sender_id,receiver_id,chat)
    print(q)
    res=insert(q)
    if res :
        return jsonify(status="ok",data=res)
    else:
        return jsonify(status="no")





@api.route('/user_view_sended_chat',methods=['post'])
def user_view_sended_chat():
    sender_id=request.form['sender_id']    
    receiver_id=request.form['receiver_id']
    print("sender_id",sender_id)
    print("receiver_id",receiver_id)
    q="SELECT * FROM `chat` where sender_id='%s' and receiver_id=(select login_id from user where user_id='%s') or sender_id=(select login_id from user where user_id='%s') and receiver_id='%s' "%(sender_id,receiver_id,receiver_id,sender_id)
    print(q)

    res=select(q)
    if res :
        return jsonify(status="ok",data=res)
    else:
        return jsonify(status="no")



@api.route('/usersend_view_request_chat',methods=['post'])
def usersend_view_request_chat():
    sender_id=request.form['sender_id']    
    receiver_id=request.form['receiver_id']
    chat=request.form['details']
  
    q="insert into `chat` values(null,'%s','%s','%s',curdate())"%(sender_id,receiver_id,chat)
    print(q)
    res=insert(q)
    if res :
        return jsonify(status="ok",data=res)
    else:
        return jsonify(status="no")







@api.route('/user_view_request_chat',methods=['post'])
def user_view_request_chat():
    sender_id=request.form['sender_id']    
    receiver_id=request.form['receiver_id']
    q="SELECT * FROM `chat` where (sender_id='%s' and receiver_id='%s') or (sender_id='%s' and receiver_id='%s') "%(sender_id,receiver_id,receiver_id,sender_id)
    print(q)

    res=select(q)
    if res :
        return jsonify(status="ok",data=res)
    else:
        return jsonify(status="no")




@api.route('/user_view_payment',methods=['post'])
def user_view_payment():
    req_id=request.form['req_id']    
    q="SELECT * FROM `payment` inner join request using(request_id) inner join user using (user_id) where request_id='%s' "%(req_id)
    print(q)

    res=select(q)
    if res :
        return jsonify(status="ok",data=res)
    else:
        return jsonify(status="no")

@api.route('/user_view_upload',methods=['post'])
def user_view_upload():
    data={} 
    # login_id=request.form['login_id']
    # req_id=request.form['req_id']
    # r="select * from issues where prequest_id='%s'"%(req_id)
    r="select * from upload "
    res=select(r)
    if res :
        return jsonify(status="ok",data=res)
    else:
        return jsonify(status="no")

@api.route('/user_view_notes',methods=['post'])
def user_view_notes():
    data={} 
    # login_id=request.form['login_id']
    # req_id=request.form['req_id']
    # r="select * from issues where prequest_id='%s'"%(req_id)
    r="select * from notes "
    res=select(r)
    if res :
        return jsonify(status="ok",data=res)
    else:
        return jsonify(status="no")
    
    
    
@api.route('/add_payment',methods=['get','post'])
def add_payment():
    data={}
    amount=request.args['amount']
    login_id=request.args['login_id']
    req_id=request.args['req_id']
    
    print("amount",amount)
    print("login_id",login_id)
    print("req_id",req_id)
    res="update request set amount='%s' ,status='amount_sended' where  request_id='%s' and user_id='%s'"%(amount,req_id,login_id)
    ok=update(res)
    if ok :
        return jsonify(status="ok",data=ok)
    else:
        return jsonify(status="no")
@api.route('/upload_video', methods=['POST', 'GET'])
def upload_video():
    try:
        print("Request received", file=sys.stderr)
        req_id=request.form.get('req_id')
        print("Request ID:", req_id)

        if 'video' not in request.files:
            print("No video file part", file=sys.stderr)
            return jsonify(status="error", method="upload_video", message="No video file provided")

        video = request.files['video']
        if video.filename == '':
            print("Empty filename", file=sys.stderr)
            return jsonify(status="error", method="upload_video", message="Empty filename")

        title = request.form.get('title', 'Untitled')
        print("Title:", title, file=sys.stderr)

        # Save path
        save_dir = "static/videos/"
        os.makedirs(save_dir, exist_ok=True)
        filename = str(uuid.uuid4()) + "_" + video.filename
        path = os.path.join(save_dir, filename)

        video.save(path)
        print("Saved video at:", path, file=sys.stderr)

        # DB insert
        q = "INSERT INTO videos (request_id, title, videos, date) VALUES ('%s', '%s', '%s', CURDATE())" % (
            req_id,title, path
        )
        res = insert(q)
        print("Insert result:", res, file=sys.stderr)

        if res:
            return jsonify(status="success", method="upload_video", message="Video uploaded successfully")
        else:
            os.remove(path)
            return jsonify(status="error", method="upload_video", message="Database error")

    except Exception as e:
        print("Exception:", str(e), file=sys.stderr)
        return jsonify(status="error", method="upload_video", message="Exception: " + str(e))
import sys

@api.route('/add_class', methods=['GET'])
def add_class():
    try:
        # Get parameters
        class_name = request.args.get('class', '')
        meetlink = request.args.get('meetlink', '')
        request_id = request.args.get('request_id', '')
        login_id = request.args.get('lid', '')
        
        # Insert into database
        q = "INSERT INTO classes (request_id, class, meetlink) VALUES ('%s', '%s', '%s')" % (
            request_id, class_name, meetlink
        )
        res = insert(q)

        if res:
            return jsonify(status="success", method="add_class")
        else:
            return jsonify(status="no", method="add_class")

    except Exception as e:
        print("Add class error:", str(e))
        return jsonify(status="no", method="add_class", message=str(e))

@api.route('/view_feedback', methods=['GET'])
def view_feedback():
    try:
        request_id = request.args.get('request_id')
        if not request_id:
            return jsonify(status="error", message="Request ID is required")

        q = """SELECT feedback.*, 
               user.ufname, user.ulname 
               FROM feedback 
               INNER JOIN user ON feedback.user_id = user.user_id 
               WHERE feedback.request_id = '%s'""" % (request_id)
        
        res = select(q)
        
        if res:
            return jsonify(status="success", data=res)
        else:
            return jsonify(status="no", message="No feedback found")

    except Exception as e:
        print("View feedback error:", str(e))
        return jsonify(status="error", message=str(e))

@api.route('/user_view_videos', methods=['GET'])
def user_view_videos():
    try:
        request_id = request.args.get('req_id')
        if not request_id:
            return jsonify(status="error", message="Request ID is required")

        q = """SELECT video_id, request_id, title, videos, date 
               FROM videos 
               WHERE request_id = '%s'
               ORDER BY date DESC""" % (request_id)
        
        res = select(q)
        if res:
            return jsonify(status="success", data=res)
        else:
            return jsonify(status="no", message="No videos found")

    except Exception as e:
        print("View videos error:", str(e))
        return jsonify(status="error", message=str(e))

@api.route('/view_class', methods=['GET'])
def view_class():
    try:
        request_id = request.args.get('request_id')
        if not request_id:
            return jsonify(status="error", message="Request ID is required")

        q = """SELECT class_id, request_id, class, meetlink 
               FROM classes 
               WHERE request_id = '%s'
               ORDER BY class_id DESC""" % (request_id)
        
        res = select(q)
        if res:
            return jsonify(status="success", data=res)
        else:
            return jsonify(status="no", message="No classes found")

    except Exception as e:
        print("View class error:", str(e))
        return jsonify(status="error", message=str(e))

@api.route('/user_send_feedback', methods=['GET'])
def user_send_feedback():
    try:
        feedback = request.args.get('feedback')
        request_id = request.args.get('request_id')
        login_id = request.args.get('login_id')
        
        if not all([feedback, request_id]):
            return jsonify(status="error", message="Feedback and request ID are required")

        # Fix NULL handling for user_id
        q = """INSERT INTO feedback (request_id, feedback, user_id, date) 
                   VALUES ('%s', '%s', (select user_id from user where login_id='%s'), CURDATE())""" % (
                request_id, feedback, login_id)
        res = insert(q)
        if res:
            return jsonify(status="success", message="Feedback submitted successfully")
        else:
            return jsonify(status="no", message="Failed to submit feedback")

    except Exception as e:
        print("Send feedback error:", str(e))
        return jsonify(status="error", message=str(e))


@api.route('/status_Completed', methods=['GET','POST'])
def status_Completed():
    try:
        request_id = request.args.get('request_id')
        if not request_id:
            return jsonify(status="error", message="Request ID is required")

        q = "UPDATE request SET status='Completed' WHERE request_id='%s'" % (request_id)
        res = update(q)

        if res:
            return jsonify(status="success", message="Status updated to Completed")
        else:
            return jsonify(status="no", message="Failed to update status")

    except Exception as e:
        print("Status update error:", str(e))
        return jsonify(status="error", message=str(e))
    
    
@api.route('/view_certificate', methods=['GET','POST'])
def view_certificate():
    try:
        request_id = request.args.get('request_id')
        if not request_id:
            return jsonify(status="error", message="Request ID is required")

        q = """SELECT certificate_id, request_id, file, date 
               FROM certificate 
               WHERE request_id = '%s'""" % (request_id)
        
        res = select(q)
        print(q)
        if res:
            return jsonify(status="success", data=res)
        else:
            return jsonify(status="no", message="No certificates found")

    except Exception as e:
        print("View certificate error:", str(e))
        return jsonify(status="error", message=str(e))
    
    
@api.route('/view_skills', methods=['POST', 'GET'])
def view_skills():
    data={}
    y="select * from skills"
    res=select(y)
    if res :
        return jsonify(status="success",data=res)
    else:
        return jsonify(status="no")