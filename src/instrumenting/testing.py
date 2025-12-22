import sys
import traceback
import logging
import tempfile
import bdb
import pdb
import threading
from doctest import _SpoofOut

import instrumenting

root = logging.getLogger()
logger = logging.getLogger('instrumenting.testing')


def main(*args, **kw):
    logger.debug('debug message')
    logger.info('info message')
    logger.warning('warning message')
    logger.error('error message')
    try:
        raise ValueError('Forced program exception')
    except BaseException as e:
        logger.exception('exception message: %s' % e)
    logger.critical('critical message')


def logging_set_trace(*args, **kw):
    print('TESTING pdb.set_trace() called: %r, %r' % (args, kw))


def logging_interaction(*args, **kw):
    print('TESTING pdb.interaction() called: %r, %r' % (args, kw))


def quitting_set_trace(*args, **kw):
    logging_set_trace(*args, **kw)
    raise bdb.BdbQuit()


def quitting_interaction(*args, **kw):
    logging_interaction(*args, **kw)
    raise bdb.BdbQuit()


def interrupting_set_trace(*args, **kw):
    logging_set_trace(*args, **kw)
    raise KeyboardInterrupt()


def interrupting_interaction(*args, **kw):
    logging_interaction(*args, **kw)
    raise KeyboardInterrupt()


def excepting_set_trace(*args, **kw):
    logging_set_trace(*args, **kw)
    raise ValueError('instrumenting.testing set_trace forced exception')


def excepting_interaction(*args, **kw):
    logging_interaction(*args, **kw)
    raise ValueError('instrumenting.testing interaction forced exception')


isatty_value = True


def isatty(self):
    return isatty_value


def setUpPdb(test):
    test.globs.update(
        stdin=sys.stdin, stdout=sys.stdout,
        orig_isatty=_SpoofOut.isatty,
        orig_set_trace=pdb.Pdb.set_trace,
        orig_interaction=pdb.Pdb.interaction,
        logger=logger)
    _SpoofOut.isatty = isatty
    pdb.Pdb.set_trace = logging_set_trace
    pdb.Pdb.interaction = logging_interaction


def tearDownPdb(test):
    for handler in root.handlers:
        if isinstance(handler, instrumenting.PdbHandler):
            root.removeHandler(handler)
    pdb.Pdb.set_trace = test.globs['orig_set_trace']
    pdb.Pdb.interaction = test.globs['orig_interaction']
    _SpoofOut.isatty = test.globs['orig_isatty']
    test.globs['testing_handler'].uninstall()
    global isatty_value
    isatty_value = True


class StackCondition(object):

    def __init__(self, print_stack=False):
        self.print_stack = print_stack
        self.condition = threading.Condition()

    def debug(self):
        if not self.print_stack:
            return
        frame = sys._getframe(2)
        traceback.print_stack(frame, limit=1)

    def acquire(self):
        self.debug()
        return self.condition.acquire()

    def release(self):
        self.debug()
        return self.condition.release()

    def wait(self):
        self.debug()
        return self.condition.wait()

    def notify(self):
        self.debug()
        return self.condition.notify()

    def handoff(self):
        self.debug()
        self.condition.notify()
        self.condition.wait()


thread_sync = StackCondition()


def threaded_inner_main(*args, **kw):
    thread_sync.acquire()
    logger.debug('debug message')
    logger.info('info message')
    thread_sync.handoff()
    logger.warning('warning message')
    thread_sync.handoff()
    logger.error('error message')
    thread_sync.handoff()
    thread_sync.release()
    try:
        raise ValueError('Forced program exception')
    except BaseException as e:
        logger.exception('exception message: %s' % e)
    logger.critical('critical message')


def threaded_inner_other():
    thread_sync.acquire()
    logger.info('other thread info message')
    thread_sync.handoff()
    logger.warning('other thread warning message')
    thread_sync.handoff()
    logger.error('other thread error message')
    thread_sync.notify()
    thread_sync.release()


def threaded_main():
    profiled = threading.Thread(target=threaded_inner_main)
    other = threading.Thread(target=threaded_inner_other)
    thread_sync.acquire()
    profiled.start()
    thread_sync.wait()
    other.start()
    thread_sync.release()
    profiled.join(), other.join()


def setUpProfiling(test):
    test.globs.update(logger=logger, tmp=tempfile.mkdtemp())


def tearDownProfiling(test):
    for handler in root.handlers:
        if isinstance(handler, instrumenting.ProfilingHandler):
            root.removeHandler(handler)
