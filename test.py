class N:
    def __init__(self,ranNum):
        self.n = ranNum
    def __eq__(self, other):
        if not isinstance(other,N):
            return NotImplemented
        return self.n == other.n
    
    def __repr__(self):
        return f"N({self.n})"
      
    
class T:
    def __init__(self,ranSrin):
        self.s = ranSrin
        
    
n1 = N(1)
n2 = N(2)
n3 = N(3)
n4 = N(4)
n5 = N(5)
n_3 = N(3)

nlist = [n1,n2,n3,n4,n5]
if n_3 in nlist:
    print("found")
    nlist.remove(n3)
    for n in nlist:
        print(repr(n))

else:
    print("not found")