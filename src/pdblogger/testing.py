import logging
import pdb

logger = logging.getLogger('pdblogger.testing')


def logging_set_trace(*args, **kw):
    logger.debug('pdb.set_trace() called: %r, %r' % (args, kw))


def logging_interaction(*args, **kw):
    logger.debug('pdb.interaction() called: %r, %r' % (args, kw))
    

def setUp(test):
    test.globs.update(
        orig_set_trace=pdb.Pdb.set_trace,
        orig_interaction=pdb.Pdb.interaction,
        logger=logger)
    pdb.Pdb.set_trace = logging_set_trace
    pdb.Pdb.interaction = logging_interaction
    

def tearDown(test):
    pdb.Pdb.set_trace = test.globs['orig_set_trace']
    pdb.Pdb.interaction = test.globs['orig_interaction']
