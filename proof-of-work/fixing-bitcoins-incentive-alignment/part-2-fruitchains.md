---
description: How Pass and Shi fixed Bitcoin forever (but not really).
---

# Part 2: FruitChains

> **Acknowledgement**
>
> This post was funded by the [Quai network](https://qu.ai/), which generously provided me with a grant to fund my proof-of-work education efforts.

We are now positioned to understand the FruitChains protocol and how it attempts to combine the abstract idea of shares/subblocks/samples with decentralized consensus.

I have previously described FruitChains as "the granddaddy" of on-chain incentive alignment, and I kindly request the reader to keep that in mind throughout the discussion. Since our ultimate goal is to understand PRS, we are naturally inclined to talk about the disadvantages of FruitChains. But I do not want this to be construed as criticism of the quality of the work. The FruitChains paper is a remarkable result that laid the conceptual foundation for many future works, including PRS.

## Pack My Fruit, Will Ya?

The idea of FruitChains is to define two types of blocks.

**Fruit**: "light" types of blocks that are easier to produce (one might say that these fruit are lower-hanging). Each fruit contains the following data:

* A list of transactions
* A pointer to a basket block (which we'll define very soon) that I will call its **harvest time**

**Basket (these are just called "blocks" in the actual paper, but I find this confusing)**: a basket block is a block that _packs fruit_. Each basket contains the following data:

* A list of fruit that this basket packs
* A subset of the transactions in these fruits that does not contain any conflicts
* A pointer to a single _predecessor_ basket

So the picture we get is like this: the baskets form a tree, just like in Bitcoin, but they do not include _new_ transactions, only the transactions they chose from the fruits they packed. Each fruit has its harvest point, and is possibly packed into a basket. So we get something like this:

<figure><img src="../../.gitbook/assets/image (2) (1) (1).png" alt=""><figcaption></figcaption></figure>

Note that each fruit has exactly one harvest time and is packed into at most one basket. However, some of the fruit, even though a bit old, are not packed into any basket. This is a crucial part of the honest assumption: baskets are not **required** to pack any fruit, and are not even **incentivized** to do so. They are not **penalized** for packing fruit either, so it is not entirely outlandish to expect _honest_ miners to pack them, but it is far from ideal. We will dive into the dynamics of this process shortly.

<details>

<summary>Question: Why not <em>require</em> miners to pack all fruit?</summary>

Because that's not something you can enforce. As a rule of thumb, any policy that depends on _message arrival order_ cannot be a consensus rule.

Say that I see a basket $$B$$ and a fruit $$F$$ that can be validly packed into $$B$$, but isn't. Can I safely invalidate $$B$$ on these grounds?

What if $$B$$ was mined before $$F$$ reached the miner? How can we tell whether it was omitted by purpose or due to asynchrony? What about other network nodes that learned of $$B$$ before learning of $$F$$? Should they reorganize their chains?

Yes, such a policy will cause all nodes to agree on a chain in the _honest_ scenario. But how protected is it against malicious miners, even very small one, who want to tamper with the network? I'll leave this as a question for the reader.

</details>

The analogy to Bitcoin should roughly be something like this: baskets replace block _headers_, and fruits replace _transaction data_. When choosing the heaviest chain, we disregard fruit completely. _After_ selecting the chain, the baskets are processed along with the fruit, and rewards are distributed. So we can think of the fruits themselves as the block data. Or as Hugo Krawczyk described it: _orange is the new block_.

So how are rewards distributed? Simply. Each fruit is worth the same reward (at least assuming we weren't unfortunate enough to do our analysis exactly during a halving), which goes (along with the transaction fees) to whoever mined the fruit. The **entire point** is that fruits provide higher resolution samples for how the work is divided. Rewarding any other way will undermine this goal.

"But wait?" I hear you say, if miners don't get any advantage for packing fruits other than their own, why should they even bother? Isn't it just a wasted effort?&#x20;

Eh, yeah, we'll get to that...

So the affluence of fruits represents rewards, while the scarcity of blocks represents weight. Sounds kind of familiar, doesn't it? Of course, _the fruits are the plastic chips from the previous analogy_.&#x20;

Before we dive into the incentives, there is one more crucial aspect to introduce: freshness. It is not ostensibly clear why freshness matters, and in fact, it might seem like an arbitrary imposition, but it is actually very important. The freshness threshold is the valve that trades off fairness with responsiveness. The _freshness_ from the point of view of a given block is just how long it has been since the fruit was harvested. (The term is a bit misleading, as fresher fruits have _lower_ freshness. I would rather call it _ripeness_. But it is what it is.)

The freshness threshold $$R$$ tells us how fresh a fruit must be to be valid. After that point, it becomes _spoiled_, and surely any sensible person will agree that a fruit basket that packs spoiled fruit is invalid. Here is an illustration for a freshness threshold of three:

<figure><img src="../../.gitbook/assets/image (5) (1).png" alt=""><figcaption></figcaption></figure>

With that, we understand all of the ingredients and rules that define the FruitChain protocol. So let us try to understand what it achieves.

Note that the freshness parameter $$R$$ is not the same as the window length $$k$$. The former tells us how quickly fruit must be packed, the latter tells us how many fruit we need to observe before having sufficient confidence that the reward distribution is sufficiently fair. Typically, $$k\gg R$$.

This _almost_ paints a full picture of the protocol. There is another tiny bit to address: block orphaning. We said that each fruit references a _block_. But what if this block gets orphaned? Are all the fruit harvested in this block lost too? That would be very purpose-defeating: our entire point was to decouple block reorgs from reward dispensation! Here's the crux: the fruit doesn't point at a harvest _block,_ but at a harvest _time_, or rather, _height_ $$h$$. How can we trust miners not to lie? Well, setting $$h$$ to low just harms the miner's ability to earn any reward, I'll let the reader figure out how too high values of $$h$$ might be handled. In the rest of this post, we ignore the height and assume there are no reorged blocks. We are allowed to do that since using height instead makes the analysis follow through exactly the same.

<details>

<summary>FruitChains protocol summary</summary>

### Parameters

* Freshness bound $$R$$  (a.k.a recency bound) — how long since harvesting a fruit remains fresh
* Fruit rate $$\lambda$$ — expected number of fruit per single block delay

### Minable objects

**Fruits** and **baskets**:

|                      | Basket                                                                                                                               | Fruit                                                                                                                                                                                                          |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Difficulty**       | High                                                                                                                                 | Low ($$\lambda$$ times easier than a basket)                                                                                                                                                                   |
| **Fields**           | <ul><li>Parent</li><li>List of packed fruit</li><li>List of transactions</li></ul>                                                   | <ul><li>Harvest height</li></ul><ul><li>List of txns</li></ul><ul><li>Receiver address</li></ul>                                                                                                               |
| **Weight**           | Fixed                                                                                                                                | **None**                                                                                                                                                                                                       |
| **Rewards**          | **None**                                                                                                                             | Fixed, distributed to **fruit miner** when packed into a basket                                                                                                                                                |
| **Validation Rules** | <ul><li>Packed fruit are fresh</li><li>Transactions contained in packed fruits</li><li>Transactions consistent with parent</li></ul> | <ul><li>Valid harvest height</li><li>Transactions consistent with harvest point</li><li><p>Packed fruits are fresh (harvest height at most <span class="math">R</span> below mined block)</p><p></p></li></ul> |

### Honest miners

We define honest behaviour as follows:

* Mine fruits and baskets **simultaneously**
* The fruits and baskets are valid
* The fruit harvest point is always the heaviest basket
* The basket contains all known, still fresh, yet to be packed fruit
* Once a fruit or a basket is discovered, it is immediately broadcast to the entire network

</details>

Note that there are no particular limitations on how few/many transactions can be included in a fruit, or how few/many fruits can be packed into a basket. Also, I stress again that _mining Baskets does not earn rewards_. Miners mine fruits to earn fees and rewards, and the dual-mining process makes baskets naturally emerge from the process. _Rational_ miners are incentivized to post baskets that pack _their own fruits_, earning their reward. _Honest_ miners will additionally pack all other fruits they have heard of.

## Fairness

The main result of Pass-Shi is that if FruitChains is parameterized correctly, and more than half of miners are _honest_, then selfish mining is impossible. In this section we make this statement progressively more precise and see what we run into.

First, we define a convenient term called $$\delta$$-fairness. Consider a miner with $$\alpha$$ of the global hash power. Then for any $$\delta>0$$ we say that the miner has $$\delta$$-fairness if we know that if we look at a long enough window, we are almost surely guaranteed that the miner collected at most $$\alpha(1+\delta)$$ of the rewards (that is, outside their honest cut, they had a surplus of $$\delta\cdot\alpha$$). Moreover, the time we would have to wait only depends on $$\delta$$ and $$\alpha$$.

The most immediate observation is that $$\alpha$$-fairness cannot hold for $$0.5<\alpha<1$$ simply because an attacker with the majority of the hash power can ensure they create _all_ of the blocks.

Using $$\delta$$-fairness, we can make the security statement a bit more precise: if the protocol is parameterized correctly, then $$\delta$$-fairness is guaranteed for any $$\alpha<0.5$$ adversary, given that a majority of the network is honest.

This is starting to take shape, but as we illuminate more details, we will uncover the practical limitations of FruitChains.

### Almost Surely?

For those less familiar with how security is usually defined in probabilistic settings, the "almost surely" above might sound reckless. But the fact is that it is 1. not so bad (in properly secure protocols) and 2. unavoidable.

This relates to a profound and ubiquitous principle in computer science often described as "no free lunch", or as "probably almost correct" (PAC, yes, _the_ PAC in "PAC learning"). This is usually notated with  $$\varepsilon,\delta>0$$ where "almost correct" means "correct up to a factor of  $$(1+\delta)$$", and "probably" means "with a probability of at least $$1-\varepsilon$$".

Typically, we can assume $$\varepsilon$$ to be exponentially small, which means that we write it in the form $$2^{-\kappa}$$, where the number $$\kappa$$ is usually called "bits of confidence". Saying that you have "$$\kappa$$ bits of confidence" is the same as saying "the probability that I am wrong is less likely than the probability that you flip a fair coin $$\kappa$$ times and _all_ flips land on heads". For $$\kappa=64$$, this probability is about $$5.42\cdot 10^{-20}$$, and since saying (and writing) $$64$$ is much more pleasant than saying (or writing) $$5.42\cdot 10^{-20}$$, this notation caught on.

We will use it going forward.

### What does "parameterized correctly" mean?

The only two parameters that are hardwired into the protocol are the fruits-per-block-delay $$\lambda$$ and the freshness window $$R$$.

We now choose the accuracy $$\delta$$ and bits of confidence $$\kappa$$. That is, we want the protocol to guarantee that after a long enough period of time (that we will denote $$k$$, counted in block delays) the probability that an $$\alpha$$-miner gained more than $$\alpha(1+\delta)$$ of the emission is at most $$2^{-\kappa}$$.

The constraint "parametrized correctly" means that $$R$$ is "large enough" to make it sufficiently unlikely that $$R$$ consecutive blocks are adversarial. (This is a bit unfortunate, as it forces us to choose a maximal $$\alpha$$ in advance, but that much is true for almost any proof-of-work protocol.)

In math, we obtain the bound

$$
R\ge\frac{\kappa+\log\left(\lambda\right)}{\log\left(1/\alpha\right)}\text{.}
$$

In practice, this bound is _not enough_. But it is very close to the actual bound, and shows that $$R$$ increases with our required confidence, even in excellent network conditions.

This explains how FruitChains can work with $$\lambda=1$$  (which feels equivalent to just mining blocks like Bitcoin): You would have to compensate by waiting a very long time. $$R$$ might not seem to grow _that_ fast, but $$R$$ is _not_ how long we will have to wait. It just lower-bounds it (the time you want can't be shorter than the freshness window).

### So how long _will_ we have to wait?

We now set out to find $$k$$, the number of _fruits_ we will need to _observe_ to gain the desired confidence.

The intuition is that $$\lambda\cdot k$$ is the (expected) number of samples available to us for estimating the miner sizes up to an error of $$\delta$$. Due to the central limit theorem, we know that the number of samples we need increases _quadratically_ with the accuracy we want, and _logarithmically_ with the mistake probability we want (that is, _linearly_ with the bits of confidence we want). In other words, we expect that for some sufficiently large constant $$c$$ it suffices to have

$$
\begin{aligned}\lambda\cdot k\ge c\frac{\kappa}{\delta^{2}} & \implies & k\ge c\frac{\kappa}{\delta^{2}\lambda}\end{aligned}
$$

But to get a concrete number, we need to know $$c$$ (or at least some upper bound). If our samples were taken from a simple Poisson process, then any basic probability proof will tell you that taking $$c$$ to be its standard deviation will work. However, we are analyzing a much more complicated protocols, where many dependencies lurk, biting into the degree of significance we can extract out of any statistical inference. For example, we need to account for the fact that a miner who only points to her own fruits reduces the probability of other fruits to _ever_ be included, by an amount that depends on many factors including $$R$$ itself. This coupling between the size and meaning of the sample is hard to disentangle, but Pass and Shi's meticulous analysis show that it does not change the _growth_ of the required sample size. In other words, it is entirely rolled into the constant $$c$$.

A concrete value for $$c$$ is tricky, but for reasons we will not get into, it is natural to set $$c=3\ln 2 \approx 2$$.

<details>

<summary>Is it a limitation of the protocol or the analysis?</summary>

The first limitation, that we need a huge $$\lambda$$, mostly follows from the analysis itself. The theorem proved by Pass and Shi assumes steep relationships between the parameters that increase the required $$\lambda$$ for the analysis even to apply. There is no evidence that the protocol is either safe or unsafe for much smaller values of $$\lambda$$, but follow-up published analyses have not attempted that. Since this is a question of great interest, I carefully assume many tried and failed.

The second disadvantage, that the required number of shares per block $$\lambda$$ is at least $$3k$$, is a bit more established. There is no formal argument that $$\lambda=\Omega(k)$$, but there's compelling evidence:

1. We need this margin of error to ensure that most windows will have enough samples. This is a stronger requirement than just expecting that there are sufficiently many fruit on average.
2. It is possible to show attacks that work for any $$\lambda$$  if  $$\lambda< ck$$, assuming that  $$c<0.1$$ (I'm intentionally not telling you why, look it up or try for yourselves). If this was true for all $$c$$ (not just small value of $$c$$), this would have proved that indeed $$\lambda=\Omega(k)$$.

</details>

With this assumption in mind, we obtain the bound $$k\ge\frac{2\kappa}{\delta^2 \lambda}$$. But since $$k$$ is measured in fruit, and we have (on average) $$\lambda$$ fruit per block, then if we use $$\Lambda$$ to denote the delay between consecutive _baskets,_ we get that the waiting time is

$$
T=\frac{\Lambda k}{\lambda}\ge \Lambda\frac{2\kappa}{\delta^2 \lambda^2}
$$

So if we choose $$\lambda=1$$, and say we want 50 bits of confidence (which is actually a bit low) that there's no deviation of more than $$5\%$$ (which is actually a bit high). So we plug $$\kappa=50$$ and $$\delta=0.05$$ into the equation above to get that the waiting time will be **two hundred thousand** block delays. In Bitcoin, that comes up to about a four years. That is, you are more likely to wait longer for convergence than for the next halving!

We can try to "cheat" from the other direction, and make $$\lambda$$ very large, so that convergence will be fast.

We take more realistic assumptions of $$\kappa=64$$ and $$\delta=0.01$$. And say we want the protocol to converge after $$10$$ block delays. Then we set $$T=10\Lambda$$ in the equation and solve for $$\lambda$$ to get that we want about $$16000$$ fruit. Per block.

Granted, our analysis is rather loose, but the attmpts of Pass and Shi and others to tighten it didn't bear much, err, fruit. They did not provide a precise number, but suggested that the order should be in the low thousands.

That's an inordinate many fruits. If you try to create this many, you will find that the congestion becomes dominant, effectively increasing $$R$$, and taking $$k$$ along with it. In particular, when developing the inequality, we implicitly assumed that $$k$$ will turn out larger than $$R$$, otherwise the time it takes to gain sufficiently many samples increases, as the networks throughput becomes the dominant factor.

The Pass-Shi paper provides an analysis of this case as well, and gives the asymptotics of convergence time that also take into account the network's "fruit capacity", but we will not discuss this further, as one of our purposes is to avoid the need for so many shares in the first place.

### Why is honesty essential?

Say that you are a rational miner in an otherwise honest world. Would you necessarily pack _all_ possible fruit? It is clearly irrational to compromise the packing of _your_ fruit, so you will at least pack these. But what about the rest? You don't _lose_ anything from omitting all other fruit, but can you _gain_ from it?

The nitpicky reader might exclaim that packing additional fruit is a wasted effort, making your block traverse the network slower, thereby increasing orphaning probability. And they would be correct, but to a minimal extent that I am willing to ignore.&#x20;

Other than that, there doesn't seem to be anything to gain from not packing other fruit. You know that a majority of the network packs each other's fruit. It is true that if you exclude their fruit, you very temporarily increase your fraction of the gain by delaying everybody else's fruit whenever you publish a block. But you also know that the ripeness window is so long that their fruit will very likely be included by the honest majority very soon. Hence, your little rebellious unpacking act has practically zero effect within at most $$k$$ blocks. The same logic seems to apply to pretty much whatever we try to do to gain some advantage, and the Pass-Shi analysis translates "seems to" and "pretty much whatever" to "does" and "all".

But what happens if we remove the honesty assumption?

Now you don't know that other miners include your fruit. But why should you care? Why do they pose a threat? I mean, just a second ago, it was _you_ who refused to pack _their_ fruit, and we concluded that you pose no threat. So how come they pose a threat to _you_?

Consider the extreme situation: miners who only point to their own fruits. Where does this put us?

Well, if miners only pack their own fruit, then we might as well assume that the basket and the fruit can be treated as a single unit. A unit that contains both the fruit created since the previous basket and the basket itself. Providing both transaction data and weight. In other words, we get a block.

Yes, by assuming miners don't pack other miners' fruits, we reduced FruitChains back to Bitcoin. And now selfish mining attacks _are_ possible again, _even if_ all other miners are honest.

Now, even outside this scenario, the mere possibility shows that there is plausibly something to be gained by dropping _some_ fruit and applying _some_ _sort_ of withholding strategy. This undermines the assumption that a majority of miners include all fruit, as it is not dictated by rationality. And indeed, there are quite large domains (in terms of hashrate distribution) where the honest strategy is demonstrably losing.

## Effects on Mining Centralization

A final point I wanted to cover is what mining centralization looks like in FruitChains. While resolving the pool incentives in Bitcoin, FruitChains introduces a new form of pooling incentive that seems more controllable, but is still poorly understood.

This comes to demonstrate not only how pooled mining is encouraged by protocol dynamics, but also that drawbacks and pitfalls can always come from unexpected directions, which is why a protocol has to be carefully expected from all directions.

### Bitcoin Mining

A common criticism about Bitcoin is that it naturally incentivizes large mining pools due to how payment variance scales.

Say that you have 100% of the mining power. Then you create a block on average once per ten minutes. Those who understand the [math of block creation](https://shai-deshe.gitbook.io/pow-book/supplementary-material/math/probability-theory/the-math-of-block-creation) know this means that your blocks are sampled from a _Poisson distribution_ with parameter $$\tau = 10\text{ mins}$$. This means that after, say, an hour, they _should_ have mined about six blocks. It is still possible that they mined less or more than that, but as time passes, this variance _decreases_.&#x20;

<details>

<summary>Question*: Can you quantify this?</summary>

Consider you wait a period of $$k\cdot\Delta$$. The expected number of blocks in this time is $$k$$, and the variance turns out to be $$\sqrt{\Delta\cdot k}$$. This means that the probability that you created between $$k\cdot\Delta-\sqrt{k\cdot\Delta}$$ and $$k\cdot\Delta+\sqrt{k\cdot\Delta}$$ blocks **does not change with** $$k$$, let's call it $$p$$ (what we actually ded is to only allow a deviation of one standard deviation, which gives us $$p=0.68\%$$, you can get higher $$p$$ by using more standard deviations, but the analysis remains the same).

It follows that with probability $$p$$, the ratio between the number of blocks you expected and the number of blocks you created is between $$1-\frac{1}{\sqrt{k\cdot\Delta}}$$ and $$1+\frac{1}{\sqrt{k\cdot\Delta}}$$, which drops reasonably fast with $$k$$.

</details>

The problem is that the time it would take to reach a _constant_ deviation (e.g. how long do I have to wait before I know that, with probability $$90\%$$, I've created at least $$95\%$$ of the blocks I expected to create) increases _linearly_ with $$\tau$$.

We can say generally that, if $$\Delta$$ is the Bitcoin block delay, then the blocks created by an $$\alpha$$-miner follow a Poisson distribution with $$\tau= \Delta/\alpha$$, where the above is the special case $$\alpha=1$$.

Having written the process this way, we immediately see the problem: the time it takes to reduce variance below a required threshold is _inversely proportional_ to $$\alpha$$.&#x20;

_This_ is the reason pools are needed: to mitigate this catastrophic variance. If a collusion of many tiny miners cooperate to create $$30\%$$ of the blocks and split the rewards, then even though each one of them would have had a _huge_ variance, this process allows all of them to reduce the variance to (just slightly above, rapidly improved by reducing share difficulty) the same a single $$\alpha=0.3$$ miner would experience.

Fruit Chains ostensibly solves this issue: Now, what matters is the _fruit_ delay, not the basket delay, as this is what measures the reward distribution. We didn't have a notation for the fruit delay, but it is easy to express with what we do have. If there's a basket delay of $$\Delta$$, and an average of $$\lambda$$ fruits per basket, we get that the fruit delay is $$\Delta/\lambda$$, making the variance grow like $$\Delta/(\lambda\cdot \alpha)$$. And since we can increase $$\lambda$$ well beyond $$\Delta$$ this should provide a sound mitigation to the need for pools.

### The New Bottlenecks

But does it?

The key observation is that _included fruits_ are indeed samples that decrease variance, but _what if your fruit is never included_?

We can roughly model this by introducing a new quantity: $$p_f$$. This quantity represents the probability that the next basket packed your fruit, and for simplicity, we assume all miners know of your fruit. In other words, $$p_f$$ is (approximately) the combined hashrate fraction of all miners who intend to pack your fruit.

The probability that your fruit is _not_ packed in a _given_ basket is $$1-p_f$$, making the probability that it is never packed before it spoils $$(1-p_f)^R$$.

The assumption of an honest majority is equivalent to requiring $$p_f > 1/2$$, which means that the probability a fruit is never included becomes smaller than $$1/2^R$$, which is arguably sufficiently low even for modest values of $$R$$.

exceptThis is an effect that does not exist in Bitcoin: the way a miner chooses to construct her blocks affects the variance of other miners — incentivizing, perhaps, a mining pool that only packs the fruits created by its members. Or maybe allowing large miners to adopt "pay or wait" policies, where they censor all fruits except those mined by miners who pay them a fee.

While these effects, as I described them, are already discussed in Pass and Shi's original paper, our current understanding thereof is quite shallow, but I hope I drove across the point that it is one of the aspects one must consider when designing such a system.

<figure><img src="../../.gitbook/assets/image (6) (1).png" alt=""><figcaption></figcaption></figure>

