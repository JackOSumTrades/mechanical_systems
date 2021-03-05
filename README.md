# mechanical_systems

This is a repository containing several mechanical simulations I create(d)

## Contents - mechanical_systems

- drawNodeSphere,py
  - This is my Graph implementation of a sphere made of nodes
  - This contains a simple graph of points, the drawing of edges, and the drawing of planes to simulate a surface
  - Please note: This implementation currently has difficulty drawing some surface planes 
     - This error has been identified as the use of the Quad (4 node plane) object to connect 3 nodes together
     - This error will soon be fixed
- moonAroundEarth.py
  - This is a very simple implementation of orbiting bodies due to gravitational effects
  - A more advanced version is in the montecarlo folder
- bounceBall.py
  - This contains a simple implementation of gravitational effects and simplified energy loss 
- ballCollision.py
  - This contains a very simple linear, elastic momentum simulation as well as collision detection
- collision.py
  - This contains my very first implementation of VPython -> Just a 3D representation of a 2D plane
- twoDimensionCantilever.py
  - This is an unstarted file for my implementation of 2D FEA 
 
## Contents - mechanical_systems/Math Code
This is some implementation of integration mathods and will be further populated with mathematical functions after 5/15/21
Some functions that will be made public are:
  - Integration (Gaussian:finite/infinite, adaptive trapezoidal, romberg)
  - Derivatives (central difference)
  - Several simple math problems (binomial coefficient generation, catalan number generation, prime number generation, etc)
  - Plotting of curves (deltoid, feigenbaum plots)
  - Smoothing functions (running average, least squares)
  - Algorithms (QR Algorithm)
  - Functions (Debye Temperature, Quantum potential step, madelung constant, stefan-boltzman constant, Gravitational pull on uniform sheet, Gamma Function, Electric field of a charge distribution)
  - 
## Future Implementation Plans:
  - Implement a 2D stress FEA analysis 
  - Implement a 3D stress FEA analysis
  - Implement an fea version of a bouncing/rolling ball

  - Implement a representation of earth as a collection of particles  (an object) 
    - 	Simulate the Moon Formation via Asteroid impact theory by simulating both the Earth and the Asteroid as a collection of particles

		
#### Please Note: The majority of these programs are for proof-of-concept purposes and are in need of more commentation 
