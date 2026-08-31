from deploy import load_model


model = None
device = None


def load_model_service(checkpoint_path):
    global model
    global device
    if model is None or device is None:
        model, device = load_model.load_model_device(checkpoint_path)

    return model, device