# Do the most market-sensitive cities fall furthest? Sensitivity and cumulative price falls in China's 70-city resale housing downturn, 2021–2026

Nov 26, 2026 · @Mk

## 1. Introduction and research questions

By October 2026, second-hand house prices in all 70 of China's major cities stood below their July 2021 level, and 86% of city-months since then had recorded a fall. The 70-city average had fallen for 63 months and by 27 log points (about 24%), against 11 months and about 5% in the 2014–15 downturn.

With every city falling, the useful question is which cities fall furthest. A natural gauge of a city's housing risk is its sensitivity to the national market, the housing analogue of a stock's beta (Case, Cotter and Gabriel, 2011). If the most sensitive cities are also the ones that fall furthest, sensitivity summarises a city's risk for mortgage lenders, local governments and households with homes in several cities; if not, risk must also be judged from local supply and demand.

The dissertation asks one main question: **in China's 2021–26 resale housing downturn, are the cities most sensitive to the national market the ones whose prices have fallen furthest?** A city's cumulative fall is the decline in its log second-hand price index from July 2021 to October 2026. Three sub-questions are answered within this downturn:

- **RQ1 (one national shock):** How much of city price changes does one national factor account for, and how persistent is the decline?
- **RQ2 (sensitivity and cumulative falls):** Do sensitivity and cumulative falls rank cities the same way, and which pre-downturn characteristics go with falls that sensitivity does not explain?
- **RQ3 (joint deep falls):** In the months when the national market is weakest, do cities fall deeply together more often than their ordinary correlation implies?

RQ2 and RQ3 test the same gauge across cities and over time: does sensitivity rank cumulative falls, and do worst months coincide more than the correlation behind it implies? A secondary question asks whether the official new-home and second-hand indices tell the same story. The study is descriptive: it makes no causal claim about policy or city characteristics.

## 2. Literature review

### 2.1 Housing beta and diversification

Case, Cotter and Gabriel (2011) find that housing betas against the national market are significant and time-varying across US metropolitan areas. Cotter, Gabriel and Roll (2015) show that integration across 401 US metropolitan housing markets rose during the 2000s boom, sharply reducing the gains from geographic diversification. Amaral et al. (2025) find that housing outside superstar cities earns higher returns, which they attribute to higher covariance with income growth and lower liquidity. These studies measure risk by betas, covariances or variance shares, not by how far each city falls over a downturn.

### 2.2 Which Chinese cities fall furthest, and which move with the nation?

China's construction boom left a large stock of vacant homes (Glaeser et al., 2017). Han and Lu (2018) trace the divergence of Chinese house prices to a mismatch between supply and demand: after 2003, construction-land quotas shifted towards central and western cities while people moved east. Rogoff and Yang (2024) show that the imbalance is deepest in tier-3 cities. Because housing is durable, supply barely contracts when demand falls, so urban decline is not the mirror image of growth (Glaeser and Gyourko, 2005). A pre-2021 supply overhang should therefore show up in cumulative falls rather than in month-to-month sensitivity. A separate literature finds that tier-1 cities respond more strongly to monetary shocks (Wu and Bian, 2018; Yu and Zhang, 2019). Much of this work compares city tiers rather than using a continuous measure of city strength, and the sensitivity evidence pre-dates the downturn. No study we found asks whether the cities that fell furthest in 2021–26 are the ones most exposed to the national market. RQ2 does so.

### 2.3 Synchronisation and joint deep falls

Funke, Leiva-Leon and Tsang (2019) find that the 70 cities' synchronisation rose until 2015 and then declined, which they link to regionally differentiated macroprudential policy. Other studies split city price growth into national, regional and local factors (Huang, Jin and Zhang, 2021), group city cycles into clusters (Zheng, Gong and Song, 2022) or map networks of co-movement (Xu and Zhang, 2023; 2024). All work at the mean, and every sample ends before 2022, yet mean co-movement cannot show whether cities crash together. Equity correlations are higher in down markets (Longin and Solnik, 2001; Ang and Chen, 2002), but measured dependence also rises mechanically with volatility (Boyer, Gibson and Loretan, 1999; Forbes and Rigobon, 2002). Hu and Fan (2022) find tail dependence within urban clusters in 17 cities' new-home prices for 2006–19, led by tier-1 cities. None of the housing studies covers the 2021–26 downturn or asks whether joint deep falls exceed what ordinary correlation implies; RQ3 does, using co-exceedances (Bae, Karolyi and Stulz, 2003).

### 2.4 Quantile methods and the scale effect

Quantile methods let a common shock move the tails differently from the centre, as financial conditions do for GDP growth (Adrian, Boyarchenko and Giannone, 2019) and house-price growth (Adrian et al., 2020), although simple volatility models capture the GDP lower tail as well (Brownlees and Souza, 2021). Chen, Dolado and Gonzalo (2021) extend factor models to quantiles. In quantile regressions, dependence that rises with volatility appears as a scale effect: when the national factor is mostly negative, lower-quantile slopes steepen even without genuine tail dependence.

### 2.5 What the official indices measure

The National Bureau of Statistics (NBS) compiles the new-home index from online contract records and the second-hand index from agents, platforms and field collection (NBS, 2025), and records no change when a city has no transactions (NBS, 2026). Local governments also propped up land and new-home prices in 2020–22 (Chang, Wang and Xiong, 2026). Infrequent trading smooths measured prices and biases estimated betas downwards (Dimson, 1979; Getmansky, Lo and Makarov, 2004), so a thinly traded city would look less sensitive than it is. The second-hand index is therefore the main sample, smoothing is tested before betas are compared, and the new-home index is a comparison.

## 3. Data and sources

**Primary data.** The main data are the NBS monthly price indices for second-hand and new commercial housing in 70 large and medium-sized cities, January 2011 to October 2026, obtained from CSMAR. The downturn runs from August 2021 to October 2026 (63 months), dated from the July 2021 peak of the national cumulative index; earlier years serve as background and for pre-downturn sensitivity.

City characteristics for 69 cities come from a prefecture-level panel compiled from city statistical yearbooks, 2000–2024, and from a monthly purchase-restriction panel built from 169 official policy events. Mechanism variables, all measured before 2021, are price-to-income ratios, residential land transactions and census population growth (2010–20), compiled from that panel and the Wind database; the original publisher of each series will be cited. If a second price source with a documented origin can be obtained by 10 December 2026, the main results will be replicated on it.

**Secondary sources.** Published papers and NBS method notes (NBS, 2025).

**Ethics.** Only official statistics and published data are used, so no ethics approval is needed.

## 4. Methods

Let yᵢₜ be the month-on-month log change (%) in city i's second-hand price index, f₋ᵢ,ₜ the average change of the other 69 cities, and T = 63 the number of months. Every test is carried out within the downturn, against a model benchmark or differences across cities.

**One national shock (RQ1).** Breadth is the monthly share of falling cities (Mink, Jacobs and de Haan, 2012). Two variance shares of the national mean, with and without each city's average, separate the persistent common trend from synchronised monthly swings. The number of factors follows Bai and Ng (2002) and Ahn and Horenstein (2013).

```latex
S^{\text{raw}} = 1 - \frac{\sum_{i,t}\left(y_{it}-\bar{y}_t\right)^2}{\sum_{i,t} y_{it}^2}, \qquad S^{\text{dm}} = 1 - \frac{\sum_{i,t}\left(\tilde{y}_{it}-\bar{\tilde{y}}_t\right)^2}{\sum_{i,t}\tilde{y}_{it}^2}, \qquad \tilde{y}_{it} = y_{it}-\bar{y}_i
```

**Sensitivity and cumulative falls (RQ2).** A city's sensitivity βᵢ is the slope below. Summing over the downturn splits its cumulative change Dᵢ into the part implied by sensitivity, β̂ᵢFᵢ with Fᵢ = Σₜ f₋ᵢ,ₜ, and a cumulative deviation from that benchmark, T·âᵢ, akin to a cumulative abnormal return. The split is an accounting identity, so it describes rather than tests.

```latex
y_{it} = a_i + \beta_i\, f_{-i,t} + e_{it}, \qquad D_i = \sum_t y_{it} = \hat{\beta}_i F_i + T\,\hat{a}_i
```

The main statistic is the Spearman rank correlation between βᵢ and the cumulative fall −Dᵢ, with the overlap between the quarter of cities that fell furthest and the most sensitive quarter; quantile-regression slopes at τ = 0.25 check whether the answer changes in the lower tail. A city-strength index S, the first principal component of six 2016–21 averages (property investment and loans relative to GDP, fiscal self-sufficiency, GDP per head, population and purchase-restriction months), is correlated with D and β. β is related to pre-downturn price-to-income ratios, and D to land supply relative to population growth (Han and Lu, 2018) and to population growth, controlling for β. Before cross-city differences in β are read, a thin-market check corrects for lagged responses (Dimson, 1979), uses three-month changes, controls for zero-change months and compares cities within tiers.

**Joint deep falls (RQ3).** Tails are defined by each series' ranks R within the downturn: the weakest k = ⌊0.25T⌋ = 15 months, with ties counted fractionally. The lower co-exceedance Cᵢᴸ is the share of the other cities' weakest k months in which city i is also in its own weakest k. It is compared with the value implied by a Gaussian copula with the same normal-scores correlation, and with the upper tail, which any radially symmetric dependence would match.

```latex
C_i^{L} = \frac{1}{k}\sum_{t} \mathbf{1}\left(R^{y}_{it} \le k\right)\mathbf{1}\left(R^{f}_{it} \le k\right)
```

City-by-city quantile regressions (Koenker and Bassett, 1978) give slopes λᵢ(τ). In the location–scale model of Machado and Santos Silva (2019), symmetric errors imply λᵢ(0.25) + λᵢ(0.75) = 2λᵢ(0.5), however strongly the spread varies with the national factor; a positive deviation Δᵢ signals lower-tail amplification beyond this scale effect. A one-factor quantile factor model (Chen, Dolado and Gonzalo, 2021) compares common-factor shares across quantiles. Simulations that plant joint deep falls of known size on the actual national path give the smallest effect each test can detect, so negative results are reported as upper bounds.

```latex
Q_{\tau}\left(y_{it} \mid f_{-i,t},\, y_{i,t-1}\right) = \alpha_i(\tau) + \lambda_i(\tau)\, f_{-i,t} + \rho_i(\tau)\, y_{i,t-1}, \qquad \Delta_i = \lambda_i(0.25) + \lambda_i(0.75) - 2\,\lambda_i(0.5)
```

**Secondary question.** All statistics are recomputed for the new-home index.

**Inference.** Confidence intervals come from a moving-block bootstrap (Künsch, 1989) that resamples the same six-month blocks for all cities and re-estimates factors, thresholds and quantiles in every draw. For cross-city correlations, cities are also resampled and S re-estimated (cf. Menzel, 2021); because this downturn's falls are already realised, intervals that resample cities only are also reported. Decision rules are fixed in written analysis plans before each formal test, and estimates already seen during exploration are flagged.

## 5. Proposed structure

Nine sections are planned, with robustness tables in an appendix; each results section ends with the new-home comparison.

1. Introduction
2. Literature review
3. Framework and hypotheses
4. Data and measurement
5. Methodology
6. Results I: one national shock and its persistence
7. Results II: sensitivity versus cumulative falls
8. Results III: joint deep falls
9. Conclusion

## 6. Feasibility and timeline

The data are cleaned, and the main tests have been run under analysis plans locked in November 2026, on months from January 2022 (point estimates barely change from August 2021). The national mean accounts for 69% of city price changes. Stronger cities are more sensitive to the national market (rank correlation 0.62, 95% interval \[0.35, 0.74\]), and this survives the thin-market checks. There is no evidence that the most sensitive cities fell furthest: the rank correlation between β and the cumulative fall is −0.13 \[−0.59, 0.42\], and only 4 of the 17 cities that fell furthest are among the 17 most sensitive, against 4.2 expected by chance. Cities often weaken together (Cᴸ is about 0.56, against 0.25 under independence), but Cᴸ exceeds its Gaussian benchmark by only 0.03 \[−0.05, 0.11\]. These last two intervals include zero.

December 2026 adds the mechanism tests, the symmetry test and the power simulations, each locked before it is run, and settles the second price source by 10 December. Analysis ends in mid-January 2027, a full draft goes to the supervisor in mid-February, and the dissertation is submitted on 8 April 2027.

## References

Adrian, T., Boyarchenko, N. and Giannone, D. (2019) ‘Vulnerable growth’, *American Economic Review*, 109(4), pp. 1263–1289. [doi:10.1257/aer.20161923](https://doi.org/10.1257/aer.20161923)

Adrian, T., Deghi, A., Katagiri, M., Shahid, S. and Valckx, N. (2020) ‘Predicting downside risks to house prices and macro-financial stability’, IMF Working Paper 20/11. Washington, DC: International Monetary Fund.

Ahn, S.C. and Horenstein, A.R. (2013) ‘Eigenvalue ratio test for the number of factors’, *Econometrica*, 81(3), pp. 1203–1227.

Amaral, F., Dohmen, M., Kohl, S. and Schularick, M. (2025) ‘Superstar returns? Spatial heterogeneity in returns to housing’, *Journal of Finance*, 80(5), pp. 3057–3094.

Ang, A. and Chen, J. (2002) ‘Asymmetric correlations of equity portfolios’, *Journal of Financial Economics*, 63(3), pp. 443–494.

Bae, K.-H., Karolyi, G.A. and Stulz, R.M. (2003) ‘A new approach to measuring financial contagion’, *Review of Financial Studies*, 16(3), pp. 717–763. [doi:10.1093/rfs/hhg012](https://doi.org/10.1093/rfs/hhg012)

Bai, J. and Ng, S. (2002) ‘Determining the number of factors in approximate factor models’, *Econometrica*, 70(1), pp. 191–221.

Boyer, B.H., Gibson, M.S. and Loretan, M. (1999) ‘Pitfalls in tests for changes in correlations’, International Finance Discussion Papers 597. Washington, DC: Board of Governors of the Federal Reserve System.

Brownlees, C. and Souza, A.B.M. (2021) ‘Backtesting global Growth-at-Risk’, *Journal of Monetary Economics*, 118, pp. 312–330. [doi:10.1016/j.jmoneco.2020.11.003](https://doi.org/10.1016/j.jmoneco.2020.11.003)

Case, K.E., Cotter, J. and Gabriel, S.A. (2011) ‘Housing risk and return: evidence from a housing asset-pricing model’, arXiv:1103.5971. Available at: <https://arxiv.org/abs/1103.5971>

Chang, J., Wang, Y. and Xiong, W. (2026) ‘Price and volume divergence in China's real estate markets: the role of local governments’, *Review of Financial Studies*, 39(2), pp. 343–386. [doi:10.1093/rfs/hhaf089](https://doi.org/10.1093/rfs/hhaf089)

Chen, L., Dolado, J.J. and Gonzalo, J. (2021) ‘Quantile factor models’, *Econometrica*, 89(2), pp. 875–910. [doi:10.3982/ECTA15746](https://doi.org/10.3982/ECTA15746)

Cotter, J., Gabriel, S. and Roll, R. (2015) ‘Can housing risk be diversified? A cautionary tale from the housing boom and bust’, *Review of Financial Studies*, 28(3), pp. 913–936. [doi:10.1093/rfs/hhu085](https://doi.org/10.1093/rfs/hhu085)

Dimson, E. (1979) ‘Risk measurement when shares are subject to infrequent trading’, *Journal of Financial Economics*, 7(2), pp. 197–226. [doi:10.1016/0304-405X(79)90013-8](<https://doi.org/10.1016/0304-405X(79)90013-8>)

Forbes, K.J. and Rigobon, R. (2002) ‘No contagion, only interdependence: measuring stock market comovements’, *Journal of Finance*, 57(5), pp. 2223–2261.

Funke, M., Leiva-Leon, D. and Tsang, A. (2019) ‘Mapping China's time-varying house price landscape’, *Regional Science and Urban Economics*, 78, 103464. [doi:10.1016/j.regsciurbeco.2019.103464](https://doi.org/10.1016/j.regsciurbeco.2019.103464)

Getmansky, M., Lo, A.W. and Makarov, I. (2004) ‘An econometric model of serial correlation and illiquidity in hedge fund returns’, *Journal of Financial Economics*, 74(3), pp. 529–609. [doi:10.1016/j.jfineco.2004.04.001](https://doi.org/10.1016/j.jfineco.2004.04.001)

Glaeser, E.L. and Gyourko, J. (2005) ‘Urban decline and durable housing’, *Journal of Political Economy*, 113(2), pp. 345–375.

Glaeser, E., Huang, W., Ma, Y. and Shleifer, A. (2017) ‘A real estate boom with Chinese characteristics’, *Journal of Economic Perspectives*, 31(1), pp. 93–116. [doi:10.1257/jep.31.1.93](https://doi.org/10.1257/jep.31.1.93)

Han, L. and Lu, M. (2018) ‘供需错配：解开中国房价分化之谜’ \[Supply–demand mismatch: solving the puzzle of house-price divergence in China\], *世界经济* \[*The Journal of World Economy*\], 41(10), pp. 126–149.

Hu, G. and Fan, G.-Z. (2022) ‘Empirical evidence of risk contagion across regional housing markets in China’, *Economic Modelling*, 115, 105945. [doi:10.1016/j.econmod.2022.105945](https://doi.org/10.1016/j.econmod.2022.105945)

Huang, X., Jin, T. and Zhang, J. (2021) ‘Monetary policy, hot money and housing price growth across Chinese cities’, *Applied Economics*, 53(59), pp. 6855–6877. [doi:10.1080/00036846.2021.1949433](https://doi.org/10.1080/00036846.2021.1949433)

Koenker, R. and Bassett, G. (1978) ‘Regression quantiles’, *Econometrica*, 46(1), pp. 33–50.

Künsch, H.R. (1989) ‘The jackknife and the bootstrap for general stationary observations’, *Annals of Statistics*, 17(3), pp. 1217–1241. [doi:10.1214/aos/1176347265](https://doi.org/10.1214/aos/1176347265)

Longin, F. and Solnik, B. (2001) ‘Extreme correlation of international equity markets’, *Journal of Finance*, 56(2), pp. 649–676.

Machado, J.A.F. and Santos Silva, J.M.C. (2019) ‘Quantiles via moments’, *Journal of Econometrics*, 213(1), pp. 145–173. [doi:10.1016/j.jeconom.2019.04.009](https://doi.org/10.1016/j.jeconom.2019.04.009)

Menzel, K. (2021) ‘Bootstrap with cluster-dependence in two or more dimensions’, *Econometrica*, 89(5), pp. 2143–2188. [doi:10.3982/ECTA15383](https://doi.org/10.3982/ECTA15383)

Mink, M., Jacobs, J.P.A.M. and de Haan, J. (2012) ‘Measuring coherence of output gaps with an application to the euro area’, *Oxford Economic Papers*, 64(2), pp. 217–236.

National Bureau of Statistics of China (2025) ‘住宅销售价格数据的基础数据来源’ \[Sources of base data for residential sales prices\]. Available at: <https://www.stats.gov.cn/zs/tjws/zytjzbqs/zzxsjgzs/202501/t20250121_1958389.html>

National Bureau of Statistics of China (2026) *Sales prices of commercial residential buildings in 70 large and medium-sized cities* (release and explanatory notes). Available at: <https://www.stats.gov.cn/sj/zxfb/202608/t20260817_1965050.html>

Rogoff, K.S. and Yang, Y. (2024) ‘A tale of tier 3 cities’, *Journal of International Economics*, 152, 103989. [doi:10.1016/j.jinteco.2024.103989](https://doi.org/10.1016/j.jinteco.2024.103989)

Wu, L. and Bian, Y. (2018) ‘Housing, consumption and monetary policy: how different are the first-, second- and third-tier cities in China?’, *Applied Economics Letters*, 25(15), pp. 1107–1111.

Xu, X. and Zhang, Y. (2023) ‘Network analysis of housing price comovements of a hundred Chinese cities’, *National Institute Economic Review*, 264, pp. 110–128.

Xu, X. and Zhang, Y. (2024) ‘Network analysis of comovements among newly-built residential house price indices of seventy Chinese cities’, *International Journal of Housing Markets and Analysis*, 17(3), pp. 726–749. [doi:10.1108/IJHMA-09-2022-0134](https://doi.org/10.1108/IJHMA-09-2022-0134)

Yu, S. and Zhang, L. (2019) ‘The impact of monetary policy and housing-purchase restrictions on housing prices in China’, *International Economic Journal*, 33(2), pp. 286–309.

Zheng, T., Gong, J. and Song, T. (2022) ‘中国城市房价波动的周期性及集群分解’ \[Cyclicality and cluster decomposition of urban house price fluctuations in China\], *计量经济学报* \[*China Journal of Econometrics*\], 2(4), pp. 946–970. [doi:10.12012/CJoE2021-0085](https://doi.org/10.12012/CJoE2021-0085)
