import cv2
import numpy as np
import pyrealsense2 as rs

def get_frame():
    # Create a pipeline
    pipeline = rs.pipeline()
    print('pipeline started')
    # Create a config and configure the pipeline to stream
    # different resolutions of color and depth streams
    config = rs.config()

    print("Setting up config of running in live data")
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

    # Getting the depth sensor's depth scale (see rs-align example for explanation)
    profile = pipeline.start(config)
    depth_sensor = profile.get_device().first_depth_sensor()
    depth_scale = depth_sensor.get_depth_scale()
    print("Depth Scale is: " , depth_scale)

    # We will be removing the background of objects more than
    #  clipping_distance_in_meters meters away
    #clipping_distance_in_meters = 15 #10 meter
    #clipping_distance = clipping_distance_in_meters / depth_scale

    # Create an align object
    # rs.align allows us to perform alignment of depth frames to others frames
    # The "align_to" is the stream type to which we plan to align depth frames.
    align_to = rs.stream.color
    align = rs.align(align_to)

    while True:

        # Declare pointcloud object, for calculating pointclouds and texture mappings
        pc = rs.pointcloud()

        # We want the points object to be persistent so we can display the last cloud when a frame drops
        points = rs.points()

        # Get frameset of color and depth
        frames = pipeline.wait_for_frames()
        # frames.get_depth_frame() is a 640x360 depth image
        
        # Align the depth frame to color frame
        aligned_frames = align.process(frames)
        
        # Get aligned frames
        aligned_depth_frame = aligned_frames.get_depth_frame() # aligned_depth_frame is a 640x480 depth image
        color_frame = aligned_frames.get_color_frame()
        
        # Tell pointcloud object to map to this color frame
        pc.map_to(color_frame)

        # Generate the pointcloud and texture mappings
        points = pc.calculate(aligned_depth_frame)

        points_array = np.asanyarray(points.get_vertices())

        # Validate that both frames are valid
        if not aligned_depth_frame or not color_frame:
            continue
        
        depth_image = np.asanyarray(aligned_depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())
        
        # Remove background - Set pixels further than clipping_distance to grey
        grey_color = 153
        depth_image_3d = np.dstack((depth_image,depth_image,depth_image)) #depth image is 1 channel, color is 3 channels
        #bg_removed = np.where((depth_image_3d > clipping_distance) | (depth_image_3d <= 0), grey_color, color_image)
        
        # Render images
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
        #images = np.hstack((bg_removed, depth_colormap))

        yield color_image, depth_image, points_array