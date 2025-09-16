---
description: How Eyal and Sirer ruined Bitcoin forever (but not really)
---

# Part I: Bitcoin

> **Acknowledgement**
>
> This post was funded by the [Quai network](https://qu.ai/), which generously provided me with a grant to fund my proof-of-work education efforts.

The Bitcoin protocol famously assumes that _honest_ miners follow two rules: always point at the tip of the selected chain, and never withhold blocks. We call this the _honest strategy_.

How reasonable is it for miners to follow this rule in practice? For that, we consider a mixture of honest and _rational_ miners. Honest miners are those who follow the honest strategy. We only make two assumptions about rational miners: that they are seeking to _maximize profits from mining_, and that they are not colluding.

<details>

<summary>What makes this utility "rational"?</summary>

From my experience, many people first find the rationality assumption reasonable: after all, what does a miner want if not to earn money from mining? After some thought, doubts start to creep in: why should a rational person care about the _source_ of revenue? Any miner would agree to stop mining if I pay them twice their expected revenue. Why isn't this reflected in what a "rational behavior" should be?

My answer to that is that you shouldn't take the term "rational" too seriously. It is meant to designate the desire to maximize a given utility — in our case, the utility is mining revenue. Calling a miner irrational implies that they have _a different utility._ There are quite a few scenarios where this happens. It could be that the miner has some _externality_ they consider, such as wanting to harm one chain to help another, or an eccentric millionaire willing to pay them a hefty sum to disturb the network. Of course, it could simply be the case that the miner is a lunatic who wants to watch the world burn, but it is not the _only case_ where miners might be irrational.

To obfuscate this point of confusion, many authors use the term "byzantine" instead of irrational to consider miners who behave arbitrarily, and we can make no assumptions about their utility (or even that there exists a utility that they are maximizing).

For a more extended discussion, see the relevant section of [my book](https://shai-deshe.gitbook.io/pow-book/part-1-blockchains-and-blockdags/chapter-2-the-block-chain-paradigm/honesty-and-rationality).

</details>

<details>

<summary>Why can you assume miners do not collude?</summary>

This assumption is just a technicality that simplifies things. Any strategy that a colluding $$\alpha$$ miner and $$\beta$$ miner might be employed can be simulated by a single $$\alpha+\beta$$ miner, so "clumping together" colluding miners into a single miner simplifies the discussion without sacrificing security.

</details>

It is not hard to convince oneself that a rational miner will always point to the tip of the heaviest chain they know: pointing to any other tip increases the probability your block will be orphaned, thus reducing your expected value. However, it is not so clear that rational miners will never choose to withhold a block. In fact, it is false.

[In their paper](https://arxiv.org/abs/1311.0243), Eyal and Sirer present a strategy that increases the profit of a large miner by withholding blocks.

The idea is that by withholding the blocks they created, only releasing them at strategic times, a large miner can increase the orphan rates of the rest of the network more than its own orphan rates, causing their proportion of non-orphaned work to increase, whereby earning then a bigger cut of the reward than their contribution to mining.

<details>

<summary>Why even talk about honest miners?</summary>

Some readers might find the notion of honest miners superfluous. After all, if rational miners are not necessarily honest, why should any miner be honest?

There are several reasons why honest miners are important.

First, they are our baseline. The entire point of this series is to understand incentive _alignment_. The honest strategy tells us _how_ we want to align the incentives: such that rational miners employ the honest strategy.

Second, they allow us to make stronger negative statements: the Eyal-Sirer proves that a sufficiently large rational miner can earn more than their share. But it actually prove something _much stronger_: that selfish mining works even assuming an _honest majority_. It is _not_ a consequence of most miners choosing rationality over honesty. Selfish mining is possible even if you have a majority of altruistic miners that follow the honest strategy to the letter out of the kindness of their hearts. That is a much stronger statement!

Finally, they allow us to make reasonably weaker assumptions. Working in a fully rational setting can be very challenging, and sometimes even not well defined. Consequently, many results and analyses about Bitcoin rely on an honest majority assumption. In this sense, the proportional reward splitting mechanism is unique because it manages to remove this honest majority assumption.

</details>

## Bitcoin and Selfishness

For those who want the details of the Eyal-Sirer attack, as well as an overview of the subsequent attacks and countermeasures, I recommend the [relevant section](https://shai-deshe.gitbook.io/pow-book/part-1-blockchains-and-blockdags/chapter-2-the-block-chain-paradigm/selfish-mining-in-bitcoin) of my book.

The upshot of the attack, in concrete number form, is summarized in this figure lifted from their paper:

<figure><img src="../../.gitbook/assets/image (3) (1).png" alt=""><figcaption><p>(Fig 2. from Eyal-Sirer. The horizontal axis is the selfish miner hashrate fraction <span class="math">\alpha</span>, the vertical axis is the expected gain <span class="math">\alpha(1+\delta)</span>)</p></figcaption></figure>

$$\gamma$$ is the _tie-winning probability_. Imagine that Alice withholds a block until she hears about a competing block from the honest network, and then she releases _her withheld block_. We let $$\gamma$$ be the probability that the network prefers Alice's withheld block over the honest block. It is a measure of how "well connected" Alice is.

We see that even if we assume zero connectivity, an attacker with more than 33% can profitably carry out the attack, while as little as 42% suffices to create a _majority_ of the blocks non-orphaned.&#x20;

With perfect connectivity, 33% is already enough to create a majority of the non-orphaned blocks, and _any_ perfectly connected attacker has something to gain from a selfish mining attack.

The most realistic scenario is that the attacker's connectivity parameter is somewhere in between, say halfway. In this case, we see that 25% is enough for a profitable attack, while 38% is enough to create a majority of non-orphaned blocks.

A common misconception is that because a 38% attacker can create a majority of the blocks, she can double-spend. It makes sense that by making more blocks than the honest network, you can create a competing chain, but that's _not what you do_ in selfish mining. The _total_ fraction of blocks remains the same, but you constantly headbutt with honest blocks to kick them off the chain. You can only do this by pointing at, or near, the heaviest tip, which is impossible if you spend your efforts on mining a side chain.&#x20;

A successful double-spend attack looks like this:

<figure><img src="../../.gitbook/assets/image (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

whereas a successful selfish mining attack looks like this:

<figure><img src="../../.gitbook/assets/image (2) (1) (1).png" alt=""><figcaption></figcaption></figure>

Note that in the latter example, the red blocks constitute the majority of _chain_ blocks, but the blue blocks are still the majority of _all_ blocks. That is, judging from the chain alone it seems like the red miner has a majority of the hashrate, but the orphans reveal that this is not quite the case. In this scenario, the attacker will receive a majority of the rewards despite not mining a majority of the block, which is exactly the crux of selfish mining attacks.

### Chain Quality (and Lack Thereof)

A key nuance in the discussion above is that _we don't like selfish mining_, but it _doesn't allow a double-spend attack_. In other words, it is a behavior that is considered adversarial, but is not captured in the colloquial definition of [what makes a blockchain secure](https://shai-deshe.gitbook.io/pow-book/part-1-blockchains-and-blockdags/chapter-2-the-block-chain-paradigm/security-notions).

It is natural to [define a security notion](https://shai-deshe.gitbook.io/pow-book/part-1-blockchains-and-blockdags/chapter-2-the-block-chain-paradigm/security-notions) that captures selfish mining attacks. That is exactly what Garay, Kiayias, and Leonardos did when they described the [Bitcoin backbone protocol](https://eprint.iacr.org/2014/765), a version of Bitcoin that is simplified enough for mathematical analysis, but more accurate than previously used models.

In that paper, they introduce the _chain quality_ property. The precise definition is a bit technical, but the gist is this:

**Definition** (reproduced from Definition 4 in [GKL](https://eprint.iacr.org/2014/765), simplified, informal): A blockchain has _ideal_ chain-quality if the amount of non-orphaned blocks produced by a miner with a fraction $$\alpha$$ of the global hashrate gets closer to a fraction of $$\alpha$$ of the blocks as time passes.

The key hidden detail here is how long we need to wait before the fraction becomes sufficiently close to $$\alpha$$. GKL did not answer this question for a straightforward reason: Bitcoin does _not_ satisfy the _ideal_ chain-quality property.

<details>

<summary>Is there "non-ideal" chain quality?</summary>

Yes!&#x20;

The GKL analytical framework (the so-called "Bitcoin backbone protocol") makes two assumptions: semi-asynchronisity (the network delay is bounded), and honest majority.

In this framework, the "real" property we're after (in a notation slightly more approachable than GKL's) is $$\ell$$-chain $$\alpha$$-quality, where $$\alpha$$ is a number between zero and one representing the fraction of an arbitrary, possibly selfish miner while, and $$\ell$$ is a positive integer designating how many blocks we look at when we check for fairness.

In other words, we can define $$e_{\ell,\alpha}$$  to be the expected proportion of blocks out of the next $$\ell$$ blocks that were created by the $$\alpha$$-miner, and we define $$\alpha$$-chain-quality to be the case where $$e_{\ell,\alpha}$$ approaches the constant $$\alpha$$ (that is, the _variance_ vanishes) as $$\ell$$ increases (GKL's definition is actually stronger, and guarantees a _deterministic_ upper bound, but this version is accurate enough for our purposes).

Having _ideal_ chain quality is the same as having $$\alpha$$-chain-quality for any $$\alpha<1/2$$.

GKL note that Bitcoin does have perfect _honest_ chain-quality. That is, in case everyone follows the protocol, the reward is distributed fairly. But this is a trivial statement that we know already. The analysis gets interesting when the $$\alpha$$-miner is _arbitrary_, and in particular may be adversarial.

Eyal and Sirer's attack proves that Bitcoin does not have ideal chain quality. Even if we assume a very poorly connected miner ($$\gamma = 0$$), Eyal-Sirer tells us we can hope for at most $$1/3$$-chain-quality, and for a perfectly connected adversary ($$\gamma=1$$) there's no $$\alpha$$-chain-quality for _any_ $$\alpha>0$$. GKL extend the analysis to provide more accurate lower bounds on a worst-case attacker.

Note that the chain quality does not quantify _how profitable_ selfish-mining is (for that there's the $$\delta$$-fairness property we will discuss a bit later), nor does it care about _how quickly_ we obtain fairness, that is, how large do we need $$\ell$$  to be to accurately estimate $$\alpha$$ by observing $$\ell$$ blocks. This will also come up a bit later.

(Note that $$\ell$$ can depend on $$\alpha$$, and indeed it must be the case that $$\ell$$ increases as $$\alpha$$ approaches $$1/2$$, even for a fixed confidence.)

</details>

### Selfish Generals?

In my experience, what I am about to explain in the following section tends to contradict how many people view Bitcoin's security properties.

The following statements are facts:

1. Deterministic finality [cannot handle a situation where more than a third of the nodes are faulty](https://shai-deshe.gitbook.io/pow-book/part-1-blockchains-and-blockdags/chapter-1-bft-vs.-pow/byzantine-fault-tolerance).&#x20;
2. In particular, BFT protocols cannot guarantee that they reach an agreement if close to half of the nodes allow themselves to deviate from the protocol
3. In Bitcoin, we only need (slightly more than) half of the miners to be honest to assure consensus is reached in a timely manner and becomes irreversible fast

It is natural to assume that in this case, we can also use Bitcoin for binary voting: just let each miner post a "yes" or "no" on their blocks and then do a majority count.

Selfish mining proves that this is not the case: a sufficiently connected 34% attacker can create a majority of the blocks and win the vote.

Apparently, while it is true that Bitcoin can handle a higher fault threshold, the property that a collusion of more than a third of the voters could always create a majority of the blocks _persists_. In particular, for _any protocol,_ including probabilistic ones, a _perfectly connected adversary_ with more than a third of the global hashrate could _always_ produce a majority of the blocks.

<details>

<summary>Really? <em>Any</em> protocol?</summary>

OK, not exactly. There are protocols that manage to provide a higher than third bound even for an attacker that wins all ties. The most known (perhaps only) example is the [Bobtail](https://arxiv.org/pdf/1709.08750) protocol and its derivatives.

But there's obviously a caveat: Bobtail changes the rules for _block discovery._ This is a very deep consensus change that excludes Bobtail from the so-called "backbone protocol", the most standard framework for analyzing blockchain protocols (now don't get me wrong, there is _a lot_ of meaningful analysis outside the relatively limited backbone protocol framework, but in most cases, the protocol _itself_ can be described in this framework).

Consequently, the techniques and general theorems proved within the backbone protocol no longer apply to the protocol, forcing a proper analysis to either provide complicated reductions or generalize these theorems to more refined models. So, for example, the Bobtail paper falls short of providing a rigorous analysis or even a formal model and relies on evidence such as security proofs in limited threat models and empirical data.

</details>

So why are we even doing this?

Because the assumption of a perfectly connected adversary is unrealistic. A perfectly connected adversary _always_ wins ties. She hears of _all_ blocks _extremely_ fast (no matter who created the block, she _always_ hears about it before more than half of the network), and can transmit blocks to almost _anyone._

It's hard to imagine such an adversary in reality. Even for a very well-connected adversary, there must be some other miner sufficiently distant that, by the time the attacker learns of their blocks, most honest miners also have, giving the attacker's block a _zero_ chance to win.

Furthermore, the ability to selfishly mine becomes quite limited quite fast as $$\gamma$$ becomes smaller. This is already apparent in the Eyal-Sirer graph above. However, we see that for low (even zero) values of $$\gamma$$, a sufficiently large less-than-half adversary can still accrue disproportionate gains.

Fixing _this_ is the problem that inspired the protocols we are about to discuss.

## Unselfishing Bitcoin?

The aftermath of the discovery of selfish mining led to various approaches for mitigating its effects. As usual, the Bitcoin community was averse to modifying the underlying protocol. Some suggested changes to peer-to-peer policies (such as block relaying and tie-breaking rules) that, while not prohibiting the attack, would make it harder to carry out. Others argued that selfish mining is not a significant concern, given the extreme measures required to carry it out profitably.

On the theoretical front — where the motivation is not the preservation of Bitcoin, but understanding what probabilistic consensus can or cannot do — people work on developing protocols where this problem does not exist.

### Statistical Convergence Rates

We laid out our goal: to make reward shares more fair.

However, we must recall that altering the reward distribution method can also affect properties we often take for granted. One crucial aspect is how long it takes the reward share to converge into a fair distribution. Say that a protocol assures that if we track the earnings of an $$\alpha<0.5$$ miner for long enough, they will approach a fraction of $$\alpha$$ of the total emissions. How long is "long enough"?

Even if the protocol assures that it eventually happens, it could be that as we require more exact approximations, the waiting times shoot through the roof, even if the precision we expect is completely within reason. For example, we will see soon an example where obtaining reasonable confidence that the error is less than $$1\%$$ can take _days_.

Preserving chain quality is a qualitative statement that poses no requirements on the convergence rate (except that it can be computed from the precision and confidence we expect). In practice, this is not enough.

This is not just about patience. Tracking reward distribution is crucial for the everyday operations of pools and exchanges. In a while, we will introduce _shares_, a way for a miner to prove to a pool that they have done part of the work. A pool typically pays out for the share in advance, based on an _estimation_ of the actual reward. An incorrect estimation can lead to a pool bleeding money. A protocol that forces pools to either take monetary risks or withhold payouts for days or weeks is impractical.

### The State of the Art

A holy grail solution to selfish mining is a protocol that assures rapidly converging chain quality even if we only assume that a majority of miners is _rational._

We are not quite there yet.

The first successful attempt at aligning proof-of-work incentives is the [_FruitChains_](https://eprint.iacr.org/2016/916) protocol, introduced in 2016 by Pass and Shi. FruitChains manages to find a little weak, but still very satisfying, compromise between rationality and honesty. The chain quality property holds, in the sense that an _honest_ miner will earn as much as they should _as long a majority of miners are honest_.

Wait what? Isn't this precisely what we _don't_ want to assume?

Well, its subtle: in Bitcoin, a large miner can deviate and _immediately benefit_, even if all other miners are honest. In FruitChain, this is no longer the case. Deviation does not penalize you, but as long as no other miner deviates in the same way, it does not gain you anything either. This is a _highly non-trivial_ property.

However, FruitChains has a drawback that makes it unusable: the time it takes to converge _increases_ with the security guarantees we want.&#x20;

Let us make this statement a bit more quantifiable: say we want the protocol to guarantee that if we count shares for $$k$$ blocks, there's a probability of $$2^{-\kappa}$$ that rewards will not deviate by more than $$\delta > 0$$. What should we set the number of shares per block $$\lambda$$ to be? (If these notations are unclear to you, hang tight, I introduce them in more detail in the next part).

In PRS, for whatever values of $$\kappa,\delta,k$$ you choose, there is a corresponding $$\lambda$$. **This is not true for FruitChains**. In fruitchains, it turns out that we can only find $$\lambda$$ when $$k$$ is large enough. Moreover, $$k$$ also grows with the fraction of maximal assumed attacker $$\alpha$$. Writing the actual dependence is complicated, but a necessary condition is that $$k\ge2\cdot({\kappa + \log(\kappa/\delta^2)})$$.

This inequality is _very loose_, but even the rough estimate it provides establishes the point.

Say that we want $$50$$ bits of security that the distribution is fair up to an error of $$10\%$$. We get from the inequality above that this will require at least $$126$$ blocks, _regardless_ of how much shares per block we produce.

These are very lax assumptions. More realistic security expectations are $$\delta = 0.05$$ and $$\kappa=64$$. Here we find that $$k$$ must be at least $$160$$. (And some would argue that $$\delta=0.05$$ is still too lax).

Even with these rough estimates, we see that the convergence runs into days. More tight analyses show that it runs into weeks and months on very reasonable parameter choices.

This remained the state-of-the-art for a while. Literature on selfish-mining-resistant protocols continued to be published, primarily focusing on no-go theorems that demonstrate the vulnerability of various natural approaches to modifying FruitChains. We will mention some of these in part two. A few protocols, such as Bobtail and Prism, tried radically different approaches that weren't adopted due to drawbacks we will not get into.

As far as I know, the only new _recent_ approach (at least within the backbone framework) to emerge following FruitChains is [Proportional Reward Splitting](https://arxiv.org/abs/2503.10185) (PRS), authored by a collaboration of the Quai team and Dionysis Zindros (with whom I am already familiar as the coauthor of [NiPoPoWs](https://eprint.iacr.org/2017/963) and [Mining in Log-Space](https://eprint.iacr.org/2021/623), famously used in Kaspa's pruning protocol).

The PRS protocol is heavily inspired by FruitChains. It is easily the most similar to FruitChains in terms of structure and assumptions. But PRS takes just enough liberties to stand on its own feet and introduces two major improvements.

First, it manages to remove the honesty assumption, replacing it with rationality. Note that this is still not the holy grail. Even in PRS, a rational majority alone is not sufficient to ensure chain quality. Even if all miners are rational, this is not guaranteed. What _is_ guaranteed is that if all miners are rational and none deviates, then a single miner with less than half of the hash rate _gains nothing_ by deviating. The only way to earn from deviating is if there is a majority of deviators. But again, the deviation is not penalized either.

Second, and crucially, the security argument for PRS does not limit the range of $$k$$. In particular, it can be parametrized with as few or as many shares as you want. More shares still provide better convergence, but only because it would take less time to collect **the same number** of shares.

But in our world, there are no solutions, only trade-offs, and what PRS gains in speed and game-theoretic leniency, it pays back in precision. While FruitChain can, in theory, provide selfish mining resilience against **any** $$\gamma=0$$ attacker with less than half of the hashrate, PRS can only provide such security (though with softer assumptions) for miners with at most  $$\sim 40\%$$ of the total hashrate.

For comparison, in Bitcoin, for $$\gamma=0$$ the Eyal-Sirer strategy has a threshold of  $$33\%$$. However, this attack is **not** optimal. A paper by [Sapirshtein and Zohar et al.](https://arxiv.org/abs/1507.06183) isolates the optimal strategies and proves that, for  $$\gamma=0$$, a selfish miner with anywhere above $$25\%$$ of the global hashrate can mine profitably.

We can summarize this into the following table:

<table><thead><tr><th> </th><th width="163">Bitcoin</th><th width="215.79998779296875">FruitChain</th><th>PRS</th></tr></thead><tbody><tr><td>Selfish mining threshold</td><td><span class="math">25\%</span> (<span class="math">\gamma=0</span>)<br>(<a href="https://arxiv.org/abs/1507.06183">Sapirshtein et al.</a>)</td><td><span class="math">50\%</span></td><td><span class="math">38\%-42\%</span></td></tr><tr><td>Model assumptions</td><td></td><td>Honest majority</td><td><strong>Rational</strong> majority</td></tr><tr><td>Required shares/block <span class="math">(\lambda)</span> required to obtain fairness <span class="math">\delta</span> with confidence <span class="math">2^{-\kappa}</span> within <span class="math">k</span> blocks</td><td></td><td><span class="math">\lambda = \Omega\left(\frac{\kappa}{k\delta^2}\right)</span></td><td><span class="math">\lambda = \Omega\left(\frac{\kappa}{k\delta^2}\right)</span></td></tr><tr><td>Lower bound on <span class="math">k</span></td><td></td><td><span class="math">k\ge 2\cdot\left(\kappa + \log_2\left(\frac{\kappa}{k\delta^2}\right)\right)</span></td><td><strong>None</strong></td></tr></tbody></table>

These advances arguably place PRS as the best way yet to make a chain resistant to selfish mining, but  the Quai team is not satisfied. As we will see, the rational strategy is still not the best we can do. Among the rational strategies, there is a unique one that, if all miners follow, maximizes the performance of the protocol. The next goal is to modify the protocol such that all other rational strategies vanish. We will conclude the series with a discussion of this problem and current attempts at a solution.

## Marco? Polo!

Before describing FruitChains and PRS, it's worth considering a similar problem: designing a mining pool.

When you think about it, mining pools have to solve a similar problem: how to divide the block reward among the pool users, such that each user is rewarded proportionally to their contribution.

The setting of mining pools is very different from selfish mining. Since the pool's decision does not affect consensus, the decision doesn't have to be inferable from the chain. Mining pools and users transmit _off-chain_ data in the decision-making process, and only post the final decision to the chain. This is a trade-off: on the one hand, we need this additional information to make a fair decision. On the other hand, this makes the decision process vulnerable to censorship, data manipulation, and other problems that blockchains solve. Reconciling the latter drawback requires sophisticated protocols such as  PPS+, PPLNS, FPPS, and others.

FruitChain and PRS essentially try to take the core idea and try to reverse it: let's post enough of this additional information on-chain, but find a way to do so that is hard to manipulate. The first step to understanding these protocols is to understand what "additional information" mining pools collect and how it is helpful. (While conveniently ignoring the problem of aggregating the information trustlessly).

So, how do mining pools work?

### I had a Witty Title for this Subsection, but it was Too Corny

I like to think of miners in a pool as a search excavation looking for a treasure lost in a vast field of corn. And when I say vast, I mean **vast**, with billions upon trillions of corn stalks.

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

### Shares are for Sharing

Consider this idea: Before the search starts, the excavation manager flies over the search area in his helicopter, randomly scattering plastic tokens across the vast corn fields. The number of tokens is tiny compared to the billions upon trillions of stalks of corn, but still large enough to count. Say, ten million of them.

Now, each member of the search excavation can collect these tokens as they encounter them, giving a rough approximation of how much ground they covered. When the treasure is finally recovered, each member will get a share proportional to the number of tokens they found. For example, if Alice, Bobette, and Charline found 3, 5, and 7 tokens, then Bobette will get a fraction of  $$5/(3+5+7)$$, or _one-third,_ of the treasure. Note that we only divide by the number of _found_ tokens.

<div align="center"><figure><img src="../../.gitbook/assets/image (4) (1).png" alt="" width="375"><figcaption></figcaption></figure></div>

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

Subblocks/shares seem to be a handy tool indeed to probe the hash rate among miners. But applying it requires more work. For protocols that want to use them on-chain, we need to find a way to include them that will not degrade the security of the network and will not be vulnerable to the same selfish mining attacks that exist in Bitcoin.
