# -*- coding: utf-8 -*-
"""
Class DynamicStockModel
Check https://github.com/IndEcol/ODYM for latest version.

Methods for efficient handling of dynamic stock models (DSMs)

Created on Mon Jun 30 17:21:28 2014

@author: Stefan Pauliuk, NTNU Trondheim, Norway, later Uni Freiburg, Germany
with contributions from
Sebastiaan Deetman, CML, Leiden, NL
Tomer Fishman, IDC Herzliya, IL
Chris Mutel, PSI, Villingen, CH

standard abbreviation: DSM or dsm

dependencies:
    numpy >= 1.9
    scipy >= 0.14

Repository for this class, documentation, and tutorials: https://github.com/IndEcol/ODYM

"""

import numpy as np
import scipy.stats

def __version__():
    """Return a brief version string and statement for this class."""
    return str('1.0'), str('Class DynamicStockModel, dsm. Version 1.0. Last change: July 25th, 2019. Check https://github.com/IndEcol/ODYM for latest version.')


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
                                 str(self.lt['Type']) + '.<br>')
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
        The pdf is computed from the survival table sf, where the type of the lifetime distribution enters.
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

            if self.lt['Type'] == 'Fixed': # fixed lifetime, age-cohort leaves the stock in the model year when the age specified as 'Mean' is reached.
                for m in range(0, len(self.t)):  # cohort index
                    self.sf[m::,m] = np.multiply(1, (np.arange(0,len(self.t)-m) < self.lt['Mean'][m])) # converts bool to 0/1
                # Example: if Lt is 3.5 years fixed, product will still be there after 0, 1, 2, and 3 years, gone after 4 years.

            if self.lt['Type'] == 'Normal': # normally distributed lifetime with mean and standard deviation. Watch out for nonzero values 
                # for negative ages, no correction or truncation done here. Cf. note below.
                for m in range(0, len(self.t)):  # cohort index
                    if self.lt['Mean'][m] != 0:  # For products with lifetime of 0, sf == 0
                        self.sf[m::,m] = scipy.stats.norm.sf(np.arange(0,len(self.t)-m), loc=self.lt['Mean'][m], scale=self.lt['StdDev'][m])
                        # NOTE: As normal distributions have nonzero pdf for negative ages, which are physically impossible, 
                        # these outflow contributions can either be ignored (violates the mass balance) or
                        # allocated to the zeroth year of residence, the latter being implemented in the method compute compute_o_c_from_s_c.
                        # As alternative, use lognormal or folded normal distribution options.
                        
            if self.lt['Type'] == 'FoldedNormal': # Folded normal distribution, cf. https://en.wikipedia.org/wiki/Folded_normal_distribution
                for m in range(0, len(self.t)):  # cohort index
                    if self.lt['Mean'][m] != 0:  # For products with lifetime of 0, sf == 0
                        self.sf[m::,m] = scipy.stats.foldnorm.sf(np.arange(0,len(self.t)-m), self.lt['Mean'][m]/self.lt['StdDev'][m], 0, scale=self.lt['StdDev'][m])
                        # NOTE: call this option with the parameters of the normal distribution mu and sigma of curve BEFORE folding,
                        # curve after folding will have different mu and sigma.
                        
            if self.lt['Type'] == 'LogNormal': # lognormal distribution
                # Here, the mean and stddev of the lognormal curve, 
                # not those of the underlying normal distribution, need to be specified! conversion of parameters done here:
                for m in range(0, len(self.t)):  # cohort index
                    if self.lt['Mean'][m] != 0:  # For products with lifetime of 0, sf == 0
                        # calculate parameter mu    of underlying normal distribution:
                        LT_LN = np.log(self.lt['Mean'][m] / np.sqrt(1 + self.lt['Mean'][m] * self.lt['Mean'][m] / (self.lt['StdDev'][m] * self.lt['StdDev'][m]))) 
                        # calculate parameter sigma of underlying normal distribution:
                        SG_LN = np.sqrt(np.log(1 + self.lt['Mean'][m] * self.lt['Mean'][m] / (self.lt['StdDev'][m] * self.lt['StdDev'][m])))
                        # compute survial function
                        self.sf[m::,m] = scipy.stats.lognorm.sf(np.arange(0,len(self.t)-m), s=SG_LN, loc = 0, scale=np.exp(LT_LN)) 
                        # values chosen according to description on
                        # https://docs.scipy.org/doc/scipy-0.13.0/reference/generated/scipy.stats.lognorm.html
                        # Same result as EXCEL function "=LOGNORM.VERT(x;LT_LN;SG_LN;TRUE)"
                        
            if self.lt['Type'] == 'Weibull': # Weibull distribution with standard definition of scale and shape parameters
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
                    # 1) Compute outflow from previous age-cohorts up to m-1
                    self.o_c[m, 0:m] = self.s_c[m-1, 0:m] - self.s_c[m, 0:m] # outflow table is filled row-wise, for each year m.
                    # 2) Determine inflow from mass balance:
                    if NegativeInflowCorrect is False: # if no correction for negative inflows is made 
                        if self.sf[m,m] != 0: # Else, inflow is 0.
                            self.i[m] = (self.s[m] - self.s_c[m, :].sum()) / self.sf[m,m] # allow for outflow during first year by rescaling with 1/sf[m,m]
                        # 3) Add new inflow to stock and determine future decay of new age-cohort
                        self.s_c[m::, m] = self.i[m] * self.sf[m::, m]
                        self.o_c[m, m]   = self.i[m] * (1 - self.sf[m, m])
                    # 2a) Correct remaining stock in cases where inflow would be negative:
                    if NegativeInflowCorrect is True: # if the stock declines faster than according to the lifetime model, this option allows to extract additional stock items.
                        # The negative inflow correction implemented here was developed in a joined effort by Sebastiaan Deetman and Stefan Pauliuk.
                        InflowTest = self.s[m] - self.s_c[m, :].sum()
                        if InflowTest < 0: # if stock-driven model would yield negative inflow
                            Delta = -1 * InflowTest # Delta > 0!
                            self.i[m] = 0 # Set inflow to 0 and distribute mass balance gap onto remaining cohorts:
                            if self.s_c[m,:].sum() != 0:
                                Delta_percent = Delta / self.s_c[m,:].sum() 
                                # Distribute gap equally across all cohorts (each cohort is adjusted by the same %, based on surplus with regards to the prescribed stock)
                                # Delta_percent is a % value <= 100%
                            else:
                                Delta_percent = 0 # stock in this year is already zero, method does not work in this case.
                            # correct for outflow and stock in current and future years
                            # adjust the entire stock AFTER year m as well, stock is lowered in year m, so future cohort survival also needs to decrease.
                            self.o_c[m, :] = self.o_c[m, :] + (self.s_c[m, :] * Delta_percent)  # increase outflow according to the lost fraction of the stock, based on Delta_c
                            self.s_c[m::,0:m] = self.s_c[m::,0:m] * (1-Delta_percent) # shrink future description of stock from previous age-cohorts by factor Delta_percent in current AND future years.
                        else: # If no negative inflow would occur
                            if self.sf[m,m] != 0: # Else, inflow is 0.
                                self.i[m] = (self.s[m] - self.s_c[m, :].sum()) / self.sf[m,m] # allow for outflow during first year by rescaling with 1/sf[m,m]    
                            # Add new inflow to stock and determine future decay of new age-cohort
                            self.s_c[m::, m] = self.i[m] * self.sf[m::, m]
                            self.o_c[m, m]   = self.i[m] * (1 - self.sf[m, m])                                
                        # NOTE: This method of negative inflow correction is only of of many plausible methods of increasing the outflow to keep matching stock levels.
                        # It assumes that the surplus stock is removed in the year that it becomes obsolete. Each cohort loses the same fraction.
                        # Modellers need to try out whether this method leads to justifiable results.
                        # In some situations it is better to change the lifetime assumption than using the NegativeInflowCorrect option.
                    
                return self.s_c, self.o_c, self.i
            else:
                # No lifetime distribution specified
                return None, None, None
        else:
            # No stock specified
            return None, None, None
        

    def compute_stock_driven_model_initialstock(self,InitialStock,SwitchTime,NegativeInflowCorrect = False):
        """ With given total stock and lifetime distribution, the method builds the stock by cohort and the inflow.
        The extra parameter InitialStock is a vector that contains the age structure of the stock at the END of the year Switchtime -1 = t0.
        ***
        Convention 1: Stocks are measured AT THE END OF THE YEAR. Flows occur DURING THE YEAR.
        Convention 2: The model time t spans both historic and future age-cohorts, and the index SwitchTime -1 indicates the first future age-cohort.
        Convention 3: SwitchTime = len(InitialStock) + 1, that means SwitchTime is counted starting from 1 and not 0.
        Convention 4: The future stock time series has 0 as its first len(InitialStock) elements.
        ***
        In the year SwitchTime the model switches from the historic stock to the stock-driven approach. 
        The year SwitchTime is the first year with the stock-driven approach.
        InitialStock contains the age-cohort composition of the stock AT THE END of year SwitchTime -1.
            InitialStock must have length = SwithTime -1.
        For the option "NegativeInflowCorrect", see the explanations for the method compute_stock_driven_model(self, NegativeInflowCorrect = True).
        NegativeInflowCorrect only affects the future stock time series and works exactly as for the stock-driven model without initial stock.
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
                if NegativeInflowCorrect is False:
                    for m in range(SwitchTime-1, len(self.t)):  # for all years m, starting at SwitchTime
                        # 1) Determine inflow from mass balance:
                        if self.sf[m,m] != 0: # Else, inflow is 0.
                            self.i[m] = (self.s[m] - self.s_c[m, :].sum()) / self.sf[m,m] # allow for outflow during first year by rescaling with 1/sf[m,m]
                        # NOTE: The stock-driven method may lead to negative inflows, if the stock development is in contradiction with the lifetime model.
                        # In such situations the lifetime assumption must be changed, either by directly using different lifetime values or by adjusting the outlfows, 
                        # cf. the option NegativeInflowCorrect in the method compute_stock_driven_model.
                        # 2) Add new inflow to stock and determine future decay of new age-cohort
                        self.s_c[m::, m]  = self.i[m] * self.sf[m::, m]
                        self.o_c[m, m]    = self.i[m] * (1 - self.sf[m, m])
                        self.o_c[m+1::,m] = self.s_c[m:-1,m] - self.s_c[m+1::,m]
                if NegativeInflowCorrect is True:
                    for m in range(SwitchTime-1, len(self.t)):  # for all years m, starting at SwitchTime
                        self.o_c[m, 0:m] = self.s_c[m-1, 0:m] - self.s_c[m, 0:m] # outflow table is filled row-wise, for each year m.
                        # 1) Determine text inflow from mass balance:
                        InflowTest = self.s[m] - self.s_c[m, :].sum()
                        if InflowTest < 0: 
                            Delta = -1 * InflowTest # Delta > 0!
                            self.i[m] = 0 # Set inflow to 0 and distribute mass balance gap onto remaining cohorts:
                            if self.s_c[m,:].sum() != 0:
                                Delta_percent = Delta / self.s_c[m,:].sum() 
                                # Distribute gap equally across all cohorts (each cohort is adjusted by the same %, based on surplus with regards to the prescribed stock)
                                # Delta_percent is a % value <= 100%
                            else:
                                Delta_percent = 0 # stock in this year is already zero, method does not work in this case.
                            # correct for outflow and stock in current and future years
                            # adjust the entire stock AFTER year m as well, stock is lowered in year m, so future cohort survival also needs to decrease.
                            # print(InflowTest)
                            # print((self.s_c[m, :] * Delta_percent).sum())
                            # print('_')
                            self.o_c[m, :] = self.o_c[m, :] + (self.s_c[m, :] * Delta_percent).copy()  # increase outflow according to the lost fraction of the stock, based on Delta_c
                            self.s_c[m::,0:m] = self.s_c[m::,0:m] * (1-Delta_percent.copy()) # shrink future description of stock from previous age-cohorts by factor Delta_percent in current AND future years.
                        else:
                            if self.sf[m,m] != 0: # Else, inflow is 0.
                                self.i[m] = (self.s[m] - self.s_c[m, :].sum()) / self.sf[m,m] # allow for outflow during first year by rescaling with 1/sf[m,m]
                            # 2) Add new inflow to stock and determine future decay of new age-cohort
                            self.s_c[m::, m]  = self.i[m] * self.sf[m::, m]
                            self.o_c[m, m]    = self.i[m] * (1 - self.sf[m, m])
                # Add historic stock series to total stock s:
                self.s[0:SwitchTime-1]= self.s_c[0:SwitchTime-1,:].sum(axis =1).copy()                    
                return self.s_c, self.o_c, self.i
            else:
                # No lifetime distribution specified
                return None, None, None
        else:
            # No stock specified
            return None, None, None       
        
  
    def compute_stock_driven_model_initialstock_typesplit(self,FutureStock,InitialStock,SFArrayCombined,TypeSplit):
        """ 
        With given total future stock and lifetime distribution, the method builds the stock by cohort and the inflow.
        The age structure of the initial stock is given for each technology, and a type split of total inflow into different technology types is given as well.
        
        SPECIFICATION: Stocks are always measured AT THE END of the discrete time interval.
        
        Indices:
          t: time: Entire time frame: from earliest age-cohort to latest model year.
          c: age-cohort: same as time.
          T: Switch time: DEFINED as first year where historic stock is NOT present, = last year where historic stock is present +1.
             Switchtime is calculated internally, by subtracting the length of the historic stock from the total model length.
          g: product type
        
        Data:
          FutureStock[t],           total future stock at end of each year, starting at T
          InitialStock[c,g],        0...T-1;0...T-1, stock at the end of T-1, by age-cohort c, ranging from 0...T-1, and product type g
                                    c-dimension has full length, all future years must be 0.
          SFArrayCombined[t,c,g],   Survival function of age-cohort c at end of year t for product type g
                                    this array spans both historic and future age-cohorts
          Typesplit[t,g],           splits total inflow into product types for future years 
            
        The extra parameter InitialStock is a vector that contains the age structure of the stock at time t0, and it covers as many historic cohorts as there are elements in it.
        In the year SwitchTime the model switches from the historic stock to the stock-driven approach.
        Only future years, i.e., years after SwitchTime, are computed and returned.
        The InitialStock is a vector of the age-cohort composition of the stock at SwitchTime, with length SwitchTime.
        The parameter TypeSplit splits the total inflow into Ng types. """
        
        if self.s is not None:
            if self.lt is not None:
                
                SwitchTime = SFArrayCombined.shape[0] - FutureStock.shape[0]
                Ntt        = SFArrayCombined.shape[0] # Total no of years
                Nt0        = FutureStock.shape[0]     # No of future years
                Ng         = SFArrayCombined.shape[2] # No of product groups
                
                s_cg = np.zeros((Nt0,Ntt,Ng)) # stock for future years, all age-cohorts and product
                o_cg = np.zeros((Nt0,Ntt,Ng)) # outflow by future years, all cohorts and products
                i_g  = np.zeros((Ntt,Ng))     # inflow by product
                
                # Construct historic inflows
                for c in range(0,SwitchTime): # for all historic age-cohorts til SwitchTime - 1:
                    for g in range(0,Ng):
                        if SFArrayCombined[SwitchTime-1,c,g] != 0:
                         i_g[c,g] = InitialStock[c,g] / SFArrayCombined[SwitchTime-1,c,g]
                         
                         # if InitialStock is 0, historic inflow also remains 0, 
                         # as it has no impact on future anymore.
                         
                         # If survival function is 0 but initial stock is not, the data are inconsisent and need to be revised.
                         # For example, a safety-relevant device with 5 years fixed lifetime but a 10 year old device is present.
                         # Such items will be ignored and break the mass balance.
            
                # year-by-year computation, starting from SwitchTime
                for t in range(SwitchTime, Ntt):  # for all years t, starting at SwitchTime
                    # 1) Compute stock at the end of the year:
                    s_cg[t - SwitchTime,:,:] = np.einsum('cg,cg->cg',i_g,SFArrayCombined[t,:,:])
                    # 2) Compute outflow during year t from previous age-cohorts:
                    if t == SwitchTime:
                        o_cg[t -SwitchTime,:,:] = InitialStock - s_cg[t -SwitchTime,:,:]
                    else:
                        o_cg[t -SwitchTime,:,:] = s_cg[t -SwitchTime -1,:,:] - s_cg[t -SwitchTime,:,:] # outflow table is filled row-wise, for each year t.
                    # 3) Determine total inflow from mass balance:
                    i0 = FutureStock[t -SwitchTime] - s_cg[t - SwitchTime,:,:].sum()
                    # 4) Add new inflow to stock and determine future decay of new age-cohort
                    i_g[t,:] = TypeSplit[t -SwitchTime,:] * i0
                    for g in range(0,Ng): # Correct for share of inflow leaving during first year.
                        if SFArrayCombined[t,t,g] != 0: # Else, inflow leaves within the same year and stock modelling is useless
                            i_g[t,g] = i_g[t,g] / SFArrayCombined[t,t,g] # allow for outflow during first year by rescaling with 1/SF[t,t,g]
                        s_cg[t -SwitchTime,t,g]  = i_g[t,g] * SFArrayCombined[t,t,g]
                        o_cg[t -SwitchTime,t,g]  = i_g[t,g] * (1 - SFArrayCombined[t,t,g])
                    
                # Add total values of parameter to enable mass balance check:
                self.s_c = s_cg.sum(axis =2)
                self.o_c = o_cg.sum(axis =2)
                self.i   =  i_g[SwitchTime::,:].sum(axis =1)
                
                return s_cg, o_cg, i_g
            else:
                # No lifetime distribution specified
                return None, None, None
        else:
            # No stock specified
            return None, None, None      
        
    def compute_stock_driven_model_initialstock_typesplit_negativeinflowcorrect(self,SwitchTime,InitialStock,SFArrayCombined,TypeSplit,NegativeInflowCorrect = False):
        """ 
        With given total future stock and lifetime distribution, the method builds the stock by cohort and the inflow.
        The age structure of the initial stock is given for each technology, and a type split of total inflow into different technology types is given as well.
        For the option "NegativeInflowCorrect", see the explanations for the method compute_stock_driven_model(self, NegativeInflowCorrect = True).
        NegativeInflowCorrect only affects the future stock time series and works exactly as for the stock-driven model without initial stock.
        
        SPECIFICATION: Stocks are always measured AT THE END of the discrete time interval.
        
        Indices:
          t: time: Entire time frame: from earliest age-cohort to latest model year.
          c: age-cohort: same as time.
          T: Switch time: DEFINED as first year where historic stock is NOT present, = last year where historic stock is present +1.
             Switchtime must be given as argument. Example: if the first three age-cohorts are historic, SwitchTime is 3, which indicates the 4th year.
             That also means that the first 3 time-entries for the stock and typesplit arrays must be 0.
          g: product type
        
        Data:
          s[t],                     total future stock time series, at end of each year, starting at T, trailing 0s for historic years.
                                    ! is not handed over with the function call but earlier, when defining the dsm.
          InitialStock[c,g],        0...T-1;0...T-1, stock at the end of T-1, by age-cohort c, ranging from 0...T-1, and product type g
                                    c-dimension has full length, all future years must be 0.
          SFArrayCombined[t,c,g],   Survival function of age-cohort c at end of year t for product type g
                                    this array spans both historic and future age-cohorts
          Typesplit[t,g],           splits total inflow into product types for future years 
          NegativeInflowCorrect     BOOL, retains items in stock if their leaving would lead to negative inflows. 
            
        The extra parameter InitialStock is a vector that contains the age structure of the stock at time t0, and it covers as many historic cohorts as there are elements in it.
        In the year SwitchTime the model switches from the historic stock to the stock-driven approach.
        Only future years, i.e., years after SwitchTime, are computed and returned.
        The InitialStock is a vector of the age-cohort composition of the stock at SwitchTime, with length SwitchTime.
        The parameter TypeSplit splits the total inflow into Ng types. """
        
        if self.s is not None:
            if self.lt is not None:
                
                Ntt        = SFArrayCombined.shape[0] # Total no of years
                Ng         = SFArrayCombined.shape[2] # No of product groups
                
                s_cg = np.zeros((Ntt,Ntt,Ng)) # stock for future years, all age-cohorts and products
                o_cg = np.zeros((Ntt,Ntt,Ng)) # outflow by future years, all cohorts and products
                i_g  = np.zeros((Ntt,Ng))     # inflow for all years by product
                NIC_Flags = np.zeros((Ntt,1)) # inflow flog for future years, will be set to calculated negative inflow value if negative inflow occurs and is corrected for.
                
                self.s_c = np.zeros((len(self.t), len(self.t)))
                self.o_c = np.zeros((len(self.t), len(self.t)))
                self.i   = np.zeros(len(self.t))
                
                # construct the sdf of a product of cohort tc leaving the stock in year t
                self.compute_sf() # Computes sf if not present already.
                # Construct historic inflows
                for c in range(0,SwitchTime): # for all historic age-cohorts til SwitchTime - 1:
                    for g in range(0,Ng):
                        if SFArrayCombined[SwitchTime-1,c,g] != 0:
                            i_g[c,g] = InitialStock[c,g] / SFArrayCombined[SwitchTime-1,c,g]
                         
                         # if InitialStock is 0, historic inflow also remains 0, 
                         # as it has no impact on future anymore.
                         
                         # If survival function is 0 but initial stock is not, the data are inconsisent and need to be revised.
                         # For example, a safety-relevant device with 5 years fixed lifetime but a 10 year old device is present.
                         # Such items will be ignored and break the mass balance.
                         
                # Compute stocks from historic inflows
                s_cg[:,0:SwitchTime,:] = np.einsum('tcg,cg->tcg',SFArrayCombined[:,0:SwitchTime,:],i_g[0:SwitchTime,:])
                # calculate historic outflows
                for m in range(0,SwitchTime):
                    o_cg[m,m,:]      = i_g[m,:] * (1 - SFArrayCombined[m,m,:])
                    o_cg[m+1::,m,:]  = s_cg[m:-1,m,:] - s_cg[m+1::,m,:]
                # add historic age-cohorts to total stock:
                self.s[0:SwitchTime] = np.einsum('tcg->t',s_cg[0:SwitchTime,:,:])
                
                # for future: year-by-year computation, starting from SwitchTime
                if NegativeInflowCorrect is False:
                    for m in range(SwitchTime, len(self.t)):  # for all years m, starting at SwitchTime
                        # 1) Determine inflow from mass balance:
                        i0_test = self.s[m] - s_cg[m,:,:].sum()
                        if i0_test < 0:
                            NIC_Flags[m] = i0_test
                        for g in range(0,Ng):
                            if SFArrayCombined[m,m,g] != 0: # Else, inflow is 0.
                                i_g[m,g] = TypeSplit[m,g] * i0_test / SFArrayCombined[m,m,g] # allow for outflow during first year by rescaling with 1/sf[m,m]
                                # NOTE: The stock-driven method may lead to negative inflows, if the stock development is in contradiction with the lifetime model.
                                # In such situations the lifetime assumption must be changed, either by directly using different lifetime values or by adjusting the outlfows, 
                                # cf. the option NegativeInflowCorrect in the method compute_stock_driven_model.
                                # 2) Add new inflow to stock and determine future decay of new age-cohort
                            s_cg[m::,m,g]   = i_g[m,g] * SFArrayCombined[m::,m,g]
                            o_cg[m,m,g]     = i_g[m,g] * (1 - SFArrayCombined[m,m,g])
                            o_cg[m+1::,m,g] = s_cg[m:-1,m,g] - s_cg[m+1::,m,g]
                            
                if NegativeInflowCorrect is True:
                    for m in range(SwitchTime, len(self.t)):  # for all years m, starting at SwitchTime
                        # 1) Determine inflow from mass balance:
                        i0_test = self.s[m] - s_cg[m,:,:].sum()
                        if i0_test < 0:
                            NIC_Flags[m] = i0_test                        
                            Delta = -1 * i0_test # Delta > 0!
                            i_g[m,:] = 0 # Set inflow to 0 and distribute mass balance gap onto remaining cohorts:
                            if s_cg[m,:,:].sum() != 0:
                                Delta_percent = Delta / s_cg[m,:,:].sum() 
                                # Distribute gap equally across all cohorts (each cohort is adjusted by the same %, based on surplus with regards to the prescribed stock)
                                # Delta_percent is a % value <= 100%
                            else:
                                Delta_percent = 0 # stock in this year is already zero, method does not work in this case.
                            # correct for outflow and stock in current and future years
                            # adjust the entire stock AFTER year m as well, stock is lowered in year m, so future cohort survival also needs to decrease.
                            o_cg[m, :,:]    = o_cg[m, :,:]    + (s_cg[m, :,:] * Delta_percent).copy()  # increase outflow according to the lost fraction of the stock, based on Delta_c
                            s_cg[m::,0:m,:] = s_cg[m::,0:m,:] * (1-Delta_percent.copy())               # shrink future description of stock from previous age-cohorts by factor Delta_percent in current AND future years.
                            o_cg[m+1::,:,:] = s_cg[m:-1,:,:] - s_cg[m+1::,:,:]                         # recalculate future outflows
                        
                        else:       
                            for g in range(0,Ng):
                                if SFArrayCombined[m,m,g] != 0: # Else, inflow is 0.
                                    i_g[m,g] = TypeSplit[m,g] * i0_test / SFArrayCombined[m,m,g] # allow for outflow during first year by rescaling with 1/sf[m,m]
                                    # NOTE: The stock-driven method may lead to negative inflows, if the stock development is in contradiction with the lifetime model.
                                    # In such situations the lifetime assumption must be changed, either by directly using different lifetime values or by adjusting the outlfows, 
                                    # cf. the option NegativeInflowCorrect in the method compute_stock_driven_model.
                                    # 2) Add new inflow to stock and determine future decay of new age-cohort
                                s_cg[m::,m,g]   = i_g[m,g] * SFArrayCombined[m::,m,g]
                                o_cg[m,m,g]     = i_g[m,g] * (1 - SFArrayCombined[m,m,g])
                                o_cg[m+1::,m,g] = s_cg[m:-1,m,g] - s_cg[m+1::,m,g]    
                                
                # Add total values of parameter to enable mass balance check:
                self.s_c = s_cg.sum(axis =2)
                self.o_c = o_cg.sum(axis =2)
                self.i   = i_g.sum(axis =1)
                
                return s_cg, o_cg, i_g, NIC_Flags
            
            else:
                # No lifetime distribution specified
                return None, None, None, None
        else:
            # No stock specified
            return None, None, None, None
      
        

#
#
# The end.
#

