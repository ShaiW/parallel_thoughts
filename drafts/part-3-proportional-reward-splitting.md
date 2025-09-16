---
description: Split Rewards, not Hairs
---

# Part 3: Proportional Reward Splitting

**Warning**: This post is [**a draft**](./). Please don't read it before reading [this](https://shai-deshe.gitbook.io/parallel-thoughts/drafts/drafts). For the parts that were already published as non-drafts, see [here](../proof-of-work/fixing-bitcoins-incentive-alignment/).

We are finally ready to present the protocol that motivated this entire series, the [_proportional reward splitting_](https://arxiv.org/abs/2503.10185) mechanism.

In previous posts, we described _selfish mining_, a phenomenon first observed on Bitcoin by Eyal and Sirer, and explained how it leads to a security property known as _fairness._ We roughly defined fairness as the assertion that, over a sufficiently long period of time, the proportion of rewards collected by an $$\alpha$$-miner should converge to $$\alpha$$.

We noted that the selfish mining attack by Eyal and Sirer demonstrates that Bitcoin lacks the fairness property, even assuming an honest majority of miners!

This motivated&#x20;
