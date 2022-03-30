# SHA1 hash of gzip compressed data

---
```
Language: Go
Brief: Calculate the hash of just the body of a gzip file
Scope: 
Tags: 
State: 
Result: 
```
---

The GZIP libraries of Go don't seem to have an easy way to get to the compressed bytes of a GZIP file. 

Need to implement parsing the file header and calculate the sum of the body.

### Results

---

Worked!

The code is a bit rough but the calculated hash from the Go program matches the hash value from the shasum command line tool.

### If I was to do more

---

Clean up the code into a function that returns an interface to the file

Make the reading of the file contents more efficient. Right now it's one byte at a time. This is only because I was too lazy to figure out how to do handle EOFs in a ReadFull.


### Notes

---

[hex fiend](https://hexfiend.com/) utility to alter a gzip file manually chopping out the header. This was for comparison testing of my code and shasum

[gzip header](https://formats.kaitai.io/gzip/gzip.svg) diagram of header format

[RFC 1952 - Gzip format](https://datatracker.ietf.org/doc/html/rfc1952)

None of the other code i looked at seemed to be able to handle more than one GZip Subsection extra header. Weird

### Example 

---

Output of my Go code
```azure
GOROOT=/usr/local/go #gosetup
GOPATH=/Users/pickard/projects/100_days_of_code_2022/local/go-path #gosetup
/usr/local/go/bin/go build -o /private/var/folders/6m/h4gzwp_n73v0m0l0550st65c0000gn/T/GoLand/___go_build_gzipfilereader_go /Users/pickard/projects/100_days_of_code_2022/day_23/gzipfilereader.go #gosetup
/private/var/folders/6m/h4gzwp_n73v0m0l0550st65c0000gn/T/GoLand/___go_build_gzipfilereader_go
timestamp 2022-03-28 12:29:46 -0400 EDT
OS is 'FAT'
No Extra headers, not signed


Name in header 'lorumipsum.txt' len is '15'
No comment in GZip header
Error trying to read checksum from header
Total read header bytes '25'

Got EOF 0
Total read body bytes '422'

Hash of GZip body is 'a70db4ca237103d9f2da15cdeaeaf155a9a36976'
Process finished with the exit code 0


```

SHA1 sum of gzip file with header manually removed. Leaving just the compressed bytes
```azure
(base) [pickard@eris.local:] projects/100_days_of_code_2022/day_23 [main] ?? % shasum lorumipsum.txt.gz_HEADLESS
a70db4ca237103d9f2da15cdeaeaf155a9a36976  lorumipsum.txt.gz_HEADLESS

```

Both calculated 'a70db4ca237103d9f2da15cdeaeaf155a9a36976'