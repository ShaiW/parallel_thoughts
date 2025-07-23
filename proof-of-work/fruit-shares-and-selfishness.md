---
description: What are selfish mining, subshares, and PRS?
---

# Fruit, Shares, and Selfishness

> **Acknowledgement**
>
> This post was funded by the [Quai network](https://qu.ai/), which generously provided me with a grant to fund proof-of-work education.

In this post, we present two solutions for selfish mining, the Fruitchain bla bla bla

## Selfish Mining Primer

In a previous post, I explained [selfish mining in Bitcoin](https://shai-deshe.gitbook.io/pow-book/part-1-blockchains-and-blockdags/chapter-2-the-block-chain-paradigm/selfish-mining-in-bitcoin).

If you're not familiar with selfish mining, I suggest reading that post first. The executive summary is that the incentives in Bitcoin aren't exactly aligned with how we would like miners to behave.

The Bitcoin protocol assumes that _honest_ miners follow two simple rules:

1. Always mine over the top of the heaviest chain
2. Whenever you discover a new block (either by solving it yourself or hearing about it from one of your peers), broadcast it to all your peers _immediately_

In reality, we [do not expect miners to be honest, but _rational_](https://shai-deshe.gitbook.io/pow-book/part-1-blockchains-and-blockdags/chapter-2-the-block-chain-paradigm/honesty-and-rationality). We assume a majority of the miners in the network are seeking to maximize their Bitcoin profits from fees and mining. Under this assumption, we can influence miners' behavior by _incentivizing_ them.

The incentive in Bitcoin is straightforward: if your block is on the heaviest chain, you win fees and a block reward. It is not hard to believe that mining over any block but the top of the heaviest chain increases the chances that your block will be orphaned, thus decreasing your expected gain and encouraging miners to follow the first rule. The second rule doesn't align quite as nicely. It is rational for small miners to follow it, but as it turns out, sufficiently large miners can gain from _withholding_ (and potentially orphaning) blocks.

[In their paper](https://arxiv.org/abs/1311.0243), Eyal and Sirer present a strategy that increases the profit of a large miner by withholding blocks.

The idea is that by withholding the blocks they created, only releasing them at strategic times, a large miner can increase the orphan rates of the rest of the network more than its own orphan rates, causing their proportion of non-orphaned work to increase, whereby earning then a bigger cut of the reward than their coontribution to mining.

For some concrete numbers, consider this figure from their paper:

<figure><img src="../.gitbook/assets/image.png" alt=""><figcaption><p>(Fig 2. from Eyal-Sirer)</p></figcaption></figure>

$$\gamma$$ measures _connectivity:_ the probability a majority of the miners would choose the attacker's block if it is released exactly at the same time as an honest block.&#x20;

We see that even if we assume zero connectivity, an attacker with more than 33% can profitably carry out the attack, while as little as 44% suffices to create a _majority_ of the blocks non-orphaned.&#x20;

With perfect connectivity, 33% is already enough to create a majority of the non-orphaned blocks, and _any_ perfectly connected attacker has something to gain from a selfish mining attack.

The most realistic scenario is that the attacker's connectivity parameter is somewhere in between, say halfway. In this case we see that 25% are enough for a profitable attack, while 38% are enough to create a majority of non-orphaned blocks.

A common misconception is that because a 38% attacker can create a majority of the blocks, she can double-spend. It makes sense that by making more blocks than the honest network, you can create a competing chain, but that's _not what you do_ in selfish mining. The _total_ fraction of blocks remains the same, but you constantly headbutt with honest blocks to kick them off the chain. You can only do this by pointing at, or near, the heaviest tip, which is impossible if you spend your efforts on mining a side chain.&#x20;

A successful double-spend attack looks like this:

<figure><img src="../.gitbook/assets/image (1).png" alt=""><figcaption></figcaption></figure>

whereas a successful selfish mining attack looks like this:

<figure><img src="../.gitbook/assets/image (2).png" alt=""><figcaption></figcaption></figure>

Note that in the latter example, the red blocks constitute the majority of _chain_ blocks, but the blue blocks are still the majority of _all_ blocks.

## Chain Quality (and Lack Thereof)

A key nuance in the discussion above is that _we don't like selfish mining_, but it _doesn't allow a double-spend attack_. In other words, it is a behavior that is considered adversarial, but is not captured in the colloquial definition of [what makes a blockchain secure](https://shai-deshe.gitbook.io/pow-book/part-1-blockchains-and-blockdags/chapter-2-the-block-chain-paradigm/security-notions).

It is natural to [define a security notion](https://shai-deshe.gitbook.io/pow-book/part-1-blockchains-and-blockdags/chapter-2-the-block-chain-paradigm/security-notions) that captures selfish mining attacks. That is exactly what Garay, Kiayias, and Leonardos did when they described the [Bitcoin backbone protocol](https://eprint.iacr.org/2014/765), a version of Bitcoin that is simplified enough for mathematical analysis, but more accurate than previously used models.

In that paper, they introduce the _chain quality_ property. The precise definition is a bit technical, but the gist is this:

**Definition** (reproduced from Definition 4 in [GKL](https://eprint.iacr.org/2014/765), simplified, informal): A blockchain has the chain quality property if the amount of non-orphaned blocks produced by a miner with a fraction $$\alpha$$ of the global hashrate gets closer to a fraction of $$\alpha$$ of the blocks as time passes.

The key hidden detail here is how long we need to wait before the fraction becomes sufficiently close to $$\alpha$$. GKL did not answer this question for a straightforward reason: Bitcoin does _not_ satisfy the chain-quality property.

## Selfish Generals?

In my experience, what I am about to explain in the following section shatters the way many people view Bitcoin's security properties.

The following statements are facts:

1. Deterministic finality [cannot handle a situation where more than a third of the nodes are faulty](https://shai-deshe.gitbook.io/pow-book/part-1-blockchains-and-blockdags/chapter-1-bft-vs.-pow/byzantine-fault-tolerance).&#x20;
2. In particular, BFT protocols cannot guarantee that they reach an agreement if close to half of the nodes allow themselves to deviate from the protocol
3. In Bitcoin, we only need (slightly more than) half of the miners to be honest to assure consensus is reached in a timely manner and becomes irreversible fast

It is natural to assume that in this case, we can also use Bitcoin for binary voting: just let each miner post a "yes" or "no" on their blocks and then do a majority count.

Selfish miner proves that this is not the case: a sufficiently connected 34% attacker can create a majority of the blocks and win the vote.

Apparently, while it is true that Bitcoin can handle a higher fault threshold, the property that a collusion of more than a third of the voters could always create a majority of the blocks _persists_. In particular, for _any protocol,_ including probabilistic ones, a _perfectly connected adversary_ with more than a third of the global hashrate could _always_ produce a majority of the blocks.

So why are we even doing this?

Because the assumption of a perfectly connected adversary is unrealistic. Remember, a perfectly connected adversary has the following property: if the adversary withholds a block $$B$$, and then upon hearing about a competing block $$C$$ releases block $$B$$, they are _guaranteed_ that the network will prefer $$B$$ over $$C$$.

It's hard to imagine such an adversary in reality. Even for a very well-connected adversary, there must be some other miner sufficiently distant that, by the time the attacker learns of their blocks, most honest miners also have, giving the attacker's block a _zero_ chance to win.

Furthermore, the ability to selfishly mine becomes quite limited quite fast as the connectivity parameter $$\gamma$$ becomes smaller. This is already apparent in the Eyal-Sirer graph above. However, we see that for low (even zero) values of $$\gamma$$, a sufficiently larger less-than-half adversary can still accrue disproportionate gains.

Fixing _this_ is the problem that inspired the protocols we are about to discuss.

## Marco? Polo!

Mining pools actually have to face a very similar problem. In a mining pool, many miners work together to produce a single block. Despite their cooperation, only _one of them_ produces the winning nonce, so how can you divide the reward?

Think about it like a search excavation looking for a lost treasure. Make sure you understand the analogy, because we'll be building on it.

The excavation decides in advance that the treasure will be shared, with the reward of each participant proportional to the ground they covered in the search. How can you know how to split the reward?&#x20;

Based only on knowing who found the treasure, you _can't_. The finder might have done most of the work, or their fair share of work, or maybe they were extremely lucky and found the treasure in the first place they looked. If the only information you have is who found the treasure, all three scenarios are _indistinguishable_.

To better suit our analogy, we recall that [in proof of work](https://shai-deshe.gitbook.io/pow-book/part-1-blockchains-and-blockdags/chapter-1-bft-vs.-pow/how-pow-works) there isn't just one treasure, but $$T$$ of them, where $$T$$ is known as the _difficulty target_. When mining, we try various different _nonces_, until we find one such that the hash is smaller than $$T$$. Since the result of hashing a new nonce is a uniformly random number between $$0$$ and $$N-1$$ (where $$N$$ is fixed and depends on the hash function, in most cases $$N=2^{256}$$). This is similar to assuming our excavation area is $$N$$ square feet, and we consider checking one square foot as one unit of work. That the difficulty is $$T$$ is like assuming there are $$T$$ treasures randomly scattered in the area, but that there is no benefit in finding more than one treasure (say, all treasures contain the secret key of the same Quai wallet).

So, you need additional information, but what kind of information? Imagine this: before the search starts, the excavation manager flies over the search area in his helicopter, from which he throws a million plastic tokens that scatter randomly across the landscape.

The digital version of this idea is _subblocks_. To understand what a subblock is, first consider this question: what is the probability that I find a nonce such that the hash is less than $$2T$$?  This is twice as easy as finding a nonce (because there are twice as many numbers that are smaller than $$2T$$ than there are numbers that are smaller than $$T$$). We call a block header with a nonce that satisfies the condition a $$1$$-_subblock_. More generally, a $$k$$_-subblock_ is a block whose hash (including the nonce) is at most $$2^k\cdot T$$.

**Remark**: The reason it is defined like this, and not simply as $$k\cdot T$$, is that it is technically easier. In proof of work it is often more natural to talk in terms of _entropy_, which essentially counts _bits_. If $$T$$ happens to be a power of two, $$T=2^m$$, then saying that the output is "smaller than $$T$$" is saying that all digits in the output, except perhaps the least $$m$$ digits, are zero. We allow a $$k$$-subblock to be $$2^k$$ times larger, which means we soften the requirement to allow the least $$m+k$$ digits to be non-zero. That is, a $$k$$-subblock is required to have $$k$$ zeros less than a valid block.

Say we set $$k=10$$, then finding a $$k$$-subblocks is $$2^{10} \approx 1000$$ easier than finding a block. In other words, we expect about a thousand $$k$$-subblocks to be found in the process of looking for the block. Moreover, the number of $$k$$-subblocks each miner finds should be about proportional to the fraction of the work they did. Just like an excavator that covered a twice larger area will find roughly twice as many plastic chips.

**Exercise**: The analogy I made is not entirely accurate. Can you spot the lie? Assuming that we want to modify the protocol to match the analogy, how would you fix this?

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

So now the problem seems rather simple, right? Just ask miners to send over their subblocks (which in this context are more commonly called _shares_) to the pool operator, and tally them up to divide rewards.

Well, it's not that simple. This kind allows pool operators to cheat. They have no accountability for "losing" some of the shares or lying about shares that do not exist. There is an entire family of protocols designed to reduce the trust element, including PPS+, PPLNS, FPPS, and others.

However, remember that we don't want to build a mining pool; we want to counter selfish mining. So what if we ask each miner to attach all shares they found while mining, and divide the prizes proportionally to the share count? We don't need any trust here, because the shares must be _on chain_ and thus verifiable by _everyone_. This observation inspired the first protocol we will examine.

## Grab Me a Fruit, Will Ya?

