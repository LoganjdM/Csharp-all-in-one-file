# C# "interpreter"/All in one (.csi)
Simple python script that allows you to stuff a .csproj and a .cs into one .csi, then when the .csi that holds the source code and is executable(kinda..). ![1](https://github.com/LoganjdM/Csharp-all-in-one-file/assets/138932791/848137f5-a761-4bdf-8299-e1a405fa56b7) ![2](https://github.com/LoganjdM/Csharp-all-in-one-file/assets/138932791/6c11e2a9-9389-4343-9487-afff853d6ced)

### Features
* Create a .csi file containing the source code and the project file.
* Build and execute directly from the csi file.
![2](https://github.com/LoganjdM/Csharp-all-in-one-file/assets/138932791/6c11e2a9-9389-4343-9487-afff853d6ced)

# Prerequisites
1. ![Python](https://www.python.org/) (*for the script*)
2. ![.NET SDK](https://dotnet.microsoft.com/en-us/download/visual-studio-sdks) (*for well.. the c#*)

# Usage
1. Clone/Download
2. Place C# project(and source file) in the project directory.
3. Open a terminal and navigate to the directory.
4. To package, input the "**m**" command.
5. To execute, input the "**r**" command.
## Example
An example number guessing game I generated with GPT and a simple hello world application is includedin examples, with project files included.

# Plans on forward
Just to improve this thing though I have some noticable plans
1. Right now you can only include one c# source file, I wish for this to be able to include multiple. should'nt be hard- just lazy
2. Not have to have the .csi in the same path as the python script.
3. Maybe file compression of some sort
