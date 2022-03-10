package main

import (
	"errors"
	"fmt"
	"io/ioutil"
	"os"
	"strings"
)

func MinInt(x, y int) int {
	if x > y {
		return y
	}
	return x
}

func MaxInt(x, y int) int {
	if x > y {
		return x
	}
	return y
}

func PrependFile(toAppendFileName string, fileByteLocation int, fromAppendFileName string) bool {
	// Create a swapfile
	swapFileName := toAppendFileName + ".SWAP"
	if _, err := os.Stat(swapFileName); err == nil {
		fmt.Printf("Swap file %s exists. Not appending\n", swapFileName)
		return false
	}
	if err := os.Rename(toAppendFileName, swapFileName); err != nil {
		fmt.Printf("Create swap file %s failed. Not appending\n", swapFileName)
		return false
	}

	swapfileBytes, err := ioutil.ReadFile(swapFileName)
	if err != nil {
		fmt.Printf("Could not read swapfile %s. Not appending\n", swapFileName)
		return false
	}

	fromFileBytes, err := ioutil.ReadFile(fromAppendFileName)
	if err != nil {
		fmt.Printf("Could not read from input file %s. Not appending\n", fromAppendFileName)
		return false
	}

	err = ioutil.WriteFile(toAppendFileName, fromFileBytes[:fileByteLocation], 0644)
	if err != nil {
		fmt.Printf("Write to  file %s failed. Appending failed in bad state\n", toAppendFileName)
		return false
	}

	f, err := os.OpenFile(toAppendFileName, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		fmt.Printf("Could not open file to append %s. Appending failed in bad state\n", toAppendFileName)
		return false
	}
	defer f.Close()
	if _, err := f.WriteString(string(swapfileBytes)); err != nil {
		fmt.Printf("Failed writing data file to append %s. Appending failed in bad state\n", toAppendFileName)
	}

	os.Remove(swapFileName)
	return true
}

func AppendFile(toAppendFileName string, fileByteLocation int, fromAppendFileName string) bool {

	// Create a swapfile
	swapFileName := toAppendFileName + ".SWAP"
	if _, err := os.Stat(swapFileName); err == nil {
		fmt.Printf("Swap file %s exists. Not appending\n", swapFileName)
		return false
	}
	if err := os.Rename(toAppendFileName, swapFileName); err != nil {
		fmt.Printf("Create swap file %s failed. Not appending\n", swapFileName)
		return false
	}

	swapfileBytes, err := ioutil.ReadFile(swapFileName)
	if err != nil {
		fmt.Printf("Could not read swapfile %s. Not appending\n", swapFileName)
		return false
	}

	err = ioutil.WriteFile(toAppendFileName, swapfileBytes, 0644)
	if err != nil {
		fmt.Printf("Write to swap file %s failed. Appending failed in bad state\n", swapFileName)
		return false
	}

	appendfileBytes, err := ioutil.ReadFile(fromAppendFileName)
	if err != nil {
		fmt.Printf("Could not from append file %s. Appending failed in bad state\n", fromAppendFileName)
		return false
	}

	f, err := os.OpenFile(toAppendFileName, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		fmt.Printf("Could not open file to append %s. Appending failed in bad state\n", toAppendFileName)
		return false
	}
	defer f.Close()
	if _, err := f.WriteString(string(appendfileBytes[fileByteLocation:])); err != nil {
		fmt.Printf("Failed writing data file to append %s. Appending failed in bad state\n", toAppendFileName)
	}

	os.Remove(swapFileName)
	return true
}

func main() {

	var filesToJoin []string
	var outputFileName = ""

	if len(os.Args) > 2 {

		var allFilesAccessible = true
		outputFileName = os.Args[1]

		// Make sure output file doesn't already exist
		if _, err := os.Stat(outputFileName); err == nil {
			fmt.Printf("Output file %s already exists. Won't overwrite or append. Exiting.\n", outputFileName)
			os.Exit(-1)
		} else {
			fmt.Printf("Saving output to file '%s'\n", outputFileName)
		}

		// Loop through all the files listed as parameters and make sure they're accessible
		for _, filename := range os.Args[2:] {
			if _, err := os.Stat(filename); err == nil {
				//fmt.Println("hello world " + filename)
				filesToJoin = append(filesToJoin, filename)
			} else if errors.Is(err, os.ErrNotExist) {
				fmt.Printf("File '%s' does not exist or can't be opened\n", filename)
				allFilesAccessible = false
			} else {
				fmt.Printf("File '%s' can't be accessed for some unknown reason\n", filename)
				allFilesAccessible = false
			}
		}
		if !allFilesAccessible {
			// Not all the filenames passed as parameters were accessible so exit out
			os.Exit(-1)
		}
	} else {
		fmt.Println("Usage: go run file_joiner output_file_name [file1] [file2] ... [fileN]")
	}

	// OK done sanity checking input, now try to join files together

	// Take first file and copy it to the output file
	firstFileByteRead, err := ioutil.ReadFile(filesToJoin[0])
	if err != nil {
		fmt.Printf("Could not read first file to copy for some reason. Exiting")
		os.Exit(-1)
	}
	err = ioutil.WriteFile(outputFileName, firstFileByteRead, 0644)
	if err != nil {
		fmt.Printf("Could not write first file to copy for some reason. Exiting")
		os.Exit(-1)
	}

	for _, filename := range filesToJoin[1:] {

		outputFileBytes, err := ioutil.ReadFile(outputFileName)
		fmt.Printf("Output file size %d\n", len(outputFileBytes))
		// TODO This assumes there is at least 100 bytes in the file. Should do a test to make sure
		outputFileFirst100ByteAsString := string(outputFileBytes[0:100])
		outputFileLast100ByteAsString := string(outputFileBytes[len(outputFileBytes)-100 : len(outputFileBytes)])

		// Does this read the whole file into memory or is there some smarter access-on-demand happening?
		fileBytes, err := ioutil.ReadFile(filename)
		if err != nil {
			fmt.Printf("Error reading file %s. Exiting.", filename)
			os.Exit(-1)
		}

		pieceFileAsString := string(fileBytes)

		indexFirstOfTop := strings.Index(pieceFileAsString, outputFileFirst100ByteAsString)
		indexLastOfTop := strings.LastIndex(pieceFileAsString, outputFileFirst100ByteAsString)
		indexFirstOfBottom := strings.Index(pieceFileAsString, outputFileLast100ByteAsString)
		indexLastOfBottom := strings.Index(pieceFileAsString, outputFileLast100ByteAsString)

		fmt.Printf("file %s Top First %d Top Last %d Bottom First %d Bottom Last %d\n",
			filename,
			indexFirstOfTop, indexLastOfTop, indexFirstOfBottom, indexLastOfBottom)

		if indexFirstOfBottom != -1 && indexLastOfBottom != -1 {
			// The current file overlaps at the bottom of the output file
			overlapClosestToEnd := MaxInt(indexFirstOfBottom, indexFirstOfBottom)
			fmt.Printf("Max position %d\n", overlapClosestToEnd)
			worked := AppendFile(outputFileName, overlapClosestToEnd+len(outputFileLast100ByteAsString), filename)
			if worked {
				fmt.Printf("IT WORKED!\n")
			} else {
				fmt.Printf("IT DIDN'T WORK!\n")
				os.Exit(-1)
			}
		} else if indexFirstOfTop != -1 && indexLastOfTop != -1 {
			// The current file overlaps at the top of the output file
			overlapNearestBeginning := MinInt(indexFirstOfTop, indexLastOfTop)
			worked := PrependFile(outputFileName, overlapNearestBeginning, filename)
			if worked {
				fmt.Printf("IT WORKED!\n")
			} else {
				fmt.Printf("IT DIDN'T WORK!\n")
				os.Exit(-1)
			}
		}

	}
}
