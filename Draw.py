import pandas as pd
import mplfinance as mpf


class Draw:
    def __init__(self):
        return

    def draw(self, df):
        """확인용 캔들차트 그리기"""
        pd_df = pd.DataFrame(df)
        pd_df.set_index('Date', inplace=True)
        kwargs = dict(type='candle')
        mc = mpf.make_marketcolors(up='red', down='blue', inherit=True)
        style_final = mpf.make_mpf_style(marketcolors=mc)
        mpf.plot(pd_df, **kwargs, style=style_final)

def draw_check(self, D, H_idx, L_idx, df):
    """방향 업데이트"""
    if D == 0:
        if H_idx > L_idx:
            D = 0
        else:
            if H_idx < L_idx:
                D = 1
            elif H_idx == L_idx:
                D = 2
            # self.draw(df)
        return D

    elif D == 1:
        if H_idx < L_idx:
            D = 1
        else:
            if H_idx > L_idx:
                D = 0
            elif H_idx == L_idx:
                D = 2
            # self.draw(df)
        return D

    elif D == 2:
        if H_idx > L_idx:
            D = 0
            # self.draw(df)
        elif H_idx < L_idx:
            D = 1
            # self.draw(df)
        else:
            D = 2
        return D


def non_draw_check(self, D, H_idx, L_idx):
    """첫번째 데이터 삭제 후 방향 업데이트"""
    if H_idx > L_idx:
        D = 0
    elif H_idx < L_idx:
        D = 1
    else:
        D = 2
    return D