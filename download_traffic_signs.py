#!/usr/bin/env python3
"""
下載香港運輸署交通標誌圖片
"""
import urllib.request
import os
import time

# 常見的香港交通標誌（基於運輸署官方標誌）
# 使用公開的交通標誌資源
traffic_signs = {
    # 禁制標誌 (Regulatory Signs)
    "no_entry": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b0/Vienna_Convention_road_sign_C1.svg/200px-Vienna_Convention_road_sign_C1.svg.png",
    "no_vehicles": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/29/Vienna_Convention_road_sign_C3a.svg/200px-Vienna_Convention_road_sign_C3a.svg.png",
    "no_left_turn": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e8/Vienna_Convention_road_sign_C13a.svg/200px-Vienna_Convention_road_sign_C13a.svg.png",
    "no_right_turn": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Vienna_Convention_road_sign_C13b.svg/200px-Vienna_Convention_road_sign_C13b.svg.png",
    "no_u_turn": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/Vienna_Convention_road_sign_C13c.svg/200px-Vienna_Convention_road_sign_C13c.svg.png",
    "no_overtaking": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/Vienna_Convention_road_sign_C11a.svg/200px-Vienna_Convention_road_sign_C11a.svg.png",
    "no_parking": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ed/Vienna_Convention_road_sign_C18.svg/200px-Vienna_Convention_road_sign_C18.svg.png",
    "no_stopping": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/00/Vienna_Convention_road_sign_C19.svg/200px-Vienna_Convention_road_sign_C19.svg.png",
    "stop": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f9/Vienna_Convention_road_sign_B2a.svg/200px-Vienna_Convention_road_sign_B2a.svg.png",
    "yield": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c8/Vienna_Convention_road_sign_B1.svg/200px-Vienna_Convention_road_sign_B1.svg.png",
    
    # 速度限制 (Speed Limits)
    "speed_limit_50": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/92/Vienna_Convention_road_sign_C14-V50.svg/200px-Vienna_Convention_road_sign_C14-V50.svg.png",
    "speed_limit_70": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f4/Vienna_Convention_road_sign_C14-V70.svg/200px-Vienna_Convention_road_sign_C14-V70.svg.png",
    
    # 警告標誌 (Warning Signs)
    "warning_curve_left": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ea/Vienna_Convention_road_sign_Aa%2C2a-left.svg/200px-Vienna_Convention_road_sign_Aa%2C2a-left.svg.png",
    "warning_curve_right": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1c/Vienna_Convention_road_sign_Aa%2C2a-right.svg/200px-Vienna_Convention_road_sign_Aa%2C2a-right.svg.png",
    "warning_junction": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Vienna_Convention_road_sign_Aa%2C10a-left.svg/200px-Vienna_Convention_road_sign_Aa%2C10a-left.svg.png",
    "warning_pedestrian": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/58/Vienna_Convention_road_sign_Aa%2C11a.svg/200px-Vienna_Convention_road_sign_Aa%2C11a.svg.png",
    "warning_children": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f4/Vienna_Convention_road_sign_Aa%2C11b.svg/200px-Vienna_Convention_road_sign_Aa%2C11b.svg.png",
    "warning_traffic_light": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b7/Vienna_Convention_road_sign_Aa%2C12.svg/200px-Vienna_Convention_road_sign_Aa%2C12.svg.png",
    "warning_slippery": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Vienna_Convention_road_sign_Aa%2C13.svg/200px-Vienna_Convention_road_sign_Aa%2C13.svg.png",
    
    # 指示標誌 (Information Signs)
    "one_way": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/54/Vienna_Convention_road_sign_D1a.svg/200px-Vienna_Convention_road_sign_D1a.svg.png",
    "parking": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Vienna_Convention_road_sign_E%2C5a.svg/200px-Vienna_Convention_road_sign_E%2C5a.svg.png",
    "hospital": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8c/Vienna_Convention_road_sign_F2.svg/200px-Vienna_Convention_road_sign_F2.svg.png",
}

def download_sign(name, url, output_dir="images/signs"):
    """下載單個交通標誌"""
    try:
        output_path = os.path.join(output_dir, f"{name}.png")
        
        # 檢查文件是否已存在
        if os.path.exists(output_path):
            print(f"⏭️  {name}.png 已存在，跳過")
            return True
        
        print(f"📥 下載 {name}...")
        
        # 設置 User-Agent 避免被封鎖
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'}
        req = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(req, timeout=10) as response:
            data = response.read()
            with open(output_path, 'wb') as f:
                f.write(data)
        
        print(f"✅ {name}.png 下載成功")
        time.sleep(0.5)  # 避免請求過快
        return True
        
    except Exception as e:
        print(f"❌ {name} 下載失敗: {e}")
        return False

def main():
    output_dir = "images/signs"
    os.makedirs(output_dir, exist_ok=True)
    
    print("🚦 開始下載香港交通標誌...")
    print(f"📁 輸出目錄: {output_dir}\n")
    
    success_count = 0
    fail_count = 0
    
    for name, url in traffic_signs.items():
        if download_sign(name, url, output_dir):
            success_count += 1
        else:
            fail_count += 1
    
    print(f"\n📊 下載完成:")
    print(f"   ✅ 成功: {success_count}")
    print(f"   ❌ 失敗: {fail_count}")
    print(f"   📁 位置: {output_dir}/")

if __name__ == "__main__":
    main()
