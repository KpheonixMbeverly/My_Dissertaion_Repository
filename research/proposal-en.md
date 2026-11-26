# Which housing downside risks can cross-city holdings diversify? Evidence from China’s 70-city resale downturn, 2021–2026

27 November 2026

## 1. Introduction and research questions

By October 2026, second-hand house prices in all 70 of China’s major cities stood below their July 2021 level, and 86% of city-months since then had recorded a fall. The 70-city average had fallen for 63 months and by 27 log points (about 24%), against 11 months and about 5% in the 2014–15 downturn.

Mortgage lenders and developers hold housing exposure across many cities, and two in five urban households own more than one home (PBoC, 2020). Spreading holdings across cities is the standard defence against local risk, but it protects only against the part of a fall that cities do not share. In the United States, rising integration of metropolitan markets sharply reduced what geographic diversification could achieve (Cotter, Gabriel and Roll, 2015). No study we found examines China’s longer and broader downturn this way.

The dissertation asks one main question: **in China’s 2021–26 housing downturn, which downside risks to house prices could holding homes across cities diversify, and which could it not?** Three sub-questions separate risk across cities from risk over time, then ask what lies behind them:

- **RQ1 (across cities: selection risk):** How much does holding more cities reduce the loss from having picked the worst-hit cities, and could those cities have been identified beforehand from their sensitivity to the national market or their economic strength?
- **RQ2 (over time: bad-month risk):** How much of the loss in the worst months does holding more cities remove, and is diversification weaker when the national market falls, or in this downturn than in the 2015–21 upturn?
- **RQ3 (mechanisms):** Which pre-downturn city characteristics go with the part of the fall that diversification removes, and with the timing of stabilisation?

Because purchase restrictions limited cross-city buying by households, the portfolios measure risk; they are not an investment strategy. The study is descriptive and makes no causal claim about policy or city characteristics.

## 2. Literature review

### 2.1 Geographic diversification of housing risk

Evans and Archer (1968) measured diversification by drawing random equal-weight stock portfolios of increasing size. Callender et al. (2007) used over 10,000 UK commercial properties to estimate how risk falls with portfolio size, and Devaney and Lee (2005) found that downside risk falls as property portfolios grow. For housing, Cotter, Gabriel and Roll (2015) estimate integration across 401 US metropolitan markets and show by portfolio simulation that the 2000s boom left far less room for diversification. In China, an efficient-frontier portfolio of five cities’ residential markets improved risk-adjusted returns by about 40% over a single city (Higgins and Fang, 2012), and the value of geographic diversification to developers falls with their exposure to the most developed cities (Chu, Tsang and Wong, 2023). Diversification also has costs: geographically diversified US lenders screened borrowers less, and the shares of concentrated lenders fell less in 2007–08 (Loutskina and Strahan, 2011). These studies measure risk by variance or Sharpe ratios, often with weights optimised in hindsight, and the Chinese housing evidence covers five cities over six years. None asks how much of a realised nationwide fall diversification removed, or whether it failed in the worst months.

### 2.2 Common and local components of Chinese house prices

Funke, Leiva-Leon and Tsang (2019) find that the 70 cities’ synchronisation rose until 2015 and then declined, which they link to regionally differentiated macroprudential policy. Other studies split city price growth into national, regional and local factors (Huang, Jin and Zhang, 2021), group city cycles into clusters (Zheng, Gong and Song, 2022) or map networks of co-movement (Xu and Zhang, 2023; 2024). Tier-1 prices respond more strongly to monetary shocks (Wu and Bian, 2018; Yu and Zhang, 2019), which suggests judging cities by their sensitivity to the national market. Cumulative falls may instead reflect local supply. Construction land shifted towards central and western cities while people moved east (Han and Lu, 2018), the imbalance is deepest in tier-3 cities (Rogoff and Yang, 2024), and durable housing means that supply barely contracts when demand falls (Glaeser and Gyourko, 2005). This work studies the mean, compares tiers rather than continuous measures of city strength, ends before 2022 and never turns the common component into the share of a fall that cannot be diversified.

### 2.3 Diversification in bad times

Equity correlations are higher in down markets (Longin and Solnik, 2001; Ang and Chen, 2002), but measured dependence also rises mechanically with volatility (Boyer, Gibson and Loretan, 1999; Forbes and Rigobon, 2002). In quantile regression (Koenker and Bassett, 1978) the same mechanism appears as a scale effect: in a location–scale model, a common shock widens the conditional spread, so lower-quantile slopes steepen without any extra tail dependence (Machado and Santos Silva, 2019). Hu and Fan (2022) find tail dependence within urban clusters in 17 cities’ new-home prices for 2006–19. Housing studies rarely compare tail co-movement with what correlation and volatility alone imply, and none covers 2021–26. RQ2 therefore compares diversification in bad months with diversification in ordinary months rather than with zero, using co-exceedances (Bae, Karolyi and Stulz, 2003) and quantile regressions.

## 3. Data and sources

**Primary data.** The main data are the National Bureau of Statistics (NBS) monthly price indices for second-hand and new commercial housing in 70 large and medium-sized cities, January 2011 to October 2026, obtained from CSMAR. The downturn runs from August 2021 to October 2026 (63 months), dated from the July 2021 peak of the national cumulative index; April 2015 to July 2021 is the comparison upturn. City characteristics for 69 cities come from a prefecture-level panel compiled from city statistical yearbooks and from a monthly purchase-restriction panel built from 169 dated policy events. Mechanism variables, all measured before 2021, are price-to-income ratios, residential land transactions and census population growth (2010–20), from that panel and the Wind database; the original publisher of each series will be cited.

**Measurement.** The second-hand index is compiled from agents, platforms and field collection (NBS, 2025) and records no change when a city has no transactions (NBS, 2026), and local governments propped up land and new-home prices in 2020–22 (Chang, Wang and Xiong, 2026). Infrequent trading smooths measured prices (Dimson, 1979; Getmansky, Lo and Makarov, 2004), which would understate bad-month losses. The second-hand index is therefore the main sample, thin-market checks come before cross-city comparisons, and the new-home index serves as a comparison. If a second price source with a documented origin can be obtained by 10 December 2026, the main results will be replicated on it.

**Secondary sources and ethics.** Published papers and NBS method notes. Only official statistics and published data are used, so no ethics approval is needed.

## 4. Methods

Let yᵢₜ be the month-on-month log change (%) in city i’s second-hand price index and f₋ᵢ,ₜ the average change of the other 69 cities.

**Common and city-specific parts.** A city’s sensitivity βᵢ is the slope below. Summing over the T = 63 downturn months splits its cumulative change Dᵢ into the part implied by the national fall, β̂ᵢFᵢ with Fᵢ = Σₜ f₋ᵢ,ₜ, and a city-specific deviation T·âᵢ. Holding more cities averages the deviation away but not the national part.

```math
y_{it} = a_{i} + \beta_{i}f_{- i,t} + e_{it},\quad\quad D_{i} = \sum_{t}^{}y_{it} = {\widehat{\beta}}_{i}F_{i} + T\,{\widehat{a}}_{i}
```

**Random portfolios (RQ1, RQ2).** Following Evans and Archer (1968), for each n ∈ {1, 2, 3, 5, 10, 20, 35, 70}, up to 10,000 sets of n cities are drawn at random, bought in equal amounts at the end of July 2021 and held to October 2026, so the results measure diversification without foresight. Selection risk is CVaR₁₀(n), the average cumulative loss Lₚ of the worst tenth of portfolios. Bad-month risk is ES₁₀, the average of a portfolio’s k = 6 worst monthly returns rₚₜ. Sensitivities estimated over January 2011 to July 2021 test whether the worst-hit cities could have been identified beforehand, and a city-strength index, the first principal component of six 2016–21 characteristics, tests which cities stabilise first.

```math
{CVaR}_{10}(n) = E\left\lbrack L_{p} \mid L_{p} \geq q_{0.9}(L) \right\rbrack,\quad\quad{ES}_{10,p} = \frac{1}{k}\sum_{t \in \text{worst }k}^{}r_{pt}
```

**Diversification in national declines (RQ2).** Quantile regressions over 2011–26 are estimated for every city and portfolio, where a portfolio’s yₚₜ is the average of its cities’ changes. The national factor fₚₜ is taken over the remaining cities and split into rises hₚₜ = max(fₚₜ, 0) and falls gₚₜ = max(−fₚₜ, 0):

```math
Q_{\tau}\left( y_{pt} \mid \cdot \right) = a_{p}(\tau) + \beta_{p}^{+}(\tau)\, h_{pt} + \beta_{p}^{-}(\tau)\, g_{pt} + d_{p}(\tau)\, y_{p,t - 1},\quad\quad\tau \in \lbrace  0.25,\ 0.5,\ 0.75 \rbrace
```

The gap between the median and the lower quartile measures city-specific downside spread, and ω = β⁻(0.5) − β⁻(0.25) is how far it widens per point of national fall. Averaging narrows every spread, so the test compares the share of ω that survives in ten-city portfolios, R_ω, with the share of the ordinary-month spread that survives, R_w. A positive θ = R_ω − R_w means that diversification is weaker in national declines. Co-exceedances against a Gaussian-copula benchmark, an expected-shortfall version of θ and the same portfolios in the 2015–21 upturn complement this test.

**Mechanisms (RQ3).** Cross-city regressions relate the city-specific deviation T·âᵢ, and the price change over the last six months, to pre-downturn land supply relative to population growth (Han and Lu, 2018), price-to-income ratios and population growth, controlling for βᵢ. Because the strongest cities kept purchase restrictions longest, the restriction panel can show whether early stabilisation followed local demand or the easing of restrictions.

**Inference.** Intervals come from a circular block bootstrap (Künsch, 1989) with six-month blocks shared by all cities, and from resampling cities for realised cross-city outcomes (cf. Menzel, 2021). Decision rules are fixed in analysis plans locked before each test, and estimates seen during exploration are flagged.

## 5. Proposed structure

Eight sections are planned, with robustness tables in an appendix:

1.  Introduction
2.  Literature review
3.  Data, measurement and the 2021–26 downturn
4.  Methods: factor split, random portfolios and portfolio quantile regressions
5.  Results I: risk across cities
6.  Results II: risk over time
7.  Mechanisms
8.  Conclusion and limitations

## 6. Preliminary evidence, risks and timeline

**Preliminary evidence.** The data are cleaned, and the portfolio tests were run in November 2026 under a locked plan. Since 2022 the national mean has accounted for 69% of city price changes. Holding ten cities instead of one cut the average loss of the worst tenth of holdings from 30.5% to 26.2%, by 4.3 percentage points (95% interval \[3.3, 5.2\]); even all 70 cities lost 23.7%, the part no diversification removes. Bad months were barely diversifiable: the average loss in the six worst months fell only from 1.16% to 0.94% a month, so about four-fifths remains. Pre-downturn sensitivity did not identify the cities that fell furthest (rank correlation with the fall −0.13 \[−0.36, 0.11\]), but stronger cities have begun to stabilise (rank correlation with the last six months’ change 0.36 \[0.12, 0.59\]). Diversification worked less well than in the 2015–21 upturn: ten-city portfolios kept 69% of their cities’ gap between average and worst months, against 51% in the upturn (difference 0.18 \[0.04, 0.26\]), and ordinary months show a similar difference. Cities did not crash together beyond what their correlation implies (excess co-exceedance 0.03 \[−0.05, 0.11\]), and the test of θ is inconclusive (0.08 \[−0.35, 0.48\]).

**Risks.** Smoothing in the official index may understate bad-month losses, so thin-market checks and a second price source come first. One downturn is a single episode, so the results describe it rather than forecast the next. Tail tests have little power with 63 months, so simulations that plant effects of known size give each test’s smallest detectable effect, and negative results are reported as upper bounds. City indices average away the risk of individual homes, so only diversification between cities is measured.

**Timeline.** December 2026 adds the mechanism tests and power simulations, each locked before it is run. Analysis ends in mid-January 2027, a full draft goes to the supervisor in mid-February, and the dissertation is submitted on 8 April 2027.

## References

Ang, A. and Chen, J. (2002) ‘Asymmetric correlations of equity portfolios’, *Journal of Financial Economics*, 63(3), pp. 443–494.

Bae, K.-H., Karolyi, G.A. and Stulz, R.M. (2003) ‘A new approach to measuring financial contagion’, *Review of Financial Studies*, 16(3), pp. 717–763. [doi:10.1093/rfs/hhg012](https://doi.org/10.1093/rfs/hhg012)

Boyer, B.H., Gibson, M.S. and Loretan, M. (1999) ‘Pitfalls in tests for changes in correlations’, International Finance Discussion Papers 597. Washington, DC: Board of Governors of the Federal Reserve System.

Callender, M., Devaney, S., Sheahan, A. and Key, T. (2007) ‘Risk reduction and diversification in UK commercial property portfolios’, *Journal of Property Research*, 24(4), pp. 355–375. [doi:10.1080/09599910801916279](https://doi.org/10.1080/09599910801916279)

Chang, J., Wang, Y. and Xiong, W. (2026) ‘Price and volume divergence in China’s real estate markets: the role of local governments’, *Review of Financial Studies*, 39(2), pp. 343–386. [doi:10.1093/rfs/hhaf089](https://doi.org/10.1093/rfs/hhaf089)

Chu, X., Tsang, D. and Wong, S.K. (2023) ‘Geographic diversification and real estate firm value: where firms diversify matter’, *Journal of Real Estate Research*, 45(4), pp. 431–461.

Cotter, J., Gabriel, S. and Roll, R. (2015) ‘Can housing risk be diversified? A cautionary tale from the housing boom and bust’, *Review of Financial Studies*, 28(3), pp. 913–936. [doi:10.1093/rfs/hhu085](https://doi.org/10.1093/rfs/hhu085)

Devaney, S. and Lee, S.L. (2005) ‘Real estate portfolio size and risk reduction’, Working Papers in Real Estate & Planning 24/05. Reading: University of Reading.

Dimson, E. (1979) ‘Risk measurement when shares are subject to infrequent trading’, *Journal of Financial Economics*, 7(2), pp. 197–226. [doi:10.1016/0304-405X(79)90013-8](https://doi.org/10.1016/0304-405X(79)90013-8)

Evans, J.L. and Archer, S.H. (1968) ‘Diversification and the reduction of dispersion: an empirical analysis’, *Journal of Finance*, 23(5), pp. 761–767. [doi:10.1111/j.1540-6261.1968.tb00315.x](https://doi.org/10.1111/j.1540-6261.1968.tb00315.x)

Forbes, K.J. and Rigobon, R. (2002) ‘No contagion, only interdependence: measuring stock market comovements’, *Journal of Finance*, 57(5), pp. 2223–2261.

Funke, M., Leiva-Leon, D. and Tsang, A. (2019) ‘Mapping China’s time-varying house price landscape’, *Regional Science and Urban Economics*, 78, 103464. [doi:10.1016/j.regsciurbeco.2019.103464](https://doi.org/10.1016/j.regsciurbeco.2019.103464)

Getmansky, M., Lo, A.W. and Makarov, I. (2004) ‘An econometric model of serial correlation and illiquidity in hedge fund returns’, *Journal of Financial Economics*, 74(3), pp. 529–609. [doi:10.1016/j.jfineco.2004.04.001](https://doi.org/10.1016/j.jfineco.2004.04.001)

Glaeser, E.L. and Gyourko, J. (2005) ‘Urban decline and durable housing’, *Journal of Political Economy*, 113(2), pp. 345–375.

Han, L. and Lu, M. (2018) ‘供需错配：解开中国房价分化之谜’ \[Supply–demand mismatch: solving the puzzle of house-price divergence in China\], *世界经济* \[*The Journal of World Economy*\], 41(10), pp. 126–149.

Higgins, D. and Fang, F. (2012) ‘Analysing the risk and return profile of Chinese residential property markets’, *Pacific Rim Property Research Journal*, 18(2), pp. 149–162. [doi:10.1080/14445921.2012.11104356](https://doi.org/10.1080/14445921.2012.11104356)

Hu, G. and Fan, G.-Z. (2022) ‘Empirical evidence of risk contagion across regional housing markets in China’, *Economic Modelling*, 115, 105945. [doi:10.1016/j.econmod.2022.105945](https://doi.org/10.1016/j.econmod.2022.105945)

Huang, X., Jin, T. and Zhang, J. (2021) ‘Monetary policy, hot money and housing price growth across Chinese cities’, *Applied Economics*, 53(59), pp. 6855–6877. [doi:10.1080/00036846.2021.1949433](https://doi.org/10.1080/00036846.2021.1949433)

Koenker, R. and Bassett, G. (1978) ‘Regression quantiles’, *Econometrica*, 46(1), pp. 33–50.

Künsch, H.R. (1989) ‘The jackknife and the bootstrap for general stationary observations’, *Annals of Statistics*, 17(3), pp. 1217–1241. [doi:10.1214/aos/1176347265](https://doi.org/10.1214/aos/1176347265)

Longin, F. and Solnik, B. (2001) ‘Extreme correlation of international equity markets’, *Journal of Finance*, 56(2), pp. 649–676.

Loutskina, E. and Strahan, P.E. (2011) ‘Informed and uninformed investment in housing: the downside of diversification’, *Review of Financial Studies*, 24(5), pp. 1447–1480. [doi:10.1093/rfs/hhq142](https://doi.org/10.1093/rfs/hhq142)

Machado, J.A.F. and Santos Silva, J.M.C. (2019) ‘Quantiles via moments’, *Journal of Econometrics*, 213(1), pp. 145–173. [doi:10.1016/j.jeconom.2019.04.009](https://doi.org/10.1016/j.jeconom.2019.04.009)

Menzel, K. (2021) ‘Bootstrap with cluster-dependence in two or more dimensions’, *Econometrica*, 89(5), pp. 2143–2188. [doi:10.3982/ECTA15383](https://doi.org/10.3982/ECTA15383)

National Bureau of Statistics of China (2025) ‘住宅销售价格数据的基础数据来源’ \[Sources of base data for residential sales prices\]. Available at: <https://www.stats.gov.cn/zs/tjws/zytjzbqs/zzxsjgzs/202501/t20250121_1958389.html>

National Bureau of Statistics of China (2026) *Sales prices of commercial residential buildings in 70 large and medium-sized cities* (release and explanatory notes). Available at: <https://www.stats.gov.cn/sj/zxfb/202608/t20260817_1965050.html>

PBoC \[People’s Bank of China, Survey and Statistics Department\] (2020) ‘2019年中国城镇居民家庭资产负债情况调查’ \[Survey of the assets and liabilities of urban households in China, 2019\], *中国金融* \[*China Finance*\], 2020(9).

Rogoff, K.S. and Yang, Y. (2024) ‘A tale of tier 3 cities’, *Journal of International Economics*, 152, 103989. [doi:10.1016/j.jinteco.2024.103989](https://doi.org/10.1016/j.jinteco.2024.103989)

Wu, L. and Bian, Y. (2018) ‘Housing, consumption and monetary policy: how different are the first-, second- and third-tier cities in China?’, *Applied Economics Letters*, 25(15), pp. 1107–1111.

Xu, X. and Zhang, Y. (2023) ‘Network analysis of housing price comovements of a hundred Chinese cities’, *National Institute Economic Review*, 264, pp. 110–128.

Xu, X. and Zhang, Y. (2024) ‘Network analysis of comovements among newly-built residential house price indices of seventy Chinese cities’, *International Journal of Housing Markets and Analysis*, 17(3), pp. 726–749. [doi:10.1108/IJHMA-09-2022-0134](https://doi.org/10.1108/IJHMA-09-2022-0134)

Yu, S. and Zhang, L. (2019) ‘The impact of monetary policy and housing-purchase restrictions on housing prices in China’, *International Economic Journal*, 33(2), pp. 286–309.

Zheng, T., Gong, J. and Song, T. (2022) ‘中国城市房价波动的周期性及集群分解’ \[Cyclicality and cluster decomposition of urban house price fluctuations in China\], *计量经济学报* \[*China Journal of Econometrics*\], 2(4), pp. 946–970. [doi:10.12012/CJoE2021-0085](https://doi.org/10.12012/CJoE2021-0085)
