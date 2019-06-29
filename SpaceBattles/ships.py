from projectiles import Bullet

class Shuttle(object):
    
    def __init__(self, shipImage, gunImage,bulletImage,gunFlashImage, x, y,piew, angle=0):
        self.shipImage = shipImage
        self.gunImage = gunImage
        self.x = x
        self.y = y
        self.angle = angle
        self.rotateSpeed = 0.05
        self.currentGunOrientation = 0
        self.lastShot = 0
        self.ROF = 500
        self.bullets = []
        self.bulletImage = bulletImage
        self.gunFlashImage = gunFlashImage
        self.currentGunBarrel = 0
        self.shootTimer = 0
        self.fireRate = 40
        self.piew = piew
        
    def update(self):
        pi = radians(360)
        # Move turret
        with pushMatrix():
            translate(self.x,self.y)
            rotate(self.angle)
            image(self.shipImage,self.shipImage.width*0.22, 0)
            mouseangle = atan2(mouseY-self.y,mouseX-self.x)
            newAngle = mouseangle-self.angle
            delta = newAngle - self.currentGunOrientation
            if delta > pi/2:
                delta -= pi
            elif delta < -pi/2:
                delta += pi
            if delta > self.rotateSpeed:
                newAngle = self.currentGunOrientation + self.rotateSpeed
            elif delta < -self.rotateSpeed:
                newAngle = self.currentGunOrientation - self.rotateSpeed
            rotate(newAngle)
            image(self.gunImage,0,0)
            self.currentGunOrientation = newAngle
        # Update bullets
        newbullets = []
        for bullet in self.bullets:
            if not bullet.isDestroyed:
                bullet.update()
                newbullets.append(bullet)
        self.bullets = newbullets
        if self.shootTimer != 0:
            self.shootTimer -= 1
        
        return self.bullets
        
        
    def shoot(self):
        if self.shootTimer == 0:
            # Alternate the gun barrels
            if self.currentGunBarrel == 0:
                # Spawn on the end of the gun barrel
                xb = self.x + self.gunImage.width/2*cos(self.currentGunOrientation) + self.gunImage.height/5*sin(self.currentGunOrientation)
                yb = self.y + self.gunImage.width/2*sin(self.currentGunOrientation) - self.gunImage.height/5*cos(self.currentGunOrientation)
                self.currentGunBarrel = 1
            else:
                xb = self.x + self.gunImage.width/2*cos(self.currentGunOrientation) - self.gunImage.height/5*sin(self.currentGunOrientation)
                yb = self.y + self.gunImage.width/2*sin(self.currentGunOrientation) + self.gunImage.height/5*cos(self.currentGunOrientation)
                self.currentGunBarrel = 0
            # Generate the bullet
            self.bullets.append(Bullet(xb,yb,self.currentGunOrientation,self.bulletImage,self.gunFlashImage))
            self.shootTimer = self.fireRate
            self.piew.play()
