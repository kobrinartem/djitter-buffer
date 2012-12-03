__author__ = 'artem'

import numpy
import pylab
import random

def xfrange(start, stop, step):
    x = []
    while start < stop:
        x.append(start)
        start += step
    return x

def kalman():
    #init

    x = 0.025 # truth value (typo in example at top of p. 13 calls this z)
    z = []
    Q = 1e-3 # process variance
    for i in range(50, 0, -1):
        z.append(0.025+random.normalvariate(0, 0.0005))
    x2= xfrange(0, 200, 1)
    for i in range(0, len(x2), 1):
        z.append(0.00005*x2[i] + 0.025+random.normalvariate(0, 0.0005))
    for i in range(len(x2)-1, 0, -1):
        z.append(0.00005*x2[i] + 0.025+random.normalvariate(0, 0.0005))
    for i in range(50, 0, -1):
        z.append(0.025+random.normalvariate(0, 0.0005))


    n_iter = len(z)
    sz = (n_iter,) # size of array

    # allocate space for arrays
    xhat=numpy.zeros(sz)      # a posteri estimate of x
    P=numpy.zeros(sz)         # a posteri error estimate
    xhatminus=numpy.zeros(sz) # a priori estimate of x
    Pminus=numpy.zeros(sz)    # a priori error estimate
    K=numpy.zeros(sz)         # gain or blending factor
    ystar=numpy.zeros(sz)

    R = 0.1**3 # estimate of measurement variance, change to see effect

    # intial guesses
    xhat[0] = 1.0
    P[0] = 1.0
    ystar[0] = x
    for k in range(1,n_iter):
        # time update
        xhatminus[k] = xhat[k-1]
        Pminus[k] = P[k-1]+Q

        # measurement update
        K[k] = Pminus[k]/( Pminus[k]+R )
        xhat[k] = xhatminus[k]-K[k]*(xhatminus[k]*z[k]-x)/x

        ystar[k] = xhat[k]*z[k]
        print xhatminus[k]*z[k]-x, K[k], xhat[k], z[k], ystar[k]
        P[k] = (1-K[k])*Pminus[k]

    pylab.figure()
    pylab.plot(z,'r-+',label='x')
    #pylab.plot(xhat,'b-',label='a posteri estimate')
    pylab.plot(ystar,'g--',label='y*')
    pylab.axhline(x,color='g',label='Yetalon')
    pylab.legend()
    pylab.xlabel('Iteration')
    pylab.ylabel('Interval')

    pylab.figure()
    valid_iter = range(1,n_iter) # Pminus not valid at step 0
    pylab.plot(valid_iter,Pminus[valid_iter],label='a priori error estimate')
    pylab.xlabel('Iteration')
    pylab.ylabel('$(Interval)^2$')
    pylab.setp(pylab.gca(),'ylim',[0,.01])

    pylab.figure()
    pylab.plot(z,'k+',label='noisy measurements')
    #pylab.plot(xhat,'b-',label='a posteri estimate')
    pylab.axhline(x,color='g',label='truth value')
    pylab.legend()
    pylab.xlabel('Iteration')
    pylab.ylabel('Interval')
    pylab.show()

if __name__=='__main__':
    kalman()