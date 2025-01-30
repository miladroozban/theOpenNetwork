class Figures:
    def __init__(self, title, xLabel, yLabel, time_data, hdata, ldata, cdata, vdata):
        self.time_data = time_data
        self.title = title
        self.xLabel = xLabel
        self.yLabel = yLabel
        self.hdata = hdata
        self.ldata = ldata
        self.cdata = cdata

    def fit(self):
        # Check if data for scatter plot is provided
        if self.time_data.any() and self.hdata.any() and self.ldata.any() and self.cdata.any():
            plt.figure(1, figsize=(10, 6)).set_facecolor('lightgrey')
            plt.title(self.title)
            plt.xlabel(self.xLabel)
            plt.ylabel(self.yLabel)
            plt.scatter(self.time_data, self.hdata)
            plt.scatter(self.time_data, self.ldata)
            plt.scatter(self.time_data, self.cdata)
            plt.plot(self.time_data, self.cdata)
            plt.show()
            plt.savefig(self.title, dpi=400)
            print("data applied perfectly")

        elif self.time_data.any() and self.hdata.any() and self.ldata.any() and self.cdata.any():
            plt.figure(2, figsize=(10, 6)).set_facecolor('lightgrey')
            plt.title(self.title)
            plt.xlabel(self.xLabel)
            plt.ylabel(self.yLabel)
            plt.scatter(self.time_data, self.hdata)
            plt.scatter(self.time_data, self.ldata)
            plt.scatter(self.time_data, self.cdata)
            plt.plot(self.time_data, self.cdata)  # Plot the closing prices
            plt.show()
            plt.savefig(self.title, dpi=400)
        else:
            print("You have to provide data for scatter plot")

        # plt.savefig(self.title, dpi=400)

        #
        # elif self.time_data and self.hdata and self.ldata and self.cdata:
        #     plt.figure(1, figsize=(10, 6)).set_facecolor('lightgrey')
        #     plt.title(self.title)
        #     plt.xlabel(self.xLabel)
        #     plt.ylabel(self.yLabel)
        #     plt.scatter(self.time_data, self.hdata)
        #     plt.scatter(self.time_data, self.ldata)
        #     plt.scatter(self.time_data, self.cdata)
        #     plt.plot(self.time_data, self.cdata)  # Plot the closing prices
        #     plt.show()
        #     # plt.savefig(self.title, dpi=400)
        # else:
        #     print("You have to provide data for scatter plot")


price_changes = Figures("Price changes",
                        "Date",
                        "Price",
                        date,
                        hdata=candle_high,
                        ldata=candle_low,
                        cdata=candle_close,
                        vdata=0)
price_changes.fit()
Volume_changes = Figures("Volume changes",
                         "Date",
                         "Volume",
                         date,
                         hdata=candle_high,
                         ldata=candle_low,
                         cdata=candle_close,
                         vdata=candle_volume)
Volume_changes.fit()