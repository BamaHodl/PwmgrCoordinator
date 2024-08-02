#!/usr/bin/python3
from dataclasses import dataclass
import qrcode
import cv2 
import numpy 
from PIL import Image
from pathlib import Path
import time
import argparse
import string

def convert_from_image_to_cv2(img: Image) -> numpy.ndarray:
    open_cv_image = numpy.array(img, dtype=numpy.uint8)

    #convert grayscale
    open_cv_image *= 255
    return open_cv_image

@dataclass
class BaseQrEncoder:
    qr_density: str = 'high'


    def part_to_image(self, part, width, height, border: int = 3, background_color: str = "ffffff"):
        img = qrcode.make(part).get_image()
        opencvImage = convert_from_image_to_cv2(img)
        return opencvImage


    def next_part_image(self, width=240, height=240, border=3, background_color="bdbdbd"):
        part = self.next_part()
        return self.part_to_image(part, width, height, border, background_color=background_color)




@dataclass
class PubkeyQrEncoder(BaseQrEncoder):
    qr_data : bytes = None

    def seq_len(self):
        return 1

    def next_part(self) -> bytes:
        return self.qr_data

@dataclass
class BaseSimpleAnimatedQREncoder(BaseQrEncoder):
    def __post_init__(self):
        self.parts = []
        self.part_num_sent = 0
        self.sent_complete = False
        self._create_parts()


    @property
    def is_complete(self):
        return self.sent_complete


    def seq_len(self):
        return len(self.parts)


    def next_part(self) -> str:
        # if part num sent is gt number of parts, start at 0
        if self.part_num_sent > (len(self.parts) - 1):
            self.part_num_sent = 0

        part = self.parts[self.part_num_sent]

        # increment to next part
        self.part_num_sent += 1

        return part


    def cur_part(self) -> str:
        if self.part_num_sent == 0:
            # Rewind all the way back to the end
            self.part_num_sent = len(self.parts) - 1
        else:
            self.part_num_sent -= 1
        return self.next_part()


    def restart(self) -> str:
        self.part_num_sent = 0



@dataclass
class PwmgrQrEncoder(BaseSimpleAnimatedQREncoder):
    qr_data : str = None

    @property
    def qr_max_fragment_size(self):
        density_mapping = {
            'low': 40,
            'medium': 65,
            'high': 90,
        }
        return density_mapping.get(self.qr_density, 65)


    def _create_parts(self):
        start = 0
        stop = self.qr_max_fragment_size
        qr_cnt = ((len(self.qr_data)-1) // self.qr_max_fragment_size) + 1

        if qr_cnt == 1:
            self.parts.append(self.qr_data[start:stop])

        cnt = 0
        while cnt < qr_cnt and qr_cnt != 1:
            part = "pwm" + str(cnt+1) + "of" + str(qr_cnt) + " " + self.qr_data[start:stop]
            self.parts.append(part)

            start = start + self.qr_max_fragment_size
            stop = stop + self.qr_max_fragment_size
            if stop > len(self.qr_data):
                stop = len(self.qr_data)
            cnt += 1

parser = argparse.ArgumentParser("pwmgr_sender")
parser.add_argument('-f', '--file', required=True, type=str)
args = parser.parse_args()

input_string = Path(args.file).read_text().strip()
if 66==len(input_string) and set(input_string).issubset(string.hexdigits):
    # this is a pubkey
    encoder = PubkeyQrEncoder(qr_data=bytes.fromhex(input_string))
    print("Interpreting input as pubkey and sending 33 bytes of binary data")
else:
    encoder = PwmgrQrEncoder(qr_data=input_string)

print("Press q in the img window or ctrl-c in the terminal to end...")
img = encoder.next_part_image()
cv2.imshow("QRCODEncoder", img)     
while True:
    if cv2.waitKey(1) == ord("q") :
        break
    if encoder.seq_len() > 1:
        time.sleep(0.3)
        img = encoder.next_part_image()
        cv2.imshow("QRCODEncoder", img)     

