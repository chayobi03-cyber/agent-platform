# 투자 프로젝트 — 다음 세션 프롬프트

## 세션 목적
현재 확정된 `Market Regime Engine V1`을 실제 데이터 기반의 종목 선별 엔진으로 연결한다.
오늘 만든 임시/수동 랭킹은 참고자료로만 사용하고, 임의의 숫자 생성이나 사후 조정을 하지 않는다.

## 1. 기준 프레임 고정
시장 상태는 다음 순서를 따른다.

```text
원시 데이터
→ 정규화(0~100)
→ Trend / Breadth / Risk / Macro / Cross-Asset
→ Market Score
→ Stress Override
→ Regime(R1~R6)
```

시장·섹터·종목은 분리한다.

```text
MarketScore → 시장 전체 환경
SectorScore → 섹터 상대강도/환경
StockScore  → 개별 종목 상태
BuyStrength → 실제 매수 우선순위
```

기준 문서: `docs/investment/MARKET_REGIME_ENGINE_V1.md`

## 2. 다음 세션 최우선 작업
### A. 데이터 연결 가능성 조사
다음 데이터를 현재 시점 기준으로 실제 확보 가능한 출처부터 정리한다.

- KRX 종목 OHLCV / 거래량
- KRX 시장 breadth
- 섹터별 가격 및 상대강도
- 외국인/기관 수급
- 미국: S&P 500, SOX, VIX, VIX3M, HY OAS, DXY, 금리
- USD/KRW
- Gold, WTI, BTC
- 기업: 매출/영업이익/EPS/FCF/부채/밸류에이션
- 이벤트/실적/가이던스 등 Catalyst

가능하면 1차 자료 및 공식 데이터 제공원을 우선한다.

### B. Stock Score 명세 확정
종목별 다음 축을 별도로 계산한다.

```text
Long Score
Medium Score
Short Score
```

권장 기본 가중치:

```text
Long   = 50%
Medium = 30%
Short  = 20%
```

단, 이 가중치는 백테스트 전까지 고정된 운영 가정으로 취급하고 최적화하지 않는다.

### C. Stock Score 구성
최소한 다음 요소를 분리한다.

```text
Trend / Momentum
Earnings / Fundamental
Valuation
Relative Strength
Supply / Demand
Institutional-Foreign Flow
Sector Strength
Market Regime
Catalyst
Risk / Drawdown
```

중복 설명변수와 이중계산을 점검한다.

### D. BuyStrength 확정
기본 구조는 다음을 출발점으로 사용한다.

```text
BuyStrength
= 0.40*Stock
+ 0.25*Sector
+ 0.25*Market
+ 0.10*Catalyst
```

실제 데이터 연결 후 각 항목의 내부 구성과 시간축 집계 방법을 명확히 정의한다.

## 3. 시간축별 질문
각 종목마다 반드시 다음 질문에 답한다.

### 장기
- 1년 이상 보유할 구조적 이유가 있는가?
- 이익 성장과 ROIC/FCF가 유지되는가?
- 밸류에이션이 장기 기대수익률을 훼손하지 않는가?
- 장기 추세와 200DMA가 유효한가?

### 중기
- 1~6개월 상대강도와 실적 모멘텀이 상승하는가?
- 기관/외국인 수급이 개선되는가?
- 섹터 리더십이 강화되는가?

### 단기
- 5~20일 모멘텀이 유효한가?
- 과매수/추격매수 위험은 어느 정도인가?
- 최근 급등 후 진입 위치가 불리하지 않은가?
- 단기 손절/무효화 조건이 명확한가?

## 4. 종목 선정 Universe
우선 다음 종목부터 계산한다.

```text
삼성전자
SK하이닉스
삼성SDI
KB금융
현대차
삼성화재
SK이노베이션
두산에너빌리티
NAVER
삼성바이오로직스
```

이후 필요하면 KOSPI/KOSDAQ 대형주 전체로 확장한다.

## 5. 출력 형식
최종 출력은 반드시 다음 표를 포함한다.

| Rank | 종목 | 장기 | 중기 | 단기 | 종합 | Sector | Market | Catalyst | Risk | BuyStrength | Action |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|

Action은 최소 다음 중 하나로 제한한다.

```text
강한 매수
분할매수
눌림목 매수
보유
관망
매수 금지
```

그리고 각 종목에 대해 **왜 그 점수가 나왔는지 핵심 근거 2~3개**를 제시한다.

## 6. 중요한 운영 규칙

1. 실시간 데이터가 필요한 질문은 반드시 최신 데이터를 검색한다.
2. 데이터가 없는 경우 추정값을 실제값처럼 쓰지 않는다.
3. 장중 데이터와 장 마감 데이터를 구분한다.
4. 종목 점수와 시장 점수를 혼동하지 않는다.
5. 급등률 하나만으로 매수 순위를 높이지 않는다.
6. Market Score가 좋더라도 개별 종목 위험이 크면 매수를 제한할 수 있다.
7. Score와 Risk Alarm을 별도로 표시한다.
8. 데이터 시점(t) 이후 정보를 의사결정에 사용하지 않는다.
9. rolling percentile은 해당 시점까지의 과거 데이터만 사용한다.
10. 가중치 변경은 백테스트/OOS 검증 이전에는 하지 않는다.
11. 모든 중요한 결론에는 근거 데이터와 출처를 남긴다.

## 7. 검증
실제 계산 엔진이 완성되면 다음을 검증한다.

- Market Score quintile별 미래 20/60/120D 수익률
- R1~R6별 수익률/승률/MDD
- Long/Medium/Short Score의 예측력
- BuyStrength quintile별 미래수익률
- Parameter sensitivity
- Walk-Forward
- PBO / CSCV
- Deflated Sharpe Ratio
- Randomization / permutation test
- Regime persistence / false transition
- Turnover / 실행가능성

목표는 최고의 파라미터가 아니라 **파라미터 변화에도 효과가 유지되는 견고성**을 확인하는 것이다.

## 8. 오늘 세션에서 이어받을 핵심 레슨런

- 시장점수와 종목점수는 분리해야 한다.
- 장기/중기/단기 점수를 따로 계산해야 단순한 급등 추격을 방지할 수 있다.
- 현재 보유 종목이 있는 경우 신규 매수 우선순위와 절대적인 종목 랭킹은 다를 수 있다.
- 가격 모멘텀만으로 판단하지 말고 Sector / Market / Catalyst / Risk를 함께 반영한다.
- 데이터가 실제로 연결되지 않은 상태에서는 정교한 숫자를 만들어내지 않는다.

## 9. 세션 종료 규칙
세션 종료 시 반드시:

```text
결과 요약
→ 새로 확인된 문제
→ 레슨런
→ 재사용할 규칙 변경 필요성 검토
→ Git 저장 필요 여부 검토
```

재사용 가능한 규칙은 적절한 운영 문서에 반영한다.
Git 저장이 필요하다고 판단되면 별도 확인을 묻지 않고 바로 commit한다.
