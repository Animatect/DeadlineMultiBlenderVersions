# DeadlineMultiBlenderVersions
Modification of deadline blender plugin to handle multiple Blender versions

This files should be copied and pasted in the deadline repository ovewriting the files in the same structure with the same Name.
The folder called repoFolder serves as a proxy for the actual repository folder on the deadline server.

The modification made to the submission process is basically that when the blender client addon calls the submitBlenderToDeadline Script, whe capture the blender version, pass it piggybagged in the output file argument to the BlenderSubmission script and there we write it to the .job file to pass it to the Blender.py script where we modify the logic to take the version into account.

Finally on the Blender.param file we add an entry using the format [Blender_X.X_RenderExecutable] where X.X is the version ignoring any number after the firs two.

I'm adding version executables from 3.3 to 4.0 but feel free to add as meny as you like.

Example:

[Blender_3.3_RenderExecutable]
Type=multilinemultifilename
Label=Blender 3.3 Executable
Category=Render Executables
CategoryOrder=0
Default=C:\Program Files\Blender Foundation\Blender 3.3\blender.exe;C:\Program Files (x86)\Blender Foundation\Blender 3.3\blender.exe;/Applications/Blender 3.3/blender.app/Contents/MacOS/blender;/usr/local/Blender 3.3/blender
Description=The path to the Blender executable file used for rendering. Enter alternative paths on separate lines.