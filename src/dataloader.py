from torch.utils.data import DataLoader


def create_dataloader(dataset,batch_size,shuffle=True):
    loader = DataLoader(
        dataset=dataset,
        batch_size=batch_size,
        shuffle=shuffle,
        num_workers=0
    )

    return loader