import cv2
from flask import Flask, render_template, render_template_string, Response

app = Flask(__name__)
video_capture = cv2.VideoCapture(2)


def gen():
    while True:
        ret, image = video_capture.read()
        cv2.imwrite('t.jpg', image)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + open('t.jpg', 'rb').read() + b'\r\n')
    video_capture.release()


@app.route('/')
def index():
    """Video streaming"""
    # return render_template('index.html')
    return render_template_string('''<html>
<head>
    <title>Video Streaming </title>
</head>
<body>
    <div>
        <h1>Image</h1>
        <img id="img" src="{{ url_for('video_feed') }}">
    </div>

<script >
    var ctx = document.getElementById("canvas").getContext('2d');
    var img = new Image();
    img.src = "{{ url_for('video_feed') }}";

    window.setInterval("refreshCanvas()", 50);

</script>

</body>
</html>''')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run()
