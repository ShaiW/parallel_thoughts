---
description: >-
  A mathematical, historical, personal, programmatic, aesthetic, and ultimately
  spiritual journey through the patterns emerging on crystal balls
---

# Indra's Pearls

<figure><img src="../.gitbook/assets/image (21).png" alt="" width="375"><figcaption></figcaption></figure>

_Indra's Pearls_ tells a story of profound mathematical insights, discovered through a computer-navigated exploration of an impossibly complex terrain.

This is not just a visual demonstration of the pretty symmetries afforded by math. It is a _detective story_ of piecing together a coherent picture by following breadcrumb trails guided by the intricacies revealed by computerized plotting, in an era when computation was an expensive and very limited resource.

Most charmingly, the story is told from the perspective of some of the people who led that very research. This is not a retroactive historical reconstruction of what _might_ have transpired, but the direct accounts of those who were in the trenches of computational research in the 1980s. (The first author, David Mumford, is a 1974 Fields Medalist. He was the "responsible adult", while the other two authors were young, bright, upcoming researchers privileged with his tutelage.) This gives the book an air of authenticity that is impossible to recreate retroactively.

Beyond its authenticity, Indra's Pearls provides a web of threads that are almost as interwoven as the fractals it exhibits. This text freely hops between no less than _five_ accounts: The "prehistory" of the field and the classical results that served as the starting point for the authors' research. The mathematical insights and ideas that drove the development. Personal accounts of the writers' experiences conducting this research. A hands-on guide through the programmatic aspects, focusing on the computational challenges forced on the authors and the original solutions they came up with, explained in enough detail for the studious reader to replicate. And last but not least, a whole lot of pretty pictures that make this book coffee-table worthy.

You'd expect that consistently hopping between approaches and topics might make the book feel a bit schizophrenic (strong flashbacks to Gödel, Escher Bach here), but it doesn't. It feels _seamless_. At times, as infuriatingly effortless as Mozart's music. The natural ability to cohesively glue such disparate aspects feels like it simply stems from _experience_. These are just the aspects that comprised the _actual research_. And yet, the authors' ability to recount their story in such a relatable way is nothing short of marvelous.

## Alan Watt's Hyperbole

> \[This is] the highest> &#x20;doctrine of Mahayana Buddhism, which you could call the doctrine of the mutual> &#x20;interpenetration \[or] interdependence of all things, and> &#x20;its symbol is the what is called _Indra's> &#x20;net_.
>
> \
> \[...]
>
>> \
> Imagine, at dawn, a multi-dimensional> &#x20;spider's web \[...] covered with> &#x20;jewels of dew, all of which have rainbow> &#x20;coloring, and every drop of dew> &#x20;contains in it the reflection of every> &#x20;other drop of dew. And since every drop> &#x20;of dew contains the reflections of all> &#x20;the others,> &#x20;each reflected drop of dew contains the> &#x20;reflections you see of all the others

The quote above is from an [old recording](https://www.youtube.com/watch?v=DoVPZjfcHFQ) of the great thinker and self-styled philosopher Alan Watts. I couldn't have been older than fifteen when I first heard it, and yet, it left a deep impression. Not because of the mathematical epiphanies that, in hindsight, it resonates so well. (My career focus at the time was being a pothead high school dropout, leaving little time for developing my capacity for the abstract.) It was the idea that everything affects everything else to the extent that every single thing, in the marks etched on it by existence, carries the entire universe upon it. (In retrospect, it is almost as if Indra himself was just trying to teach us that "a meromorphic function carries its entire structure into any infinite discrete set").

In the century or so preceding Watt's prominence, a succession of great thinkers had noticed a curious type of geometry called _hyperbolic geometry_. The hyperbolic geometry might be a bit hard to swallow for those not used to this kind of stuff. It is a two-dimensional geometry, in the sense that it can be drawn on a piece of paper, but it is _not flat_, in the sense that what seems like "straight lines" to those who live inside the geometry does not _appear_ straight to an external viewer. (This is very similar to how we Earth residents feel comfortable with treating the equator as a straight line, whereas to our neighbours on Mars, it is clearly a circle.)

A mathematical study of the hyperbolic geometry reveals phenomena that our paper will find difficult to absorb: triangles with less than 180 degrees, distinct lines with zero degrees between them and — to Euclid's dismay — for each line L and point p not on L, one can find _infinitely many_ lines parallel to L that go through p.

If we are careful to remember that our drawings are a twisted version of the geometry, where we are forced to draw "curvy straight lines", they can actually tell us quite a lot. One nice way to do it is a nice model called the [_Poincaré disk_](https://en.wikipedia.org/wiki/Poincar%C3%A9_disk_model) (though it is commonly credited to [Eugonio Beltrami](https://en.wikipedia.org/wiki/Eugenio_Beltrami), as is often the way in math).&#x20;

The Poincaré disk model is very simple.

First, draw a circle:

<figure><img src="../.gitbook/assets/image (7).png" alt=""><figcaption></figcaption></figure>

The points of our geometry are those _inside_ the circle, but _not_ the points _along_ the circle. This is what we call an _open disc_. The lines along the circle are called its _boundary_, and they somewhat correspond to a "circle at infinity"  (or more accurately, they all represent the same unique "point at infinity"). Now, let us mark two arbitrary points on the hyperbolic disk:

<figure><img src="../.gitbook/assets/image (8).png" alt=""><figcaption></figcaption></figure>

We want to draw the "hyperbolic straight line" that goes through these two points. The recipe for doing this is to find a circle with two properties: it goes through both points, and it meets the boundary circle at right angles. A moment's reflection reveals that any two points define _exactly one_ circle with this property.

The arc of the circle that resides inside the hyperbolic disk are the straight line we are looking for.

<figure><img src="../.gitbook/assets/image (9).png" alt=""><figcaption></figcaption></figure>

More generally, the straight lines of the hyperbolic plane appear in the unit disc as circle arcs that meet the boundary at right angles. There are many such lines, and those that meet the center of the disk are precisely those that also happen to be straight in our drawing!

<figure><img src="../.gitbook/assets/image (10).png" alt=""><figcaption></figcaption></figure>

To better understand this eerie geometry, we can _tessellate it_. Just like we can cover the ordinary plane with identical squares, we can also do it with the hyperbolic disc. The result will be something like this:

<figure><img src="../.gitbook/assets/image (11).png" alt=""><figcaption><p>A square tessellation of the Poincare disc, created by <a href="https://www.researchgate.net/publication/353970526_Limitations_on_Realistic_Hyperbolic_Graph_Drawing">David Epstein</a></p></figcaption></figure>

Amazingly enough, all of the above squares are _congruent_. Not only do they have the same area, but the exact same shape! This illuminates how the disk model distorts the actual hyperbolic geometry: shapes of equal size _appear_ smaller when they are farther from the center!

A more interesting way to do so is to start with a _zero-degree triangle_, a triangle whose sides only meet on the boundary at infinity. The result is arguably much more aesthetic:

<figure><img src="../.gitbook/assets/image (14).png" alt=""><figcaption><p>A tessellation of the Poincare disc with zero-degree triangles, taken from <a href="https://mathworld.wolfram.com/PoincareHyperbolicDisk.html">MathWorld</a></p></figcaption></figure>

Building on these ideas, one can create a wealth of beautifully intricate Tessellations. The aesthetics was not lost on artists of the time, such as M. C. Escher, who is possibly the reason all of this feels oddly familiar.



<p align="center"><img src="../.gitbook/assets/image (16).png" alt=""><img src="../.gitbook/assets/image (17).png" alt=""></p>

The pursuit to understand the symmetries of these weird new geometries soon led to a startling realization. Imagine we only take _two_ such symmetrical moves. Now, I know that's hard to imagine, since _what these symmetries might look like_ is far from obvious, but bear with me. The point is that we take these two symmetry-preserving moves, and now we repeat them many times, in whatever order we want. We also allow ourselves to apply these symmetries _backwards_ (e.g., if one of the symmetries is a quarter turn clockwise, then we are also allowed to apply quarter turns counterclockwise). We can now start with a _single point_ on the plane, and trace how it jitters around as we use more and more symmetries.

In many cases, this is not a particularly interesting experiment. But it turns out that if we choose the symmetries _just right_, something miraculous happens: for some of the possible starting points, and some of the possible sequences of applying our symmetries, we will find that the starting point does not escape to infinity, or repeats itself in an infinite pattern, but it is instead _attracted_ to a particular position on the hyperbolic plane. Such positions are called _attractors_, and it turns out that the set of all attractors of two given symmetries can hide striking beauty. Just like the recurring reflections of the same object on two of Indra's Pearls can hide the entire complexity of existence. It can be as simple as a circle, or complex enough that, despite being a curvy line, it fills the entire hyperbolic plane!

<figure><img src="../.gitbook/assets/image (20).png" alt=""><figcaption><p>Limit sets can be as innocuous as a simple circle, or admit more inner symmetry like the drawing on the left, or go completely berserk like the drawing on the right. The only reason we can even see something on the right is the limited depth of the sketching algorithm. Left to its devices, it would have eventually colored the entire screen black. And let me tell you, this is <em>far</em> from being the craziest thing you'd find in this book.<br>(Sketches lifted from <a href="https://www.dumas.io/limset/">Emily Dumas' homepage</a>.)</p></figcaption></figure>

Indra's Pearls is the story of the journey to discover and classify these symmetries. It is reasonable to declare Friedrich Schottky's research during the 1870s as the starting point of this journey. Though it unavoidably calls back to relevant insights as early as ancient Greece. (Not surprisingly, Indra's Pearls has quite a lot to say about [Apollonian Circles](https://en.wikipedia.org/wiki/Apollonian_circles)!)

I am not aware that Alan Watts himself was aware of the striking mathematical analogy between the powerful metaphor he found in the Aatamaska Sutra and the astute observations of great mathematicians of the 19th and early 20th centuries, such as Bernhard Riemman, Friedrich Schottky, or Felix Klein. I like to believe that he didn't, as this renders him a striking example of his own insight (which are in themselves reflections of an ancient Buddhist metaphor), casting their reflection on yet another pearl.

## Not Art, Nature

A recurring experience I had with this book was gleefully accosting anyone who would listen with the pretty pictures, to receive a mixed response. "The shapes are cool," they would say, "but the composition and color choices are crude and amateurish." My wife described the cover art as "ugly," and in a sense, it is. The green color palette is pretty hideous. The color gradients are flat. Honestly, it gives 1990s Microsoft Office clip art kind of vibe.

But that's not what I see when I look at this picture. What I see is layers of endless symmetry enticing me to trace them with my eyes. I see how every curvy line is the edge of a crystal ball, and on both sides of the ball are perfectly identical copies of the same picture (for the hyperbolic meaning of being identical). I see the infinite path of reflections that any element of this picture follows. I appreciate the challenge of finding, for any two triangles, the sequence of reflections that eventually maps one to the other.

This is exhibited more bluntly in many other diagrams in the book, for example, figure 8.7 from the book.

<figure><img src="../.gitbook/assets/image (23).png" alt=""><figcaption><p>Figure 8.7 from Indra's Pearls inexlicibly reminds me Mr Bungle's song <a href="https://www.youtube.com/watch?v=YLMVe2_a3xY">Dead Goon</a></p></figcaption></figure>

When I look at the picture, I see how a fundamental domain of a quasi-Fuchsian group tessellates the interior of its limit set, but other people will first see neon bright colors composing what might pass as a particularly ugly circus-themed quilt.

Of course, this gap could be bridged by explaining the symmetries hidden within, endowing the picture with a profound sense of meaning. But why should I have to? Surely, the beauty of this intricate geometry should be _self-evident_? I refused to believe that one must read a thick book to appreciate the aesthetics of these diagrams.

At some point, it dawned on me that the analogy opening this review goes a long way. The authors are not artists, nor do they attempt to be. They are _cartographers_. Mapping the terra incognita of hyperbolic symmetries, and sending back the maps they drew. The maps were not _meant_ to be artistic. They were intended to be _informative_. All of the intricacies, the infinitely fine-grained complexity hidden between, are not an artist's impression, but an accurate snapshot of the wonders found in uncharted lands. Each and every render in this book is a direct consequence of running code that was not adjusted for aesthetics. The wonder lies in seeing the complexity of the geometry unravel from the simplicity of the code and the underlying mathematics.

It is like crossing the ocean for the first time to find a world of exotic life and vegetation the likes of which we have never seen before. Most people will admire the tree itself instead of pontificating on how aesthetically the branches interwine and what color palette the leaves _should_ have. And it is _this_ sense of wonder that should guide the appreciation of these diagrams. Those are the intricacies of the nature of hyperbolic symmetry in their raw, natural form. And that this raw form packs so much beauty _even without_ an artist present to frame it most effectively, does not require any conscious _understanding_ of the structure to furnish blissful humility.

## A Book of Many Virtues

The deliberate hodge-podge of approaches that characterizes books written by the originators of their subject matter (especially those written for a wide audience) is a two-edged sword. But in this case, I think it could not have gone any better. Thanks to this diversity of styles, the book affords a diversity of applications.

For casual reading, I would say that this book may sometimes be a bit terse (depending on the reader's mathematical maturity), but more often it is fluent and enjoyable. While it is hard for me to assume the perspective of a reader with no mathematical training, I believe many of the ideas pass on a qualitative level, and can be read off the pictures even if you don't care to learn what an automorphism subgroup is. The amount of value that can be extracted really depends on how studious the reader chooses to be. I believe that any reader stubborn enough could successfully tackle all the ideas in the book, but that people looking for a less intense experience should be prepared to skim or skip some of the more formal stuff.

For a mathematically trained reader, especially with some familiarity with hyperbolic plane geometry, there is not a single thing about this book that is not immensely enjoyable. A semi-trained reader, who is comfortable with linear algebra and some geometric notions, but has never heard of Möbius transformations or the Riemann sphere, will have to do a bit more work. Still, I am certain they will find said work highly gratifying.

For the codemonkeys, this book can be viewed as a lengthy, incremental, and satisfying coding challenge. The problems that arise when trying to draw fractals are often quite surprising, and the authors' algorithmic acumen is quite impressive. Even highly experienced programmers will learn new techniques and ideas they have probably never seen put into code before. The writers constantly try to goad the reader into implementing the code by proclaiming in _many_ instances that "to truly appreciate the forming picture" one should code it and see it animate. Fortunately, previous readers have already [done this for us](https://www.youtube.com/results?search_query=indras+pearls). But imagine running a script barely 100 lines long to obtain results like this:

{% embed url="https://www.youtube.com/watch?v=AT0Z1pVWqmQ" %}

Oh mama!

Finally, can this be a textbook? On its own, not so much. However, I believe it could be used if supplemented by some more formal materials. (For example, the [beautiful booklet](https://www.amazon.com/Fuchsian-Groups-Chicago-Lectures-Mathematics/dp/0226425835) about Fuchsian groups by Svetlana Katok, which I'm sure the authors of Indra's Pearls would have recommended if it weren't published three years later). The book offers rich exercises on both the theoretical and practical sides, which can be used in home assignments. But I think its level of formality just falls short of being a standalone textbook for an advanced undergraduate course.

## In Conclusion

Reading Indra's Pearls made me feel _elated_. It helped me reconnect with the kind of ambitious excitement that drew me to math in the first place. The deliberately naive discourse over topics of infinite depth reminded me of how deeply emotional it once was to reach new levels of understanding in anything, particularly in math.

I am sure anyone even slightly intrigued by these topics has something to learn from Indra's Pearls. Whether you are a curious reader looking for casual fun, a studious undergrad looking for a summer challenge, a seasoned mathematician looking for a peek into the mind of one of the greats, a historian tracing back the routes of fractals to centuries before Goa trance was invented, a programmer looking for a completely different challenge, an artist looking for new perspectives, or an interior designer trying to breath some new life into the old tradition of coffee book tables, or even none of the above, you _will_ find something in this book that you will cherish forever.

[**X thread for comments and discussion**](https://x.com/DesheShai/status/1968292443041759239)
