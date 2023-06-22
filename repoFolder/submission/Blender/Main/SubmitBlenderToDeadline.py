#
#Copyright 2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 2 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

import bpy
import os
import subprocess

def GetDeadlineCommand():
    deadlineBin = ""
    try:
        deadlineBin = os.environ['DEADLINE_PATH']
    except KeyError:
        #if the error is a key error it means that DEADLINE_PATH is not set. however Deadline command may be in the PATH or on OSX it could be in the file /Users/Shared/Thinkbox/DEADLINE_PATH
        pass
        
    # On OSX, we look for the DEADLINE_PATH file if the environment variable does not exist.
    if deadlineBin == "" and  os.path.exists( "/Users/Shared/Thinkbox/DEADLINE_PATH" ):
        with open( "/Users/Shared/Thinkbox/DEADLINE_PATH" ) as f:
            deadlineBin = f.read().strip()

    deadlineCommand = os.path.join(deadlineBin, "deadlinecommand")
    
    return deadlineCommand

def GetRepositoryFilePath(subdir):
    deadlineCommand = GetDeadlineCommand()
    
    startupinfo = None
    #if os.name == 'nt':
    #   startupinfo = subprocess.STARTUPINFO()
    #   startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    args = [deadlineCommand, "-GetRepositoryFilePath "]   
    if subdir != None and subdir != "":
        args.append(subdir)
    
    # Specifying PIPE for all handles to workaround a Python bug on Windows. The unused handles are then closed immediatley afterwards.
    proc = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, startupinfo=startupinfo)

    proc.stdin.close()
    proc.stderr.close()

    output = proc.stdout.read()

    path = output.decode("utf_8")
    path = path.replace("\r","").replace("\n","").replace("\\","/")

    return path

def main( ):
    script_file = GetRepositoryFilePath("scripts/Submission/BlenderSubmission.py")

    curr_scene = bpy.context.scene
    curr_render = curr_scene.render    

    scene_file = str(bpy.data.filepath)
    
    if scene_file != "":
        bpy.ops.wm.save_mainfile()
    
    frame_range = str(curr_scene.frame_start)
    if curr_scene.frame_start != curr_scene.frame_end:
        frame_range = frame_range + "-" + str(curr_scene.frame_end)
    
    output_path = str(curr_render.frame_path( frame=curr_scene.frame_start ))
    threads_mode = str(curr_render.threads_mode)
    threads = curr_render.threads
    if threads_mode == "AUTO":
        threads = 0
    
    platform = str(bpy.app.build_platform)
    
    deadlineCommand = GetDeadlineCommand()
    
    args = []
    args.append(deadlineCommand)
    args.append("-ExecuteScript")
    args.append(script_file)
    args.append(scene_file)
    args.append(frame_range)
    args.append(output_path)
    args.append(str(threads))
    args.append(platform)
    
    startupinfo = None
    #~ if os.name == 'nt':
        #~ startupinfo = subprocess.STARTUPINFO()
        #~ startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    
    subprocess.Popen(args, startupinfo=startupinfo)
