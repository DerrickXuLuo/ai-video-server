import contextlib
import wave

from torch.utils.tensorboard.summary import video

from server.util.openvoice_util import OpenVoiceUtil
from server.util.video_util import image_to_video, crop_video, combine_video

if __name__ == "__main__":
    text = ""
    voice_file_path = OpenVoiceUtil.text2speech(text)
    #获取音频时长
    duration_seconds = 0
    with contextlib.closing(wave.open(voice_file_path, 'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration_seconds = frames / float(rate)
    product_images = [] # file path list
    product_videos = []
    for product_image in product_images:
        product_video_path = ""
        #todo 图像转视频
        # image_to_video(product_image, )
        product_videos.append(product_video_path)
    #
    nums = duration_seconds // 5
    if nums < len(product_videos):
        product_videos = product_videos[:nums]
    else:
        nums = len(product_videos)
    interval = duration_seconds // nums
    video_list = []
    for i in range(nums):
        if i == nums - 1:
            #todo 结尾视频放进去
            #crop_video(, i * interval, duration_seconds-1,)
            video_list.append(product_videos[i])
            continue
        else:
            #todo 切割interval 间隔的视频 然后放进video list
            #crop_video(, i*interval, (i+1)*interval-1,)
            video_list.append(product_videos[i])
    # combine_video(video_list, )

