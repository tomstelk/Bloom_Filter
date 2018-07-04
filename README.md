# Bloom_Filter
Simple implementation of bloom filter
- BloomStruc has initilization method that allows user to provide initial data, Bloom parameters (M , K), a target False-Positive Rate and an expected dataset size.
- If user does not provide (M, K) these are calculated in order to hit the target FPR given expected data size
- BloomStruc can also add additional input data, which must be provided as a list
- BloomStruc calculates a theoretical FPR, that is update each time more data is added - and therefore as more data is added the theoretical FPR can be much larger than the target FPR
- BloomStruc uses pymmh3.hash function to hash input data - this function requires input to be a string
- BloomStruc creates multiple hash functions by using different hash seeds

Requirements:
pymmh3 - see https://github.com/wc-duck/pymmh3

To run test:
collections
scipy.stats
