from storage import db_empty, get_name_by_filepath, mark_attendance
from pathlib import Path
from deepface.modules.exceptions import FaceNotDetected, SpoofDetected
import streamlit as st
from deepface import DeepFace
import numpy as np
from PIL import Image
import cv2 as cv

st.session_state.authenticator.login(location="unrendered")


TOLERANCE = 0.54
SCALE = 2
FONT = cv.FONT_HERSHEY_DUPLEX
FONT_SCALE = 0.7


def get_name(person):
    parts = Path(person["identity"]).parts
    filepath = "//".join(parts)
    name = get_name_by_filepath(filepath)
    return name


def mark_attendances(names: list[str]):
    for name in names:
        if name == "Unknown":
            st.warning("Face not recognized.")
            continue
        mark_attendance(name)
        st.success(f"Marked Attendance: {name}")


def draw_rectangle(frame, person):
    frame = np.copy(frame)
    x = person["source_x"].tolist()
    y = person["source_y"].tolist()
    w = person["source_w"].tolist()
    h = person["source_h"].tolist()
    cv.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
    cv.rectangle(frame, (x, y + h), (x + w, y + h + 35), (0, 0, 255), cv.FILLED)
    name = get_name(person)
    cv.putText(frame, name, (x + 6, y + h + 24), FONT, FONT_SCALE, (255, 255, 255), 1)
    return frame


img = st.camera_input("Webcam")
if img:
    if db_empty():
        st.error("No images in database")
        st.stop()
    frame = np.array(Image.open(img))
    try:
        res = DeepFace.find(
            frame,
            "database",
            batched=True,
            detector_backend="mtcnn",
            anti_spoofing=True,

        )
    except FaceNotDetected:
        st.write("Face not detected")
        st.stop()
    except SpoofDetected:
        st.error("Image spoofing detected")
        st.stop()

    names = []
    for person in res:
        print(person)
        person = person[0]
        name = get_name(person)
        names.append(name)
        frame = draw_rectangle(frame, person)

    st.image(frame)
    st.button("Mark attendance", on_click=lambda: mark_attendances(names))
