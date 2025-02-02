import pygame

def init():
    pygame.init()
    windows = pygame.display.set_mode((400,400)) #set Control Display as 400x400 pixel
 
def getKey(keyName):
    ans = False
    for eve in pygame.event.get(): pass
    keyInput = pygame.key.get_pressed()
    myKey = getattr(pygame, "K_{}".format(keyName))
    if keyInput[myKey]:
        ans = True
    pygame.display.update()
    return ans

def main():
    if getKey("LEFT"):
        print("Left")
    if getKey("RIGHT"):
        print("Right")

if __name__ == '__main__':
    init()
    while True:
        main()