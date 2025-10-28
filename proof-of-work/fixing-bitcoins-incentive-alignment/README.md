---
description: 'Or: Selfish mining for selfless people.'
---

# Fixing Bitcoin's Incentive Alignment

This series was commissioned by [Quai network](https://qu.ai/) to introduce one of their current efforts: the Proportional Reward Splitting (PRS) protocol.

Our goal is to provide an accessible introduction to the world of incentive alignment in proof-of-work protocols. Like most of my writing, it attempts to hold the sticks on both ends by appealing to both   enthusiastic, curious amateurs and seasoned researchers looking for a primer to ease them into the discussion and provide a big picture frame before diving into the cumbersome literature.

The purpose is _not_ to dryly explain the rules of the PRS protocol. I can do that in two paragraphs (and I indeed have, when appropriate). Such a dense and unmotivated summary might be useful for experienced PoW protocol designers, but it will go very little towards helping both the amateur and the researcher. No, in order to understand PRS we first have to understand the problems it is out to solves, and the solutions that preceded it. We do so in the first two posts, and defer actually discussing PRS to the third one.

[The first part](part-i-bitcoin.md) has three goals. First, we introduce an eerie phenomenon discovered in 2014 by Eyal and Sirer: selfish mining. (This part is somewhat orthogonal to the [selfish-mining section in my book](https://shai-deshe.gitbook.io/pow-book/part-1-blockchains-and-blockdags/chapter-2-the-block-chain-paradigm/selfish-mining-in-bitcoin):  it does not dive as much into the details and history of selfish mining literature, and instead focuses on a reasonably abstract point of view primed at discussing more complicated protocols in the following parts). We then build the _game-theoretic vocabulary_ needed for a deeper understanding of the phenomenon: What _are_ incentives? What does it mean for these incentives to be _aligned_? What is the difference between _honest_, _rational_ and _Byzantine_ behavior and how can we use these terms to make formal assumptions? With this new toolbox, we can explain selfish mining as a manifestation of the gaps between honest and rational Bitcoin miners. Finally, we can start sniffing how to design a solution by inspecting how mining pools fairly distribute mining revenue by using _shares_. This discussion furnishes the key philosophical insights we are trying to import into the protocol design, and sets us on a path towards a concrete implementation of these ideas in a permissionless consensus.

[The second part](part-2-fruitchains.md) dives into the granddaddy of incentive-aligned PoW protocols: FruitChain. Proposed in 2016 by Pass and Shi, FruitChains is the first protocol that provides provably aligned incentives without deviating from Bitcoin's original trust model. This is a fascinating, theoretically significant, arguably historical protocol. It only has one small drawback: it is impossible to implement in a useful way. The post is geared towards a discussion of this limitation, where at comes from, and what could possibly rectify it.

In [the third part](part-3-proportional-reward-splitting.md), we finally arrive at the PRS algorithm. Since PRS follows the same philosophical route of FruitChains (import workshares into verifiable consensus), the two exhibit many similarities and differences. We explain the subtleties of PRS by exploring how it compares with FruitChains, and what new trade-offs it affords. We conclude the series with a brief discussion on the work that remains on improving PRS and the current efforts by the Quai team. I hope that, having read all three parts, the reader will have an exact enough understanding of this effort to either join the discussion and help complete PRS, or think about it independently.

Last point:  Throughout the post, more challenging aspects are posed as solved questions, hiding within expendable sections. These questions are meant to get your brain gears rotating, but also to clearly mark the more technical comments that might require a bit of formal background. **Skipping these questions entirely will not detract from the rest of the reading experience and is recommended on a first read**.

I hope you enjoy working through these posts as much as I enjoyed writing them!

<p align="right">Shai Deshe</p>

<figure><img src="../../.gitbook/assets/image (1) (1) (1) (1).png" alt="" width="330"><figcaption><p>A shellfish miner</p></figcaption></figure>
