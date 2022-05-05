package main

import (
	"fmt"
	"image"
	"image/color"
	"image/gif"
	"math/rand"
	"net/http"
	"os"
	"time"
)

var blackRedAndWhitePalette = []color.Color{color.White,
	color.Black,
	color.RGBA{R: 255, G: 0, B: 0, A: 255},
	color.RGBA{R: 0, G: 0, B: 255, A: 255},
	color.RGBA{R: 0, G: 255, B: 0, A: 255}}

const (
	whiteIndex = 0
	blackIndex = 1
	redIndex   = 2
	blueIndex  = 3
	greenIndex = 4
)

func main() {

	rand.Seed(time.Now().UnixNano())

	generations := 1000

	newColonyMemberMaxLifeSteps := 1000

	gifFrameDelay := 2
	gifImageSizeInPixels := 150

	anim := gif.GIF{LoopCount: generations}
	rect := image.Rect(0, 0, gifImageSizeInPixels, gifImageSizeInPixels)

	progenitorImg := image.NewPaletted(rect, blackRedAndWhitePalette)

	// Set the 'seed'
	progenitorImg.SetColorIndex(rand.Intn(gifImageSizeInPixels), rand.Intn(gifImageSizeInPixels), greenIndex)

	anim.Delay = append(anim.Delay, gifFrameDelay)
	anim.Image = append(anim.Image, progenitorImg)

	generation := 0

	//for i := 0; i < generations; i++ {
	for generation < generations {
		//fmt.Printf("Gen %d", i)

		img := image.NewPaletted(rect, blackRedAndWhitePalette)

		for x := 0; x < gifImageSizeInPixels; x++ {
			for y := 0; y < gifImageSizeInPixels; y++ {
				img.SetColorIndex(x, y, progenitorImg.ColorIndexAt(x, y))
			}
		}

		anim.Delay = append(anim.Delay, gifFrameDelay)
		anim.Image = append(anim.Image, img)

		// new colony member
		newColonyMember_x := rand.Intn(gifImageSizeInPixels)
		newColonyMember_y := rand.Intn(gifImageSizeInPixels)

		colonyNeighbors := PixelLiveNeighborsCount(progenitorImg, newColonyMember_x, newColonyMember_y)
		newColonyMember_steps := 0

		for colonyNeighbors < 1 && newColonyMember_steps < newColonyMemberMaxLifeSteps {

			//img.SetColorIndex(newColonyMember_x, newColonyMember_y, whiteIndex)

			switch rand.Intn(8) {
			case 0:
				newColonyMember_y = newColonyMember_y - 1
				newColonyMember_x = newColonyMember_x - 1
			case 1:
				newColonyMember_y = newColonyMember_y - 1
			case 2:
				newColonyMember_y = newColonyMember_y - 1
				newColonyMember_x = (newColonyMember_x + 1) % gifImageSizeInPixels
			case 3:
				newColonyMember_x = newColonyMember_x - 1
			case 4:
				newColonyMember_x = (newColonyMember_x + 1) % gifImageSizeInPixels
			case 5:
				newColonyMember_y = (newColonyMember_y + 1) % gifImageSizeInPixels
				newColonyMember_x = newColonyMember_x - 1
			case 6:
				newColonyMember_y = (newColonyMember_y + 1) % gifImageSizeInPixels
			case 7:
				newColonyMember_y = (newColonyMember_y + 1) % gifImageSizeInPixels
				newColonyMember_x = (newColonyMember_x + 1) % gifImageSizeInPixels
			}

			if newColonyMember_y < 0 {
				newColonyMember_y = gifImageSizeInPixels + newColonyMember_y
			}
			if newColonyMember_x < 0 {
				newColonyMember_x = gifImageSizeInPixels + newColonyMember_x
			}

			//fmt.Printf("Get %d step %d %d,%d\n", i, newColonyMember_steps, newColonyMember_x, newColonyMember_y)

			newColonyMember_steps += 1
			colonyNeighbors = PixelLiveNeighborsCount(progenitorImg, newColonyMember_x, newColonyMember_y)
			img.SetColorIndex(newColonyMember_x, newColonyMember_y, blackIndex)
		}

		if newColonyMember_steps >= newColonyMemberMaxLifeSteps {
			//fmt.Printf("NEW COLONY MEMBER DIED OF STEPS")
			//img.SetColorIndex(rand.Intn(gifImageSizeInPixels), rand.Intn(gifImageSizeInPixels), redIndex)
		} else {
			//fmt.Printf("KLUMP AT %d, %d", newColonyMember_x, newColonyMember_y)
			img.SetColorIndex(newColonyMember_x, newColonyMember_y, blueIndex)
			generation += 1
		}

		//progenitorImg = img
		for x := 0; x < gifImageSizeInPixels; x++ {
			for y := 0; y < gifImageSizeInPixels; y++ {
				if img.ColorIndexAt(x, y) != blackIndex {
					progenitorImg.SetColorIndex(x, y, img.ColorIndexAt(x, y))
				}
			}
		}

	}

	t := time.Now()
	gifFileName := fmt.Sprintf("brownian_tree_%d_generations_%d_pxls_%s.gif", generations, gifImageSizeInPixels, t.Format(time.RFC3339))
	f, err := os.Create(gifFileName)
	err = gif.EncodeAll(f, &anim)
	if err != nil {
		return
	}

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

	// Red is dead
	//if colorIndexValueAtPosition > whiteIndex && colorIndexValueAtPosition != redIndex {
	if colorIndexValueAtPosition == blueIndex || colorIndexValueAtPosition == greenIndex {
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
