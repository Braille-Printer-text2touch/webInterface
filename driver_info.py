############################
## This script is used to abstract getting the driver information from the system
## 
## Author: Kenneth Howes, 2025, kenneth.howes53@gmail.com
############################
import posix_ipc
from typing import Callable
from beartype import beartype
import threading

class BrailleDriverInfo:
    QUEUE_NAME = "/text2touch-driver-info"

    def __init__(self):
        if not posix_ipc.MESSAGE_QUEUES_SUPPORTED:
            raise SystemError("Messages queues are not supported on this system")

        self.mq = posix_ipc.MessageQueue(self.QUEUE_NAME)

        # default handle callback is just nothing
        self.__handle_message_cb: Callable[[str, int], None] = lambda msg, priority: None

    def message_listener(self) -> None:
        try:
            while True:
                self.__handle_message(self.mq.receive())
        except KeyboardInterrupt:
            print("\nExiting...")
            try:
                # remove process from message queue
                posix_ipc.unlink_message_queue(self.QUEUE_NAME)
            except posix_ipc.ExistentialError:
                pass

    def run(self) -> None:
        listener_thread = threading.Thread(target=self.message_listener, daemon=True)
        listener_thread.start() 

    def __handle_message(self, raw_message: tuple[str, int]) -> None:
        message, priority = raw_message
        self.__handle_message_cb(message.decode(), priority)

    @property
    def handle_message(self) -> Callable[[str, int], None]:
        '''Exists to expose a clean setter for the callback. This getter probably should not be used.'''
        return self.__handle_message_cb
        
    @handle_message.setter
    @beartype # ensure proper callback type is assigned
    def handle_message(self, callback: Callable[[str, int], None]) -> None:
        self.__handle_message_cb = callback

if __name__ == "__main__":

    def test_handle(msg: str, prio: int) -> None:
        print(f"Received: {msg} @ priority {prio}")

    driver_info = BrailleDriverInfo()
    driver_info.handle_message = test_handle
    driver_info.run()
