import argparse, random, sys

class shuf:
    def __init__(self, lines, headCount, repeat):
        self.repeat = repeat
        self.lines = lines
        self.headCount = headCount

    def shuffle(self):
        random.shuffle(self.lines)
        # Repeat is true
        if(self.repeat):
            #print indefinitely if headcount not given
            if(self.headCount == None):
                while(True):
                    print(random.choice(self.lines).strip())
            #print "headcount" times
            else:
                while(self.headCount>0):
                    print(random.choice(self.lines).strip())
                    self.headCount-=1
        else:
            #if no headcount given, number of printed lines = len(lines)
            if(self.headCount == None or self.headCount > len(self.lines)):
                self.headCount = len(self.lines)
            #print elements in lines
            for x in range(0,self.headCount):
                print(self.lines[x].strip())
        return
    
        
def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    
    #positional arguments
    group.add_argument("filename", type=str, nargs='?')

    #optional arguments
    parser.add_argument("-n","--head-count", type=int, help="Output at most count lines.\
                        By default, all input lines are output.")
    
    parser.add_argument("-r","--repeat", help="Repeat output values, that is, select with replacement.\
                        With this option the output is not a permutation pyof the input;\
                        instead, each output line is randomly chosen from all the inputs.\
                        This option is typically combined with --head-count;\
                        if --head-count is not given, shuf repeats indefinitely.", action="store_true")

    group.add_argument("-i","--input-range", help="Act as if input came from a file containing\
                        the range of unsigned decimal integers lo…hi, one per line." )

    group.add_argument("-e","--echo", nargs='*', help="Treat each command-line operand as an input line")
    
    '''
    # mutually exclusive
        -i filename
        -i -e
        filename -e
    
    '''
    
    options = parser.parse_args()
    args = sys.argv[1:]
    lines = []
    headCount = options.head_count
    repeat = options.repeat
    inputRange = options.input_range
    echo = options.echo

    #headcount cannot be negative
    if(headCount != None and headCount < 0):
        parser.error("negative headcount: {0}".format( headCount ))

    #Determin the data in lines

    #if inputRange is true
    if(inputRange != None):
        start= eval(inputRange[0:inputRange.find('-')])
        end= eval(inputRange[inputRange.find('-')+1:len(inputRange)])
        if(start > end):
            parser.error("Input Range Error: Please Follow Format (lo-hi)")
        for x in range(start, end+1):
            lines.append(str(x))
    #if echo is true
    elif(echo != None):
        lines = echo
    #if read from stdin and inputRange is false and echo is false
    elif((options.filename == None)
       or (options.filename == '-')):
        lines = sys.stdin.readlines()
    #if filename is given
    elif(options.filename != None and len(args) > 0):
        f = open(options.filename, 'r')
        lines = f.readlines()
        f.close()
            
    generator = shuf(lines, headCount, repeat)
    generator.shuffle()

if __name__ == "__main__":
    main()
