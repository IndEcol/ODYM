# -*- coding: utf-8 -*-
"""
Class DynamicStockModel
Check https://github.com/IndEcol/ODYM for latest version.

Methods for efficient handling of dynamic stock models (DSMs)

Created on Mon Jun 30 17:21:28 2014

@author: Stefan Pauliuk, NTNU Trondheim, Norway, later Uni Freiburg, Germany
with contributions from
Chris Mutel, PSI, Villingen, CH

standard abbreviation: DSM

dependencies:
    numpy >= 1.9
    scipy >= 0.14

Repository for this class, documentation, and tutorials: https://github.com/IndEcol/ODYM

"""


import numpy as np
import scipy.stats



class DynamicStockModel(object):

    """ Class containing a dynamic stock model

    Attributes
    ----------
    t : Series of years or other time intervals
    i : Discrete time series of inflow to stock

    o : Discrete time series of outflow from stock
    o_c :Discrete time series of outflow from stock, by cohort

    s_c : dynamic stock model (stock broken down by year and age- cohort)
    s : Discrete time series for stock, total

    lt : lifetime distribution: dictionary

    pdf: probability density function, distribution of outflow from a specific age-cohort
    
    sf: survival function for different age-cohorts, year x age-cohort table


    name : string, optional
        Name of the dynamic stock model, default is 'DSM'
    """

    """
    Basic initialisation and dimension check methods
    """

    def __init__(self, t=None, i=None, o=None, s=None, lt=None, s_c=None, o_c=None, name='DSM', pdf=None, sf=None):
        """ Init function. Assign the input data to the instance of the object."""
        self.t = t  # optional

        self.i = i  # optional

        self.s = s  # optional
        self.s_c = s_c  # optional

        self.o = o  # optional
        self.o_c = o_c  # optional

        if lt is not None:
            for ThisKey in lt.keys():
                # If we have the same scalar lifetime, stdDev, etc., for all cohorts,
                # replicate this value to full length of the time vector
                if ThisKey != 'Type':
                    if np.array(lt[ThisKey]).shape[0] == 1:
                        lt[ThisKey] = np.tile(lt[ThisKey], len(t))

        self.lt = lt  # optional
        self.name = name  # optional

        self.pdf = pdf # optional
        self.sf  = sf # optional

    def return_version_info(self):
        """Return a brief version statement for this class."""
        return str('Class DynamicStockModel, DSM. Version 1.0. Last change: May 9th, 2015. Check https://github.com/stefanpauliuk/pyDSM for latest version.')

    """ Part 1: Checks and balances: """

    def dimension_check(self):
        """ This method checks which variables are present and checks whether data types and dimensions match
        """
        # Compile a little report on the presence and dimensions of the elements in the SUT
        try:
            DimReport = str('<br><b> Checking dimensions of dynamic stock model ' + self.name + '.')
            if self.t is not None:
                DimReport += str('Time vector is present with ' + str(len(self.t)) + ' years.<br>')
            else:
                DimReport += str('Time vector is not present.<br>')
            if self.i is not None:
                DimReport += str('Inflow vector is present with ' +
                                 str(len(self.i)) + ' years.<br>')
            else:
                DimReport += str('Inflow is not present.<br>')
            if self.s is not None:
                DimReport += str('Total stock is present with ' + str(len(self.s)) + ' years.<br>')
            else:
                DimReport += str('Total stock is not present.<br>')
            if self.s_c is not None:
                DimReport += str('Stock by cohorts is present with ' + str(len(self.s_c)
                                                                           ) + ' years and ' + str(len(self.s_c[0])) + ' cohorts.<br>')
            else:
                DimReport += str('Stock by cohorts is not present.<br>')
            if self.o is not None:
                DimReport += str('Total outflow is present with ' +
                                 str(len(self.o)) + ' years.<br>')
            else:
                DimReport += str('Total outflow is not present.<br>')
            if self.o_c is not None:
                DimReport += str('Outflow by cohorts is present with ' +
                                 str(len(self.o_c)) + ' years and ' + str(len(self.o_c[0])) + ' cohorts.<br>')
            else:
                DimReport += str('Outflow by cohorts is not present.<br>')
            if self.lt is not None:
                DimReport += str('Lifetime distribution is present with type ' +
                                 str(self.lt['Type']) + ' and mean ' + str(self.lt['Mean']) + '.<br>')
            else:
                DimReport += str('Lifetime distribution is not present.<br>')
            return DimReport
        except:
            return str('<br><b> Checking dimensions of dynamic stock model ' + self.name + ' failed.')

    def compute_stock_change(self):
        """ Determine stock change from time series for stock. Formula: stock_change(t) = stock(t) - stock(t-1)."""
        if self.s is not None:
            stock_change = np.zeros(len(self.s))
            stock_change[0] = self.s[0]
            stock_change[1::] = np.diff(self.s)
            return stock_change
        else:
            return None

    def check_stock_balance(self):
        """ Check wether inflow, outflow, and stock are balanced. If possible, the method returns the vector 'Balance', where Balance = inflow - outflow - stock_change"""
        try:
            Balance = self.i - self.o - self.compute_stock_change()
            return Balance
        except:
            # Could not determine balance. At least one of the variables is not defined.
            return None

    def compute_stock_total(self):
        """Determine total stock as row sum of cohort-specific stock."""
        if self.s is not None:
            return self.s
        else:
            try:
                self.s = self.s_c.sum(axis=1)
                return self.s
            except:
                return None # No stock by cohorts exists, and total stock cannot be computed

    def compute_outflow_total(self):
        """Determine total outflow as row sum of cohort-specific outflow."""
        if self.o is not None:
            # Total outflow is already defined. Doing nothing.
            return self.o
        else:
            try:
                self.o = self.o_c.sum(axis=1)
                return self.o
            except:
                return None # No outflow by cohorts exists, and total outflow cannot be computed
            
    def compute_outflow_mb(self):
        """Compute outflow from process via mass balance. 
           Needed in cases where lifetime is zero."""
        try:
            self.o = self.i - self.compute_stock_change()
            return self.o
        except:
            return None # Variables to compute outflow were not present

    """ Part 2: Lifetime model. """

    def compute_outflow_pdf(self):
        """
        Lifetime model. The method compute outflow_pdf returns an array year-by-cohort of the probability of a item added to stock in year m (aka cohort m) leaves in in year n. This value equals pdf(n,m).
        This is the only method for the inflow-driven model where the lifetime distribution directly enters the computation. All other stock variables are determined by mass balance.
        The shape of the output pdf array is NoofYears * NoofYears, but the meaning is years by age-cohorts.
        The method does nothing if the pdf alreay exists.
        """
        if self.pdf is None:
            self.compute_sf() # computation of pdfs moved to this method: compute survival functions sf first, then calculate pdfs from sf.
            self.pdf   = np.zeros((len(self.t), len(self.t)))
            self.pdf[np.diag_indices(len(self.t))] = np.ones(len(self.t)) - self.sf.diagonal(0)
            for m in range(0,len(self.t)):
                self.pdf[np.arange(m+1,len(self.t)),m] = -1 * np.diff(self.sf[np.arange(m,len(self.t)),m])            
            return self.pdf
        else:
            # pdf already exists
            return self.pdf
        
        
    def compute_sf(self): # survival functions
        """
        Survival table self.sf(m,n) denotes the share of an inflow in year n (age-cohort) still present at the end of year m (after m-n years).
        The computation is self.sf(m,n) = ProbDist.sf(m-n), where ProbDist is the appropriate scipy function for the lifetime model chosen.
        For lifetimes 0 the sf is also 0, meaning that the age-cohort leaves during the same year of the inflow.
        The method compute outflow_sf returns an array year-by-cohort of the surviving fraction of a flow added to stock in year m (aka cohort m) in in year n. This value equals sf(n,m).
        This is the only method for the inflow-driven model where the lifetime distribution directly enters the computation. All other stock variables are determined by mass balance.
        The shape of the output sf array is NoofYears * NoofYears, and the meaning is years by age-cohorts.
        The method does nothing if the sf alreay exists. For example, sf could be assigned to the dynamic stock model from an exogenous computation to save time.
        """
        if self.sf is None:
            self.sf = np.zeros((len(self.t), len(self.t)))
            # Perform specific computations and checks for each lifetime distribution:

            if self.lt['Type'] == 'Fixed':
                for m in range(0, len(self.t)):  # cohort index
                    self.sf[m::,m] = np.multiply(1, (np.arange(0,len(self.t)-m) < self.lt['Mean'][m])) # converts bool to 0/1
                # Example: if Lt is 3.5 years fixed, product will still be there after 0, 1, 2, and 3 years, gone after 4 years.

            if self.lt['Type'] == 'Normal':
                for m in range(0, len(self.t)):  # cohort index
                    if self.lt['Mean'][m] != 0:  # For products with lifetime of 0, sf == 0
                        self.sf[m::,m] = scipy.stats.norm.sf(np.arange(0,len(self.t)-m), loc=self.lt['Mean'][m], scale=self.lt['StdDev'][m])
                        # NOTE: As normal distributions have nonzero pdf for negative ages, which are physically impossible, 
                        # these outflow contributions can either be ignored (violates the mass balance) or
                        # allocated to the zeroth year of residence, the latter being implemented in the method compute compute_o_c_from_s_c.
                        
            if self.lt['Type'] == 'Weibull':
                for m in range(0, len(self.t)):  # cohort index
                    if self.lt['Shape'][m] != 0:  # For products with lifetime of 0, sf == 0
                        self.sf[m::,m] = scipy.stats.weibull_min.sf(np.arange(0,len(self.t)-m), c=self.lt['Shape'][m], loc = 0, scale=self.lt['Scale'][m])

            return self.sf
        else:
            # sf already exists
            return self.sf
        

    """
    Part 3: Inflow driven model
    Given: inflow, lifetime dist.
    Default order of methods:
    1) determine stock by cohort
    2) determine total stock
    2) determine outflow by cohort
    3) determine total outflow
    4) check mass balance.
    """

    def compute_s_c_inflow_driven(self):
        """ With given inflow and lifetime distribution, the method builds the stock by cohort.
        """
        if self.i is not None:
            if self.lt is not None:
                self.compute_sf()
                self.s_c = np.einsum('c,tc->tc', self.i, self.sf) # See numpy's np.einsum for documentation.
                # This command means: s_c[t,c] = i[c] * sf[t,c] for all t, c
                # from the perspective of the stock the inflow has the dimension age-cohort, 
                # as each inflow(t) is added to the age-cohort c = t
                return self.s_c
            else:
                # No lifetime distribution specified
                return None
        else:
            # No inflow specified
            return None

    def compute_o_c_from_s_c(self):
        """Compute outflow by cohort from stock by cohort."""
        if self.s_c is not None:
            if self.o_c is None:
                self.o_c = np.zeros(self.s_c.shape)
                self.o_c[1::,:] = -1 * np.diff(self.s_c,n=1,axis=0)
                self.o_c[np.diag_indices(len(self.t))] = self.i - np.diag(self.s_c) # allow for outflow in year 0 already
                return self.o_c
            else:
                # o_c already exists. Doing nothing.
                return self.o_c
        else:
            # s_c does not exist. Doing nothing
            return None

    def compute_i_from_s(self, InitialStock):
        """Given a stock at t0 broken down by different cohorts tx ... t0, an "initial stock". 
           This method calculates the original inflow that generated this stock.
           Example: 
        """
        if self.i is None: # only in cases where no inflow has been specified.
            if len(InitialStock) == len(self.t):
                self.i = np.zeros(len(self.t))
                # construct the sf of a product of cohort tc surviving year t 
                # using the lifetime distributions of the past age-cohorts
                self.compute_sf()
                for Cohort in range(0, len(self.t)):
                    if self.sf[-1,Cohort] != 0:
                        self.i[Cohort] = InitialStock[Cohort] / self.sf[-1,Cohort]
                    else:
                        self.i[Cohort] = 0  # Not possible with given lifetime distribution
                return self.i
            else:
                # The length of t and InitialStock needs to be equal
                return None
        else:
            # i already exists. Doing nothing
            return None

    def compute_evolution_initialstock(self,InitialStock,SwitchTime):
        """ Assume InitialStock is a vector that contains the age structure of the stock at time t0, 
        and it covers as many historic cohorts as there are elements in it.
        This method then computes the future stock and outflow from the year SwitchTime onwards.
        Only future years, i.e., years after SwitchTime, are computed.
        NOTE: This method ignores and deletes previously calculated s_c and o_c.
        The InitialStock is a vector of the age-cohort composition of the stock at SwitchTime, with length SwitchTime"""
        if self.lt is not None:
            self.s_c = np.zeros((len(self.t), len(self.t)))
            self.o_c = np.zeros((len(self.t), len(self.t)))
            self.compute_sf()
            # Extract and renormalize array describing fate of initialstock:
            Shares_Left = self.sf[SwitchTime,0:SwitchTime].copy()
            self.s_c[SwitchTime,0:SwitchTime] = InitialStock # Add initial stock to s_c
            self.s_c[SwitchTime::,0:SwitchTime] = np.tile(InitialStock.transpose(),(len(self.t)-SwitchTime,1)) * self.sf[SwitchTime::,0:SwitchTime] / np.tile(Shares_Left,(len(self.t)-SwitchTime,1))
        return self.s_c
    
    

    """
    Part 4: Stock driven model
    Given: total stock, lifetime dist.
    Default order of methods:
    1) determine inflow, outflow by cohort, and stock by cohort
    2) determine total outflow
    3) determine stock change
    4) check mass balance.
    """

    def compute_stock_driven_model(self, NegativeInflowCorrect = False):
        """ With given total stock and lifetime distribution, 
            the method builds the stock by cohort and the inflow.
        """
        if self.s is not None:
            if self.lt is not None:
                self.s_c = np.zeros((len(self.t), len(self.t)))
                self.o_c = np.zeros((len(self.t), len(self.t)))
                self.i = np.zeros(len(self.t))
                # construct the sf of a product of cohort tc remaining in the stock in year t
                self.compute_sf() # Computes sf if not present already.
                # First year:
                if self.sf[0, 0] != 0: # Else, inflow is 0.
                    self.i[0] = self.s[0] / self.sf[0, 0]
                self.s_c[:, 0] = self.i[0] * self.sf[:, 0] # Future decay of age-cohort of year 0.
                self.o_c[0, 0] = self.i[0] - self.s_c[0, 0]
                # all other years:
                for m in range(1, len(self.t)):  # for all years m, starting in second year
                    # 1) Compute outflow from previous years
                    self.o_c[m, 0:m] = self.s_c[m-1, 0:m] - self.s_c[m, 0:m] # outflow table is filled row-wise, for each year m.
                    # 2) Determine inflow from mass balance:
                    if self.sf[m,m] != 0: # Else, inflow is 0.
                        self.i[m] = (self.s[m] - self.s_c[m, :].sum()) / self.sf[m,m] # allow for outflow during first year by rescaling with 1/sf[m,m]
                    # 2a) Correct remaining stock in cases where inflow would be negative:
                    if NegativeInflowCorrect is True:
                        if self.i[m] < 0: # if stock-driven model yield negative inflow
                            Delta = -1 * self.i[m].copy() # Delta > 0!
                            self.i[m] = 0 # Set inflow to 0 and distribute mass balance gap onto remaining cohorts:
                            if self.o_c[m,:].sum() != 0:
                                Delta_c = Delta * self.o_c[m, :] / self.o_c[m,:].sum() # Distribute gap proportionally to outflow
                            else:
                                Delta_c = 0
                            self.o_c[m, :] = self.o_c[m, :] - Delta_c # reduce outflow by Delta_c
                            self.s_c[m, :] = self.s_c[m, :] + Delta_c # augment stock by Delta_c
                            # NOTE: This method is only of of many plausible methods of reducing the outflow to keep stock levels high.
                            # It may lead to implausible results, and, if Delta > sum(self.o_c[m,:]), also to negative outflows.
                            # In such situations it is much better to change the lifetime assumption than using the NegativeInflowCorrect option.
                    # 3) Add new inflow to stock and determine future decay of new age-cohort
                    self.s_c[m::, m] = self.i[m] * self.sf[m::, m]
                    self.o_c[m, m]   = self.i[m] * (1 - self.sf[m, m])
                return self.s_c, self.o_c, self.i
            else:
                # No lifetime distribution specified
                return None, None, None
        else:
            # No stock specified
            return None, None, None
        

    def compute_stock_driven_model_initialstock(self,InitialStock,SwitchTime):
        """ With given total stock and lifetime distribution, the method builds the stock by cohort and the inflow.
        The extra parameter InitialStock is a vector that contains the age structure of the stock at the END of the year Switchtime -1 = t0.
        In the year SwitchTime (start counting from 1) the model switches from the historic stock to the stock-driven approach. SwithTime is the first year with the stock-driven approach.
        Convention: Stocks are measured AT THE END OF THE YEAR. Flows occur DURING THE YEAR.
        InitialStock contains the age-cohort composition of the stock AT THE END of year SwitchTime -1, counting from 1 not 0.
        InitialStock must have length = SwithTime -1.
        """
        if self.s is not None:
            if self.lt is not None:
                self.s_c = np.zeros((len(self.t), len(self.t)))
                self.s_c[SwitchTime -2,0:SwitchTime-1] = InitialStock # assign initialstock to stock-by-cohort variable at END OF YEAR SwitchTime (here -1, because indexing starts at 0.).
                self.o_c = np.zeros((len(self.t), len(self.t)))
                self.i = np.zeros(len(self.t))
                
                # construct the sdf of a product of cohort tc leaving the stock in year t
                self.compute_sf() # Computes sf if not present already.
                
                # Construct historic inflows
                for c in range(0,SwitchTime -1):
                    if self.sf[SwitchTime -2,c] != 0:
                         self.i[c] = InitialStock[c] / self.sf[SwitchTime -2,c]
                    else:
                         self.i[c] = InitialStock[c]
                         
                # Add stock from historic inflow
                self.s_c[:,0:SwitchTime-1] = np.einsum('tc,c->tc',self.sf[:,0:SwitchTime-1],self.i[0:SwitchTime-1])
                # calculate historic outflow
                for m in range(0,SwitchTime-1):
                    self.o_c[m, m]    = self.i[m] * (1 - self.sf[m, m])
                    self.o_c[m+1::,m] = self.s_c[m:-1,m] - self.s_c[m+1::,m]
                # for future: year-by-year computation, starting from SwitchTime
                for m in range(SwitchTime-1, len(self.t)):  # for all years m, starting at SwitchTime
                    # 1) Determine inflow from mass balance:
                    if self.sf[m,m] != 0: # Else, inflow is 0.
                        self.i[m] = (self.s[m] - self.s_c[m, :].sum()) / self.sf[m,m] # allow for outflow during first year by rescaling with 1/sf[m,m]
                    # NOTE: The stock-driven method may lead negative inflows, if the stock development is in contradiction with the lifetime model.
                    # In such situations the lifetime assumption must be changed, either by directly using different lifetime values or by adjusting the outlfows, 
                    # cf. the option NegativeInflowCorrect in the method compute_stock_driven_model.
                    # 2) Add new inflow to stock and determine future decay of new age-cohort
                    self.s_c[m::, m]  = self.i[m] * self.sf[m::, m]
                    self.o_c[m, m]    = self.i[m] * (1 - self.sf[m, m])
                    self.o_c[m+1::,m] = self.s_c[m:-1,m] - self.s_c[m+1::,m]
                    
                return self.s_c, self.o_c, self.i
            else:
                # No lifetime distribution specified
                return None, None, None
        else:
            # No stock specified
            return None, None, None       

