from data_provider.data_loader import Dataset_ETT_hour, Dataset_ETT_minute, Dataset_Custom, Dataset_Solar, Dataset_PEMS, \
    Dataset_Pred
from torch.utils.data import DataLoader

data_dict = {
    'ETTh1': Dataset_ETT_hour,
    'ETTh2': Dataset_ETT_hour,
    'ETTm1': Dataset_ETT_minute,
    'ETTm2': Dataset_ETT_minute,
    'Solar': Dataset_Solar,
    'PEMS': Dataset_PEMS,
    'custom': Dataset_Custom,
}


def data_provider(args, flag):
    Data = data_dict[args.data]
    timeenc = 0 if args.embed != 'timeF' else 1
    if flag == 'pred' :
        shuffle_flag = False
        drop_last = False
        batch_size = 1
        freq = args.freq
        Data = Dataset_Pred
        data_set = Data(
            root_path=args.pred_root_path,
            data_path=args.pred_data_path,
            flag=flag,
            size=[args.seq_len, args.label_len, args.pred_len],
            features=args.features,
            target=args.target,
            timeenc=timeenc,
            freq=freq,
            kind_of_scaler=args.kind_of_scaler,
            name_of_col_with_date = args.name_of_col_with_date,
            scale = args.scale,
            max_use_of_row = args.max_use_of_row if hasattr(args, 'max_use_of_row') else 'No Lim',
        )
        print(flag, len(data_set))
    else:
        if flag == 'test':
            shuffle_flag = False
            drop_last = True
            batch_size = 1  # bsz=1 for evaluation
            freq = args.freq
        else:
            shuffle_flag = True
            drop_last = True
            batch_size = args.batch_size  # bsz for train and valid
            freq = args.freq
        data_set = Data(
            root_path=args.root_path,
            data_path=args.data_path,
            flag=flag,
            size=[args.seq_len, args.label_len, args.pred_len],
            features=args.features,
            target=args.target,
            timeenc=timeenc,
            freq=freq,
            test_size = args.test_size,
            kind_of_scaler=args.kind_of_scaler,
            name_of_col_with_date = args.name_of_col_with_date,
            scale = args.scale,
        )
        print(flag, len(data_set))
    data_loader = DataLoader(
        data_set,
        batch_size=batch_size,
        shuffle=shuffle_flag,
        num_workers=args.num_workers,
        drop_last=drop_last)
    
    return data_set, data_loader
