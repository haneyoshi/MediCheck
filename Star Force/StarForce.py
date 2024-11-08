import random
import numpy as np

class StarForce:
  def __init__(self,s,d):
    self.suRate = s
    self.deRate = d
  # def getChance(self):
  #   return random.randint(1,100)
  # def enhance(self):
  #   success = self.getChance() < self.suRate
  #   if success:
      
  
#random > suRate --> fail
#random <= deRate --> degrade
class Star0(StarForce):
  def __init__(self, s, d):
    super().__init__(95, 0)


class Star1(StarForce):
  def __init__(self, s, d):
    super().__init__(90, 0)


class Star2(StarForce):
  def __init__(self, s, d):
    super().__init__(85, 0)


class Star3(StarForce):
  def __init__(self, s, d):
    super().__init__(85, 0)


class Star4(StarForce):
  def __init__(self, s, d):
    super().__init__(80, 0)


class Star5(StarForce):
  def __init__(self, s, d):
    super().__init__(75, 0)


class Star6(StarForce):
  def __init__(self, s, d):
    super().__init__(70, 0)


class Star7(StarForce):
  def __init__(self, s, d):
    super().__init__(65, 0)


class Star8(StarForce):
  def __init__(self, s, d):
    super().__init__(60, 0)


class Star9(StarForce):
  def __init__(self, s, d):
    super().__init__(55, 0)


class Star10(StarForce):
  def __init__(self, s, d):
    super().__init__(50, 0)


class Star11(StarForce):
  def __init__(self, s, d):
    super().__init__(45, 0)


class Star12(StarForce):
  def __init__(self, s, d):
    super().__init__(40, 0)


class Star13(StarForce):
  def __init__(self, s, d):
    super().__init__(35, 0)


class Star14(StarForce):
  def __init__(self, s, d):
    super().__init__(30, 0)


class Star15(StarForce):
  def __init__(self, s, d):
    super().__init__(30, 0)


class Star16(StarForce):
  def __init__(self, s, d):
    super().__init__(30, 56)


class Star17(StarForce):
  def __init__(self, s, d):
    super().__init__(30, 49)


class Star18(StarForce):
  def __init__(self, s, d):
    super().__init__(30, 42)


class Star19(StarForce):
  def __init__(self, s, d):
    super().__init__(30, 42)


class Star20(StarForce):
  def __init__(self, s, d):
    super().__init__(30, 0)


class Star21(StarForce):
  def __init__(self, s, d):
    super().__init__(30, 35)


class Star22(StarForce):
  def __init__(self, s, d):
    super().__init__(0, 0)


