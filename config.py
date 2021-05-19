DATASET_FOLDER = 'synImgs'
INPUT_CHANNEL = 3 if DATASET_FOLDER=='synImgs' else 1
LOCA_STRIDE     = 8
LOCA_CLASSES    = {0: "crazyflie"}
TRAIN_ANNOT_PATH    = "./dataset/{}/train.txt".format(DATASET_FOLDER)
TRAIN_BATCH_SIZE    = 3
TRAIN_INPUT_SIZE    = [320, 224]
TRAIN_LR_INIT       = 1e-3
TRAIN_LR_END        = 1e-6
TRAIN_WARMUP_EPOCHS = 2
TRAIN_EPOCHS        = 3