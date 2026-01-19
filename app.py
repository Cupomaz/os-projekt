import os
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename
from PIL import Image as PILImage
import uuid
from config import Config
from models import db, Image
from forms import UploadForm

app = Flask(__name__)
app.config.from_object(Config)

# Initialize database
db.init_app(app)

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def validate_image(file):
    """Validate that the file is a real image"""
    try:
        img = PILImage.open(file)
        img.verify()
        file.seek(0)  # Reset file pointer after verification
        return True
    except Exception:
        return False

@app.route('/', methods=['GET', 'POST'])
def index():
    form = UploadForm()
    
    if form.validate_on_submit():
        file = form.image.data
        
        # Additional validation
        if not allowed_file(file.filename):
            flash('Invalid file type. Only images are allowed.', 'error')
            return redirect(url_for('index'))
        
        if not validate_image(file):
            flash('Invalid image file. Please upload a valid image.', 'error')
            return redirect(url_for('index'))
        
        # Generate unique filename
        original_filename = secure_filename(file.filename)
        extension = original_filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid.uuid4().hex}.{extension}"
        
        # Save file
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.seek(0)  # Reset file pointer
        file.save(file_path)
        
        # Get file size
        file_size = os.path.getsize(file_path)
        
        # Save to database
        new_image = Image(
            filename=unique_filename,
            original_filename=original_filename,
            file_size=file_size,
            description=form.description.data
        )
        db.session.add(new_image)
        db.session.commit()
        
        flash('Image uploaded successfully!', 'success')
        return redirect(url_for('index'))
    
    # Get all images from database
    images = Image.query.order_by(Image.upload_date.desc()).all()
    
    return render_template('index.html', form=form, images=images)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/delete/<int:image_id>', methods=['POST'])
def delete_image(image_id):
    image = Image.query.get_or_404(image_id)
    
    # Delete file from filesystem
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
    if os.path.exists(file_path):
        os.remove(file_path)
    
    # Delete from database
    db.session.delete(image)
    db.session.commit()
    
    flash('Image deleted successfully!', 'success')
    return redirect(url_for('index'))

@app.cli.command()
def init_db():
    """Initialize the database."""
    db.create_all()
    print('Database initialized!')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
