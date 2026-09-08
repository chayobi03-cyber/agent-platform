# Market Regime Engine V1

## 목적
시장 상태를 `원시 데이터 → 정규화(0~100) → 5개 축 점수 → 종합 Market Score → Stress Override → Regime(R1~R6)` 순서로 계산 가능한 형태로 정의한다.

핵심 원칙은 모든 축에서 **점수가 높을수록 시장에 유리한 상태**가 되도록 방향을 통일하는 것이다.

## 1. 5개 축

### 1) Trend
Core indicators:
- 20D Return
- 60D Return
- 120D Return
- Price / MA200 - 1
- MA20/MA60/MA200 alignment + MA200 slope
- 52W drawdown

Score:
```text
Trend = 0.20*S20 + 0.20*S60 + 0.20*S120 + 0.20*SMA200
      + 0.10*SAlignment + 0.10*SDrawdown
```

수익률과 200DMA 위치는 기본적으로 최근 5년 rolling percentile(1260 trading days)로 0~100 정규화한다.

### 2) Breadth
Core indicators:
- Advance percentage
- Advance/Decline Ratio
- % stocks above 50DMA
- % stocks above 200DMA
- New Highs - New Lows

Score:
```text
Breadth = 0.15*AdvPct + 0.15*ADR + 0.20*PctAbove50
        + 0.30*PctAbove200 + 0.20*NHNL
```

200DMA 위 종목 비율에 가장 높은 가중치를 둔다.

### 3) Risk
Core indicators:
- VIX
- VIX3M - VIX term structure
- 20D realized volatility
- HY OAS
- Equity drawdown

위험지표는 낮을수록 좋은 상태이므로 역 percentile을 사용한다.
예: `VIXScore = 100 - PercentileRank(VIX)`.

Score:
```text
Risk = 0.25*VIX + 0.20*Term + 0.20*RV
     + 0.25*HY + 0.10*DD
```

### 4) Macro
시장 스트레스와 중복되지 않도록 자금조달/유동성 환경에 집중한다.

Core indicators:
- 10Y - 2Y
- Real yield
- DXY
- Short-rate / SOFR condition
- Financial Conditions

Score:
```text
Macro = 0.20*Curve + 0.25*RealYield + 0.20*DXY
      + 0.15*ShortRate + 0.20*FinancialCondition
```

HY OAS는 Risk 축의 Core로만 사용하여 이중계산을 피한다.

### 5) Cross-Asset
Core indicators:
- S&P 500 20D return
- SOX 20D return
- USD/KRW change (원화 강세가 긍정)
- Gold risk signal
- WTI 20D return
- BTC 20D return

Score:
```text
CrossAsset = 0.30*SPX + 0.20*SOX + 0.15*FX
           + 0.10*GoldRisk + 0.10*WTI + 0.15*BTC
```

금과 유가는 단순히 상승=악화로 매핑하지 않고 Risk-On/Risk-Off 맥락으로 별도 정규화한다.

## 2. 정규화 원칙

절대 임계값은 보조 규칙으로만 사용하고, 기본 점수는 rolling percentile 중심으로 계산한다.

- 기본 window: 5년 = 1260 trading days
- 높은 값이 긍정이면 `PercentileRank`
- 높은 값이 부정이면 `100 - PercentileRank`
- 분포 기반 score의 시대 의존성을 줄이기 위해 고정 절대값에 대한 의존을 최소화한다.

경제적으로 의미가 명확한 극단값은 Score와 별도의 `Stress Flag`로 관리한다.

## 3. 종합 Market Score

```text
MarketScore = 0.25*Trend + 0.20*Breadth + 0.20*Risk
            + 0.20*Macro + 0.15*CrossAsset
```

V1에서는 이 가중치를 고정하고, 백테스트 이후에만 변경한다.

## 4. Stress Override

평균점수의 희석으로 극단적 위험을 놓치지 않도록 Regime보다 먼저 평가한다.

대표 규칙:
```text
if VIX >= 35 and HY_OAS >= 500:
    Regime = R6
elif PctAbove200 <= 20%:
    Regime <= R5
elif MarketDrawdown <= -20% and VIX >= 30:
    Regime <= R5
```

Stress Override는 일반적인 Market Score와 별개의 안전계층이다.

## 5. Regime 판정

위험한 상태를 먼저 검사한다.

### R6 Panic
```text
MarketScore < 20
OR (VIX > 35 AND HY_OAS > 500)
```

### R5 Risk-Off
```text
MarketScore < 40
OR (VIX > 30 AND Drawdown < -15%)
OR PctAbove200 < 20%
```

### R4 Neutral / Transition
```text
40 <= MarketScore < 60
```

### R3 Late / Warning
```text
MarketScore >= 60
AND (Breadth < 50 OR VIX > 22)
```

### R2 Normal Risk-On
```text
60 <= MarketScore < 80
AND Breadth >= 50
```

### R1 Strong Risk-On
```text
MarketScore >= 80
AND Breadth >= 70
AND VIX <= 18
AND HY_OAS <= 250
```

## 6. Market / Sector / Stock 계층 분리

시장상태와 종목판단은 분리한다.

```text
MarketScore  -> 시장 전체 상태
SectorScore  -> 섹터 상대강도/환경
StockScore   -> 개별 종목 상태
```

예시 Buy Strength:
```text
BuyStrength = 0.40*Stock + 0.25*Sector + 0.25*Market + 0.10*Catalyst
```

따라서 시장점수 하나로 삼성전자·SK하이닉스 등 개별 종목의 매수 여부를 직접 결정하지 않는다.

## 7. 검증 프로토콜

권장 시간분할:
- 2010~2020: Development / Learning
- 2021~2023: Validation
- 2024~2026: Out-of-Sample / rolling OOS

필수 검증:
1. Market Score quintile별 20/60/120D 미래수익률
2. R1~R6별 평균수익률/승률/MDD
3. Parameter sensitivity
4. Walk-Forward
5. PBO / CSCV
6. Deflated Sharpe Ratio(DSR)
7. Randomization / permutation test
8. Regime persistence 및 false transition
9. Turnover / 실행가능성

Parameter sensitivity 예시:
```text
MA200 -> 180 / 190 / 200 / 210 / 220
```

검증의 목적은 '가장 좋은 파라미터'를 찾는 것이 아니라, **파라미터가 조금 변해도 효과가 유지되는지 확인하는 것**이다.

## 8. 운영 원칙

- Market Score와 Risk Alarm은 분리한다.
- Score는 연속적이어야 하고, Regime은 운영용 상태값이어야 한다.
- 데이터 누수 방지를 위해 시점 t의 의사결정에는 t 시점 이후 데이터가 절대 포함되지 않는다.
- 모든 rolling normalization은 해당 시점까지 관측된 과거 데이터로만 계산한다.
- 향후 가중치 최적화는 OOS 검증 전에는 수행하지 않는다.

## Status
V1 framework baseline. 이후 실제 데이터 연결 → 계산 엔진 → 백테스트 → falsification/validation 순으로 구현한다.
