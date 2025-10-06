---
description: Split Rewards, not Hairs
---

# Part 3: Proportional Reward Splitting



**Warning**: This post is [**a draft**](./). Please don't read it before reading [this](https://shai-deshe.gitbook.io/parallel-thoughts/drafts/drafts). For the parts that were already published as non-drafts, see [here](../../proof-of-work/fixing-bitcoins-incentive-alignment/).

> **Acknowledgement**
>
> This post was funded by the [Quai network](https://qu.ai/), which generously provided me with a grant to fund my proof-of-work education efforts.

We are ready at last to present the protocol that motivated this entire series: [_Proportional Reward Splitting_](https://arxiv.org/abs/2503.10185) (PRS).

The key difference between PRS and FC is in the name: _proportionality_. In FC, _each fruit has the same reward_. In PRS, we have a fixed reward for each height, and it is distributed equally to shares harvested at this height. This is a subtle yet profound difference.

## Quick Recap

[In the first post](../../proof-of-work/fixing-bitcoins-incentive-alignment/part-i-bitcoin.md), we described _selfish mining_, a phenomenon first observed on Bitcoin by Eyal and Sirer. We recast this discovery as a (bounded) violation of a retrofitted security property called [_fairness_](https://shai-deshe.gitbook.io/parallel-thoughts/proof-of-work/fixing-bitcoins-incentive-alignment/part-2-fruitchains#fairness)_._ We roughly defined fairness as the assertion that, over a sufficiently long period of time, the proportion of rewards collected by an $$\alpha$$-miner should converge to $$\alpha$$.

This motivated Pass and Shi to create the FruitChains protocol, which we discussed at great length in [the second post](../../proof-of-work/fixing-bitcoins-incentive-alignment/part-2-fruitchains.md).

Pass and Shi manage to align the incentives properly, but their protocol has a strong technical caveat: the regimes of parameters in which its security analysis holds are highly impractical. In other words, in any possible instantiation, the _rate_ at which the $$\alpha$$ miner's fraction of the rewards converges to something close to $$\alpha$$ is _much too slow_.

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

## Block Anchoring

Recall the very straightforward way FC handles orphaned blocks: _it doesn't care_. Each fruit stores the _height_ at which it was harvested, and a fruit created at height $$h$$ can be packed by any block created at a height $$h'$$ such that $$0<h'-h<R$$  where $$R$$ is the freshness window.

In PRS, things work a little differently. Each workshare references a _specific block_. What do we do with this reference? Assume for now that only workshares harvested on the selected chain count. So for example, in this case (I'm still using fruits to represent workshares because I like fruits):

<figure><img src="../../.gitbook/assets/image (5).png" alt=""><figcaption></figcaption></figure>

workshare A will count, but workshare B will not.

In a moment, we will see why this is _not_ the correct way to determine workshare validity. But for now, notice that it makes a lot of sense. The key benefit is that, since only the main chain determines what workshares count, the only way to change the reward splitting for a level retroactively is via a reorg. This property has at least two benefits: it increases stability and simplifies and localizes the computation of the reward distribution. Another benefit, which is outside of our current scope, is that computing rewards this way is compatible with the PoEM rule for choosing the main chain.

<details>

<summary>Challenge: Is this a security necessity?</summary>

For some reason, it seems "obvious" to me that "height-anchored PRS" should not be secure. However, my attempts to find an explicit selfish mining attack failed. "Height-anchored PRS" was not analyzed anywhere, because what's the point? Still, I remain in the dark about whether it's a security necessity or "just" a smart engineering choice.

I will reward 100 Quai to whoever produces the first argument that could convince me of either side. You can present your attempt in the X thread. (AI slop will be ignored on sight.)

</details>

So what is the problem with only looking at the main chain? Perhaps this picture will give you a hint:

<figure><img src="../../.gitbook/assets/image (6).png" alt=""><figcaption></figcaption></figure>

### 2 Selfish 2 Mining

It turns out that using this policy above reintroduces selfish mining. That shouldn't come as a great surprise: FruitChains solved selfish mining by decoupling block creation from fruit inclusion, only allowing workshares on the selected chain _couples them back!_

An adversary can follow any selfish-mining attack on Bitcoin (e.g., Eyal-Sirer), while also packing all workshares to their own blocks. If they manage to orphan an honest block, they get an **unfair advantage** because the blocks they introduced instead **only anchor their own workshares**. It is true that honest miners can retroactively add more shares to the adversary block, but why would they? They'd rather harvest on more recent blocks that have fewer workshares already anchored to them. So even in this scenario, only harvesting to newer blocks, leaving the adversary with their advantage, is not only honest but _rational_.

### Hahaha, You Said "Knob"

So how can we use block anchoring in a more subtle way?

Simple, we _allow repacking from uncle blocks_, as long as the repacking is on the _main chain._ Consider this scenario:

<figure><img src="../../.gitbook/assets/image (10).png" alt=""><figcaption></figcaption></figure>

The block $$C$$ packs the workshare $$B$$, but that doesn't matter, since $$C$$ is not on the main chain. _However_, $$D$$ _also_ packs $$B$$, so it _is_ counted.

Astute readers might scratch their heads and wonder: Doesn't this completely undermine the purpose of harvest blocks? How is this any better than just using height?

The answer is that it gives is an _extra knob_. Another parameter to tweak. That parameter is the _allowed uncle distance_.

In a blocktree, the "uncle distance" for each block is its distance from the selected _chain_. For example, I wrote the uncle distance for all blocks in the following tree, assuming the longest chain selection rule:

<figure><img src="../../.gitbook/assets/image (11).png" alt=""><figcaption></figcaption></figure>

<details>

<summary>What should the uncle distances above be, assuming PoEM is used instead of the longest chain? (assume constant difficulty, i.e., that all blocks in the drawing have the same difficulty target)</summary>

**Trick question!** In PoEM, the _actual hashes_ of the headers are needed to determine the selected chain, even when the difficulty is constant. Without this extra information, it is impossible to determine the selected chain.

</details>

We can also give a _relative_ definition. Given blocks $$A$$ and $$B$$, the _uncle distance_ from $$B$$ to $$A$$ is the distance of $$A$$ from the selected chain of $$B$$. So what we first called the _uncle distance_ of $$A$$ can also be called the uncle distance from _the selected tip_ to $$A$$. This is compatible with the fact that every block is created as if it _is_ the selected tip.

Moving forward, the key is to limit the allowed uncle depth, which we will denote by $$K$$. Why is this useful? We will see very soon.

### Putting Everything Together

The conclusion to all of this is that PRS has two knobs. The workshare-eligibility $$W$$ and the uncle depth $$K$$. Together they form a nice eligibility policy.&#x20;

**Definition**: A workshare $$ws$$ harvested at block $$A$$ of height $$h$$ is _eligible_ for block $$B$$ of height $$h'$$ if the following two conditions hold:

1. $$0<h'-h\le W$$
2. The uncle distance from $$A$$ to $$B$$ is at most $$K$$.

Typically, we set $$K$$ much smaller than $$W$$. $$K$$ should represent a depth beneath which forks are sufficiently unlikely. For example, taking a cue from Bitcoin, we can set $$K=6$$. The freshness parameter $$W$$, on the other hand, should be larger, to allow the shares time to converge.

Setting $$K$$ positive to allow "salvaging" workshares lost to shallow forks removes the selfish mining attack introduced by block-harvesting. Making it much smaller than $$W$$ (which needs to be much larger for other reasons anyway) retains the benefits of block-harvesting, at least approximately.

(add some examples)

And _this_ is how packing is allowed in PRS.

Let us summarize this in a table (which you are encouraged to compare with the [FruitChains table](../../proof-of-work/fixing-bitcoins-incentive-alignment/part-2-fruitchains.md#fruitchains-protocol-summary)):

<details>

<summary>Proportional Reward Splitting protocol summary</summary>

### Parameters

* Eligibility bound $$W$$  (a.k.a recency bound) — how long before we are not allowed to pack a workshare
* <mark style="color:purple;">Forking bound</mark> $$K$$  <mark style="color:purple;">(a.k.a recency bound) — how far can the workshare's harvest block be from the selected chain</mark>
* Workshare rate $$\lambda$$ — expected number of fruit per single block delay

### Minable objects

**Fruits** and **baskets**:

|                      | Block                                                                                                                                | Workshare                                                                                                                                                                                                                               |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Difficulty**       | High                                                                                                                                 | Low ($$\lambda$$ times easier than a basket), but not as low as fruits.                                                                                                                                                                 |
| **Fields**           | <ul><li>Parent</li><li>List of packed fruit</li><li>List of transactions</li></ul>                                                   | <ul><li><mark style="color:purple;">Harvest block</mark></li></ul><ul><li>List of txns</li></ul><ul><li>Receiver address</li></ul>                                                                                                      |
| **Weight**           | Fixed                                                                                                                                | **None**<mark style="color:purple;">**?**</mark>                                                                                                                                                                                        |
| **Rewards**          | **None**                                                                                                                             | Fixed amount of reward ist distributed **equally among all shares of this height**                                                                                                                                                      |
| **Validation Rules** | <ul><li>Packed fruit are fresh</li><li>Transactions contained in packed fruits</li><li>Transactions consistent with parent</li></ul> | <ul><li>Valid harvest height</li><li>Transactions consistent with harvest point</li><li><p>Packed workshares are both <em>fresh</em> and <em><mark style="color:purple;">harvested close to main chain</mark></em></p><p></p></li></ul> |

### Honest miners

We define honest behaviour as follows:

* Mine fruits and baskets **simultaneously**
* The fruits and baskets are valid
* The fruit harvest point is always the heaviest basket
* The basket contains all known, still fresh, yet to be packed fruit
* Once a fruit or a basket is discovered, it is immediately broadcast to the entire network

</details>

## PRStimating

So how does PRS perform? How does it improve upon FruitChains?

### Fairness

The first thing we should ask ourselves is _how fair is it_. We consider the fairness averaged over $$T$$ consecutive heights. Say that an $$\alpha$$ miner earned a fraction $$\rho$$ of the rewards within the window, then we would like to bound $$|\rho-\alpha|$$ in terms of the window length $$T$$, the protocol parameters, and perhaps also the network latency.

The weakest form of fairness is the statement that $$|\rho-\alpha|$$ _eventually_ goes to zero. But that's not enough for us, because we want to have guarantees on _how fast_ it goes to zero.

What is the _strongest_ possible fairness?

Since mining is an independent process, we can rely on something called the central limit theorem to conclude the absolute best we can hope for is $$|\rho-\alpha| = \theta(1/\sqrt{T})$$. This is the natural noise of independent samples that cannot be avoided. Even if we are guaranteed to have zero orphans and that everyone is honest, there is still _some noise_ [inherent to the block production process](https://shai-deshe.gitbook.io/pow-book/supplementary-material/math/probability-theory/the-math-of-block-creation). So it is only natural to assess the performance of our protocols in this metric.

Our analysis of FruitChains provided us with the following approximation, for carefully selected values of the freshness bound $$R$$ and fruit rate $$\lambda$$:

$$
|\rho-\alpha| \le O\left(\frac{\Delta}{R} + \frac{1}{\sqrt{\lambda T}} \right)
$$

where $$\Delta$$ is the network latency. Understanding this formula quantitatively requires stripping away the asymptotics and diving into the constants, but even from the asymptotics we see the limitations casting their shadows. First, the presence of $$\Delta$$ as a linear term implies that the convergence time is very sensitive to network latency, and it seems that the only knob to adjust it is $$R$$. The devil is in the fact that we must have $$T\ge R$$. Why is that? Because we have to wait _at least_ the freshness bound. So on one hand, increasing $$R$$ is the _only_ way we have to increase fairness (recall that increasing $$\lambda$$ forces increasing $$R$$ as well), but on the other hand, this comes with decreased responsiveness. Another reason we'd like to avoid inceasing $$\lambda$$ is that it directly increases bandwidth requirement.

The PRS analysis gives a completely different tradeoff:

$$
|\rho-\alpha| \le O\left(\frac{K}{W} + \frac{1}{\sqrt{T}} \right)
$$

The benefit here is very clear: the possible unfairness is completely determined by $$K$$ and $$W$$, two parameters that have no bearing on the bandwidth, and are not correlated with the sampling error. Since $$K\ll W$$, we get very close to optimal selfish mining without running into impractical assumptions.

But there's obviously the other side of the tradeoff. In the PRS analysis, we find that the selfish mining threshold has the form $$\frac{1}{2} - 2\frac{K}{W}$$, unlike FruitChains, where it is $$\frac{1}{2} - \frac{1}{R}$$. This actually makes it _significantly harder_ to reach very close to $$1/2$$. This is not a bug, but a feature: FruitChains _forces_ us to choose large $$R$$, in PRS, we can choose a bound that we like, measure an approriate $$K$$ from observing the network, and then choose $$W$$ accordingly.

It is not _quite_ true that the network latency doesn't appear at all in the analysis. It is neatly hidden in how we choose $$K$$. But its effect on the parameterization of the protocol is much weaker.

### Trust Model

A unique feature of the PRS analysis, which does not hold for the FruitChain analysis or most protocol analyses, is the reduction of the honest assumption.

The security of FruitChain holds in a model where there is an honest majority. This is a reasonable assumption, but still a relatively strong one, which we would like to reduce. In a perfect system, the rational majority coincides with the honest majority.

Relying entirely on game-theoretic considerations is complicated, and most analyses, including FruitChains', show that if _enough_ of the network is honest, then it is _rational_ for the rest of the network to remain honest. The PRS analysis shows that rational behaviour is an equilibrium, even assuming no honest players. Some would call such a protocol "self-enforcing".

### Incentive Alignment and Future Goals

But PRS _does_ inherit one drawback from FC: the degeneracy.

Recall that we had a problem with FruitChains: nothing incentivizes miners to point at other miners' fruit. It is true that honest behavior is an equilibrium, but it is _not_ unique. In fact, there is a parameter that we can freely change (determining the probability of including fruits created by someone else) without affecting the expected outcome in any way. This is called a _degeneracy_, and since this degeneracy begets strategies that are inoptimal for the protocol, it is a problem.

A straightforward approach to a solution is to add weight to the workshares themselves, thereby putting workshare-omitting miners at a disadvantage. However, this should be done _very carefully_, as it undermines the decoupling we worked so hard to achieve between chain selection and reward distribution.

The hope, at least as I see it, is for finding another "knob" that will allow us to incentivize inclusiveness at the expense of a _controlled_ trade-off of the benefits of the degenerate world. For example, we might find that an increase in share weight requires a _proportional_ increase in the required honest fraction. Such a knob will allow us to make decisions such as "increase the share weight as much as possible without raising the honesty requirement beyond 10%". Of course, this is just one possible scenario out of many.

There is currently an interesting ongoing debate among the Quai developers and collaborators on these questions: What are the consequences of increasing share weight in terms of the honesty model and profitability thresholds? What is the correct way to choose share rates and weights? How do we juggle an array of properties — honesty requirements, incentive alignments, profitability threshold, expected profit, convergence time, and so on — which admit a great deal of subtlety within themselves and even more subtle interactions with each other? Is the share weight even the right parameter, or do we need a fancier knob?

Finding a way to balance out all these requirements into a trade-off that provides sufficient guarantees to _all_ aspects is the art of protocol crafting. By watching or participating in the process of improving PRS, you can see this fascinating process unfold in real time.
