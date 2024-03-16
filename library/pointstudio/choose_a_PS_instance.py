"""Script which lists all running applications and asks the user to
select one of them. The script will connect to the application and
print all of the top-level objects contained in it.
 
If only one application is running, it will skip the application
selection step and connect to the application.
 
"""
 
from mapteksdk.project import Project
 
# Get a list of running applications.
applications = Project.find_running_applications()
 
for i, application in enumerate(applications):
  print(f"{i} - {application.bin_path}")
 
if len(applications) == 1:
  print("Only one application running - automatically connecting")
  index = 0
else:
  index = int(input("Which application do you want to connect to?\n"))
 
try:
  instance = applications[index]
except IndexError as error:
  raise IndexError(f"No application with index: {index}") from error
 
project = Project(existing_mcpd=instance)
 
for name, oid in project.get_children():
  print(name, oid)