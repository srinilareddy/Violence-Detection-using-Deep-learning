from flask import Flask, request, jsonify
import os
import cv2
import numpy as np

app = Flask(__name__)

# Dataset paths
violence_dataset_path = r"D:\New folder\violence Detection Project\Real Life Violence Dataset\Violence"
non_violence_dataset_path = r"D:\New folder\violence Detection Project\Real Life Violence Dataset\NonViolence"
temp_path = "temp"

# Helper function to extract frames from a video
def extract_frames(video_path):
    cap = cv2.VideoCapture(video_path)
    frames = []
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.resize(frame, (224, 224))  # Resize frames for consistency
        frames.append(frame)
    cap.release()
    return np.array(frames)

# Function to compute frame similarity
def compute_similarity(video_frames, dataset_frames):
    similarities = []
    for dataset_video in dataset_frames:
        similarity = np.mean([
            np.mean(cv2.absdiff(frame1, frame2))
            for frame1, frame2 in zip(video_frames, dataset_video)
        ])
        similarities.append(similarity)
    return similarities

# Compare uploaded video with dataset
def compare_video_with_dataset(uploaded_video_path, dataset_path):
    uploaded_frames = extract_frames(uploaded_video_path)
    if len(uploaded_frames) == 0:
        return "No frames in uploaded video"

    dataset_videos = os.listdir(dataset_path)
    dataset_frames = [extract_frames(os.path.join(dataset_path, video)) for video in dataset_videos]

    similarities = compute_similarity(uploaded_frames, dataset_frames)
    closest_match_index = np.argmin(similarities)  # Find the most similar video
    closest_match_video = dataset_videos[closest_match_index]
    return closest_match_video

@app.route('/classify', methods=['POST'])
def classify_video():
    video = request.files.get('video')
    if not video:
        return jsonify({"error": "No video uploaded"}), 400

    os.makedirs(temp_path, exist_ok=True)
    temp_video_path = os.path.join(temp_path, video.filename)
    video.save(temp_video_path)

    try:
        violence_match = compare_video_with_dataset(temp_video_path, violence_dataset_path)
        non_violence_match = compare_video_with_dataset(temp_video_path, non_violence_dataset_path)

        # Determine if the closest match is violent or non-violent
        if violence_match:
            result = {"type": "Violence", "match": violence_match}
        elif non_violence_match:
            result = {"type": "Non-Violence", "match": non_violence_match}
        else:
            result = {"type": "Unknown", "match": "No close matches found"}

    except Exception as e:
        result = {"error": str(e)}

    finally:
        os.remove(temp_video_path)  # Clean up the temporary file

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
