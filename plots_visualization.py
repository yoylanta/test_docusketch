import pandas as pd
import matplotlib.pyplot as plt


class DrawPlots:
    "Base class for drawing plots."

    def __init__(self, url):
        self.url = url
        self.df = pd.read_json(url)

    def _create_hist(self, series, name, logy, show_mean, show_std):
        ax = series.hist(log=logy, figsize=(12, 8), alpha=0.5, bins=50, grid=False)
        
        mean = series.mean()
        std = series.std()
        
        # mean line
        if show_mean: ax.axvline(x=mean, color = 'r', linestyle = '-')
    
        # std lines
        if show_std:
            ax.axvline(x = mean-std, color = 'r', linestyle = ':')
            ax.axvline(x = mean+std, color = 'r', linestyle = ':')
            ax.legend([f"mean: {round(mean, 2)}", f"std:     {round(std, 2)}"], loc="upper right", ncol=1)
        
        ax.legend([f"mean: {round(mean, 2)}"], loc="upper right", ncol=1)
        
        if logy:
            ax.set_title(name + " (log scale)")
        else:
            ax.set_title(name)
            
        return ax.figure

    def save_hist(self, series, name, path, logy=False, show_mean=True, show_std=True):
        plt.figure()
        self._create_hist(series, name, logy=logy, show_mean=show_mean, show_std=show_std).savefig(f"{path}/{name}.png")
        plt.close()


class DrawDeviation(DrawPlots):
    def __init__(self, url):
        super().__init__(url)

       # Setting all the objects that we re going to examine in a special dictionary to avoid repetitive code constructions in the future.
        self.series = {
            "min_diff":     self.df["floor_min"] - self.df["ceiling_min"],
            "max_diff":     self.df["floor_max"] - self.df["ceiling_max"],
            "mean_diff":    self.df["floor_mean"] - self.df["ceiling_mean"],
            "mean":         self.df["mean"],
            "ceiling_mean": self.df["ceiling_mean"],
            "floor_mean":   self.df["floor_mean"]
        }

    def show_hist(self, key, logy=False, show_mean=True, show_std=True):
        """Draws a histogram based on one of the keys: min_diff, max_diff, mean_diff, mean, ceiling_mean, floor_mean."""
        self._create_hist(self.series[key], name=key, logy=logy, show_mean=show_mean, show_std=show_std)

    def draw_plots(self, path):
        for key, value in self.series.items():
            self.save_hist(value, key, path)

        