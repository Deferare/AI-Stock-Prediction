import pandas as pd
import mplfinance as mpf
import time


class Turn:
    def __init__(self):
        return

    def save(self, df, i, target):
        i += 1
        rc = {
            "axes.labelcolor": "none",
            "axes.spines.bottom": False,
            "axes.spines.left": False,
            "axes.spines.right": False,
            "axes.spines.top": False,
            "font.size": 0,
            "xtick.color": "none",
            "ytick.color": "none",
            "figure.facecolor": "none",
        }
        df = pd.DataFrame(df)
        df.set_index('Date', inplace=True)
        kwargs = dict(type='candle')
        mc = mpf.make_marketcolors(up='red', down='blue', inherit=True)
        style_final = mpf.make_mpf_style(marketcolors=mc, rc=rc)
        mpf.plot(df, **kwargs, style=style_final, savefig=f"./img/{target}/{i}.png")
        return i

    def result(self, data, df):
        """다음 데이터 결과"""
        last_data = df[-1]
        if last_data['Close'] < data['Close']:
            target = '상승'
        elif last_data['Close'] > data['Close']:
            target = '하락'
        else:
            target = '보합'
        return target

    def turn_check(self, D, H_idx, L_idx, df, data, i):
        """반전형 모양인지 확인 후 반전형이면 학습 데이터로 선택"""
        if D == '상승형':
            if H_idx > L_idx:
                D = '상승형'
            else:
                if H_idx < L_idx:
                    D = '하락형'
                elif H_idx == L_idx:
                    D = '직선형'
                target = self.result(data, df)
                i = self.save(df, i, target)
            return D, i

        elif D == '하락형':
            if H_idx < L_idx:
                D = '하락형'
            else:
                if H_idx > L_idx:
                    D = '상승형'
                elif H_idx == L_idx:
                    D = '직선형'
                target = self.result(data, df)
                i = self.save(df, i, target)
            return D, i

        elif D == '직선형':
            if H_idx == L_idx:
                D = '직선형'
            else:
                if H_idx > L_idx:
                    D = '상승형'
                elif H_idx < L_idx:
                    D = '하락형'
                target = self.result(data, df)
                i = self.save(df, i, target)
            return D, i

    #############################################################################################
    # 실시간 데이터 확인
    def turn_check2(self, D, H_idx, L_idx, df, code):
        """반전형 모양인지 확인 후 반전형이면 학습 데이터로 선택"""
        if D == '상승형':
            if H_idx > L_idx:
                D = '상승형'
            else:
                if H_idx < L_idx:
                    D = '하락형'
                elif H_idx == L_idx:
                    D = '직선형'
                self.save2(df, code)
            return

        elif D == '하락형':
            if H_idx < L_idx:
                D = '하락형'
            else:
                if H_idx > L_idx:
                    D = '상승형'
                elif H_idx == L_idx:
                    D = '직선형'
                self.save2(df, code)
            return

        elif D == '직선형':
            if H_idx == L_idx:
                D = '직선형'
            else:
                if H_idx > L_idx:
                    D = '상승형'
                elif H_idx < L_idx:
                    D = '하락형'
                self.save2(df, code)
            return

    def save2(self, df, code):
        rc = {
            "axes.labelcolor": "none",
            "axes.spines.bottom": False,
            "axes.spines.left": False,
            "axes.spines.right": False,
            "axes.spines.top": False,
            "font.size": 0,
            "xtick.color": "none",
            "ytick.color": "none",
            "figure.facecolor": "none",
        }
        df = pd.DataFrame(df)
        df.set_index('Date', inplace=True)
        kwargs = dict(type='candle')
        mc = mpf.make_marketcolors(up='red', down='blue', inherit=True)
        style_final = mpf.make_mpf_style(marketcolors=mc, rc=rc)
        tm = time.localtime()
        mpf.plot(df, **kwargs, style=style_final, savefig=f"./test/{code}_{tm.tm_hour}:{tm.tm_min}.png")

    def non_turn_check(self, D, H_idx, L_idx):
        """최고가, 최저가 업데이트할 때 변한 방향 설정"""
        if H_idx > L_idx:
            D = '상승형'
        elif H_idx < L_idx:
            D = '하락형'
        else:
            D = '직선형'
        return D