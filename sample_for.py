class stack():
    def __init__(self):
        self.stack =[]
        self.top = -1
        self.size = 0 
    
    def push(self,d):
        self.stack.append(d)
        self.top +=1
        self.size+=1

    def pop(self,p):
        if not (self.size == 0):
            t = self.stack[self.top]
            # if t == p:
            #     del self.stack[self.top]
            #     for i in self.stack:
            #         if(p<i):
            #             p = i
            # else:
            del self.stack[self.top]
            self.top -= 1
            self.size-= 1
            return p
            
        else:
            print("stack underflow") 
    
    def print_top(self,p):
        if p in self.stack:
            if(p<self.stack[self.top]):
                p = self.stack[self.top]
        else:
             p = -1
             for i in self.stack:
                if(p<i):
                    p = i
        return p

t = input()
s = stack()
p = 0
for i in range(0,t):
    l = raw_input()
    if len(l) == 1:
        N = int(l)
    else:
       N,val = map(int,l.split(' '))
    if ( N == 1):
        s.push(val)
    elif(N == 2):
        s.pop(p)
    elif(N == 3):
        p = s.print_top(p)
        print p