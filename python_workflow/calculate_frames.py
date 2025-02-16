def calculate_frames(data:dict, framerate:int):
    """Calculate the frames for the animation

    Args:
        data (dict): keyframe data in dict format as returned by convert_tracklog
        framerate (int): frame rate of desired animation

    Returns:
        dict:  keyframe data in dict format with interpolated frames
    """
    # Calculate which animation frames are keyframes   
    keyframes = []
    for t in data['Timestamp']:
        keyframes.append(round(t * framerate))
    data['Keyframe'] = keyframes

    frames_frame = []    
    frames_altitude = []
    frames_course = []
    frames_speed = []
    frames_bank = []
    frames_pitch = []
    frames_valid = []
    
    # Process altitude, course, and speed
    keyframe_start = data['Keyframe'][0]
    keyframe_last = keyframe_start
    altitude_last = data['Altitude'][0]
    heading_last = data['Course'][0]
    speed_last = data['Speed'][0]
    i = 0
    for altitude, heading, speed, keyframe in zip(data['Altitude'], data['Course'], data['Speed'], data['Keyframe']):
        keyframe_change = keyframe - keyframe_last
        if keyframe_change == 0:
            continue
        altitude_change = altitude - altitude_last
        # how much the heading needs to change between tracklog entries
        # "rotational interpolation" from https://stackoverflow.com/questions/2708476/rotation-interpolation
        heading_change = (((heading - heading_last) + 180) % 360) - 180
        speed_change = speed - speed_last
        # calculate between keyframes
        altitude_change_interframe = altitude_change / keyframe_change
        heading_change_interframe = heading_change / keyframe_change
        speed_change_interframe = speed_change / keyframe_change
        # linearly interpolate the heading and ground speed changes for each interframe
        for frame in range(keyframe_change):
            i += 1
            frames_altitude.append(altitude_last + altitude_change_interframe * frame)
            frames_course.append(heading_last + heading_change_interframe * frame)
            frames_speed.append(speed_last + speed_change_interframe * frame)    
            frames_frame.append(i)
        keyframe_last = keyframe
        altitude_last = altitude
        heading_last = heading
        speed_last = speed

    # Process bank and pitch
    bank_last = data['Bank'][0]
    pitch_last = data['Pitch'][0]
    keyframe_start = data['Keyframe'][0]
    keyframe_last = keyframe_start
    i = 0
    for bank, pitch, keyframe, valid in zip(data['Bank'], data['Pitch'], data['Keyframe'], data['Valid']):
        keyframe_change = keyframe - keyframe_last
        if keyframe_change == 0:
            continue
        bank_change = bank - bank_last
        pitch_change = pitch - pitch_last
        # calculate between keyframes
        bank_change_interframe = bank_change / keyframe_change
        pitch_change_interframe = pitch_change / keyframe_change
        # linearly interpolate the pitch and bank for each interframe
        for frame in range(keyframe_change):
            i += 1
            frames_bank.append(bank_last + bank_change_interframe * frame)
            frames_pitch.append(pitch_last + pitch_change_interframe * frame)
            frames_valid.append(valid)
        keyframe_last = keyframe
        bank_last = bank
        pitch_last = pitch

    return {'Frame':frames_frame, 'Altitude':frames_altitude, 'Course':frames_course, 'Speed':frames_speed, 'Bank':frames_bank, 'Pitch':frames_pitch, 'Valid':frames_valid}