# Python `puid`

Simple, flexible and efficient generation of probably unique identifiers (`puid`, aka random strings) of intuitively specified entropy using pre-defined or custom characters (including Unicode).

```python
from puid import Chars, Puid

rand_id = Puid(chars=Chars.ALPHA, total=1e5, risk=1e12)
rand_id.generate()
'nWwiLXwdKsTcr'
```

## <a name="TOC"></a>TOC

- [Overview](#Overview)
  - [Usage](#Usage)
  - [Installation](#Installation)
  - [API](#API)
  - [Chars](#Chars)
- [Motivation](#Motivation)
  - [What is a random string?](#WhatIsARandomString)
  - [How random is a random string?](#RandomStringEntropy)
  - [Uniqueness](#Uniqueness)
  - [ID randomness](#IDRandomness)
  - [Efficiency](#Efficiency)
  - [Overkill and Under Specify](#Overkill)
- [Efficiencies](#Efficiencies)
- [tl;dr](#tl;dr)

## <a name="Overview"></a>Overview

`puid` provides intuitive and efficient generation of random IDs. For the purposes of `puid`, a random ID is considered a random string used in a context of uniqueness, that is, random IDs are a bunch of random strings that are hopefully unique.

Random string generation can be thought of as a _transformation_ of some random source of entropy into a string _representation_ of randomness. A general purpose random string library used for random IDs should therefore provide user specification for each of the following three key aspects:

1. **Entropy source**

   What source of randomness is being transformed?

   > `puid` allows easy specification of the function used for source randomness

2. **ID characters**

   What characters are used in the ID?

   > `puid` provides 19 pre-defined character sets, as well as allows custom characters, including Unicode

3. **ID randomness**

   What is the resulting “randomness” of the IDs?

   > `puid` allows an intuitive, explicit specification of ID randomness

[TOC](#TOC)

### <a name="Usage"></a>Usage

Creating a random ID generator using `puid` is a simple as:

```python
from puid import Puid

rand_id = Puid()
rand_id.generate()
'a78gWq7N51paZ2Hx5qkoK3'
```

**Entropy Source**

`puid` uses `secrets.token_bytes` as the default entropy source. The `entropy_source` option can be used to configure a specific entropy source:

```python
from puid import Puid
from random import getrandbits

def prng_bytes(n):
    return bytearray(getrandbits(8) for _ in range(n))

prng_id = Puid(entropy_source=prng_bytes)
prng_id.generate()
'JcQTr8u7MATncImOjO0qOS'
```

**ID Characters**

By default, `puid` use the [RFC 4648](https://tools.ietf.org/html/rfc4648#section-5) file system & URL safe characters. The `chars` option can by used to specify any of 16 [pre-defined character sets](#Chars) or custom characters, including Unicode:

```python
from puid import Chars, Puid

hex_id = Puid(chars=Chars.HEX)
hex_id.generate()
'a4b130ba638fc7db5d87e064a21e6b46'

dingosky_id = Puid(chars='dingosky')
dingosky_id.generate()
'sdosigokdsdygooggogdggisndkogonksnkodnokosg'

unicode_id = Puid(chars='dîñgø$kyDÎÑGØßK¥')
unicode_id.generate()
'îGÎØÎÑî¥gK¥Ñ¥kîDîyøøØñÑØyd¥¥ØGØÑ$KßØgøÑ'
```

**ID Randomness**

Generated IDs have 128-bit entropy by default. `puid` provides a simple, intuitive way to specify ID randomness by declaring a `total` number of possible IDs with a specified `risk` of a repeat in that many IDs:

To generate up to _10 million_ random IDs with _1 in a trillion_ chance of repeat:

```python
from puid import Chars, Puid

safe32_id = Puid(total=10e6, risk=1e15, chars=Chars.SAFE32)
safe32_id.generate()
'd7ntFnH4FngrqgdR3Dtt'
```

The `bits` option can be used to directly specify an amount of ID randomness:

```python
from puid import Chars, Puid

token = Puid(bits=256, chars=Chars.HEX_UPPER)
token.generate()
'5D241826F2A644E1B725DB1DD7E4BF742D9D0DC6D6A36F419046A02835A16B83'
```

[TOC](#TOC)

### <a name="Installation"></a>Installation

#### PyPi

```sh
pip install puid-py
```

#### Conda

```sh
conda install -c dingosky puid-py
```

[TOC](#TOC)

### <a name="API"></a>API

`puid` exports the class **Puid** which used to create random ID generators. **Puid** optionally takes arguments to configuration ID generation:

- `total`: Total number of potential (i.e. expected) IDs
- `risk`: Risk of repeat in `total` IDs
- `bits`: ID entropy bits
- `chars`: ID characters
- `entropy_source`: Function of the form `(n: number) => bytearray` for source entropy

##### Notes

- All config fields are optional
- `total/risk` must be set together
- `total/risk` and `bits` cannot both be set
- `chars` must be valid custom characters or pre-defined **Chars**
- `entropy_source` is a function of the form `(n: number) => bytearray`
- Defaults
  - `bits`: 128
  - `chars`: `Chars.SAFE64`
  - `entropy_source`: `secret.token_bytes`

#### PuidInfo

The **Puid**'s `__repr__` function provides information regarding the generator configuration:

- `bits`: ID entropy
- `bits_per_char`: Entropy bits per ID character
- `chars`: Source characters
- `entropy_source`: String `module.function`
- `ere`: Entropy representation efficiency
- `len`: ID string length

Example:

```python
from puid import Chars, Puid

rand_id = Puid(total=1e5, risk=1e14, chars=Chars.BASE32)
rand_id.generate()
'7XKJJKNZBF7GCMEX'

print(rand_id)
Puid: bits = 80.0, bits_per_char = 5.0, chars = BASE32 -> '234567ABCDEFGHIJKLMNOPQRSTUVWXYZ', len = 16, ere = 0.625, entropy_source = secrets.token_bytes
```

### <a name="Chars"></a>Chars

There are 19 pre-defined character sets:

| Name             | Characters                                                                                    |
| :--------------- | :-------------------------------------------------------------------------------------------- |
| ALPHA            | ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz                                          |
| ALPHA_LOWER      | abcdefghijklmnopqrstuvwxyz                                                                    |
| ALPHA_UPPER      | ABCDEFGHIJKLMNOPQRSTUVWXYZ                                                                    |
| ALPHANUM         | ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789                                |
| ALPHANUM_LOWER   | abcdefghijklmnopqrstuvwxyz0123456789                                                          |
| ALPHANUM_UPPER   | ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789                                                          |
| BASE16           | 0123456789ABCDEF                                                                              |
| BASE32           | ABCDEFGHIJKLMNOPQRSTUVWXYZ234567                                                              |
| BASE32_HEX       | 0123456789abcdefghijklmnopqrstuv                                                              |
| BASE32_HEX_UPPER | 0123456789ABCDEFGHIJKLMNOPQRSTUV                                                              |
| CROCKFORD32      | 0123456789ABCDEFGHJKMNPQRSTVWXYZ                                                              |
| DECIMAL          | 0123456789                                                                                    |
| HEX              | 0123456789abcdef                                                                              |
| HEX_UPPER        | 0123456789ABCDEF                                                                              |
| SAFE_ASCII       | !#$%&()\*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[]^\_abcdefghijklmnopqrstuvwxyz{\|}~ |
| SAFE32           | 2346789bdfghjmnpqrtBDFGHJLMNPQRT                                                              |
| SAFE64           | ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-\_                             |
| SYMBOL           | !#$%&()\*+,-./:;<=>?@[]^\_{\|}~                                                               |
| WORD_SAFE32      | 23456789CFGHJMPQRVWXcfghjmpqrvwx                                                              |

Any string of up to 256 unique characters can be used for **`puid`** generation.

#### Description of non-obvious character sets

| Name             | Description                                                |
| :--------------- | :--------------------------------------------------------- |
| BASE16           | https://datatracker.ietf.org/doc/html/rfc4648#section-8    |
| BASE32           | https://datatracker.ietf.org/doc/html/rfc4648#section-6    |
| BASE32_HEX       | Lowercase of Base32HexUpper                                |
| BASE32_HEX_UPPER | https://datatracker.ietf.org/doc/html/rfc4648#section-7    |
| CROCKFORD32      | https://www.crockford.com/base32.html                      |
| SAFE_ASCII       | Printable ascii that does not require escape in String     |
| SAFE32           | Alpha and numbers picked to reduce chance of English words |
| SAFE64           | https://datatracker.ietf.org/doc/html/rfc4648#section-5    |
| WORD_SAFE32      | Alpha and numbers picked to reduce chance of English words |

Note: SAFE32 and WORD_SAFE32 are two different strategies for the same goal.

[TOC](#TOC)

## <a name="Motivation"></a>Motivation

Developers frequently need random strings in applications ranging from long-term (e.g., data store keys) to short-term (e.g. DOM IDs on a web page). These IDs are, of course, of secondary concern. No one wants to think about them much, they just want to be easy to generate.

But developers _should_ think about the random strings they use. The generation of random IDs is a design choice, and just like any other design choice, that choice should be explicit in nature and based on a familiar with why such choices are made. Yet a cursory review of random string libraries, as well as random string usage in many applications, yields a lack of clarity that belies careful consideration.

[TOC](#TOC)

### <a name="WhatIsARandomString"></a>What is a random string?

Although this may seem to have an obvious answer, there is actually a key, often overlooked subtlety: a random string _is not random_ in and of itself. To understand this, we need to understand [_entropy_](<https://en.wikipedia.org/wiki/Entropy_(information_theory)>) as it relates to computers.

A somewhat simplistic statement for entropy from information theory is: _entropy is a measure of uncertainty in the possible outcomes of an event_. Given the base 2 system inherent in computers, this uncertainty naturally maps to a unit of bits (known as Shannon entropy). So we see statements like "_this random string has 128 bits of entropy_". But here is the subtlety:

> _**A random string does not have entropy**_

Rather, a random string represents _captured_ entropy, entropy that was produced by _some other_ process. For example, you cannot look at the hex string **`'18f6303a'`** and definitively say it has 32 bits of entropy. To see why, suppose you run the following code snippet and get **`'18f6303a'`**:

```python
from random import random

rand_id = lambda: '18f6303a' if random() < 0.5 else '1'
rand_id()
'18f6303a'
```

The entropy of the resulting string **`'18f6303a'`** is 1 bit. That's it; 1 bit. The same entropy as when the outcome **`'1'`** is observed. In either case, there are two equally possible outcomes and the resulting entropy is therefore 1 bit. It's important to have this clear understanding:

> _**Entropy is a measure in the uncertainty of an event, independent of the representation of that uncertainty**_

In information theory you would state the random process emits two symbols, **`18f6303a`** and **`1`**, and the outcome is equally likely to be either symbol. Hence there is 1 bit of entropy in the process. The symbols don't matter. It would be much more likely to see the symbols **`T`** and **`F`**, or **`0`** and **`1`**, or even **`ON`** and **`OFF`**, but regardless, the process _produces_ 1 bit of entropy and symbols used to _represent_ that entropy do not effect the entropy itself.

#### Entropy source

Random string generators need an external source of entropy and typically use a system resource for that entropy. In Python, this could be, for example, `secrets.token_bytes` or `random.getrandbits`. Nonetheless, it is important to appreciate that the properties of the generated random strings depend on the characteristics of the entropy source. Whether a random string is suitable for use as a secure token depends on the security characteristics of the entropy source, not on the string representation of the token.

#### ID characters

As noted, the characters (symbols) used for a random string do not determine the entropy. However, the number of unique characters available does. Under the assumption that each character is equally probable (which maximizes entropy) it is easy to show the entropy per character is a constant log<sub>2</sub>(N), where `N` is of the number of characters available.

#### ID randomness

String randomness is determined by the entropy per character times the number of characters in the string. The _quality_ of that randomness is directly tied to the quality of the entropy source. The _randomness_ depends on the number of available characters and the length of the string.

And finally we can state: a random string is a character representation of captured entropy.

[TOC](#TOC)

### <a name="Uniqueness"></a>Uniqueness

The goal of `puid` is to provide simple, intuitive random ID generation using random strings. As noted above, we can consider random string generation as the _transformation_ of system entropy into a character _representation_, and random IDs as being the use of such random strings to represent unique IDs. There is a catch though; a big catch:

> _**Random strings do not produce unique IDs**_

Recall that entropy is the measure of uncertainty in the possible outcomes of an event. It is critical that the uncertainty of each event is _independent_ of all prior events. This means two separate events _can_ produce the same result (i.e., the same ID); otherwise the process isn't random. You could, of course, compare each generated random string to all prior IDs and thereby achieve uniqueness. But some such post-processing must occur to ensure random IDs are truly unique.

Deterministic uniqueness checks, however, incur significant processing overhead and are rarely used. Instead, developers (knowingly?) relax the requirement that random IDs are truly, deterministically unique for a much lesser standard, one of probabilistic uniqueness. We "trust" that randomly generated IDs are unique by virtue of the chance of a repeated ID being very low.

And once again, we reach a point of subtlety. (And we thought random strings were easy!) The "trust" that randomly generated IDs are unique actually turns entropy as it's been discussed thus far on it's head. Instead of viewing entropy as a measure of uncertainty in the _generation_ of IDs, we consider entropy as a measure of the probability that no two IDs will be the same. To be sure, we want this probability to be very low, but for random strings it _cannot be zero_! And to be clear, _entropy is not such a measure_. Not directly anyway. Yes, the higher the entropy, the lower the probability, but it takes a bit of math to correlate the two in a proper manner. (Don't worry, `puid` takes care of this math for you).

Furthermore, the probable uniqueness of ID generation is always in some limited context. Consider IDs for a data store. You don't care if a generated ID is the same as an ID used in another data store in another application in another company in a galaxy far, far away. You care that the ID is (probably) unique within the context of your application.

To recap, random string generation does not produce unique IDs, but rather, IDs that are probably unique (within some context). That subtlety is important enough it's baked into the name of `puid`. And it is fully at odds with the naming of a version 4 `uuid`. Why? Because being generated via a random process means a `uuid` _cannot be unique_. As a corollary, it can't be universal either. As noted above, we don't care about the universal part anyway, but the fact remains, a `uuid` isn't **uu**.

[TOC](#TOC)

### <a name="IDRandomness"></a>ID randomness

So what does the statement "_these IDs have 122 bits of entropy_" actually mean? Entropy is a measure of uncertainty after all, and we're concerned that our IDs be unique, probably unique anyway. So what does "122 bits of entropy" mean for the probable uniqueness of IDs?

First, let's be clear what it _doesn't_ mean. We're concerned with uniqueness of a bunch of IDs in a certain context. The randomness of _any one_ of those ID isn't the real concern. Yes, we can say "_given 122 bits of entropy_" each ID has a probability of 2<sup>-122</sup> of occurring. And yes, that certainly makes the occurrence of any particular ID rare. But with respect to the uniqueness of IDs, it simply isn't "enough" to tell the whole story.

And here again we hit another subtlety. It turns out the question, as posed, is underspecified, i.e. it is not specific enough to be answered. To properly determine how entropy relates to the probable uniqueness of IDs, we need to specify _how many_ IDs are to be generated in a certain context. Only then can we determine the probability of generating unique IDs. So our question really needs to be: given **N** bits of entropy, what is the probability of uniqueness in **T** random IDs?

Fortunately, there is a mathematical correlation between entropy and the probability of uniqueness. This correlation is often explored via the [Birthday Paradox](https://en.wikipedia.org/wiki/Birthday_problem#Cast_as_a_collision_problem). Why paradox? Because the relationship, when cast as a problem of unique birthdays in some number of people, is initially quite surprising. But nonetheless, the relationship exists, it is well-known, and `puid` will take care of the math for us.

At this point we can now note that rather than say "_these IDs have **N** bits of entropy_", we actually want to say "_generating **T** of these IDs has a risk **R** of a repeat_". And fortunately, `puid` allows straightforward specification of that very statement for random ID generation. Using `puid`, you can easily specify "_I want **T** random IDs with a risk **R** of repeat_". `puid` will take care of using the correct entropy in efficiently generating the IDs.

[TOC](#TOC)

### <a name="Efficiency"></a>Efficiency

The efficiency of generating random IDs has no bearing on the statistical characteristics of the IDs themselves. But who doesn't care about efficiency? Unfortunately, most random string generation, it seems.

#### Entropy source

As previously stated, random ID generation is basically a _transformation_ of an entropy source into a character _representation_ of captured entropy. But the entropy of the source and the entropy of the captured ID _is not the same thing_.

To understand the difference, we'll investigate an example that is, surprisingly, quite common. Consider the following strategy for generating random strings: using a fixed list of **k** characters, use a random uniform integer **i**, `0 <= i < k`, as an index into the list to select a character. Repeat this **n** times, where **n** is the length of the desired string. In Python this might look like:

```python
from random import randint
import string

chars = string.ascii_lowercase
n_chars = len(chars)
common_id = lambda len: "".join([chars[randint(0,n_chars)] for _ in range(len)])
common_id(8)
# => 'wnplkyiz'
```

First, consider the amount of source entropy used in the code above. The Python spec declares `random.random()` (upon which `randint` depends) generates 53-bits of precision. So generating an 8 character ID above consumes 8 \* 53 = 424 bits of source entropy.

Second, consider how much entropy was captured by the ID. Given there are 26 characters, each character represents log<sub>2</sub>(26) = 4.7 bits of entropy. So each generated ID represents 8 \* 4.7 = 37.6 bits of entropy.

Hmmm. That means the ratio of ID entropy to source entropy is 37.6 / 424 = 0.09, or a whopping **9%**. That's not an efficiency most developers would be comfortable with. Granted, this is a particularly egregious example, but most random ID generation suffers such inefficient use of source entropy.

Without delving into the specifics (see the code?), `puid` employs various means to maximize the use of source entropy. As comparison, `puid` uses **87.5%** of source entropy in generating random IDs using lower case alpha characters. For character sets with counts equal a power of 2, `puid` uses 100% of source entropy.

#### Characters

As previous noted, the entropy of a random string is equal to the entropy per character times the length of the string. Using this value leads to an easy calculation of **entropy representation efficiency** (`ere`). We can define `ere` as the ratio of random string entropy to the number of bits required to represent the string. For example, the lower case alphabet has an entropy per character of 4.7, so an ID of length 8 using those characters has 37.6 bits of entropy. Since each lower case character requires 1 byte, this leads to an `ere` of 37.6 / 64 = 0.59, or 59%. Non-ascii characters, of course, occupy more than 1 byte. `puid` uses the utf-8 character encoding to compute `ere`.

<a name="UUIDCharacters"></a>

The total entropy of a string is the product of the entropy per character times the string length _only_ if each character in the final string is equally probable. This is always the case for `puid`, and is usually the case for other random string generators. There is, however, a notable exception: the version 4 string representation of a `uuid`. As defined in [RFC 4122, Section 4.4](https://tools.ietf.org/html/rfc4122#section-4.4), a v4 `uuid` uses a total of 32 hex and 4 hyphen characters. Although the hex characters can represent 4 bits of entropy each, 6 bits of the hex representation in a `uuid` are actually fixed, so there is only `32*4 - 6 = 122`-bits of entropy (not 128). The 4 fixed-position hyphen characters contribute zero entropy. So a 36 character `uuid` has an `ere` of `122 / (36*8) = 0.40`, or **40%**. Compare that to, say, the default `puid` generator, which has slightly higher entropy (132 bits) and yet yields an `ere` of 0.75, or **75%**. Who doesn't love efficiency?

[TOC](#TOC)

### <a name="Overkill"></a>Overkill and Under Specify

#### Overkill

Random string generation is plagued by overkill and under specified usage. Consider the all too frequent use of `uuid`s as random strings. The rational is seemingly that the probability of a repeated `uuid` is low. Yes, it is admittedly low, but is that sufficient reason to use a `uuid` without further thought? For example, suppose a `uuid` is used as a key in a data store that will have at most a thousand items. What is the probability of a repeated `uuid` in this case? It's 1 in a nonillion. That's 10^30, or 1 followed by 30 zeros, or million times the estimated number of stars in the universe. Really? Doesn't that seem a bit overkill? Do really you need that level of assurance? And if so, why stop there? Why not concatenate two `uuid`s and get an even more ridiculous level of "assurance".

Or why not be a bit more reasonable and think about the problem for a moment. Suppose you accept a 1 in 10^15 risk of repeat. That's still a _really_ low risk. Ah, but wait, to do that you can't use a `uuid`, because `uuid` generation isn't flexible. The characters are fixed, the representation is fixed, and the bits of entropy are fixed.

You could generate the IDs by determining the actual amount of ID entropy required (it's 68.76 bits), selecting some set of characters, calculate the string length necessary given those characters, and finally generate the IDs as outlined in the earlier common ID generation scheme.

Whew, maybe that's another reason developers tend to use uuids. That seems like a lot of effort.

Ah, but there is another way. You could very easily use `puid` to generate such IDs:

```python
from puid import Puid

db_id = Puid(total=1000, risk=1e15)
db_id.generate()
'tcDPzTAjoRcU'
```

The resulting IDs have 72 bits of entropy. But guess what? You don't care. What you care is having explicitly stated you expect to have 1000 IDs and your level of repeat risk is 1 in a quadrillion. It's right there in the code. And as added bonus, the IDs are only 12 characters long, not 36. Who doesn't like ease, control and efficiency?

#### Under specify

Another head-scratcher in schemes that generate random strings is using an API that explicitly declares string length. Why is this troubling? Because that declaration doesn't specify the actual amount of desired randomness, either needed or achieved. Suppose you are tasked with maintaining code that is using random IDs of 15 characters composed of digits and lower alpha characters. Why are the IDs 15 characters long? Without code comments, you have no idea. And without knowing how many IDs are expected, you can't determine the risk of a repeat, i.e., you can't even make a statement about how random the random IDs actually are! Was 15 chosen for a reason, or just because it made the IDs look good?

Now, suppose you are tasked to maintain this code:

```python
from puid import Chars, Puid
rand_id = Puid(total=500_000, risk=1e12, chars=Chars.ALPHANUM_LOWER)
```

Hmmm. Looks like there are 500,000 IDs expected and the repeat risk is 1 in a trillion. No guessing. The code is explicit. Oh, and by the way, the IDs are 15 characters long. But who cares? It's the ID randomness that matters, not the length.

[TOC](#TOC)

### <a name="Efficiencies"></a>Efficiencies

`Puid` employs a number of efficiencies for random ID generation:

- Only the number of bytes necessary to generate the next `puid` are fetched from the entropy source
- Each `puid` character is generated by slicing the minimum number of entropy bits possible
- Any left-over bits are carried forward and used in generating the next `puid`
- All characters are equally probable to maximize captured entropy
- Only characters that represent entropy are present in the final ID
- Easily specified `total/risk` ensures ID are only as long as actually necessary

[TOC](#TOC)

### <a name="tl;dr"></a>tl;dr

`puid` is a simple, flexible and efficient random ID generator:

- **Ease**

  Random ID generator specified in one line of code

- **Flexible**

  Full control over entropy source, ID characters and amount of ID randomness

- **Secure**

  Defaults to a secure source of entropy and at least 128 bits of ID entropy

- **Efficient**

  Maximum use of system entropy

- **Compact**

  ID strings represent maximum entropy for characters used

- **Explicit**

  Clear specification of ID generation

```python
from puid import Chars, Puid

rand_id = Puid(chars=Chars.SAFE32, total=10e6, risk=1e15)
rand_id.generate()
'RHR3DtnP9B3J748NdR87'
```

[TOC](#TOC)
