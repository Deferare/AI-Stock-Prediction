


# 캔들 장대 양음봉 판별.
def labeling(S, H, L, E):
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
    # top_t = round(top_t/candle_sum, 5); bottom_t = round(bottom_t/candle_sum, 5);
    body = round(body/candle_sum, 5)

    # 양봉 음봉 판별.
    if up_down_state > 0:
        answer = "U"
    else:
        answer = "D"
    if body >= 1: # body 비중이 100% 넘으면 장대로 봄.
        answer += '1'
    else:
        answer = "-1"
    return answer
