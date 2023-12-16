---
title: Rendering and Transformations
article: false
---

## Vector Dot Product Applications

![Dot product applications](/images/hpg-notes/comp5812m/001-vector-dotproduct-applications.png)

## Vector Cross Product

$$\vec{w} = \vec{u} \times \vec{v} =
\begin{bmatrix}
  u_{y}v_{z} - u_{z}v_{y} \\
  u_{z}v_{x} - u_{x}v_{z} \\
  u_{x}v_{y} - u_{y}v_{x} \\
\end{bmatrix}
$$

## Rendering Steps

1. Describe our scene: where each object is.
   - Transformations
   - Homogeneous Coordinates
   - Quaternions
2. Model our camera: what is it able to see?
   - Camera models
3. Model the sensing process: what ends up where?
   - Intersections / Projection: different rendering algorithms
4. Model the light / film interaction: what color is it?
   - Shading

## Coordinate Systems

- OCS is the Object Coordinate System
- WCS is the World Coordinate System
- VCS is the View Coordinate System
- CCS is the Clipping Coordinate System
- NDCS is the Normalized DCS
- DCS is the Device Coordinate System

![Coordinate systems](/images/hpg-notes/comp5812m/001-coordinate-systems-brief.png)

![Changing coordinate systems by applying matrices](/images/hpg-notes/comp5812m/001-coordinate-systems-changing.png)

## Why we need Homogeneous Coordinates?

We have to:

- Represent translation in matrix form
- Apply sequences of transmations efficiently
- Represent perspective in matrix form

And about the cost of transformation, using Homogeneous Coordinates (x, y, z, w) is more efficient than using Cartesian Coordinates (x, y, z).

![Homogeneous Matrix](/images/hpg-notes/comp5812m/001-homogeneous-matrix.png)