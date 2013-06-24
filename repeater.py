
import logging
import time

log = logging.getLogger('pg.%s' % __name__)

class DoNotRepeatError(Exception):
    """Raise DoNotRepeatError in a function to force repeat() to exit."""
    
    def __init__(self, error):
        Exception.__init__(self, error.message)
        self.error = error

class PauseRepeatError(Exception):
    """Raise PauseRepeatError in a function to delay repeating for a set number
    of seconds."""
    
    def __init__(self, error, delay):
        Exception.__init__(self, error.message)
        self.error = error
        self.delay = delay

def repeat(func, n=5, standoff=1.5):
    """Execute a function repeatedly until success (no exceptions raised).

    Args:
        func (function): The function to repeat

    Kwargs:
        n (int): The number of times to repeate `func` before raising an error
        standoff (float): Multiplier increment to wait between retrying `func`

    >>>import repeater.repeat

    >>>@repeater.repeat
    >>>def fail():
    >>>    print 'A'
    >>>    raise Exception()
    >>>    print 'B'

    >>>@repeater.repeat
    >>>def pass():
    >>>    print 'B'

    >>>@repeater.repeat
    >>>def failpass():
    >>>    print 'C'
    >>>    raise repeater.DoNotRepeatError(Exception())
    >>>    print 'D'

    >>>fail() # prints 'A' 10 times, failing each time
    A
    A
    A
    A
    A
    A
    A
    A
    A
    A

    >>>pass() # prints 'B' once, succeeding on first try
    B

    >>>failpass() # prints 'C' once, then fails
    C

    """

    def wrapped(*args, **kwargs):
        retries = 0
        while True:
            try:
                return func(*args, **kwargs)
            except DoNotRepeatError as e:
                # raise the exception that caused funciton failure
                raise e.error
            except PauseRepeatError as e:
                log.exception(e)
                time.sleep(e.delay)
                retries += 1
            except Exception as e:
                log.exception(e)
                if retries < n:
                    retries += 1
                    time.sleep(retries * standoff)
                else:
                    raise
    return wrapped

