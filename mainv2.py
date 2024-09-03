import os
import subprocess
from shutil import copyfile

def make_executable(file_path):
    os.chmod(file_path, os.stat(file_path).st_mode | 0o111)

def create_desktop_entry(app_name, app_image_path, icon_path):
    desktop_entry = f"""
    [Desktop Entry]
    Name={app_name}
    Exec={app_image_path}
    Type=Application
    Terminal=false
    """
    if icon_path:
        desktop_entry += f"Icon={icon_path}\n"
    return desktop_entry.strip()

def save_desktop_file(desktop_content, file_path):
    with open(file_path, 'w') as file:
        file.write(desktop_content)

def main():
    # Gather user input
    app_name = input("Enter the application name: ")
    app_image_path = input("Enter the full path to the AppImage: ")
    
    # Ask if the user has an icon
    has_icon = input("Do you have an icon for the application? (yes/no): ").lower().strip()
    
    if has_icon == 'yes':
        icon_path = input("Enter the full path to the icon: ")
    else:
        icon_path = ""  # Set to empty string if no icon is provided

    # Make AppImage executable
    make_executable(app_image_path)

    # Paths for the .desktop file
    desktop_file_name = f"{app_name}.desktop"
    local_applications_dir = os.path.expanduser("~/.local/share/applications")
    desktop_dir = os.path.expanduser("~/Desktop")

    # Create .desktop file content
    desktop_entry = create_desktop_entry(app_name, app_image_path, icon_path)

    # Save .desktop file to local applications directory
    desktop_file_path = os.path.join(local_applications_dir, desktop_file_name)
    save_desktop_file(desktop_entry, desktop_file_path)

    # Copy .desktop file to the Desktop
    desktop_file_desktop_path = os.path.join(desktop_dir, desktop_file_name)
    copyfile(desktop_file_path, desktop_file_desktop_path)

    # Make the .desktop file on the Desktop executable
    make_executable(desktop_file_desktop_path)

    # Refresh the applications menu
    subprocess.run(['update-desktop-database', local_applications_dir])
    print(f"{app_name} has been added to your applications menu and Desktop.")

if __name__ == "__main__":
    main()
