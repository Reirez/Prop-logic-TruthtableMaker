from tabulate import tabulate

class Parser:
    def __init__(self, proposition):
        self.singles = []
        self.propo = proposition
        self.props = {}
        self.counter = 0
        
    def single(self):
        operands = set(['v', '^', '>', ':', '-', '(', ')', '='])
        for content in self.propo:
            if content not in operands:
                self.singles.append(content)
       
    def appewnd(self, to_append):
        self.counter += 1
        self.props[str(self.counter)] = to_append
            
    def pthesis(self):
        while '(' in self.propo or ')' in self.propo:
            owpen, clowse = 0, 0 
            for index, item in enumerate(self.propo):
                if item == '(':
                    owpen = index
                if item == ')':
                    clowse = index
                    break
            self.appewnd(self.propo[owpen + 1:clowse])
            self.propo = self.propo[:owpen] + [str(self.counter)] + self.propo[clowse + 1:]
            
    def operations(self, operand):
        if operand == '-': o = 0
        else: o = -1
        i = 0
        while operand in self.propo:
            if self.propo[i] == operand:
                self.appewnd(self.propo[i+o:i+2])
                self.propo = self.propo[:i+o] + [str(self.counter)] + self.propo[i+2:]
            i += 1
        
    def main(self):
        self.single()
        self.pthesis()
        for operand in ['-', '^', 'v', '>', '=']:
            self.operations(operand)

class TruthTable(Parser):
    def __init__(self, proposition):
        super().__init__(proposition)
        self.main()
        self.tsingles = self.singles_truth()
        self.premises = {}
        for key, premise in self.props.items():
            self.premises[tuple(premise)] = []
        
    def singles_truth(self):
        idk = [True, False] #0, 1
        somedict, counter = {}, 1
        rows = 2 ** len(self.singles)
        divider = rows / 2
        turns = 0
        for letter in self.singles:
            somelist = []
            for i in range(rows):
                if counter > divider:
                    counter = 1
                    turns += 1
                somelist.append(idk[turns % 2])
                counter += 1
            somedict[letter] = somelist
            divider = divider / 2
        return somedict
                
    def propo_trans(self, statement):
        legend = {'v': 'or', '^': 'and',
                  '-': 'not', '=': '=='}
        translated = ""
        for content in statement:
            if content in legend:
                translated += f' {legend[content]}'
            elif content == '(' or content == ')':
                translated += content
            else:
                translated += f" self.tsingles['{content}'][i]"
        return translated
    
    def material_imp(self, premise):
        if '>' not in premise: return premise
        i = 0
        while i < len(premise):
            if premise[i] == '>':
                premise[i] = 'v'
                premise.insert(i - 1, '-')
                i += 2
            else: i += 1
        return premise 
    
    def turnback(self, statement):
        i = 0
        while i<len(statement):
            statement = self.material_imp(statement[:])
            if statement[i].isdigit():
                statement = statement[:i] + ['('] + self.props[statement[i]] + [')'] + statement[i+1:] 
                continue
            i += 1
        return statement
            
    def assignval(self):
        for i in range(0, 2**len(self.singles)):
            for premise in self.props.values():
                premise2 = self.turnback(premise)
                translated = self.propo_trans(premise2)
                self.premises[tuple(premise)].append(eval(translated))
    
    def main2(self):
        self.assignval()
        self.to_table()
            
    def to_table(self):
        tlists = []
        for key, value in self.props.items():
            text = ''
            for content in value: text += content
            print(f'{key}: {text}')
            
        for single, bools in self.tsingles.items():
            to_append = list(single) + bools
            tlists.append(to_append)
            
        for premise, bools in self.premises.items():
            text = ''
            for content in premise:
                text += ' ' + content
            to_append = [text] + bools
            tlists.append(to_append)
            
        self.tlists = []
        for i in range(0, 2**len(self.singles) + 1):
            somelist = []
            for o in range(len(tlists)):
                somelist.append(tlists[o][i])
            self.tlists.append(somelist)
            
x = list(input("Enter proposition: "))
x = [content for content in x if content != " "]
                    
p = TruthTable(x)
p.main2()
print(tabulate(p.tlists))

