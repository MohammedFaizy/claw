import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.conditions import IfCondition
from launch.conditions import UnlessCondition
from launch_ros.actions import Node
import xacro


def generate_launch_description():

    # Specify the name of the package and path to xacro file within the package
    
    pkg_name = 'claw'
    
    file_subpath = 'description/example_robot.urdf.xacro'
    rviz_subpath = 'rviz/Config4.rviz'

    use_gui_arg = DeclareLaunchArgument(
        'use_gui', default_value = 'true',
        description= 'Use joint_state_publisher_gui if true, else joint_state_publisher')
        
    use_rviz_arg = DeclareLaunchArgument(
        'use_rviz', default_value='true',
        description='Launch RViz2 if true')
        
    use_sim_time_arg = DeclareLaunchArgument(
        'use_sim_time', default_value = 'false',
        description = 'If true, nodes will use the /clock topic')
        
    use_gui = LaunchConfiguration('use_gui')
    use_rviz = LaunchConfiguration('use_rviz')
    use_sim_time = LaunchConfiguration('use_sim_time')


    # Use xacro to process the file
    xacro_file = os.path.join(get_package_share_directory(pkg_name),file_subpath)
    robot_description_raw = xacro.process_file(xacro_file).toxml()


    # Configure the node
    node_rsp = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_description_raw,
                     'use_sim_time':use_sim_time}] # add other parameters here if    required
    )
    
    node_jsp = Node(
      condition = UnlessCondition(use_gui),
      package='joint_state_publisher',
      executable='joint_state_publisher',
      output='screen',
      parameters=[{'use_sim_time': use_sim_time}])
      
    
    node_jsp_gui = Node(
      condition = IfCondition(use_gui),
      package='joint_state_publisher_gui',
      executable='joint_state_publisher_gui',
      output='screen',
      parameters=[{'use_sim_time': use_sim_time}])
     
    rviz_config= os.path.join(get_package_share_directory('claw'),rviz_subpath) 
    
    node_rviz= Node(
      condition= IfCondition(use_rviz),
      package='rviz2',
      executable='rviz2',
      output='screen',
      arguments=['-d', rviz_config],
      parameters=[{'use_sim_time': use_sim_time}])
      
    # Run the node
    return LaunchDescription([
        use_gui_arg, use_rviz_arg, use_sim_time_arg,
        node_rsp, node_jsp, node_jsp_gui, node_rviz
    ])
