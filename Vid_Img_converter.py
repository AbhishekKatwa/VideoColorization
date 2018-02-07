import cv2
import os
import time

def video_to_frames(input_loc, output_loc):
    """Function to extract frames from input video file
    and save them as separate frames in an output directory.
    Args:
        input_loc: Input video file.
        output_loc: Output directory to save the frames.
    Returns:
        None
    """
    try:
        os.mkdir(output_loc)
    except OSError:
        pass
    # Log the time
    time_start = time.time()
    # Start capturing the feed
    cap = cv2.VideoCapture(input_loc)
    # Find the number of frames
    video_length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) - 1
    print ("Number of frames: ", video_length)
    count = 0
    print ("Converting video..\n")
    # Start converting the video
    while cap.isOpened():
        # Extract the frame
        ret, frame = cap.read()
        # Write the results back to output location.
        cv2.imwrite(output_loc + "/%#05d.jpg" % (count+1), frame)
        count = count + 1
        # If there are no more frames left
        if (count > (video_length-1)):
            # Log the time again
            time_end = time.time()
            # Release the feed
            cap.release()
            # Print stats
            print ("Done extracting frames.\n%d frames extracted" % count)
            print ("It took %d seconds for conversion." % (time_end-time_start))
            break


def frames_to_video(inputpath,outputpath,fps):
    """Function to convert frames from input path
    and save them as a video in an output directory at defined fps.
    Args:
        inputpath: Input frames folder.
        outputpath: Output directory to save the video.
        fps:frames per second
    Returns:
        None
    """
    image_array = []
    files = [f for f in os.listdir(inputpath) if os.path.isfile(inputpath+"/"+f)]
    files.sort(key = lambda x: int(x[0:-4]))
    for i in range(len(files)):
       img = cv2.imread(inputpath +"/"+ files[i])
       size =  (img.shape[1],img.shape[0])
       img = cv2.resize(img,size)
       image_array.append(img)
    fourcc = cv2.VideoWriter_fourcc('D','I','V','X')
    out = cv2.VideoWriter(outputpath,fourcc, fps, size)
    for i in range(len(image_array)):
       out.write(image_array[i])
    out.release()
    
def color_to_gray(colorpath,graypath):
    """Function to convert color images to grayscale
    Args:
        colorpath: folder of color images
        graypath: folder of gray images
    Returns:
        None
    """
    files = [f for f in os.listdir(colorpath) if os.path.isfile(colorpath+"/"+f)]
    files.sort(key = lambda x: int(x[0:-4]))
    print(files)
    try:
        os.mkdir(graypath)
    except OSError:
        pass
    for i in range(len(files)):
       img = cv2.imread(colorpath +"/"+ files[i])
       gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
       cv2.imwrite(graypath+"/"+files[i],gray_image)



inputpath = "bw"
outpath =  "video_bw.mp4"
fps = 24
frames_to_video(inputpath,outpath,fps)

'''
input_loc="video.mp4"
output_loc="out"
video_to_frames(input_loc,output_loc)
'''

'''
colorpath="./out"
graypath="./bw"
color_to_gray(colorpath,graypath)
'''
