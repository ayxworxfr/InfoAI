from dataclasses import dataclass

import akshare as ak
import pandas as pd
from fund.feishu_msg import send_feishu_msg


class FundDataFetcher:
    def __init__(self):
        self.fund_codes = None
        self.start_date = None
        self.end_date = None
        self.columns_keywords = None
        self.fund_info_df = None

    def _fetch_fund_data(self, fund_code):
        try:
            # 获取指定基金代码的财务信息
            data = ak.fund_financial_fund_info_em(symbol=fund_code)
            data["净值日期"] = pd.to_datetime(data["净值日期"]).dt.strftime("%Y-%m-%d")
            # 日期为空查询最新数据
            if self.start_date:
                data = data[
                    (data["净值日期"] >= self.start_date)
                    & (data["净值日期"] <= self.end_date)
                ]
            else:
                data = data[data["净值日期"] == data["净值日期"].max()]
            # 过滤日期范围
            return data
        except Exception as e:
            print(f"Error fetching data for fund {fund_code}: {e}")
            return pd.DataFrame()

    def set_fund_codes(self, fund_codes):
        if isinstance(fund_codes, str):
            self.fund_codes = [fund_codes]
        elif isinstance(fund_codes, list):
            self.fund_codes = fund_codes
        return self

    def set_date(self, date):
        self.start_date = date
        self.end_date = date
        return self

    def set_date_range(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date
        return self

    def set_columns_keywords(self, keywords):
        if isinstance(keywords, str):
            self.columns_keywords = [keywords]
        elif isinstance(keywords, list):
            self.columns_keywords = keywords
        return self

    def execute(self):
        all_data = []
        if not self.fund_codes:
            print("No fund codes specified.")
            return pd.DataFrame()

        for code in self.fund_codes:
            data = self._fetch_fund_data(code)
            if not data.empty:
                # 为每个基金数据添加基金基本信息
                self.fill_fund_info(data, code)
                all_data.append(data)

        if not all_data:
            print("No data available for the specified fund codes.")
            return pd.DataFrame()

        # 合并所有基金的数据
        result_data = pd.concat(all_data, ignore_index=True)
        return result_data

    def get_fund_list(self, fund_codes=None, fund_names=None, fund_types=None):
        # 使用 AkShare 获取基金基本信息
        fund_df = ak.fund_name_em()
        # 选择需要的列
        fund_df = fund_df[["基金代码", "基金简称", "基金类型"]]
        # 过滤基金, 构建布尔索引
        conditions = []
        if fund_codes:
            conditions.append(fund_df["基金代码"].isin(fund_codes))
        if fund_names:
            conditions.append(
                fund_df["基金简称"].str.contains(
                    "|".join(fund_names), case=False, na=False
                )
            )
        if fund_types and "基金类型" in fund_df.columns:
            conditions.append(
                fund_df["基金类型"].str.contains(
                    "|".join(fund_types), case=False, na=False
                )
            )
        # 如果有条件，使用"或"操作符组合条件
        if conditions:
            combined_condition = conditions[0]
            for condition in conditions[1:]:
                combined_condition |= condition
            fund_df = fund_df[combined_condition]
        return fund_df

    def fill_fund_info(self, data, code: str):
        # 获取基金基本信息
        if self.fund_info_df is None:
            self.fund_info_df = self.get_fund_list(fund_codes=self.fund_codes)
        fund_info = self.fund_info_df[self.fund_info_df["基金代码"] == code]
        if not fund_info.empty:
            # 添加到前面
            data.insert(0, "基金简称", fund_info["基金简称"].values[0])
            data.insert(0, "基金代码", code)
            data["基金代码"] = code


@dataclass
class MonitorMsg:
    fund_code: str
    fund_name: str
    net_value_date: str
    daily_growth_rate: float
    unit_net_value: float

    def to_dict(self):
        return {
            "fund_code": self.fund_code,
            "fund_name": self.fund_name,
            "net_value_date": self.net_value_date,
            "daily_growth_rate": self.daily_growth_rate,
            "unit_net_value": self.unit_net_value,
        }

    @staticmethod
    def build_columns():
        return [
            {
                "name": "fund_code",
                "display_name": "基金代码",
                "data_type": "text",
                "width": "auto",
                "horizontal_align": "center",
            },
            {
                "name": "fund_name",
                "display_name": "基金名称",
                "data_type": "text",
                "width": "auto",
                "horizontal_align": "left",
            },
            {
                "name": "net_value_date",
                "display_name": "净值日期",
                "data_type": "text",
                "width": "auto",
                "horizontal_align": "left",
            },
            {
                "name": "daily_growth_rate",
                "display_name": "日增长率(%)",
                "data_type": "number",
                "width": "auto",
                "horizontal_align": "left",
            },
            {
                "name": "unit_net_value",
                "display_name": "单位净值",
                "data_type": "number",
                "width": "auto",
                "horizontal_align": "left",
            },
        ]

    @staticmethod
    def to_rows(monitor_msgs):
        rows = [msg.to_dict() for msg in monitor_msgs]
        return rows

    @staticmethod
    def construct_monitor_msgs(df, threshold=0, check_date=None):
        monitor_msgs = []

        # 日增长改为float类型, 考虑空值情况
        for _, row in df.iterrows():
            daily_growth_rate = row["日增长率"]
            if not daily_growth_rate or (check_date and row["净值日期"] != check_date):
                print(f"Skipping row: {row}")
                continue

            daily_growth_rate = float(daily_growth_rate)
            # 检查日增长率是否超过 threshold
            if abs(daily_growth_rate) >= threshold:
                msg = MonitorMsg(
                    fund_code=row["基金代码"],
                    fund_name=row["基金简称"],
                    net_value_date=row["净值日期"],
                    daily_growth_rate=daily_growth_rate,
                    unit_net_value=row["单位净值"],
                )
                monitor_msgs.append(msg)

        return monitor_msgs


def query_daily_info():
    fetcher = FundDataFetcher()
    fund_codes = init_fund_codes()

    # 查询特定日期的数据
    result_specific_date = (
        fetcher.set_fund_codes(fund_codes)
        .set_date("2024-10-10")  # 查询单一天的数据
        .set_columns_keywords(["单位净值", "日增长率", "累计净值"])
        .execute()
    )
    print("Specific Date Result:")
    print(result_specific_date)

    # 查询最新的数据
    fetcher = FundDataFetcher()  # 重新实例化以清除之前的设置
    result_latest_data = (
        fetcher.set_fund_codes(fund_codes)
        .set_columns_keywords(["单位净值", "日增长率", "累计净值"])
        .execute()
    )
    print("Latest Data Result:")
    print(result_latest_data)


def query_fund_list():
    fetcher = FundDataFetcher()
    # fund_list = fetcher.get_fund_list(fund_names=['招商', '华夏'])
    fund_list = fetcher.get_fund_list(
        fund_codes=["007844"],
        fund_names=[
            "华夏鼎茂债券C",
            "中信建投稳祥C",
            "广发双债",
            "华宝标普油气上游股票人民币C",
        ],
    )
    print("Fund List:")
    print(fund_list)


def init_fund_codes() -> list:
    fund_codes = ["004043", "380006", "003979", "161716", "009267"]
    stock_fund_codes = ["007844", "007722", "018044"]
    fund_codes.extend(stock_fund_codes)
    return fund_codes


def monitor():
    # 查询最新的数据
    fetcher = FundDataFetcher()
    fund_codes = init_fund_codes()
    result_latest_data = (
        fetcher.set_fund_codes(fund_codes)
        .set_columns_keywords(["单位净值", "日增长率", "累计净值"])
        .execute()
    )
    print("Latest Data Result:")
    print(result_latest_data)

    # 构建监控消息
    monitor_msgs = MonitorMsg.construct_monitor_msgs(result_latest_data)
    columns = MonitorMsg.build_columns()
    rows = MonitorMsg.to_rows(monitor_msgs)
    print(f"Monitor Messages: {rows}")
    send_feishu_msg(columns=columns, rows=rows, title="每日基金监控")
    if len(monitor_msgs) == 0:
        return

    monitor_msgs = MonitorMsg.construct_monitor_msgs(result_latest_data, threshold=0.1)
    columns = MonitorMsg.build_columns()
    rows = MonitorMsg.to_rows(monitor_msgs)
    send_feishu_msg(columns=columns, rows=rows, title="基金波动监控")


if __name__ == "__main__":
    # query_fund_list()
    # query_daily_info()
    monitor()
