import os
# glob allows uyou to navigate through folders and identify the files
import glob
import numpy as np
from skimage.filters import gaussian # most of filters will convert numbers into floating point numbers
from skimage import img_as_ubyte # converting floating number imgaes into 8 bit images 
import cv2 # to read images
images_list=[]
SIZE=512
def create_directory(path):
    try:
        # use try block to make sure if the directory is already exists or not 
        if not os.path.exists(path):
            os.makedirs(path)
    except OSError:
        print(f"ERROR: creating directory with name {path}")

def apply_roi():
    # path from where the images will be taken to apply roi
    images_path = "frames/videos/1/*.*"
    for file in glob.glob(images_path):
        print(file)
        img=cv2.imread(file,0) # reading image into grayscale
        img=cv2.resize(img,(SIZE,SIZE))
        images_list.append(img)
        
        
images_list = np.array(images_list)


def save_frame(video_path, save_dir, gap=10):
    # inside the framefolder we are creating the folder with the name videos
    name = video_path.split("/")[-1].split(".")[0]
    # creating the folder where we save the frame
    save_path = os.path.join(save_dir, name)
    create_directory(save_path)
    apply_roi()


   # used cv2 librarcy to capture video
    cap = cv2.VideoCapture(video_path)
    idx = 0  # used idx variable to sequnce the frames

    while True:
        ret, frame = cap.read() # 

        if ret == False: #  it means we are at the end of the video and we don't have more frames, so we release the video we captured 
            cap.release()
            break

        if idx == 0:
            cv2.imwrite(f"{save_path}/{idx}.png", frame)
        else:
            if idx % gap == 0:
                cv2.imwrite(f"{save_path}/{idx}.png", frame)

        idx += 1

if __name__ == "__main__":
    # path to the folder from where we are taking all the videos
    video_paths = "videos/*"
    # directory to save the frames 
    save_dir = "frames"

    for path in glob.glob(video_paths):
        # this function takes two arguments video path and save directory
        # gap is used to extract the frames from video after some gap 
        save_frame(path, save_dir, gap=10)
