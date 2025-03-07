import numpy as np
import matplotlib.pyplot as plt
from lib import detector as d
from lib import particles as p
from lib import experiments as e
from lib import source as s

# File path to save the output spectrum plot
file_path = "/mnt/c/Users/User/Desktop/info/Compton/Simulation/plots/"

def plot_energy_spectrum(energies, fileNamePNG, bins=100, title="Energy Spectrum"):
    """
    Plots a histogram of the detected photon energies.
    
    :param energies: List of detected photon energies in keV.
    :param fileNamePNG: File path to save the plot as a PNG image.
    :param bins: Number of bins for the histogram.
    :param title: Title of the plot.
    """
    # Filter out energies less than or equal to 1 keV, which might be noise or irrelevant
    energies_def = [energy for energy in energies if energy > 1]

    if not energies_def:
        print("No energies to plot.")
        return

    # Create a histogram of detected energies
    plt.figure(figsize=(10, 6))
    plt.hist(energies_def, bins=bins, color="blue", alpha=0.7, edgecolor="blue")
    
    # PP ---> Photopeak, CE ---> Compton Edge
    # Mark the photopeak (PP) and Compton Edge (CE) for the energies of interest
    plt.axvline(511, color='red', linestyle='--', linewidth=1.5, label='PP for 511 keV')
    plt.axvline(1274, color='red', linestyle='--', linewidth=1.5, label='PP for 1274 keV')
    plt.axvline(341, color='orange', linestyle='--', linewidth=1.5, label='CE for 511 keV') # 2/3 511
    plt.axvline(1061, color='orange', linestyle='--', linewidth=1.5, label='CE for 1274 keV') 
    plt.legend(loc="upper right")

    # Set plot title and labels
    plt.title(title, fontsize=16)
    plt.xlabel("Energy (keV)", fontsize=14)
    plt.ylabel("Counts", fontsize=14)
    plt.yscale("log")  # Log scale for better visibility of data
    plt.grid(alpha=0.4)  # Grid for readability
    plt.tight_layout()  # Adjust layout to fit everything
    plt.savefig(fileNamePNG)  # Save the plot as PNG
    plt.close()  # Close the plot to free up resources

def visualization_3D(fileNamePNG, detectors, photons, target=None):
    """
    Creates a 3D visualization of the photon hit points and detector positions.
    
    :param fileNamePNG: Path to save the output 3D visualization image.
    :param detectors: List of detector objects.
    :param photons: List of photon objects, each with a position attribute.
    :param target: Optional target object to visualize.
    """
    hit_points = np.array([photon.position for photon in photons])  # Extract photon hit positions
    
    # 3D Plot of photon hit points
    fig = plt.figure(figsize=(16, 12))
    ax = fig.add_subplot(221, projection='3d')
    ax.scatter(hit_points[:, 0], hit_points[:, 1], hit_points[:, 2], s=10, color='red', marker='x', label='Hit Points')  # Red X
    [detector.draw_detector_3D(ax) for detector in detectors]  # Draw 3D detectors
    if target:
        target.draw_target_3D(ax)  # Draw 3D target if available
    ax.set_xlabel('X (cm)')
    ax.set_ylabel('Y (cm)')
    ax.set_zlabel('Z (cm)')
    ax.set_title('3D Photon Hit Positions')
    ax.legend(loc='upper right')
    
    # 2D Projections on different planes
    ax_xy = fig.add_subplot(222)
    ax_xy.scatter(hit_points[:, 0], hit_points[:, 1], s=20, color='red', marker='x', label='Hits in XY')  # Red X
    [detector.draw_detector_2D(ax_xy, plane='xy') for detector in detectors]
    if target:
        target.draw_target_2D(ax_xy, plane='xy')
    ax_xy.set_xlabel('X (cm)')
    ax_xy.set_ylabel('Y (cm)')
    ax_xy.set_title('Projection on XY Plane')
    ax_xy.grid()
    ax_xy.legend(loc='upper right')

    ax_xz = fig.add_subplot(223)
    ax_xz.scatter(hit_points[:, 0], hit_points[:, 2], s=20, color='red', marker='x', label='Hits in XZ')  # Red X
    [detector.draw_detector_2D(ax_xz, plane='xz') for detector in detectors]
    if target:
        target.draw_target_2D(ax_xz, plane='xz')
    ax_xz.set_xlabel('X (cm)')
    ax_xz.set_ylabel('Z (cm)')
    ax_xz.set_title('Projection on XZ Plane')
    ax_xz.grid()
    ax_xz.legend(loc='upper right')

    ax_yz = fig.add_subplot(224)
    ax_yz.scatter(hit_points[:, 1], hit_points[:, 2], s=20, color='red', marker='x', label='Hits in YZ')  # Red X
    [detector.draw_detector_2D(ax_yz, plane='yz') for detector in detectors]
    if target:
        target.draw_target_2D(ax_yz, plane='yz')
    ax_yz.set_xlabel('Y (cm)')
    ax_yz.set_ylabel('Z (cm)')
    ax_yz.set_title('Projection on YZ Plane')
    ax_yz.grid()
    ax_yz.legend(loc='upper right')

    plt.savefig(fileNamePNG)  # Save the 3D visualization as PNG
    plt.close()

# Initialize detectors with their respective positions and dimensions
ugo = d.Detector([0, 15, 0], 1.27, 2.58, 0.0903)  # Detector "Ugo"
franco = d.Detector([0, -15, 0], 2.54, 5.08, 0.0695)  # Detector "Franco"

number_of_photons = 1000000  # Number of photons to simulate

# Simulate spectroscopy measurements and plot the energy spectrum 
energies = e.spectroscopy_measurement(number_of_photons, ugo, s.Source(), True)
plot_energy_spectrum(energies, file_path + "spectrum/spettroscopy_ugo.png", 10000)
energies = e.spectroscopy_measurement(number_of_photons, franco, s.Source(), True)
plot_energy_spectrum(energies, file_path + "spectrum/spettroscopy_franco.png", 10000)

print("End spettroscopy")

# Simulate coincidence measurement and plot the energy spectrum
energies = e.coincidence_measurement(number_of_photons, ugo, franco, s.Source({511: 1, 1274: 0}), True)
plot_energy_spectrum(energies, file_path + "spectrum/coincidence_spectrum.png", 10000)

# Simulate photon emission from a source
source = s.Source()  # Create a source object
photons = source.photon_emission(1000)  # Simulate photon emission
[photon.propagation(np.linalg.norm(franco.position)) for photon in photons]  # Propagate the photons

# Visualize the 3D photon hit positions and detectors for coincidence measurement
visualization_3D(file_path + "3D_plots/coincidence_3D_visualization.png", [ugo, franco], photons)
print("End coicidence")

print("End")

