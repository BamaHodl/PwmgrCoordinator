#!/usr/bin/python3
import cv2 
import re
import argparse

class BaseQrDecoder:
    def __init__(self):
        self.total_segments = None
        self.collected_segments = 0
        self.complete = False

    @property
    def is_complete(self) -> bool:
        return self.complete

    def add(self, segment, qr_type):
        raise Exception("Not implemented in child class")
    
    def get_qr_data(self) -> dict:
        raise Exception("get_qr_data must be implemented in decoder child class")


class BaseAnimatedQrDecoder(BaseQrDecoder):
    def __init__(self):
        super().__init__()
        self.segments = []

    def current_segment_num(self, segment) -> int:
        raise Exception("Not implemented in child class")

    def total_segment_nums(self, segment) -> int:
        raise Exception("Not implemented in child class")

    def parse_segment(self, segment) -> str:
        raise Exception("Not implemented in child class")
    
    def add(self, segment, qr_type=None):
        if self.total_segments == None:
            self.total_segments = self.total_segment_nums(segment)
            self.segments = [None] * self.total_segments
        elif self.total_segments != self.total_segment_nums(segment):
            raise Exception('Segment total changed unexpectedly')

        if self.segments[self.current_segment_num(segment) - 1] == None:
            self.segments[self.current_segment_num(segment) - 1] = self.parse_segment(segment)
            self.collected_segments += 1
            if self.total_segments == self.collected_segments:
                self.complete = True
                return True
        return False



class SpecterAnimatedQrDecoder(BaseAnimatedQrDecoder):
    """
    """
    def get_data(self) -> str:
        if self.complete: 
            data = "".join(self.segments)
            return data
        return None


    def current_segment_num(self, segment) -> int:
        if re.search(r'^pwm(\d+)of(\d+) ', segment, re.IGNORECASE) != None:
            return int(re.search(r'^pwm(\d+)of(\d+) ', segment, re.IGNORECASE).group(1))


    def total_segment_nums(self, segment) -> int:
        if re.search(r'^pwm(\d+)of(\d+) ', segment, re.IGNORECASE) != None:
            return int(re.search(r'^pwm(\d+)of(\d+) ', segment, re.IGNORECASE).group(2))


    def parse_segment(self, segment) -> str:
        return segment.split(" ")[-1].strip()


parser = argparse.ArgumentParser("pwmgr_receiver")
parser.add_argument('-f', '--file', required=True, type=str)
args = parser.parse_args()

out_file = open(args.file, "w")

print("Press q in the img window or ctrl-c in the terminal to end...")

cap = cv2.VideoCapture(0)
# initialize the cv2 QRCode detector
detector = cv2.QRCodeDetector()


decoder = SpecterAnimatedQrDecoder()

font                   = cv2.FONT_HERSHEY_SIMPLEX
topLeftCornerOfText = (10,20)
fontScale              = 1
fontColor              = (247,147,26)
thickness              = 2
lineType               = 2

while True:
   _, img = cap.read()
   text = "Awaiting data" if not decoder.total_segments else str(decoder.collected_segments) + " of " + str(decoder.total_segments)
   cv2.putText(img,text,
       topLeftCornerOfText, 
       font, 
       fontScale,
       fontColor,
       thickness,
       lineType)


   cv2.imshow("QRCODEscanner", img)     
   if cv2.waitKey(1) == ord("q"): 
        break
   data, bbox, _ = detector.detectAndDecode(img)
   # check if there is a QRCode in the image
   if data:
       decoder.add(data)
       if decoder.is_complete:
           break

#cv2.imshow("QRCODEscanner", img)     
#if cv2.waitKey(1) == ord("q"): 
    #break
print("Got data:")
print(decoder.get_data())

out_file.write(decoder.get_data())
print("Wrote received data to " + args.file)
print("\nDone\n")
