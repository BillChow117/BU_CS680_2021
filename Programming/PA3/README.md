# Programming Assignment 03: 3D Vivarium


## 1. Overview

The purpose of the assignment is to introduce you to OpenGL animation for hierarchical modeling, and collision detection. You will program a 3-D vivarium: a simulated 3-D world with polyhedral creatures moving around.


### Basic Requirements


1. **Predator/Prey Models:** To build your vivarium, you will first need to construct two different creatures using polyhedral (solid) parts. Implement your code as we did at "TODO 1" in the _ModelLinkage_ file.
    * For the basic parts of your creatures, feel free to use routines provided with the previous assignment. You are also free to create your own basic parts, but they must be polyhedral (solid).
    * The creatures you design should have moving linkages of the basic parts: legs, arms, wings, antennae, fins, tentacles, etc. 
    * Model requirements:
        1. Predator: At least one (1) creature. Should have at least two moving parts in addition to the main body
        2. Prey: At least two (2) creatures. The two prey can be instances of the same design. Should have at least one moving part.
        3. The predator and prey should have distinguishable different colors. You are welcome to reuse your PA2 creature in this assignment. 
2. **Model animation:** Use transforms to control the motion of each creature and its parts. Implement your code like what we did at "TODO 2" in the _ModelLinkage_ file _animationUpdate_ method.
    * Set reasonable joints limit for your creature
    * The linkages should move back and forth in a periodic motion, as the creatures move about the vivarium. 
    * Your creatures should be able to move in 3 dimensions, not only on a plane. 
3. **Collision Detection & Reaction:** Creatures in the vivarium should react to where other creatures are and move accordingly. Implement your code at "TODO 3" in the _ModelLinkage_ file _animationUpdate_ method.
    * Your creature should always stay within the fixed-size 3D "tank". You should do collision detection between the creatures and tank walls. When creatures hit the tank walls, they should turn and change direction to stay within the tank.
    * Your creatures should have a prey/predator relationship. For example, you could have a bug being chased by a spider, or a fish eluding a shark. This means your creature should react to other creatures in the tank:
        * Use potential functions to change its direction based on other creatures’ location, their inter-creature distances, and their current configuration.
        * You should detect collisions between creatures. 
            1. Predator-prey collision: The prey should disappear (get eaten) from the tank.
            2. Collision between the same species: They should bounce apart from each other. You can use a reflection vector about a plane to decide the after-collision direction.
        * You are welcome to use bounding spheres for collision detection.
4. **Creature orientation:** Creatures should face in the direction they are moving. For instance, a fish should be facing the direction in which it swims. Remember that we require your creatures to be movable in 3 dimensions, so they should be able to face any direction in 3D space. Implement your code at "TODO 4" in the _ModelLinkage_ file _animationUpdate_ method.


### Extra Credits (You may only receive up to 10 extra credits)


5. **(Required for CS680 Students)** **Feed your creatures with food:** Add chunks of food to the vivarium which can be eaten by your creatures. Implement your code at "BONUS 5(TODO 5)" in the _Vivarium_ file. 
    * When ‘f’ is pressed, have a food particle be generated at random within the vivarium. 
    * Be sure to draw the food on the screen with an additional model. It should drop slowly to the bottom of the vivarium and remain there within the tank until eaten.
    * The food should disappear once it has been eaten. Food is eaten by the first creature that touches it.
6. **Flocking behavior:** Add at least 5 creatures to the vivarium and make it possible for creatures to engage in group behaviors, for instance flocking together. This can be achieved by implementing the [Boids animation algorithms](http://www.red3d.com/cwr/boids/) of Craig Reynolds. Implement your code at "BONUS 6" in the _ModelLinakge_ file.


### Programming Style



7. For any modified or newly added source file, you should include a brief explanation about what you did in this file at the file heading and add your name to the author list. Your code should be readable with sufficient comments. You should use consistent variable naming and keep reasonable indentation. In python, we prefer to use reStructuredText format docstring, for more details about this format, please check **[here](https://devguide.python.org/documenting/)**.


## 2. Resources


### 2.1 Start code

A Python Program skeleton, which includes basic classes, methods, and main pipeline, is provided for you. You are expected to complete the parts marked with TODO. There are comments in the skeleton code that will help guide you in writing your own subroutines.


### 2.2 Environment Setup

Installing the appropriate programming environment should be covered in a lab session. For more step-by-step instructions, please check the environment set up on Blackboard.


### 2.3 User Interface

The user interface to the program is provided through mouse buttons and keyboard keys. 

**R/r**: Reset everything in the Vivarium (including put eaten creatures back) \
**F/f:** Add food

You can set key bindings to add creatures to the Vivarium. 


### 2.4 Video Demo

We prepared a video demo for you, hope this can help you better understand your tasks and speed up your debugging process. Please check it on the Blackboard.


## 3. Submission (due by midnight, Tuesday, 11/9)


### 3.1 Source Code

Your program's source files are to be submitted electronically on Gradescope. The code you submit should conform to the program assignment guidelines.


### 3.2 Demo

Part of your grade for this programming assignment will be based on your giving a short demo (5 minutes) during the CS480/680 scheduled labs following the assignment due date. You will be expected to talk about how your program works.


## 4. Grading

| Requirements                                                          | CS680 Credits |
| :-------------------------------------------------------------------- | :------------ |
| Produce predator & prey with moving parts                             | 20            |
| Creatures face in direction they are moving                           | 25            |
| Collision detection and creatures react to each other                 | 20            |
| Creatures stay inside the tank as described above                     | 15            |
| Food can be added, creatures find and eat the food as described above | 10            |
| Group behavior modeling                                               | 10(extra)     |
| Programming Style                                                     | 10            |



## 5. Code Distribution Policy

You acknowledge this code is only for the course learning purpose. You should never distribute any part of this assignment, especially the completed version, to any publicly accessible website or open repository without our permission. Keeping the code in your local computer or private repository is allowed. You should never share, sell, gift, or copy the code in any format with any other person without our permission.
