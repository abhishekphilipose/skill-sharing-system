from flask import Blueprint, render_template, request
from pyzbar.pyzbar import decode
from PIL import Image
import hashlib, os

verify = Blueprint('verify', __name__)

def generate_hash(data: str) -> str:
    return hashlib.sha256(data.encode()).hexdigest()

@verify.route('/verify', methods=['GET', 'POST'])
def verify_page():
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
                recalculated_hash = generate_hash(combined_data)

                # Compare
                if qr_hash == recalculated_hash:
                    result = "✅ Certificate is VALID and untampered."
                else:
                    result = "❌ Certificate is INVALID or TAMPERED!"

    return render_template("verify.html", result=result)
