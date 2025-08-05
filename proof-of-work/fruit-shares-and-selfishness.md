---
description: What are selfish mining, subshares, and PRS?
---

# Fruit, Shares, and Selfishness

> **Acknowledgement**
>
> This post was funded by the [Quai network](https://qu.ai/), which generously provided me with a grant to fund proof-of-work education.

\[This post is **not complete**. If you conicidentally found your way here looking for information, **you are early**. I hope to finish it by the second weekend of August]

In this post, we present two solutions for selfish mining, the Fruitchain bla bla bla

Throughout the post, more challenging aspects are posed as answers with solutions. These questions are meant to get your brain gears rotating, but also to clearly mark the more technical comments that might require a bit of formal background. **Skipping these questions entirely will not detract the reading experience, and is recommended on a first read**.

<figure><img src="../.gitbook/assets/image (1).png" alt="" width="330"><figcaption><p>A shellfish miner</p></figcaption></figure>

## Selfish Mining Primer

In a previous post, I explained [selfish mining in Bitcoin](https://shai-deshe.gitbook.io/pow-book/part-1-blockchains-and-blockdags/chapter-2-the-block-chain-paradigm/selfish-mining-in-bitcoin).

If you're not familiar with selfish mining, I suggest reading that post first. The executive summary is that the incentives in Bitcoin aren't exactly aligned with how we would like miners to behave.

The Bitcoin protocol assumes that _honest_ miners follow two simple rules:

1. Always mine over the top of the heaviest chain
2. Whenever you discover a new block (either by solving it yourself or hearing about it from one of your peers), broadcast it to all your peers _immediately_

In reality, we [do not expect miners to be honest, but _rational_](https://shai-deshe.gitbook.io/pow-book/part-1-blockchains-and-blockdags/chapter-2-the-block-chain-paradigm/honesty-and-rationality). We assume a majority of the miners in the network are seeking to maximize their Bitcoin profits from fees and mining. Under this assumption, we can influence miners' behavior by _incentivizing_ them.

The incentive in Bitcoin is straightforward: if your block is on the heaviest chain, you win fees and a block reward. It is not hard to believe that mining over any block but the top of the heaviest chain increases the chances that your block will be orphaned, thus decreasing your expected gain and encouraging miners to follow the first rule. The second rule doesn't align quite as nicely. It is rational for small miners to follow it, but as it turns out, sufficiently large miners can gain from _withholding_ (and potentially orphaning) blocks.

### How Eyal and Sirer Ruined Bitcoin Forever (but not really)

[In their paper](https://arxiv.org/abs/1311.0243), Eyal and Sirer present a strategy that increases the profit of a large miner by withholding blocks.

The idea is that by withholding the blocks they created, only releasing them at strategic times, a large miner can increase the orphan rates of the rest of the network more than its own orphan rates, causing their proportion of non-orphaned work to increase, whereby earning then a bigger cut of the reward than their contribution to mining.

For those who want the details of the Eyal-Sirer attack, as well as an overview of the subsequent attacks and countermeasures, I recommend the [relevant section](https://shai-deshe.gitbook.io/pow-book/part-1-blockchains-and-blockdags/chapter-2-the-block-chain-paradigm/selfish-mining-in-bitcoin) of my book.

The upshot of the attack, in concrete number form, is summarized in this figure lifted from their paper:

<figure><img src="../.gitbook/assets/image (3).png" alt=""><figcaption><p>(Fig 2. from Eyal-Sirer)</p></figcaption></figure>

$$\gamma$$ measures _connectivity:_ the probability that an attacker block _wins_ (that is, not orphaned) if it releases at the exact same time the adversary hears of a competing honest block.

We see that even if we assume zero connectivity, an attacker with more than 33% can profitably carry out the attack, while as little as 44% suffices to create a _majority_ of the blocks non-orphaned.&#x20;

With perfect connectivity, 33% is already enough to create a majority of the non-orphaned blocks, and _any_ perfectly connected attacker has something to gain from a selfish mining attack.

The most realistic scenario is that the attacker's connectivity parameter is somewhere in between, say halfway. In this case we see that 25% are enough for a profitable attack, while 38% are enough to create a majority of non-orphaned blocks.

A common misconception is that because a 38% attacker can create a majority of the blocks, she can double-spend. It makes sense that by making more blocks than the honest network, you can create a competing chain, but that's _not what you do_ in selfish mining. The _total_ fraction of blocks remains the same, but you constantly headbutt with honest blocks to kick them off the chain. You can only do this by pointing at, or near, the heaviest tip, which is impossible if you spend your efforts on mining a side chain.&#x20;

A successful double-spend attack looks like this:

<figure><img src="../.gitbook/assets/image (1) (1).png" alt=""><figcaption></figcaption></figure>

whereas a successful selfish mining attack looks like this:

<figure><img src="../.gitbook/assets/image (2) (1).png" alt=""><figcaption></figcaption></figure>

Note that in the latter example, the red blocks constitute the majority of _chain_ blocks, but the blue blocks are still the majority of _all_ blocks.

### Chain Quality (and Lack Thereof)

A key nuance in the discussion above is that _we don't like selfish mining_, but it _doesn't allow a double-spend attack_. In other words, it is a behavior that is considered adversarial, but is not captured in the colloquial definition of [what makes a blockchain secure](https://shai-deshe.gitbook.io/pow-book/part-1-blockchains-and-blockdags/chapter-2-the-block-chain-paradigm/security-notions).

It is natural to [define a security notion](https://shai-deshe.gitbook.io/pow-book/part-1-blockchains-and-blockdags/chapter-2-the-block-chain-paradigm/security-notions) that captures selfish mining attacks. That is exactly what Garay, Kiayias, and Leonardos did when they described the [Bitcoin backbone protocol](https://eprint.iacr.org/2014/765), a version of Bitcoin that is simplified enough for mathematical analysis, but more accurate than previously used models.

In that paper, they introduce the _chain quality_ property. The precise definition is a bit technical, but the gist is this:

**Definition** (reproduced from Definition 4 in [GKL](https://eprint.iacr.org/2014/765), simplified, informal): A blockchain has the chain quality property if the amount of non-orphaned blocks produced by a miner with a fraction $$\alpha$$ of the global hashrate gets closer to a fraction of $$\alpha$$ of the blocks as time passes.

The key hidden detail here is how long we need to wait before the fraction becomes sufficiently close to $$\alpha$$. GKL did not answer this question for a straightforward reason: Bitcoin does _not_ satisfy the chain-quality property.

### Selfish Generals?

In my experience, what I am about to explain in the following section tends to contradict how many people view Bitcoin's security properties.

The following statements are facts:

1. Deterministic finality [cannot handle a situation where more than a third of the nodes are faulty](https://shai-deshe.gitbook.io/pow-book/part-1-blockchains-and-blockdags/chapter-1-bft-vs.-pow/byzantine-fault-tolerance).&#x20;
2. In particular, BFT protocols cannot guarantee that they reach an agreement if close to half of the nodes allow themselves to deviate from the protocol
3. In Bitcoin, we only need (slightly more than) half of the miners to be honest to assure consensus is reached in a timely manner and becomes irreversible fast

It is natural to assume that in this case, we can also use Bitcoin for binary voting: just let each miner post a "yes" or "no" on their blocks and then do a majority count.

Selfish mining proves that this is not the case: a sufficiently connected 34% attacker can create a majority of the blocks and win the vote.

Apparently, while it is true that Bitcoin can handle a higher fault threshold, the property that a collusion of more than a third of the voters could always create a majority of the blocks _persists_. In particular, for _any protocol,_ including probabilistic ones, a _perfectly connected adversary_ with more than a third of the global hashrate could _always_ produce a majority of the blocks.

So why are we even doing this?

Because the assumption of a perfectly connected adversary is unrealistic. A perfectly connected adversary has the following property: if they withhold a block $$B$$, only releasing it upon hearing about a a competing block $$C$$ releases block $$B$$, they are _guaranteed_ that the network will prefer $$B$$ over $$C$$.

It's hard to imagine such an adversary in reality. Even for a very well-connected adversary, there must be some other miner sufficiently distant that, by the time the attacker learns of their blocks, most honest miners also have, giving the attacker's block a _zero_ chance to win.

Furthermore, the ability to selfishly mine becomes quite limited quite fast as the connectivity parameter $$\gamma$$ becomes smaller. This is already apparent in the Eyal-Sirer graph above. However, we see that for low (even zero) values of $$\gamma$$, a sufficiently larger less-than-half adversary can still accrue disproportionate gains.

Fixing _this_ is the problem that inspired the protocols we are about to discuss.

## Unselfishing Bitcoin?

The aftermath of the discovery of selfish mining has led to various approaches for mitigating its effects. As usual, the Bitcoin community was averse to modifying the underlying protocol. Some suggested changes to peer-to-peer policies (such as block relaying and tie-breaking rules) that, while not prohibiting the attack, would make it harder to carry out. Others argued that selfish mining is not a significant concern, given the extreme measures required to carry it out profitably.

On the theoretical front — where the motivation is not the preservation of Bitcoin, but understanding what probabilistic consensus can or cannot do — people work on developing protocols where this problem does not exist.

### Statistical Convergence

We laid out our goal: to make reward shares more fair.

However, we must recall that altering the reward distribution method can also affect properties we often take for granted. One crucial aspect is how long it takes the reward share to converge into a fair distribution. Say that you have $$\alpha$$ of the hashrate, and a particular protocol guarantees that on average, over time, you will gain $$\alpha$$ of the rewards. How long will it take? Is it possible that the variance is so substantial that it will take days, even weeks, before the probability of deviating significantly from the amount of reward you were expecting becomes negligibly small?

This is not just about patience. Tracking reward distribution is crucial for the everyday operations of pools and exchanges. In a while, we will introduce _shares_, a way for a miner to prove to a pool that they have done part of the work. A pool typically pays out for the share in advance, based on an _estimation_ of the actual reward. An incorrect estimation can lead to a pool bleeding money. A protocol that forces pools to either take monetary risks or withhold payouts for days or weeks is impractical.

### The State of the Art

A holy grail solution to selfish mining is a protocol where, assuming a majority of the miners are _rational_, no miner with a fraction $$\alpha$$ of the network can obtain, in the long term, more than a fraction of $$\alpha$$ of the rewards. Such a protocol necessarily works by delaying the distribution of rewards to collect enough data to make the distribution fair.&#x20;

We are not quite there yet.

The first successful attempt at better aligning mining incentives is the [_FruitChains_](https://eprint.iacr.org/2016/916) protocol, introduced in 2016 by Pass and Shi. FruitChains manages to find a little weak, but still rather satisfying, compromise between rationality and honesty. The chain quality property holds, in the sense that an _honest_ miner will earn as much as they should _as long as other miners are honest_.

Wait what? Isn't this precisely what we _don't_ want to assume?

Well, here is the thing: in Bitcoin, a large miner can deviate and _immediately benefit_, even if all other miners are honest. In FruitChain, this is no longer the case. Deviation does not penalize you, but as long as no other miner deviates in the same way, it does not gain you anything either.

However, FruitChains has two drawbacks that make it nearly unusable. The first is that for its security to even guarantee any resilience at all, we need to make **a lot** of shares. Much more than it is reasonable for current networks to support. The second is that the number of **blocks** that we have to wait for before the reward share _starts_ to converge to the mining share is about a third of the number of fruit. To put this in proportion, for the security analysis to kick in, we need about 12.5 **thousand** shares per block, which means we will have to wait for more than 4 thousand blocks before we can say anything about how fair the share is. In Bitcoin, this would take about a month.

<details>

<summary>Is it a limitation of the protocol or the analysis?</summary>

The first limitation, that we need a huge $$\lambda$$, mostly follows from the analysis itself. The theorem proved by Pass and Shi assumes steep relationships between the parameters that increase the required $$\lambda$$ for the analysis even to apply. There is no evidence that the protocol is either safe or unsafe for much smaller values of $$\lambda$$, but follow-up published analyses have not attempted that. Since this is a question of great interest, I carefully assume many people tried and failed.

The second disadvantage, that the convergence time $$k$$ is $$\lambda/3$$, is a bit more established. There is no formal argument that $$k=\Omega(\lambda)$$, but there's compelling evidence:

1. We need this margin of error to ensure that most windows will have enough samples. This is a stronger requirement than just expecting that there are sufficiently many fruit on average.
2. It is possible to show attacks that work for any $$\lambda$$  if  $$\lambda< ck$$, assuming that  $$c<0.1$$. If this was true for all $$c$$ (not just small value of $$c$$), this would have proved that indeed $$k=\Omega(\lambda)$$.

</details>

This remained the state-of-the-art for a while. Literature on selfish-mining-resistant protocols continued to be published, primarily focusing on no-go theorems that demonstrate the vulnerability of various natural approaches to modifying FruitChains. We will mention some of these results as we learn how FruitChains works.

As far as I know, the only new approach to emerge following FruitChains is the very recent [Proportional Reward Splitting](https://arxiv.org/abs/2503.10185) (PRS), authored by a collaboration of the Quai team and Dionysis Zindros (with whom I am already familiar as the coauthor of [NiPoPoWs](https://eprint.iacr.org/2017/963) and [Mining in Log-Space](https://eprint.iacr.org/2021/623)).

The PRS protocol is heavily inspired by FruitChains, but takes just enough liberties to stand on its own feet. It introduces two major improvements.

First, it manages to remove the honesty assumption, replacing it with rationality. Note that this is still not the holy grail. Even in PRS, a rational majority alone is not sufficient to ensure chain quality. Even if all miners are rational, this is not guaranteed. What _is_ guaranteed is that if all miners are rational and none deviates, then a single miner with less than half of the hash rate _gains nothing_ by deviating. The only way to earn from deviating is if there is a majority of deviators. But again, the deviation is not penalized either.

Second, and crucially, the security of argument for PRS **does not couple** the number of shares required to attain given confidence to the number of shares per block. In particular, it can be parametrized with as few or as many shares as you want. More shares still provide better convergence, but only because it would take less time to collect **the same number** of shares.

I stress again that this is not the confirmation time, but rather the time it takes to gain confidence that

So PRS provides improvements in two important directions: it reduces some of the honesty assumptions to rationality assumptions, and shortens the convergence times by several orders of magnitude. But in our world, there are no solutions, only trade-offs, and what PRS gains in speed and game-theoretic leniency, it pays back in precision. While FruitChain can, in theory, provide selfish mining resilience against **any** $$\gamma=0$$ attacker with less than half of the hashrate, PRS can only provide such security (though with softer assumptions) for miners with at most  $$\sim 40\%$$ of the total hashrate.

For comparison, in Bitcoin, for $$\gamma=0$$ the Eyal-Sirer strategy has a threshold of  $$33\%$$. However, this attack is **not** optimal. A paper by [Sapirshtein and Zohar et al.](https://arxiv.org/abs/1507.06183) isolates the optimal strategies and proves that, for  $$\gamma=0$$, a selfish miner with anywhere above $$25\%$$ of the global can mine profitably.

We can summarize this into the following table:

|                                         | Bitcoin                                                                                                      | FruitChain                                                       | PRS                         |
| --------------------------------------- | ------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------- | --------------------------- |
| Selfish mining threshold ($$\gamma=0$$) | <p><span class="math">25\%</span><br>(<a href="https://arxiv.org/abs/1507.06183">Sapirshtein et al.</a>)</p> | $$50\%$$                                                         | $$38\%-42\%$$               |
| Rationality/Honesty assumptions         |                                                                                                              | Honest majority                                                  | **Rational** majority       |
| Required shares/block                   |                                                                                                              | <p><span class="math">~1.4\cdot 10^5</span><br>(impractical)</p> | **No requirement**          |
| Number of samples needed                |                                                                                                              | Grows with fruits/block                                          | Independent of fruits/block |

These advances arguably place PRS as the best way yet to make a chain resistant to selfish mining, but the Quai team is not satisfied. They are now looking into removing the remaining honesty assumptions and only rely on rationality. We will survey why and how at the end of the post.

### Marco? Polo!

Before describing FruitChains and PRS, it's worth considering a similar problem: designing a mining pool.

When you think about it, mining pools have to solve a similar problem: how to divide the block reward to the pool users, such that each user is rewarded proportionally to their contribution.

The setting of mining pools is very different from selfish mining. Since the pool's decision does not affect consensus, the decision doesn't have to be inferable from the chain. Mining pools and users transmit _off-chain_ data in the decision-making process, and only post the final decision to the chain. This is a trade-off: on the one hand, we need this additional information to make a fair decision. On the other hand, this makes the decision process vulnerable to censorship, data manipulation, and other problems that blockchains solve. Reconciling the latter drawback requires sophisticated protocols such as  PPS+, PPLNS, FPPS, and others.

FruitChain and PRS essentially try to take the core idea and try to reverse it: let's post enough of this additional information on-chain, but find a way to do so that is hard to manipulate. The first step to understanding these protocols is to understand what "additional information" mining pools collect and how it is helpful. (While conveniently ignoring the problem of aggregating the information trustlessly).

So, how do mining pools work?

I like to think of miners in a pool as a search excavation looking for a treasure lost in a vast cornfield. And when I say vast, I mean **vast**, with billions upon trillions of corn stalks.

To keep things fair, they decide that the treasure will be divided such that each member is rewarded in proportion to how much ground they covered.

The million Quai question is of course: how can they determine how much ground each member covered?

Say that a party member called Seamus found the treasure. Based on this fact alone, it is _impossible_ to distribute the treasure fairly. To see why that is, consider three scenarios: First, all search members worked equally hard, and Seamus lucked upon the treasure. Second, Seamus did all the work, while the rest of the party were... partying, I guess? Third, Seamus was lazing on the beach while everyone else was hard at work, but when he got peckish and went to get a cob of corn, he just happened to stumble into a treasure chest. While all three scenarios should furnish wildly different distributions, in all cases we have the same information: Seamus found the treasure.

So, we need additional information, but _what_ information? What could the treasure hunter provide that would _prove_ how much work they did?

One idea is to ask all excavators to collect cobs of corn as they go, but trying this, we unsurprisingly find that a vast corn field has **too much corn**. Excavators will rapidly find themselves hauling huge crates of corn, and counting them at the end becomes prohibitively tedious. The analogy, if it wasn't clear, is to ask each miner to provide the entire list of nonces they hashed and the resulting values, proving they indeed computed as many hashes. To fathom how unreasonable this is, recall that a single Antminer produces about **200 trillion hashes per second**.

**Question:** You could also argue that collecting all nonces and hashes is actually **much worse**, as validating a nonce requires computing the hash, so arguably, validating all the nonces doesn't just need tons of space, but also the same amount of work that went into actually mining the block. Is this a good argument?

<details>

<summary>Hint</summary>

Try to find a _probabilistic_ method to provide a very good _approximation_ of the work distribution by only looking at a fraction of the hashes.

</details>

<details>

<summary>Answer</summary>

No, it is not a good argument.

We could validate a heap of nonces by picking a few random nonces and only checking them. How accurate is this approach?

Say that we only check $$k$$ nonces. Also say that someone tries to cheat, they sent us a lot of nonces, but a fraction of  $$\alpha>1$$  of them are real. What are the chances that they escape our detection?

Assuming that $$k$$ is much smaller than the number of hashes. For each hash we check, the probability it is not fake is $$\alpha$$, making the probability all of them are not fake  $$\alpha^k$$.

The key observation here is that the success probability of the fraud only depends on $$\alpha$$ and $$k$$, not on the actual number of nonces.

We can set $$k$$ rather high. The computational cost of our test increases linearly with $$k$$ and (since computing a single hash is very efficient) with a very small constant. So even setting $$k$$ to one-million will not cause anyone to break a sweat.

But let's be modest and analyze $$k=1000$$. What is the probability that we miss an adversary who faked $$0.1\%$$ of their shares? This corresponds to $$\alpha = 0.999$$, so the probability is $$0.999^{1000} \approx 37\%$$.

Too much? By taking $$k=10000$$ this goes down to less than $$0.005\%$$, and adding another zero to $$k$$ makes the result so small that even my scientific calculator just evaluates it to zero.

</details>

We see that only providing the winning nonce is not enough, and providing all of them is way too much. Is there a middle ground?

Consider this idea: Before the search starts, the excavation manager flies over the search area in his helicopter, randomly scattering plastic tokens across the vast corn fields. The number of tokens is tiny compared to the billions upon trillions of stalks of corn, but still large enough to count. Say, ten million of them.

Now, each member of the search excavation can collect these tokens as they encounter them, giving a rough approximation of how much ground they covered. When the treasure is finally recovered, each member will get a share proportional to the number of tokens they found. For example, if Alice, Bobette, and Charline found 3, 5, and 7 tokens, then Bobette will get a fraction of  $$5/(3+5+7)$$, or _one-third,_ of the treasure. Note that we only divide by the number of _found_ tokens.

To translate this intuition to blockchains, recall that [in proof-of-work](https://shai-deshe.gitbook.io/pow-book/part-1-blockchains-and-blockdags/chapter-1-bft-vs.-pow/how-pow-works), attempting to solve the block means changing it a little bit (in particular, a field called the _nonce_, designated for that purpose) and _hashing_ it. The hashing operation will return, for each attempt, a _uniformly random_ number between $$0$$ and $$N-1$$ for some huge $$N$$ (typically, $$N=2^{256}$$). Solving the block means finding a nonce that hashes below some _difficulty target_ $$T$$.

In our search excavation analogy, the members are miners, the ground they cover is the nonces they tried, and the treasure is a nonce that hashes to a number smaller than the difficulty target. But what are the plastic tokens?

An ubiquitous way to capture them is in terms of something called a subblock.&#x20;

Say that we are looking for a nonce that hashes below $$T$$, how many nonces that hash below $$2T$$ do we expect to find along the way?

Well, since the hash value is uniformly random, hashing below $$2T$$ is _twice as likely_. So we expect to find _two_ such nonces along the way. Similarly, we expect to find $$3$$ hashes below $$3T$$ and, more generally, $$n$$ hashes below $$n\cdot T$$.

We usually like $$n$$ to be a power of two, so we assume $$n=2^k$$. If the difficulty target is $$T$$, we call a block with a nonce that causes it to hash below $$2^k\cdot T$$ a $$k$$-_subblock_.

**Question**: What do you think is the reason we use $$k$$-subblocks to refer to blocks that hash below $$2^k\cdot T$$ and not $$k\cdot T$$?

<details>

<summary>Answer</summary>

Because it is often much more natural to think how much a block is eavier/lighter than it should be in terms of _how many leading zeros_ it has, and not the actual numerical value. A $$k$$-subblock has at most $$k$$ more leading zeros than a full block.

In proof of work it is often more natural to talk in terms of _entropy_, which essentially counts _bits_. If $$T$$ happens to be a power of two, $$T=2^m$$, then saying that the output is "smaller than $$T$$" is saying that all digits in the output, except perhaps the least $$m$$ digits, are zero. We allow a $$k$$-subblock to be $$2^k$$ times larger, which means we soften the requirement to allow the least $$m+k$$ digits to be non-zero. That is, a $$k$$-subblock is required to have $$k$$ zeros less than a valid block..

</details>

Say we set $$k=10$$, then finding a $$k$$-subblocks is $$2^{10} \approx 1000$$ easier than finding a block. In other words, we expect about a thousand $$k$$-subblocks to be found in the process of looking for the block. Moreover, the number of subblocks each miner finds should be proportional to the fraction of the work they did. Just like an excavator that covers twice as large an area will find roughly twice as many plastic chips (and the approximation becomes rapidly more accurate as we increase the number of chips).

**Exercise**: The analogy I made is not entirely accurate. Can you spot the lie? How would you modify _the algorithm_ such that it matches the definition?

<details>

<summary>Hint</summary>

Think about how shares distribute with respect to blocks. Now, think about how plastic chips distribute with respect to treasures.

</details>

<details>

<summary>Answer</summary>

Note that in our definition, a _block is always a subblock_. We defined a $$k$$-subblock as having a hash below $$2^k\cdot T$$, and a block as having a hash below $$T$$. Clearly satisfying the latter term implies satisfying the former.

In our analogy, a "block" is a treasure, and a "subshare" is a chip. However, it is possible to find a treasure without finding a chip! Fixing the analogy means making sure there is a chip in every treasure chest. However, we actually prefer to go the other way, and fix the protocol to match the analogy. Why? Because generally speaking, unneeded dependencies should be avoided, and there's no good reason to insist on retaining a dependency between blocks and shares we can easily remove.

We can remove this by using what's known as the "two-for-one PoW trick". To check if a nonce gives a block, hash it and check whether the result is smaller than $$T$$. To check if a nonce gives a share, hash it, _reverse the result_ (when written as a binary string), _flip its bits_, and check whether the result is smaller than $$2^k\cdot T$$. The idea is that when checking for one thing, we use the rightmost bits, and when checking for the other, we use the leftmost bits. That is, for one purpose we read the number left-to-right, and for the other we read it right-to-left.

If we assume $$2 \log(T) + k \ll \log(N)$$, we get that the dependency between being a block and being a share is overwhelmingly small. The details are left as a recommended exercise in elementary probability theory.

</details>

Subblocks/share seem to be a handy tool indeed to probe the hash rate among miners. But applying it requires more work. For protocols that want to use them on-chain, we need to find a way to include them that will not degrade the security of the network and will not be vulnerable to the same selfish mining attacks that exist in Bitcoin.

<div align="center"><figure><img src="../.gitbook/assets/image (4).png" alt="" width="375"><figcaption></figcaption></figure></div>



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

<figure><img src="../.gitbook/assets/image (2).png" alt=""><figcaption></figcaption></figure>

Note that each fruit has exactly one harvest time and is packed into at most one basket. However, some of the fruit, even though a bit old, are not packed into any basket. This is a crucial part of the honest assumption: baskets are not **required** to pack any fruit, and are not even **incentivized** to do so. They are not **penalized** for packing fruit either, so it is not entirely outlandish to expect _honest_ miners to pack them, but it is far from ideal. We will dive into the dynamics of this process shortly.

The analogy to Bitcoin should roughly be something like this: baskets replace blocks, and fruits replace _transaction data_. When choosing the heaviest chain, we disregard fruit completely. _After_ selecting the chain, the baskets are processed along with the fruit, and rewards are distributed.

So how are rewards distributed? Simply. Each fruit is worth the same reward (at least assuming we weren't unfortunate enough to do our analysis exactly during a halving), which goes (along with the transaction fees) to whoever mined the fruit. The **entire point** is that fruits provide higher resolution samples for how the work is divided. Rewarding any other way will undermine this goal.

"But wait?" I hear you say, if miners don't get any advantage for packing fruits other than their own, why should they even bother? Isn't it just a wasted effort?&#x20;

Eh, yeah, we'll get to that...

So the affluence of fruit represents rewards, while the scarcity of blocks represents weight. Sounds kind of familiar, doesn't it? Of course, _the fruits are the plastic chips from the previous analogy_. But how well do they work?

Before we dive into the incentives, there is one more crucial aspect to introduce: freshness. It is not ostensibly clear why freshness matters, and in fact, it might seem like an arbitrary imposition, but it is actually very important. The freshness threshold is the valve that trades off fairness with responsiveness. The _freshness_ from the point of view of a given block is just how long it has been since the fruit was harvested. (The term is a bit misleading, as fresher fruits have _lower_ freshness. I would rather call it _ripeness_. But it is what it is.)

The freshness threshold tells us how fresh a fruit must be to be valid. After that point, it becomes _spoiled_, and surely any sensible person will agree that a fruit basket that packs spoiled fruit is invalid. Here is an illustration for a freshness threshold of three:

<figure><img src="../.gitbook/assets/image (5).png" alt=""><figcaption></figcaption></figure>

With that, we understand all of the ingredients and rules that define the FruitChain protocol. So let us try to understand what it achieves.

<details>

<summary>FruitChains protocol summary</summary>

### Parameters

* Freshness bound $$R$$  (a.k.a recency bounded) — how long since harvesting a fruit remains fresh
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

### The Advantages

