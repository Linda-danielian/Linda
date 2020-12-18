import pygame, random, sys
from pygame.locals import *

WINDOWWIDTH = 1500
WINDOWHEIGHT = 800
TEXTCOLOR = (0, 0, 0)
BACKGROUNDCOLOR = (255, 255, 255)
FPS = 60
ENEMY_MIN_SIZE = 10 #минимальное значение вариативного размера врага (пиксели)
ENEMY_MAX_SIZE = 40 #максимальное значение вариативного размера врага (пиксели)
ENEMY_MIN_SPEED = 1 #минимальное значение вариативной скорости врага (пиксели на итерацию)
ENEMY_MAX_SPEED = 8 #максимальное значение вариативной скорости врага (пиксели на итерацию)
ADD_ENEMY_PERIOD = 6 #период появления врагов (итерации)
MOUSE_MOVE_PIX = 5 #перемещение игрока на каждую итерацию (пиксели)

def close(): #процедура завершения процесса
    pygame.quit()
    sys.exit()

def key_screen(): #бесконечный цикл который прерывается клавишей, нужен для экрана с ожиданием ввода клавиш
    while True:
        for event in pygame.event.get():
            if event.type == QUIT: #если пользователь закрыл окно
                close()
            if event.type == KEYDOWN: #выход из цикла при нажатии на клавишу
                if event.key == K_ESCAPE: #инициация процедуры выхода при нажатии ESC
                    close()
                return

def player_enemy_contact(playerRect, enemies): #факт столкновения игрока с врагом, булево значение
    for b in enemies: #проходим всех врагов и проверяем факт касания c использованием класса rect и метода colliderect (сильно проще, чем считать столкновения руками)
        if playerRect.colliderect(b['rect']):
            return True
    return False

def drawText(text, font, surface, x, y): #вывод текста
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

pygame.init()
clock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Грантовик') #подпись окошка
pygame.mouse.set_visible(False) #скрываем курсор

font = pygame.font.SysFont(None, 48) #шрифты

gameOverSound = pygame.mixer.Sound('fail.wav') #установка звука проигрыша
pygame.mixer.music.load('music.mp3') #установка звука в процессе игры

player_skin = pygame.image.load('player.png') #скин игрока
playerRect = player_skin.get_rect()
enemy_skin = pygame.image.load('enemy.png') #скин врага

windowSurface.fill(BACKGROUNDCOLOR) #начальный экран и надписи на нем
drawText('Грантовик', font, windowSurface, (WINDOWWIDTH / 3)-300,
       (WINDOWHEIGHT / 4))
drawText('Испытай судьбу на физтехе', font, windowSurface,
       (WINDOWWIDTH / 3) - 300, (WINDOWHEIGHT / 3) + 150)
drawText('с грантовой программой от ФБМФ.', font, windowSurface,
       (WINDOWWIDTH / 3) - 300, (WINDOWHEIGHT / 3) + 200)
drawText('Нажми любую клавишу', font, windowSurface,
       (WINDOWWIDTH / 2) - 300, (WINDOWHEIGHT / 3) + 400)
pygame.display.update()
key_screen()

topScore = 0 #максимальный балл
while True: #этот цикл нужен чтобы отображать окно, пока игра не завершена
    enemies = [] #cписок врагов
    score = 0
    playerRect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 50) #начальное положение игрока
    moveLeft = moveRight = moveUp = moveDown = False
    reverseCheat = slowCheat = False
    enemyAddCounter = 0
    pygame.mixer.music.play(-1, 0.0) #вызываем диджея, включаем музыку

    while True: #игровой цикл
        score += 1 #счетчик очков

        for event in pygame.event.get():
            if event.type == QUIT:
                close()

            if event.type == KEYDOWN:
                if event.key == K_LEFT or event.key == K_a:
                    moveRight = False
                    moveLeft = True
                if event.key == K_RIGHT or event.key == K_d:
                    moveLeft = False
                    moveRight = True
                if event.key == K_UP or event.key == K_w:
                    moveDown = False
                    moveUp = True
                if event.key == K_DOWN or event.key == K_s:
                    moveUp = False
                    moveDown = True

            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    close()

                if event.key == K_LEFT or event.key == K_a:
                    moveLeft = False
                if event.key == K_RIGHT or event.key == K_d:
                    moveRight = False
                if event.key == K_UP or event.key == K_w:
                    moveUp = False
                if event.key == K_DOWN or event.key == K_s:
                    moveDown = False

            if event.type == MOUSEMOTION: #движения мыши
                playerRect.centerx = event.pos[0]
                playerRect.centery = event.pos[1]
        enemyAddCounter += 1 #добавляем новых врагов
        if enemyAddCounter == ADD_ENEMY_PERIOD: 
            enemyAddCounter = 0
            enemiesize = random.randint(ENEMY_MIN_SIZE, ENEMY_MAX_SIZE)
            newenemy = {'rect': pygame.Rect(random.randint(0,
                                WINDOWWIDTH - enemiesize), 0 - enemiesize,
                                enemiesize, enemiesize),
                         'speed': random.randint(ENEMY_MIN_SPEED,
                                ENEMY_MAX_SPEED),
                         'surface':pygame.transform.scale(enemy_skin,
                                (enemiesize, enemiesize)),
                        }

            enemies.append(newenemy)

        if moveLeft and playerRect.left > 0: #движения игрока
            playerRect.move_ip(-1 * MOUSE_MOVE_PIX, 0)
        if moveRight and playerRect.right < WINDOWWIDTH:
            playerRect.move_ip(MOUSE_MOVE_PIX, 0)
        if moveUp and playerRect.top > 0:
            playerRect.move_ip(0, -1 * MOUSE_MOVE_PIX)
        if moveDown and playerRect.bottom < WINDOWHEIGHT:
            playerRect.move_ip(0, MOUSE_MOVE_PIX)

        for b in enemies: #движения врагов
            b['rect'].move_ip(0, b['speed'])

        for b in enemies[:]: #избавляемся от врагов, ушедших за нижний край
            if b['rect'].top > WINDOWHEIGHT:
                enemies.remove(b)

        windowSurface.fill(BACKGROUNDCOLOR) #чистим экран после каждой итерации

        drawText('Score: %s' % (score), font, windowSurface, 10, 0) #рисуем счет
        drawText('Top Score: %s' % (topScore), font, windowSurface,
               10, 40) #лучший счет за партию

        windowSurface.blit(player_skin, playerRect) #рисуем игрока

        for b in enemies: #рисуем врагов
            windowSurface.blit(b['surface'], b['rect'])

        pygame.display.update()

        if player_enemy_contact(playerRect, enemies): #условия поражения и проверка, выше ли счет лучшего счета
            if score > topScore:
                topScore = score
            break

        clock.tick(FPS)

    pygame.mixer.music.stop() #выключаем музыку, если игра проиграна (завершение цикла через break)
    gameOverSound.play() #музыка для проигравших

    drawText('Попрощайся с грантом', font, windowSurface, (WINDOWWIDTH / 3), #текст для проигравших
           (WINDOWHEIGHT / 3))
    drawText('или', font, windowSurface, (WINDOWWIDTH / 3),
           (WINDOWHEIGHT / 3) + 100)
    drawText('Нажми на кнопку чтобы выпросить еще семестр', font, windowSurface,
           (WINDOWWIDTH / 3) - 80, (WINDOWHEIGHT / 3) + 200)
    pygame.display.update()
    key_screen()

    gameOverSound.stop()



