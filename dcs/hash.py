import hashlib
import os
from flask import Blueprint, render_template, request
from database import *
import segno

hash = Blueprint('hash', __name__)

def generate_hash(data: str) -> str:
    return hashlib.sha256(data.encode()).hexdigest()

# @hash.route('/', methods=['GET', 'POST'])
def home():
    data = {}

    if request.method == 'POST' and 'sub' in request.form:
        name = request.form['name']
        course = request.form['course']
        date = request.form['date']

        # Insert into DB
        query = "INSERT INTO details (name, course, date) VALUES ('%s', '%s', '%s')" % (name, course, date)
        res=insert(query)

        # Get last inserted ID
        cert_id = res

        # Combine data and generate hash
        combined = f"{name}|{course}|{date}|{cert_id}"
        hash_val = generate_hash(combined)

        # Generate QR and save
        qr = segno.make_qr(hash_val)
        qr_filename = f"cert_{cert_id}.png"
        qr_path = os.path.join('static', qr_filename)
        qr.save(qr_path, scale=5)
        u="update details set qr='%s' where id='%s'"%(qr_path,cert_id)
        update(u)
        # Prepare data to send to HTML
        data = {
            'name': name,
            'course': course,
            'date': date,
            'qr': qr_filename,
            'msg': "✅ QR generated successfully!"
        }

    return render_template('home.html', data=data)




 


        

