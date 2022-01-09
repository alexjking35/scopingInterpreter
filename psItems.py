"""Parts of this code was adopted from https://composingprograms.com/. 
The code has been changed according to Postscript syntax. 
https://creativecommons.org/licenses/by-sa/3.0/
"""
class Expr:
    """
    When you type input into this interpreter, it is parsed (read) into an expression. 
    This expression is represented in our code as an instance of this `Expr` class.
    In our interpreter, there are five types of expressions:
        1.	Literal:  represents primitive constants : integers or booleans . The `value` attribute contains the fixed value the `Literal` refers to. 
        2.	Name: represents names of variables, functions, or operators .  The `var_name` attribute contains the name of the variable as a Python string, e.g., '/sq','sq','add','def'. If the `var_name` starts with a `/` character, Name represents a name constant, otherwise it represents a variable reference ,  function call, or a built-in operator call. 
        3.	Array: represents arrays.  The `value` attribute is a Python list that includes the elements of the PostScript array it represents, e.g., [Literal(1),Name(x), Literal(2), Literal(3), Name(y),Name(add)] 
        4.	Block: represents body of a function or if, ifelse, or for expressions. The `value` attribute is a Python list that includes the tokens of the PostScript code-array (block) it represents [Literal(10), Literal(5),Name(mul)]
    In our code, the four types of expressions are subclasses of the `Expr`
    class: `Literal`, `Name`, `Array`, and `Block`.
    """
    def __init__(self, value):
        self.value = value

    def evaluate(self, psstacks):
        """
        Each subclass of Expr implements its own evaluate method.
        `psstacks` is the Operators object that include the `opstack` and `dictstack`. 
        Subclasses of `Expr` should implement this method. (i.e., `Literal`, `Name`, `Array`, and `Block`  )
        This method should return a `Value` instance, the result of  evaluating the expression.
        """
        raise NotImplementedError

    def __str__(self):
        """
        Returns a parsable and human-readable string of this expression (i.e.    what you would type into the interpreter).
        """
        raise NotImplementedError
    
    def __repr__(self):
        """
        Returns how this expression is written in our Python representation.
        """
        return "{}({})".format(type(self).__name__, self.value)

class Literal(Expr):
    """A literal is notation for representing a primitive constant value in code. 
    In our interpreter, a `Literal` evaluates to a number (int or float) or a boolen. The evaluated value is pushed onto the stack. 
    The `value` attribute contains the fixed value the `Literal` refers to.
    """
    def __init__(self, value):
        Expr.__init__(self, value)
        self.value = value

    def evaluate(self, psstacks): 
        psstacks.opPush(self.value)
        return self.value

    def __str__(self):
        return str(self.value)

class Array(Expr):
    """An Array is notation for representing an array constant in code. `
    -  In our interpreter, an `Array` evaluates to an `ArrayValue` object. 
    -  The `value` attribute is a Python list that includes the elements of the PostScript array it represents. e.g., [Literal(1),Name(x), Literal(2), Literal(3), Name(y),Name(add)]  
       The elements in the array `value` to be evaluated first and  the `ArrayValue` should be initialized with this evaluated list of elements, i.e., [1,10,2,23]. 
    -  The evaluated `ArrayValue` is pushed onto the stack. 
    """
    def __init__(self, value):
        Expr.__init__(self, value)
        self.value = value

    #needs to be updated
    def evaluate(self,psstacks):
        for i in self.value:
            i.evaluate(psstacks)
            psstacks.opPop()
        psstacks.opPush(self.value)
        return ArrayValue(self.value)

    def __str__(self):
        return str(self.value)

class Name(Expr):
    """A `Name` is a variable , a built-in operator, or a function. 
        a.	If the `Name` represents a name constant (i.e., its `var_name` attribute starts with a `/`), it will be evaluated to a Python string having value `var_name` . The evaluated value will be pushed onto the opstack.
        b.	If the `Name` represents a built-in operator (i.e., its `var_name` attribute is one of the built-in operator names),  then we will evaluate it by executing the operator function defined in stacks.py in the current environment (opstack). 
        c.	If the `Name` represents a variable or function, interpreter looks up the value of the variable in the current environment (dictstack).
            i.	If the variable value is a function (`FunctionValue`), it should be applied (i.e., executed) by calling its `apply` method.  
            ii.	Otherwise, the variable value is a constant and it should be pushed onto the opstack. 

    The `var_name` attribute contains the name of the variable (as a Python string).
    """
    def __init__(self, var_name):
        Expr.__init__(self, var_name)
        self.var_name = var_name
        self.refVal = 0

    def staticlink(self,psstacks,name):
        index = len(psstacks.dictstack)-1
        if index>=0:
            while True:
                val = psstacks.dictstack[index][1].get(name,None)
                if val is not None:
                    return index
                if index == 0 :
                    return None
                index = psstacks.dictstack[index][0] 
        return None

    def evaluate(self,psstacks):
        if self.var_name[0]=='/':
            self.var_name = self.value
            self.refVal = psstacks.getRefLevel(self.value)
            psstacks.opPush(self.value)
            return self.var_name
        elif self.var_name == 'def':
            psstacks.psDef()
            return self.var_name
        elif self.var_name == 'add':
            psstacks.add()
            return self.var_name
        elif self.var_name == 'sub':
            psstacks.sub()
            return self.var_name
        elif self.var_name == 'mul':
            psstacks.mul()
            return self.var_name
        elif self.var_name == 'div':
            psstacks.div()
            return self.var_name
        elif self.var_name == 'mod':
            psstacks.mod()
            return self.var_name
        elif self.var_name == 'eq':
            psstacks.eq()
            return self.var_name
        elif self.var_name == 'lt':
            psstacks.lt()
            return self.var_name
        elif self.var_name == 'gt':
            psstacks.gt()
            return self.var_name
        elif self.var_name == 'length':
            psstacks.length()
            return self.var_name
        elif self.var_name == 'putInterval':
            psstacks.putInterval()
            return self.var_name
        elif self.var_name == 'getInterval':
            psstacks.getInterval()
            return self.var_name
        elif self.var_name == 'roll':
            psstacks.roll()
            return self.var_name
        elif self.var_name == 'aload':
            psstacks.aload()
            return self.var_name
        elif self.var_name == 'astore':
            psstacks.astore()
            return self.var_name
        elif self.var_name == 'pop':
            psstacks.pop()
            return self.var_name
        elif self.var_name == 'stack':
            psstacks.stack()
            return self.var_name
        elif self.var_name == 'dup':
            psstacks.dup()
            return self.var_name
        elif self.var_name == 'copy':
            psstacks.copy()
            return self.var_name
        elif self.var_name == 'count':
            psstacks.count()
            return self.var_name
        elif self.var_name == 'exch':
            psstacks.exch()
            return self.var_name
        elif self.var_name == 'begin':
            psstacks.begin()
            return self.var_name
        elif self.var_name == 'end':
            psstacks.end()
            return self.var_name 
        elif self.var_name == 'clear':
            psstacks.clear()
            return self.var_name  
        elif self.var_name == 'if':
            psstacks.psIf()
            return self.var_name
        elif self.var_name == 'ifelse':
            psstacks.psIfelse()
            return self.var_name
        elif self.var_name == 'repeat':
            psstacks.repeat()
            return self.var_name
        elif self.var_name == 'forall':
            psstacks.forall()
            return self.var_name
        else:
            val = psstacks.lookup(self.var_name)
            if isinstance(val,FunctionValue):
                static_link = self.staticlink(psstacks,'/'+ self.var_name )
                val.apply(psstacks,static_link)
            else:
                psstacks.opPush(val)
            # x = psstacks.lookup(self.var_name)
            # psstacks.opPush(x)
        

    def __str__(self):
        return str(self.var_name)
    
    def __repr__(self):
        """ Returns how this expression is written in our Python representation. """
        return "{}('{}')".format(type(self).__name__, self.var_name)

class Block(Expr):
    """A `Block` is notation for representing a code block in PostScript, i.e., a function body, `if` block, `ifelse` block, or `for` loop block. 
    In our interpreter, `Block` object is evaluated to `FunctionValue` value.  For example: a `Block` with `value`  attribute [Name(dup), Name(mul)] will be evaluated to `FunctionValue` with the same `value`  (i.e., [Name(dup), Name(mul)]. The evaluated `FunctionValue` is pushed onto the stack. 
    The `value` attribute contains the list of tokens in the function body.
    """
    def __init__(self, value):
        Expr.__init__(self, value)
        self.value = value
    
    def staticlink(self,psstacks,name):
        i = len(psstacks.dictstack)-1
        if name in psstacks.dictstack:
            i = psstacks.dictstack.index(name)
        return i

    def evaluate(self, psstacks):
        x = FunctionValue(self.value)
         
            # for i in x.body:
            #     i.evaluate(psstacks)
            #x.apply(psstacks,self.staticlink)
        psstacks.opPush(x)
            

    def __str__(self):
        return str(self.value)

## -----------------------------------------------------------------------------------
## -----------------------------------------------------------------------------------

class Value:
    """
    "Value" objects represent the array and code-array constants that are pushed onto the stack.  
    
    In our interpreter,
        -  For simplicity, the integers and boolean values are pushed onto the opstack as integers and booleans, respectively. 
        -  Similarly, name constants (e.g. '/x') are pushed to the opstack as strings. 
        -  The array, and codearray constants are represented as ArrayValue and FunctionValue objects, 
           which are subclasses of the `Value`. 
        -  ArrayValue, and FunctionValue implement the following methods in the `Value` interface:
            * apply : Evaluates the value. `apply` is only applicable to FunctionValue objects (applies the function, evaluates all the tokens in the function's code-array, i.e., FunctionValue )  
            * __str__: Conversts the value to  a human-readable version (i.e., string) for printing.
    """

    def __init__(self, value):
        self.value = value

    def apply(self, psstack):
        """
        Each subclass of Value implements its own `apply` method.
        Note that only `FunctionValue`s can be "applied"; attempting to apply an ArrayValue will give an error. 
        """
        raise NotImplementedError

    def __str__(self):
        """
        Returns a parsable and human-readable version of this value (i.e. the string to be displayed in the interpreter).
        """
        raise NotImplementedError

    def __repr__(self):
        """
        Returns how this value is printed in our Python representation.
        """
        return "{}({})".format(type(self).__name__, self.value)

# ------------------------------------------------------------

class ArrayValue(Value):
    """An array constant delimited in square brackets. Attempting to apply an `array constant` will give an error.
      The `value` attribute is the Python list that this value represents.

      You may add additional methods to this class as needed and use them in your operator implementations. 
    """
    def __init__(self, value):
        Value.__init__(self, value)
        self.value = value

    def apply(self, psstacks):
        raise TypeError("Ouch! Cannot apply `array constant` {} ".format(self.value))

    def __str__(self):
        return "{}({})".format(type(self).__name__, self.value)
        #return str(self.value)

# ------------------------------------------------------------

class FunctionValue(Value):
    """The constant-array that represents the body of a (user-defined) function, or if, ifelse, for operators. 
    The `body` attribute is a nested list of expressions.
    The `apply` method will evaluate each expression in the `body` by calling token's `evaluate` method. 
    Expressions will be evaluated in in the current referencing environment (psstacks).  
    """
    def __init__(self, body):
        Value.__init__(self, body)
        self.body = body

    def apply(self, psstacks,staticlink):
        psstacks.dictPush(staticlink,{})
        #print(psstacks.dictstack)
        for i in self.body:
            i.evaluate(psstacks)
            # print(i.value)
            # if isinstance(i.value,int) or isinstance(i.value,bool) or isinstance(i.value,float):
            #     n = Literal(i.value)
            #     n.evaluate(psstacks)
            # if isinstance(i.value,str):
            #     n = Name(i.value)
            #     n.evaluate(psstacks)
        psstacks.dictPop()
        #pop the dictstack

    def __str__(self):
        return '<function {}>'.format(self.body)   