import ROOT as rt
import numpy as np
import array as ar
"""
Class interface for automatic histogram binning
"""

from abc import ABCMeta, abstractmethod
class HistogramBinning:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_histogram(self):
        pass

class UniformBinning1D(HistogramBinning):
    """
    Uniform binning provider
    """
    def __init__(self,nbins,xmin,xmax):
        self._nbins = nbins
        self._xmin = xmin
        self._xmax = xmax
    
    def binning(self,**kwargs):
        self._nbins = kwargs.get('nbins',self._nbins)
        self._xmin = kwargs.get('xmin',self._xmin)
        self._xmax = kwargs.get('xmax',self._xmax)

    def get_histogram(self):
        return rt.TH1D("sample_hist","",self._nbins,self._xmin,self._xmax)

class OprimizedBinning(HistogramBinning):
    """
    Optimized binning provider.
    Theory behind optimality of equiprobable binning can be found
    in F.James "Statistical Methods in Experimental Physics" 2nd ed.
    Sec. 11.2.3. number of bins is determined according to eq. 11.8
    Alternative binning schemes: Sturges, Scott 
    (see https://en.wikipedia.org/wiki/Histogram#Number_of_bins_and_width)
    """
    def __init__(self,vec,xmin=None,xmax=None):
        self._lowstat_algo = 'fd'
        self._lowstat_thresh = 20
        self._vec=vec
        self._xmin=xmin
        self._xmax=xmax
        self._bin_edges = []
        # Normal distr. 1% alpha-point lambda(0.01)
        self._lambda_alpha = 2.33
        # Normal distr. (1-p0) alpha point, when p0=0.8. 
        # Prob to accept H0, when false is 1-p0
        self._lambda_false_positive = 0.84
        #b parameter can be between 2 and 4 (b=4 for simple hypothesis, i.e. no free parameters)
        self._b = 2

    def get_n_bins_fd(self):
        self._lowstat_algo='fd'
        n_entries = len(self._vec)
        self._vec.sort()
        irq = np.subtract(*np.percentile(self._vec, [75, 25]))
        min,max=self._vec[0],self._vec[-1]
        bin_width = 2.*irq/(n_entries)**(1./3.)
        nbins = (max - min)/bin_width
        print "FD: ", nbins
        return int(nbins)

    def get_n_bins_scott(self):
        self._lowstat_algo='scott'
        n_entries = len(self._vec)
        print self._vec
        self._vec.sort()
        sigma = np.std(self._vec)
        min,max=self._vec[0],self._vec[-1]
        bin_width = 3.5*sigma/(n_entries)**(1./3.)
        print sigma,n_entries,self._vec
        nbins = (max - min)/bin_width
        print "Scott: ", nbins
        return int(nbins)

    def get_n_bins_sturges(self,n_entries):
        self._lowstat_algo='sturge'
        nbins = 1+rt.TMath.Log2(n_entries)
        print "Sturges: ", nbins
        return int(nbins)

    def get_n_bins_james(self,n_entries):
        self._lowstat_algo='james'
        #eq. 11.8 from F.James
        num = self._b*2.**0.5*(n_entries-1)**(2./5.)
        den = (self._lambda_alpha+self._lambda_false_positive)**(2./5.)
        nbins = int(num/den)
        print "James: ", nbins
        return nbins

    def get_histogram(self):
        self.binning()
        bin_edges = ar.array('d',self._bin_edges)
        return rt.TH1D("sample_hist","",len(self._bin_edges)-1,bin_edges)

    def binning(self,**kwargs):
        self._lowstat_algo = kwargs.get('lowstat_algo',self._lowstat_algo)
        self._lambda_alpha = kwargs.get('lambda_alpha',self._lambda_alpha)
        self._lambda_false_positive = kwargs.get('lambda_false_positive',self._lambda_false_positive)
        self._b = kwargs.get('b',self._b)
        
        #sort in ascending order for empirical cdf
        self._vec.sort()

        n_entries = len(self._vec)
        nbins = None
        if n_entries<self._lowstat_thresh:
            if self._lowstat_algo == 'sturge': nbins = self.get_n_bins_sturges(n_entries) 
            elif self._lowstat_algo == 'fd': nbins = self.get_n_bins_fd()
            elif self._lowstat_algo == 'scott': nbins = self.get_n_bins_scott()
            elif self._lowstat_algo == 'james': nbins = self.get_n_bins_james(n_entries)
            else: print "Error!"
        else:
            nbins = self.get_n_bins_james(n_entries)
        n_entries_per_bin = int(n_entries/nbins)
        current_entry = 0
        bin_edges_set = set()
        if self._xmax: bin_edges_set.add(self._xmax)
        else: bin_edges_set.add(self._vec[-1]+self._vec[-1]*0.01)
        for el in reversed(self._vec):
            current_entry+=1
            if current_entry > n_entries_per_bin:
                bin_edges_set.add(el)
                current_entry=0
        if self._xmin: bin_edges_set.add(self._xmin)
        else: bin_edges_set.add(self._vec[0])
        self._bin_edges = list(bin_edges_set)
        self._bin_edges.sort()
        print "bins:", self._bin_edges