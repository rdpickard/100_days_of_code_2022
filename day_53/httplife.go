package main

import (
	"fmt"
	"github.com/gorilla/mux"
	"image"
	"image/color"
	"image/gif"
	"log"
	"math/rand"
	"net/http"
	"time"
)

var blackRedAndWhitePalette = []color.Color{color.White, color.Black, color.RGBA{R: 255, G: 0, B: 0, A: 255}, color.RGBA{R: 0, G: 0, B: 255, A: 255}}

const (
	whiteIndex = 0
	blackIndex = 1
	redIndex   = 2
	blueIndex  = 3
)

func main() {
	requestRouter := mux.NewRouter()
	requestRouter.HandleFunc("/{phrase:[a-z]+}", ConwayGameOfLifeHandler).Methods("GET") // each request calls handler

	http.Handle("/", requestRouter)

	log.Fatal(http.ListenAndServe("localhost:8000", nil))
}

func ContinuousPlanePixelValue(img *image.Paletted, x int, y int) uint8 {

	bounds := img.Bounds()

	value_x := x
	value_y := y

	if value_x < bounds.Min.X {
		value_x = bounds.Max.X - 1
	}
	if value_x >= bounds.Max.X {
		value_x = bounds.Min.X
	}

	if value_y < bounds.Min.Y {
		value_y = bounds.Max.Y - 1
	}
	if value_y >= bounds.Max.Y {
		value_y = bounds.Min.Y
	}

	return img.ColorIndexAt(value_x, value_y)
}

func PixelIsAlive(img *image.Paletted, x int, y int) uint8 {
	colorIndexValueAtPosition := ContinuousPlanePixelValue(img, x, y)

	if colorIndexValueAtPosition > whiteIndex {
		return 1
	} else {
		return 0
	}
}

func PixelLiveNeighborsCount(img *image.Paletted, x int, y int) uint8 {

	/**
	aliveNeighbors := PixelIsAlive(img, x-1, y-1) +
		PixelIsAlive(img, x-1, y) +
		PixelIsAlive(img, x-1, y+1) +
		PixelIsAlive(img, x, y-1) +
		PixelIsAlive(img, x, y+1) +
		PixelIsAlive(img, x+1, y-1) +
		PixelIsAlive(img, x+1, y) +
		PixelIsAlive(img, x+1, y+1)
	**/

	aliveNeighbors := PixelIsAlive(img, x-1, y-1) +
		PixelIsAlive(img, x, y-1) +
		PixelIsAlive(img, x+1, y-1) +
		PixelIsAlive(img, x-1, y) +
		PixelIsAlive(img, x+1, y) +
		PixelIsAlive(img, x-1, y+1) +
		PixelIsAlive(img, x, y+1) +
		PixelIsAlive(img, x+1, y+1)

	/*
		fmt.Printf("(%dx%d):%d\n", x, y, aliveNeighbors)
		fmt.Printf("[%d%d%d\n", PixelIsAlive(img, x-1, y-1), PixelIsAlive(img, x-1, y), PixelIsAlive(img, x-1, y+1))
		fmt.Printf(" %d %d\n", PixelIsAlive(img, x, y-1), PixelIsAlive(img, x, y+1))
		fmt.Printf(" %d%d%d]\n\n", PixelIsAlive(img, x+1, y-1), PixelIsAlive(img, x+1, y), PixelIsAlive(img, x+1, y+1))
	*/
	return aliveNeighbors
}

func ConwayGameOfLifeHandler(w http.ResponseWriter, r *http.Request) {

	rand.Seed(time.Now().UnixNano())

	generations := 100

	gifFrameDelay := 10
	gifImageSizeInPixels := 100

	anim := gif.GIF{LoopCount: generations}
	rect := image.Rect(0, 0, gifImageSizeInPixels, gifImageSizeInPixels)

	progenitorImg := image.NewPaletted(rect, blackRedAndWhitePalette)
	for y := 0; y < gifImageSizeInPixels; y++ {
		for x := 0; x < gifImageSizeInPixels; x++ {
			if rand.Intn(2) == 1 {
				progenitorImg.SetColorIndex(x, y, blackIndex)
			}
		}
	}

	/*
		progenitorMatrix := [10][10]int{
			{0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
			{0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
			{0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
			{0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
			{0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
			{0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
			{0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
			{0, 0, 0, 0, 1, 0, 0, 0, 0, 0},
			{0, 0, 0, 0, 0, 1, 0, 0, 0, 0},
			{0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
		}

		for x := 0; x < gifImageSizeInPixels; x++ {
			for y := 0; y < gifImageSizeInPixels; y++ {
				if progenitorMatrix[y][x] == 1 {
					progenitorImg.SetColorIndex(x, y, blackIndex)
				}
			}
		}
	*/

	// Add in some gliders
	var glider = [3][3]int{
		{0, 1, 0},
		{0, 0, 1},
		{1, 1, 1},
	}

	for k := 1; k < 2; k++ {
		//progenitorx := rand.Intn(gifImageSizeInPixels)
		//progenitory := rand.Intn(gifImageSizeInPixels)
		progenitorx := 2
		progenitory := 2

		for glidery := 0; glidery < 3; glidery++ {

			for gliderx := 0; gliderx < 3; gliderx++ {
				progenitorImg.SetColorIndex(
					progenitorx+gliderx,
					progenitory+glidery,
					uint8(glider[glidery][gliderx]))
			}
		}
	}

	anim.Delay = append(anim.Delay, gifFrameDelay)
	anim.Image = append(anim.Image, progenitorImg)

	for i := 0; i < generations; i++ {

		img := image.NewPaletted(rect, blackRedAndWhitePalette)
		mortis := true

		//"copy" the progenitorImg
		/**
		for x := 0; x < gifImageSizeInPixels; x++ {
			for y := 0; y < gifImageSizeInPixels; y++ {
				img.SetColorIndex(x, y, progenitorImg.ColorIndexAt(x, y))
			}
		}
		**/
		for y := 0; y < gifImageSizeInPixels; y++ {

			for x := 0; x < gifImageSizeInPixels; x++ {

				pixelIsLive := progenitorImg.ColorIndexAt(x, y) >= 1

				pixelNeighbors := PixelLiveNeighborsCount(progenitorImg, x, y)

				if pixelIsLive && (pixelNeighbors < 2) {
					img.SetColorIndex(x, y, whiteIndex)
				} else if pixelIsLive && (pixelNeighbors == 2 || pixelNeighbors == 3) {
					img.SetColorIndex(x, y, blueIndex)
				} else if pixelIsLive && (pixelNeighbors > 3) {
					img.SetColorIndex(x, y, whiteIndex)
				} else if !pixelIsLive && (pixelNeighbors > 3) {
					img.SetColorIndex(x, y, redIndex)
				} else if pixelIsLive {
					fmt.Printf("WHAT?? %d\n", pixelNeighbors)
				}

				if mortis && (img.ColorIndexAt(x, y) != progenitorImg.ColorIndexAt(x, y)) {
					mortis = false
				}
			}

		}

		if mortis {
			for x := 0; x < gifImageSizeInPixels; x++ {
				for y := 0; y < gifImageSizeInPixels; y++ {
					if img.ColorIndexAt(x, y) >= 1 {
						img.SetColorIndex(x, y, redIndex)
					}
				}
			}

			anim.Delay = append(anim.Delay, gifFrameDelay*(generations-i))
			anim.Image = append(anim.Image, img)
			fmt.Printf("mortis")
			break
		} else {
			anim.Delay = append(anim.Delay, gifFrameDelay)
			anim.Image = append(anim.Image, img)
			//progenitorImg = img
			for x := 0; x < gifImageSizeInPixels; x++ {
				for y := 0; y < gifImageSizeInPixels; y++ {
					progenitorImg.SetColorIndex(x, y, img.ColorIndexAt(x, y))
				}
			}
		}
	}

	err := gif.EncodeAll(w, &anim)
	if err != nil {
		return
	}

}
