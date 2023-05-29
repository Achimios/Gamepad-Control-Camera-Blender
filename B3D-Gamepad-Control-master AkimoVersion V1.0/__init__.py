#加俩代码
#上下+-移速，左右+-视角速度，LS/RS 2倍/0.5倍移速，LB/RB左右翻滚，
#Y切换飞行模式（无人机还是穿越机？）

#研究物理性（行走，驾驶，飞行）


bl_info = {
    "name": "Gamepad Control",
    "description": "Allows you to control the camera with your gamepad.",
    "author": "Fabien RICHARD & Leo Akimo",
    "version": (1, 1),
    "blender": (2, 80, 0),
    "category": "3D View",
}

import bpy
import time
import math
import threading
from .inputs import get_gamepad
from mathutils import Vector
from mathutils import Quaternion

events = [];
_t = None;

def worker():
    global events
    while True :
        events.append(get_gamepad())
                
class GamepadControl(bpy.types.Operator):
    """Gamepad Control"""
    bl_idname = "view3d.gamepad_control"
    bl_label = "Gamepad_control"
    bl_space_type = "View_3D"
    bl_region_type = "UI"
    bl_category = "Gamepad_control"

    _timer = None
    
    move = {
        'x':0,
        'y':0,
        'z':0,
        'yaw':0,
        'pitch':0,
        'roll':0
    }

    xMove = 0
    yMove = 0
    zDown = 0
    zUp = 0

    Yaw = 0
    Pitch = 0
    RollDown = 0
    RollUp = 0

    movement_speed = {
        'x':0.12,
        'y':0.12,
        'z':0.08
    }
    rotation_speed = {
        'yaw':1.8,
        'pitch':1.8,
        'roll':1.2
    }
    mSpeedAll = 1
    rSpeedAll = 1
    flyMode = 1
    Scope = False
    def execute(self, context):
        global _t
        if not _t :
            _t = threading.Thread(target=worker)
            _t.daemon = True  # 设置线程为守护线程
            _t.start()


        wm = context.window_manager
        self._timer = wm.event_timer_add(0.01, window=context.window)
        wm.modal_handler_add(self)

        return {'RUNNING_MODAL'}
    
    def cancel(self, context):
        wm = context.window_manager
        wm.event_timer_remove(self._timer)

    def modal(self, context, event):
        #catch gamepad input here
        global events

        cam_obj = bpy.context.scene.camera

        if event.type in {'RIGHTMOUSE', 'ESC'}:
            self.cancel(context)
            return {'CANCELLED'}

        if event.type == 'TIMER':
            #worker()
            while len(events) > 0 :
                for event in events[0]:
                    gpd_input = ""
                    gpd_value = event.state
                    #Move
                    if event.code == "ABS_X":
                        gpd_input = "Left Stick X"
                        if abs(gpd_value) < 100 :
                            gpd_value = 0
                        self.xMove = (float(gpd_value)/32768.0)*self.movement_speed['x']
                    elif event.code == "ABS_Y":
                        gpd_input = "Left Stick Y"
                        if abs(gpd_value) < 100 :
                            gpd_value = 0
                        self.yMove = (float(gpd_value)/32768.0)*self.movement_speed['y']
                    #Ascend
                    elif event.code == "ABS_Z":
                        gpd_input = "Left Trigger"
                        self.zDown = -(float(gpd_value)/255.0)*self.movement_speed['z']
                    elif event.code == "ABS_RZ":
                        gpd_input = "Right Trigger"
                        self.zUp = (float(gpd_value)/255.0)*self.movement_speed['z']

                    #Yaw
                    elif event.code == "ABS_RX":
                        gpd_input = "Right Stick X"
                        if abs(gpd_value) < 100 :
                            gpd_value = 0
                        self.Yaw = -(float(gpd_value)/32768.0)*self.rotation_speed['yaw']
                    #Pitch
                    elif event.code == "ABS_RY":
                        gpd_input = "Right Stick Y"
                        if abs(gpd_value) < 100 :
                            gpd_value = 0
                        self.Pitch = (float(gpd_value)/32768.0)*self.rotation_speed['pitch']
                    # Roll
                    elif event.code == "BTN_TL":
                        gpd_input = "LB"
                        if gpd_value == 1:
                            self.RollDown = -self.rotation_speed['roll']
                        else:
                            self.RollDown = 0
                    elif event.code == "BTN_TR":
                        gpd_input = "RB"
                        if gpd_value == 1:
                            self.RollUp = self.rotation_speed['roll']
                        else:
                            self.RollUp = 0

                    #Move Speed Mul/Div 2
                    elif event.code == "BTN_THUMBL":
                        gpd_input = "LS"
                        if gpd_value == 1:
                            self.mSpeedAll *= 2
                    elif event.code == "BTN_THUMBR":
                        gpd_input = "RS"
                        if gpd_value == 1:
                            self.mSpeedAll /= 2
                    #Move Speed Mul/Div 1.2
                    elif event.code == "ABS_HAT0Y":
                        gpd_input = "DPad Up Down"
                        if gpd_value == -1:
                            self.mSpeedAll *= 1.2
                        elif gpd_value == 1:
                            self.mSpeedAll /= 1.2
                    #Rotate Speed +- 0.2
                    elif event.code == "ABS_HAT0X":
                        gpd_input = "DPad Left Right"
                        if gpd_value == -1:
                            self.rSpeedAll -= 0.2
                        elif gpd_value == 1:
                            self.rSpeedAll += 0.2

                    # X 1/2FOV, like Scope in games
                    elif event.code == "BTN_WEST":
                        gpd_input = "X"
                        if gpd_value == 1:
                            self.Scope = not self.Scope
                            if self.Scope == True:
                                cam_obj.data.angle /= 2
                            else:
                                cam_obj.data.angle *= 2
                    # B FOV+
                    elif event.code == "BTN_EAST":
                        gpd_input = "Key B"
                        if gpd_value == 1:
                            cam_obj.data.angle += 0.1745329
                    # A FOV-
                    elif event.code == "BTN_SOUTH":
                        gpd_input = "Key A"
                        if gpd_value == 1:
                            cam_obj.data.angle -= 0.1745329

                    #3 Mode Switch(Horizontal, Heading with Vertical Ascend, Heading)
                    elif event.code == "BTN_NORTH":
                        gpd_input = "Key Y"
                        if gpd_value == 1:
                            self.flyMode += 1
                        if self.flyMode > 3:
                            self.flyMode = 1
                            #cam_obj.rotation_mode = 'XYZ'
                            #cam_obj.rotation_euler[1] = 0#reset Roll cuz not good in Horizontal mode & Euler System



                events.pop(0)


            self.move['x'] = self.xMove*self.mSpeedAll# I remap xMove to move['x'] to avoid some jiggle problem
            self.move['y'] = self.yMove*self.mSpeedAll
            self.move['z'] = (self.zDown + self.zUp)*self.mSpeedAll
            # Handle translation first
            if self.flyMode == 1:
                theta = cam_obj.rotation_euler[2]
                cam_obj.location.x += self.move['x']*math.cos(theta)-self.move['y']*math.sin(theta)
                cam_obj.location.y += self.move['x']*math.sin(theta)+self.move['y']*math.cos(theta)
                cam_obj.location.z += self.move['z']
            if self.flyMode == 2:
                move_vector = Vector((self.move['x'], 0, -self.move['y']))
                cam_obj.matrix_world.translation += cam_obj.matrix_world.to_3x3() @ move_vector
                cam_obj.location.z += self.move['z']
                cam_obj.keyframe_insert(data_path="location")
            if self.flyMode == 3:
                move_vector = Vector((self.move['x'], self.move['z'], -self.move['y']))
                cam_obj.matrix_world.translation += cam_obj.matrix_world.to_3x3() @ move_vector
                cam_obj.keyframe_insert(data_path="location")


            self.move['yaw'] = self.Yaw*self.rSpeedAll/0.69*cam_obj.data.angle#Keep Same Visual Speed after changing FOV, like in FPS games
            self.move['pitch'] = self.Pitch*self.rSpeedAll/0.69*cam_obj.data.angle
            self.move['roll'] = -(self.RollUp + self.RollDown) * self.rSpeedAll

            if self.flyMode < 4:
                if cam_obj.rotation_mode != 'XYZ':
                    cam_obj.rotation_mode = 'XYZ'
                cam_obj.rotation_euler[0] += self.move['pitch']*(math.pi / 180.0)
                #cam_obj.rotation_euler[1] -= self.move['roll']*(math.pi / 180.0)
                #I dont suggest change roll in Euler System Mode
                #if you want to roll the world, you can parent a tilted object to the cam
                #if you want to only roll the view, you give a child cam to the original cam, roll the child cam and use its view, 
                #it need to change cam_obj = bpy.context.scene.objects.get('Pcam'), Pcam is the parent cam's name
                #then add cam_child_obj = bpy.context.scene.objects.get('Ccam')
                #then here cam_child_obj.rotation_euler[1] -= self.move['roll']*(math.pi / 180.0)
                #and X A B keys' fov setting should also use cam_child_obj instead of cam_obj
                cam_obj.rotation_euler[2] += self.move['yaw']*(math.pi / 180.0)
                cam_obj.keyframe_insert(data_path="rotation_euler")
            #QUATERNION Mode. Preserved for Aircraft Mode
            else:
                # Then handle rotation
                if cam_obj.rotation_mode != 'QUATERNION':
                    cam_obj.rotation_mode = 'QUATERNION'
                #Yaw
                if self.move['yaw'] != 0:
                    axis = cam_obj.matrix_world.to_quaternion() @ Vector((0.0, 1.0, 0.0))
                    roll_quat = Quaternion(axis, math.radians(self.move['yaw']))
                    cam_obj.rotation_quaternion = roll_quat @ cam_obj.rotation_quaternion
                #Pitch
                if self.move['pitch'] != 0:
                    axis = cam_obj.matrix_world.to_quaternion() @ Vector((1.0, 0.0, 0.0))
                    roll_quat = Quaternion(axis, math.radians(self.move['pitch']))
                    cam_obj.rotation_quaternion = roll_quat @ cam_obj.rotation_quaternion
                #Roll
                if self.move['roll'] != 0:
                    axis = cam_obj.matrix_world.to_quaternion() @ Vector((0.0, 0.0, 1.0))
                    roll_quat = Quaternion(axis, math.radians(self.move['roll']))
                    cam_obj.rotation_quaternion = roll_quat @ cam_obj.rotation_quaternion

                cam_obj.keyframe_insert(data_path="rotation_quaternion")


        return {'PASS_THROUGH'}

def menu_func(self, context):
    self.layout.operator(GamepadControl.bl_idname)

def register():
    bpy.utils.register_class(GamepadControl)
    bpy.types.VIEW3D_MT_object.append(menu_func)


def unregister():
    bpy.utils.unregister_class(GamepadControl)

if __name__ == "__main__":
    register()