import sys
import signal

def exit_signal_handler(signal, frame):
    print 'exit_signal_handler() '

if __name__ == '__main__':
    print 'Enter .. '
    signal.signal(signal.SIGINT, exit_signal_handler)
    print 'set signal '
    signal.pause()
    print 'paused '
    sys.exit(1)