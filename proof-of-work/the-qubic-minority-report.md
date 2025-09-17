# The Qubic Minority Report

## Clarifications

I... eh... made a mistake.

Ever since I entered the crypto space, it seems that people expect me to work for free. And it always rubbed me in a very wrong way.

Following my departure from Kaspa, I started providing freelance counseling and advisory services. This gave me a very straightforward way to quantify the value of my time, which I proceeded to use to drive the point across.&#x20;

So, for example, if I state that I see a possible attack vector on some project, and some frothing degen goes "_oh yeah **\*drools\*** then why don't you attack it yourself? **\*shits pants\***"_, I calmly respond that "I will gladly do security analysis for you for $600/hour, DM me for details".

Recently, I've been bothered a lot by the Qubic community. No, you know what? Scratch that. I am _constantly_ bothered by the Qubic community (though usually in good spirits). But in the past few weeks, I was bothered particularly about their Monero brigading.

In true "I should've thought about it more carefully" fashion, I [responded to one of them](https://x.com/DesheShai/status/1954484745225527656) with "I dislike both projects equally enough to be impartial. CFB can DM me for a price offer." It took me about thirty seconds to realize that, in this case, it might _actually happen_.

_shit._

Perhaps against my better judgment, I decided this entire situation is too amusing to back away now. CFB, in his known fashion, proceeded to [hold the entire negotiation publicly](https://x.com/c___f___b/status/1954541241275756777) on X.

He might have done it for the lol and troll (and he might have not), but either way, I _loved_ this decision on his part. I have always been opposed to the "never talk publicly about money" sentiment, and I have always considered this culture as something that was instilled into us by corporate overlords to make it harder for workers to realize when they are being underpaid. Look at me deflecting from the story, la di da.

So the upshot is that I was hired buy the Qubic community to write hither post.

The service is clear: I am to analyze the relevant portion of the XMR chain, and explain what I see, and what can and cannot be verified.

But why me?

Simple: because I am, by far, the most vocal, harsh, and obnoxious Qubic critic on CT. It could not have been clearer that I have _no motivation_ to blemish my hard-earned reputation as a ~~nitpicky asshole~~ non-compromising critic for the sake of Qubic, and have every incentive to be as objective as possible.

In fact, if I get to poke fun at them in the process, I consider it a bonus.

Also, just so we're clear on that: I hold exactly zero Qubic and twice as much Monero.

## This Report

In this report, I provide:

1. Cryptographically, independently verifiable proof of the fraction of blocks that were created by the wallet whose seed was provided to me by CFB, in the period of time\
   11.08.2025 12:00:00 UTC - 12.08.2025 12:00:00 UTC\
   (Block heights 3475510-3476208)
2. Instructions on how to verify this proof against any Monero node
3. A preliminary analysis of the Monero difficulty curve
4. My interpretation of the observed data and what it implies about Qubic's hashrate

## Assumptions and Terminology

I assume all blocks whose coinbase transaction was provably paid to the wallet provided by CFB were mined by Qubic in one way or another. This is not something that can be verified cryptographically, as nothing is stopping any other miner from paying this wallet. But this is the weakest assumption we can make that allows us to connect blocks to Qubic.

I will refer to these blocks as "created by Qubic", and to the rest as "not created by Qubic".

Sometimes it is important to distinguish orphaned blocks from non-orphaned blocks, which I will call chain blocks, or just _blocks_ when the intention is clear from context.

If you want to validate the data yourself, here is the proof:&#x20;

{% file src="../.gitbook/assets/coinbase_proofs.csv" %}

and the script to validate it:

{% file src="../.gitbook/assets/validate.py" %}

## Raw Results

Out of the 699 blocks created in the interval 3475510-3476208, exactly 250 were created by Qubic. Setting 3475509 = 0, the blocks created by Qubic are of height $$n=3475510$$ for $$n$$ in:

```python
[3, 6, 8, 13, 15, 19, 20, 22, 35, 36, 40, 45, 53, 54, 55, 58, 67, 68, 73, 74, 80, 81, 82, 83, 87, 99, 100, 114, 122, 127, 129, 132, 133, 135, 137, 142, 143, 144, 148, 158, 159, 163, 164, 165, 166, 171, 172, 176, 177, 178, 179, 186, 187, 196, 197, 207, 208, 209, 220, 221, 225, 226, 228, 229, 230, 231, 234, 235, 237, 238, 253, 254, 257, 260, 261, 265, 266, 271, 272, 275, 276, 277, 278, 279, 280, 281, 282, 283, 284, 287, 288, 289, 290, 291, 292, 293, 294, 295, 296, 297, 298, 309, 310, 311, 313, 314, 315, 316, 320, 324, 328, 329, 330, 331, 332, 336, 337, 338, 339, 340, 341, 344, 345, 348, 349, 350, 356, 357, 360, 362, 363, 364, 370, 371, 373, 374, 377, 378, 379, 380, 381, 382, 383, 384, 385, 387, 388, 392, 393, 397, 398, 399, 400, 401, 403, 404, 407, 408, 411, 412, 424, 425, 435, 436, 437, 438, 439, 467, 468, 469, 470, 471, 472, 473, 474, 476, 477, 484, 485, 486, 487, 488, 489, 490, 491, 492, 494, 495, 500, 503, 504, 507, 510, 514, 521, 524, 526, 529, 537, 547, 548, 551, 556, 559, 562, 564, 568, 569, 570, 572, 575, 578, 579, 582, 583, 584, 588, 590, 591, 593, 594, 600, 602, 614, 615, 619, 620, 621, 625, 628, 629, 637, 638, 642, 644, 649, 650, 651, 654, 655, 665, 667, 670, 673, 674, 676, 687, 689, 691, 692]
```

The script provided above also outputs this array.

## Data Analysis and Interpretation

First, let us make a plot:

<figure><img src="../.gitbook/assets/image (3) (1).png" alt=""><figcaption></figcaption></figure>

Here, the X axis represents the total number of blocks since the start of the inspected period. The blue graph indicates, at each point, what fraction of blocks observed so far (since the period started) are Qubic blocks. The red plot averages a symmetric window around each block, with a radius of 15 blocks, giving the ratio of Qubic blocks among 30 consecutive blocks, or about an hour.

Finally, the gray line is a regression line of the red samples. That is, it is the best linear predictor of the fraction in a given hour, given the data.

The most pressing question is what we can learn from the red line. Are the spikes, e.g. around 270, indicative of a period of strong domination, or are they just stochastic spikes (which are also called in the professional pidgin "a fluke")?

The fact that the regression line is almost flat indicates the latter option. The variance of block creation seems wild, but a variance analysis shows that such deviations are expected in the presence of a 35% large miner, and that's even before discussing the selfish mining/liveness aspect.

Hence, from this data alone, _I cannot concur that during any period Qubic produced more than 35% of the hash power_. In fact, I'd say its most likely that they haven't, but that doesn't mean this experiment was without merit.

### Orphaning and Selfish Mining

So, how much hash power _can_ I confidently attribute to Qubic? That's a tough one.

Qubic mining does not follow the honest strategy, but rather applies a _selfish-mining_ strategy. Selfish miners deliberately withhold blocks and release them at strategic times meant to ensure honest blocks are orphaned. In certain conditions, selfish mining strategies allows miners to make their fraction of _chain_ blocks larger than their _total_ fraction of blocks, making an appearance of higher hash-rate than they already have. Famously, with only 33% of the hashrate, an (extremely well-connected) miner can create a majority of non-orphaned block.

Qubic [claimed in a recent tweet](https://x.com/_Qubic_/status/1956037446732308559) that they implemented a particular selfish mining attack called Eyal-Sirer. While I cannot verify that they actually used this strategy (and that they implement it correctly), I will use this as an assumption. I consider this a safe assumption, as: if they implemented it wrong, it will only play in their favour, as they will need _more_ hashrate to achieve the same result, and they probably didn't implement a better performing strategy, as these tend to be unwieldy in practice.

To learn more about partical selfish mining and Eyal-Sirer, see [this section](https://shai-deshe.gitbook.io/pow-book/part-1-blockchains-and-blockdags/chapter-2-the-block-chain-paradigm/selfish-mining-in-bitcoin) of my book. For a deeper dive into the theory of selfish mining, check out my [currently ongoing series](https://shai-deshe.gitbook.io/parallel-thoughts/proof-of-work/fixing-bitcoins-incentive-alignment) about incentive alignment.

The Eyal-Sirer strategy is very well understood up to a single mysterious parameter: the tie-breaking probability $$\gamma$$. Selfish mining is all about withholding blocks, and releasing them if a competing block arises. In this scenario, what is the probability that the network prefers the withheld block? While the dependency on $$\gamma$$ is typically very strong, it is quite well behaved around the 35% line:

<figure><img src="../.gitbook/assets/image (5).png" alt=""><figcaption></figcaption></figure>

Based on this graph alone, and the length of the attack, we can say that it is highly unlikely that Qubic ever held less than 28% of the total hashrate, and probably had more than 30% (unless their minority of nodes is somehow _considerably_ more connected well connected, among itself and to the rest of the network, than the rest of the network).

But that's with respect to the _current_ hashrate. How much did Qubic hold w.r.t the _original_ hashrate?

### Difficulty Footprint

Given the block data alone, one can't tell whether it was mined by Monero miners who switched to Qubic's pool, or by a sweatshop of kids with abacuses rented to compute RandomX by hand, or by an AGI living in a singularity under Sergey's pillow.

Or can they?

Yes, this is the case when only looking at the block topology, but we have another secret weapon at our disposal: _difficulty_.

Since difficulty adjustment relies on external information (in the form of clocks, used to prevent users from deliberately setting timestamps into the future to reduce difficulty, see [here](https://shai-deshe.gitbook.io/pow-book/part-1-blockchains-and-blockdags/chapter-1-bft-vs.-pow/how-pow-works#difficulty-adjustment)), it provides us with a new keyhole to peep at miners from:

<figure><img src="../.gitbook/assets/image (1) (1).png" alt=""><figcaption></figcaption></figure>

We can see that there is a very clear-cut point where the variance of the curve instantly changes its behaviour. Starting July 16th, the variance sharply increases inexplicably, which is apparent both in the increased rate and amplitude at which it thrashes from minima to maxima (which is sometimes called the "DAA frequency"), and in how jagged it is on a smaller scale.&#x20;

This graph is what you would expect from selfish mining: the serration corresponds to small chain reorgs, while the increased DAA frequency is due to more variance in the difficulty itself (recall that the DAA only sees non-orphaned blocks, so each successful SM reorg is conceived as a sudden hashrate drop).

Qubic announced that "the takeover" will start on Aug 2nd, but from this graph alone, I carefully guess they have been testing in non-negligible volumes as early as July 16th.

To get a better insight on what's going on, I sampled the difficulty on some random but evenly spaced points in two intervals: 20.6.25-15.7.25, and 15.7.25-10.8.25, and for each data set I computed the regression line to understand the trend. With an average of 25 blocks per sample (or about 40 semples/day), we get a very clear picture:&#x20;

<figure><img src="../.gitbook/assets/image (2) (1).png" alt=""><figcaption></figcaption></figure>

ever since selfish mining started, there has been a _constant_ _increase_ in perceived hashrate. While it's a bit hard to see in the picture, the increase is about 0.01 GH/s (or about 0.001%) per day, which amounts to nothing.

This provides more solid evidence that Qubic's endeavor did not cause a significant shift in the global hashrate, only in its noisiness. However, this _does_ mean that Qubic had to bring in at least _some_ of their own hashrate.

Why? Simple: if they just caused existing miners to start selfish mining, the perceived hashrate would _drop_. Yet, we see neither a drop nor a downward trend. This discrepancy _cannot_ be explained in terms of noise alone, as we have a very large window size and sample density (I tried to add error bars, but they were too small to plot). This brings me to my second conclusion: it is highly likely that Qubic increased the _actual_ (not _perceived_) Monero hashrate by around 5%.

Now, it could be more than that actually: if switch miners abandoned Monero mining due to the increased hashrate/fluctuations/price drops, then Qubic filled the gaps. But even under the strict assumption that no Monero miner switched to another coin (though _some_ had to switch to mining through qubic), this discrepancy can only be explained with a new hashing source that was not mining Monero before.

Given that Monero is _that much_ larger than Qubic, I would say that it is at least _somewhat_ of a feat.

## Verdict

Given the data and analysis above, I can say with confidence that Qubic managed to obtain at least 28% of the current Monero hashrate. This is congruent with the 35% _perceived_ hashrate, as well as the known bounds for Eyal-Sirer.

Of the hashrate used by Qubic for selfish mining, at least 5% came from new sources of hash and not migrating Monero miners.

It is _implausible_ that Qubic managed to obtain a majority of the actual hashrate, as applying Eyal-Sirer with a majority miner reduces to an indefinitely long double-spending attack.

The probability of creating a six-block-deep reorg with 28% of the hashrate applying Eyal-Sirer is about 0.3% (using the "random walk approximation" $$\left(\frac{\alpha}{1-\alpha}\right)^C$$ with $$\alpha=0.28$$ and $$C=6$$), which is congruent with the fact that only one such occurrence was observed. However, this should be taken _very_ lightly, as the standard deviation of this process is about the same magnitude as the sample window we have: a couple of weeks. However, that we've seen it _once_ but not _a lot_ means that it is _plausibly_ in the right ballpark.

## Interpretation and Conclusion

It does not matter at all that Qubic most likely didn't manage to get 51%. Hyperfocusing on whether they have is a distraction. The elephant in the room is not what this means for Qubic, but what this means for Monero.

Monero brands itself as a provider of military grade security, suited for sensitive, high-profile applications. They aspire to become part of the global economic infrastructure designed to provide reliability and robustness. Having been disrupted to such a thorough extent by an overall niche movement should considerably undermine their ability to do so. They maybe didn't succeed this time, but they definitely showed that it is possible, and I believe that they can get there if they choose to persist (though I am not sure what that would accomplish).

But what is the point of failure? To me, it is obvious, and I have been warning about this for years, so I find the vindication provided by Qubic pleasant. The answer is, of course, _ASIC resistance_.

I have advocated for ASIC friendliness in the trenches, originally to justify Kaspa's choice of mining algorithm, but eventually as a cause of its own. Yes, ASIC friendliness has its problems, and creative solutions (ehm ehm rapid emissions and insane block rates) are required to ensure good coin spread. But anything other than ASIC friendliness is _a security vulnerability_. That was the weak point that allowed a relatively small movement to bring a giant like Monero down on its knees.

Some argue that this has nothing to do with generic hardware, and the "attack" boils down to enticing a collusion of selfish miners, but that is not quite the case. The attack was made feasible by the availability of switch miners, which resulted from the absurdity of relying on _generic_ hardware for _scarcity_.

As Dr. K pointed out in a [Quai space](https://x.com/QuaiNetwork/status/1956023043580448982) that was primarily dedicated to Qubic's attack, the scarcity of ASICs is not obvious, and should be researched, examined, and not taken for granted. However, I replied that while that is true, the _superfluity_ of ASICs is not something to be taken for granted either, and that's just not something you can say about generic hardware. It is almost the dictionary definition of generic.

Some may argue that Qubic's raid is unethical, but I beg to differ. The way I see it, crypto is in its formative stage, and we owe a debt of gratitude to anyone who stress tests claims. As long as Qubic did not abuse their dominance for a double-spend, as long as they give due notice about their raids, I see this as essential. I am not claiming they are being altruistic. I am claiming you should not expect _anyone_ to be. And if they managed to cheat the system (not _other users_ of the system, but _the system itself_), then the system is broken.

Hate the game, not the player.

[X thread for comments, discussion, and questions](https://x.com/DesheShai/status/1956400476888412257)
