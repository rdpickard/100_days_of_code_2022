package main

import (
	"bytes"
	"compress/gzip"
	"encoding/binary"
	"fmt"
	"os"
)

type GSigHeader struct {
	HeaderSegmentId  [2]byte
	HeaderSegmentLen [2]byte
	GSigVersion      byte
}

func main() {

	//gzipedFilePath := "/Volumes/my_secret_file"
	gzipedFilePath := "day_21/lorumipsum.txt.gz"

	gzipedFile, err := os.Open(gzipedFilePath)
	if err != nil {
		fmt.Printf("Could not read file to hash for some reason. Exiting")
		os.Exit(-1)
	}

	gzReader, err := gzip.NewReader(gzipedFile)
	if err != nil {
		fmt.Printf("Could not create gzip reader for some reason. Exiting")
		fmt.Println(err)
		os.Exit(-1)
	}

	fmt.Printf("Name: %s\nComment: %s\nModTime: %s\n\n", gzReader.Name, gzReader.Comment, gzReader.ModTime.UTC())

	fmt.Printf("name header len: %d\n\n", binary.Size(gzReader.Name))
	fmt.Printf("name header len: %d\n\n", len(gzReader.Name))

	if len(gzReader.Header.Extra) == 0 {
		fmt.Println("Extra: (none)")
	} else {
		fmt.Printf("Extra %x\n", gzReader.Extra)
		fmt.Printf("Extra length %d\n", len(gzReader.Extra))

		gsigHeader := GSigHeader{}
		//err := binary.Read(bytes.NewBuffer(gzReader.Extra), binary.LittleEndian, &gsigHeader)
		err := binary.Read(bytes.NewBuffer(gzReader.Extra), binary.LittleEndian, &gsigHeader)

		if err != nil {
			panic(err)
		}
		fmt.Println()

		siglen := uint16(gsigHeader.HeaderSegmentLen[0])<<8 | uint16(gsigHeader.HeaderSegmentLen[1])

		fmt.Printf("gsigHeader ID %s\n", gsigHeader.HeaderSegmentId)
		fmt.Printf("gsigHeader len %d\n", siglen)
		fmt.Printf("gsigHeader version %d\n", gsigHeader.GSigVersion)

		var sig []byte = make([]byte, siglen-1)

		err = binary.Read(bytes.NewBuffer(gzReader.Extra[5:]), binary.LittleEndian, &sig)

		if err != nil {
			panic(err)
		}

		fmt.Printf("Sig %x", sig)

	}

	defer gzipedFile.Close()
	defer gzReader.Close()

}
