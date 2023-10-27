import subprocess
import re
import os
import time
import shutil
import threading

constSeperator = '⇔'
constBuildCmd = 'dotnet build'
constFilePath = os.path.dirname(os.path.abspath(__file__))

class runningCsi:
    def __init__(self, fileName):
        self.fileName = fileName
        self.buildDir = os.path.join(constFilePath, fileName+'_NittyGritty')
    #

    def makeCsiFiles(self, csProjCont, csSourceCont):
        try:
            os.makedirs(self.buildDir)
            filesPath = os.path.join(self.buildDir, self.fileName)
            with open(filesPath+'.csproj', 'w', encoding='utf-8') as csproj:
                csproj.write(csProjCont)
            with open(filesPath+'.cs', 'w', encoding='utf-8') as cs:
                cs.write(csSourceCont)
        except Exception as e:
            print('\033[31m'+'Error seperating csi file into its parts! '+'\033[0m'+'\n', e)
    #

    def seperateCsi(self):
        try:
            csiCont = open(os.path.join(constFilePath, self.fileName+'.csi'), 'r', encoding='utf-8').read()
            parts = csiCont.split(constSeperator)
            if len(parts) != 5:
                print("Invalid .csi format. must contain first .csproj then .cs section. Both seperated with '⇔'.")

            csProjCont = parts[1]
            csSourceCont = parts[3]
            self.makeCsiFiles(csProjCont, csSourceCont)

            print('.csi initiated...')
        except FileNotFoundError:
            print('File was not found!')
    #

    def build(self):
        try:
            start = time.time()
            subprocess.run(constBuildCmd, cwd=self.buildDir, stdout=subprocess.DEVNULL, text=False)
            print('\033[32m'+f'Built in {time.time()-start} seconds.'+'\033[0m')
        except subprocess.CalledProcessError as e:
            print('\033[31m'+'Build error!'+'\033[0m'+'\n', e,)
        except Exception as e:
            print('Error during build\n',e)
    #

    def runningApp(self, exe):
        try:
            print('\033[33m'+'You can close by inputting "#"'+'\033[0m')
            def readOut(exe):
                while exe.poll() is None:
                    out = exe.stdout.readline()
                    if out:
                        print(out, end='')
            def readIn(exe):
                while exe.poll() is None:
                    if exe.stdin is not None:
                        uInput = input()
                        if uInput == '#':
                            print('closing...'), exe.kill()
                            break
                        exe.stdin.write(uInput), exe.stdin.flush()

            ## this has to be done on 2 seperate threads or else the input and output start blocking eachother ##
            outThread = threading.Thread(target=readOut, args=(exe,))
            inThread = threading.Thread(target=readIn, args=(exe,))
            outThread.start()
            inThread.start()
            outThread.join()
            inThread.join()

            print('\nClosed on exit code ', exe.returncode)
        except subprocess.CalledProcessError:
            print('Error occurred while running the csi')
    #

    def executeApp(self):
        def dotNetVers(file):
            try:
                csprojCont = open(os.path.join(self.buildDir, file + ".csproj"), 'r', encoding='utf-8').read()
                match = re.search(r'<TargetFramework>(.*?)</TargetFramework>', csprojCont)
                if not match:
                    raise Exception('TargetFramework not found in .csproj file!')

                return match.group(1)
            except subprocess.CalledProcessError as e:
                print('\033[31m'+'Error finding the .net version! '+'\033[0m', e)
                return None 
        try:
            print(dotNetVers(self.fileName))
            buildPath = os.path.join(self.buildDir, dotNetVers(self.fileName))
            self.runningApp(subprocess.Popen(os.path.join(buildPath, f'{self.fileName}.exe'), stdout=subprocess.PIPE, text=True))   
        except FileNotFoundError:
            print('File not found! have you tried having exe as your output? Or  moving the script to the same director as the csi?')
    #
    
    def delete(self):
        try:
            shutil.rmtree(self.buildDir)
        except Exception as e:
            print('\033[34m'+'coudlnt finish up and remove all the dirty work; oops')
            print('heres why though!\n'+'\033[0m',e)
    #

class makingCsi:
    def __init__(self, csproj, cs):
        self.csproj = os.path.join(constFilePath, csproj+".csproj")
        self.cs = os.path.join(constFilePath, cs+".cs")
        self.csi = open(os.path.join(constFilePath, csproj+'.csi'), 'a', encoding='utf-8')
    #

    @staticmethod
    def changeOutPath(csProjCont):
        ##  change out path  ##
        if '<OutputPath>' in csProjCont:
            outPattern = re.compile(r'<OutputPath>.*?</OutputPath>', re.DOTALL)
            csProjCont = outPattern.sub('<OutputPath>./</OutputPath>', csProjCont)
        ## add out path  ##
        else:
            outTypeMatch = re.search('<PropertyGroup>', csProjCont, re.DOTALL)
            if outTypeMatch:
                insertPoint = outTypeMatch.end()
                csProjCont = csProjCont[:insertPoint] + '\n    <OutputPath>./</OutputPath>' + csProjCont[insertPoint:]
        return csProjCont
    #

    def packCsProj(self):
        try:
            csProjCont = open(self.csproj, 'r', encoding='utf-8').read()
            csProjFinal = makingCsi.changeOutPath(csProjCont)

            self.csi.write(constSeperator)
            self.csi.write(csProjFinal)
            self.csi.write(constSeperator)
            
            print('\033[32m'+f'{self.csproj}.csproj packed into {self.csproj}.csi'+'\033[0m')
        except FileNotFoundError:
            print('File does not exist!')
        except Exception as e:
            print('\033[31m'+'Couldnt pack the csproj! '+'\033[0m',e)
    #
    
    def packCsSource(self):
        try:
            csSourceCont = open(self.cs, 'r', encoding='utf-8').read()
                
            self.csi.write('\n'+constSeperator)
            self.csi.write(csSourceCont)
            self.csi.write(constSeperator)
            
            print('\033[32m'+f'{self.cs}.cs packed into {self.csproj}.csi'+'\033[0m')
        except FileNotFoundError:
            print('Files does not exist!')
        except Exception as e:
            print('\033[31m'+'Error while packing the cs file! '+'\033[0m',e)
    #

def run():
    csi = runningCsi(input('Input the .csi file: '))
    csi.seperateCsi()
    csi.build()
    print()#\n
    csi.executeApp()
    ## finish up ##
    csi.delete()

def make():
    csi = makingCsi(input('Input the .csproj file: '), input('Input the .cs file: '))
    csi.packCsProj()
    csi.packCsSource()

def main():
    inp = input('\nDo you want to run or make a csi file?(r/m):').lower()
    if inp  == 'r':
        run()
    elif inp == 'm':
        make()
    
    main()

if __name__ == '__main__':
    main()