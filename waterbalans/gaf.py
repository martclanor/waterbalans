"""This file contains the polder class

"""

from collections import OrderedDict
import numpy as np
import pandas as pd
from .eag import Eag


class Gaf:
    """The Gaf class is the main object for a waterbalance.

    Parameters
    ----------
    id: int
        Integer id for the Gaf.

    Notes
    -----
    Gebieden-AfvoerGebieden

    """

    def __init__(self, id=None, name=None, eags=[], series=None):
        # Basic information
        self.id = id
        self.name = name

        # EAG
        self.eags = OrderedDict()

        for e in eags:
            if isinstance(e, Eag):
                self.eags[e.name] = e
            else:
                print("Warning! added Eags must be instance of Eag object.")

        self.data = pd.DataFrame()
        self.parameters = pd.DataFrame()

        if series is None:
            self.series = pd.DataFrame()
        else:
            self.series = series

    def add_eag(self, eag):
        self.eags[eag.name] = eag

    def add_series(self, series, tmin="2000", tmax="2015", freq="D",
                   fillna=False):
        for eagname, eag in self.eags.items():
            eagseries = series.loc[series.EAGCode == eagname, :]
            eag.add_series(eagseries, tmin=tmin, tmax=tmax,
                           freq=freq, fillna=fillna)

    def add_eag_series(self, series, name=None, tmin="2000", tmax="2015", freq="D",
                       fillna=False, method=None):
        """Method to add series directly to EAG. Series must contain volumes (so 
        not divided by area). Series must be negative for water taken out of the 
        EAG and positive for water coming into the EAG.

        Parameters
        ----------
        series: pandas.DataFrame or pandas.Series
        name: str, default None
            name of series to add, if not provided uses 
            first column name in DataFrame or Series name
        tmin: str or pandas.Timestamp, optional
        tmax: str or pandas.Timestamp, optional
        freq: str

        """
        if self.series.index.shape[0] == 0:
            self.series = pd.DataFrame(index=pd.date_range(pd.Timestamp(tmin),
                                                           pd.Timestamp(tmax), freq="D"))

        if name is None:
            if isinstance(series, pd.DataFrame):
                name = series.columns[0]
            elif isinstance(series, pd.Series):
                name = series.name

        if fillna:
            if (series.isna().sum() > 0).all():
                print("Filled {0} NaN-values with '{1}' in series {2}.".format(
                    np.int(series.isna().sum()), method, name))
                if isinstance(method, str):
                    series = series.fillna(method=method)
                elif isinstance(method, float) or isinstance(method, int):
                    series = series.fillna(method)

        if name in self.series.columns:
            print(
                "Warning! Series {} already present in EAG, overwriting data!".format(name))

        self.series.loc[series.index.intersection(
            self.series.index), name] = series.loc[series.index.intersection(self.series.index)].values.squeeze()

    def simulate(self, parameters, tmin=None, tmax=None):
        """Method to calculate the waterbalance for the Gaf.

        """
        for eagname, eag in self.eags.items():
            eag.get_series_from_gaf()
            params = parameters.loc[parameters.EAGCode == eagname, :]
            eag.simulate(params, tmin=tmin, tmax=tmax)

    def get_eags(self):
        return [e for e in self.eags.values()]
