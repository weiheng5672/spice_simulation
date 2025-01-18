####################################################################################################

#r# =============================
#r#  電壓與電流分壓器
#r# =============================

#r# 此電路是電子學中的基礎區塊，允許使用阻抗比來縮放電壓：

#f# circuit_macros('voltage-divider.m4') # 引入電壓分壓器電路的圖形表示

#r# 輸入電壓與輸出電壓之間的關係為：
#r#
#r# .. math::
#r#
#r#     \frac{V_{out}}{V_{in}} = \frac{R_2}{R_1 + R_2}
#r#
#r# 此公式適用於各種阻抗元件，如電阻、電容和電感等。

####################################################################################################

import PySpice.Logging.Logging as Logging
logger = Logging.setup_logging()

####################################################################################################

from PySpice.Spice.Netlist import Circuit

# 下面這行是關鍵，它並非普通的註解
# 若無此行，PyCharm 會錯誤解析程式碼中 @ 符號的含義
# 使得 IDE 認為未使用 `from PySpice.Unit import` 匯入的內容

# noinspection PyUnresolvedReferences
from PySpice.Unit import *

####################################################################################################

# 建立一個名為 "Voltage Divider"（電壓分壓器）的電路
circuit = Circuit('Voltage Divider')

# 定義一個輸入電壓源 V(input)，電壓為 10 伏特
circuit.V('input', 1, circuit.gnd, 10@u_V)
# 定義兩個電阻 R1 和 R2，分別為 2kΩ 和 1kΩ
circuit.R(1, 1, 2, 2@u_kΩ)
circuit.R(2, 2, circuit.gnd, 1@u_kΩ)

# 建立模擬器，設定溫度為 25°C
simulator = circuit.simulator(temperature=25, nominal_temperature=25)
analysis = simulator.operating_point()

# 輸出節點電壓，格式化為 5.2f 格式的伏特
for node in analysis.nodes.values():
    print('Node {}: {:5.2f} V'.format(str(node), float(node))) # Fixme: 修正格式化為包含單位的輸出

####################################################################################################

#r# 類似地，可以建立一個電路來使用阻抗比縮放電流：

#f# circuit_macros('current-divider.m4') # 引入電流分壓器電路的圖形表示

#r# 輸入電流與輸出電流之間的關係為：
#r#
#r# .. math::
#r#
#r#     \frac{I_{out}}{I_{in}} = \frac{R_1}{R_1 + R_2}
#r#
#r# 注意 R1 和 R2 的角色與電壓分壓器中的位置互換。
#r#
#r# 此公式適用於各種阻抗元件，如電阻、電容和電感等。

####################################################################################################

# 建立一個名為 "Current Divider"（電流分壓器）的電路
circuit = Circuit('Current Divider')

# 定義輸入電流源 I(input)，電流為 1 安培
circuit.I('input', 1, circuit.gnd, 1@u_A) # Fixme: 調整輸入電流值
# 定義兩個並聯的電阻 R1 和 R2，分別為 2kΩ 和 1kΩ
circuit.R(1, 1, circuit.gnd, 2@u_kΩ)
circuit.R(2, 1, circuit.gnd, 1@u_kΩ)

# 為兩個電阻設定電流探針，確保輸出的電流值為正值
for resistance in (circuit.R1, circuit.R2):
    resistance.minus.add_current_probe(circuit)

# 建立模擬器，設定溫度為 25°C
simulator = circuit.simulator(temperature=25, nominal_temperature=25)
analysis = simulator.operating_point()

# 輸出每個元件的電流，格式化為 5.2f 格式的安培
for node in analysis.branches.values():
    print('Node {}: {:5.2f} A'.format(str(node), float(node))) # Fixme: 修正格式化為包含單位的輸出
