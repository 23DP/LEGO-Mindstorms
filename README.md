# LEGO-Mindstorms
My part of the projest for RealTimeControlAlgorithms course 

Theme: Veljko is the name of the robot, that will play the role of the parking lot officer. When he receives the signal that a new
car parked, he will wait for some time, and take a tour to check if the driver had paid the parking.
To do this, he has to follow a line on the lot, and stop when he reaches the car (he will have a sensor on the parking spot, that
is how he will know where to stop). After that, he should return to his starting point, and wait until he recieves another signal

Since we only have one robot, thus one color sensor, Veljko will follow the edge of the line, using the reflection mode on the color 
sensor. When he is standing half on the line, and hald on the free surface, the reflection should be, theoretically, 50%. Of course, this 
depends on the material of the groundwork, so it should be measured experimentally. 
