import pandas as pd
import mplfinance as mpf

class Turn:    
    def __init__(self):
        return

    def labeling(self, row_data):
        """캔들 모양 라벨링"""
        S = row_data['Open']
        E = row_data['Close']
        H = row_data['High']
        L = row_data['Low']

        up_down_state = E-S
        if up_down_state > 0:
            body = E-S
            top_t = H - E
            bottom_t = S - L
        else:
            body = S-E
            top_t = H-S
            bottom_t = E-L
        candle_sum = top_t + bottom_t + body

        if candle_sum == 0: # 0으로 나눌 수 없어 1로 변경
            candle_sum = 1

        top_t = round(top_t/candle_sum, 5); bottom_t = round(bottom_t/candle_sum, 5); body = round(body/candle_sum, 5)

        if body < 0.05: # body 비중이 5% 이하면, E 구간.
            if top_t < 0.05: # 동시에 위 꼬리의 비중도 10%가 안되면,
                answer = "E2"
            elif bottom_t < 0.05: # 아래 꼬리의 비중이 10%가 안되면,
                answer = 'E4'
            elif top_t > 0.3 and bottom_t > 0.3: # 위아래 꼬리 둘다 각각 30% 이상의 비중을 차지하면,
                answer = 'E3'
            else: # 그 외.
                answer = 'E1'
        else:
            # 양봉 음봉 판별.
            if up_down_state > 0:
                answer = "U"
            else:
                answer = "D"

            if body > 0.95: # body 비중이 95% 넘으면 장대로 봄.
                answer += '1'
            else:
                if top_t < 0.01: # body 비중이 95%가 안되고 위 꼬리의 비중이 1%가 안될때,
                    if bottom_t < 0.25:
                        answer += '2'
                    elif bottom_t < 0.5:
                        answer += '3'
                    else:
                        answer += '4'
                elif bottom_t < 0.01: # body 비중이 95%가 안되고 아래 꼬리의 비중이 1%가 안될때,
                    if top_t < 0.25:
                        answer += '10'
                    elif top_t < 0.5:
                        answer += '9'
                    else:
                        answer += '8'
                elif body > 0.7: # 위의 조건에 성립 되지 않고, body의 비중이 70%가 넘는다면,
                    answer += '5'
                elif body > 0.5: # body의 비중이 50%가 넘는다면,
                    answer += '6'
                else: # 그 외.
                    answer += '7'
        return answer

    def candle_labeling(self, df):
        """끝에서 두 개 데이터만 인덱싱"""
        df1 = df[-2]
        df2 = df[-1]
        C1 = self.labeling(df1)
        C2 = self.labeling(df2)
        return C1, C2

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

    def turn_check(self, D, H_idx, L_idx, df, test_df, data):
        """반전형 모양인지 확인 후 반전형이면 학습 데이터로 선택"""
        if D == '상승형':
            if H_idx > L_idx:
                D = '상승형'
            else:
                if H_idx < L_idx:
                    D = '하락형'
                elif H_idx == L_idx:
                    D = '직선형'
                C1, C2 = self.candle_labeling(df)
                target = self.result(data, df)
                test_df = test_df.append({'D' : D, 'C1' : C1, 'C2' : C2, 'result' : target}, ignore_index=True)
            return D , test_df

        elif D == '하락형':
            if H_idx < L_idx:
                D = '하락형'
            else:
                if H_idx > L_idx:
                    D = '상승형'
                elif H_idx == L_idx:
                    D = '직선형'
                C1, C2 = self.candle_labeling(df)
                target = self.result(data,df)
                test_df = test_df.append({'D' : D, 'C1' : C1, 'C2' : C2, 'result' : target}, ignore_index=True)
            return D , test_df

        elif D == '직선형':
            if H_idx == L_idx:
                D = '직선형'
            else:
                if H_idx > L_idx:
                    D = '상승형'
                elif H_idx < L_idx:
                    D = '하락형'
                C1, C2 = self.candle_labeling(df)
                target = self.result(data,df)
                test_df = test_df.append({'D' : D, 'C1' : C1, 'C2' : C2, 'result' : target}, ignore_index=True)
            return D , test_df

    def non_turn_check(self, D, H_idx, L_idx):
        """최고가, 최저가 업데이트할 때 변한 방향 설정"""
        if H_idx > L_idx:
            D = '상승형'
        elif H_idx < L_idx:
            D = '하락형'
        else:
            D = '직선형'
        return D