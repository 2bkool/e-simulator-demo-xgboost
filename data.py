import pandas as pd
# from workalendar.asia import SouthKorea


DATA_DIR = './datas'
TARGET_KEY = 'target'


def get_dataframe():
    # cal = SouthKorea()

    df = pd.read_csv(f'{DATA_DIR}/preprocessed.csv', index_col=[0],
                     parse_dates=[0], encoding='euc-kr')

    # df['년'] = df.index.year
    # df['월'] = df.index.month
    # df['week'] = df.index.week
    # df['일'] = df.index.day
    # df['요일'] = df.index.dayofweek
    # df['주차'] = df.index.weekofyear
    # df['휴일'] = df.index.map(lambda x: 1 if(cal.is_holiday(x)) else 0)
    #
    # # 대체 공유일 재 설정
    # df.at['2018-01-01', '휴일'] = 1
    # df['2018-02-15': '2018-02-17']['휴일'] = 1
    # df.at['2018-03-01', '휴일'] = 1
    # df.at['2018-05-07', '휴일'] = 1
    # df.at['2018-05-22', '휴일'] = 1
    # df.at['2018-06-06', '휴일'] = 1
    # df.at['2018-06-13', '휴일'] = 1   # 지방선거
    # df.at['2018-08-15', '휴일'] = 1
    # df['2018-09-23': '2018-09-26']['휴일'] = 1
    # df.at['2018-10-03', '휴일'] = 1
    # df.at['2018-10-09', '휴일'] = 1
    # df.at['2018-12-25', '휴일'] = 1
    #
    # df.at['2019-01-01', '휴일'] = 1
    # df['2019-02-05': '2018-02-06']['휴일'] = 1
    # df.at['2019-03-01', '휴일'] = 1
    # df.at['2019-05-06', '휴일'] = 1
    # df.at['2019-05-12', '휴일'] = 1
    # df.at['2019-06-06', '휴일'] = 1
    # df.at['2019-08-15', '휴일'] = 1
    # df['2019-09-12': '2019-09-14']['휴일'] = 1
    # df.at['2019-10-03', '휴일'] = 1
    # df.at['2019-10-09', '휴일'] = 1
    # df.at['2019-12-25', '휴일'] = 1
    #
    # df.at['2020-01-01', '휴일'] = 1
    # df['2020-01-24': '2020-01-27']['휴일'] = 1
    # df['holiday'] = df.index.map(lambda x: cal.is_holiday(x))
    # df = pd.get_dummies(df, columns=['holiday'])
    # df.to_csv('./aaaaa.csv')
    print(df.describe())
    return df
