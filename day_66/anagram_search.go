package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"regexp"
	"strings"
	"time"
)

func niaveSliceContainsString(s []string, str string) bool {
	for _, v := range s {
		if v == str {
			return true
		}
	}

	return false
}

func factorialOfN(n uint64) uint64 {
	var fn uint64
	var i uint64
	fn = 1
	for i = 0; i < n; i++ {
		fn *= n - i
	}
	return fn
}

func stringPermutationsPIntoPackedSlice(targetStringAsRune []rune,
	permutations *[]int,
	permutationsOffset *int,
	left int, right int) {

	if left == right {
		//fmt.Printf("offset is %d\n", (*permutationsOffset))
		for i := 0; i < len(targetStringAsRune); i++ {
			(*permutations)[(*permutationsOffset)+i] = int(targetStringAsRune[i])
		}
		(*permutationsOffset) += len(targetStringAsRune)
	} else {
		for i := left; i <= right; i++ {
			targetStringAsRune[left], targetStringAsRune[i] = targetStringAsRune[i], targetStringAsRune[left]
			stringPermutationsPIntoPackedSlice(targetStringAsRune, permutations, permutationsOffset, left+1, right)
			targetStringAsRune[left], targetStringAsRune[i] = targetStringAsRune[i], targetStringAsRune[left]
		}
	}

}

func stringPermutationsRunes(targetString string) []string {

	// Figure out how big the slice to keep permutations will be
	slen := len(targetString)
	var numberOfPermutations = factorialOfN(uint64(slen))
	var permutationsPackedSlice []int
	permutationsPackedSlice = make([]int, numberOfPermutations*uint64(slen))

	targetStringAsRune := []rune(targetString)

	packedSliceOffset := 0

	stringPermutationsPIntoPackedSlice(targetStringAsRune, &permutationsPackedSlice, &packedSliceOffset, 0, slen-1)

	packedSliceOffset = 0
	var permutationsAsString []string

	/**
	for i := 0; i < int(numberOfPermutations); i++ {
		derp := ""
		off := i * len(targetString)

		for k := 0; k < len(targetString); k++ {
			derp = derp + string(rune(permutationsPackedSlice[off+k]))
		}
		permutationsAsString = append(permutationsAsString, derp)
	}
	**/

	var baseRuneSlice []rune
	baseRuneSlice = make([]rune, slen, slen)
	for i := 0; i < int(numberOfPermutations); i++ {

		for k := 0; k < slen; k++ {
			baseRuneSlice[k] = rune(permutationsPackedSlice[(i*slen)+k])
		}
		permutationsAsString = append(permutationsAsString, string(baseRuneSlice))

	}

	return permutationsAsString

}

func stringPermutationsPreSlicePreAllocated(targetStringAsSlice []string, permutations []string, left int, right int) []string {
	if left == right {
		permutations = append(permutations, strings.Join(targetStringAsSlice, ""))
	} else {

		for i := left; i <= right; i++ {
			targetStringAsSlice[left], targetStringAsSlice[i] = targetStringAsSlice[i], targetStringAsSlice[left]
			permutations = stringPermutationsPreSlice(targetStringAsSlice, permutations, left+1, right)
			targetStringAsSlice[left], targetStringAsSlice[i] = targetStringAsSlice[i], targetStringAsSlice[left]
		}
	}
	return permutations
}

func stringPermutationsPreSlice(targetStringAsSlice []string, permutations []string, left int, right int) []string {
	if left == right {
		permutations = append(permutations, strings.Join(targetStringAsSlice, ""))
	} else {

		for i := left; i <= right; i++ {
			targetStringAsSlice[left], targetStringAsSlice[i] = targetStringAsSlice[i], targetStringAsSlice[left]
			permutations = stringPermutationsPreSlice(targetStringAsSlice, permutations, left+1, right)
			targetStringAsSlice[left], targetStringAsSlice[i] = targetStringAsSlice[i], targetStringAsSlice[left]
		}
	}
	return permutations
}

func stringPermutations(targetString string, permutations []string, left int, right int) []string {

	if left == right {
		permutations = append(permutations, targetString)
	} else {

		for i := left; i <= right; i++ {
			targetStringAsSlice := strings.Split(targetString, "")
			targetStringAsSlice[left], targetStringAsSlice[i] = targetStringAsSlice[i], targetStringAsSlice[left]
			permutations = stringPermutations(strings.Join(targetStringAsSlice[:], ""), permutations, left+1, right)
			targetStringAsSlice[left], targetStringAsSlice[i] = targetStringAsSlice[i], targetStringAsSlice[left]
		}
	}
	return permutations
}

func main() {

	isAllLowerCaseLetters := regexp.MustCompile(`^[a-z]+$`).MatchString

	file, err := os.Open("./day_66/words.txt")
	if err != nil {
		log.Fatal(err)
	}

	var sortedWordsList []string

	defer file.Close()

	start := time.Now()

	scanner := bufio.NewScanner(file)

	// optionally, resize scanner's capacity for lines over 64K, see next example
	for scanner.Scan() {
		cword := scanner.Text()
		if isAllLowerCaseLetters(cword) {
			sortedWordsList = append(sortedWordsList, cword)
		}
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	time_end := time.Now()

	elapsed := time_end.Sub(start).Nanoseconds()

	fmt.Printf(" %d ns to read %d words into slice\n", elapsed, len(sortedWordsList))

	start = time.Now()
	count := 0
	for _, word := range sortedWordsList {

		var numberOfPermutations = factorialOfN(uint64(len(word)))
		var wordPermutations []string
		fmt.Printf("\n%s -> %d\n", word, numberOfPermutations)

		//wordPermutations = stringPermutationsPreSlice(strings.Split(word, ""), wordPermutations, 0, len(word)-1)
		wordPermutations = stringPermutationsRunes(word)
		fmt.Printf("calculated wp %d expected %d\n", len(wordPermutations), numberOfPermutations)

		count += 1
		if count > 100 {
			fmt.Println("did %d\n", count)
			break
		}

	}

	time_end = time.Now()

	elapsed = time_end.Sub(start).Nanoseconds()

	fmt.Printf(" %d ns to calculate all permutations of all words in list\n", elapsed)

}
