import shutil

total, used, free = shutil.disk_usage("/")

print("Total: %d GiB" % (total // (2**30)))
print("Used: %d GiB" % (used // (2**30)))
print("Free: %d GiB" % (free // (2**30)))



import psutil

obj_Disk = psutil.disk_usage('/')

print (obj_Disk.total / (1024.0 ** 3))
print (obj_Disk.used / (1024.0 ** 3))
print (obj_Disk.free / (1024.0 ** 3))
print (obj_Disk.percent)
