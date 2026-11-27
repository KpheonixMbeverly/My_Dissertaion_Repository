# 文献地图：跨城持有能分散哪些下跌风险？

Nov 27, 2026 · @Mk

## 总览

论文的主问题：在 2021–26 年这一轮下行中，跨城持有住房能分散哪些房价下跌风险，哪些分散不了。开题报告（11 月 27 日版）分三个子问题：城市之间的选城风险（RQ1）、时间上的坏月份风险（RQ2）和机制（RQ3）；第五部分的组合检验已按锁定方案跑完，附录 B 的机制检验还是草稿，跨城尾部同步放进附录、交完开题再做。

文献按开题报告第 2 节的三个主题排（2.1 地理分散、2.2 共同与本地成分、2.3 坏时候的分散），再加机制、数据与测量、推断、附录与扩展四组。开题报告引了 33 条：你电脑上已有 25 条，统计局网页 2 条，还要下载 6 条，都是这次为“地理分散”新加的，链接见文末清单。你刚下好的两篇都核对过：`Network_analysis_of_comovement.pdf` 是 Xu & Zhang (2024)，`14445921.2012.11104356.pdf` 是 Higgins & Fang (2012)。

| 部分 | 问题 | 关键统计量 | 现有结果（截至 2026-11-27） |
| --- | --- | --- | --- |
| 结果一：城市之间（RQ1） | 多持有几个城市，能把选中重跌城市的损失减少多少？重跌城市能否事先识别？ | 因子分解 Dᵢ = β̂ᵢFᵢ + T·âᵢ；随机等权组合的 CVaR₁₀(n) 与 Δ\_cross(n)；H-P5 事前 β；H-P4 实力指数与最近 6 个月变化；H-P3 同区域与跨区域 | 全国均值解释 69% 的城市价格变化；持有 10 城比 1 城，最差一成少跌 4.28 个百分点 \[3.33, 5.17\]，持有全部 70 城仍跌 23.66%；H-P5 ρ = −0.13 \[−0.36, 0.11\]，事前识别不出；H-P4 ρ = 0.36 \[0.12, 0.59\]，强城市先止跌；H-P3 差别不明显 |
| 结果二：坏月份（RQ2） | 最差月份的损失有多少能靠多持有城市消除？全国下跌时、或与 2015–21 年上行期相比，分散是否更弱？ | 最差 6 个月的 ES₁₀ 与 Δ\_time(n)；H-P2 组合与单城分位数回归的 θ(10)（唯一主检验）；同时超越与高斯基准；H-P6 上行期对照 | 最差 6 个月平均跌幅从每月 1.16% 降到 0.94%，约五分之四留下；θ(10) = 0.08 \[−0.35, 0.48\]，最小可检测效应 1.0，没有结论；H-P6 下行期多保留 0.18 \[0.04, 0.26\]，分散比上行期差；超额同时超越 +0.03 \[−0.05, 0.11\] |
| 机制（RQ3，附录 B） | 哪些下跌前的城市特征，与分散能消除的那部分跌幅、与止跌早晚有关？ | H-B1 房价收入比与 β（同时控制 S）；H-B2 控制 β 后，累计跌幅与供给积压、人口增长；H-B3 最近 6 个月变化，控制限购解除早晚 | 草稿，未锁定、未运行；锁定前要在 Wind 核对用地口径、补九江 2010 年人口、查 6 个区划调整城市的可比人口增长 |
| 数据与测量 | 官方二手房指数撑得起这些比较吗？ | 两套指数的编制口径；薄市场检验；新房指数对照；第二套价格数据 | 二手房为主样本，新房作对照；第二套价格数据 12 月 10 日前拿到就复现主要结果 |
| 附录：跨城尾部同步 | 扣除全国因子后，城市两两之间的坏月份是否扎堆？ | 待定 | 交完开题报告后再研究 |

读法：每条文献标出它提供的是**结论**（可对照的实证发现）、**思路**（问题框架或识别逻辑）还是**工具**（统计量、估计或推断方法），以及接到哪个子问题或章节。状态一栏：**已下载**指在你电脑上、我核对过是哪一篇并读了摘要，写进论文前要读原文；**待下载**指开题已引、你还没有原文；**建议引**指开题没引、正文最好加上；**可选**指不下也不影响论证。“开题已引”指开题报告 11 月 27 日版的 33 条参考文献里有。研报和媒体不进参考文献，单列一节，只在草稿里出现。

&#91;embedded content: 文献组 → 论文部分 · 7 组文献、五个部分\]

箭头表示该组文献为哪一部分提供结论、思路或工具；左框第三行是该组必引篇数和缺口。缺口都在 2.1 地理分散一组（6 篇待下载）；附录与扩展一组开题没有引，用不用看附录做不做。

## 文献综述 2.1：住房风险的地理分散（接 RQ1、RQ2）

这一组是 11 月 27 日改题后新加的，给论文提供问题和方法。随机抽取规模递增的等权组合（Evans & Archer 1968）在房地产上已有先例，Cotter 等 (2015) 几乎就是本文的美国版。本文的不同在于：用一轮已发生的全国性下跌，指标是最差一成组合的整轮跌幅和最差月份的跌幅，而不是方差或夏普比率；权重随机抽取，不靠事后优化；中国住房的现有证据只有五个城市、六年（Higgins & Fang 2012）。

| 文献 | 提供什么 | 接到哪里 | 状态 |
| --- | --- | --- | --- |
| Evans & Archer (1968), *Journal of Finance* 23(5) | 工具：随机抽取规模递增的等权股票组合，看组合的离散程度随持有数量怎样下降 | 第五部分随机组合（n 从 1 到 70，每档最多 1 万组）的方法原型；分散曲线 | 待下载 · 开题已引 |
| Callender, Devaney, Sheahan & Key (2007), *Journal of Property Research* 24(4) | 结论 + 工具：用 Investment Property Databank 跟踪的一万多处英国物业，检验风险降低和分散效果怎样随组合规模变化 | 文献综述一句：随机组合用于房地产的先例 | 待下载 · 开题已引 |
| Devaney & Lee (2005), Reading Working Papers in Real Estate & Planning 24/05 | 结论：用蒙特卡洛模拟 IPD 中 1,728 处物业 1995–2004 年的回报，组合越大下行风险越低，但大幅跑赢基准的机会也变少 | 用下行指标衡量分散的房地产先例，对应本文的 CVaR₁₀ 和 ES₁₀ | 待下载（免费）· 开题已引 |
| Cotter, Gabriel & Roll (2015), *Review of Financial Studies* 28(3) | 结论 + 工具：401 个美国都市区在 2000 年代一体化上升，组合模拟显示地理分散的潜力随之下降 | 最直接的先例；引言的动机；H-P6“下行期分散比上行期差”与它方向一致 | 已下载（2012 年工作稿）· 开题已引 |
| Higgins & Fang (2012), *Pacific Rim Property Research Journal* 18(2) | 结论：北京、上海、广州、天津、成都五城高端住宅，六年季度数据；有效前沿组合的风险调整收益比单城高约 40%，高净值投资者在主要城市外再加一套房至少改善 16%；表 9 是单城与组合的对比 | 单城与组合比较的中国先例（第五部分 4(a)(b) 的比较逻辑）；区别：权重在样本内优化、用均值–方差、只有高端住宅 | 已下载（本次核对，摘要与开题报告的“约 40%”一致）· 开题已引 |
| Chu, Tsang & Wong (2023), *Journal of Real Estate Research* 45(4) | 结论：中国房企在最发达城市的敏口越高，地理分散对公司价值的好处越小 | 引言：开发商持有跨城敏口；“在哪里分散”也要紧，接 H-P3 | 待下载 · 开题已引 |
| Loutskina & Strahan (2011), *Review of Financial Studies* 24(5) | 结论：地理分散的按揭机构对借款人审查更少；业务集中的机构利润更高、波动更小，2007–08 年股价跌得更少 | 文献综述一句“分散也有代价”；结论的讨论 | 待下载 · 开题已引 |
| 中国人民银行调查统计司课题组 (2020)，《中国金融》2020 年第 9 期 | 数据：2019 年 3 万余户城镇家庭调查，有两套住房的占 31.0%，三套及以上的占 10.5%；调查没有说这些房子是否在不同城市 | 引言“五分之二的城镇家庭拥有不止一套住房” | 待下载（知网；澎湃有转载）· 开题已引 |
| Case, Cotter & Gabriel (2011), arXiv 1103.5971 | 工具：把都市区房价收益对全国收益回归得到“住房 β”，并检验特质风险 | 方法章定义敏感度 β 时引；开题 11 月 27 日版已删 | 已下载（2010 年工作稿）· 建议引 |
| Giacoletti (2021), *Review of Financial Studies* 34(8) | 结论：单套住房资本利得的特质成分很大，计入后住房的夏普比率明显下降 | 局限：城市指数平均掉了单套住房的风险，本文只衡量城市之间的分散 | 未下载 · 建议引 |

## 文献综述 2.2：中国房价的共同成分与本地成分（接“分散不掉的部分”与 RQ1）

这一组说明哪部分风险分散不掉、哪部分可以。中国 70 城的同步性、集群和网络研究都在均值层面，样本都在 2022 年以前结束，也没有把共同成分换算成一轮跌幅里分散不掉的份额。

一线城市对冲击更敏感的发现提示可以按敏感度挑城，H-P5 检验的正是这一点，结果是事前 β 识别不出重跌城市。郑挺国等 (2022) 已发现中西部城市收缩期跌得更深，所以新意要写在“分散能消除多少”和“事先能否识别”上，不写“谁跌得深”。

| 文献 | 提供什么 | 接到哪里 | 状态 |
| --- | --- | --- | --- |
| Funke, Leiva-Leon & Tsang (2019), *Regional Science and Urban Economics* 78 | 结论：70 城（2006-07 至 2017-01，统计局新房与二手房指数的几何平均），马尔可夫切换模型；同步性升到 2015 年，之后脱钩，作者把它与各地宏观审慎政策力度不同联系起来；分成四个集群，集群内同步高、集群间低；人口增长、收入和空气质量的差异能解释两两同步性 | 均值层面的中国先例，样本在本轮之前。它的集群内同步高，而 H-P3 按四大区域没有发现同区域组合更难分散，写的时候要解释（区域划分和时期都不同） | 已下载（期刊版）· 开题已引 |
| Huang, Jin & Zhang (2021), *Applied Economics* 53(59) | 结论 + 工具：70 城（2005-06 至 2015-04）；作者认为统计局数据过于平滑，改用 CNFS 房地产数据；四层动态因子模型（全国、区域、省、城市），月度涨跌中本地因子解释约 78% 的方差，期限拉长到半年，全国因子升到 51%；VAR 显示货币政策和热钱冲击显著影响全国因子 | 期限越长，全国部分越大：整轮累计跌幅里分散不掉的比重高于月度；数据章：作者因统计局数据平滑而换数据，正是薄市场检验要回应的担忧 | 已下载（期刊版）· 开题已引 |
| 郑挺国、龚金金、宋涛 (2022)，《计量经济学报》2(4) | 结论：70 城新房月度环比（2006–2020），聚类马尔可夫切换模型；全国性扩张和收缩之外还有两个特异性收缩集群，集群内收缩期相同、集群间不同；一线和热门二线城市的集群领先全国扩张，含中西部城市的集群先于全国收缩，中西部城市在收缩期跌得比一二线深；需求因素主导一线和热门二线城市的同步，供给因素在中西部更重要 | 引言和文献综述要划清界限（见上）；数据章还要回应它选新房指数的三条理由（见“数据与测量”一节） | 已下载（期刊版）· 开题已引 |
| Xu & Zhang (2023), *National Institute Economic Review* 264 | 结论：中指“百城价格指数”（楼盘新房价格按建筑面积加权），99 城，2010-06 至 2019-05，相关系数分层聚类与同步分析；2017 年 3 月后联动稍低，但没有持续下降；识别出几组城市，组内同步较强但不稳定 | 网络方法的中国先例；用的是新房价格，也接新房对照 | 已下载（期刊版）· 开题已引 |
| Xu & Zhang (2024), *International Journal of Housing Markets and Analysis* 17(3) | 结论：70 城新房价格指数，2011-01 至 2020-12，网络分析加拓扑和层级刻画；八组直接相连的城市，组内同步高于全国；全国和各组的联动从 2018 年起普遍变低，各城的同步强度从 2019 年初起转低 | 同上；2018 年后联动走低，与 Funke 等“2015 年后脱钩”方向一致，样本都在本轮之前 | 已下载（本次核对）· 开题已引 |
| Wu & Bian (2018), *Applied Economics Letters* 25(15)；Yu & Zhang (2019), *International Economic Journal* 33(2) | 结论：Yu & Zhang 用 Fang 等的新房特征价格指数（约 2003–2013），一线城市房价对货币冲击更敏感，作者推测是限购下需求旺、供给少；Wu & Bian 把 70 城按能级分组（2005-07 至 2015-12）做 SVAR，一线城市房价对加息的反应更强，房价下跌时消费降得更多 | 开题 2.2 节“可以按敏感度判断城市”的依据；H-P5 检验事前 β 能否识别重跌城市，结果是不能（ρ = −0.13 \[−0.36, 0.11\]） | 已下载（Yu & Zhang 是 EPUB，有 PDF 最好换）· 开题已引（两篇） |
| Del Negro & Otrok (2007), *Journal of Monetary Economics* 54(7)；Kallberg, Liu & Pasquariello (2014), *Real Estate Economics* 42(1) | 结论：美国各州房价以本地成分为主，2000 年代繁荣中全国成分上升；14 个 Case-Shiller 城市 1992–2008 年联动上升，多数可归于共同基本面 | 讲“全国部分分散不掉”时作美国对照；开题未引 | 已下载 · 可选 |
| 刘海云、吕龙 (2018)，《中国工业经济》第 12 期 | 结论 + 思路：42 城季度数据（2007–2017），用时变参数的基础价值模型测算泡沫，以 DAG 和 SVAR 刻画传染路径；约 48.5% 的泡沫可由传染解释，传染总体由东向西、由核心向外围（据 PDF 末尾的英文摘要） | 中文文献对城市房价传染的既有讲法 | 已下载 · 可选 |

## 文献综述 2.3：坏时候的分散（接 RQ2）

RQ2 问的是最差的月份里分散还剩多少作用。这一组提供三样东西：熊市里资产相关性升高，但测得的相依会随波动机械上升，所以要和高斯基准比；同时超越的度量；位置–尺度结构下，共同冲击本身就会让下分位斜率变陡，所以 H-P2 不拿组合的变宽和 0 比，而是比“下跌时的变宽”和“平时的宽度”在组合里各保留几成。Hu & Fan (2022) 是中国城市房价尾部相依的直接先例，正文要回应，也是附录跨城尾部同步的起点。

| 文献 | 提供什么 | 接到哪里 | 状态 |
| --- | --- | --- | --- |
| Longin & Solnik (2001), *Journal of Finance* 56(2)；Ang & Chen (2002), *Journal of Financial Economics* 63(3) | 结论 + 工具：国际股市熊市尾部相关上升、牛市不升；超越相关与正态基准比较 | “坏时候分散失效”的经典证据；θ 和 H-P6 是住房上的同类问题，θ 没有结论，H-P6 显示下行期比上行期差 | 已下载（Longin–Solnik 为期刊前稿）· 开题已引（两篇） |
| Forbes & Rigobon (2002), *Journal of Finance* 57(5) | 思路 + 工具：危机期相关上升可能只是波动上升带来的偏差；校正后“传染”多变成“相互依存” | 为什么要和高斯基准比；“没有超出相关性的同时深跌”的表述来源 | 已下载（1999 年 NBER 工作稿）· 开题已引 |
| Boyer, Gibson & Loretan (1999), Fed IFDP 597 | 工具：按高波动或尾部子样本计算的相关会机械上升 | 同上；也说明 H-P6 为什么要同时报告平常月份的比值（平常月份也有类似差别） | 已下载 · 开题已引 |
| Bae, Karolyi & Stulz (2003), *Review of Financial Studies* 16(3) | 工具：用“共超越”（同一时期多个市场同时出现极端负收益的次数）度量传染 | 同时超越概率的定义出处（超出高斯基准 +0.03 \[−0.05, 0.11\]） | 已下载（2000 年 NBER 工作稿）· 开题已引 |
| Koenker & Bassett (1978), *Econometrica* 46(1) | 工具：分位数回归的原始出处 | H-P2：组合与单城的分位数回归（全国涨跌拆成涨、跌两段） | 已下载（JSTOR 期刊版）· 开题已引 |
| Machado & Santos Silva (2019), *Journal of Econometrics* 213(1) | 工具：位置–尺度分位模型，各分位的斜率 = 位置斜率 + 尺度斜率 × 该分位的标准化分位数 | H-P2 为什么比较保留比 R\_ω 和 R\_w，而不是看组合的 ω 是否为 0 | 已下载（2018 年会议稿，引用以期刊版为准）· 开题已引 |
| Hu & Fan (2022), *Economic Modelling* 115 | 结论：三大城市群 17 城的新房月度指数（2006–2019），用 AR–GARCH–t 去波动后拟合藤 copula，城市群内存在尾部相依，一线城市是传染源 | 必须回应的直接先例：本文用二手房、本轮下跌、各城对全国因子，并以高斯基准衡量超额；附录跨城尾部同步的起点 | 已下载 · 开题已引 |

## 机制：供需错配与城市分化（接 RQ3、附录 B）

RQ3 只解释分散能消除的那部分：控制 β 之后的累计跌幅，以及最近 6 个月的止跌早晚。附录 B 的三项检验按这一组设定：房价收入比解释 β（H-B1）；供给积压和人口增长解释控制 β 后的跌幅（H-B2，即供需错配）；同样的指标解释止跌早晚，并控制限购解除早晚（H-B3）。全部是城市间的相关，不作因果解释。

| 文献 | 提供什么 | 接到哪里 | 状态 |
| --- | --- | --- | --- |
| 韩立彬、陆铭 (2018)，《供需错配：解开中国房价分化之谜》，《世界经济》41(10) | 结论 + 思路：2003 年后土地供给转向中西部，供地相对收紧的多是人口流入的沿海和内地大城市；2004–2013 年，供地相对收紧的城市房价平均高 10.6%，也只有这些城市的房价–工资比上升；房价分化的根源是土地供给在空间上与需求错配 | H-B2 的供给积压：2016–20 年住宅用地成交对城市规模和人口增长回归的残差 | 已下载（期刊版）· 开题已引 |
| Rogoff & Yang (2024), *Journal of International Economics* 152 | 结论：供需失衡在较小、低收入的三线城市更深；2021 年约 78% 的住房建设在三线城市 | H-B2 的方向；引言“城市间跌幅差距大”的学术出处 | 已下载（2022 年 NBER 工作稿）· 开题已引 |
| Glaeser & Gyourko (2005), *Journal of Political Economy* 113(2) | 结论：住房建得快、消失得慢，城市衰退不是增长的镜像；负需求冲击压低房价多于减少人口，衰退高度持续；房价低于建造成本时城市才会收缩 | 供给积压为什么进入累计跌幅而不是敏感度；人口增长要和收入一起看（H-B2、H-B3） | 已下载（期刊版重印；另一份 NBER 工作稿可删）· 开题已引 |
| Glaeser, Huang, Ma & Shleifer (2017), *Journal of Economic Perspectives* 31(1) | 思路：中国建设热潮的规模、地方政府控制土地供给、空置住房大增 | 附录 B 供给积压的背景；开题 11 月 27 日版已删 | 已下载（2016 年工作稿）· 可选 |

## 数据与测量：指数编制、新房价格管理与薄市场（接数据章）

数据章要交代四件事：两套指数怎么编（新房用网签数据；二手房合并中介、平台报送和实地采价，无成交按持平，只覆盖市辖区）；新房受地方政府托价，所以只作对照；指数平滑会低估坏月份的损失，所以城市间比较之前先做薄市场检验；为什么以二手房为主样本。

最后一件要正面回应郑挺国等 (2022) 选新房指数的三条理由：新房指数用网签数据并做了质量调整；二手房指数来自重点调查和典型调查，没有质量调整；买卖双方为避税有低报成交价的动机。他们也说用二手房指数测得的周期相近。开题报告第 3 节还没有回应，可以对照统计局 2025 年说明里的现行做法。

| 文献 | 提供什么 | 接到哪里 | 状态 |
| --- | --- | --- | --- |
| 国家统计局：《住宅销售价格数据的基础数据来源》（2025）；70 城月度发布及说明（2026） | 工具（数据口径）：新房指数用网签数据；二手房合并中介、平台报送与实地采价；无成交按持平；调查覆盖市辖区，不含县 | 数据章；两套指数为何不同的第一层解释；附录 B 地理口径的依据 | 网页 · 开题已引 |
| Chang, Wang & Xiong (2026), *Review of Financial Studies* 39(2) | 结论：2020–2022 年土地和新房价格上涨而成交骤降，原因是地方政府的价格管理（供给控制、城投拿地、限制预售证）；2021–2022 年 20 多个城市发文禁止新房低于基准价销售 | 新房只作对照的理由；局限：弱城市的价格可能有行政粘滞 | 已下载（2025 年 NBER 工作稿 34303，引用以期刊版为准）· 开题已引 |
| Dimson (1979), *Journal of Financial Economics* 7(2) | 工具：交易不频繁时，用同期加滞后系数之和估计 β | 薄市场检验；平滑会低估坏月份损失（开题第 6 节的风险） | 已下载 · 开题已引 |
| Getmansky, Lo & Makarov (2004), *Journal of Financial Economics* 74(3) | 工具：用收益的序列相关刻画非流动性和平滑，平滑使波动与 β 被低估 | 同上；也说明 ES₁₀ 可能偏低 | 已下载 · 开题已引 |
| Wu, Deng & Liu (2014), *JREFE* 48(3)；Fang, Gu, Xiong & Zhou (2016), *NBER Macroeconomics Annual* 30；Francke (2010), *JREFE* 41(1) | 工具 + 结论：官方新房指数的测量偏差（繁荣期涨幅被低估）；成交稀少市场的指数构造 | 数据章一句；开题 11 月 27 日版已删。前两篇讲的是繁荣期，不能推出下跌期跌幅被低估 | 已下载 · 可选 |

## 推断：块自助与城市重抽（接方法章和各部分的锁定方案）

所有区间都来自两种重抽：月份用 6 个月的循环块，所有城市共用同一组块；已实现的城市间结果（整轮累计跌幅、H-P3 至 H-P5）对城市重抽。判定规则先写进分析方案、锁定后再运行。Spearman 秩相关、偏秩相关和最小可检测效应（2.5 × 自助标准误）是通用做法，不需要专门引文。

| 文献 | 提供什么 | 接到哪里 | 状态 |
| --- | --- | --- | --- |
| Künsch (1989), *Annals of Statistics* 17(3)；Politis & Romano (1992) | 工具：移动块自助（Künsch）与循环块自助（Politis & Romano） | 时间维度的全部区间：6 个月块，所有城市共用 | Künsch 已下载（扫描件）· 开题已引；Politis & Romano 只引不下，开题未引 |
| Menzel (2021), *Econometrica* 89(5) | 工具：两维及以上聚类相依下自助法的有效性 | 城市重抽与双向自助（月份块 × 城市）；H-P4、H-P5 另报双向区间，附录 B 以双向自助为主 | 已下载（2017 年 arXiv 稿）· 开题已引 |

## 附录与扩展（开题报告没有引，看附录做不做）

这一组都在你电脑上，只差导师的论文。跨城尾部同步（扣除全国因子后，城市两两之间）放进附录，交完开题再定方法；因子个数和分位数因子模型在论文里的位置写作时再定（第五部分方案第 7 节）。

| 文献 | 提供什么 | 接到哪里 | 状态 |
| --- | --- | --- | --- |
| Hong, Tu & Zhou (2007), *Review of Financial Studies* 20(5) | 工具：上下尾不对称的模型无关检验 | 附录跨城尾部同步：坏月份与好月份的同步是否对称（H-P2 的上尾镜像 θ⁺ 也是这个意思） | 已下载（扫描件） |
| Bai & Ng (2002), *Econometrica* 70(1)；Ahn & Horenstein (2013), *Econometrica* 81(3) | 工具：因子个数的信息准则；特征值比估计 | 附录 C 若保留因子个数估计：佐证“一个全国因子”，和 H-P3“同区域与跨区域差别不明显”放在一起讲 | 已下载（期刊版；Bai & Ng 的文件名写 2003，实为 2002） |
| Yaping Wang（导师）, Cross-Validating the Number of Factors for Prediction，工作论文 | 工具：用交叉验证选因子个数 | 同上；答辩时可能被问到 | 待找（只在附录 C 做因子个数时需要） |
| Bailey, Kapetanios & Pesaran (2016), *Journal of Applied Econometrics* 31(6) | 工具：截面相依的指数 α，衡量因子强度 | 同上：全国因子是不是“强因子” | 已下载（2012 年 CESifo 工作稿，引用以期刊版为准） |
| Chen, Dolado & Gonzalo (2021), *Econometrica* 89(2) | 工具：分位数因子模型，可发现只移动尾部、不移动均值的共同因子 | 已有结果 QF1 +0.034 \[−0.041, 0.109\]，各分位因子与均值的相关都在 0.97 以上；位置写作时再定 | 旧库·已精读 |
| Campbell, Giglio & Pathak (2011), *American Economic Review* 101(5) | 结论：马萨诸塞州约 20 年的交易，止赎房平均折价约 27%（2010 年稿）；附近的止赎会压低房价 | 讨论：坏月份不是集中抛售引起的急崩盘，本文的法拍数据只作描述 | 已下载（2010 年稿，引用以 AER 期刊版为准；另一份 2009 年 NBER 稿可删） |

## 研报与非学术来源（只在草稿中列出，正式论文隐去）

按本项目的规则，研报不写进论文的数据来源和参考文献，只借鉴其数据和思路，在草稿里列出；正式稿把对应的经验事实换成学术文献、统计局数据或本文自己的检验结果。下表前八行与开题报告中文对照稿末尾的研报清单一致，后两行是国信均价和媒体；37 份研报的全部清单和优先级在[研报矩阵](https://claude.ai/artifact/Af73Qhz1oVcj3u9QVg996Q)。

| 来源 | 借鉴了什么 | 借鉴到哪里 | 正式稿换成 |
| --- | --- | --- | --- |
| Oxford Economics（2025-09-12），Research Briefing “House prices continue to slide for China's cities” | 三线小城市自 2021 年高点下跌多达 30%，北京、上海不到 10%；家庭收入增长最慢的城市跌得最深 | RQ1 的动机（城市间跌幅差距大）；H-B1 的房价收入比 | 本文用统计局指数算的累计跌幅和房价收入比 |
| AMRO（2026-01-16），Analytical Note “China's Property Market: Navigating a Path Toward Stability” | 以库存衡量的供给冲击对低能级城市影响更大 | H-B2 供给积压的思路 | 韩立彬、陆铭 (2018)；Rogoff & Yang (2024) |
| 申万宏源《核心城市先行，星火亦可燎原》（2026-05-18，p27） | 冰山 40 城二手房成交价 2021-07 以来累计跌 41% | 数据与测量、开题第 6 节风险：官方指数可能低估跌幅，要第二套价格数据 | Dimson (1979)；Getmansky 等 (2004) |
| 申万宏源（同上，p1、p33） | 核心城市止跌领先全国；上海、北京挂牌去化约 4、8 个月，部分二线及以下 20 个月以上 | H-P4“实力强的城市先止跌”；H-B3 止跌早晚的机制 | 本文自己的检验结果（H-P4：ρ = 0.36） |
| 东吴证券《消费“向下”、地产“向上”》（2026-05-25，p1、p7–p8、p16–p17） | 2020–24 年人口“双流出”城市由 89 个增至 161 个，97.5% 为三线及以下 | H-B2、H-B3 的人口增长 | 用第六、第七次普查人口自己构造 |
| 开源证券《鉴往知来，人口不是影响房价唯一因素》（2025-09-24，p1） | 人口要通过收入才能转化为有效需求 | RQ3 中人口增长与房价收入比一起看 | Glaeser & Gyourko (2005) |
| 58 安居客研究院《2025 年全国二手房市场年报》（2026-01，p3、p11、p20） | 三四线挂牌量同比 +17.07%；找房热度与挂牌价的相关系数一线 −0.57、三四线 −0.05 | 数据与测量：薄市场检验 | Dimson (1979) |
| 国金证券《楼市的双重分化》（2026-06-23，p1） | 城市内部不同类型住房走势分化 | 开题第 6 节风险：城市指数平均掉单套住房的风险 | 开题稿不引研报；正文可改引 Giacoletti (2021)（建议） |
| 国信证券整理的城市商品住宅均价（工作区“国信房地产数据”） | 房价收入比的分子 | H-B1 的估值变量 | 写到原始机构：查明国信均价的原始出处后照实写，或换成统计年鉴口径；两样都做不到就只放稳健性 |
| 媒体：彭博 2026-09-15 的报道；MLQ.ai 对 2026 年 10 月数据的统计 | 2026 年 8 月 70 城新房环比 −0.17%、二手房 −0.31%；10 月 49 城新房、58 城二手房环比下跌 | 新房对照的旁证 | 直接用统计局 70 城数据算同样的数 |

研究计划 3.10 节登记的中信建投、东方财富两份研报，开题稿没有用到。国际清算银行工作论文 No. 1319 是学术工作论文，不是研报，核实原文前不引。申万宏源、东吴、58 安居客三份不在研报矩阵的 37 份里；开源证券那份应是矩阵 B 级第 16 份（《房价止跌回稳系列三：人口不是影响房价唯一因素》），矩阵里可以补上这三份。

研报矩阵里 A 级还有 9 份没有用到。下面按题目粗分它们可能借鉴到的部分（以矩阵为准）；以后借鉴了哪一份，就挪进上表：

- 下跌期与持续性（结果二的背景）：《地产周期见底判断：指标、分歧、政策》；《不一样的地产周期：从“同起同落”到“城市分化”》
- 城市分化与止跌（RQ1、H-P4）：《房价专题：一线城市房价韧性更强，低线城市房价已经深度调整》；《哪些二线城市有望率先企稳？》；《我国房价正迎来二阶导转正》
- 机制（RQ3）：《300个地级市人口流动与需求变迁》；《房地产市场何时迎来“最后一跌”》（房价收入比）
- 引言背景：《海外房价深度调整期的经验启示》；《房地产行业4月月报》

## 降为可选或备查的文献（含 11 月 26 日、27 日两次删掉的）

在你电脑上的不用删，新设计用不上，或只在个别地方可引。前五行是 11 月 27 日改题后新降下来的；标“11-26 精简”的几行没有下载，也不用再下。

| 文献 | 原来的用途 | 现在 |
| --- | --- | --- |
| Mink, Jacobs & de Haan (2012), *Oxford Economic Papers* 64(2) | 下跌广度对应“同步性” | 备查（11-27）：不再度量同步性，下跌广度 86% 只作描述 |
| Amaral, Dohmen, Kohl & Schularick (2025), *Journal of Finance* 80(5) | 超级城市以外的超额回报是风险补偿 | 可选（11-27 开题已删）：讨论“强城市先止跌”时可引一句；它的风险是相对收入增长的协方差，不是相对全国房价的 β |
| Adrian, Boyarchenko & Giannone (2019), *AER* 109(4)；Adrian 等 (2020), IMF WP 20/11；Brownlees & Souza (2021), *JME* 118 | 在险增长与在险房价；尺度效应的同伴证据 | 可选（11-27）：文献综述若要交代“本文衡量下行风险，但不为它建条件分位数模型”，引 Adrian 等一句 |
| Koenker & Machado (1999), *JASA* 94(448)；Ando & Bai (2020), *JASA* 115(529) | 分位数回归拟合优度；带公共因子的面板分位数回归 | 备查（11-27）：组合分位数回归用不上 |
| Gelman & Stern (2006), *The American Statistician* 60(4) | 不用“H5 不显著、H6 显著”推断两者不同 | 备查（11-27）：H5、H6 不再是论文的检验 |
| Glaeser, Gyourko & Saiz (2008), *Journal of Urban Economics* 64(2) | 供给弹性作为敏感度的候选解释 | 可选：供给弹性不作机制，只在说明原因时与 Glaeser & Gyourko (2005) 并引 |
| Sun, Zheng, Geltner & Wang (2017), *JREFE* 55(3)；Du & Zhang (2015), *Journal of Econometrics* 188(2) | 实力指数中限购项的依据 | 可选：本文不估计政策效应；介绍限购面板和 H-B3 的“限购解除早晚”时可引 |
| Gong, Hu & Boelhouwer (2016), *RSUE* 59；Liu & Xiong (2020)，Handbook of China's Financial System 一章 | 引言背景；“剔除本区域”稳健性的理由 | 可选：文献综述已有更直接的中国先例 |
| IMF GFSR 2019 第 2 章；Plagborg-Møller, Reichlin, Ricco & Hasenzagl (2020), BPEA；Huang, Liao, Luo & Ma (2024), JEDC | H4 的同伴证据 | 备查：H4 现在只作 H-P2 的单城一侧（n = 1） |
| Korobilis & Schröder；Clark, Huber, Koop, Marcellino & Pfarrhofer (2024), JBES；Gneiting 等 (2023) | 分位数因子模型的同伴文献；R¹ 用检验损失的依据 | 备查：分位数因子模型的位置待定 |
| Giglio, Kelly & Pruitt (2016)；Surprenant (2025)；Brownlees, Pavanello & Souza (2026)；Jurado, Ludvigson & Ng (2015)；Manzan (2015) | 分位数预测与不确定性文献 | 备查：论文不做预测 |
| Wang & Li (2021)；张晓晶、刘磊 (2020) | 引言：房价是宏观下行风险的来源之一 | 备查（研究计划 10.4 节）。张晓晶、刘磊 (2020) 的题名已按 PDF 末尾的英文题名核实：Financial Risk and Economic Growth under the New Paradigm of Macro-analysis，即《宏观分析新范式下的金融风险与经济增长》；研究计划记的《外部环境与中国增长分布》有误 |
| Parente & Santos Silva（聚类夹心标准误）；Chavleishvili 等 (2021) | 限购分位数事件研究试算；讨论限购 | 备查：本文不再估计政策效应 |
| Yang, Yu & Deng (2018), *Regional Science and Urban Economics* 68 | 均值层面溢出研究的代表（69 城广义 VAR） | 备查（11-26 精简）：Funke 等和 Huang 等已覆盖；研究计划标“部分核实” |
| Sijp (2025), arXiv 2512.01139 | 地区 β 异质性的国外先例 | 备查（11-26 精简）：预印本，未经同行评审 |
| Ando, Greenwood-Nimmo & Shin (2022), *Management Science* 68(4) | 分位数关联 | 备查（11-26 精简）：方法已删去 |
| Genesove & Mayer (2001), *QJE* 116(4)；Stein (1995), *QJE* 110(2) | “调整更多体现在成交量”的理论依据 | 备查（11-26 精简）：成交量只有 10 城、只作描述；被迫抛售留 Campbell 等一篇 |
| van Dijk (2019), DNB WP 637；Machado & Santos Silva (2005), *JASA* 100(472) | 下跌期薄市场问题更重；一位小数造成的结用抖动处理 | 备查（11-26 精简）：薄市场已有 Dimson 和 Getmansky 等；抖动做法在附录里说明即可 |
| 国家统计局《房地产价格统计调查制度》（2026 年版）；《经济科学》2024 年第 5 期《住房限购、公众预期与房价调控》 | 指数编制细节；新房限价的中文证据 | 备查（11-26 精简）：统计局两个网页已够；新房限价有 Chang, Wang & Xiong (2026) |

旧库里其余文献（系统性风险指标、预测方法与评价、中国宏观下行风险）与当前研究没有直接联系，不引。

## 完整文献清单（2026-11-27）

正文要引 34 项：开题报告 11 月 27 日版的 33 条，加 Politis & Romano (1992)。33 条里你电脑上已有 25 条，统计局网页 2 条，还要下载 6 条。另有建议引的 2 篇（Case, Cotter & Gabriel 2011 已下载，Giacoletti 2021 未下载），附录与扩展一组 7 项看附录做不做。

### 还要下载的（6 项，最好 11 月 30 日前）

这 6 条都已写进开题报告，依据的是另一个对话里核对的摘要和书目，你还没有原文。至少把 Chu, Tsang & Wong (2023) 和人民银行的调查打开核对一遍：开题报告里关于房企和“五分之二的城镇家庭”的两句话直接依赖它们。

- Evans, J.L. & Archer, S.H. (1968). Diversification and the reduction of dispersion: an empirical analysis. *Journal of Finance*, 23(5), 761–767. [DOI](https://doi.org/10.1111/j.1540-6261.1968.tb00315.x)（学校账号）
- Callender, M., Devaney, S., Sheahan, A. & Key, T. (2007). Risk reduction and diversification in UK commercial property portfolios. *Journal of Property Research*, 24(4), 355–375. [DOI](https://doi.org/10.1080/09599910801916279)（学校账号；[阿伯丁大学仓储](https://aura.abdn.ac.uk/items/60f7c1c4-36db-44fe-bbd8-c41e85cea5f9/full)也有记录）
- Devaney, S. & Lee, S.L. (2005). Real estate portfolio size and risk reduction. Working Papers in Real Estate & Planning 24/05. University of Reading. [免费下载](https://centaur.reading.ac.uk/20874/)
- Chu, X., Tsang, D. & Wong, S.K. (2023). Geographic diversification and real estate firm value: where firms diversify matter. *Journal of Real Estate Research*, 45(4), 431–461. [DOI](https://doi.org/10.1080/08965803.2023.2178739)（学校账号；[港大仓储](https://hub.hku.hk/handle/10722/339625)）
- Loutskina, E. & Strahan, P.E. (2011). Informed and uninformed investment in housing: the downside of diversification. *Review of Financial Studies*, 24(5), 1447–1480. [DOI](https://doi.org/10.1093/rfs/hhq142)（学校账号；[NBER 会议稿](https://projects.nber.org/confer/2009/cfs09/strahan.pdf)免费）
- 中国人民银行调查统计司城镇居民家庭资产负债调查课题组 (2020). 2019 年中国城镇居民家庭资产负债情况调查. 《中国金融》2020 年第 9 期。知网下期刊版，顺便补上页码（开题参考文献现在没有页码）；[澎湃转载](https://www.thepaper.cn/newsDetail_forward_7119614)可先读

### 正文写作时（开题之后，3 项）

- Politis, D.N. & Romano, J.P. (1992). A circular block-resampling procedure for stationary data. In R. LePage & L. Billard (eds.), *Exploring the Limits of Bootstrap*. New York: Wiley, 263–270。只引不下。
- Giacoletti, M. (2021). Idiosyncratic risk in housing markets. *Review of Financial Studies*, 34(8), 3695–3741. [DOI](https://doi.org/10.1093/rfs/hhab033)。建议引，局限一句的出处。
- Wang, Y. Cross-validating the number of factors for prediction. 工作论文（导师的，从[导师主页](https://yapingw.github.io)下，没有就向导师要）。只在附录 C 做因子个数估计时需要。

### 已齐、正文要引的（25 项 + 2 个网页）

| 论文部分 | 文献 | 在哪里 |
| --- | --- | --- |
| 2.1 地理分散（2 项） | Cotter, Gabriel & Roll (2015)；Higgins & Fang (2012) | Cotter 等在第一组；Higgins & Fang 在“26号文件更新” |
| 2.2 共同与本地成分（7 项） | Funke, Leiva-Leon & Tsang (2019)；Huang, Jin & Zhang (2021)；郑挺国、龚金金、宋涛 (2022)；Xu & Zhang (2023)；Xu & Zhang (2024)；Wu & Bian (2018)；Yu & Zhang (2019) | 都在“26号文件更新” |
| 2.3 坏时候的分散（8 项） | Longin & Solnik (2001)；Ang & Chen (2002)；Forbes & Rigobon (2002)；Boyer, Gibson & Loretan (1999)；Bae, Karolyi & Stulz (2003)；Koenker & Bassett (1978)；Machado & Santos Silva (2019)；Hu & Fan (2022) | 第一、二组；Koenker & Bassett、Machado & Santos Silva 在“26号文件更新” |
| 机制（3 项） | 韩立彬、陆铭 (2018)；Rogoff & Yang (2024)；Glaeser & Gyourko (2005) | Rogoff & Yang 在第一组；其余在“26号文件更新” |
| 数据与测量（3 项 + 2 个网页） | Chang, Wang & Xiong (2026)；Dimson (1979)；Getmansky, Lo & Makarov (2004)；统计局 2025、2026 两个网页 | 第一、二组；网页链接见开题报告参考文献 |
| 推断（2 项） | Künsch (1989)；Menzel (2021) | 第二、三组 |

参考文献以正式发表版为准。必引文献里你手上是工作稿或会议稿的有：Cotter, Gabriel & Roll（2012 年工作稿，正式版是 RFS 28(3)）、Chang, Wang & Xiong（2025 年 NBER 稿，正式版是 RFS 39(2)）、Forbes & Rigobon、Bae 等、Rogoff & Yang、Machado & Santos Silva（2018 年会议稿）、Menzel（2017 年 arXiv 稿）、Longin & Solnik（期刊前稿）。重复的文件可以删：第一组和第二组各有一份 Ang & Chen (2002)；“26号文件更新”里 Glaeser & Gyourko 的 NBER 工作稿（留期刊重印版）和 Campbell 等的 2009 年 NBER 稿（留 2010 年稿）。那个文件夹里有四个文件名看不出是哪篇：`96975_327268.pdf` 是 Francke (2010)，`NIE_2100034 110..128.pdf` 是 Xu & Zhang (2023)，`Network_analysis_of_comovement.pdf` 是 Xu & Zhang (2024)，`14445921.2012.11104356.pdf` 是 Higgins & Fang (2012)。

### 可选（不下也不影响论证）

- 联动：时变 GAS 空间模型（Journal of Asian Economics）、贝叶斯面板 VAR（Cities 2023）、空间惩罚图 VAR（Empirical Economics 2023），作者都待核，文献综述一句带过时可引；Harding & Pagan (2006)、Meen (1999)、陈明华等 (2016)
- 尾部与分位数：国际房地产的分位数关联研究（JIMF 2025，作者待查）；空间分位数回归的房价调控研究（待核）
- 分化：Rogoff & Yang (2021), *China & World Economy* 29(1)；用 XGBoost 与 SHAP 研究 70 城房价分化的中文论文（出处待查）
- 新房：Zhou (2024)，AEA 年会论文，上海新房限价的福利损失（作者全名待核）
- 薄市场：Geltner (1991)，已由 Getmansky 等顶替
- 方法：Hendricks & Koenker (1992)；Benjamini & Hochberg (1995)（只在报告逐城检验时需要）；Davezies 等 (2021)；Lahiri (2003)；导师的 Bridging Dense and Sparse Models in High-Dimensional Quantile Regression（只在做研究计划 6.6 节可选的稠密与稀疏对照时引；同名 FAQR 另有一篇 arXiv 2508.00275，引用时要说明区别）
- 已下载、降为可选的，以及 11 月 26 日、27 日删掉的，见上一节

### 还没有答案的问题

- 研究计划（Docs 版）的标题和第 0 节还是 11 月 26 日的 A 版（“对全国市场最敏感的城市跌得最深吗？”），新主问题只写在开题报告 11 月 27 日版和第五部分锁定方案里。两份文件主问题不一致，导师看到会困惑，研究计划要同步。
- 开题报告把循环块自助只归给 Künsch (1989)。循环块是 Politis & Romano (1992) 提出的，Künsch 提出的是移动块；开题报告可以改成“(Künsch, 1989; Politis and Romano, 1992)”，多 4 个词，仍在 2,000 词以内。
- 附录 C 还做不做因子个数估计？开题报告 11 月 27 日版已不提。不做的话，Bai & Ng、Ahn & Horenstein、Bailey 等和导师的论文都降为备查。
- 新题目还没在知网查过。11 月 25 日的检索针对的是旧题目；开题报告写了“我们检索到的研究中，还没有用这种方法研究中国这轮下跌”，交稿前建议用“住房 地理分散”“房价 组合 城市”“房地产 分散化”再查一次。
- CVaR 和期望损失（ES）的定义，开题报告没有引出处；正文可以引一篇，例如 Acerbi & Tasche (2002, *Journal of Banking & Finance* 26(7))，用之前先核对。
- 数据章要回应郑挺国等 (2022) 选新房指数的三条理由（见“数据与测量”一节）；开题报告第 3 节只写了两套指数怎么编。
- 房价收入比的分子现在用国信整理的均价，正式稿要写到原始机构；附录 B 第 8 节做数据准备时一起查。
- 郑挺国等 (2022) 的两个收缩集群名单在正文表里，写引言前要读。

## 来源

本版依据：[开题报告草稿](https://claude.ai/artifact/3EnCREU8GZZuH1Mc75YGJ8)（11 月 27 日版：英文页的 33 条参考文献，据此标“开题已引”；中文对照稿末尾的研报清单）；仓库里已锁定的第五部分方案 `docs/analysis_plan_hp_part5_portfolio_20261127.md` 和结果 `results/hp_portfolio/report_portfolio.md`；附录 B 方案草稿 `docs/analysis_plan_hp_part4b_mechanism_20261127.md`；[研究计划](https://claude.ai/artifact/SpFPZ4xZf6wpvTrkfK5SuS)只取 3.10 节的研报登记（第 0 节仍是 11 月 26 日的设计）；[研报矩阵](https://claude.ai/artifact/Af73Qhz1oVcj3u9QVg996Q)；你电脑上的“ture D 文献”文件夹（11 月 27 日核对：“26号文件更新”新增的 2 个文件打开看过首页和摘要）。旧库文献的内容取自 outputs 里的文献比较矩阵和各篇精读档案。

11 月 27 日核实新增文献书目信息时检索到的页面：

- [Evans & Archer (1968)（EconPapers）](https://econpapers.repec.org/RePEc:bla:jfinan:v:23:y:1968:i:5:p:761-767)
- [Callender, Devaney, Sheahan & Key (2007)（Reading 仓储）](https://centaur.reading.ac.uk/29413/)
- [Devaney & Lee (2005)（Reading 仓储）](https://centaur.reading.ac.uk/20874/)
- [Chu, Tsang & Wong (2023)（IDEAS）](https://ideas.repec.org/a/taf/rjerxx/v45y2023i4p431-461.html)；[港中大商学院的介绍](https://cbk.bschool.cuhk.edu.hk/when-emerging-cities-offer-better-real-estate-returns/)
- [Loutskina & Strahan (2011)（EconPapers）](https://econpapers.repec.org/RePEc:oup:rfinst:v:24:y:2011:i:5:p:1447-1480)
- [人民银行 2019 年城镇居民家庭资产负债调查（澎湃转载）](https://www.thepaper.cn/newsDetail_forward_7119614)；[《中国经济周刊》的报道](https://paper.people.com.cn/zgjjzk/html/2020-05/15/content_1987791.htm)
- [Giacoletti (2021)（DOI）](https://doi.org/10.1093/rfs/hhab033)

先前核实出处时打开的页面：

- [Rogoff & Yang, A Tale of Tier 3 Cities（NBER）](https://www.nber.org/papers/w30519)
- [Adrian 等, Predicting Downside Risks to House Prices（IMF WP 20/11）](https://www.imf.org/en/publications/wp/issues/2020/01/17/predicting-downside-risks-to-house-prices-and-macro-financial-stability-48932)
- [IMF GFSR 2019 年 4 月第 2 章](https://www.imf.org/-/media/files/publications/gfsr/2019/april/english/ch2.pdf)
- [Chang, Wang & Xiong, Price and Volume Divergence（NBER WP 34303）](https://ideas.repec.org/p/nbr/nberwo/34303.html)
- [Hu & Fan, Risk contagion across regional housing markets in China](https://ideas.repec.org/a/eee/ecmode/v115y2022ics0264999322001912.html)
- [Mink, Jacobs & de Haan, Measuring coherence of output gaps](https://econpapers.repec.org/RePEc:oup:oxecpp:v:64:y:2012:i:2:p:217-236)
- [Kallberg, Liu & Pasquariello, Price comovement of U.S. residential real estate](https://econpapers.repec.org/RePEc:bla:reesec:v:42:y:2014:i:1:p:71-108)
- [Fang, Gu, Xiong & Zhou, Demystifying the Chinese Housing Boom](https://www.nber.org/papers/w21112)
- [Case, Cotter & Gabriel, Housing risk and return（arXiv）](https://www.arxiv.org/abs/1103.5971)
- [Sun, Zheng, Geltner & Wang, Home purchase restrictions in Beijing](https://dspace.mit.edu/server/api/core/bitstreams/ff203123-ddf9-4876-9436-5545703f6180/content)
- [陈明华等 (2016)、刘海云和吕龙 (2018) 的书目信息](https://xbzs.ecnu.edu.cn/CN/Y2026/V58/I3/167)

已下载的文献都逐一打开你的 PDF 核对过是哪一篇。工作稿版本不含期刊卷期，写参考文献时以期刊版为准。
