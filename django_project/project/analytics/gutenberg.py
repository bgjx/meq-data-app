import numpy as np
import pandas as pd
from scipy.stats import linregress
from typing import Dict, Any

def gutenberg_analysis(magnitude: pd.Series, bin_width: float = 0.1) -> Dict[str, Any]:
    """
    Perform Gutenberg-Richter analysis on a given series of earthquake magnitudes.
    
    This function implements the Gutenberg-Richter law to analyze the distribution of earthquake 
    magnitudes. It computes cumulative and non-cumulative counts, fits a line to the cumulative counts,
    and identifies a breakpoint for better fitting.

    Parameters:
    magnitude (pd.Series): A pandas Series containing earthquake magnitudes.
    bin_width (float): The width of the bins to use for histogram calculation. Default is 0.1.

    Returns:
    Dict[str, Any]: A dictionary containing the results of the analysis, including:
        - 'b_value': The slope of the fitted line (negative value as per Gutenberg-Richter).
        - 'a_value': The intercept of the fitted line.
        - 'b_value_stderr': Standard error of the slope.
        - 'r_squared': R-squared value of the fit indicating goodness of fit.
        - 'mc': Tuple containing the breakpoint magnitude and corresponding fitted log cumulative count.
        - 'cumulative': Dictionary with keys 'x' and 'y' for the x and y values of the cumulative counts.
        - 'non_cumulative': Dictionary with keys 'x' and 'y' for the x and y values of the non-cumulative counts.
        - 'fitted_line': Dictionary with keys 'x' and 'y' for the x and y values of the fitted line.
    """

    min_magnitude = np.round(np.floor(magnitude.min() / bin_width) * bin_width, 3)
    max_magnitude = np.round(np.ceil(magnitude.max() / bin_width) * bin_width, 3)

    filtered_magnitudes = magnitude[magnitude >= min_magnitude]
    mag_bins = np.round(np.arange(min_magnitude, (max_magnitude + bin_width), bin_width), 3)

    cumulative_counts = np.array([len(filtered_magnitudes[filtered_magnitudes >= m]) for m in mag_bins])
    non_cumulative_counts, _ = np.histogram(filtered_magnitudes, bins=mag_bins)

    mag_bins_non_cum = mag_bins[:-1] + bin_width / 2

    valid_count_indices_cum = [i for i, c in enumerate(cumulative_counts) if c > 0]
    valid_count_indices_non_cum = [i for i, c in enumerate(non_cumulative_counts) if c > 0]

    if len(valid_count_indices_cum) < 5:
        return {}
    
    mag_bins_cum = mag_bins[valid_count_indices_cum]
    cumulative_counts = cumulative_counts[valid_count_indices_cum]
    log_cumulative_counts = np.log10(cumulative_counts)

    mag_bins_non_cum = mag_bins_non_cum[valid_count_indices_non_cum]
    non_cumulative_counts = non_cumulative_counts[valid_count_indices_non_cum]
    log_non_cumulative_counts = np.log10(non_cumulative_counts)

    best = {
        "r_squared": 0
    }

    for i in range(1, len(mag_bins_cum) // 2):
        breakpoint = mag_bins_cum[i]
        mask = mag_bins_cum >= breakpoint
        x_subset = mag_bins_cum[mask]
        y_subset = log_cumulative_counts[mask]

        if len(x_subset) < 2:
            continue

        slope, intercept, r_value, _, std_err = linregress(x_subset, y_subset)
        
        if r_value ** 2 > best["r_squared"]:
            best.update({
                'breakpoint': breakpoint,
                'slope': slope,
                'intercept': intercept,
                'r_squared': r_value**2,
                'index': i,
                'std_err': std_err
            })
        
    fit_log_cumulative = (best['slope'] * mag_bins_cum) + best['intercept']
    mc = (best['breakpoint'], fit_log_cumulative[best['index']])

    return {
        'b_value': -1 *  best['slope'],
        'a_value': best['intercept'],
        'b_value_stderr': best['std_err'],
        'r_squared': best['r_squared'],
        'mc': mc,
        'cumulative': {
            'x': mag_bins_cum.tolist(),
            'y': log_cumulative_counts.tolist()
        },
        'non_cumulative': {
            'x': mag_bins_non_cum.tolist(),
            'y': log_non_cumulative_counts.tolist()
        },
        'fitted_line': {
            'x': mag_bins_cum.tolist(),
            'y': fit_log_cumulative.tolist()
        }
    }
