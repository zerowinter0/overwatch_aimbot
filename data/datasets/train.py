from ultralytics import YOLO
#from ultralytics import YOLOv10
if __name__ == '__main__':
# Load a model
    #model = YOLO('yolov8n.yaml')  # build a new model from YAML
    model = YOLO('yolov8n.yaml')  # load a pretrained model (recommended for training)
    #model = YOLOv10('yolov10n.yaml')
    #model = YOLO('yolov8n.yaml').load('yolov8n.pt')  # build from YAML and transfer weights
    # Train the model
    # model.train(data='D:/aimbot/data/datasets/mydata.yaml', epochs=1000, imgsz=640)
    model.train(data='D:\\aimbot\data\datasets\data\overwatch.v2i.yolov8\data.yaml', epochs=1000, imgsz=640,batch=5)