# B3D-Gamepad-Control-Akimo's Version
Blender 3D Add-on to control camera with a gamepad

* copy the folder to this position C:\Users\Your Name\AppData\Roaming\Blender Foundation\Blender\Your Version\scripts\addons
* Activate it in Edit - Preference
* In the 3d Viewport press Numpad 0 (Camera View)
* Press F3 (Search Menu) and look after "View3D:   Gamepad Control"
* Use your gamepad trigger and joystick to move your camera smoothly.


# **Key Binding**
Control | Description
------------ | -------------
Left X | Move left right
Left Y | Move forward back
Left Trigger | Move Down
Right Trigger | Move Up
Right X | Yaw
Right Y | Pitch
RB | Roll Right(currently not supported in Euler System)
LB | Roll Left (currently not supported in Euler System)
Key X |  2X Zoom UP On/Off
Key A |  Zoom + (fov -5)
Key B |  Zoom - (fov +5)
Left Stick Press | Speed x2
Right Stick Press | Speed /2
Cross Up | Speed x1.2
Cross Down| Speed /1.2
Cross Left  | Rotate speed -20%
Cross Right | Rotate speed +20%

# **Flying Mode**
Key Y | Switch Mode  

There are 3 Modes:  
Horizontal ---- move horizontally and vertically, like a infantry, or a DJI drone  
Heading with vertical Up Down ---- move forward to where you are heading, but still vertical Up Down  
Heading ---- move forward to where you are heading, like a FPV drone  

# **Drifting Problem**
If your gamepad is old with drifting, change these 4 lines '''if abs(gpd_value) < 100 :''' to higher value like 300, 1000...  
Same solution for Left Right Trigger. Simply add if '''abs(gpd_value) < 10: gpd_value = 0'''

# **Blender Version**
If your blender version doesn't support it, change line 13 "blender": (2, 80, 0), to your own blender version

QUATERNION Mode will be developed soon with physics for types of Aircraft,  
FPV drone, Helicopter, Fixed Wing, Space ship, Sci fi Vector propulsion ship etc.  
Means you can fly aircraft with physics in Blender! ;->  
nice way to animate vehicles.  

Thanks for the original work from Fabuloup  
https://github.com/Fabuloup/B3D-Gamepad-Control  
https://www.reddit.com/r/blender/comments/ifuy7k/blender_addon_gamepad_camera_control/  

