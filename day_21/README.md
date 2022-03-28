# Basic file signing in Go

---
```
Language: Go
Brief: Some basic crypto work of 'signing' a file
Scope: 
Tags: cryptography
State: 
Result: 
```
---

There is a utility program for stuffing signed SHA-1 digests of gzip files into the header of the same gzip. I can't get the source to
easily compile because it was written years ago against versions of openssl that are way outdated. 

I am going to see if I can recreate the functionality in a new utility program written in Go.

Seems like a fine little project to tinker with some of the crypto primitives in Go and reenforce some of the IO stuff i learned in the file joiner project from day_3, which is already getting a bit fuzzy.

### Results

---

Not a lot of progress. I got bits and pieces working, but haven't put it all together.

I don't think I like Go.

### If I was to do more

---

### Notes

---

GZSig uses SHA1 as hash

```azure
/* Compute SHA1 checksum over compressed data and trailer. */
	sig = (u_char *)(gd + 1);
	siglen = gx->subfield.len - sizeof(*gd);

	SHA1_Init(&ctx);
	
	while ((i = fread(buf, 1, sizeof(buf), fin)) > 0) {
		SHA1_Update(&ctx, buf, i);
	}
	SHA1_Final(digest, &ctx);
	
	/* Verify signature. */
	if (key_verify(key, digest, sizeof(digest), sig, siglen) < 0) {
		fprintf(stderr, "Error verifying signature\n");
		return (-1);
	}
```

sha1 of "lorumipsum.txt" -> 3bdeac7d1687e00dc10b5070ca40615fbdcbcf48

Original util supports RSA / DSA keys in x509 certs

openssl genrsa -out rsaprivkey.pem 2048
openssl rsa -in rsaprivkey.pem -outform PEM -pubout -out public.pem

openssl dsaparam -out dsaparam.pem 2048
openssl gendsa -out dsaprivkey.pem dsaparam.pem


### Example 

---