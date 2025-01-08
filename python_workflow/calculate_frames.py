def calculate_frames(data, framerate):
    outputList = []
    # Calculate which animation frames are keyframes   
    keyframes = []
    for t in data['Timestamp']:
        keyframes.append(round(t * framerate))
    data['Keyframe'] = keyframes
        

    
    # timestamp_start = data['Timestamp'][0]
    # timestamp_last = timestamp_start
    altitude_last = data['Altitude'][0]
    heading_last = data['Course'][0]
    speed_last = data['Speed'][0]
    bank_last = data['Bank'][0]
    pitch_last = data['Pitch'][0]
    keyframe_start = data['Keyframe'][0]
    keyframe_last = keyframe_start

    i = 0
    for altitude, heading, speed, bank, pitch, keyframe, valid in zip(data['Altitude'], data['Course'], data['Speed'], data['Bank'], data['Pitch'], data['Keyframe'], data['Valid']):
        keyframe_change = keyframe - keyframe_last
        if keyframe_change == 0:
            continue
        altitude_change = altitude - altitude_last
        # how much the heading needs to change between tracklog entries
        # "rotational interpolation" from https://stackoverflow.com/questions/2708476/rotation-interpolation
        heading_change = (((heading - heading_last) + 180) % 360) - 180
        speed_change = speed - speed_last
        bank_change = bank - bank_last
        pitch_change = pitch - pitch_last     
        
        # calculate between keyframes
        altitude_change_interframe = altitude_change / keyframe_change
        heading_change_interframe = heading_change / keyframe_change
        speed_change_interframe = speed_change / keyframe_change
        bank_change_interframe = bank_change / keyframe_change
        pitch_change_interframe = pitch_change / keyframe_change

        # linearly interpolate the heading and ground speed changes for each interframe
        for frame in range(int(round(keyframe_change))):
            i += 1
            altitude = altitude_last + altitude_change_interframe * frame
            rotation = heading_last + heading_change_interframe * frame
            speed = speed_last + speed_change_interframe * frame
            bank = bank_last + bank_change_interframe * frame
            pitch = pitch_last + pitch_change_interframe * frame
            outputList.append([i, valid, altitude, rotation, speed, bank, pitch])
            if not logOnly:
                saveImage(rotation, speed, altitude, bank, pitch, i)
        
        keyframe_last = keyframe
        altitude_last = altitude
        heading_last = heading
        speed_last = speed
        bank_last = bank
        pitch_last = pitch