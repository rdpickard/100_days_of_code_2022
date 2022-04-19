package main

import (
	"math/rand"
	"os"
	"strconv"
)

func main() {

	f, err := os.Create("./local/random_ints.txt")
	if err != nil {
		panic(err)
	}

	for i := 0; i < 10_000_000; i++ {
		_, err := f.WriteString(strconv.FormatInt(int64(rand.Int31()), 10) + "\n")
		if err != nil {
			break
		}
	}
}
