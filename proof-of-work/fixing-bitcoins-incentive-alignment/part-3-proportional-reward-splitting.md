---
description: Split Rewards, not Hairs
---

# Part 3: Proportional Reward Splitting

> **Acknowledgement**
>
> This post was funded by the [Quai network](https://qu.ai/), which generously provided me with a grant to fund my proof-of-work education efforts.

We have dedicated two lengthy posts to exploring incentive alignment in blockchains. We first reviewed the phenomenon of selfish mining on Bitcoin and how it suggests the definitions of chain quality and fairness. We proceeded to examine the FruitChains protocol, and discuss at length its benefits and drawbacks, culminating in the unfortunate realization that — while solving all problems asymptotically — it can not be reasonably parameterized.

Now, we are finally in a position to present the protocol that motivated this entire series: [_Proportional Reward Splitting_](https://arxiv.org/abs/2503.10185) (PRS).

The key difference between PRS and FC is in the name: _proportionality_. In FC, _each fruit has the same reward_. In PRS, each share has a well-defined _height_. The amount of reward emitted at each _height_ is fixed and is distributed _equally_ among _all shares_ of that height. This is a subtle yet profound difference. (Note that FruitChains also classifies blocks by height, but only for tracking freshness. Height does not affect the reward distribution.)

This is a subtle yet profound difference. In part because a new share retroactively affects the rewards gained by preexisting shares of the same height, making liveness trickier.

## Quick Recap

[In the first post](part-i-bitcoin.md), we described _selfish mining_, a phenomenon first observed on Bitcoin by Eyal and Sirer. We recast this discovery as a (bounded) violation of a retrofitted security property called [_fairness_](https://shai-deshe.gitbook.io/parallel-thoughts/proof-of-work/fixing-bitcoins-incentive-alignment/part-2-fruitchains#fairness)_._ Roughly, we defined $$\alpha$$-fairness as the assertion that as we consider increasingly long time frames, the proportion of rewards collected by an $$\alpha$$-miner should converge to $$\alpha$$.

By furnishing a profitable selfish mining strategy, Eyal and Sirer demonstrated that Bitcoin is not $$\alpha$$ fair for a wide range of $$\alpha$$ values (the exact range depends on the underlying network conditions, but even at optimal conditions, their strategy shows that $$\alpha$$-fairness is impossible for any $$\alpha>1/3$$).

Selfish mining motivated Pass and Shi to create the FruitChains protocol, which we discussed at great length in [the second post](part-2-fruitchains.md).

### Incentive Alignment

FruitChains achieves perfect incentive alignment, but with a significant technical caveat: it only works in highly impractical parameter regimes. In other words, the time it takes the $$\alpha$$-miner's reward proportion to converge to a value close to $$\alpha$$ is _very long_, while the required rate of fruit production is _unreasonably high_. It is _not known_ whether FruitChains remains secure in reasonable parameter regimes. However, the security analysis strongly relies on assuming these regimes, and most would agree that analysing FruitChains in any other regime will require a brand new approach.

PRS solves this problem by providing a new trade-off: it allows exchanging the quality of incentive alignment for efficiency. This allows architects to choose a _sweetspot_ where the incentive alignment is sufficiently strong (for example, the practical parametrization discussed in the paper guarantees $$\alpha$$-fairness for any $$\alpha<0.42$$), yet the protocol is quick and lean enough for everyday applications.

<details>

<summary>We can use a more precise notation to measure the fairness violation</summary>

We say that the chain is $$(\alpha,\epsilon)$$-_fair_ if a $$(1-\alpha)$$ honest majority implies that the profit of any dishonest miner is at most $$\alpha(1+\epsilon)$$. For example, if an $$\alpha$$-miner has a strategy that increases her profit by 10%, then the chain is _not_ $$(\alpha,0.1)$$-fair.

**Exercise**: Complete the statement correctly: $$(\alpha,\epsilon)$$-fairness implies $$(\alpha',\epsilon')$$-fairness whenever $$\alpha'\le\alpha$$ and \_\_\_\_\_

A perfect chain is $$(1/2,0)$$-fair, which turns out to be good to be true.

We can nicely fit selfish mining strategies such as Eyal-Sirer into this mold. Eyal and Sirer's analysis assumes an $$\alpha$$ miner with a probability of $$\gamma$$ to win a tie (which arguably proxies her connectivity). When making a security statement, we always assume that the adversary is the strongest possible in any respect not parametrized in that statement. Since we only want to consider the adversary fraction $$\alpha$$, we assume that $$\gamma=1$$, as this describes the most powerful $$\alpha$$ miner. Eyal and Sirer exactly compute the expected profit of an $$\alpha$$ miner deploying their strategy, from which the corresponding $$\epsilon_\alpha$$ can be recovered. The exact value of $$\epsilon_\alpha$$ is available in the paper, but it is a bit messy, so I will not reproduce it.

Eyal-Sirer's results imply that Nakamoto Consensus is not $$(\alpha,\varepsilon_\alpha)$$-fair.

This notation makes it easy to talk about arbitrary approximation. For example, while a perfect chain does not exist, FruitChains provides a recipe for constructing a $$(1/2-\delta,\epsilon)$$ chain for any $$\delta,\epsilon>0$$. The key is that $$\delta,\epsilon$$ must be chosen _in advance_, and then the recipe tells you ways to choose the fruit rates and freshness window length that will provide the requested security.

</details>

### Rational Equilibrium

A second property of FruitChains that is less than ideal is the necessity of an honest majority. The feat FruitChain achieves is that if at least half of the network is _honest_, then it is rational to follow the honest strategy.

This is a great improvement over Bitcoin, where a sufficiently large (yet still much smaller than $$\alpha=1/2$$) rational miner will choose to selfish mine even if _all_ remaining miners are honest. However, we would ideally want to remove the honesty assumption altogether, and only assume that a majority of miners is _rational_ (which is the minimal possible requirement, as a blockchain with a Byzantine majority cannot stand). And that's exactly what the PRS paper shows.

### Equilibria Degeneracy

The third issue we recognized in FruitChains is that the equilibrium is _degenerate_. Note the careful phrasing in the previous subsection: "it is rational to follow the honest strategy." Why not "rational miners will follow the honest strategy"? Ah, because as we noted, that's not the _only_ rational strategy.

The problem is that there are decisions that miners can make that, on the one hand, affect the convergence, but on the other hand, do not affect the miner's expected profit. More concretely, FruitChains define the honest strategy as "packing all fruit you can", but what prevents a miner from only packing their own fruit? It's easier, and it doesn't lose any reward. Furthermore, if all miners choose this strategy, the benefits of FruitChains fade away.

Mathematically, we say that the honest strategy is a _degenerate equilibrium_. It is only a point in an entire section of equally profitable strategies. And it turns out that "baveling" the equilibrium to become unique is quite tricky.

This is a problem that PRS _doesn't solve_. And solving it is the motivation for the currently ongoing further research, which we will touch on at the end of the post.

## Block Anchoring

FruitChain deals with orphaned blocks in a very straightforward way: _it doesn't care_. Each fruit of a given height can be repacked by any (sufficiently old) block. A fruit harvested at height $$h$$ can be packed by any basket with height $$h'$$, as long as $$0<h'-h<R$$ where $$R$$ is the freshness window length.

In PRS, things work a little differently. Each workshare points to a _specific block_ called its _anchor_. How can we use this information to design a robust reward distribution mechanism?

<details>

<summary>Challenge: Is this a security necessity?</summary>

For some reason, it seems "obvious" to me that "height-anchored PRS" should not be secure. However, my attempts to find an explicit selfish mining attack failed. "Height-anchored PRS" was not analyzed anywhere, because what's the point? Still, I remain in the dark about whether it's a security necessity or "just" a smart engineering choice.

I will reward 100 Quai to whoever produces the first argument that could convince me of either side. You can present your attempt in the X thread. (AI slop will be ignored on sight.)

</details>

As a warm-up, first assume that shares anchored outside the main chain do not count. So, for example, in this case (I'm still using fruits and baskets to represent workshares and blocks because I like fruit):

<figure><img src="../../.gitbook/assets/image (5).png" alt=""><figcaption></figcaption></figure>

workshare A will count, but workshare B will not. This is a _bad_ assumption, which we will soon remove, but it is instructive for kicking off the discussion.

While this is ultimately not the correct way to determine workshare validity, it does make a lot of sense. The key benefit is that only the main chain determines what workshares count, so the only way to change how the reward for a particular height is split retroactively is via a reorg. This increases stability and, while making the computation of reward distribution simpler and more localized. (Another benefit, well outside our current scope, is that computing rewards this way is compatible with the PoEM chain selection rule.)

So what is the problem with only looking at the main chain? Perhaps this picture will give you a hint:

<figure><img src="../../.gitbook/assets/image (6).png" alt=""><figcaption></figcaption></figure>

### 2 Selfish 2 Mining

It turns out that ignoring orphaned workshares makes selfish mining possible again!

With some reflection, this shouldn't be such a great surprise. FruitChain works because it _decouples_ block creation from reward distribution. But ignoring shares outside the selected chain couples them right back! Not only is selfish mining possible again, but the very same attacks on Bitcoin can be used here!

An adversary can follow any selfish-mining attack on Bitcoin (e.g., Eyal-Sirer), while also packing all workshares to their own blocks. If they manage to orphan an honest block, they get an **unfair advantage** because the blocks they introduced instead **only anchor their own workshares**. It is true that other miners can retroactively add more shares to the adversary block, but why would they? They'd rather harvest on more recent blocks that have fewer workshares already anchored to them. So even in this scenario, only harvesting to newer blocks, leaving the adversary with their advantage, is not only honest but _rational_.

### Hahaha, You Said "Knob"

So how can we use block anchoring in a more subtle way?

Simple, we _allow repacking shares anchored in uncle blocks_, as long as we are repacking on the _main chain._ In other words: we are still only counting workshares _packed_ on the main chain, but we allow these workshares to be anchored on uncle blocks.

Consider this scenario:

<figure><img src="../../.gitbook/assets/image (10).png" alt=""><figcaption></figcaption></figure>

The block $$C$$ packs the workshare $$B$$, but that doesn't matter, since $$C$$ is not on the main chain. _However_, $$D$$ _also_ packs $$B$$. Hence $$B$$ is counted despite being anchored on an uncle block.

Astute readers might scratch their heads and wonder: Doesn't this completely undermine the purpose of anchor blocks? How is this any better than just using height? And those astute readers are completely right! The key is that we are not allowing _all_ uncles, but only uncles _close enough to the main chain_.

_This_ is the _extra knob_ we alluded to earlier: the _allowed uncle distance_. Lets take the time to formalize this a bit.

In a blocktree, the "uncle distance" for each block is its distance from the selected _chain_. As an exercise, I urge you to examine the blocktree below and make sure you understand why the numbers below correctly reflect the uncle distance of each block, assuming the longest chain rule. (You can challenge yourself further by computing the uncle distance assuming the GHOST chain selection rule.)

<figure><img src="../../.gitbook/assets/image (11).png" alt=""><figcaption></figcaption></figure>

<details>

<summary>What should the uncle distances above be, assuming PoEM is used instead of the longest chain? (assume constant difficulty, i.e., that all blocks in the drawing have the same difficulty target)</summary>

**Trick question!** In PoEM, the _actual hashes_ of the headers are needed to determine the selected chain, even when the difficulty is constant. Without this extra information, it is impossible to determine the selected chain.

</details>

This definition allows us to finally define our second knob $$K$$ to be the _maximum allowed uncle distance_.&#x20;

### Relative Uncle Distance

It will be convenient to provide a _relative_ definition. That is, given blocks $$A$$ and $$B$$, determine "how far an uncle" $$A$$ is to $$B$$. The _uncle distance_ from $$A$$ to $$B$$ is defined to be the distance from $$A$$ to the selected chain of $$B$$. (Note that this is not a symmetric notion. The distance from $$A$$ to $$B$$ can be very different than the distance from $$B$$ to $$A$$, which is why we say "from $$A$$ to $$B$$" instead of "between $$A$$ and $$B$$". This can be fixed by choosing a bit more precise definition, but we don't require this precision.)&#x20;

As an example, consider the following blocktree:

<figure><img src="../../.gitbook/assets/image.png" alt=""><figcaption></figcaption></figure>

The uncle distance from the red block to the blue block is $$1$$. (The uncle distance from the blue block to the red block is $$3$$.)

To recover the previous (non-relative) definition of uncle distance, we note that the uncle distance of $$A$$ is simply the uncle distance from $$A$$ to the selected tip.

### Putting Everything Together

So the upshot is that we defined two knobs. The workshare eligibility depth $$W$$ (previously known as freshness window), and the allowed uncled distance $$K$$. The share eligibility policy implied by these two quantities is how PRS is defined. Let's make it explicit:

**Definition**: A workshare $$ws$$ is _eligible_ for block $$B$$ if the following conditions hold:

1. $$0<h'-h\le W$$, where $$h$$ is the height of $$ws$$'s anchor and $$h'$$ is the height of $$B$$.
2. The uncle distance from $$A$$ to $$B$$ is at most $$K$$.

So how should we set $$W$$ and $$K$$? We will get quantitative about it in the next section. Qualitatively, we want to set $$K$$ to be much smaller than $$W$$. $$K$$ should represent a depth beneath which forks are sufficiently unlikely. For example, we can take a cue from Bitcoin and set $$K=6$$. On the other hand, $$W$$ should be large enough to ensure shares are unlikely to be excluded (at least assuming enough honest miners).

Setting $$K$$ positive to allow "salvaging" workshares lost to shallow forks removes the selfish mining attack introduced by block-harvesting. Making it much smaller than $$W$$ (which needs to be much larger for other reasons anyway) retains the benefits of block-harvesting, at least approximately.

And _this_ is how packing is allowed in PRS.

Let us summarize this in a table (which you are encouraged to compare with the [FruitChains table](part-2-fruitchains.md#fruitchains-protocol-summary)):

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

We define honest behavior as follows:

* Mine fruits and baskets **simultaneously**
* The fruits and baskets are valid
* The fruit harvest point is always the heaviest basket
* The basket contains all known, still fresh, yet to be packed fruit
* Once a fruit or a basket is discovered, it is immediately broadcast to the entire network

</details>

## PRStimating

After working so hard to define PRS, we conclude by reviewing the results of the analysis in the PRS paper, and how they compare to FruitChain.

### Fairness and Convergence;

Since it was fairness we were after, it makes sense to first ask how fair PRS is. For that, let us consider the fairness averaged over $$T$$ consecutive levels. Say that an $$\alpha$$ miner earned a fraction $$\rho$$ of the rewards within the window, then we would like to bound $$|\rho-\alpha|$$ in terms of the window length $$T$$, the protocol parameters, and perhaps also the network latency.&#x20;

<details>

<summary>But isn't <span class="math">|\rho-\alpha|</span> ill defined?</summary>

Yes. This is a technicality that I chose to gloss over. The value $$\rho$$ is not deterministic, but a random variable that represents how the fraction of the $$\alpha$$ miner _distributes_. There is always _some_ probability that $$\rho=1$$, so we can't hope for $$|\rho-\alpha|$$ to _always_ converge to $$0$$.

The typical way to deal with it is to remove a _light tail_. That is, instead of trying to bound $$|\rho-\alpha|$$ with certainty, we are satisfied with a bound that'll work say $$99\%$$ of the time (or even better, $$1-O\left(e^{-T}\right)$$ of the time. If we can show that this bound vanishes quickly as $$T$$ increases, we are good.

</details>

The weakest form of fairness is the statement that $$|\rho-\alpha|$$ _eventually_ vanishes. That's not enough. We need guarantees on _how fast_ $$|\rho-\alpha|$$ decays.

As a yardstick to measure how fast $$|\rho-\alpha|$$ decays, we will first work out the _strongest_ possible fairness.

Mining is an _independent_ process: the probability of an $$\alpha$$-miner to mine the next block is not affected by any past events. It only depends on everyone's relative hash rates and mining strategies. This means that the best we can hope for is $$|\rho-\alpha| = \theta(1/\sqrt{T})$$. This is the part we can't remove. The natural noise of a Poisson process. The background hum of [block production](https://shai-deshe.gitbook.io/pow-book/supplementary-material/math/probability-theory/the-math-of-block-creation). The price of independence.

<details>

<summary>Seriously though, where does the square root come from?</summary>

Imagine a drunkard staggering on the integer line. Starting at zero, he takes a step in a random direction, and another one, ad infimum. After $$T$$ steps, how far should he be from zero?

A pillar of human intelligence called the central limit theorem tells us that the answer is $$\sqrt{T}$$.

We can (carefully) apply this logic to block, setting things up so that the drunkard's position measures how far the miner is from their expected number of blocks (which is $$\alpha T$$, not $$0$$), to obtain an expected distance of about $$\sqrt{T}$$. The fairness deviation works out to be roughly $$\sqrt{T}/\alpha T \approx 1/\sqrt{T}$$.

</details>

For FruitChains, we had the following approximation (for appropriately selected $$R,\lambda$$):

$$
|\rho-\alpha| \le O\left(\frac{\Delta}{R} + \frac{1}{\sqrt{\lambda T}} \right)
$$

The interesting part of this bound is the term $$1/\sqrt{\lambda T}$$. Comparing it to our yardstick, we see that it already vanishes as fast as we could hope. So what more is there to say? The problem is neatly tucked away into the asymptotic notation. It turns out that the constant preceding $$1/\sqrt{\lambda T}$$ is _quite large_. Not huge by any means, but formidable. The tragedy is that the only knob we have for scaling it down is $$\lambda$$, and $$\lambda$$ is under a square root.  To balance the bound, we must choose $$\lambda$$ on the magnitude of the (quite large) constant _squared_!&#x20;

And now the real kicker: recall the "impractical parameter regimes" we kept alluding to? They are impractical because on the one hand, we must have $$\lambda$$ of size "quite large squared". But on the other hand, the parameter regimes force $$R$$ to increase with $$\lambda$$. The final coffin is the trivial observation that $$T\ge R$$, because the convergence time can't be shorter than the freshness window.

PRS manages to squeeze a much better tradeoff:

$$
|\rho-\alpha| \le O\left(\frac{K}{W} + \frac{1}{\sqrt{(\lambda-1) T}} \right)
$$

Our yardstick reminds us again that asymptotically, $$1/\sqrt{\lambda T}$$ is the best we could hope for. But this time, the constants are _nice_. Nice enough that even for $$\lambda = 2$$ it only exerts a mild effect, and for say $$\lambda = 8$$ it becomes small enough to ignore within a few dozen blocks.

The time-independent component that remains  is $$K/W$$. One might wonder: how come the time latency doesn't affect the bound? Don't worry, it does. The latency is not directly visible, but it manifests in how we choose $$K$$ (in the sense that any fixed $$K$$ will fail for sufficiently large $$\Delta$$). $$K$$ wraps the stiff $$\Delta$$ with a tweakable quantity.

But there's obviously the other side of the tradeoff. In the PRS analysis, we find that the selfish mining threshold has the form $$\frac{1}{2} - \theta\left(\frac{K}{W}\right)$$. Since we agreed that $$K\ll W$$, we get that $$\theta\left(\frac{K}{W}\right)$$ can be scaled down. However, we still want to avoid making $$W$$ too large. The convergence time scales linearly with $$W$$, so setting it to moderately large values like $$W=1000$$ is already purpose-defeating.

So, how _should_ we set $$W$$? It is hard to provide analytical answers, so we turn to simulations. And indeed, the authors found via simulation that for a "moderately connected" adversary with a tie-winning probability of $$\gamma = 1/2$$, setting $$K=6$$ and $$W=100$$ furnishes $$\alpha$$-fairness for any $$\alpha<42\%$$, a huge improvement over the $$<25\%$$  Bitcoin can offer in the same regime.

### Trust Model

A unique feature of the PRS analysis, which does not hold for the FruitChain analysis or most protocol analyses, is the reduction of the honest assumption.

The security of FruitChain holds in a model where there is an honest majority. This is a reasonable assumption, but still a relatively strong one, which we would like to reduce. In a perfect system, the rational majority coincides with the honest majority.

Relying entirely on game-theoretic considerations is complicated, and most analyses, including FruitChains', show that if _enough_ of the network is honest, then it is _rational_ for the rest of the network to remain honest. The PRS analysis shows that rational behavior is an equilibrium, even when _no_ honest players are assumed. However, the analysis _must_ assume that a majority is rational, and a quick reflection reveals that, for any protocol, without this assumption, it is impossible to establish anything.

Some would call such a protocol "self-enforcing".

### Incentive Alignment and Future Goals

As mentioned above, PRS _does_ inherit one drawback from FruitChains: equilibria degeneracy. In other words, referring to all workshares is _a_ rational strategy, but not _the_ rational strategy. There are other rational strategies that are equally profitable for the miner but are hazardous for the network. More concretely, a miner is rational if and only if they point to each of their _own_ shares. But they have full freedom to choose how to regard shares by _other_ miners.

Removing this limitation is currently a key priority in PRS research. So how would one go about this?

The hope, at least as I see it, is for finding another "knob" that will allow us to incentivize inclusiveness at the expense of a _controlled_ trade-off of the benefits of the degenerate world. For example, we might find that an increase in share weight begets a _proportional_ increase in the required _honest_ fraction. Such a knob will allow us to make decisions such as "increase the share weight as much as possible without raising the honesty requirement beyond 10%". Of course, this is just one possible scenario out of many.

There is currently an interesting ongoing debate among the Quai developers and collaborators on these questions: What are the consequences of increasing share weight in terms of the honesty model and profitability thresholds? What is the correct way to choose share rates and weights? How do we juggle this array of properties — honesty requirements, incentive alignments, profitability threshold, expected profit, convergence time, and so on — which admit a great deal of subtlety within themselves and even more subtle interactions with each other? Is the share weight even the right parameter, or do we need a fancier knob?

Finding a way to balance out all these requirements into a trade-off that provides sufficient guarantees to _all_ aspects is the art of protocol crafting. By watching or participating in improving PRS, you can see it unfold in real time.
