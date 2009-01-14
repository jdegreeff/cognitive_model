#
#i = 3
#if i == (1 or 2):
#    print "yes"
#else:
#    print "no"


def function(i):
    x = 0 
    while x < i:
        print "test"
        return x
        x += 1
    print "end"
    
print function(5)