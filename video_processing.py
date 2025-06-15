import cv2
import os

def center_handle(x, y, w, h):
    x1 = int(w / 2)
    y1 = int(h / 2)
    cx = x + x1
    cy = y + y1
    return cx, cy

def process_video(input_path, filename):
    cap = cv2.VideoCapture(input_path)
    count_line_position = 550
    min_width_react = 80
    min_height_react = 80
    algo = cv2.bgsegm.createBackgroundSubtractorMOG()

    detect = []
    offset = 6
    counter = 0

    # Output file path
    output_path = os.path.join("static/processed", filename)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = cap.get(cv2.CAP_PROP_FPS)
    width  = int(cap.get(3))
    height = int(cap.get(4))
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(grey, (3, 3), 5)
        img_sub = algo.apply(blur)
        dilat = cv2.dilate(img_sub, cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5)))
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        dilatada = cv2.morphologyEx(dilat, cv2.MORPH_CLOSE, kernel)
        dilatada = cv2.morphologyEx(dilatada, cv2.MORPH_CLOSE, kernel)
        counterShape, _ = cv2.findContours(dilatada, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        cv2.line(frame, (25, count_line_position), (width - 25, count_line_position), (255, 127, 0), 3)

        for c in counterShape:
            (x, y, w, h) = cv2.boundingRect(c)
            if w >= min_width_react and h >= min_height_react:
                center = center_handle(x, y, w, h)
                detect.append(center)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.circle(frame, center, 4, (0, 0, 255), -1)

        for (x, y) in detect:
            if count_line_position - offset < y < count_line_position + offset:
                counter += 1
                detect.remove((x, y))

        cv2.putText(frame, "Vehicle Counter: " + str(counter), (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)
        out.write(frame)

    cap.release()
    out.release()
    return filename, counter
