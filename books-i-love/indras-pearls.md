---
description: >-
  A mathematical, historical, personal, programmatic, aesthetic, and ultimately
  spiritual journey through the patterns emerging on crystal balls
---

# Indra's Pearls

<figure><img src="../.gitbook/assets/image (21).png" alt="" width="375"><figcaption></figcaption></figure>

_Indra's Pearls_ is a story of profound mathematical insights, discovered through a computer-navigated exploration of an impossibly complex terrain.

This is not just a visual demonstration of the pretty symmetries afforded by math. It is a _detective story_ of piecing together a coherent picture by following breadcrumb trails guided by the intricacies revealed by computerized plotting, in an era when computation was an expensive and very limited resource.

Most charmingly, it tells the story from the perspective of researchers who led that very research. This is not a retroactive historical reconstruction of what _might_ have transpired, but the direct accounts of those who were in the trenches of 1980s computer labs, carefully crafting efficient code and patiently waiting for hours, even days, to see if meaningful patterns emerge. (The first author, David Mumford, is a 1974 Fields Medalist. He was the "responsible adult", while the other two authors were young, bright, upcoming researchers privileged with his tutelage.) Isma's Pearls has an air of authenticity about it that is impossible to recreate.

Beyond its authenticity, Indra's Pearls provides a web of threads that are almost as interwoven as the fractals it exhibits. It freely hops between no less than _five_ accounts: The "prehistory" of the field and the classical results that served as the starting point for the authors' research. The mathematical insights and ideas, exposed by the writers  and their collaborators, that drove the research further. Personal accounts of the writers' experiences conducting this research. A hands-on guide through the programmatic aspects, focusing on the computational challenges forced on the authors and the original solutions they came up with, explained in enough detail for the studious reader to replicate. And last but not least, a whole lot of pretty pictures that make this book coffee-table worthy.

You'd expect that consistently hopping between approaches and topics might make the book feel a bit schizophrenic (strong flashbacks to Gödel, Escher Bach here), but it doesn't. It feels _seamless_. At times, as infuriatingly effortless as Mozart's music. The authors' natural ability to cohesively glue such disparate aspects smells like _experience_. These are the aspects that comprise _actual research_. And yet, the authors' ability to recount their story in such a relatable way is nothing short of marvelous.

## Alan Watt's Hyperbole

> \[This is] the highest> &#x20;doctrine of Mahayana Buddhism, which you could call the doctrine of the mutual> &#x20;interpenetration \[or] interdependence of all things, and> &#x20;its symbol is the what is called _Indra's> &#x20;net_.
>
> \
> \[...]
>
>> \
> Imagine, at dawn, a multi-dimensional> &#x20;spider's web \[...] covered with> &#x20;jewels of dew, all of which have rainbow> &#x20;coloring, and every drop of dew> &#x20;contains in it the reflection of every> &#x20;other drop of dew. And since every drop> &#x20;of dew contains the reflections of all> &#x20;the others,> &#x20;each reflected drop of dew contains the> &#x20;reflections you see of all the others

The quote above is from an [old recording](https://www.youtube.com/watch?v=DoVPZjfcHFQ) of the great thinker and self-styled philosopher Alan Watts. I couldn't have been older than fifteen when I first heard it, and yet, it left a deep impression. Not because of the mathematical epiphanies that, in hindsight, it resonates so well. (My career focus at the time was being a pothead high school dropout, leaving little time to develop my capacity for the abstract.) It was the idea that everything affects everything else to the extent that every single thing, in the marks etched on it by existence, carries the entire universe upon it. (In retrospect, it is almost as if Indra himself was trying to teach us that "a meromorphic function carries its entire structure in any infinite discrete set").

In the century or so preceding Watt's prominence, a succession of great thinkers noticed a curious type of geometry, which they called _hyperbolic geometry_. Hyperbolic geometry might be a bit hard to swallow for those not accustomed to this kind of visual exploration. It is a two-dimensional geometry, in the sense that it can be drawn on a piece of paper, but it is _not flat_, in the sense that what seems like "straight lines" to those who live inside the geometry does not _appear_ straight to an external viewer. (Not unlike how the straight line that bisects a standard map of the earth, the one that we call "the equator",  is actually a circle.)

A mathematical study of the hyperbolic geometry reveals phenomena that our paper will find difficult to absorb: triangles with less than 180 degrees, distinct lines with an angle of zero degrees between them, and — to Euclid's dismay — for each line L and point p not on L, _infinitely many_ that go through p without ever meeting L. (Euclid's fifth postulate asserts that for any line L and any point p not on L, there is _exactly one_ line that goes through p and never meets L. We call it "_the_ through p parallel to L", and hyperbolic geometry shows one way it can fail. The other way it could fail is exhibited by _spherical geometry_, where triangles have _more_ than 180 degrees, and _any two straight lines meet_.)&#x20;

We can draw a _twisted_ version of the geometry on our Euclidean page. This just means that what looks like a straight line to an ant living within the geometry will generally not look like a straight line, and vice versa. (Not unlike how we consider longitude lines as straight lines, yet on a map, they appear curved. Worse yet! Even though all such lines are similar in reality, on the map, they become curvier as they are farther from the center! Clearly, had we chosen a different center, the longitudinal lines would have curved differently. This emphasizes how this curviness is not in the longitude lines themselves, but a consequence of the arbitrary inaccuracies we chose when we tried to fit the curvy surface of Earth onto a flat piece of paper.)

While this twisted version can deceive us as to what is considered a straight line (and consequently, when  shapes are congruent), there are ways to draw it that are highly effective in exposing the properties of this geometry. One nice way to do it is a nice model called the [_Poincaré disk_](https://en.wikipedia.org/wiki/Poincar%C3%A9_disk_model) (_not_ named after its inventor [Eugonio Beltrami](https://en.wikipedia.org/wiki/Eugenio_Beltrami), as is often the way in math).&#x20;

The Poincaré disk model is very simple. First, draw a circle:

<figure><img src="../.gitbook/assets/image (7) (1).png" alt=""><figcaption></figcaption></figure>

The points of our geometry are those _inside_ the circle, but _not_ the points _along_ the circle. This is what we call an _open disc_. The lines along the circle are called its _boundary_, and they somewhat correspond to a "circle at infinity". (More accurately, all the boundary points represent a single "point at infinity". By pressing all of the boundary points into a single point, the disc becomes the Riemann Sphere.)

Our next task is to understand what curves in our map correspond to straight lines in the actual hyperbolic geometry. Luckily, there's a recipe for that which requires _zero_ equations. Start with two points:

<figure><img src="../.gitbook/assets/image (8) (1).png" alt=""><figcaption></figcaption></figure>

The recipe for the hyperbolic line that passes through these points is to draw a unique circle with two properties: it passes through both points, and it intersects the boundary circle at right angles. (A moment's reflection reveals why, for  any two points, there is _exactly one_ such circle.)

The arc of the circle that resides inside the hyperbolic disk is the straight line we are looking for!

<figure><img src="../.gitbook/assets/image (9) (1).png" alt=""><figcaption></figcaption></figure>

Any curve drawn this way, regardless of the points we started with, is a hyperbolic line. Moreover, these are the _only_ hyperbolic lines. This correspondence furnishes a very nice visual characterization of hyperbolic lines. (With some reflection, we can convince ourselves that a hyperbolic line seems straight on our map if and only if it goes through the center of the disc.)

<figure><img src="../.gitbook/assets/image (10) (1).png" alt=""><figcaption></figcaption></figure>

Now that we know how to draw lines, we can draw polygons. And once we have polygons, we can use them to _tessellate_ the plane. This just means covering it up with identical shapes, like a chessboard. But when we try to do so, we find something weird: at each corner, _five_ squares meet. Perhaps a bit annoyed to find out that a hyperbolic chessboard can't be colored like a chessboard, we press on. The full tessellation will end up like this:

<figure><img src="../.gitbook/assets/image (11) (1).png" alt=""><figcaption><p>A square tessellation of the Poincare disc, created by <a href="https://www.researchgate.net/publication/353970526_Limitations_on_Realistic_Hyperbolic_Graph_Drawing">David Epstein</a></p></figcaption></figure>

Amazingly enough, all of the shapes above are _squares_. If you assumed a hyperbolic vantage, you'd see that _all_ edges in the drawing are _straight_ and of length _one-half_, and angles between edges that meet are always 72 degrees. This tesselation illuminates how the disk model distorts the actual hyperbolic geometry: shapes of equal size _appear_ smaller when they are farther from the center!

A somewhat more curious tessellation arises from using an equilateral zero-degree triangle. The result is arguably much more aesthetic:

<figure><img src="../.gitbook/assets/image (14).png" alt=""><figcaption><p>A tessellation of the Poincare disc with zero-degree triangles, taken from <a href="https://mathworld.wolfram.com/PoincareHyperbolicDisk.html">MathWorld</a></p></figcaption></figure>

Building on these ideas, one can create a wealth of beautifully intricate Tessellations. The aesthetics were not lost on artists of the time, such as M. C. Escher, who is possibly the reason all of this feels eerily familiar.



<p align="center"><img src="../.gitbook/assets/image (16).png" alt=""><img src="../.gitbook/assets/image (17).png" alt=""></p>

The pursuit to understand the symmetries of these weird new geometries soon led to a startling realization.

Now that we understand what the hyperbolic plane is, we can define a _symmetry_ of the hyperbolic plane as any transformation that maps hyperbolic lines to hyperbolic lines of the same length. A simple example of a symmetry is rotating the entire plane by any amount about its center. If we stop to think about it (or look it up), we can find satisfying ways to visualize other symmetries, such as shifting the entire hyperbolic plane, or rotating about a point not in the center. (When I say shifting, I mean that someone who lives in the hyperbolic world decided to move _everything_ one meter to the right. From outside, the hyperbolic plane was mapped into itself, so in our map, the corresponding change happens _inside_ the hyperbolic disc, which is _not the same_ as shifting the disc itself to the right. What we will see is shapes on the left side of the disc grow as they move right towards the center, while shapes on the right side of the disc squeeze as they move away from it. If you find this hard to visualize, imagine what would happen to a map of the earth if we "rotate" it by deciding that some arbitrary longitudinal line should become the central line.)

Shifting and rotating are symmetries that make perfect sense both in Euclidean and hyperbolic geometry. But there is another type of symmetry that we are well familiar with: reflection. We can draw any straight line, and think of it as a mirror. Replacing the right side of the line with the reflection on the left side of the mirror and vice versa will reflect the entire plane through this line.

This will also work in hyperbolic space: choose any hyperbolic line, and think of it as a mirror, and you will find that you can reflect through it just the same. However, the hyperbolic plane has other, "hidden" symmetries. Draw _any_ circle inside the hyperbolic disc. Note that this circle is _not_ a straight line in hyperbolic geometry: we already said that straight lines must meet the border at right angles, while the circle you drew does not meet the border at all! However, it turns out that reflecting about this circle as if it were a (hyperbolic) mirror _still_ produces a symmetry. This is a very unique property of hyperbolic geometry that endows it with a much richer symmetry than other geometries. Understanding the structure of this group of symmetries as a whole is the pretext of the research that led to this book.

So how do we explore it? One way is to take only two symmetries and see what other symmetries we can build with _these two symmetries_ _alone_. We are allowed to apply them as many times and in any order that we want. We are also allowed to apply them backwards: if one of the symmetries is a quarter rotation clockwise, then we are also allowed to apply a quarter rotation _counte&#x72;_&#x63;lockwise.

We can now take any point and start applying these two symmetries in all possible orders to see what happens to it. The point will dance around the disc in ways that are, generally, not very interesting. However, it turns out that there are ways to choose these two symmetries such that curious things happen: no matter what point we start from, and in what order we apply the symmetries (as long as we avoid applying the same symmetry back and forth consecutively, which does nothing anyway), the point will drift towards another point within the disc, we call such a destination point an attractor. There are many attractors, and the one that we land on depends on the starting point and the order in which we apply the symmetries. The set of all these attractors is called the _limit set_ of the two symmetries we used.

It turns out that the limit set of two given symmetries can hide striking beauty. We can choose the symmetries in such a way that the limit set is a perfect circle, or a more complicated nesting of circles, or unhinged wild curves that seem to collapse upon themselves in complicated patterns  that eventually fill the entire hyperbolic disc, or just half of it. Just like the recurring reflections of the same object on two of Indra's Pearls hide the entire complexity of existence.

<figure><img src="../.gitbook/assets/image (20).png" alt=""><figcaption><p>Limit sets can be as innocuous as a simple circle, or admit more inner symmetry like the drawing on the left, or go completely berserk like the drawing on the right. The only reason we can even see something on the right is the limited depth of the sketching algorithm. Left to its devices, it would have eventually colored the entire screen black. And let me tell you, this is <em>far</em> from being the craziest thing you'd find in this book.<br>(Sketches lifted from <a href="https://www.dumas.io/limset/">Emily Dumas' homepage</a>.)</p></figcaption></figure>

Indra's Pearls plot is set within the journey to classify all the limit sets imposed by pairs of symmetries. A journey that arguably started with Friedrich Schottky's research during the 1870s. Though it unavoidably calls back to relevant insights as early as ancient Greece. (Not surprisingly, Indra's Pearls has quite a lot to say about [Apollonian Circles](https://en.wikipedia.org/wiki/Apollonian_circles)!)

I am not aware that Alan Watts himself knew of the striking mathematical analogy between the powerful metaphor he found in the Aatamaska Sutra and the astute observations of great mathematicians of the 19th and early 20th centuries. But I like to believe that he didn't, as this would mean Watts' insights exemplify themselves by casting their reflection on yet another one of Indra's pearls.

## Not Art, Nature

A recurring experience I had with this book was gleefully accosting anyone who would listen with an illustration I found incredibly beautiful, only to receive a lukewarm response. "The shapes are cool," they would say, "but the composition and color choices are crude and amateurish." My wife described the cover art as "ugly". In a sense, it is. The green color palette is pretty hideous. The color gradients are flat. Honestly, it gives 1990s Microsoft Office clip art kind of vibe.

But that's not what I see when I look at this picture. What I see is layers of endless symmetry enticing me to trace them with my eyes. I see how every curvy line is the edge of a crystal ball, and on both sides of the ball are perfectly identical copies of the same picture (for the hyperbolic meaning of being identical). I see the infinite path of reflections that any element of this picture follows. I appreciate the challenge of finding, for any two triangles, the sequence of reflections that eventually maps one to the other.

This is exhibited more bluntly in many other diagrams in the book, for example, figure 8.7:

<figure><img src="../.gitbook/assets/image (23).png" alt=""><figcaption><p>Figure 8.7 from Indra's Pearls inexlicibly reminds me Mr Bungle's song <a href="https://www.youtube.com/watch?v=YLMVe2_a3xY">Dead Goon</a></p></figcaption></figure>

When I look at the picture, I see how a fundamental domain of a quasi-Fuchsian group tessellates the interior of its limit set. But without this mathematical context, people are more likely to notice neon bright colors composing what might pass as a particularly ugly circus-themed quilt.

Of course, this gap can be bridged by explaining the symmetries hidden within, endowing the picture with a profound sense of meaning. But why should I have to? Surely, the beauty of this intricate geometry should be _self-evident_? I refused to believe that one must read a thick book to appreciate the aesthetics of these diagrams.

Throughout reading, it dawned on me that I should not be presenting these diagrams as art. They aren't. Just like even the most beautiful tree you have seen was not crafted by any human visionary. The authors are not artists, nor do they attempt to be. They are _explorers and_ _cartographers_. Mapping the terra incognita of hyperbolic symmetries. The maps they draw, the pictures they take, were not _meant_ to be artistic. They were intended to be _informative_. All of the intricacies, the infinitely fine-grained complexity hidden between, are not an artist's impression, but an accurate snapshot of the wonders they found in the uncharted. Each and every render in this book is a direct consequence of running code that was not adjusted for aesthetics. The wonder lies in seeing the complexity of the geometry unravel from the simplicity of the code and the underlying mathematics.

It is like crossing the ocean for the first time to find a world of exotic life and vegetation the likes of which we have never seen before. Most people will admire the tree itself instead of pontificating on how aesthetically the branches interwine and what color palette the leaves _should_ have. And it is _this_ sense of wonder that should guide the appreciation of these diagrams. Those are the intricacies of the nature of hyperbolic symmetry in their raw, natural form. And that this raw form packs so much beauty, _even without_ an artist's touch framing them effectively, does not require any conscious _understanding_ of the structure to furnish blissful humility.

## A Book of Many Virtues

The deliberate hodge-podge of approaches that characterizes books written by the originators of their subject matter (especially those written for a wide audience) is a two-edged sword. But in this case, I think it could not have gone any better. Thanks to this diversity of styles, the book affords a diversity of applications.

For the casual reader, I would say that this book may sometimes be a bit terse (depending on the reader's mathematical maturity), but more often than not, it is fluent and enjoyable. While it is hard for me to assume the perspective of a reader with no mathematical training, I believe many of the ideas pass on a qualitative level, and can be read off the pictures even if you don't care to learn what an automorphism subgroup is. The amount of value that can be extracted really depends on how studious the reader chooses to be. I believe that any reader stubborn enough could successfully tackle all the ideas in the book. People looking for a less intense experience should be prepared to skim or skip some of the more exacting discussions.

For a mathematically trained reader, especially with some familiarity with hyperbolic plane geometry, there is not a single thing about this book that is not immensely enjoyable. A semi-trained reader, who is comfortable with linear algebra and some geometric notions, but has never heard of Möbius transformations or the Riemann sphere, will have to do a bit more work. Still, I am certain they will find said work highly gratifying.

For the codemonkeys, this book can be viewed as a lengthy, incremental, and satisfying coding challenge. The problems that arise when trying to draw fractals are often quite surprising, and the authors' algorithmic acumen is quite impressive. Didactically, each chapter is accompanied by "project" problems that guide the reader through coding tasks. Even highly experienced programmers will learn new techniques and ideas they have probably never seen put into code before. The writers constantly try to goad the reader into implementing the code by proclaiming in _many_ instances that "to truly appreciate the forming picture" one should code it and see it animate. Fortunately, previous readers have already [done this for us](https://www.youtube.com/results?search_query=indras+pearls). But imagine running a script barely 100 lines long to obtain results like this:

{% embed url="https://www.youtube.com/watch?v=AT0Z1pVWqmQ" %}

Oh mama!

Finally, can Indra's Pearls be a textbook? On its own, not so much. However, I believe it could be used if supplemented by some more formal materials. (For example, the [beautiful booklet](https://www.amazon.com/Fuchsian-Groups-Chicago-Lectures-Mathematics/dp/0226425835) about Fuchsian groups by Svetlana Katok, which I'm sure the authors of Indra's Pearls would have recommended if it weren't published three years later). The book offers rich theoretical and practical exercises, which can be used in home assignments. But I think its level of formality falls short of being a standalone textbook for an advanced undergraduate course.

## In Conclusion

Reading Indra's Pearls made me feel _elated_. It reconnected to the ambitious excitement that drew me to math in the first place. The deliberately naive discourse over topics of infinite depth reminded me how deeply emotional it once was to feel the dawning of a new level of understanding, particularly in mathematics.

I am sure anyone even slightly intrigued by these topics has something to learn from Indra's Pearls. Whether you are a curious reader looking for casual fun, a studious undergrad looking for a summer challenge, a seasoned mathematician looking for a peek into the mind of one of the greats, a historian tracing back the routes of fractals to centuries before Goa trance was invented, a programmer looking for a completely different challenge, an artist looking for new perspectives, an interior designer trying to breath some new life into the old tradition of coffee book tables, or none of the above, you _will_ find something in this book that you will cherish forever.

[**X thread for comments and discussion**](https://x.com/DesheShai/status/1968292443041759239)
