# game/constants.py

BOTTOM_Y = 490

# 一開始設為 None，延遲載入
smoke_images = None
electric_images = None
gas_images = None
physic_images = None
csmoke_images1 = None
csmoke_images2 = None

def init_effect_images():
    """
    在遊戲開始後（pygame.display.set_mode 已呼叫）呼叫此函數來載入所有特效圖片
    這樣可以避免 pygame.display not initialized 的錯誤
    """
    global smoke_images, electric_images, gas_images, physic_images, csmoke_images1, csmoke_images2
    
    from .load_images import (
        load_smoke_images,
        load_electric_images,
        load_gas_images,
        load_physic_images,
        load_csmoke_images
    )
    
    smoke_images = load_smoke_images()
    electric_images = load_electric_images()
    gas_images = load_gas_images()
    physic_images = load_physic_images()
    csmoke_images1, csmoke_images2 = load_csmoke_images()

    print("所有特效圖片載入完成")