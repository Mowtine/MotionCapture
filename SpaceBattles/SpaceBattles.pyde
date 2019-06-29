add_library('sound')
from ships import Shuttle
from projectiles import Bullet
import pickle
import math

moveArray = []
pi = radians(360)
aTimer = 0
hsnake = [0 for h in range(21)]

def setup():
    # Setup globals
    global mainShip
    global bulletImage
    global gunFlashImage
    global monster
    global monster1
    global monster2
    global monster1r
    global monster2r
    global explosion
    global explosion3
    global grunt
    global piew
    global reflect
    global windowSize
    global angles
    global shipScale
    global health
    global bg
    size(1000,1000*3//4)
    windowSize = 1000
    imageMode(CENTER)
    
    # Load in images, sounds and process them
    bg = loadImage("desert planet and the derilict.png")
    bg.resize(windowSize*5//4,0)
    bulletImage = loadImage("bullet.png")
    gunFlashImage = loadImage("Gun flash.png")
    ship1 = loadImage("Spaceship 1.png")
    explosion = loadImage("Explosion1.png")
    explosion3 = loadImage("Explosion3.png")
    monster = loadImage("Monster.png")
    monster.resize(150,0)
    monster1 = loadImage("monster1.png")
    monster2 = loadImage("monster2.png")
    monster1r = loadImage("monster1r.png")
    monster2r = loadImage("monster2r.png")
    monster1.resize(70,0)
    monster2.resize(70,0)
    monster1r.resize(70,0)
    monster2r.resize(70,0)
    shipScale = 0.0002*windowSize
    gunFlashImage.resize(int(gunFlashImage.width*shipScale),0)
    bulletImage.resize(int(bulletImage.width*shipScale),0)
    ship1.resize(int(ship1.width*shipScale),0)
    gunFlashImage.resize(int(ship1.width*shipScale),0)
    gun1 = loadImage("Gun1 level 1.png")
    gun1.resize(int(gun1.width*shipScale),0)
    piew = SoundFile(this, "piew.wav")
    mainShip = Shuttle(ship1,gun1,bulletImage,gunFlashImage,100,height/2,piew)
    grunt = SoundFile(this, "grunt.wav")
    reflect = SoundFile(this, "reflect.wav")
    
    # Load in array from Monkey
    with open("positions.txt", "rb") as fp:
        moveArray = pickle.load(fp)
    health = 20
    
    # Process it to a ready-to-use array
    angles = []
    anglePrev = [moveArray[0][4],pi/8,pi/8+pi/4,-pi/8,-pi/8-pi/4]
    for Pos in moveArray:
        if len(Pos) == 5:
            angleOne = []
            angleOne.append(Pos[4])
            angleOne.append(Pos[0])
            angleOne.append(Pos[1])
            angleOne.append(Pos[2])
            angleOne.append(Pos[3])
            
    # This is unused alternate code for hands instead of heads
            # # rLeg angle
            # if Pos[0] == Pos[4]:
            #     angleOne.append(anglePrev[1])
            # else:
            #     angleOne.append(atan2(Pos[0][1]-Pos[4][1],Pos[0][0]-Pos[4][0]))
            # # lLeg angle
            # if Pos[1] == Pos[4]:
            #     angleOne.append(anglePrev[2])
            # else:
            #     angleOne.append(atan2(Pos[1][1]-Pos[4][1],Pos[1][0]-Pos[4][0]))
            # # rHand angle        
            # if Pos[0] == Pos[4]:
            #     angleOne.append(anglePrev[3])
            # else:
            #     angleOne.append(atan2(Pos[2][1]-Pos[4][1],Pos[2][0]-Pos[4][0]))
            # # lHand angle
            # if Pos[0] == Pos[4]:
            #     angleOne.append(anglePrev[4])
            # else:
            #     angleOne.append(atan2(Pos[3][1]-Pos[4][1],Pos[3][0]-Pos[4][0]))
                        
            anglePrev = angleOne
            angles.append(angleOne)
    
def draw(): 
    global aTimer
    global health
    global hsnake
    
    # set BG
    image(bg,windowSize//2,windowSize*3//8)
    
    # Updates
    bulletList = mainShip.update()
    marionet(windowSize*2//3-200, windowSize*3//8-100, bulletList)
    
    # Draw health snake who snakes according to y movement of puppet
    hsnake[health] = angles[aTimer][0][1]
    if health == 0:
        exit()
    else:
        for i in range(health):
            ellipse(100+i*40+random(-5,5),100+random(-5,5)+hsnake[i]//2,50,50)
            hsnake[i] = hsnake[i+1]
            
    # Re-set animation if needed
    aTimer += 1
    if aTimer >= len(angles):
        aTimer = 0
    
    # Shoot!
    if mousePressed and mouseButton == LEFT:
        mainShip.shoot()
    
def marionet(x, y, bullets):
    global health
    # Find body center
    xbody = x + angles[aTimer][0][0]
    ybody = y + angles[aTimer][0][1]
    image(monster,xbody,ybody)
    fill(51,153,0)
    
    # Draw hands/heads
    with pushMatrix():
        translate(x + angles[aTimer][1][0],y + angles[aTimer][1][1])
        #ellipse(0,0,50,50)
        image(monster1,0,0)
    with pushMatrix():
        translate(x + angles[aTimer][2][0],y + angles[aTimer][2][1])
        #ellipse(0,0,50,50)
        image(monster1r,0,0)
    with pushMatrix():
        translate(x + angles[aTimer][3][0],y + angles[aTimer][3][1])
        #ellipse(0,0,50,50)
        image(monster2,0,0)
    with pushMatrix():
        translate(x + angles[aTimer][4][0],y + angles[aTimer][4][1])
        #ellipse(0,0,50,50)
        image(monster2r,0,0)
    newbul = None
    for bullet in bullets:
        if math.sqrt((bullet.x-(x + angles[aTimer][1][0]))**2+(bullet.y-(y + angles[aTimer][1][1]))**2) < 60:
            bullet.isDestroyed = True
            image(explosion,bullet.x,bullet.y)
            reflect.play()
            newbul = Bullet(bullet.x, bullet.y,random(pi/4,pi*3/4),bulletImage,gunFlashImage)
            newbul.update
        elif math.sqrt((bullet.x-(x + angles[aTimer][2][0]))**2+(bullet.y-(y + angles[aTimer][2][1]))**2) < 60:
            bullet.isDestroyed = True
            image(explosion,bullet.x,bullet.y)
            reflect.play()
            newbul = Bullet(bullet.x, bullet.y,random(pi/4,pi*3/4),bulletImage,gunFlashImage)
            newbul.update
        elif math.sqrt((bullet.x-(x + angles[aTimer][3][0]))**2+(bullet.y-(y + angles[aTimer][3][1]))**2) < 60:
            bullet.isDestroyed = True
            image(explosion,bullet.x,bullet.y)
            reflect.play()
            newbul = Bullet(bullet.x, bullet.y,random(pi/4,pi*3/4),bulletImage,gunFlashImage)
            newbul.update
        elif math.sqrt((bullet.x-(x + angles[aTimer][4][0]))**2+(bullet.y-(y + angles[aTimer][4][1]))**2) < 60:
            bullet.isDestroyed = True
            image(explosion,bullet.x,bullet.y)
            reflect.play()
            newbul = Bullet(bullet.x, bullet.y,random(pi/4,pi*3/4),bulletImage,gunFlashImage)
            newbul.update
        elif math.sqrt((bullet.x-(x + angles[aTimer][0][0]))**2+(bullet.y-(y + angles[aTimer][0][1]))**2) < monster.width*2//3:
            bullet.isDestroyed = True
            image(explosion3,bullet.x,bullet.y)
            grunt.play()
            health -= 1
    
    # Save the reflected bullet
    if newbul != None:
        bullets.append(newbul)
        
    # with pushMatrix():
    #     translate(xbody,ybody)
    #     rotate(angles[aTimer][1])
    #     translate(100,0)
    #     ellipse(0,0,50,50)
    # with pushMatrix():
    #     translate(xbody,ybody)
    #     rotate(angles[aTimer][2])
    #     translate(100,0)
    #     ellipse(0,0,50,50)
    # with pushMatrix():
    #     translate(xbody,ybody)
    #     rotate(angles[aTimer][3])
    #     translate(100,0)
    #     ellipse(0,0,50,50)
    # with pushMatrix():
    #     translate(xbody,ybody)
    #     rotate(angles[aTimer][4])
    #     translate(100,0)
    #     ellipse(0,0,50,50)
    
    
