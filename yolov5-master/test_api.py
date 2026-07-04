from ultralytics.utils.patches import torch_load
import torch

model = torch.hub.load('.', 'custom', r'C:\Users\h2\Desktop\work\P4\yolov5-master\weights\yolov5s.pt', source='local')
results = model([r'C:\Users\h2\Desktop\work\P4\yolov5-master\data\images\bus.jpg',r'C:\Users\h2\Desktop\work\P4\yolov5-master\data\images\zidane.jpg'])
# print(results)
print(results.pandas().xyxy[0])
# print(results.pandas().xyxy[0].shape)
# results.print()
# results.show()