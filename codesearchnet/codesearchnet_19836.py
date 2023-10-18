def filter_gaussian(Ys,sigma,plotToo=False):
    """simple gaussian convolution. Returns same # of points as gotten."""
    timeA=time.time()
    window=scipy.signal.gaussian(len(Ys),sigma)
    window/=sum(window)
    Ys2=np.convolve(Ys,window,'same')
    print("LEN:",len(Ys2),len(Ys))
    timeB=time.time()
    print("convolution took %.03f ms"%((timeB-timeA)*1000))
    if len(Ys2)!=len(Ys):
        print("?!?!?!? convolution point size mismatch")
    if plotToo:
        pylab.plot(Ys,label='original',alpha=.2)
        pylab.plot(Ys2,'b-',label='smooth')
        pylab.legend()
        pylab.show()
    return Ys2