import os
import time

import torch

from open_voice.common.constant import OPENVOICE_DIR
from open_voice.openvoice import se_extractor
from open_voice.openvoice.api import BaseSpeakerTTS, ToneColorConverter
from server.common.constant import SERVER_DIR


class OpenVoiceUtil:
    @staticmethod
    def text2speech(text, language="English", emotion="excited", speed=1.0):
        #emotion:friendly, cheerful, excited, sad, angry, terrified, shouting, whispering
        now = int(round(time.time() * 1000))
        ckpt_base = OPENVOICE_DIR + '/checkpoints/base_speakers/EN'
        ckpt_converter = OPENVOICE_DIR + '/checkpoints/converter'
        device = "cuda:0" if torch.cuda.is_available() else "cpu"
        output_src_dir = SERVER_DIR + '/outputs/open_voice/src'
        output_tone_clone_dir = SERVER_DIR + '/outputs/open_voice/tone_clone'

        base_speaker_tts = BaseSpeakerTTS(f'{ckpt_base}/config.json', device=device)
        base_speaker_tts.load_ckpt(f'{ckpt_base}/checkpoint.pth')

        tone_color_converter = ToneColorConverter(f'{ckpt_converter}/config.json', device=device)
        tone_color_converter.load_ckpt(f'{ckpt_converter}/checkpoint.pth')

        os.makedirs(output_src_dir, exist_ok=True)
        os.makedirs(output_tone_clone_dir, exist_ok=True)

        reference_speaker = SERVER_DIR + '/resources/open_voice/example_reference.mp3'  # This is the voice you want to clone
        target_se, audio_name = se_extractor.get_se(reference_speaker, tone_color_converter, target_dir='processed',
                                                    vad=True)


        source_se = torch.load(f'{ckpt_base}/en_style_se.pth').to(device)
        save_path = output_tone_clone_dir + "/" + str(now) + ".wav"

        # Run the base speaker tts
        src_path =  output_src_dir + "/" + str(now) + ".wav"
        base_speaker_tts.tts(text, src_path, speaker=emotion, language=language, speed=speed)

        # Run the tone color converter
        encode_message = "@MyShell"
        tone_color_converter.convert(
            audio_src_path=src_path,
            src_se=source_se,
            tgt_se=target_se,
            output_path=save_path,
            message=encode_message)
        return save_path

if __name__ == "__main__":
    OpenVoiceUtil.text2speech("hello boy", "English", "cheerful",)