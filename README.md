Directional Parity Encoder and Decoder
======================================

Encode a number in a reversible sequence of bits using only a single additional bit

    # directional_parity_encode 7 42  # <number of bits> <value to encode>
    0 1 0 0 1 0 1
    # directional_parity_decode 0 1 0 0 1 0 1
    42
    # directional_parity_decode 1 0 1 0 0 1 0 
    42

Background
----------

This project was borne of the [WNYC Cicada
Tracker](http://project.wnyc.org/cicadas).  During our hack events
we've been asked more than a few times "how does this work" and "can I
use this in my own project."  I hope this project answers both questions.   

Gradually the number of languages this library is implemented in will
grow.  Currently there is a pure python version and a set of command
line tools in the `python` subdirectory.  I hope to add versions for
more languages shortly.

Installation
============

These instructions are fo the python version.  

    pip install directional_parity

Or install the python version of the code base from this repository

    git clone 
    cd directional_parity/python
    python setup.py install

Usage
=====

To determine the largest number you can encode in a given number of bits:

    # directional_parity_encode 7
    71

To encode a number as a directional parity bit sequence:

    # directional_parity_encode 7 42
    0 1 0 0 1 0 1

To decode a bit stream

    # directional_parity_decode 0 1 0 0 1 0 1
    42

Notice that the order of bits does not matter, reversing the order gives the same results

    # directional_parity_decode 1 0 1 0 0 1 0 
    42


This project was originally designed to keep users of WNYC's cicada
tracker from worrying about the orientation of their device when
entering data.  We've also provided a decoder that allows you to read
your device without using the WNYC website:

    $ wnyc_cicada_decode_temp 0 1 1 1 1 1 0 1 1
    27.50C 81.50F


How Directional Parity works
============================

Directional Parity can encode any integer less than 2**(n-1) +
2**(n//2) within n bits.  Here are the steps taken to encode a number:

If your number is less than 2**(n-1) go to Part A, if it is larger
than 2**(n-1) but smaller than 2**(n-1) + 2**(n//2) go to Part B:

Part A
------

Turn your number into a list of "bits" where B[n] is the value of the
nth bit.  Order this sequence from left to right such that:

    B0 B1 B2 ... Bn-2

Now split your number into two and treat these values as separate
numbers so you have (for an 8 bit number):

    B0, B1, B2, B3
    B4, B5, B6, B7

Convert these back to numbers and compare them.  If the B0...B3 is
larger than B4...B7 write:

    B0, B1, B2, B3, 1, B7, B6, B5, B4

otherwise write:

    B0, B1, B2, B3, 0, B7, B6, B5, B4

Reversing B4-B7 is important, when reading the bits back we're unsure
of the orientation if reversed properly we can still tell if the
reconstituted nibbles don't match the center parity bit.

Part B 
------ 

Your number is a little bit large than 2**(n-1).  No
problem.  Subtract 2**(n-1) from your number.  Convert your number to
bits such that B0, B1, B2 represent the position of the binary digits.
B0 will is the least significant bit.

Write your number as follows:

    B0, B1, B2, B3, 1, B3, B2, B1, B0

B4 - B7 should be zero; if they aren't your number is out of range and
can't be encoded in the number of bits you've selected.


Motivation
==========

When we set out in mid February to design a thermometer for the Cicada
Tracker project we had two overwhelming requirements: That the design
be inexpensive, simple to build and simple to use, simple to source and fun. 

Our goal was to ensure that any interested listener would be able to
build a unit from in Radio Shack.  We started digging through
individual parts in Radio Shack's parts bins, but we quickly found
4that are local store didn't have everything we needed.  We walked down
the street to another Radio Shack in lower Manhattan we found some of
the parts we needed but noted other necessary parts were missing.  We
again walked to another Radio Shack (we're located in lower Manhattan,
there really are multiple Radio Shacks within a 15 minute walk) and
found yet another collection of different parts.

What we did find however is most Radio Shacks carried at least an
Arduino Uno and the same simple collection of parts.  The parts bin we
settled on for our "buy this" list did have a 50kilo Ohm NTC resistor,
piles of LEDs, but only one 7-segment display.

Our initial prototype encoded the temperature as a straight binary
number, which worked well for it would allowed us to encode all
expected temperatures in Fahrenheit within a 7 bit number.  Except we
ran into two problems.  First, it wasn't always obvious which way was
up on the finished design.  "Hey, can you try entering this into my
website" resulted in misorientation with almost chance probabilities.


To solve this problem I developed the directional parity algorithm
implemented in this code, but I felt unhappy about the precision I was
wasting.  The directional parity algorithm works in odd length bit
strings and is capable of encoding a little more than n-1 bits of
information.  It felt wrong to waste a bit, and the idea of encoding
half degrees Fahrenheit didn't sit well for another reason: me.
This is engineering, we should be using metric, right?

I sat down and considered how much precision I might require to give
my coworkers the impression that we're working in Fahrenheit even
when we are not.  With 9 bits using the directional parity algorithm
I can encode values between 0 and 271 inclusive.  I then considered
5the coldest ground temperature we're likely to encounter.  The northern
most realistic range of Brood II is New England; I myself am a Native
Vermonter and recall just two winters ago seeing -30 Fahrenheit on a
temperature gouger and I'm designing this in February, but the earliest
deployment is likely to be in the spring.

Rather arbitrarily I decided to make -20oC the coldest temperature the
thermometer can read, although admittedly the device I'm designing
might not be accurate at such a temperature.  The thermistor in the
Radio Shack kit, and the thermistor we've been supplying at our events
is a 50kOhm NTC resistor.  The temperature rises as it gets colder,
dramatically and enough that the resistance might be so high that the
Arduino will have trouble measuring the voltage from the resistor
network because the ADC itself will have a low enough resistance to
affect the value.  But that's okay, whether its -20 or -10 doesn't
matter very much when predicting when the ground will hit the 17.75
degrees Celsius required for Cicadas to hatch.

At the other end the highest realistic temperature we'd encounter is
not from the ground, but folks measuring their own body temperature
with the thermistor.  Time and time again at the Brooklyn Brewery
event folks would place the thermistor in their hands, so we had to
reach body temperature.

Its about 57 degrees from -20 to body temperature, so reporting in
quarter degrees Celsius using the 0-271 range offered by a 9 bit
directional parity value seems about optimal - we had a range from
-20oC to +47oC with enough precision that each degree Fahrenheit is
covered by at least one sample.

