# AI History Causal Chain Verification Results

Verified: 2026-06-06
Skill: ai-history-basics v2.3+

## Day 1-6 (1950-1980s)

| Chain | Accuracy | Issue |
|-------|----------|-------|
| 1→2 (AI concept → Perceptron) | Medium | Neural net origins more complex than just "thinking machines" |
| 2→3 (Perceptron limits → AI Winter) | Low | Perceptron criticism was ONE cause, not THE cause. Also: Lighthill Report 1973, DARPA cuts |
| 3→4 (Generic AI failure → Expert Systems) | High | Accurate |
| 4→5 (Expert System limits → Backpropagation) | Low | Parallel events, not directly causal. Backprop was algorithm breakthrough (Rumelhart 1986), motivated by connectionism not expert system failure |
| 5→6 (Expert System costs → 2nd AI Winter) | High | Accurate, but also Lisp machine crash, Japan 5th Gen failure |

**Fixes applied**: Added Lighthill Report, DARPA cuts as co-causes. Changed Day 4→5 to "algorithm breakthrough + connectionism revival".

## Day 7-12 (1990-2012)

| Chain | Accuracy | Issue |
|-------|----------|-------|
| Day 7 (NN stagnation → SVM) | Medium | Coexisted, not replacement. SVM provided mathematical rigor |
| Day 8 (Image recognition → CNN) | Medium | CNN originated 1980 (Neocognitron), not 1990s |
| Day 9 (Sequence processing → RNN) | Medium | RNN concept dates to 1943, LSTM 1995 |
| Day 10 (Training expensive → GPU) | Accurate | But CUDA wasn't designed for AI originally |
| Day 11 (Can't prove progress → ImageNet) | Accurate | Core motivation: data bottleneck, not just benchmarking |
| Day 12 (GPU+BigData+CNN → AlexNet) | Fully accurate | 2012, 15.3% vs 26.2% top-5 error |

**Key papers**:
- Fukushima 1980: Neocognitron (CNN origin)
- LeCun 1998: LeNet-5
- Hochreiter & Schmidhuber 1997: LSTM
- Krizhevsky, Sutskever, Hinton 2012: AlexNet

## Day 13-18 (2013-2017)

| Chain | Accuracy | Issue |
|-------|----------|-------|
| Day 13 (BOW limits → Word2Vec) | Medium | Word2Vec solved semantic capture, not BOW directly. Bengio 2003 NNLM was earlier |
| Day 14 (Translation → Seq2Seq) | Accurate | Sutskever et al. 2014 |
| Day 15 (Long sequence → Attention) | Accurate | Bahdanau et al. 2014 |
| Day 16 (RNN can't parallel → Transformer) | Accurate | Vaswani et al. 2017, paper explicitly states this |
| Day 17 (Global understanding → Self-Attention) | Accurate | O(1) path length vs O(n) for RNN |
| Day 18 (Parallel loses position → Positional Encoding) | Accurate | Self-attention is permutation invariant |

**Key papers**: Mikolov 2013, Sutskever 2014, Bahdanau 2014, Vaswani 2017

## Day 19-30 (2018-2022)

All 12 causal relationships verified as accurate. No issues.

## Day 31-42 (2020-2024)

| Item | Status | Note |
|------|--------|------|
| Day 40 Skills | Needs clarification | Term not formally standardized yet |

All others accurate.

## Day 43-60 (2024-2026)

All 18 concepts verified as accurate. Minor notes:
- Vibe Coding term coined Feb 2025 (Karpathy)
- A2A protocol released April 2025 (Google)
- Context Engineering term formalized 2024-2025
