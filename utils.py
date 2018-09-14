from threading import Thread


def create_thread_helper(handler):
    communicator = Thread(target=handler, args=())
    communicator.start()
    communicator.join()
