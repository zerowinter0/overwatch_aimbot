from ultralytics import YOLO
if __name__ == '__main__':
    model = YOLO('yolov8m.pt',task='train')
    ksplit = 5
    # 从文本文件中加载内容并存储到一个列表中
    ds_yamls = []
    with open('D:\\aimbot\data\\file_paths.txt', 'r') as f:
        for line in f:
            # 去除每行末尾的换行符
            line = line.strip()
            ds_yamls.append(line)

    # 打印加载的文件路径列表
    print(ds_yamls)


    results = {}
    for k in range(ksplit):
        dataset_yaml = ds_yamls[k]
        model.train(data=dataset_yaml, batch=5, epochs=150, imgsz=640, workers=8, single_cls=False, ) 
