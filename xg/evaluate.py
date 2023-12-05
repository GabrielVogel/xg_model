import matplotlib.pyplot as plt
from sklearn.calibration import CalibrationDisplay


def plot_calibration_curve(ytrue,ypred,nbins=20):
    """Given ytrue and predicted probabilites, show calibration plot with given bins."""
    disp = CalibrationDisplay.from_predictions(ytrue, ypred,n_bins=nbins)
    disp.plot()
    

