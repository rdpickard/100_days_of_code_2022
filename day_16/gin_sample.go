package main

import (
	"github.com/gin-gonic/gin"
	"net/http"
)

func APIImage(c *gin.Context) {
	var images []string

	if c.Request.Method == "GET" {
		c.JSON(http.StatusOK, gin.H{"images": images})
	} else if c.Request.Method == "POST" {
		c.JSON(http.StatusOK, gin.H{"image": "derp"})
	} else {
		c.JSON(http.StatusMethodNotAllowed, gin.H{"image": "crap"})
	}

}

func APIGetImage(c *gin.Context) {
	var books []string
	print(c)
	c.JSON(http.StatusOK, gin.H{"data": books})
}

func main() {
	r := gin.Default()

	r.GET("/", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{"data": "hello world"})
	})

	r.PUT("/api/image", APIImage)
	r.GET("/api/image", APIImage)
	r.POST("/api/image", APIImage)

	r.Run()
}
