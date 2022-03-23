package main

import (
	"github.com/gin-gonic/gin"
	"net/http"
)

func APIAddImage(c *gin.Context) {
	var books []string
	c.JSON(http.StatusOK, gin.H{"data": books})
}

func APILabelImage(c *gin.Context) {
	var books []string
	c.JSON(http.StatusOK, gin.H{"data": books})
}

func main() {
	r := gin.Default()

	r.GET("/", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{"data": "hello world"})
	})

	r.Run()
}
