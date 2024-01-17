'''
In this code, we represent in matplotlyb some lounches, use json to read the information of each flight, and give some usefull information like max height.
'''
import math
import json
import PySimpleGUI as sg
import matplotlib.pyplot as plt
import numpy as np

# Here we use the json file data to calculate all trajectories of the each projectile. Also we use trigonometry and cinematics to calculate them

def calculate_trajectory(initial_velocity, launch_angle):
    g = 9.8  # acceleration due to gravity (m/s^2)
    launch_angle_rad = math.radians(launch_angle)
    
    # Calculate time of flight
    time_of_flight = (2 * initial_velocity * math.sin(launch_angle_rad)) / g
    
    # Calculate horizontal range
    horizontal_range = initial_velocity * math.cos(launch_angle_rad) * time_of_flight
    
    # Calculate maximum height
    max_height = (initial_velocity**2 * math.sin(launch_angle_rad)**2) / (2 * g)
    
    return time_of_flight, horizontal_range, max_height

# Here we define the variables calcullated to use them in matplotlib

def plot_trajectory(initial_velocity, launch_angle):
    g = 9.8 
    launch_angle_rad = math.radians(launch_angle)
    
    # Time intervals for plotting
    time_intervals = np.linspace(0, (2 * initial_velocity * math.sin(launch_angle_rad)) / g, num=100)
    
    # Calculate x and y positions at each time interval for matplotlib
    x_positions = initial_velocity * np.cos(launch_angle_rad) * time_intervals
    y_positions = initial_velocity * np.sin(launch_angle_rad) * time_intervals - 0.5 * g * time_intervals**2
    
    # Plot the trajectory
    plt.plot(x_positions, y_positions, label=f'Launch - V: {initial_velocity} m/s, θ: {launch_angle}°')

# Here we create the layout and interface of the screen

def main():
    layout = [
        [sg.Text('Select JSON input file:'), sg.InputText(key='file_path'), sg.FileBrowse()],
        [sg.Button('Analyze'), sg.Button('Exit')],
        [sg.Output(size=(80, 15))]
    ]

    window = sg.Window('Projectile Analysis', layout)

    while True:
        event, values = window.read()

        if event in (sg.WINDOW_CLOSED, 'Exit'):
            break
        elif event == 'Analyze':
            file_path = values['file_path']

            try:
                with open(file_path, 'r') as file:
                    data = json.load(file)

                max_height_launch = None
                max_height_value = 0

                # Initialize the plot
                plt.figure()
                plt.title('Projectile Trajectories')
                plt.xlabel('Horizontal Distance (m)')
                plt.ylabel('Vertical Distance (m)')

                for i, launch in enumerate(data['launches'], 1):
                    initial_velocity, launch_angle = launch['initial_velocity'], launch['launch_angle']
                    time_of_flight, horizontal_range, max_height = calculate_trajectory(initial_velocity, launch_angle)

                    print(f"\nLaunch #{i}:")
                    print(f"Initial Velocity: {initial_velocity} m/s")
                    print(f"Launch Angle: {launch_angle} degrees")
                    print(f"Time of Flight: {time_of_flight:.2f} seconds")
                    print(f"Horizontal Range: {horizontal_range:.2f} meters")
                    print(f"Maximum Height: {max_height:.2f} meters")
                    print(f"Maximum Distance: {horizontal_range:.2f} meters")
                    print("=" * 40)

                    # Plot the trajectory for each launch
                    plot_trajectory(initial_velocity, launch_angle)

                    # Identify launch with the highest maximum height
                    if max_height > max_height_value:
                        max_height_value = max_height
                        max_height_launch = i

                    # Identify launches with flight time exceeding 5 seconds
                    if time_of_flight > 5:
                        print(f"Flight time exceeds 5 seconds for Launch #{i}")

                print("\nSummary:")
                print(f"Launch with the highest maximum height: #{max_height_launch} ({max_height_value:.2f} meters)")

                # Show the plot
                plt.legend()
                plt.grid(True)
                plt.show()

            except Exception as e:
                print(f"Error: {e}")

    window.close()

if __name__ == '__main__':
    main()
