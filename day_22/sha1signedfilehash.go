package main

import (
	"crypto"
	"crypto/rand"
	"crypto/rsa"
	"crypto/sha1"
	"crypto/x509"
	"encoding/pem"
	"fmt"
	"io/ioutil"
	"os"
	"strings"
)

func main() {

	privateKeyFilePath := "local/day_21/rsa_privatekey.pem"
	//privateKeyFilePath := "local/day_21/rsa_privatekey_withpassword.pem"
	publicKeyFilePath := "local/day_21/rsa_publickey.pem"

	fileToHashPath := "day_21/lorumipsum.txt.gz"

	privKeyFileBytes, err := ioutil.ReadFile(privateKeyFilePath)
	if err != nil {
		fmt.Printf("Could not open private key file %s\n", privateKeyFilePath)
		println(err)
		os.Exit(-1)
	}

	privKeyPEMBlock, _ := pem.Decode(privKeyFileBytes)
	//P The 'Block' postfix is a little clunky but the Decode function returns a struct called Block, so I'm doing this for clarity
	if privKeyPEMBlock == nil {
		println("Could not decode private key file bytes with PEM coding")
		println(err)
		os.Exit(-1)
	}

	var privateRSAKeyPreamble = "RSA PRIVATE KEY"
	if privKeyPEMBlock.Type != privateRSAKeyPreamble {
		fmt.Printf("Expected preamble '%s' in PEM data, but got '%s'. Exiting.", privateRSAKeyPreamble, privKeyPEMBlock.Type)
		os.Exit(-1)
	}

	fmt.Println("PEM Block headers: ", privKeyPEMBlock.Headers)

	var privateRSAKeyBytes []byte
	var privateKeyPEMBlockLooksEncrypted bool
	if val, ok := privKeyPEMBlock.Headers["Proc-Type"]; ok {
		if strings.Contains(val, "ENCRYPTED") {
			privateKeyPEMBlockLooksEncrypted = true
			var privatekeyPassphrase string

			println("Looks encrypted")
			fmt.Print("Enter passphrase: ")
			fmt.Scanf("%s", &privatekeyPassphrase)

			privateRSAKeyBytes, err = x509.DecryptPEMBlock(privKeyPEMBlock, []byte(privatekeyPassphrase))
		}
	} else {
		// Unencrypted private key file
		privateKeyPEMBlockLooksEncrypted = false
		privateRSAKeyBytes = privKeyPEMBlock.Bytes
	}

	var parsedKey interface{}
	parsedKey, err = x509.ParsePKCS1PrivateKey(privateRSAKeyBytes)
	if err != nil {
		if privateKeyPEMBlockLooksEncrypted {
			println("Could not parse private key PEM bytes into PKCS1. Maybe bad passphrase?")
		} else {
			println("Could not parse private key PEM bytes into PKCS1. Maybe bad passphrase?")
		}
		println(err)
		os.Exit(-1)
	}

	var privateKey *rsa.PrivateKey
	var ok bool
	privateKey, ok = parsedKey.(*rsa.PrivateKey)
	if !ok {
		println("Could not cast to a private key. Exiting")
		os.Exit(-1)
	}

	// OK should have me signing key all loaded now
	fmt.Println(privateKey.Primes)

	// Calculate the SHA1 of the file
	fileToHashByes, err := ioutil.ReadFile(fileToHashPath)
	if err != nil {
		fmt.Printf("Could not open file to hash at path '%s' for some reason", fileToHashPath)
		os.Exit(-1)
	}

	sha1Hasher := sha1.New()
	sha1Hasher.Write(fileToHashByes)
	fileHashSum := sha1Hasher.Sum(nil)

	// P confirmed this worked with the output of the command line shasum day_21/lorumipsum.txt.gz
	fmt.Printf("File hash %x\n", fileHashSum)

	//signature, signerr := privateKey.Sign(rand.Reader, fileHashSum, nil)
	signature, signerr := rsa.SignPSS(rand.Reader, privateKey, crypto.SHA1, fileHashSum, nil)
	if signerr != nil {
		fmt.Printf("Sign error")
		fmt.Println(signerr)
		os.Exit(-1)
	}
	fmt.Printf("Signature %x\n", signature)
	fmt.Printf("Signature len %d\n", len(signature))

	fmt.Printf("\n\n")

	// OK so now i've got a private key, a SHA1 hash of a file, that SHA1 hash signed by the private key

	publicKeyFileBytes, err := ioutil.ReadFile(publicKeyFilePath)
	if err != nil {
		fmt.Printf("Could not load public key file from path '%s'\n", publicKeyFilePath)
		fmt.Println(err)
		os.Exit(-1)
	}
	publicKeyPEMBlock, _ := pem.Decode(publicKeyFileBytes)
	if publicKeyPEMBlock == nil {
		fmt.Printf("Could not parse public key file '%s' with PEM coding\n", publicKeyFilePath)
		os.Exit(-1)
	}
	var publicRSAKeyPreamble = "PUBLIC KEY"
	if publicKeyPEMBlock.Type != publicRSAKeyPreamble {
		fmt.Printf("Expected preamble '%s' in public key file '%s' instead got '%s'. Exiting", publicRSAKeyPreamble, publicKeyFilePath, publicKeyPEMBlock.Type)
		os.Exit(-1)
	}
	var parsedPublicKey interface{}
	parsedPublicKey, err = x509.ParsePKIXPublicKey(publicKeyPEMBlock.Bytes)
	if err != nil {
		fmt.Printf("Could not parse public key PEM into public key object")
		println(err)
		os.Exit(-1)
	}

	var publicKey *rsa.PublicKey
	publicKey, ok = parsedPublicKey.(*rsa.PublicKey)
	if !ok {
		fmt.Printf("Could not cast public key  into public RSA key object")
		println(err)
		os.Exit(-1)
	}

	err = rsa.VerifyPSS(publicKey, crypto.SHA1, fileHashSum, signature, nil)
	if err != nil {
		fmt.Printf("poop")
	} else {
		fmt.Printf("not poop")
	}
}
