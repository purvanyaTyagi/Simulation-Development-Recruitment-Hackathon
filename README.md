DRIVERLESS RACING TEAM HACKATHON 

1. SLAM 
 Data Association
Problem statement- what i concluded is that robot drives around and builds a map of cones so now the coordinates of cones are saved by the robot when the robot moves again its camera LIDAR system sees con es again and now the sensors are not so perfect and noise is there so now the coordinates they measure are not the same as they have stored there is some error. So the robot asks which cone in my map this is, which means it observes the LIDAR system, then compares it with the stored coordinate, like it observes something and calls it cone A on comparing coordinates. Still, sometimes this gives trouble because the sensor reads very wrong, so it doesn't belong to the mapped cones. But still, the algorithm is careless, and it will still map the observation with some cone, which disturbs the map as the bot will think the position of the cone has changed. So in order to correct it, we add a distance limit or threshold distance if the distance between the coordinate stored and the observation made is greater than a particular 2 or 3m, then we can't call it the same cone. real life comparison we can do by imagine if your friend usually sits next to you in class if you see someone very far away in another building you will not say that is my friend as the distance is too big but the old algorithm will call it as your friend or in short i can which observation corresponds to which landmark on map this is important in SLAM if we make wrong landmarks match then wrong map wrong robot position SLAM fails. So in our solution, it will just check if the distance is less than the threshold, and it will say it's the same cone; otherwise, it is a new cone 

Data association - a step to decide whether this is a new cone or if it's the same cone I already saw


Localisation
What I understood about the localisation function is that it tells the bot where it is on the map. So the old algorithm basically uses a model that is simple dead reckoning to get the coordinate of the bot like we know the old coordinate new is just the old coordinate + velocity*sintheta or velocity*costheta depends on which coordinate we are talking about x or y multiplied by t . this give the coordinate oof bot at any instant issue in this model is that it assumes the bot travels in straight lines, which is not the case; vehicles move in curves. So basically, the baseline model takes the starting point direction and does all calculations based on it. We will take the midpoint direction and do all calculations based on it, which will give a better fit straight line and give a better result. So, the straight line with the initial heading and the straight line with the midpoint as heading, the nearest to the actual curve, will be the average heading. This is important because if the robot doesn't know where it is, it can't build a correct map  

Mapping

Mapping tells where the true cone position is as robot sees one cone multiple time so there is noise in each reading and they come close but not exactly same so the algorithm can’t take each reading of a single cone as as new cone so it updates the position of existing cone gradually by a formula new position = old position + gain*(measurement-old_position) this shows map slowly adjusts towards the new positon. This makes the cone position stable rather than jumping here and there. So mapping is important, as if the map is unstable, then robot localisation becomes harder, and slam becomes unreliable .In simplified way i can say this mapping updates landmark positions based on sensor observations. However, sensor measurements contain noise, which can cause landmarks to appear at slightly different positions each time they are observed. To address this, we implemented a landmark update mechanism that gradually adjusts landmark positions using new observations instead of replacing them directly. This acts as a noise filter and produces a more stable and accurate map. 

2. Simulation development
Originally, the code was making an infinite-shaped trajectory. There was no physics involved; the robot was not using any velocity, acceleration, or force concept. So the problem was that the simulation was ignoring physics, so we made a trajectory with a physics-based motion model, and we will use the equation of motion to get x and y as functions of time. This was important because if we ignore physics, then the simulation will run, but in real life, the algorithm may fail and result in not following the trajectory and functioning. We use robot kinematics, numerical integration and physics-based simulation 

3.PPC

Planning 
I modified the python code of planner.py . initially there was no path planning logic . so robot has no idea to drive  and planner job is to generate the driving path .I used midpoint path planning that dividing cones into left and right cones and compute midpoint as waypoint  so this mid point becomes centerline of the track  this is one of the most secure way to plan a path as it is center path driving exactly in mid so keeping equal margin from both side 


Controller
I modified the controller.py . basically the controller function is to convert path into actual driving commands. I implemented two algoritham here that is Pure Pursuit Steering and speed control (PID-like throttle)

Steering algorithm 
This works like car will see a point ahead in the path and then try to reach that point by steering toward it steer = atan(2l sin(alpha) / lookahead) (L = wheel base and alpha = angle to target )

This will produce smooth steering stable path following , simple implementation and widely used in robotics 

Throttle control 
I am implementing proportional speed control . so lets see it work like control system in EE103 we have to maintain target speed error = target_speed - current_speed throttle=kp*error  so if the car is slow it will increase throttle and in case it is too fast then it will reduce throttle or brake . this makes controller keep vehicle speed stable and prevents aggressive steering and follow the planned path 
