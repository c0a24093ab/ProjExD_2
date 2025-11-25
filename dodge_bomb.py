import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0)
    }
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """""
    引数:こうかとんRectか爆弾Rect
    戻り値:タプル（横方向判定結果, 縦方向判定結果）
    画面内ならTrue, 画面外ならFalse
    """""
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right: #横方向のはみ出し判定
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom: #縦方向のはみ出し判定
        tate = False
    return yoko, tate
 
    
def gameover(screen: pg.Surface) -> None:
    black = pg.Surface((WIDTH, HEIGHT)) #空のSurface
    pg.draw.rect(black, (0, 0, 0), (0, 0, WIDTH, HEIGHT)) #黒で塗りつぶし
    
    black.set_alpha(180) # 透明度を設定
    
    font = pg.font.Font(None, 80)
    txt = font.render("Game Over", True, (255, 255, 255))
    txt_rct = txt.get_rect()
    txt_rct.center = WIDTH / 2, HEIGHT / 2
    black.blit(txt, txt_rct) #"Game Over"の描画

    kk_cry = pg.image.load("fig/8.png")
    kk1_rct = kk_cry.get_rect()
    kk2_rct = kk_cry.get_rect()
    kk1_rct.center = (WIDTH / 2) - 175, HEIGHT / 2
    kk2_rct.center = (WIDTH / 2) + 175, HEIGHT / 2
    black.blit(kk_cry, kk1_rct) #こうかとん泣き顔の描画
    black.blit(kk_cry, kk2_rct) #こうかとん泣き顔の描画
    screen.blit(black, (0, 0)) #Surfaceの描画
    
    pg.display.update()
    time.sleep(5)
    return
    
    
def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20, 20)) #空のSurface
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10) #半径10の赤い円を描画
    bb_img.set_colorkey((0, 0, 0)) #黒い部分を透過
    bb_rct = bb_img.get_rect() #爆弾Rect
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT) #乱数爆弾座標
    vx, vy = +5, +5 #爆弾の横速度, 縦速度
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            if kk_rct.colliderect(bb_rct): #こうかとんRectと爆弾Rectが重なったら
                gameover(screen)
                print("ゲームオーバー")
                return
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        # if key_lst[pg.K_UP]:
        # #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        # #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        # #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        # #     sum_mv[0] += 5
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0] #横方向の移動量
                sum_mv[1] += mv[1] #縦方向の移動量
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True): #画面外なら
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1]) #移動を無かったことにする
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx, vy)
        yoko, tate = check_bound(bb_rct) 
        if not yoko: #横方向にはみ出していたら
            vx *= -1 #横座標反転
        if not tate: #縦方向にはみ出していたら
            vy *= -1 #縦座標反転 
        screen.blit(bb_img, bb_rct) #bb_imgをbb_rctで描画
        if key_lst[pg.K_ESCAPE]:
            gameover(screen)
            return
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
