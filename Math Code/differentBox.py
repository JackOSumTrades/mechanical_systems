import numpy as np

num_known = 11
known_weight = 5
otherBoxWeight = 7

boxes = np.full(num_known, 5)
boxes=np.append(boxes,otherBoxWeight)
np.random.shuffle(boxes)
# print(boxes)


boxFound = False
i =0
while not boxFound:
    
    if len(boxes)%2 != 0:
        
        randomBoxIdx2Remove = np.random.randint(0,len(boxes))
        randomBox = boxes[randomBoxIdx2Remove]
        boxes = np.delete(boxes,randomBoxIdx2Remove)
        
        leftBoxes = boxes[0: int(len(boxes)/2)]
        leftScale = sum(leftBoxes)
        
        rightBoxes = boxes[int(len(boxes)/2): len(boxes)]
        rightScale= sum(rightBoxes)
        
        
        
        
        if rightScale == leftScale:
            boxFound = True
            boxes = randomBox
            
        elif rightScale > leftScale:
            boxes = rightBoxes
        else:
            boxes = leftBoxes
            

    
    else:
        leftBoxes = boxes[0: int(len(boxes)/2)]
        leftScale = sum(leftBoxes)
        
        rightBoxes = boxes[int(len(boxes)/2): len(boxes)]
        rightScale= sum(rightBoxes)
        # print(boxes, leftScale, rightScale)
        
        if len(leftBoxes) == 1:
            boxFound = True
            
        if rightScale > leftScale:
            boxes = rightBoxes
        else:
            boxes = leftBoxes
            
    i +=1
        
print( "The different box was found in %d iterations (the weight was %d but would not be known using a real scale)" % (i, boxes))    