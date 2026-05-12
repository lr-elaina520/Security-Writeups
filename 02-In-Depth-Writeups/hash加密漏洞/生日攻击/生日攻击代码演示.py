import hashlib
import random
import string

def random_string(length=16):
    """生成随机字符串"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def find_md5_collision(max_attempts=10_000_000):
    """
    生日攻击：不断生成随机字符串，将 MD5 哈希值存入字典，
    一旦发现某个哈希值已经存在，就输出碰撞对。
    """
    hash_map = {}
    for i in range(max_attempts):
        # 生成随机字符串
        s = random_string(20)
        md5_hash = hashlib.md5(s.encode()).hexdigest()
        
        if md5_hash in hash_map:
            # 找到碰撞
            s2 = hash_map[md5_hash]
            if s != s2:   # 确保两个字符串不同
                print(f"碰撞成功！")
                print(f"字符串1: {s}")
                print(f"字符串2: {s2}")
                print(f"MD5 值: {md5_hash}")
                return (s, s2)
        else:
            hash_map[md5_hash] = s
        
        if (i+1) % 100000 == 0:
            print(f"已尝试 {i+1} 次，当前字典大小 {len(hash_map)}")
    
    print(f"在 {max_attempts} 次尝试内未找到碰撞。")
    return None

if __name__ == "__main__":
    find_md5_collision(max_attempts=50_000_000)   # 可以调大次数
