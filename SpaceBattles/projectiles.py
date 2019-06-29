
class Bullet(object):
    
    def __init__(self,x,y,angle,bulletImage,gunFlashImage):
        self.x = x
        self.y = y
        self.angle = angle
        self.bulletImage = bulletImage
        self.gunFlashImage = gunFlashImage
        self.isDestroyed = False
        # Create initial bullet and muzzle flash
        with pushMatrix():
            translate(self.x,self.y)
            rotate(self.angle)
            image(self.bulletImage,self.bulletImage.width/2, 0)
            image(self.gunFlashImage,self.gunFlashImage.width/2, 0)
        
    def update(self):
        
        # Move the bullet forward random distance
        distanceChange = random(10,30)
        self.x += distanceChange*cos(self.angle)
        self.y += distanceChange*sin(self.angle)
        with pushMatrix():
            translate(self.x,self.y)
            rotate(self.angle)
            image(self.bulletImage,0,0)
        
