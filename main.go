package main

import (
	"fmt"
	"math/big"
	"time"
)

const p = 1099511627791

const logN1 = 20
const numChallengeBits = 1 << logN1
const N1 = numChallengeBits - logN1
// math.ceil(math.log2(p) * 2))
const checkLen = 81

var legendreEvals uint64 = 0

// logN1 bits number
type Num uint64

// jacobi (-1 -> false, 0 -> false, 1 -> true)
func jacobiBitMpz(a Num, n Num) bool {
	legendreEvals++
	//assert(n > a > 0 and n%2 == 1)
	t := true
	for a != 0 {
		for a%2 == 0 {
			a /= 2
			if r := n % 8; r == 3 || r == 5 {
				t = !t
			}
		}
		a, n = n, a
		if a%4 == 3 && n%4 == 3 {
			t = !t
		}
		a %= n
	}
	if n == 1 {
		return t
	} else {
		return false
	}
}

func bitstringToInt(bits [logN1]bool) (out Num) {
	for i := uint8(0); i < logN1; i++ {
		if bits[i] {
			out |= 1 << i
		}
	}
	return
}

func computeSubsequence(keyStart Num) (out Num) {
	for i := uint8(0); i < logN1; i++ {
		if jacobiBitMpz(keyStart + Num(i), p) {
			out |= 1 << i
		}
	}
	return
}

// Solve challenge using Khovratovich algorithm
func main() {
	// Create challenge
	// key = 3**1000 % p
	key := Num(new(big.Int).Exp(
		new(big.Int).SetUint64(3),
		new(big.Int).SetUint64(1000),
		new(big.Int).SetUint64(p)).Uint64())
	challenge := make([]bool, numChallengeBits, numChallengeBits)
	for i := Num(0); i < numChallengeBits; i++ {
		challenge[i] = jacobiBitMpz(key + i, p)
	}

	// count pre-computation time too, like python code
	start := time.Now()

	cdict := make(map[Num][]Num)
	v := [logN1]bool{}
	for i := Num(0); i < N1; i++ {
		copy(v[:], challenge[i:i+logN1])
		c := bitstringToInt(v)
		cdict[c] = append(cdict[c], i)
	}

	fpCount := uint64(0)

	findMatch := func() Num {
		currentKey := Num(0)
		expectedN2 := p / N1 / 2
		numberOfTries := uint64(0)
		for {
			numberOfTries++
			if numberOfTries%100000 == 0 {
				fmt.Printf("Tried %d keys (expected = %d)\n", numberOfTries, expectedN2)
			}
			currentKey = (currentKey + N1) % p
			c := computeSubsequence(currentKey)
			if offsets, ok := cdict[c]; ok {
				offsetLoop: for _, keyOffset := range offsets {
					predictedKey := currentKey - keyOffset
					for x := Num(0); x < checkLen; x++ {
						if jacobiBitMpz(predictedKey+x, p) != challenge[x] {
							fpCount++
							continue offsetLoop
						}
					}
					return predictedKey
				}
			}
		}
	}

	legendreEvals = 0
	res := findMatch()
	if res != key {
		panic("found unexpected key")
	}
	end := time.Now()
	fmt.Printf("False positive count %d\n", fpCount)
	fmt.Printf("Time taken: %s\n", end.Sub(start).String())
	fmt.Printf("Total Legendre evaluations: %d\n", legendreEvals)
}
