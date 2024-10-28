from linuxpy.video.device import Device, VideoCapture

dev_source = Device.from_id(0)
with dev_source:
    source = VideoCapture(dev_source)
    source.set_format(640, 480, "MJPG")
    with source:
        for frame in source:
            print(frame.data)

