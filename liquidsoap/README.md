# Liquidsoap environment

## Install

First, we need to install Liquidsoap v.1.3.3 (or more recent), which unfortunately is not packaged for Debian/Ubuntu anymore.
Download it from Liquidsoap's (Github releases page)[https://github.com/savonet/liquidsoap/releases].

Make sure you have installed all the dependencies, then :
```bash
cp PACKAGES.default PACKAGES
./configure
./make
./make install
```
