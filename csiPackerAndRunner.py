import subprocess as subp
import os
import time
import re
import shutil
import threading as thread
import xml.etree.ElementTree as et

currDirPath = os.path.dirname(os.path.abspath(__file__))
constSeperator = '⇔'
constErrorKey = 'failed'.encode()
constBuildCmd = 'dotnet build --configuration Release'

class decreaseFileSize:
    whiteSpace = {
        '    ' : '\t', #4 spaces = tab
        '   ' : '\t', #3 spaces = tab
        '  ' : ' ', #2 spaces = space
        '\f' : ' ', #form feed = space
        '\v' : ' ' #vertical tab = space
    }
    def __init__(self, file) -> None: 
        self.write = open(file.csproj, 'w', encoding='utf-8')    
        self.read = open(file.csproj, 'r', encoding='utf-8')
    #

    def removeWhiteSpaceChar(self) -> None:
        cont = self.read.read()
        for key, value in self.whiteSpace.items():
            cont = cont.replace(key, value)
        self.write.write(cont.strip())
    #    
    def removeComments(self) -> None:
        cont = self.read.read()
        cont = re.sub(r'//.*', '', cont)
        cont = re.sub(r'/\*.*?\/', '', cont, flags=re.DOTALL)
        self.write.write(cont.strip())
    #

#
class runningCsi:
    def __init__(self, fileName):
        self.fileName = fileName
        self.buildDir = os.path.join(currDirPath, fileName+'_NittyGritty')
    #

    def splitCsiSub(self, cont:str, fileName) -> None:
        try:
            if not os.path.exists(self.buildDir):
                os.makedirs(self.buildDir)
    
            with open(os.path.join(self.buildDir, fileName), 'w', encoding='utf-8') as file:
                file.write(cont)
        except Exception as e:
            print('\033[31mError seperating '+fileName+' from '+self.fileName+'.csi!', e,'\033[0m')
    #
    
    @staticmethod
    def splitCsi(csi, parts) -> bool:
        try:
            csProjCont = parts[0]
            csi.splitCsiSub(csProjCont, csi.fileName+'.csproj')
            sourceCode = parts[1:-1]
            i = 0
            for cs in sourceCode:
                i+=1
                csi.splitCsiSub(cs, f'{csi.fileName}{i}.cs')
            
            return True
        except Exception as e:
            print('\033[31m',e,'\033[0m')
            return False
    #

    def openCsi(self) -> None:
        try:
            csiCont = open(os.path.join(currDirPath, self.fileName+'.csi'), 'r', encoding='utf-8').read()
            parts = csiCont.split(constSeperator)
            if len(parts) <= 2:
                print("Invalid .csi format. must contain first .csproj then .cs sections. All seperated with '⇔'.")

            if not runningCsi.splitCsi(self, parts):
                raise Exception()
            print('.csi initiated...')
        except FileNotFoundError:
            print('File was not found!')
        except Exception as e:
            print('\033[31mError opening csi file!\033[0m')
    #

    def build(self) -> bool:
        try:
            start = time.time()
            proc = subp.run(constBuildCmd, cwd=self.buildDir, stdout=subp.PIPE, text=False)
            if constErrorKey in proc.stdout.lower(): 
                raise Exception(proc.stdout.lower().decode('utf-8'))
            
            print('\033[32m'+f'Built in {time.time()-start} seconds.'+'\033[0m')
            return True
        except Exception as e:
            print('\033[31mError during build:', e, '\033[0m')
            return False
    #

    @staticmethod
    def stdOut(exe) -> None:
        while exe.poll() is None:
            out = exe.stdout.read()
            print(out, end='')
    #

    @staticmethod
    def stdIn(exe) -> None:
        while exe.poll() is None:
            if exe.stdin is not None:
                uInput = input()
                if uInput.strip() == '#':
                    print('closing...')
                    exe.kill()
                    return
                exe.stdin.write(uInput)
                exe.stdin.flush()
    #

    def runApp(self, exe) -> None:
        print('\033[33m'+'You can close by inputting "#"'+'\033[0m')
        try:
            ## jank but if this isnt on 2 threads in and out block each other ##
            outThread = thread.Thread(target=runningCsi.stdOut, args=(exe,))
            inThread = thread.Thread(target=runningCsi.stdIn, args=(exe,))

            outThread.start()
            inThread.start()
            outThread.join()
            inThread.join()
        except subp.CalledProcessError as e:
            print('\033[31mError occurred while running the csi: \033[0m', e)

        print('\nClosed on exit code ', exe.returncode)
    #

    @staticmethod
    def dotNetVers(csiOut) -> str:
        try:
            parse = et.parse(os.path.join(csiOut.buildDir, csiOut.fileName+'.csproj'))
            root = parse.getroot()
            targetFramework = root.find('.//TargetFramework')

            if targetFramework is None:
                raise Exception('TargetFramework not found in .csproj file!')

            return targetFramework.text # type: ignore
        except Exception as e:
            print('\033[31mError finding the .net version!: ', e,'\033[0m')
            return "" 
    #
    
    def executeApp(self) -> None:
        try:
            netVers = runningCsi.dotNetVers(self)
            buildPath = os.path.join(self.buildDir, netVers)
            print('\033[94mApp .NET version:', netVers, '\033[0m')
            self.runApp(subp.Popen(os.path.join(buildPath, f'{self.fileName}.exe'), stdin=subp.PIPE, stdout=subp.PIPE, text=True))   
        except FileNotFoundError:
            print('File not found! have you tried moving the script to the same director as the csi?')
    #
    
    def delete(self) -> None:
        try:
            shutil.rmtree(self.buildDir)
        except Exception as e:
            print('\033[34mcoudlnt finish up and remove all the dirty work; oops')
            print('heres why though!\n',e,'\033[0m')
    #
#

class makingCsi:
    def __init__(self, csproj:str, csFiles:list[str]):
        self.csproj = os.path.join(currDirPath, csproj+".csproj")
        self.cs = [os.path.join(currDirPath, cs + ".cs") for cs in csFiles]
        self.csi = open(os.path.join(currDirPath, csproj+'.csi'), 'a', encoding='utf-8')
    #

    @staticmethod
    def changeTag(cont:str, tag:str, tagText:str) -> str:
        root = et.fromstring(cont)
        tagPath = root.find(tag)
        if tagPath is None:
            ##  add tag  ##
            try:
                propGroup:et.Element = root.find('.//PropertyGroup') # type: ignore
                if propGroup is None:
                    ## shit ##
                    root.append(et.Element('PropertyGroup'))
                tagPath = et.Element(tag)
                tagPath.text = tagText
                propGroup.append(tagPath)
            except AttributeError as e:
                print('Failed to append required tag to csproj: ',e)
            except Exception as e:
                print('Exception while appending needed tags!: ',e)
        else:
            ##  just change it  ##
            tagPath.text = tagText
        return et.tostring(root).decode()
    #

    @staticmethod
    def changeTags(csProjCont) -> str:
        csProjCont = makingCsi.changeTag(csProjCont, 'OutputType', 'Exe')
        return makingCsi.changeTag(csProjCont, 'OutputPath', './')
    #
    
    def packFile(self, file:str, csproj:bool) -> None:
        try:
            cont = open(file, 'r', encoding='utf-8').read()
            if csproj:
                cont = makingCsi.changeTags(cont)
            
            self.csi.write('\n'+cont+'\n'+constSeperator)
        
            print('\033[32m' + f'{os.path.basename(file)} packed into .csi' + '\033[0m')
        except FileNotFoundError:
            print('Files does not exist!')
        except Exception as e:
            print('\033[31mError while packing file! \033[0m',e)
    #
#

def run() -> None:
    csi = runningCsi(input('Input the .csi file: '))
    csi.openCsi()
    if csi.build():
        print()#\n
        csi.executeApp()
    ## finish up ##
    csi.delete()
#

def make() -> None:
    while True:
        try:
            csAmnt = int(input('Input amount of .cs files: '))
            break
        except Exception:
            print('please put in a valid number.')

    csproj = input('Input the .csproj file: ')
    cs = [input(f'Input .cs file{i+1}: ') for i in range(csAmnt)]
    csi = makingCsi(csproj, cs)

    csi.packFile(csi.csproj, True)
    for cs in csi.cs:
        csi.packFile(cs, False)

    csiStep2 = decreaseFileSize(csi)
    csiStep2.removeComments()
    csiStep2.removeWhiteSpaceChar()
#

def cd(relative, path) -> str:
    if 'y' in relative:
        change = os.path.join(currDirPath, path)
        print('Changed to ',change)
        return change
    print('Changed to ',path)
    return path
    
def main() -> None:
    inp = input('\nDo you want to change directory, or run/make a csi file?(c/r/m)').lower()

    if 'c' in inp:
        currDirPath = cd(input('relative[compared to script] file path?(y/n): '), input('where to?: '))
    elif 'r' in inp:
        run()
    elif 'm' in inp:
        make()

    main()
#

if __name__ == '__main__':
    main()