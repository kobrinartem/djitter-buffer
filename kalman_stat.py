__author__ = 'artem'
import numpy
import pylab

def kalman():
    #init
    n_iter = 500
    sz = (n_iter,) # size of array
    x = 0.025 # truth value (typo in example at top of p. 13 calls this z)
    z = numpy.random.normal(x,0.005,size=sz)
    Q = 1e-3 # process variance

    # allocate space for arrays
    xhat=numpy.zeros(sz)      # a posteri estimate of x
    P=numpy.zeros(sz)         # a posteri error estimate
    xhatminus=numpy.zeros(sz) # a priori estimate of x
    Pminus=numpy.zeros(sz)    # a priori error estimate
    K=numpy.zeros(sz)         # gain or blending factor

    R = 0.1**2 # estimate of measurement variance, change to see effect

    # intial guesses
    xhat[0] = 0.0
    P[0] = 1.0

    for k in range(1,n_iter):
        # time update
        xhatminus[k] = xhat[k-1]
        Pminus[k] = P[k-1]+Q

        # measurement update
        K[k] = Pminus[k]/( Pminus[k]+R )
        xhat[k] = xhatminus[k]+K[k]*(z[k]-xhatminus[k])
        P[k] = (1-K[k])*Pminus[k]

    pylab.figure()
    pylab.plot(z,'k+',label='noisy measurements')
    pylab.plot(xhat,'b-',label='a posteri estimate')
    pylab.axhline(x,color='g',label='truth value')
    pylab.legend()
    pylab.xlabel('Iteration')
    pylab.ylabel('Interval')

    pylab.figure()
    valid_iter = range(1,n_iter) # Pminus not valid at step 0
    pylab.plot(valid_iter,Pminus[valid_iter],label='a priori error estimate')
    pylab.xlabel('Iteration')
    pylab.ylabel('$(Interval)^2$')
    pylab.setp(pylab.gca(),'ylim',[0,.01])
    pylab.show()




if __name__=='__main__':
    kalman()