package main

import (
	"bufio"
	"crypto/sha1"
	"encoding/binary"
	"fmt"
	"io"
	"log"
	"os"
	"time"
)

// P theses are taken right from the gunzip.go
const (
	gzipID1     = 0x1f
	gzipID2     = 0x8b
	gzipDeflate = 8
	flagText    = 1 << 0
	flagHdrCrc  = 1 << 1
	flagExtra   = 1 << 2
	flagName    = 1 << 3
	flagComment = 1 << 4

	os_id_FAT             = 0
	os_id_Amiga           = 1
	os_id_VMS             = 2
	os_id_Unix            = 3
	os_id_VM_CMS          = 4
	os_id_Atari_TOS       = 5
	os_id_HPFS_filesystem = 6
	os_id_Macintosh       = 7
	os_id_Z_System        = 8
	os_id_CP_M            = 9
	os_id_TOPS_20         = 10
	os_id_NTFS_filesystem = 11
	os_id_QDOS            = 12
	os_id_Acorn_RISCOS    = 13
	os_id_unknown         = 255
)

func main() {

	var totalHeaderBytesRead uint16 = 0

	gzipedFilePath := "day_23/lorumipsum.txt.gz"

	gzipedFile, err := os.Open(gzipedFilePath)
	if err != nil {
		fmt.Printf("Could not open gzip file '%s' for some reason. Exitin\n", gzipedFilePath)
		fmt.Println(err)
		os.Exit(-1)
	}

	buf := make([]byte, 10)
	var readCount int
	if readCount, err = io.ReadFull(gzipedFile, buf); err != nil {
		log.Fatal(err)
	}
	totalHeaderBytesRead += uint16(readCount)

	if !(buf[0] == gzipID1 && buf[1] == gzipID2) {
		fmt.Printf("File does not start with GZIP 'magic' id. Maybe not a gzip file. Exiting")
		os.Exit(-1)
	}
	if buf[2] != gzipDeflate {
		fmt.Printf("GZIP compression_method in header is not expected value of '%x'. got '%x' instead. Exiting.", gzipDeflate, buf[2])
		os.Exit(-1)
	}

	var timestamp time.Time
	var hasTimestamp bool = false
	if t := int64(binary.LittleEndian.Uint32(buf[4:8])); t > 0 {
		timestamp = time.Unix(t, 0)
		hasTimestamp = true
	}
	if hasTimestamp {
		fmt.Printf("timestamp %s\n", timestamp)
	} else {
		fmt.Printf("timestamp (none)")
	}

	switch buf[8] {
	case os_id_FAT:
		{
			fmt.Printf("OS is 'FAT'\n")
		}
	case os_id_Amiga:
		{
			fmt.Printf("OS is 'Amiga'\n")
		}
	case os_id_VMS:
		{
			fmt.Printf("OS is 'VMS'\n")
		}
	case os_id_Unix:
		{
			fmt.Printf("OS is 'Unix'\n")
		}
	case os_id_VM_CMS:
		{
			fmt.Printf("OS is 'VM CMS'\n")
		}
	case os_id_Atari_TOS:
		{
			fmt.Printf("OS is 'Atari TOS'\n")
		}
	case os_id_HPFS_filesystem:
		{
			fmt.Printf("OS is 'HPFS filesystem'\n")
		}
	case os_id_Macintosh:
		{
			fmt.Printf("OS is 'Macintosh'\n")
		}
	case os_id_Z_System:
		{
			fmt.Printf("OS is 'Z-System'\n")
		}
	case os_id_CP_M:
		{
			fmt.Printf("OS is 'CP M'\n")
		}
	case os_id_TOPS_20:
		{
			fmt.Printf("OS is 'TOPS 20'\n")
		}
	case os_id_NTFS_filesystem:
		{
			fmt.Printf("OS is 'NTFS filesystem'\n")
		}
	case os_id_QDOS:
		{
			fmt.Printf("OS is 'QDOS'\n")
		}
	case os_id_Acorn_RISCOS:
		{
			fmt.Printf("OS is 'Acorn RISCOS'\n")
		}
	case os_id_unknown:
		{
			fmt.Printf("OS is 'unknown'\n")
		}
	default:
		{
			fmt.Printf("OS val is of documented type value '%d'\n", buf[8])
		}
	}

	//buf[9] is 'extra_flags', with is different than extra headers

	if buf[3]&flagExtra == 0 {
		fmt.Printf("No Extra headers, not signed\n")
	} else {

		extrasTotalLenBuf := make([]byte, 2)
		if readCount, err = io.ReadFull(gzipedFile, extrasTotalLenBuf); err != nil {
			log.Fatal(err)
		}
		totalHeaderBytesRead += uint16(readCount)

		var extrasTotalLen = binary.LittleEndian.Uint16(extrasTotalLenBuf)

		var totalExtraBytesRead uint16 = 0

		fmt.Printf("Total extras len '%d'\n", extrasTotalLen)

		for totalExtraBytesRead < extrasTotalLen {
			fmt.Printf("Total extras read '%d'\n", totalExtraBytesRead)

			cExtraHeaderSubfieldIDBuf := make([]byte, 2)
			cExtraHeaderSubfieldLenBuf := make([]byte, 2)

			if readCount, err = io.ReadFull(gzipedFile, cExtraHeaderSubfieldIDBuf); err != nil {
				log.Fatal(err)
			}
			totalHeaderBytesRead += uint16(readCount)
			totalExtraBytesRead += uint16(readCount)
			if readCount, err = io.ReadFull(gzipedFile, cExtraHeaderSubfieldLenBuf); err != nil {
				log.Fatal(err)
			}
			totalHeaderBytesRead += uint16(readCount)
			totalExtraBytesRead += uint16(readCount)

			var cExtraHeaderSubfieldLen = binary.LittleEndian.Uint16(cExtraHeaderSubfieldLenBuf)

			fmt.Printf("Current extra header id is '%c%c' len is '%d'\n", cExtraHeaderSubfieldIDBuf[0], cExtraHeaderSubfieldIDBuf[1], cExtraHeaderSubfieldLen)

			cExtraHeaderSubfieldDataBuf := make([]byte, cExtraHeaderSubfieldLen)
			if readCount, err = io.ReadFull(gzipedFile, cExtraHeaderSubfieldDataBuf); err != nil {
				log.Fatal(err)
			}
			totalHeaderBytesRead += uint16(readCount)
			totalExtraBytesRead += uint16(readCount)

			if string(cExtraHeaderSubfieldIDBuf) == "GS" {
				fmt.Printf("Found GSig extra header. Len is '%d'\n", cExtraHeaderSubfieldLen)
			}

		}
	}

	fmt.Printf("\n\n")

	if buf[3]&flagName == 0 {
		fmt.Printf("No name in GZip header\n")
	} else {
		nameHeader, err := bufio.NewReader(gzipedFile).ReadString(0)
		if err != nil {
			fmt.Printf("Error trying to read name value out of GZip file header\n")
			fmt.Println(err)
			os.Exit(-1)
		}
		fmt.Printf("Name in header '%s' len is '%d'\n", nameHeader, len(nameHeader))
		totalHeaderBytesRead += uint16(len(nameHeader))

	}

	if buf[3]&flagComment == 0 {
		fmt.Printf("No comment in GZip header\n")
	} else {
		commentHeader, err := bufio.NewReader(gzipedFile).ReadString(0)
		if err != nil {
			fmt.Printf("Error trying to read comment value out of GZip file header\n")
			fmt.Println(err)
			os.Exit(-1)
		}
		fmt.Printf("Comment in header '%s' len is '%d'\n", commentHeader, len(commentHeader))
		totalHeaderBytesRead += uint16(len(commentHeader))
	}

	headerCRC16Buf := make([]byte, 2)
	if readCount, err = io.ReadFull(gzipedFile, headerCRC16Buf); err != nil {
		fmt.Printf("Error trying to read checksum from header\n")
	}
	totalHeaderBytesRead += uint16(readCount)

	fmt.Printf("Total read header bytes '%d'\n\n", totalHeaderBytesRead)

	// P Buffered reader seems to mess with reading from the gzipedFile pointer, so reset the read position to the
	// P end of the headers

	gzipedFile.Seek(int64(totalHeaderBytesRead), 0)

	sha1Hasher := sha1.New()
	fileHashReader := io.TeeReader(gzipedFile, sha1Hasher)

	data := make([]byte, 1)
	var totalDataBytesRead uint16 = 0

	for {
		dataRead, err := io.ReadFull(fileHashReader, data)
		if err != nil {
			if err == io.EOF {
				fmt.Printf("Got EOF %d\n", dataRead)
				break
			}
			fmt.Printf("Error reading data from gzip\n")
			fmt.Println(err)
			break
		}
		totalDataBytesRead += uint16(dataRead)

	}

	fmt.Printf("Total read body bytes '%d'\n\n", totalDataBytesRead)

	fileHashSum := sha1Hasher.Sum(nil)

	fmt.Printf("Hash of GZip body is '%x'", fileHashSum)

}
