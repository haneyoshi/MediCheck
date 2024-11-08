import numpy as np

def simulate_enhancement(initial_level, target_level, num_simulations=1000):
    success_count = 0

    for _ in range(num_simulations):
        current_level = initial_level

        while current_level < target_level:
            # 判斷是否是 15>16 的階段，以及對應的機率
            if current_level == 15 and np.random.rand() > 0.3:
                current_level -= 1
            else:
                # 普通的強化階段
                success_prob = 0.3 if current_level >= 16 else 0.7
                if np.random.rand() < success_prob:
                    current_level += 1
                else:
                    if current_level == 22:
                        break  # 已經是最高等級，結束循環
                    elif current_level == 21 and np.random.rand() < 0.35:
                        break  # 21>22 失敗但不下滑，結束循環
                    else:
                        current_level -= 1

        if current_level == target_level:
            success_count += 1

    success_rate = success_count / num_simulations
    return success_rate

# 模擬從等級 18 到等級 22 的成功機率
initial_level = 18
target_level = 22
success_rate = simulate_enhancement(initial_level, target_level)

print(f"模擬 {num_simulations} 次，成功升級到等級 {target_level} 的機率為: {success_rate * 100:.2f}%")
