class tracer(object):
    def __init__(self, func):
        self.calls = 0
        self.func = func
    def __call__(self, *args):
        self.calls += 1
        print ('call %s to %s ' % (self.calls, self.func.__name__))
        
        arg_sum = ''
        for arg in args:
            arg_sum = str(arg_sum) + str(arg)
            print ('sum of arguments as string %s  ' % (arg_sum))
        self.func(*args)

@tracer
def spam(a, b, c):
        print( a, b, c )

if __name__ == '__main__':
    spam(1, 2, 3)
    spam('a', 'b', 'c')
