# Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this
# software and associated documentation files (the "Software"), to deal in the Software
# without restriction, including without limitation the rights to use, copy, modify,
# merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))  # noqa
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'launch'))  # noqa

import launch

from launch_ros import get_default_launch_description
import launch_ros.actions

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import ThisLaunchFileDir
from launch.actions import ExecuteProcess
from launch.substitutions import LaunchConfiguration
# Added for gazebo_ros -- spawn entity node 
from launch_ros.actions import Node

import lifecycle_msgs.msg


def generate_launch_description():
    gui = LaunchConfiguration('gui', default='true')
    paused = LaunchConfiguration('paused', default='false')
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    headless = LaunchConfiguration('headless', default='false')
    debug = LaunchConfiguration('debug', default='false')
    verbose = LaunchConfiguration('verbose', default='true')
    
    world_file_name = 'small_house.world'
    package_dir = get_package_share_directory('aws_robomaker_small_house_world')
    world = os.path.join(package_dir, 'worlds', world_file_name)
    launch_file_dir = os.path.join(get_package_share_directory('turtlebot3_simulation_description'), 'models','turtlebot3_waffle/model.sdf')
    # GAZEBO_MODEL_PATH has to be correctly set for Gazebo to be able to find the model
    # ros2 run gazebo_ros spawn_entity.py -entity myentity -x 7.5 -y 1.2 -z 0 -file src/turtlebot3_simulation_description/models/turtlebot3_waffle/model.sdf 
    spawn_entity = Node(package='gazebo_ros', node_executable='spawn_entity.py',
                        arguments=['-entity', 'myentity', '-x','6.5','-y','-0.3','-z','0','-file',launch_file_dir],
                        output='screen')
    
    return LaunchDescription([       
        ExecuteProcess(
            # cmd=['gazebo', world, '-s', 'libgazebo_ros_init.so','libgazebo_ros_state.so','libgazebo_ros_factory.so', gui, paused, use_sim_time, headless, debug, verbose],
            cmd=['gazebo', world, '-s','libgazebo_ros_factory.so','libgazebo_ros_init.so','libgazebo_ros_state.so', gui, paused, use_sim_time, headless, debug, verbose],
            output='screen'),
        spawn_entity,
    ])

if __name__ == '__main__':
    generate_launch_description()