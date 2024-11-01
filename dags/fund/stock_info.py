import akshare as ak
import pandas as pd

class StockDataFetcher:
    def __init__(self):
        self.stock_codes = None
        self.stock_info_df = None

    def set_stock_codes(self, stock_codes):
        """设置需要查询的股票代码"""
        if isinstance(stock_codes, str):
            self.stock_codes = [stock_codes]
        elif isinstance(stock_codes, list):
            self.stock_codes = stock_codes
        else:
            raise ValueError("Stock codes should be a string or a list of strings.")
        return self

    def fetch_realtime_stock_data(self):
        """获取指定股票代码的实时行情数据，并补充股票简称"""
        if not self.stock_codes:
            print("No stock codes specified.")
            return pd.DataFrame()

        try:
            # 使用 AkShare 获取所有 A 股的实时行情数据
            all_realtime_data = ak.stock_zh_a_spot()
            # 筛选出我们需要的股票代码
            filtered_data = all_realtime_data[all_realtime_data['代码'].isin(self.stock_codes)]
            if filtered_data.empty:
                print("No real-time data available for the specified stock codes.")
                return pd.DataFrame()

            # 填充股票简称
            filtered_data = self.fill_stock_info(filtered_data)

            # 选择需要的列
            return filtered_data[['代码', '股票简称', '最新价', '今开', '涨跌幅']]

        except Exception as e:
            print(f"Error fetching real-time stock data: {e}")
            return pd.DataFrame()

    def fill_stock_info(self, data):
        """补充股票的基本信息，包括股票简称"""
        if self.stock_info_df is None:
            self.stock_info_df = self.get_stock_list()

        # 合并股票信息
        data = data.merge(self.stock_info_df[['股票代码', '股票简称']], on='股票代码', how='left')
        # 移动股票简称到股票代码的下一列
        data = data[['股票代码', '股票简称'] + [col for col in data.columns if col not in ['股票代码', '股票简称']]]
        return data

    def get_stock_list(self):
        """获取所有股票的基本信息"""
        try:
            stock_info = ak.stock_info_a_code_name()
            stock_info.rename(columns={'code': '股票代码', 'name': '股票简称'}, inplace=True)
            return stock_info
        except Exception as e:
            print(f"Error fetching stock list: {e}")
            return pd.DataFrame()

    def fetch_historical_stock_data(self, start_date, end_date, adjust='qfq'):
        """获取指定股票代码的历史行情数据"""
        if not self.stock_codes:
            print("No stock codes specified.")
            return pd.DataFrame()

        all_historical_data = pd.DataFrame()

        for code in self.stock_codes:
            try:
                # 获取历史数据
                historical_data = ak.stock_zh_a_hist(symbol=code, start_date=start_date, end_date=end_date, adjust=adjust)
                all_historical_data = pd.concat([all_historical_data, historical_data], ignore_index=True)

            except Exception as e:
                print(f"Error fetching historical data for stock {code}: {e}")

        all_historical_data = self.fill_stock_info(all_historical_data)

        return all_historical_data

if __name__ == '__main__':
    fetcher = StockDataFetcher()
    fetcher.set_stock_codes(['000001', '600519'])  # 设置股票代码

    # 获取实时股票信息
    realtime_data = fetcher.fetch_realtime_stock_data()
    print("Real-time Data:")
    print(realtime_data)

    # 获取历史股票信息
    historical_data = fetcher.fetch_historical_stock_data(start_date='20241011', end_date='20241021')
    print("\nHistorical Data:")
    print(historical_data)


