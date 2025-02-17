'''Render a video from a folder of images'''
import os
import cv2

def render_video(image_folder, fps=30):
    '''Render a video from a folder of images'''
    images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
    images.sort()  # Ensure the images are in the correct order

    if not images:
        print("No images found in the folder.")
        return

    # Read the first image to get the dimensions
    first_image_path = os.path.join(image_folder, images[0])
    frame = cv2.imread(first_image_path)
    height, width, layers = frame.shape

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    output_video_file = os.path.join(image_folder, 'output.mp4')
    video = cv2.VideoWriter(os.path.join(image_folder, 'output.mp4'), fourcc, fps, (width, height))

    for image in images:
        image_path = os.path.join(image_folder, image)
        frame = cv2.imread(image_path)
        video.write(frame)

    video.release()
    print(f"Video saved as {output_video_file}")
