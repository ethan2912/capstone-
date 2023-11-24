import cv2
import streamlit as st
import image_dehazer
from pathlib import Path

def dehaze_video(input_video_path, output_video_path, frame_skip=1):
     # Open the input video
    cap = cv2.VideoCapture(input_video_path)

    # Get the video's frame width and height
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))

    # Create a VideoWriter object to save the processed video with the same dimensions as the input
    out = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(*'XVID'), 60, (frame_width, frame_height))

    # Create an instance of the image_dehazer
    dehazer = image_dehazer.image_dehazer()

    frame_count = 0

    frame_placeholder = st.empty()
    frame_placeholder_1 = st.empty()
    stop_button_pressed = st.button("stop")


    while True:
        ret, frame = cap.read()
        if not ret:
            st.write("the video is ended")
            break

        # Process every "frame_skip" frames and skip the rest
        if frame_count % frame_skip == 0:
            # Process the frame to remove haze
            dehazed_frame, _ = dehazer.remove_haze(frame)

            # Write the processed frame to the output video
            out.write(dehazed_frame)

            # Display the original and processed frames
            #cv2.imshow('Original Frame', frame)
            #cv2.imshow('Dehazed Frame', dehazed_frame)
            #frame_placeholder.image(dehazed_frame, channels="RGB")
            frame_placeholder.image(frame,channels="RGB")
            frame_placeholder_1.image(dehazed_frame, channels="RGB")

        frame_count += 1

        if cv2.waitKey(1) & 0xFF == ord('q') or stop_button_pressed:
            break

    # Release the video objects
    cap.release()
    out.release()

    # Close all OpenCV windows
    cv2.destroyAllWindows()
    # Rest of your dehazing code

if __name__ == "__main__":
    st.title("Video Dehazing App")

    uploaded_file = st.file_uploader("Upload a video file", type=["mp4", "avi", "mov"])

    if uploaded_file is not None:
        input_video_path = Path("input_video.mp4")
        input_video_path.write_bytes(uploaded_file.read())

        # Display the uploaded video
        #st.video(str(input_video_path))

        frame_skip = st.slider("Frame Skip", 1, 50, 20)

        if st.button("Process"):
            output_video_path = Path("output_video.mp4")
            dehaze_video(str(input_video_path), str(output_video_path), frame_skip)

            # Display the dehazed video
           # st.title("Dehazed Video")
           # st.video(output_video_path)
