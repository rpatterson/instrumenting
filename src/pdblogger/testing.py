import logging
import pdb

from zope.testing import loggingsupport

logger = logging.getLogger('pdblogger.testing')


def main(*args, **kw):
    logger.debug('debug message')
    logger.info('info message')
    logger.warning('warning message')
    logger.error('error message')
    try:
        raise ValueError('Forced program exception')
    except BaseException, e:
        logger.exception('exception message: %s' % e)
    logger.critical('critical message')


def logging_set_trace(*args, **kw):
    logger.debug('pdb.set_trace() called: %r, %r' % (args, kw))


def logging_interaction(*args, **kw):
    logger.debug('pdb.interaction() called: %r, %r' % (args, kw))
    

def setUp(test):
    testing_handler = loggingsupport.InstalledHandler('pdblogger.testing')
    test.globs.update(
        orig_set_trace=pdb.Pdb.set_trace,
        orig_interaction=pdb.Pdb.interaction,
        logger=logger,
        testing_handler=testing_handler)
    pdb.Pdb.set_trace = logging_set_trace
    pdb.Pdb.interaction = logging_interaction
    

def tearDown(test):
    pdb.Pdb.set_trace = test.globs['orig_set_trace']
    pdb.Pdb.interaction = test.globs['orig_interaction']
