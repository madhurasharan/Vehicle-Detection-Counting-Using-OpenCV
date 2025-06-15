from flask import Flask, render_template, request, redirect, url_for
import os
from video_processing import process_video

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['PROCESSED_FOLDER'] = 'static/processed'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    video = request.files['video']
    if video:
        filename = video.filename
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        video.save(upload_path)

        # Process and return count + processed filename
        processed_filename, vehicle_count = process_video(upload_path, filename)

        return render_template('result.html',
                               processed_video=processed_filename,
                               count=vehicle_count)
    return redirect(url_for('index'))

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['PROCESSED_FOLDER'], exist_ok=True)
    app.run(debug=True)
