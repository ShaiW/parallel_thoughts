---
description: Split Rewards, not Hairs
---

# Part 3: Proportional Reward Splitting

**Warning**: This post is [**a draft**](./). Please don't read it before reading [this](https://shai-deshe.gitbook.io/parallel-thoughts/drafts/drafts). For the parts that were already published as non-drafts, see [here](../../proof-of-work/fixing-bitcoins-incentive-alignment/).

> **Acknowledgement**
>
> This post was funded by the [Quai network](https://qu.ai/), which generously provided me with a grant to fund my proof-of-work education efforts.

We are ready at last to present the protocol that motivated this entire series: [_Proportional Reward Splitting_](https://arxiv.org/abs/2503.10185) (PRS).

## Quick Recap

[In the first post](../../proof-of-work/fixing-bitcoins-incentive-alignment/part-i-bitcoin.md), we described _selfish mining_, a phenomenon first observed on Bitcoin by Eyal and Sirer. We recast this discovery as a (bounded) violation of a retrofitted security property called [_fairness_](https://shai-deshe.gitbook.io/parallel-thoughts/proof-of-work/fixing-bitcoins-incentive-alignment/part-i-bitcoin#chain-quality-and-lack-thereof)_._ We roughly defined fairness as the assertion that, over a sufficiently long period of time, the proportion of rewards collected by an $$\alpha$$-miner should converge to $$\alpha$$.

This motivated Pass and Shi to create the FruitChains protocol, which we discussed at great length in [the second post](../../proof-of-work/fixing-bitcoins-incentive-alignment/part-2-fruitchains.md).

Pass and Shi manage to properly align the incentives, but their protocol has a strong technical caveat: the regimes of parameters in which its security analysis holds are highly impractical. In other words, in any possible instantiation, the _rate_ at which the $$\alpha$$ miner's fraction of the rewards converges to something close to $$\alpha$$ is _much too slow_.

This is an example of a problem that PRS _solves_.

A second property of FruitChains that we do not like is the necessity of the honest assumption. FC improves upon Bitcoin in that the honest strategy is rational, but it is not the _only_ rational strategy. In particular, the "only pack your own fruit" strategy is perfectly rational, but if a majority of miners follow it, FruitChain will revert to Bitcoin.

This is an example of a problem that PRS _doesn't solve_. In fact, it is the motivation for the currently ongoing further research, which we will touch on at the end of the post.

<details>

<summary>We can use a more precise notation to measure the fairness violation</summary>

We say that the chain is $$(\alpha,\epsilon)$$-_fair_ if a $$(1-\alpha)$$ honest majority implies that the profit of any dishonest miner is at most $$\alpha(1+\epsilon)$$. For example, if an $$\alpha$$-miner has a strategy that increases her profit by 10%, then the chain is _not_ $$(\alpha,0.1)$$-fair.

**Exercise**: Complete the statement correctly: $$(\alpha,\epsilon)$$-fairness implies $$(\alpha',\epsilon')$$-fairness whenever $$\alpha'\le\alpha$$ and \_\_\_\_\_

A perfect chain is $$(1/2,0)$$-fair, which turns out to be good to be true.

We can nicely fit selfish mining strategies such as Eyal-Sirer into this mold. Eyal and Sirer's analysis assumes an $$\alpha$$ miner with a probability of $$\gamma$$ to win a tie (which arguably proxies her connectivity). When making a security statement, we always assume that the adversary is the strongest possible in any respect not parametrized in that statement. Since we only want to consider the adversary fraction $$\alpha$$, we assume that $$\gamma=1$$, as this describes the most powerful $$\alpha$$ miner. Eyal and Sirer exactly compute the expected profit of an $$\alpha$$ miner deploying their strategy, from which the corresponding $$\epsilon_\alpha$$ can be recovered. The exact value of $$\epsilon_\alpha$$ is available in the paper, but it is a bit messy, so I will not reproduce it.

Eyal-Sirer's results imply that Nakamoto Consensus is not $$(\alpha,\varepsilon_\alpha)$$-fair.

This notation makes it easy to talk about arbitrary approximation. For example, while a perfect chain does not exist, FruitChains provides a recipe for constructing a $$(1/2-\delta,\epsilon)$$ chain for any $$\delta,\epsilon>0$$. The key is that $$\delta,\epsilon$$ must be chosen _in advance_, and then the recipe tells you ways to choose the fruit rates and freshness window length that will provide the requested security.

</details>

## The Risks of Proportionality

The key difference between PRS and FC is in the name: _proportionality_. In FC, _each fruit has the same reward_. In PRS, we have a fixed reward for each _block_ (actually, as we'll shortly see, for each _level_), and it is distributed equally to shares that are anchored to this block. So the cut each miner gets is proportional to the fraction of shares they anchored.

This is a subtle yet profound difference. The key issue is that it is much more sensitive to _delayed shares_. In FC, incoming packed fruits do not affect the value of already dispensed rewards. In PRS, any new workshare that points to a block $$B$$ _reduces_ $$B$$'s per share payout.

If we are not careful, this could allow a new form of selfish mining. Say that the current tip of the network is the block $$B$$.

The honest network will mine workshares over the blocks, and other blocks will include them. So one block later, the honest network might have this view (I'm still using fruit to designate workshares because I like fruit)

### Workshare-Eligibility

In PRS, like FC, a workshare $$ws$$ is a "low difficulty" object that is supposed to represent a "unit of participation". Each workshare must contain a reference to a single _block_ that we denote $$ws.base$$. This _base block_ is nothing but an attestation to the time $$ws$$ was created, like taking a picture with today's newspaper. (Of course, $$ws$$ can point at _any_ block, as long as it already exists, but pointing at anything but the tip of the best chain only harms the miner.)

The purpose of workshare eligibility is to make sure that a block does not include "stale" workshares that are more than $$W$$ blocks old. This description might lead you to assume that the eligibility condition should be "For any workshare $$ws$$ that $$B$$ is pointing at, $$ws.base$$ is at most $$W$$ blocks below $$B$$", but that is not quite the case. The problem is that $$ws.base$$ is _not necessarily below_ $$B$$. Huh? Let's explain what's going on.

<details>

<summary>Unique chain inclusion assumption</summary>

For this definition to make sense, we also have to assume that if $$B$$ points at $$ws$$,  then no block below $$B$$ points at $$ws$$. Otherwise, we might consider $$B$$ invalid for pointing at a workshare that his grandparents already included. The paper does not make this assumption, and it is easy to generalize anything that we do to work without it, but it makes everything messier for no particular gain, so I am just going to make this assumption implicitly

</details>

### Uncle Lovers

Consider the following situation:

<figure><img src="../../.gitbook/assets/image.png" alt=""><figcaption></figcaption></figure>

As a miner planning their next, you might find yourself in a dilemma:

<figure><img src="../../.gitbook/assets/image (1).png" alt=""><figcaption></figcaption></figure>

Stress not, miner! We love _uncle blocks_ here. This means that you are allowed to enjoy both worlds!

There is nothing preventing you from doing something like this:

<figure><img src="../../.gitbook/assets/image (2).png" alt=""><figcaption></figcaption></figure>

The block A is called an _uncle block_ of B. This terminology is surprisingly exact. For $$A$$ to be an uncle of $$B$$ we must have that $$A$$ and $$B$$ are on separate chain, but that $$A$$ is higher than $$B$$. Just like how your (first) uncle was born in your parents' generation!

However, to truly accommodate uncles, we must make our definitions uncle-friendly.

### Workshare-Eligibility Revisited

Adapting the definition is straightforward. For every block $$B$$, let $$h(B)$$ be its distance from the genesis block (it's "generation"). The workshare-eligibility rule requires:

> A block $$B$$ is only allowed to point at the workshare $$ws$$ if it satisfies $$h(B) \le h(ws.base) + W$$

This assures that blocks are allowed to point at workshares not based on their chain, as long as the height difference is within the parameter.

This means that workshares do not get lost even as a result of a reorg. As long as the reorg is shallow enough, the workshares based on the "wrong side" of the reorg are still usable. This already provides a strong intuition as to how PRS prevents the Eyal-Sirer attack: using withheld blocks to orphan honest blocks won't help you gain more profit, as the makeup of the workshares remains the same.

### Fork-Eligibility

Uncle blocks add, quite literally, a new dimension to our workshare supply. If we disregard uncles, then all workshares are based on the same chain, which makes workshare-eligibility enough to seal the ability to add new shares to a sufficiently old block.

(sketch of dilution attack, explain the fork rule and how it resolves it)
