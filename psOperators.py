#alex king 11657564

from psItems import Value, ArrayValue, FunctionValue
class Operators:
    def __init__(self, scoperule):
        #stack variables
        self.opstack = []  #assuming top of the stack is the end of the list
        self.dictstack = []  #assuming top of the stack is the end of the list
        self.scope = scoperule
        #The builtin operators supported by our interpreter
        self.builtin_operators = {'opPop':'pop'

             # TO-DO in part1
             # include the key value pairs where he keys are the PostScrip opertor names and the values are the function values that implement that operator. 
             # Make sure **not to call the functions** 
        }
    #-------  Operand Stack Operators --------------
    """
        Helper function. Pops the top value from opstack and returns it.
    """
    def opPop(self):
        if len(self.opstack) > 0:
            item = self.opstack[len(self.opstack) - 1]
            self.opstack.pop(len(self.opstack) - 1)
            return item
        else:
            print("Error: opPop - Operand stack is empty")

    """
       Helper function. Pushes the given value to the opstack.
    """
    def opPush(self,value):
        self.opstack.append(value)
        
    #------- Dict Stack Operators --------------
    
    """
       Helper function. Pops the top dictionary from dictstack and returns it.
    """   
    def dictPop(self):
        if len(self.dictstack)>0:
            self.dictstack.pop(len(self.dictstack)-1)
        else:
            print("ERROR dictionary stack is empty :(")

        
        

    """
       Helper function. Pushes the given dictionary onto the dictstack. 
    """   
    def dictPush(self,index,d):
        self.dictstack.append((index,d))
    
    def getRefLevel(self,element):
        for i in self.dictstack:
            if i[1]==element:
                return self.dictstack[i][0]
        return 0
    

    """
       Helper function. Adds name:value pair to the top dictionary in the dictstack.
       (Note: If the dictstack is empty, first adds an empty dictionary to the dictstack then adds the name:value to that. 
    """   
    def define(self,name, value):
        if len(self.dictstack)>0:
            self.dictstack[-1][1][name] = value
            # lastref = self.dictstack[len(self.dictstack)-1][0]
            # self.dictstack.append((lastref+1,{name:value}))
        else:
            self.dictstack.append((0,{name:value}))

    """
       Helper function. Searches the dictstack for a variable or function and returns its value. 
       (Starts searching at the top of the opstack; if name is not found returns None and prints an error message.
        Make sure to add '/' to the begining of the name.)
    """
    def lookup(self,name):
        if self.scope == 'dynamic':
            for i in reversed(self.dictstack):
                if i[1].get('/'+name,None)!=None:
                    return i[1].get('/'+name,None)
            return None
        else:
            # count = 0
            # x =None
            # z=1
            index = len(self.dictstack)-1
            if index>=0:
                while True:
                    val = self.dictstack[index][1].get('/'+name,None)
                    if val is not None:
                        return val
                    if index == 0 :
                        return None
                    index = self.dictstack[index][0] 
            
                    # while self.dictstack[count][0]==self.dictstack[count+z][0]:
                    #     x = self.dictstack[count+z][1]
            #     count+=1
            # return x
        
        # name = '/'+name
        # if name in self.dictstack[-1]:
        #    return self.dictstack[-1][name]
        # else: 
        #     print("not in stack")
    
    #------- Arithmetic Operators --------------
    
    """
       Pops 2 values from opstack; checks if they are numerical (int); adds them; then pushes the result back to opstack. 
    """   
    def add(self):
        if len(self.opstack) > 1:
            op1 = self.opPop()
            op2 = self.opPop()
            if isinstance(op1,int) and isinstance(op2,int):
                self.opPush(op1 + op2)
            else:
                print("Error: add - one of the operands is not a number value")
                self.opPush(op2)
                self.opPush(op1)             
        else:
            print("Error: add expects 2 operands")
 
    """
       Pop 2 values from opstack; checks if they are numerical (int); subtracts them; and pushes the result back to opstack. 
    """   
    def sub(self):
        if len(self.opstack)>1:
            op1 = self.opPop()
            op2 = self.opPop()
            if isinstance(op1,int) and isinstance(op2,int):
                self.opPush(op2-op1)
            else:
                print("error: add - one of the operands is of invalid type")
                self.opPush(op2)
                self.opPush(op1)

    """
        Pops 2 values from opstack; checks if they are numerical (int); multiplies them; and pushes the result back to opstack. 
    """    
    def mul(self):
        if len(self.opstack)>1:
            op1 = self.opPop()
            op2 = self.opPop()
            if isinstance(op1,int) and isinstance(op2,int):
                self.opPush(op1*op2)
            else:
                print("error: mul-operand of invalid type")
                self.opPush(op2)
                self.opPush(op1)
        

    """
        Pops 2 values from stack; checks if they are int values; calculates the remainder of dividing the bottom value by the top one; 
        pushes the result back to opstack.
    """ 
    def mod(self):
        if len(self.opstack)>1:
            op1 = self.opPop()
            op2 = self.opPop()
            if isinstance(op1,int) and isinstance(op2,int):
                self.opPush(op2%op1)
            else:
                print("ERROR! mod-operand of invalid type")
                self.opPush(op2)
                self.opPush(op1)

    #---------- Comparison Operators  -----------------
    """
       Pops the top two values from the opstack; pushes "True" is they are equal, otherwise pushes "False"
    """ 
    def eq(self):
        if len(self.opstack)>1:
            op1 = self.opPop()
            op2 = self.opPop()
            if op1==op2:
                self.opPush(True)
            else:
                self.opPush(False)

    """
       Pops the top two values from the opstack; pushes "True" if the bottom value is less than the top value, otherwise pushes "False"
    """ 
    def lt(self):
        if len(self.opstack)>1:
            op1 = self.opPop()
            op2 = self.opPop()
            if op2<op1:
                self.opPush(True)
            else:
                self.opPush(False)

    """
       Pops the top two values from the opstack; pushes "True" if the bottom value is greater than the top value, otherwise pushes "False"
    """ 
    def gt(self):
        if len(self.opstack)>1:
            op1 = self.opPop()
            op2 = self.opPop()
            if op2>op1:
                self.opPush(True)
            else:
                self.opPush(False)

    # ------- Array Operators --------------
    """ 
       Pops an array value from the operand opstack and calculates the length of it. Pushes the length back onto the opstack.
       The `length` method should support ArrayValue values.
    """
    def length(self):
        if len(self.opstack)>0:
            a1 = self.opPop()
            print(a1)
            count = 0
            if (isinstance(a1,ArrayValue)):
                
                self.opPush(len(a1.value))
            else:
                print("ERROR INVALID TYPE")
        else:
            print("ERROR OPSTACK EMPTY")

    
    """ 
        Pops the `count` (int), an (zero-based) start `index`, and an array constant (ArrayValue) from the operand stack.  
        Pushes the slice of the array of length `count` starting at `index` onto the opstack.(i.e., from `index` to `index`+`count`) 
        If the end index of the slice goes beyond the array length, will give an error. 
    """
    def getinterval(self):
        if len(self.opstack)>2:
            count = self.opPop()
            index1 = self.opPop()
            arr1 = self.opPop()
            
            if (count+index1 > len(arr1.value)):
                self.opPush(arr1.value[index1:count])
        else:
            print("ERROR NOT ENOUGH OPERANDS FOR GETINTERVAL")

    """ 
        Pops an array constant (ArrayValue), start `index` (int), and another array constant (ArrayValue) from the operand stack.  
        Replaces the slice in the bottom ArrayValue starting at `index` with the top ArrayValue (the one we popped first). 
        The result is not pushed onto the stack.
        The index is 0-based. If the end index of the slice goes beyond the array length, will give an error. 
    """
    def putinterval(self):
        if len(self.opstack)>2:
            arr1 = self.opPop()
            index1 = self.opPop()
            arr2 = self.opPop()
            self.opPush(arr2.value[index1:].append(arr1))
        else:
            print("ERROR NOT ENOUGH OPERANDS")
            

    """ 
        Pops an array constant (ArrayValue) from the operand stack.  
        Pushes all values in the array constant to the opstack in order (the first value in the array should be pushed first). 
        Pushes the orginal array value back on to the stack. 
    """
    def aload(self):
        a1 = self.opPop()
        if len(self.opstack)>0:
            for i in a1.value:
                self.opPush(i)
            self.opPush(a1)
        else:
            print("ERROR INVALID LENGTH of OPSTACK")
        
        
    """ 
        Pops an array constant (ArrayValue) from the operand stack.  
        Pops as many elements as the length of the array from the operand stack and stores them in the array constant. 
        The value which was on the top of the opstack will be the last element in the array. 
        Pushes the array value back onto the operand stack. 
    """
    def astore(self):
        a1 = self.opPop()
        num = self.length()
        if len(self.opstack)>num:
            for i in range(0,len(a1.value)-1):
                a1.value.append(self.opPop())
            self.opPush(a1)
        else:
            print("ERROR INVALID OPSTACK LENGTH")


    #------- Stack Manipulation and Print Operators --------------

    """
       This function implements the Postscript "pop operator". Calls self.opPop() to pop the top value from the opstack and discards the value. 
    """
    def pop (self):
        self.opPop()

    """
       Prints the opstack. The end of the list is the top of the stack. 
    """
    def stack(self):
        print("*********OPSTACK*********")
        for i in self.opstack:
            print(i)
        print("*********DICTSTACK********")
        for i in self.dictstack:
            print(i)

    """
       Copies the top element in opstack.
    """
    def dup(self):
        thing = self.opPop()
        self.opPush(thing)
        self.opPush(thing)

    """
       Pops an integer count from opstack, copies count number of values in the opstack. 
    """
    def copy(self):
        if len(self.opstack)>0:
            l = []
            t = self.opPop()
            for i in range(0,t):
                l.append(self.opPop())
            for i in reversed(l):
                self.opPush(i)
            for i in reversed(l):
                self.opPush(i)
        else:
            print("ERROR EMPTY STACK")

    """
        Counts the number of elements in the opstack and pushes the count onto the top of the opstack.
    """
    def count(self):
        count1 = len(self.opstack)
        self.opPush(count1)

    """
       Clears the opstack.
    """
    def clear(self):
        while len(self.opstack)!=0:
            self.opPop()
        
    """
       swaps the top two elements in opstack
    """
    def exch(self):
        if len(self.opstack)>1:
            op2 = self.opPop()
            op1 = self.opPop()
            self.opPush(op2)
            self.opPush(op1)

        else:
            print("ERROR STACK INCORRECT LENGTH")

    """
        Implements roll operator.
        Pops two integer values (m, n) from opstack; 
        Rolls the top m values in opstack n times (if n is positive roll clockwise, otherwise roll counter-clockwise)
    """
    def roll(self):
        if len(self.opstack)>2:
            m = self.opPop()
            n = self.opPop()
            s = self.opstack[len(self.opstack)-n:]
            if m>0:
                temp = s[m:]
                s[m:]=[]
                s[:0]=temp
            elif m<0:
                temp = s[0:(-1*m)]
                s[:(-1*m)]=[]
                s[len(s):]=temp
            

            for i in range(0,n):
                self.opPop()
            for i in s:
                self.opPush(i)  
        else:
            print("ERROR OPSTACK OF INVALID LENGTH") 

    """
       Pops an integer from the opstack (size argument) and pushes an  empty dictionary onto the opstack.
    """
    def psDict(self):
        if len(self.opstack)>0:
            num = self.opPop()
            self.opPush({})
        else:
            print("ERROR OPSTACK EMPTY")

    """
       Pops the dictionary at the top of the opstack; pushes it to the dictstack.
    """
    def begin(self):
        d={}
        if len(self.opstack)>0:
            d=self.opPop()
            self.dictPush(d)
        else:
            print("ERROR OPSTACK EMPTY")

    """
       Removes the top dictionary from dictstack.
    """
    def end(self):
        if len(self.dictstack)>0:
            self.dictPop()
        else:
            print("ERROR DICTSTACK EMPTY")
        
    """
       Pops a name and a value from opstack, adds the name:value pair to the top dictionary by calling define.  
    """
    def psDef(self):
        if len(self.opstack)>=2:
            val = self.opPop()
            name = self.opPop()
            name=name[0:]
            self.define(name,val)

        else:
            print("ERROR OPSTACK DOES NOT CONTAIN ENOUGH OPERANDS")



    # ------- if/ifelse Operators --------------
    """
       Implements if operator. 
       Pops the `ifbody` and the `condition` from opstack. 
       If the condition is True, evaluates the `ifbody`.  
    """
    def psIf(self):
        if len(self.opstack)>1:
            func = self.opPop()
            cond = self.opPop()
            if cond:
                func.evaluate(self)
            else:
                print("condition false")
                self.opPush(cond)
                self.opPush(func)
        else:
            print("ERROR OPSTACK OF INVALID LENGTH")
            
        

    """
       Implements ifelse operator. 
       Pops the `elsebody`, `ifbody`, and the condition from opstack. 
       If the condition is True, evaluate `ifbody`, otherwise evaluate `elsebody`. 
    """
    def psIfelse(self):
        if len(self.opstack)>2:
            elsebody = self.opPop()
            ifbody = self.opPop()
            cond = self.opPop()
            if cond:
                ifbody.evaluate(self)
            else:
                elsebody.evaluate(self)
        # TO-DO in part2


    #------- Loop Operators --------------
    """
       Implements repeat operator.   
       Pops the `loop_body` (FunctionValue) and loop `count` (int) arguments from opstack; 
       Evaluates (applies) the `loopbody` `count` times. 
       Will be completed in part-2. 
    """  
    def repeat(self):
        if len(self.opPop())>1:
            loopBod = self.opPop()
            count = self.opPop()
            loopBod.apply(self,len(self.dictstack)-1)
            #call apply  staticlink = len(dictstack)-1
            #self
            for i in count:
                i.evaluate(self)
        else:
            print("NOT ENOUGH OPERANDS")
        
    """
       Implements forall operator.   
       Pops a `codearray` (FunctionValue) and an `array` (ArrayValue) from opstack; 
       Evaluates (applies) the `codearray` on every value in the `array`.  
       Will be completed in part-2. 
    """ 
    def forall(self):
        if len(self.opstack)>1:
            codeArr = self.opPop()
            arry1 = self.opPop()
            for i in arry1.value:
                i.apply(self) 
        else:
            print("ERROR OPSTACK NOT ENOUGH OPERANDS FOR FORALL")

    #--- used in the setup of unittests 
    def clearBoth(self):
        self.opstack[:] = []
        self.dictstack[:] = []

    def cleanTop(self): 
        if len(self.opstack)>1: 
            if self.opstack[-1] is None: 
                self.opstack.pop() 
    
