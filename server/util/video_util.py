import ffmpeg


def crop_video(input_video, start_time, end_time, output_video):
    ffmpeg.input(input_video).filter('trim', start=start_time, end=end_time).output(output_video).run(
        overwrite_output=True)


def add_audio_to_video(input_audio, input_video, output_video):
    ffmpeg.input(input_video).audio.addinput(ffmpeg.input(input_audio)).output(output_video).run(
        overwrite_output=True)


def combine_video(video_list, output_video):
    video_input_list = []
    for video in video_list:
        video_input = ffmpeg.input(video).setpts('PTS-STARTPTS')
        video_input_list.append(video_input)

    video_concat = ffmpeg.concat(*video_input_list)

    ffmpeg.output(video_concat, output_video).run(overwrite_output=True)


def image_to_video(img, duration, fps, output_video):
    img_input = ffmpeg.input(img, loop=1, t=duration, framerate=fps)
    ffmpeg.output(img_input, output_video, vcodec='libx264', vf=f'scale=1920:1080').run(
        overwrite_output=True)
