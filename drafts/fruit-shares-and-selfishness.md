---
description: What are selfish mining, subshares, and PRS?
---

# Fruit, Shares, and Selfishness



> **Acknowledgement**
>
> This post was funded by the [Quai network](https://qu.ai/), which generously provided me with a grant to fund proof-of-work education.

**Warning**: This post is [**a draft**](./). Please don't read it before reading [this](https://shai-deshe.gitbook.io/parallel-thoughts/drafts/drafts). For the parts that were already published as non-drafts, see [here](../proof-of-work/fixing-bitcoins-incentive-alignment/).



## Grab Me a Fruit, Will Ya?

The idea of FruitChains is to define two types of blocks.

**Fruit**: "light" types of blocks that are easier to produce (one might say that these fruit are lower-hanging). Each fruit contains the following data:

* A list of transactions
* A pointer to a basket block (which we'll define very soon) that I will call its **harvest time**

**Basket (these are just called "blocks" in the actual paper, but I find this confusing)**: a basket block is a block that _packs fruit_. Each basket contains the following data:

* A list of fruit that this basket packs
* A subset of the transactions in these fruits that does not contain any conflicts
* A pointer to another basket.

So the picture we get is like this: the baskets form a tree, just like in Bitcoin, but they do not include transactions. Each fruit has its harvest point, and is possibly packed into a basket. So we get something like this:

<figure><img src="../.gitbook/assets/image (2) (1).png" alt=""><figcaption></figcaption></figure>

Note that each fruit has exactly one harvest time and is packed into at most one basket. However, some of the fruit, even though a bit old, are not packed into any basket. This is a crucial part of the honest assumption: baskets are not **required** to pack any fruit, and are not even **incentivized** to do so. They are not **penalized** for packing fruit either, so it is not entirely outlandish to expect _honest_ miners to pack them, but it is far from ideal. We will dive into the dynamics of this process shortly.

The analogy to Bitcoin should roughly be something like this: baskets replace blocks, and fruits replace _transaction data_. When choosing the heaviest chain, we disregard fruit completely. _After_ selecting the chain, the baskets are processed along with the fruit, and rewards are distributed.

So how are rewards distributed? Simply. Each fruit is worth the same reward (at least assuming we weren't unfortunate enough to do our analysis exactly during a halving), which goes (along with the transaction fees) to whoever mined the fruit. The **entire point** is that fruits provide higher resolution samples for how the work is divided. Rewarding any other way will undermine this goal.

"But wait?" I hear you say, if miners don't get any advantage for packing fruits other than their own, why should they even bother? Isn't it just a wasted effort?&#x20;

Eh, yeah, we'll get to that...

So the affluence of fruit represents rewards, while the scarcity of blocks represents weight. Sounds kind of familiar, doesn't it? Of course, _the fruits are the plastic chips from the previous analogy_. But how well do they work?

Before we dive into the incentives, there is one more crucial aspect to introduce: freshness. It is not ostensibly clear why freshness matters, and in fact, it might seem like an arbitrary imposition, but it is actually very important. The freshness threshold is the valve that trades off fairness with responsiveness. The _freshness_ from the point of view of a given block is just how long it has been since the fruit was harvested. (The term is a bit misleading, as fresher fruits have _lower_ freshness. I would rather call it _ripeness_. But it is what it is.)

The freshness threshold tells us how fresh a fruit must be to be valid. After that point, it becomes _spoiled_, and surely any sensible person will agree that a fruit basket that packs spoiled fruit is invalid. Here is an illustration for a freshness threshold of three:

<figure><img src="../.gitbook/assets/image (5) (1).png" alt=""><figcaption></figcaption></figure>

With that, we understand all of the ingredients and rules that define the FruitChain protocol. So let us try to understand what it achieves.

<details>

<summary>FruitChains protocol summary</summary>

### Parameters

* Freshness bound $$k$$  (a.k.a recency bound) — how long since harvesting a fruit remains fresh
* Fruit rate $$\lambda$$ — expected number of fruit per single block delay

### Minable objects

**Fruits** and **baskets**:

|                      | Basket                                                                                                                               | Fruit                                                                                                                                                                                                              |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Difficulty**       | High                                                                                                                                 | Low ($$\lambda$$ times easier than a basket)                                                                                                                                                                       |
| **Fields**           | <ul><li>Parent</li><li>List of packed fruit</li><li>List of transactions</li></ul>                                                   | <ul><li>Harvest point</li></ul><ul><li>List of txns</li></ul><ul><li>Receiver address</li></ul>                                                                                                                    |
| **Weight**           | Fixed                                                                                                                                | **None**                                                                                                                                                                                                           |
| **Rewards**          | **None**                                                                                                                             | Fixed, distributed to fruit miner when packed into a basket                                                                                                                                                        |
| **Validation Rules** | <ul><li>Packed fruit are fresh</li><li>Transactions contained in packed fruits</li><li>Transactions consistent with parent</li></ul> | <ul><li>Valid harvest point</li><li>Transactions consistent with harvest point</li><li><p>Packed fruits are fresh (harvest time at most <span class="math">R</span> blocks below mined block)</p><p></p></li></ul> |

### Honest miners

We define honest behaviour as follows:

* Mine fruits and baskets **simultaneously**
* The fruits and baskets are valid
* The fruit harvest point is always the heaviest basket
* The basket contains all known, still fresh, yet to be packed fruit
* Once a fruit or a basket is discovered, it is immediately broadcast to the entire network

</details>



<details>

<summary>Ah yes, the two types of freshness</summary>

We actually made a simplifying assumption in our description of the honest strategy: that the freshness miners expect is the same as the freshness limit.

In practice, it is more reasonable to set some  $$R\ge k$$ as the maximal allowed freshness, but only expect honest miners to pack fruit that are at most $$k$$ fresh. The region $$R>k$$ is relevant when the fruit rate is comparable to (or faster than) the network delay. We ignore this aspect in our exposition.

</details>

### Fairness

The main result of Pass-Shi is that if FruitChains is parameterized correctly, and more than half of miners are _honest_, then selfish mining is impossible. In this section we make this statement progressively more precise and see what we run into.

First, we define a convenient term called $$\delta$$-fairness. Consider a miner with $$\alpha$$ of the global hash power. Then for any $$\delta>0$$ we say that the miner has $$\delta$$-fairness if we know that if we look at a long enough window, we are almost surely guaranteed that the miner collected at most $$\alpha(1+\delta)$$ of the rewards (that is, outside their honest cut, they had a surplus of $$\delta\cdot\alpha$$). Moreover, the time we would have to wait only depends on $$\delta$$ and $$\alpha$$.

The most immediate observation is that $$\alpha$$-fairness cannot hold for $$0.5<\alpha<1$$ simply because an attacker with the majority of the hash power can ensure they create _all_ of the blocks.

Using $$\delta$$-fairness, we can make the security statement a bit more precise: if the protocol is parameterized correctly, then $$\delta$$-fairness is guaranteed for any $$\alpha<0.5$$ adversary, given that a majority of the network is honest.

This is starting to take shape, but as we illuminate more details, we will uncover the practical limitations of FruitChains.

#### Almost Surely?

For those less familiar with how security is usually defined in probabilistic settings, the "almost surely" above might sound reckless. But the fact is that it is 1. not so bad (in properly secure protocols) and 2. unavoidable.

This relates to a profound and ubiquitous principle in computer science often described as "no free lunch", or as "probably almost correct" (PAC, yes, _the_ PAC in "PAC learning"). This is usually notated with  $$\varepsilon,\delta>0$$$$\e\delta$$ where "almost correct" means "correct up to a factor of  $$(1+\delta)$$", and "probably" means "with a probability of at least $$1-\varepsilon$$".

Typically, we can assume $$\varepsilon$$ to be exponentially small, which means that we write it in the form $$2^{-\kappa}$$, where the number $$\kappa$$ is usually called "bits of confidence". Saying that you have "$$\kappa$$ bits of confidence" is the same as saying "the probability that I am wrong is not higher than the probability that you flip a fair coin $$\kappa$$ times and it always lands on tails". We will use this notation going forward.

#### What does "parameterized correctly" mean?

The only two parameters that are hardwired into the protocol are the fruits-per-block-delay $$\lambda$$ and the freshness window $$R$$.

We now choose the accuracy $$\delta$$ and bits of confidence $$\kappa$$. That is, we want the protocol to guarantee that after a long enough period of time (that we will denote $$k$$, counted in block delays) the probability that an $$\alpha$$-miner gained more than $$\alpha(1+\delta)$$ of the emission is at most $$2^{-\kappa}$$.

The constraint "parametrized correctly" means that $$R$$ is "large enough" to make it sufficiently unlikely that $$R$$ consecutive blocks are adversarial. (This is a bit unfortunate, as it forces us to choose a maximal $$\alpha$$ in advance, but that much is true for almost any proof-of-work protocol.)

In math, we obtain the bound

$$
R\ge\frac{\kappa+\log\left(\lambda\right)}{\log\left(1/\alpha\right)}\text{.}
$$

In practice, this bound is _not enough_. But it is very close to the actual bound, and shows that $$R$$ increases with our required confidence, even in excellent network conditions.

This explains how FruitChains can work with $$\lambda=1$$  (which feels equivalent to just mining blocks like Bitcoin). You would have to compensate by waiting a very long time. $$R$$ might not seem to grow _that_ fast, but $$R$$ is _not_ how long we will have to wait. It just lower-bounds it (the time you want can't be shorter than the freshness window).

#### So how long _will_ we have to wait?

We now set out to find $$k$$, the number of _fruits_ we will need to observe before we gain the desired confidence.

The intuition is that $$\lambda\cdot k$$ is the (expected) number of samples available to us for estimating the miner sizes up to an error of $$\delta$$. Due to the central limit theorem, we know that the number of samples we need increases _quadratically_ with the accuracy we want, and _logarithmically_ with the mistake probability we want (that is, _linearly_ with the bits of confidence we want). In other words, we expect that for some sufficiently large constant $$c$$ it suffices to have

$$
\begin{aligned}\lambda\cdot k\ge c\frac{\kappa}{\delta^{2}} & \implies & k\ge c\frac{\kappa}{\delta^{2}\lambda}\end{aligned}
$$

But to get a concrete number, we need to know $$c$$ (or at least some upper bound). If our samples were taken from a simple Poisson process, then any basic probability proof will tell you that taking $$c$$ to be its standard deviation will work. However, we are analyzing a much more complicated protocols, where many dependencies lurk, biting into the significance of any statistical inference. For example, we need to account for the fact that a miner who only points to her own fruits reduces the probability of other fruits to _ever_ be included, by an amount that depends on many factors including $$k$$ itself. This coupling between the size and meaning of the sample is hard to disentangle, but Pass and Shi's meticulous analysis show that it does not change the _growth_ of the required sample size. In other words, it is entirely rolled into the constant $$c$$.

A concrete value for $$c$$ is tricky, as it depends on unrolling the analysis, as well as network conditions. I asked ChatGPT5 to upper bound it for me, and she concluded that choosing $$c=100$$ is "very conservative", so for the rest of this section let us assume that $$c=10$$ is enough. (That being said, trusting an AI without verifying its answer yourself is _always_ a bad idea, so if you intend to implement FruitChains, start with finding a more reliable way to parameterize it.)

<details>

<summary>Is it a limitation of the protocol or the analysis?</summary>

The first limitation, that we need a huge $$\lambda$$, mostly follows from the analysis itself. The theorem proved by Pass and Shi assumes steep relationships between the parameters that increase the required $$\lambda$$ for the analysis even to apply. There is no evidence that the protocol is either safe or unsafe for much smaller values of $$\lambda$$, but follow-up published analyses have not attempted that. Since this is a question of great interest, I carefully assume many people tried and failed.

The second disadvantage, that the required number of shares per block $$\lambda$$ is at least $$3k$$, is a bit more established. There is no formal argument that $$\lambda=\Omega(k)$$, but there's compelling evidence:

1. We need this margin of error to ensure that most windows will have enough samples. This is a stronger requirement than just expecting that there are sufficiently many fruit on average.
2. It is possible to show attacks that work for any $$\lambda$$  if  $$\lambda< ck$$, assuming that  $$c<0.1$$. If this was true for all $$c$$ (not just small value of $$c$$), this would have proved that indeed $$\lambda=\Omega(k)$$.

</details>

With this assumption in mind, we obtain the bound $$k\ge\frac{10\kappa}{\delta^2 \lambda}$$. But since $$k$$ is measured in fruit, and we have (on average) $$\lambda$$ fruit per block, then if we use $$\Lambda$$ to denote the delay between consecutive _baskets,_ we get that the waiting time is

$$
T=\frac{\Lambda k}{\lambda}\ge \Lambda\frac{10\kappa}{\delta^2 \lambda^2}
$$

So if we choose $$\lambda=1$$, and say we want 50 bits of confidence (which is actually a bit low) that there's no deviation of more than $$5\%$$ (which is actually a bit high). So we plug $$\kappa=50$$ and $$\delta=0.05$$ into the equation above to get that the waiting time will be **two hundred thousand** block delays. In Bitcoin, that comes up to about a four years. That is, you are more likely to wait longer for convergence than for the next halving!

We can try to "cheat" from the other direction, and make $$\lambda$$ very large, so that convergence will be fast.

We take more realistic assumptions of $$\kappa=64$$ and $$\delta=0.01$$. And say we want the protocol to converge after $$10$$ block delays. Then we set $$T=10\Lambda$$ in the equation and solve for $$\lambda$$ to get that we want about $$80000$$ fruit. Per block.

That's an inordinately many fruits. If you try to create this many, you will find that the congestion becomes dominant, effectively increasing $$R$$, and taking $$k$$ along with it. In particular, when developing the inequality, we implicitly assumed that $$k$$ will turn out larger than $$R$$, otherwise the time it takes to gain sufficiently many samples increases, as the networks throughput becomes the dominant factor.

The Pass-Shi paper provides an analysis of this case as well, and gives the asymptotics of convergence time that also take into account the network's "fruit capacity", but we will not discuss this further, as one of our purposes is to avoid the need for so many shares in the first place.

#### Why is honesty essential?

Say that you are a rational miner in an otherwise honest world. Would you necessarily pack _all_ possible fruit? It is clearly irrational to compromise the packing of _your_ fruit, so you will at least pack these. But what about the rest? You don't _lose_ anything from omitting all other fruit, but can you _gain_ from it?

The nitpicky reader might exclaim that packing additional fruit is a wasted effort, making your block traverse the network slower, thereby increasing orphaning probability. And they would be correct, but to a minimal extent that I am willing to ignore.&#x20;

Other than that, there doesn't seem to be anything to gain from not packing other fruit. You know that a majority of the network packs each other's fruit. It is true that if you exclude their fruit, you very temporarily increase your fraction of the gain by delaying everybody else's fruit whenever you publish a block. But you also know that the ripeness window is so long that their fruit will very likely be included by the honest majority very soon. Hence, your little rebellious unpacking act has practically zero effect within at most $$k$$ blocks. The same logic seems to apply to pretty much whatever we try to do to gain some advantage, and the Pass-Shi analysis translates "seems to" and "pretty much whatever" to "does" and "all".

But what happens if we remove the honesty assumption?

Now you don't know that other miners include your fruit. But why should you care? Why do they pose a threat? I mean, just a second ago, it was _you_ who refused to pack _their_ fruit, and we concluded that you pose no threat. So how come they pose a threat to _you_?

Consider the extreme situation: miners who only point to their own fruits. Where does this put us?

Well, if miners only point to their own fruit, then we might as well assume that the basket and the fruit can be treated as a single unit. A unit that contains both the fruit created since the previous basket and the basket itself. Providing both transaction data and weight. In other words, we get a block.

Yes, by assuming miners don't pack other miners' fruits, we reduced FruitChains back to Bitcoin. And now selfish mining attacks _are_ possible again.

Now, even outside this scenario, the mere possibility shows that there is plausibly something to be gained by dropping _some_ fruit and applying _some_ _sort_ of withholding strategy. This undermines the assumption that a majority of miners include all fruit, as it is not dictated by rationality. And indeed, there are quite large domains (in terms of hashrate distribution) where the honest strategy is demonstrably losing.

### Centralization Concerns

## Split Rewards, not Hairs

