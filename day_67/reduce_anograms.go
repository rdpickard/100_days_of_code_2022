package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"sort"
	"strings"
	"time"
)

func main() {

	file, err := os.Open("./day_66/words.txt")
	if err != nil {
		log.Fatal(err)
	}

	defer file.Close()

	start := time.Now()

	scanner := bufio.NewScanner(file)

	anogramsMap := make(map[string][]string)
	totalWordsReadCount := 0
	// optionally, resize scanner's capacity for lines over 64K, see next example
	for scanner.Scan() {
		cword := strings.ToLower(scanner.Text())
		cwordSortedLetters := strings.Split(cword, "")
		sort.Strings(cwordSortedLetters)
		cwordLetters := strings.Join(cwordSortedLetters, "")
		anogramsMap[cwordLetters] = append(anogramsMap[cwordLetters], cword)
		totalWordsReadCount += 1
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	time_end := time.Now()

	elapsed := time_end.Sub(start).Nanoseconds()

	fmt.Printf(" %d ns to read %d words into sorted map of size %d\n", elapsed, totalWordsReadCount, len(anogramsMap))

	for _, v := range anogramsMap {
		if len(v) < 2 {
			continue
		}
		fmt.Printf("%v\n", v)
	}
}
