package main

import (
	"bufio"
	"fmt"
	"log"
	"math/big"
	"os"
	"strconv"
	"time"
)

func main() {

	var bits big.Int

	file, err := os.Open("./local/random_ints.txt")
	if err != nil {
		log.Fatal(err)
	}

	defer file.Close()

	start := time.Now()

	i := 0
	scanner := bufio.NewScanner(file)
	max_val := 0
	c_val := 0
	// optionally, resize scanner's capacity for lines over 64K, see next example
	for scanner.Scan() {
		//fmt.Println(scanner.Text())
		scanner.Text()
		c_val, _ = strconv.Atoi(scanner.Text())
		//fmt.Printf("%d\n", c_val)
		bits.SetBit(&bits, c_val, 1)
		if c_val > max_val {
			max_val = c_val
		}
		i += 1
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	time_end := time.Now()

	elapsed := time_end.Sub(start).Nanoseconds()

	fmt.Printf("%d linse in %d ns with  max check with bitset\n", i, elapsed)
	fmt.Printf("%d max val\n", max_val)

}
