class Ref:
    myTello = None
    recorder = None

    def __del__(self):
        Ref.myTello.streamoff()
        Ref.recorder.join()