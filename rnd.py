import random

class discrete:
    """An efficient sampler for discrete distributions with specified probabilities."""

    def __init__(self, probabilities):
        """Sampler constructor.
        
        Parameters
        ----------
        probabilities: list of float between 0 and 1, in decreasing order.
            (sub)probabilities measures. The surplus of probability is put on the last symbol."""
        
        s=0
        cumul=[0]*len(probabilities)
        for i in range(0,len(probabilities)-1):
            assert(probabilities[i]>=0)
            s+=probabilities[i]
            cumul[i+1]=s
            assert(probabilities[i+1]<=probabilities[i])
        assert(probabilities[-1]>=0)
        s+=probabilities[-1]
        assert(s<=1)
        self.cumul=cumul

    def __sample(self):
        """Binary search."""
        x=random.random()
        inf=0
        sup=len(self.cumul)-1
        if x>self.cumul[sup]:
            return sup
        while(sup-inf>1):
            mid=inf+(sup-inf)//2
            if self.cumul[mid]<x:
                inf=mid
            else:
                sup=mid
        return inf

    def sample(self, n=None):
        """Sampler.
        
        Parameters
        ----------
        n (optional): integer
            How many samples. If unspecified, n=1 is assumed.
        
        Returns
        -------
        res: int or list
            List of int if n is specified, otherwise an integer reprenseting the single realization."""
        if n is None:
            return self.__sample()
        res=[-1]*n
        for i in range(n):
            res[i]=self.__sample()
        return res

