class A:
    def foo(self):
        print('A')
    def bar(self):
        print('BAR')
class B:
    def foo(self):
        print('B')
		
class C(B,A):
    pass
	
c = C()
c.foo()
c.bar()
