---
title: Raster Images
author: Lazy_V
date: 2023-04-05 15:55:00
category:
  - GameEngineDev
tag:
  - GameEngineDev
  - ComputerGraphics
  - Theory
  - Images
isOriginal: true
---

## Images

There are two popular types of images:

- Raster images
- Vector images

A raster image stores a 2D rectangular array of pixels, while a vector image stores some points and their paths.

For example, a JPEG format image file is a raster image, a SVG format image file is a vector image.

::: info
Here are some popular formats of raster images:
- PNG
  
  Lossless format with a good set of open source management tools.
- JPEG
  
  Lossy format that works well for natural images.
- TIFF
  
  Hold binary images or losslessly compressed 8- or 16-bit RGB although many other options exist.
:::

In Computer Graphics, we usually focus on raster images rather than vector images. This is due to the fact that we widely use a technique named **Rasterization** for rendering.

## Raster Devices

Output:

- Display
  - Transmissive: liquid crystal display (LCD)
  - Emissive: light-emitting diode (LED) display

- Hardcopy
  - Binary: ink-jet printer
  - Continuous tone: dye sublimation printer

Input:

- 2D array sensor: digital camera
- 1D array sensor: flatbed scanner

### Displays

Emissive displays: Using pixels that directly emit controllable amounts of light.

Transmissive displays: Pixels don't emit light but instead vary the amount of light that they allow to pass through them. They require a light source to illuminate them.

**LED** displays are an example of the emissive type. Each pixel is composed of one or more LEDs, which are semiconductor devices that emit light with intensity depending on the electrical current passing through them.

![The operation of a light-emitting diode (LED) display.](/images/game-engine-dev/basic-theories/LED1.png)

The pixels in a color display are divided into three independently controlled subpixels--one red, one green, and one blue--each with its own LED made using different materials so that they emit light of different colors.

![The red, green, and blue subpixels within a pixel of a flat-panel display.](/images/game-engine-dev/basic-theories/subpixels.png)

**LCD**s are an example of the transmissive type. A liquid crystal is a material whose molecular structure enables it to rotate the polarization of light that passed through it, and the degree of rotation can be adjusted by an applied voltage.

![The operation of a liquid crystal display (LCD).](/images/game-engine-dev/basic-theories/LCD1.png)

![One pixel of an LCD in the off state (bottom), in which the front polarizer blocks all the light that passes the back polarizer, and the on state (top), in which the liquid crystal cell rotates the polarization of the light so that it can pass through the front polarizer.](/images/game-engine-dev/basic-theories/LCD2.png)

### Hardcopy Devices

Printers are raster devices like displays, but many printers can only print binary images--pigment is either deposited or not at each grid position, with no intermediate amounts possible.

An **ink-jet printer** is an example of a device that forms a raster image by scanning. It has no physical array of pixels; the resolution is determined by how small the drops can be made and how far the paper is advanced after each sweep.

![The operation of an ink-jet printer](/images/game-engine-dev/basic-theories/ink-jet-printer.png)

The **thermal dye transfer** process is an example of a continuous tone printing process, meaning that varying amounts of dye can be deposited at each pixel--it is not all-or-noting like an ink-jet printer.

![The operation of a thermal dye transfer printer](/images/game-engine-dev/basic-theories/thermal-dye-transfer-printer.png)

### Input Devices

A **digital camera** is an example of a 2D array input device. The image sensor in a camera is a semiconductor device with a grid of light-sensitive pixels.

![The operation of a digital camera.](/images/game-engine-dev/basic-theories/digital-camera.png)

- CCD (charge-coupled devices)
- CMOS (complimentary metal-oxide-semiconductor)

In much the same way as color displays use red, green and blue subpixels, most color cameras work by using a color-filter array or mosaic to allow each pixel to see only red, green or blue light, leaving the image processing software to fill in the missing values in a process known as demosaicking.

![Most color digital cameras use a color-filter array. Each pixel measures either red, green or blue light.](/images/game-engine-dev/basic-theories/color-filter-array.png)

A **flatbed scanner** also measures red, green, and blue values for each of a grid of pixels, but like a thermal dye transfer printer, it uses a 1D array that sweeps across the page being scanned, making many measurements per second.

![The operation of a flatbed scanner.](/images/game-engine-dev/basic-theories/flatbed-scanner.png)